#!/usr/bin/env python3
"""
Map-frame sound localizer based on the "Steam Leak Localization Algorithm".

Inputs:
- /leak_detected (std_msgs/Bool)
- /doa_angle (std_msgs/Int32): bearing in base_link, degrees [0, 360)

Outputs:
- /sound_localizer/estimate_valid (std_msgs/Bool)
- /sound_localizer/estimate_stable (std_msgs/Bool)
- /sound_localizer/current_estimate (geometry_msgs/PoseStamped)
- /sound_localizer/estimated_locations (geometry_msgs/PoseArray)
- /sound_localizer/approach_waypoints (geometry_msgs/PoseArray)
- /sound_localizer/markers (visualization_msgs/MarkerArray)

The node mirrors the paper flow:
1. Convert the ODAS DoA from dog frame to map frame.
2. Intersect the previous and current bearing lines.
3. Optionally generate approach waypoints using the walking-distance rule:
   step = min(0.1 * distance_to_estimate, 1.0)
"""

from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass
from typing import Deque, Optional, Tuple

import rclpy
from geometry_msgs.msg import Point, Pose, PoseArray, PoseStamped
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.time import Time
from std_msgs.msg import Bool, Int32
from tf2_ros import Buffer, TransformException, TransformListener
from visualization_msgs.msg import Marker, MarkerArray


EPS = 1.0e-9


@dataclass(frozen=True)
class RobotPose2D:
    x: float
    y: float
    yaw: float


@dataclass(frozen=True)
class Measurement:
    x_map: float
    y_map: float
    yaw_map: float
    doa_base_rad: float
    doa_map_rad: float
    doa_msg_ns: int

    def baseline_to(self, other: "Measurement") -> float:
        return math.hypot(self.x_map - other.x_map, self.y_map - other.y_map)


@dataclass(frozen=True)
class EstimateSample:
    x_map: float
    y_map: float
    baseline_m: float
    bearing_separation_rad: float


def wrap_pi(angle_rad: float) -> float:
    return math.atan2(math.sin(angle_rad), math.cos(angle_rad))


def angle_diff_rad(a_rad: float, b_rad: float) -> float:
    return abs(wrap_pi(a_rad - b_rad))


def yaw_from_quaternion(q) -> float:
    siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny_cosp, cosy_cosp)


def pose_with_yaw(x: float, y: float, yaw: float) -> Pose:
    pose = Pose()
    pose.position.x = float(x)
    pose.position.y = float(y)
    pose.position.z = 0.0
    pose.orientation.z = math.sin(yaw / 2.0)
    pose.orientation.w = math.cos(yaw / 2.0)
    return pose


def point_xy(x: float, y: float, z: float = 0.05) -> Point:
    point = Point()
    point.x = float(x)
    point.y = float(y)
    point.z = float(z)
    return point


class SoundLocalizer(Node):
    def __init__(self) -> None:
        super().__init__("sound_localizer")

        self.map_frame = str(self.declare_parameter("map_frame", "map").value)
        self.base_frame = str(self.declare_parameter("base_frame", "base_link").value)
        self.leak_topic = str(self.declare_parameter("leak_topic", "/leak_detected").value)
        self.doa_topic = str(self.declare_parameter("doa_topic", "/doa_angle").value)
        self.sample_period_s = float(self.declare_parameter("sample_period_s", 0.25).value)
        self.doa_timeout_s = float(self.declare_parameter("doa_timeout_s", 1.0).value)
        self.min_baseline_m = float(self.declare_parameter("min_baseline_m", 0.10).value)
        self.min_bearing_separation_deg = float(
            self.declare_parameter("min_bearing_separation_deg", 5.0).value
        )
        self.stable_min_baseline_m = float(
            self.declare_parameter("stable_min_baseline_m", 0.50).value
        )
        self.stable_min_bearing_separation_deg = float(
            self.declare_parameter("stable_min_bearing_separation_deg", 10.0).value
        )
        self.stable_required_consecutive_estimates = max(
            1,
            int(
                self.declare_parameter(
                    "stable_required_consecutive_estimates", 3
                ).value
            ),
        )
        self.stable_centroid_radius_m = float(
            self.declare_parameter("stable_centroid_radius_m", 0.20).value
        )
        self.stable_max_doa_age_s = float(
            self.declare_parameter("stable_max_doa_age_s", 1.0).value
        )
        self.parallel_tan_epsilon = float(
            self.declare_parameter("parallel_tan_epsilon", 1.0e-6).value
        )
        self.intersection_method = str(
            self.declare_parameter("intersection_method", "geometric").value
        ).strip().lower()
        self.use_absolute_x_positions = bool(
            self.declare_parameter("use_absolute_x_positions", False).value
        )
        self.measurement_history_size = max(
            2, int(self.declare_parameter("measurement_history_size", 20).value)
        )
        self.estimate_history_size = max(
            self.stable_required_consecutive_estimates,
            int(self.declare_parameter("estimate_history_size", 10).value),
        )
        self.marker_topic = str(
            self.declare_parameter("marker_topic", "/sound_localizer/markers").value
        )
        self.publish_markers = bool(
            self.declare_parameter("publish_markers", True).value
        )
        self.publish_waypoints = bool(
            self.declare_parameter("publish_waypoints", False).value
        )
        self.num_waypoints = max(0, int(self.declare_parameter("num_waypoints", 0).value))
        self.max_step_m = float(self.declare_parameter("max_step_m", 1.0).value)
        self.step_gain = float(self.declare_parameter("step_gain", 0.10).value)
        self.goal_tolerance_m = float(self.declare_parameter("goal_tolerance_m", 0.25).value)
        self.enable_reasonableness_filter = bool(
            self.declare_parameter("enable_reasonableness_filter", False).value
        )
        self.max_estimate_distance_m = float(
            self.declare_parameter("max_estimate_distance_m", 50.0).value
        )
        self.marker_ray_length_m = float(
            self.declare_parameter("marker_ray_length_m", 2.0).value
        )

        if self.intersection_method not in ("geometric", "paper"):
            self.get_logger().warn(
                f'Unknown intersection_method="{self.intersection_method}". '
                'Falling back to "geometric".'
            )
            self.intersection_method = "geometric"

        self.min_bearing_separation_rad = math.radians(self.min_bearing_separation_deg)
        self.stable_min_bearing_separation_rad = math.radians(
            self.stable_min_bearing_separation_deg
        )
        self._tf_buffer = Buffer(cache_time=Duration(seconds=10.0))
        self._tf_listener = TransformListener(self._tf_buffer, self)

        self._leak_detected = False
        self._last_doa_rad: Optional[float] = None
        self._last_doa_stamp: Optional[Time] = None

        self._measurements: Deque[Measurement] = deque(maxlen=self.measurement_history_size)
        self._estimate_history: Deque[EstimateSample] = deque(maxlen=self.estimate_history_size)
        self._latest_estimate: Optional[Tuple[float, float]] = None
        self._estimate_stable = False
        self._estimate_locked = False
        self._last_pair: Optional[Tuple[Measurement, Measurement]] = None

        self._warn_times_ns: dict[str, int] = {}

        self.estimate_valid_pub = self.create_publisher(
            Bool, "/sound_localizer/estimate_valid", 10
        )
        self.estimate_stable_pub = self.create_publisher(
            Bool, "/sound_localizer/estimate_stable", 10
        )
        self.current_estimate_pub = self.create_publisher(
            PoseStamped, "/sound_localizer/current_estimate", 10
        )
        self.estimate_history_pub = self.create_publisher(
            PoseArray, "/sound_localizer/estimated_locations", 10
        )
        self.waypoints_pub = self.create_publisher(
            PoseArray, "/sound_localizer/approach_waypoints", 10
        )
        self.marker_pub = self.create_publisher(
            MarkerArray, self.marker_topic, 10
        )

        self.create_subscription(Bool, self.leak_topic, self._leak_cb, 10)
        self.create_subscription(Int32, self.doa_topic, self._doa_cb, 10)
        self.create_timer(self.sample_period_s, self._timer_cb)

        self._publish_valid(False)
        self._publish_stable(False)
        self._publish_empty_arrays()
        self._clear_markers()
        self.get_logger().info(
            "Sound localizer started: "
            f"leak_topic={self.leak_topic}, doa_topic={self.doa_topic}, "
            f"map_frame={self.map_frame}, base_frame={self.base_frame}, "
            f"marker_topic={self.marker_topic}, "
            f"intersection_method={self.intersection_method}, "
            f"publish_waypoints={self.publish_waypoints}, "
            f"num_waypoints={self.num_waypoints}, "
            f"min_baseline_m={self.min_baseline_m:.2f}, "
            f"stable_min_baseline_m={self.stable_min_baseline_m:.2f}, "
            f"stable_required_consecutive_estimates={self.stable_required_consecutive_estimates}"
        )

    def _warn_throttled(self, key: str, message: str, period_s: float = 5.0) -> None:
        now_ns = self.get_clock().now().nanoseconds
        last_ns = self._warn_times_ns.get(key, 0)
        if (now_ns - last_ns) >= int(period_s * 1.0e9):
            self._warn_times_ns[key] = now_ns
            self.get_logger().warn(message)

    def _publish_valid(self, is_valid: bool) -> None:
        self.estimate_valid_pub.publish(Bool(data=bool(is_valid)))

    def _publish_stable(self, is_stable: bool) -> None:
        self.estimate_stable_pub.publish(Bool(data=bool(is_stable)))

    def _publish_empty_arrays(self) -> None:
        stamp = self.get_clock().now().to_msg()

        empty_estimates = PoseArray()
        empty_estimates.header.stamp = stamp
        empty_estimates.header.frame_id = self.map_frame
        self.estimate_history_pub.publish(empty_estimates)

        empty_waypoints = PoseArray()
        empty_waypoints.header.stamp = stamp
        empty_waypoints.header.frame_id = self.map_frame
        self.waypoints_pub.publish(empty_waypoints)

    def _clear_markers(self) -> None:
        if not self.publish_markers:
            return

        delete_all = Marker()
        delete_all.action = Marker.DELETEALL

        marker_array = MarkerArray()
        marker_array.markers.append(delete_all)
        self.marker_pub.publish(marker_array)

    def _reset_session(self, reason: str) -> None:
        self._measurements.clear()
        self._estimate_history.clear()
        self._latest_estimate = None
        self._estimate_stable = False
        self._estimate_locked = False
        self._last_pair = None
        self._publish_valid(False)
        self._publish_stable(False)
        self._publish_empty_arrays()
        self._clear_markers()
        self.get_logger().info(f"Reset sound-localization session: {reason}")

    def _lock_stable_estimate(self) -> None:
        if self._estimate_locked or self._latest_estimate is None:
            return

        self._estimate_locked = True
        self._estimate_stable = True
        self._publish_stable(True)
        self.get_logger().info(
            "Locked stable sound estimate after "
            f"{self.stable_required_consecutive_estimates} consecutive matching estimates. "
            "Stopping new sound measurements."
        )

    def _publish_markers(self, robot_pose: RobotPose2D) -> None:
        if not self.publish_markers or self._latest_estimate is None:
            return

        est_x, est_y = self._latest_estimate
        stamp = self.get_clock().now().to_msg()
        markers = MarkerArray()

        estimate_marker = Marker()
        estimate_marker.header.frame_id = self.map_frame
        estimate_marker.header.stamp = stamp
        estimate_marker.ns = "sound_localizer"
        estimate_marker.id = 0
        estimate_marker.type = Marker.SPHERE
        estimate_marker.action = Marker.ADD
        estimate_marker.pose = pose_with_yaw(est_x, est_y, 0.0)
        estimate_marker.scale.x = 0.35
        estimate_marker.scale.y = 0.35
        estimate_marker.scale.z = 0.35
        estimate_marker.color.r = 1.0
        estimate_marker.color.g = 0.35
        estimate_marker.color.b = 0.10
        estimate_marker.color.a = 1.0 if self._estimate_locked else 0.55
        markers.markers.append(estimate_marker)

        robot_path_marker = Marker()
        robot_path_marker.header.frame_id = self.map_frame
        robot_path_marker.header.stamp = stamp
        robot_path_marker.ns = "sound_localizer"
        robot_path_marker.id = 1
        robot_path_marker.type = Marker.LINE_STRIP
        robot_path_marker.action = Marker.ADD
        robot_path_marker.pose.orientation.w = 1.0
        robot_path_marker.scale.x = 0.05
        robot_path_marker.color.r = 0.15
        robot_path_marker.color.g = 0.95
        robot_path_marker.color.b = 0.30
        robot_path_marker.color.a = 0.90
        robot_path_marker.points = [
            point_xy(meas.x_map, meas.y_map, z=0.03) for meas in self._measurements
        ]
        if len(robot_path_marker.points) == 1:
            robot_path_marker.points.append(
                point_xy(self._measurements[0].x_map, self._measurements[0].y_map, z=0.03)
            )
        markers.markers.append(robot_path_marker)

        estimate_trail_marker = Marker()
        estimate_trail_marker.header.frame_id = self.map_frame
        estimate_trail_marker.header.stamp = stamp
        estimate_trail_marker.ns = "sound_localizer"
        estimate_trail_marker.id = 2
        estimate_trail_marker.type = Marker.LINE_STRIP
        estimate_trail_marker.action = Marker.ADD
        estimate_trail_marker.pose.orientation.w = 1.0
        estimate_trail_marker.scale.x = 0.06
        estimate_trail_marker.color.r = 0.10
        estimate_trail_marker.color.g = 0.90
        estimate_trail_marker.color.b = 1.00
        estimate_trail_marker.color.a = 0.85
        estimate_trail_marker.points = [
            point_xy(sample.x_map, sample.y_map) for sample in self._estimate_history
        ]
        if len(estimate_trail_marker.points) == 1:
            estimate_trail_marker.points.append(point_xy(est_x, est_y))
        markers.markers.append(estimate_trail_marker)

        link_marker = Marker()
        link_marker.header.frame_id = self.map_frame
        link_marker.header.stamp = stamp
        link_marker.ns = "sound_localizer"
        link_marker.id = 3
        link_marker.type = Marker.LINE_STRIP
        link_marker.action = Marker.ADD
        link_marker.pose.orientation.w = 1.0
        link_marker.scale.x = 0.04
        link_marker.color.r = 1.00
        link_marker.color.g = 0.95
        link_marker.color.b = 0.20
        link_marker.color.a = 0.90
        link_marker.points = [
            point_xy(robot_pose.x, robot_pose.y, z=0.08),
            point_xy(est_x, est_y, z=0.08),
        ]
        markers.markers.append(link_marker)

        ray_specs = (
            (4, 0.95, 0.25, 0.25),
            (5, 0.35, 0.55, 1.00),
        )
        if self._last_pair is not None:
            for (marker_id, red, green, blue), measurement in zip(ray_specs, self._last_pair):
                ray_marker = Marker()
                ray_marker.header.frame_id = self.map_frame
                ray_marker.header.stamp = stamp
                ray_marker.ns = "sound_localizer"
                ray_marker.id = marker_id
                ray_marker.type = Marker.LINE_STRIP
                ray_marker.action = Marker.ADD
                ray_marker.pose.orientation.w = 1.0
                ray_marker.scale.x = 0.035
                ray_marker.color.r = red
                ray_marker.color.g = green
                ray_marker.color.b = blue
                ray_marker.color.a = 0.90
                ray_marker.points = [
                    point_xy(measurement.x_map, measurement.y_map, z=0.06),
                    point_xy(
                        measurement.x_map + self.marker_ray_length_m * math.cos(measurement.doa_map_rad),
                        measurement.y_map + self.marker_ray_length_m * math.sin(measurement.doa_map_rad),
                        z=0.06,
                    ),
                ]
                markers.markers.append(ray_marker)
        else:
            for marker_id, _, _, _ in ray_specs:
                ray_marker = Marker()
                ray_marker.header.frame_id = self.map_frame
                ray_marker.header.stamp = stamp
                ray_marker.ns = "sound_localizer"
                ray_marker.id = marker_id
                ray_marker.action = Marker.DELETE
                markers.markers.append(ray_marker)

        self.marker_pub.publish(markers)

    def _leak_cb(self, msg: Bool) -> None:
        detected = bool(msg.data)
        if detected and not self._leak_detected:
            self._reset_session("new leak event")
        self._leak_detected = detected

    def _doa_cb(self, msg: Int32) -> None:
        doa_deg = float(msg.data) % 360.0
        self._last_doa_rad = math.radians(doa_deg)
        self._last_doa_stamp = self.get_clock().now()

    def _lookup_robot_pose(self) -> Optional[RobotPose2D]:
        try:
            tf_msg = self._tf_buffer.lookup_transform(
                self.map_frame,
                self.base_frame,
                Time(),
            )
        except TransformException as exc:
            self._warn_throttled(
                "tf_lookup",
                f"TF lookup {self.map_frame}->{self.base_frame} failed: {exc}",
            )
            return None

        tx = tf_msg.transform.translation
        yaw = yaw_from_quaternion(tf_msg.transform.rotation)
        return RobotPose2D(x=float(tx.x), y=float(tx.y), yaw=yaw)

    def _build_measurement(self, robot_pose: RobotPose2D) -> Optional[Measurement]:
        if self._last_doa_rad is None or self._last_doa_stamp is None:
            return None

        age_s = (self.get_clock().now() - self._last_doa_stamp).nanoseconds / 1.0e9
        if age_s > self.doa_timeout_s:
            return None

        # Paper equation (1): w_L/I = w_L/D - w_I/D.
        # Since w_I/D = -yaw_D/I in ROS, this becomes global_bearing = yaw + doa.
        doa_map_rad = wrap_pi(robot_pose.yaw + self._last_doa_rad)
        return Measurement(
            x_map=robot_pose.x,
            y_map=robot_pose.y,
            yaw_map=robot_pose.yaw,
            doa_base_rad=self._last_doa_rad,
            doa_map_rad=doa_map_rad,
            doa_msg_ns=self._last_doa_stamp.nanoseconds,
        )

    def _select_measurement_pair(self) -> Optional[Tuple[Measurement, Measurement]]:
        if len(self._measurements) < 2:
            return None

        current = self._measurements[-1]
        best_previous: Optional[Measurement] = None
        best_baseline = -1.0

        for previous in reversed(tuple(self._measurements)[:-1]):
            baseline = current.baseline_to(previous)
            if baseline < self.min_baseline_m:
                continue
            if angle_diff_rad(current.doa_map_rad, previous.doa_map_rad) < self.min_bearing_separation_rad:
                continue
            if baseline > best_baseline:
                best_baseline = baseline
                best_previous = previous

        if best_previous is None:
            return None

        return best_previous, current

    def _paper_lines_crossing_point(
        self, previous: Measurement, current: Measurement
    ) -> Tuple[float, float]:
        # This mirrors the MATLAB helper supplied by the user/paper.
        x1 = abs(previous.x_map) if self.use_absolute_x_positions else previous.x_map
        x2 = abs(current.x_map) if self.use_absolute_x_positions else current.x_map
        y1 = previous.y_map
        y2 = current.y_map
        tan1 = math.tan(previous.doa_map_rad)
        tan2 = math.tan(current.doa_map_rad)
        denom = tan1 - tan2

        if abs(denom) < self.parallel_tan_epsilon:
            raise ValueError("Bearing lines are nearly parallel.")

        x_map = (y2 - y1 + x2 * tan2 - x1 * tan1) / denom
        y_map = (tan1 * x_map) + y1 + (x1 * tan1)

        if math.isfinite(x_map) and math.isfinite(y_map):
            return float(x_map), float(y_map)

        return self._geometric_line_intersection(previous, current)

    @staticmethod
    def _geometric_line_intersection(
        previous: Measurement, current: Measurement
    ) -> Tuple[float, float]:
        p_x, p_y = previous.x_map, previous.y_map
        q_x, q_y = current.x_map, current.y_map
        r_x = math.cos(previous.doa_map_rad)
        r_y = math.sin(previous.doa_map_rad)
        s_x = math.cos(current.doa_map_rad)
        s_y = math.sin(current.doa_map_rad)

        denom = (r_x * s_y) - (r_y * s_x)
        if abs(denom) < EPS:
            raise ValueError("Bearing lines are parallel in fallback solver.")

        qp_x = q_x - p_x
        qp_y = q_y - p_y
        t = ((qp_x * s_y) - (qp_y * s_x)) / denom
        return (p_x + t * r_x, p_y + t * r_y)

    def _intersect_measurements(
        self, previous: Measurement, current: Measurement
    ) -> Tuple[float, float]:
        if self.intersection_method == "paper":
            return self._paper_lines_crossing_point(previous, current)
        return self._geometric_line_intersection(previous, current)

    def _estimate_is_reasonable(
        self,
        estimate_xy: Tuple[float, float],
        previous: Measurement,
        current: Measurement,
    ) -> bool:
        if not self.enable_reasonableness_filter:
            return True

        est_x, est_y = estimate_xy
        dist_prev = math.hypot(est_x - previous.x_map, est_y - previous.y_map)
        dist_curr = math.hypot(est_x - current.x_map, est_y - current.y_map)
        max_dist = max(dist_prev, dist_curr)
        if max_dist > self.max_estimate_distance_m:
            self._warn_throttled(
                "estimate_distance",
                "Rejected sound estimate because it is too far away: "
                f"{max_dist:.2f} m > {self.max_estimate_distance_m:.2f} m",
                period_s=2.0,
            )
            return False
        return True

    def _latest_doa_age_s(self) -> Optional[float]:
        if self._last_doa_stamp is None:
            return None
        return (self.get_clock().now() - self._last_doa_stamp).nanoseconds / 1.0e9

    def _evaluate_stability(self) -> tuple[bool, str]:
        if not self._leak_detected:
            return False, "leak_not_latched"

        doa_age_s = self._latest_doa_age_s()
        if doa_age_s is None:
            return False, "missing_doa"
        if doa_age_s > self.stable_max_doa_age_s:
            return False, f"doa_stale:{doa_age_s:.2f}s"

        if len(self._estimate_history) < self.stable_required_consecutive_estimates:
            return False, "need_more_estimates"

        recent_samples = list(self._estimate_history)[-self.stable_required_consecutive_estimates :]
        min_baseline_m = min(sample.baseline_m for sample in recent_samples)
        if min_baseline_m < self.stable_min_baseline_m:
            return False, f"baseline_too_small:{min_baseline_m:.2f}m"

        min_bearing_sep_rad = min(
            sample.bearing_separation_rad for sample in recent_samples
        )
        if min_bearing_sep_rad < self.stable_min_bearing_separation_rad:
            return False, (
                f"bearing_separation_too_small:{math.degrees(min_bearing_sep_rad):.1f}deg"
            )

        centroid_x = sum(sample.x_map for sample in recent_samples) / len(recent_samples)
        centroid_y = sum(sample.y_map for sample in recent_samples) / len(recent_samples)
        max_spread_m = max(
            math.hypot(sample.x_map - centroid_x, sample.y_map - centroid_y)
            for sample in recent_samples
        )
        if max_spread_m > self.stable_centroid_radius_m:
            return False, f"estimate_spread_too_large:{max_spread_m:.2f}m"

        return True, "stable"

    def _update_stability_state(self) -> str:
        if self._estimate_locked:
            self._estimate_stable = True
            self._publish_stable(True)
            return "locked"

        is_stable, reason = self._evaluate_stability()
        if is_stable != self._estimate_stable:
            if is_stable:
                self.get_logger().info(
                    "Sound estimate became stable: "
                    f"reason={reason}, required_estimates={self.stable_required_consecutive_estimates}, "
                    f"centroid_radius_m={self.stable_centroid_radius_m:.2f}"
                )
            else:
                self.get_logger().warn(
                    "Sound estimate is no longer stable: "
                    f"reason={reason}"
                )
        self._estimate_stable = is_stable
        self._publish_stable(is_stable)
        return reason

    def _generate_waypoints(
        self, robot_pose: RobotPose2D, estimate_xy: Tuple[float, float]
    ) -> PoseArray:
        est_x, est_y = estimate_xy
        pose_array = PoseArray()
        pose_array.header.stamp = self.get_clock().now().to_msg()
        pose_array.header.frame_id = self.map_frame

        if not self.publish_waypoints or self.num_waypoints <= 0:
            return pose_array

        wp_x = robot_pose.x
        wp_y = robot_pose.y

        for _ in range(self.num_waypoints):
            rel_x = est_x - wp_x
            rel_y = est_y - wp_y
            distance_to_estimate = math.hypot(rel_x, rel_y)
            if distance_to_estimate <= self.goal_tolerance_m:
                break

            # Paper equation (8): L_i = (1/10) * ||X_L/D_i||_2, step = min(L_i, 1 m).
            walk_distance = min(self.step_gain * distance_to_estimate, self.max_step_m)
            if walk_distance <= EPS:
                break

            wp_x += walk_distance * (rel_x / distance_to_estimate)
            wp_y += walk_distance * (rel_y / distance_to_estimate)
            yaw = math.atan2(est_y - wp_y, est_x - wp_x)
            pose_array.poses.append(pose_with_yaw(wp_x, wp_y, yaw))

        return pose_array

    def _publish_outputs(self, robot_pose: RobotPose2D) -> None:
        if self._latest_estimate is None:
            return

        est_x, est_y = self._latest_estimate
        stamp = self.get_clock().now().to_msg()

        estimate_msg = PoseStamped()
        estimate_msg.header.stamp = stamp
        estimate_msg.header.frame_id = self.map_frame
        estimate_msg.pose = pose_with_yaw(est_x, est_y, 0.0)
        self.current_estimate_pub.publish(estimate_msg)

        history_msg = PoseArray()
        history_msg.header.stamp = stamp
        history_msg.header.frame_id = self.map_frame
        history_msg.poses = [
            pose_with_yaw(sample.x_map, sample.y_map, 0.0)
            for sample in self._estimate_history
        ]
        self.estimate_history_pub.publish(history_msg)

        self.waypoints_pub.publish(self._generate_waypoints(robot_pose, self._latest_estimate))
        self._publish_markers(robot_pose)
        self._publish_valid(True)
        self._publish_stable(self._estimate_stable)

    def _timer_cb(self) -> None:
        robot_pose = self._lookup_robot_pose()
        if robot_pose is not None and self._latest_estimate is not None:
            stability_reason = self._update_stability_state()
            if stability_reason == "stable":
                self._lock_stable_estimate()
            elif not self._estimate_locked:
                # Surface the live blocker even when no new estimate is being
                # produced (e.g. insufficient baseline movement / stale DoA), so a
                # stuck localization is diagnosable from the logs.
                self._warn_throttled(
                    "stability_blocked",
                    "Leak estimate not yet stable: "
                    f"reason={stability_reason} (need "
                    f"{self.stable_required_consecutive_estimates} consecutive "
                    f"estimates with baseline>={self.stable_min_baseline_m:.2f}m, "
                    f"bearing_sep>={self.stable_min_bearing_separation_deg:.0f}deg, "
                    f"spread<={self.stable_centroid_radius_m:.2f}m).",
                    5.0,
                )
            self._publish_outputs(robot_pose)

        if not self._leak_detected:
            return
        if robot_pose is None:
            return
        if self._estimate_locked:
            return

        current_measurement = self._build_measurement(robot_pose)
        if current_measurement is None:
            return

        if self._measurements:
            last_measurement = self._measurements[-1]
            if current_measurement.doa_msg_ns <= last_measurement.doa_msg_ns:
                return
            if current_measurement.baseline_to(last_measurement) < self.min_baseline_m:
                return

        self._measurements.append(current_measurement)

        if len(self._measurements) == 1:
            self.get_logger().info(
                "Recorded first sound bearing at "
                f"({current_measurement.x_map:.2f}, {current_measurement.y_map:.2f})"
            )
            return

        pair = self._select_measurement_pair()
        if pair is None:
            return

        previous, current = pair
        try:
            estimate_xy = self._intersect_measurements(previous, current)
        except ValueError as exc:
            self._warn_throttled("parallel_lines", f"Skipping estimate update: {exc}", 2.0)
            return

        if not self._estimate_is_reasonable(estimate_xy, previous, current):
            return

        baseline_m = current.baseline_to(previous)
        bearing_separation_rad = angle_diff_rad(
            current.doa_map_rad, previous.doa_map_rad
        )
        self._last_pair = (previous, current)
        self._latest_estimate = estimate_xy
        self._estimate_history.append(
            EstimateSample(
                x_map=estimate_xy[0],
                y_map=estimate_xy[1],
                baseline_m=baseline_m,
                bearing_separation_rad=bearing_separation_rad,
            )
        )
        stability_reason = self._update_stability_state()
        if stability_reason == "stable":
            self._lock_stable_estimate()
        self._publish_outputs(robot_pose)

        est_x, est_y = estimate_xy
        self.get_logger().info(
            "Updated sound estimate in map frame: "
            f"x={est_x:.2f}, y={est_y:.2f}, "
            f"baseline={baseline_m:.2f} m, "
            f"bearing_separation={math.degrees(bearing_separation_rad):.1f} deg, "
            f"stable={self._estimate_stable}, reason={stability_reason}, "
            f"bearings=({math.degrees(previous.doa_map_rad):.1f}, "
            f"{math.degrees(current.doa_map_rad):.1f}) deg"
        )


def main(args=None) -> None:
    rclpy.init(args=args)
    node = SoundLocalizer()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
