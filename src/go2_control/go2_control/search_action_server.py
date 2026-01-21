#!/usr/bin/env python3
# Leak-search Action Server
# Two-point triangulation using global costmap (Nav2) + DoA angle
#
# Robot Operating System (ROS 2) Humble

import math
import time
from dataclasses import dataclass
from typing import Optional, Tuple, List

import numpy as np

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.duration import Duration

from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from std_msgs.msg import Bool, Int32
from visualization_msgs.msg import Marker
from nav2_msgs.msg import Costmap

from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import tf2_ros

from go2_interfaces.action import Search

# ---------------- Parameters (tune here) ----------------

# Microphone "reach" (for single-bearing fallback)
MIC_RADIUS_M = 10.0

# Lateral step distance candidates from current pose
STEP_RADII_M = [3.0, 2.0, 1.0]

# Perpendicular search sweep (deg) around exact perpendicular
SWEEP_OFFSETS_DEG = [0.0, 15.0, -15.0, 30.0, -30.0, 45.0, -45.0]

# Max Nav2 attempts to reach a lateral waypoint
MAX_NAV_ATTEMPTS = 4

# Time to listen for DoA angles at each vantage (seconds)
BEARING_TIMEOUT_S = 15.0

# Free-space cost threshold for global costmap
#  - 0 = free, >=254 = lethal/obstacle, 255 = unknown in costmap_2d
FREE_COST_THRESHOLD = 10

# Input topics
DETECT_TOPIC  = '/leak_detected'
BEARING_TOPIC = '/doa_angle'  # Int32 degrees [0,360), CCW in base_link

# Output topics
EST_TOPIC     = '/leak_estimate'
MARKER_TOPIC  = 'visualization_marker'

# Marker radius (for visualization)
ROI_RADIUS_M  = 1.0
# --------------------------------------------------------


@dataclass
class BearingMeasurement:
    x: float
    y: float
    phi: float   # global bearing angle in map frame


class LeakSearchServer(Node):
    def __init__(self):
        super().__init__('leak_search_server')

        # Action server
        self._as = ActionServer(
            self,
            Search,
            'search',
            execute_callback=self.execute_cb,
            goal_callback=self.goal_cb,
            cancel_callback=self.cancel_cb,
        )

        # Nav2 helper + TF
        self.navigator = BasicNavigator()
        self.tfbuf = tf2_ros.Buffer(cache_time=Duration(seconds=10.0))
        self.tflistener = tf2_ros.TransformListener(self.tfbuf, self)

        # Subscribed state
        self._det: bool = False
        self._last_bearing: Optional[float] = None  # radians in base_link

        self.create_subscription(Bool,  DETECT_TOPIC,  self._det_cb, 10)
        self.create_subscription(Int32, BEARING_TOPIC, self._bearing_cb, 10)

        # Publishers
        self.est_pub    = self.create_publisher(PoseWithCovarianceStamped, EST_TOPIC, 10)
        self.marker_pub = self.create_publisher(Marker, MARKER_TOPIC, 10)

    # --------- ROS 2 action plumbing ----------
    def goal_cb(self, goal_req: Search.Goal):
        self.get_logger().info('Search goal received.')
        return GoalResponse.ACCEPT

    def cancel_cb(self, goal_handle):
        self.get_logger().info('Search cancel requested.')
        return CancelResponse.ACCEPT

    # ---------- Subscribers ----------
    def _det_cb(self, msg: Bool):
        self._det = bool(msg.data)

    def _bearing_cb(self, msg: Int32):
        """Device gives angle in degrees [0, 360), CCW, in base_link frame."""
        deg = float(msg.data)
        rad = math.radians(deg)
        # Wrap into [-pi, pi]
        rad_wrapped = math.atan2(math.sin(rad), math.cos(rad))
        self._last_bearing = rad_wrapped
        # Debug if needed:
        # self.get_logger().info(f"DoA callback: {deg:.1f} deg -> {rad_wrapped:.3f} rad")

    # ---------- Small helpers ----------
    @staticmethod
    def _wrap_pi(angle: float) -> float:
        """Wrap angle to [-pi, pi]."""
        return math.atan2(math.sin(angle), math.cos(angle))

    # ---------- TF helpers ----------
    def _get_robot_pose_map(self) -> Optional[Tuple[float, float, float]]:
        """Return (x,y,yaw) of base_link in map frame."""
        try:
            tf = self.tfbuf.lookup_transform('map', 'base_link', rclpy.time.Time())
            tx = tf.transform.translation
            q  = tf.transform.rotation
            siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
            cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
            yaw = math.atan2(siny_cosp, cosy_cosp)
            return (tx.x, tx.y, yaw)
        except Exception as e:
            self.get_logger().warn(f'TF lookup map->base_link failed: {e}')
            return None

    # ---------- Costmap helpers ----------
    def _world_to_costmap_index(self, costmap: Costmap,
                                x_map: float, y_map: float) -> Optional[int]:
        """Project a map-frame (x,y) into global costmap index, if in bounds."""
        res    = costmap.metadata.resolution
        size_x = int(costmap.metadata.size_x)
        size_y = int(costmap.metadata.size_y)
        origin = costmap.metadata.origin.position

        ix = int((x_map - origin.x) / res)
        iy = int((y_map - origin.y) / res)
        if ix < 0 or iy < 0 or ix >= size_x or iy >= size_y:
            return None

        return iy * size_x + ix

    def _is_free_in_costmap(self, costmap: Costmap,
                            x_map: float, y_map: float) -> bool:
        """Return True if costmap cell is considered free."""
        idx = self._world_to_costmap_index(costmap, x_map, y_map)
        if idx is None:
            return False
        cost = costmap.data[idx]
        # 255 = unknown, >=254 = lethal in costmap_2d; treat anything low as free
        if cost == 255 or cost >= 254:
            return False
        return cost <= FREE_COST_THRESHOLD

    def _generate_lateral_candidates(self,
                                     x0: float, y0: float,
                                     phi0_global: float,
                                     costmap: Costmap) -> List[PoseStamped]:
        """Generate candidate lateral waypoints in free space around current pose.

        - Perpendicular to sound direction, +/-45° sweep.
        - Radii: 3m, then 2m, then 1m.
        """
        candidates: List[PoseStamped] = []

        # Left (+90°) and right (-90°) perpendicular bases
        sides = [+1.0, -1.0]  # +1 => left, -1 => right

        for radius in STEP_RADII_M:
            for side in sides:
                base_perp = phi0_global + side * (math.pi / 2.0)
                for off_deg in SWEEP_OFFSETS_DEG:
                    theta = base_perp + math.radians(off_deg)
                    cx = x0 + radius * math.cos(theta)
                    cy = y0 + radius * math.sin(theta)

                    if not self._is_free_in_costmap(costmap, cx, cy):
                        continue

                    ps = PoseStamped()
                    ps.header.frame_id = 'map'
                    ps.header.stamp    = self.get_clock().now().to_msg()
                    ps.pose.position.x = cx
                    ps.pose.position.y = cy
                    ps.pose.position.z = 0.0
                    # Orient the robot along the travel direction for this waypoint
                    ps.pose.orientation.z = math.sin(theta / 2.0)
                    ps.pose.orientation.w = math.cos(theta / 2.0)

                    candidates.append(ps)

            # If we found any free positions at this radius, stop; we prefer larger baselines
            if candidates:
                break

        return candidates

    # ---------- Path feasibility helper ----------
    def _has_valid_global_path(self,
                               start: PoseStamped,
                               goal: PoseStamped) -> bool:
        """Use Nav2 global planner (via BasicNavigator.getPath) to pre-check reachability."""
        try:
            path = self.navigator.getPath(start, goal)
        except Exception as e:
            self.get_logger().warn(f"getPath failed for candidate lateral waypoint: {e}")
            return False

        if path is None or len(path.poses) == 0:
            return False

        return True

    # ---------- DoA helpers ----------
    def _wait_for_fresh_bearing(self, timeout_s: float) -> Optional[float]:
        """
        Listen for DoA angles up to timeout_s, while /leak_detected is True,
        and return the circular mean of all angles observed in that window.

        If no angles were seen, return None.
        """
        start = time.time()
        angles: List[float] = []

        while (time.time() - start) < timeout_s and rclpy.ok():
            if self._det and self._last_bearing is not None:
                # Sample current angle; if topic is at 5–10 Hz this will build a nice average
                angles.append(self._last_bearing)
            time.sleep(0.05)

        if not angles:
            return None

        # Circular mean of angles
        s = sum(math.sin(a) for a in angles)
        c = sum(math.cos(a) for a in angles)
        avg = math.atan2(s, c)
        self.get_logger().info(
            f"Averaged {len(angles)} DoA samples -> {avg:.3f} rad"
        )
        return avg

    # ---------- Marker & estimate publishing ----------
    def _publish_marker(self, x: float, y: float, radius: float):
        marker = Marker()
        marker.header.frame_id = 'map'
        marker.header.stamp    = self.get_clock().now().to_msg()
        marker.ns   = 'leak_roi'
        marker.id   = 1
        marker.type = Marker.CYLINDER
        marker.action = Marker.ADD
        marker.pose.position.x = x
        marker.pose.position.y = y
        marker.pose.position.z = 0.0
        marker.pose.orientation.w = 1.0
        marker.scale.x = radius * 2.0
        marker.scale.y = radius * 2.0
        marker.scale.z = 0.05
        marker.color.r = 1.0
        marker.color.g = 0.2
        marker.color.b = 0.2
        marker.color.a = 0.7
        self.marker_pub.publish(marker)

    def _publish_estimate_marker_from_xy(self, mx: float, my: float, std: float):
        self._publish_marker(mx, my, ROI_RADIUS_M)
        msg = PoseWithCovarianceStamped()
        msg.header.frame_id = 'map'
        msg.header.stamp    = self.get_clock().now().to_msg()
        msg.pose.pose.position.x = mx
        msg.pose.pose.position.y = my
        msg.pose.pose.position.z = 0.0
        msg.pose.pose.orientation.w = 1.0
        cov = [0.0] * 36
        cov[0]  = std * std
        cov[7]  = std * std
        cov[35] = 1e-3
        msg.pose.covariance = cov
        self.est_pub.publish(msg)

    # ---------- Geometry: intersection of two bearing lines ----------
    @staticmethod
    def _intersect_two_bearings(m0: BearingMeasurement,
                                m1: BearingMeasurement) -> Tuple[Tuple[float, float], float]:
        """Return LS intersection of two bearing lines (m0, m1)."""
        meas = [m0, m1]
        # LS formulation for N lines (here N=2)
        A = np.zeros((2, 2), dtype=np.float64)
        b = np.zeros((2,), dtype=np.float64)
        for m in meas:
            n = np.array([-math.sin(m.phi), math.cos(m.phi)])
            r = np.array([m.x, m.y])
            Ni = np.outer(n, n)
            A += Ni
            b += Ni @ r

        try:
            p = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            # Degenerate / parallel; fall back to first bearing at MIC_RADIUS_M
            mx = m0.x + MIC_RADIUS_M * math.cos(m0.phi)
            my = m0.y + MIC_RADIUS_M * math.sin(m0.phi)
            return (mx, my), float('inf')

        mx, my = float(p[0]), float(p[1])

        # residual
        res2 = 0.0
        for m in meas:
            n = np.array([-math.sin(m.phi), math.cos(m.phi)])
            r = np.array([m.x, m.y])
            dist = float(n @ (p - r))
            res2 += dist**2
        std = math.sqrt(res2 / max(len(meas), 1))
        return (mx, my), std

    # --------- Execute the Action ----------
    async def execute_cb(self, goal_handle):
        self.get_logger().info('Search started.')

        # 1. Current position in map (first vantage)
        pose0 = self._get_robot_pose_map()
        while pose0 is None and rclpy.ok():
            time.sleep(0.1)
            pose0 = self._get_robot_pose_map()

        if pose0 is None:
            self.get_logger().warn("Cannot get initial map pose; aborting search.")
            goal_handle.abort()
            return Search.Result()

        x0, y0, yaw0 = pose0
        self.get_logger().info(f"Initial pose: ({x0:.2f}, {y0:.2f}), yaw={yaw0:.2f} rad.")

        # 2. Get first DoA (averaged) and build first bearing
        doa0 = self._wait_for_fresh_bearing(BEARING_TIMEOUT_S)
        if doa0 is None:
            self.get_logger().warn("No DoA angle at first vantage; using current spot as leak.")
            self._publish_estimate_marker_from_xy(x0, y0, std=999.0)
            goal_handle.succeed()
            return Search.Result()

        phi0_global = self._wrap_pi(yaw0 + doa0)
        self.get_logger().info(f"First DoA (global): phi0={phi0_global:.2f} rad.")

        # 3. Read global costmap and pick lateral waypoint
        try:
            global_cm: Costmap = self.navigator.getGlobalCostmap()
        except Exception as e:
            self.get_logger().warn(f"Failed to get global costmap: {e}")
            self._publish_estimate_marker_from_xy(x0, y0, std=999.0)
            goal_handle.succeed()
            return Search.Result()

        candidates = self._generate_lateral_candidates(x0, y0, phi0_global, global_cm)
        if not candidates:
            self.get_logger().warn("No lateral free-space waypoint found; using current spot as leak.")
            self._publish_estimate_marker_from_xy(x0, y0, std=999.0)
            goal_handle.succeed()
            return Search.Result()

        # 4. Navigate to a lateral waypoint using Nav2 (BT, recoveries, etc.)
        nav_success = False
        max_tries = min(MAX_NAV_ATTEMPTS, len(candidates))

        for i in range(max_tries):
            cand = candidates[i]

            # Build a start pose for getPath; prefer navigator.getCurrentPose, fallback to TF
            try:
                start_pose = self.navigator.getCurrentPose()
            except Exception:
                start_pose = PoseStamped()
                start_pose.header.frame_id = 'map'
                start_pose.header.stamp    = self.get_clock().now().to_msg()
                start_pose.pose.position.x = x0
                start_pose.pose.position.y = y0
                start_pose.pose.orientation.w = 1.0

            if not self._has_valid_global_path(start_pose, cand):
                self.get_logger().warn(
                    f"Candidate {i+1}/{max_tries} at "
                    f"({cand.pose.position.x:.2f}, {cand.pose.position.y:.2f}) "
                    "has no valid global path; skipping."
                )
                continue

            self.get_logger().info(
                f"Nav attempt {i+1}/{max_tries} "
                f"to lateral waypoint ({cand.pose.position.x:.2f}, {cand.pose.position.y:.2f})."
            )
            self.navigator.goToPose(cand)
            # Let Nav2 do its BT dance
            while not self.navigator.isTaskComplete():
                time.sleep(0.1)
            res = self.navigator.getResult()
            if res == TaskResult.SUCCEEDED:
                self.get_logger().info("Lateral waypoint reached.")
                nav_success = True
                break
            else:
                self.get_logger().warn(f"Lateral nav failed with result={res}; trying another candidate.")

        if not nav_success:
            self.get_logger().warn("All lateral nav attempts failed; using initial spot as leak.")
            self._publish_estimate_marker_from_xy(x0, y0, std=999.0)
            goal_handle.succeed()
            return Search.Result()

        # 5. Second vantage: get updated pose and second DoA
        pose1 = self._get_robot_pose_map()
        if pose1 is None:
            self.get_logger().warn("Cannot get pose at lateral waypoint; using initial spot as leak.")
            self._publish_estimate_marker_from_xy(x0, y0, std=999.0)
            goal_handle.succeed()
            return Search.Result()

        x1, y1, yaw1 = pose1
        self.get_logger().info(f"Second pose: ({x1:.2f}, {y1:.2f}), yaw={yaw1:.2f} rad.")

        doa1 = self._wait_for_fresh_bearing(BEARING_TIMEOUT_S)
        if doa1 is None:
            self.get_logger().warn("No DoA angle at second vantage; using lateral spot as leak.")
            self._publish_estimate_marker_from_xy(x1, y1, std=999.0)
            goal_handle.succeed()
            return Search.Result()

        phi1_global = self._wrap_pi(yaw1 + doa1)
        self.get_logger().info(f"Second DoA (global): phi1={phi1_global:.2f} rad.")

        # 6. Intersection of two lines (triangulation)
        # IMPORTANT: flip bearings by pi here to go from "wave arrival direction"
        # to "line-of-sight toward leak".
        phi0_line = self._wrap_pi(phi0_global + math.pi)
        phi1_line = self._wrap_pi(phi1_global + math.pi)

        m0 = BearingMeasurement(x=x0, y=y0, phi=phi0_line)
        m1 = BearingMeasurement(x=x1, y=y1, phi=phi1_line)
        (mx, my), std = self._intersect_two_bearings(m0, m1)
        self.get_logger().info(
            f"Leak estimate from triangulation: ({mx:.2f}, {my:.2f}), residual std={std:.2f} m."
        )

        # 7. Mark leak on map
        self._publish_estimate_marker_from_xy(mx, my, std=std)

        goal_handle.succeed()
        return Search.Result()


def main():
    rclpy.init()
    node = LeakSearchServer()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
