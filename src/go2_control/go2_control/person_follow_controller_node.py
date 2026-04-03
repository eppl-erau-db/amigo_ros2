#!/usr/bin/env python3
from __future__ import annotations

import math
import time

import rclpy
from geometry_msgs.msg import PointStamped, Twist
from nav_msgs.msg import OccupancyGrid
from rclpy.node import Node
from std_msgs.msg import Bool, String
import tf2_ros

from go2_control.person_follow_controller_core import (
    FollowControlParams,
    FollowStateMachine,
    FollowStates,
    GridMap2D,
    Pose2D,
    SafetyOracleParams,
    Twist2D,
    apply_acceleration_limits,
    compute_nominal_follow_command,
    follow_state_event,
    select_safe_command,
    trajectory_is_safe,
)
from go2_interfaces.msg import RobotModeState


class PersonFollowControllerNode(Node):
    def __init__(self) -> None:
        super().__init__("person_follow_controller_node")

        # Kept for launch compatibility during the transition to supervisor-owned mode.
        self.declare_parameter("command_topic", "/voice/command")
        self.declare_parameter("follow_command_token", "follow_me")
        self.declare_parameter("stop_command_token", "stop_follow")
        self.declare_parameter("stand_up_command_token", "stand_up")
        self.declare_parameter("resume_after_stand_up", True)
        self.declare_parameter("sport_request_topic", "/api/sport/request")

        self.robot_mode_state_topic = str(
            self.declare_parameter("robot_mode_state_topic", "/robot_mode_state").value
        )
        self.target_point_topic = str(
            self.declare_parameter(
                "target_point_topic", "/person_follow_vision_node/target_point"
            ).value
        )
        self.target_visible_topic = str(
            self.declare_parameter(
                "target_visible_topic", "/person_follow_vision_node/target_visible"
            ).value
        )
        self.target_status_topic = str(
            self.declare_parameter(
                "target_status_topic", "/person_follow_vision_node/status"
            ).value
        )
        self.local_costmap_topic = str(
            self.declare_parameter("local_costmap_topic", "/local_costmap/costmap").value
        )
        self.cmd_vel_topic = str(
            self.declare_parameter("cmd_vel_topic", "/motion/candidate/follow").value
        )
        self.base_frame = str(self.declare_parameter("base_frame", "base_footprint").value)
        self.control_frequency_hz = max(
            5.0, float(self.declare_parameter("control_frequency_hz", 20.0).value)
        )
        self.target_timeout_s = max(
            0.1, float(self.declare_parameter("target_timeout_s", 0.8).value)
        )
        self.reacquire_timeout_s = max(
            0.1, float(self.declare_parameter("reacquire_timeout_s", 1.5).value)
        )
        self.sit_on_loss_timeout_s = max(
            self.reacquire_timeout_s,
            float(self.declare_parameter("sit_on_loss_timeout_s", 3.0).value),
        )
        self.reacquire_yaw_rate_radps = max(
            0.05, float(self.declare_parameter("reacquire_yaw_rate_radps", 0.70).value)
        )
        self.debug_enable = bool(self.declare_parameter("debug_enable", False).value)
        self.use_local_costmap_safety = bool(
            self.declare_parameter("use_local_costmap_safety", True).value
        )
        self.allow_yaw_without_costmap = bool(
            self.declare_parameter("allow_yaw_without_costmap", True).value
        )
        self.allow_nominal_without_safety = bool(
            self.declare_parameter("allow_nominal_without_safety", True).value
        )
        self.safety_fallback_linear_speed_mps = max(
            0.0, float(self.declare_parameter("safety_fallback_linear_speed_mps", 0.30).value)
        )
        self.safety_fallback_yaw_rate_radps = max(
            0.0, float(self.declare_parameter("safety_fallback_yaw_rate_radps", 0.80).value)
        )

        self.control_params = FollowControlParams(
            desired_distance_m=float(self.declare_parameter("desired_distance_m", 0.75).value),
            distance_band_m=float(self.declare_parameter("distance_band_m", 0.10).value),
            min_follow_distance_m=float(
                self.declare_parameter("min_follow_distance_m", 0.60).value
            ),
            lateral_deadband_m=float(self.declare_parameter("lateral_deadband_m", 0.10).value),
            yaw_deadband_rad=float(self.declare_parameter("yaw_deadband_rad", 0.10).value),
            forward_gain=float(self.declare_parameter("forward_gain", 0.90).value),
            lateral_gain=float(self.declare_parameter("lateral_gain", 1.10).value),
            yaw_gain=float(self.declare_parameter("yaw_gain", 1.80).value),
            max_forward_speed_mps=float(
                self.declare_parameter("max_forward_speed_mps", 0.60).value
            ),
            max_reverse_speed_mps=float(
                self.declare_parameter("max_reverse_speed_mps", 0.35).value
            ),
            max_lateral_speed_mps=float(
                self.declare_parameter("max_lateral_speed_mps", 0.30).value
            ),
            max_yaw_rate_radps=float(
                self.declare_parameter("max_yaw_rate_radps", 1.20).value
            ),
            yaw_priority_start_rad=float(
                self.declare_parameter("yaw_priority_start_rad", 0.20).value
            ),
            yaw_freeze_rad=float(self.declare_parameter("yaw_freeze_rad", 0.45).value),
            max_linear_accel_mps2=float(
                self.declare_parameter("max_linear_accel_mps2", 1.20).value
            ),
            max_lateral_accel_mps2=float(
                self.declare_parameter("max_lateral_accel_mps2", 0.90).value
            ),
            max_yaw_accel_radps2=float(
                self.declare_parameter("max_yaw_accel_radps2", 3.00).value
            ),
            use_strafe=bool(self.declare_parameter("use_strafe", False).value),
        )
        self.safety_params = SafetyOracleParams(
            horizon_s=float(self.declare_parameter("candidate_horizon_s", 0.80).value),
            sim_dt_s=float(self.declare_parameter("candidate_sim_dt_s", 0.10).value),
            occupied_threshold=int(
                self.declare_parameter("costmap_occupied_threshold", 55).value
            ),
        )

        self.state_machine = FollowStateMachine(
            reacquire_timeout_s=self.reacquire_timeout_s,
            sit_on_loss_timeout_s=self.sit_on_loss_timeout_s,
        )
        self.follow_enabled = False
        self.latest_target_point: PointStamped | None = None
        self.latest_target_received_mono_s: float | None = None
        self.latest_target_visible = False
        self.latest_vision_status = ""
        self.latest_costmap: GridMap2D | None = None
        self.latest_costmap_frame = ""
        self.last_command = Twist2D()
        self.last_control_time_s = time.monotonic()
        self.last_known_bearing_rad = 0.0
        self._lost_timeout_published = False
        self._last_state_text = ""
        self._last_warning_times: dict[str, float] = {}

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        self.cmd_vel_pub = self.create_publisher(Twist, self.cmd_vel_topic, 10)
        self.state_pub = self.create_publisher(String, "~/state", 10)
        self.event_pub = self.create_publisher(String, "~/event", 10)
        self.debug_twist_pub = self.create_publisher(Twist, "~/debug_twist", 10)
        self.nominal_twist_pub = self.create_publisher(Twist, "~/nominal_twist", 10)
        self.desired_standoff_pub = self.create_publisher(
            PointStamped, "~/desired_standoff_point", 10
        )
        self.safety_status_pub = self.create_publisher(String, "~/safety_status", 10)

        self.create_subscription(
            RobotModeState, self.robot_mode_state_topic, self._robot_mode_state_cb, 10
        )
        self.create_subscription(PointStamped, self.target_point_topic, self._target_point_cb, 10)
        self.create_subscription(Bool, self.target_visible_topic, self._target_visible_cb, 10)
        self.create_subscription(String, self.target_status_topic, self._target_status_cb, 10)
        if self.use_local_costmap_safety:
            self.create_subscription(
                OccupancyGrid, self.local_costmap_topic, self._costmap_cb, 10
            )

        self.control_timer = self.create_timer(
            1.0 / self.control_frequency_hz,
            self._control_timer_cb,
        )

        self._publish_state(self.state_machine.state)
        self.get_logger().info(
            "Person follow controller ready. "
            f"robot_mode_state_topic={self.robot_mode_state_topic} "
            f"target_point_topic={self.target_point_topic} "
            f"cmd_vel_topic={self.cmd_vel_topic} "
            f"use_local_costmap_safety={self.use_local_costmap_safety}"
        )

    def _robot_mode_state_cb(self, msg: RobotModeState) -> None:
        should_follow = (
            str(msg.task_mode) == "FOLLOW" and
            str(msg.posture_mode) == "STANDING" and
            bool(msg.motion_enabled)
        )
        now_s = time.monotonic()

        if should_follow == self.follow_enabled:
            return

        self.follow_enabled = should_follow
        if self.follow_enabled:
            self._arm_follow_mode(now_s)
            return

        self._disarm_follow_mode(now_s, "Follow mode disabled by mission supervisor.")

    def _arm_follow_mode(self, now_s: float) -> None:
        self.state_machine.handle_follow_command(now_s)
        self._lost_timeout_published = False
        self.last_command = Twist2D()
        self._publish_twist(Twist2D())
        self._publish_state(self.state_machine.state)
        self.get_logger().info("Follow mode armed by mission supervisor.")

    def _disarm_follow_mode(self, now_s: float, log_message: str) -> None:
        self.state_machine.handle_stop_command(now_s)
        self._lost_timeout_published = False
        self.last_command = Twist2D()
        self._publish_twist(Twist2D())
        self._publish_state(self.state_machine.state)
        self.get_logger().info(log_message)

    def _target_point_cb(self, msg: PointStamped) -> None:
        self.latest_target_point = msg
        self.latest_target_received_mono_s = time.monotonic()
        self.latest_target_visible = True

    def _target_visible_cb(self, msg: Bool) -> None:
        self.latest_target_visible = bool(msg.data)

    def _target_status_cb(self, msg: String) -> None:
        self.latest_vision_status = str(msg.data)

    def _costmap_cb(self, msg: OccupancyGrid) -> None:
        self.latest_costmap = GridMap2D(
            resolution=float(msg.info.resolution),
            width=int(msg.info.width),
            height=int(msg.info.height),
            origin_x=float(msg.info.origin.position.x),
            origin_y=float(msg.info.origin.position.y),
            data=tuple(int(value) for value in msg.data),
        )
        self.latest_costmap_frame = str(msg.header.frame_id)

    def _control_timer_cb(self) -> None:
        now_s = time.monotonic()
        dt_s = max(1.0 / self.control_frequency_hz, now_s - self.last_control_time_s)
        self.last_control_time_s = now_s

        has_fresh_target = self._has_fresh_target(now_s)
        previous_state = self.state_machine.state
        current_state = self.state_machine.update(now_s, has_fresh_target)
        if current_state != previous_state:
            self._publish_state(current_state)
            self._publish_follow_event_if_needed(previous_state, current_state)

        if current_state == FollowStates.IDLE:
            return

        if current_state == FollowStates.WAITING_FOR_TARGET:
            self.last_command = Twist2D()
            self._publish_twist(Twist2D())
            return

        if current_state == FollowStates.LOST_SIT:
            self._handle_lost_target_timeout()
            return

        if not has_fresh_target:
            reacquire_cmd = self._build_reacquire_command(now_s)
            limited = apply_acceleration_limits(
                self.last_command, reacquire_cmd, self.control_params, dt_s
            )
            self.last_command = limited
            self._publish_twist(limited)
            return

        target_point_base = self._transform_target_point_to_base()
        if target_point_base is None:
            limited = apply_acceleration_limits(
                self.last_command, Twist2D(), self.control_params, dt_s
            )
            self.last_command = limited
            self._publish_twist(limited)
            return

        target_x, target_y, target_z = target_point_base
        self.last_known_bearing_rad = math.atan2(target_y, target_x)
        current_state = self.state_machine.note_target_seen(now_s)
        if current_state != previous_state:
            self._publish_state(current_state)

        nominal = compute_nominal_follow_command(target_x, target_y, self.control_params)
        self._publish_nominal_twist(nominal)
        desired = self._choose_safe_command(nominal)
        limited = apply_acceleration_limits(self.last_command, desired, self.control_params, dt_s)
        self.last_command = limited
        self._publish_twist(limited)
        self._publish_desired_standoff_point(target_z)

    def _publish_follow_event_if_needed(self, previous_state: str, current_state: str) -> None:
        event_name = follow_state_event(previous_state, current_state)
        if event_name is None:
            return
        event_msg = String()
        event_msg.data = event_name
        self.event_pub.publish(event_msg)

    def _has_fresh_target(self, now_s: float) -> bool:
        if not self.follow_enabled:
            return False
        if not self.latest_target_visible or self.latest_target_point is None:
            return False
        if self.latest_target_received_mono_s is None:
            return False
        return (now_s - self.latest_target_received_mono_s) <= self.target_timeout_s

    def _build_reacquire_command(self, now_s: float) -> Twist2D:
        if not self.state_machine.reacquire_motion_enabled(now_s):
            return Twist2D()
        direction = 1.0 if self.last_known_bearing_rad >= 0.0 else -1.0
        return Twist2D(vx=0.0, vy=0.0, wz=direction * self.reacquire_yaw_rate_radps)

    def _choose_safe_command(self, nominal: Twist2D) -> Twist2D:
        if not self.use_local_costmap_safety:
            self._publish_safety_status("delegated_to_unitree_backend")
            return nominal

        if self.latest_costmap is None or not self.latest_costmap_frame:
            if self.allow_yaw_without_costmap:
                self._publish_safety_status("costmap_unavailable_fallback")
                return self._fallback_command_without_safety(
                    nominal,
                    "Local costmap is unavailable; using capped nominal follow command.",
                )
            self._publish_safety_status("costmap_unavailable_stop")
            return Twist2D()

        start_pose = self._lookup_robot_pose_in_costmap_frame()
        if start_pose is None:
            if self.allow_yaw_without_costmap:
                self._publish_safety_status("costmap_tf_unavailable_fallback")
                return self._fallback_command_without_safety(
                    nominal,
                    f"Could not transform {self.base_frame} into {self.latest_costmap_frame}; "
                    "using capped nominal follow command.",
                )
            self._publish_safety_status("costmap_tf_unavailable_stop")
            return Twist2D()

        if self.latest_costmap.value_at(start_pose.x, start_pose.y) is None:
            self._publish_safety_status("robot_out_of_costmap_fallback")
            return self._fallback_command_without_safety(
                nominal,
                f"Robot pose is outside the local costmap frame {self.latest_costmap_frame}; "
                "using capped nominal follow command.",
            )

        if not trajectory_is_safe(Twist2D(), start_pose, self.latest_costmap, self.safety_params):
            self._publish_safety_status("invalid_start_pose_fallback")
            return self._fallback_command_without_safety(
                nominal,
                "Current pose is already invalid in the safety oracle; using capped nominal follow command.",
            )

        safe_command, _ = select_safe_command(
            nominal,
            start_pose,
            self.latest_costmap,
            self.safety_params,
        )
        if self._is_zero_command(safe_command) and not self._is_zero_command(nominal):
            self._publish_safety_status("blocked_by_costmap")
            self._warn_throttled(
                "blocked_by_costmap",
                "Follow nominal command was rejected by the local safety oracle; holding position.",
            )
        else:
            self._publish_safety_status("safe_command_selected")
        return safe_command

    def _fallback_command_without_safety(self, nominal: Twist2D, warning: str) -> Twist2D:
        if not self.allow_nominal_without_safety:
            self._warn_throttled("follow_safety_fallback_disabled", warning)
            return Twist2D(
                vx=0.0,
                vy=0.0,
                wz=nominal.wz if self.allow_yaw_without_costmap else 0.0,
            )

        self._warn_throttled("follow_safety_fallback", warning)
        return Twist2D(
            vx=self._clamp(
                nominal.vx,
                -self.safety_fallback_linear_speed_mps,
                self.safety_fallback_linear_speed_mps,
            ),
            vy=self._clamp(
                nominal.vy,
                -self.safety_fallback_linear_speed_mps,
                self.safety_fallback_linear_speed_mps,
            ),
            wz=self._clamp(
                nominal.wz,
                -self.safety_fallback_yaw_rate_radps,
                self.safety_fallback_yaw_rate_radps,
            ),
        )

    def _transform_target_point_to_base(self) -> tuple[float, float, float] | None:
        if self.latest_target_point is None:
            return None
        source_frame = str(self.latest_target_point.header.frame_id)
        if not source_frame:
            self._warn_throttled("missing_target_frame", "Target point frame_id is empty.")
            return None

        try:
            transform = self.tf_buffer.lookup_transform(
                self.base_frame,
                source_frame,
                rclpy.time.Time(),
            )
        except Exception as exc:
            self._warn_throttled(
                "target_transform",
                f"Failed to transform target point into {self.base_frame}: {exc}",
            )
            return None

        return self._apply_transform_to_point(
            transform.transform.translation.x,
            transform.transform.translation.y,
            transform.transform.translation.z,
            transform.transform.rotation.x,
            transform.transform.rotation.y,
            transform.transform.rotation.z,
            transform.transform.rotation.w,
            self.latest_target_point.point.x,
            self.latest_target_point.point.y,
            self.latest_target_point.point.z,
        )

    def _lookup_robot_pose_in_costmap_frame(self) -> Pose2D | None:
        try:
            transform = self.tf_buffer.lookup_transform(
                self.latest_costmap_frame,
                self.base_frame,
                rclpy.time.Time(),
            )
        except Exception as exc:
            self._warn_throttled(
                "costmap_transform",
                f"Failed to lookup {self.latest_costmap_frame}->{self.base_frame}: {exc}",
            )
            return None

        return Pose2D(
            x=float(transform.transform.translation.x),
            y=float(transform.transform.translation.y),
            yaw=self._quaternion_to_yaw(
                float(transform.transform.rotation.x),
                float(transform.transform.rotation.y),
                float(transform.transform.rotation.z),
                float(transform.transform.rotation.w),
            ),
        )

    def _handle_lost_target_timeout(self) -> None:
        self.last_command = Twist2D()
        self._publish_twist(Twist2D())
        if self._lost_timeout_published:
            return

        event_msg = String()
        event_msg.data = "lost_target_timeout"
        self.event_pub.publish(event_msg)
        self._lost_timeout_published = True
        self.get_logger().warn(
            f"Tracked person lost for {self.sit_on_loss_timeout_s:.1f}s. "
            "Published lost_target_timeout and holding position."
        )

    def _publish_twist(self, command: Twist2D) -> None:
        msg = Twist()
        msg.linear.x = float(command.vx)
        msg.linear.y = float(command.vy)
        msg.angular.z = float(command.wz)
        self.cmd_vel_pub.publish(msg)
        self.debug_twist_pub.publish(msg)

    def _publish_nominal_twist(self, command: Twist2D) -> None:
        msg = Twist()
        msg.linear.x = float(command.vx)
        msg.linear.y = float(command.vy)
        msg.angular.z = float(command.wz)
        self.nominal_twist_pub.publish(msg)

    def _publish_desired_standoff_point(self, target_z: float) -> None:
        msg = PointStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self.base_frame
        msg.point.x = float(self.control_params.desired_distance_m)
        msg.point.y = 0.0
        msg.point.z = float(target_z)
        self.desired_standoff_pub.publish(msg)

    def _publish_state(self, state: str) -> None:
        state_text = str(state)
        if state_text == self._last_state_text:
            return
        msg = String()
        msg.data = state_text
        self.state_pub.publish(msg)
        self._last_state_text = state_text

    def _publish_safety_status(self, status: str) -> None:
        msg = String()
        msg.data = str(status)
        self.safety_status_pub.publish(msg)

    def _warn_throttled(self, key: str, message: str, period_s: float = 2.0) -> None:
        now_s = time.monotonic()
        last_s = self._last_warning_times.get(key)
        if last_s is not None and (now_s - last_s) < period_s:
            return
        self._last_warning_times[key] = now_s
        self.get_logger().warn(message)

    @staticmethod
    def _clamp(value: float, lower: float, upper: float) -> float:
        return max(lower, min(upper, value))

    @staticmethod
    def _is_zero_command(command: Twist2D, epsilon: float = 1.0e-4) -> bool:
        return (
            abs(command.vx) < epsilon and
            abs(command.vy) < epsilon and
            abs(command.wz) < epsilon
        )

    @staticmethod
    def _apply_transform_to_point(
        tx: float,
        ty: float,
        tz: float,
        qx: float,
        qy: float,
        qz: float,
        qw: float,
        px: float,
        py: float,
        pz: float,
    ) -> tuple[float, float, float]:
        rx, ry, rz = PersonFollowControllerNode._rotate_vector_by_quaternion(
            qx, qy, qz, qw, px, py, pz
        )
        return tx + rx, ty + ry, tz + rz

    @staticmethod
    def _rotate_vector_by_quaternion(
        qx: float,
        qy: float,
        qz: float,
        qw: float,
        vx: float,
        vy: float,
        vz: float,
    ) -> tuple[float, float, float]:
        tx = 2.0 * ((qy * vz) - (qz * vy))
        ty = 2.0 * ((qz * vx) - (qx * vz))
        tz = 2.0 * ((qx * vy) - (qy * vx))
        rx = vx + (qw * tx) + ((qy * tz) - (qz * ty))
        ry = vy + (qw * ty) + ((qz * tx) - (qx * tz))
        rz = vz + (qw * tz) + ((qx * ty) - (qy * tx))
        return rx, ry, rz

    @staticmethod
    def _quaternion_to_yaw(qx: float, qy: float, qz: float, qw: float) -> float:
        siny_cosp = 2.0 * ((qw * qz) + (qx * qy))
        cosy_cosp = 1.0 - (2.0 * ((qy * qy) + (qz * qz)))
        return math.atan2(siny_cosp, cosy_cosp)


def main() -> None:
    rclpy.init()
    node = PersonFollowControllerNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
