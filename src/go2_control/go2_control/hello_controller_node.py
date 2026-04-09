#!/usr/bin/env python3
from __future__ import annotations

import math
import re
import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from rclpy.time import Time
from std_msgs.msg import String
import tf2_ros
from unitree_api.msg import Request as UnitreeRequest
from zed_msgs.msg import ObjectsStamped

from go2_control.hello_controller_core import (
    GreetedTargetRecord,
    HelloCandidate,
    HelloControlParams,
    compute_centering_yaw_rate,
    greeting_target_key,
    hello_session_limit_reached,
    prune_greeted_history,
    record_greeted_target,
    select_hello_candidate,
    update_wave_dispatch_window,
)
from go2_interfaces.msg import RobotModeState
from go2_interfaces.srv import SetRobotMode


ROBOT_SPORT_API_ID_HELLO = 1016
TRACKING_STATE_OK = 1
TRACKING_STATE_SEARCHING = 2


class HelloControllerNode(Node):
    def __init__(self) -> None:
        super().__init__("hello_controller_node")

        self.robot_mode_state_topic = str(
            self.declare_parameter("robot_mode_state_topic", "/robot_mode_state").value
        )
        self.objects_topic = str(
            self.declare_parameter("objects_topic", "/zed/zed_node/obj_det/objects").value
        )
        self.cmd_vel_topic = str(
            self.declare_parameter("cmd_vel_topic", "/motion/candidate/hello").value
        )
        self.sport_request_topic = str(
            self.declare_parameter("sport_request_topic", "/api/sport/request").value
        )
        self.mode_service_name = str(
            self.declare_parameter("mode_service_name", "/mission_supervisor_node/set_mode").value
        )
        self.base_frame = str(self.declare_parameter("base_frame", "base_footprint").value)
        self.greet_memory_frame = str(
            self.declare_parameter("greet_memory_frame", "odom").value
        )
        self.max_greetings_per_session = max(
            0, int(self.declare_parameter("max_greetings_per_session", 3).value)
        )
        self.control_frequency_hz = max(
            2.0, float(self.declare_parameter("control_frequency_hz", 10.0).value)
        )
        self.target_timeout_s = max(
            0.1, float(self.declare_parameter("target_timeout_s", 1.0).value)
        )
        self.wave_hold_s = max(
            0.5, float(self.declare_parameter("wave_hold_s", 3.5).value)
        )
        self.pre_wave_stop_s = max(
            0.0, float(self.declare_parameter("pre_wave_stop_s", 0.75).value)
        )
        self.min_target_confidence = max(
            0.0, float(self.declare_parameter("min_target_confidence", 40.0).value)
        )
        self.target_label = self._normalize_label(
            str(self.declare_parameter("target_label", "person").value)
        )
        self.debug_enable = bool(self.declare_parameter("debug_enable", False).value)

        self.control_params = HelloControlParams(
            search_yaw_rate_radps=max(
                0.05, float(self.declare_parameter("search_yaw_rate_radps", 0.55).value)
            ),
            yaw_gain=max(0.1, float(self.declare_parameter("yaw_gain", 1.8).value)),
            max_yaw_rate_radps=max(
                0.1, float(self.declare_parameter("max_yaw_rate_radps", 0.9).value)
            ),
            target_yaw_deadband_rad=max(
                0.01, float(self.declare_parameter("target_yaw_deadband_rad", 0.18).value)
            ),
            greeted_target_memory_s=max(
                1.0, float(self.declare_parameter("greeted_target_memory_s", 30.0).value)
            ),
            greeted_target_xy_bin_m=max(
                0.1, float(self.declare_parameter("greeted_target_xy_bin_m", 0.75).value)
            ),
            greeted_target_match_radius_m=max(
                0.2, float(self.declare_parameter("greeted_target_match_radius_m", 1.25).value)
            ),
        )

        self.hello_enabled = False
        self.latest_objects: ObjectsStamped | None = None
        self.latest_objects_received_mono_s: float | None = None
        self.greeted_targets: list[GreetedTargetRecord] = []
        self.wave_active_until_s = 0.0
        self._pending_wave_target_key: tuple[int, int] | None = None
        self._pending_wave_ready_at_s = 0.0
        self._greetings_completed_in_session = 0
        self._auto_exit_after_wave = False
        self._auto_exit_request_accepted = False
        self._auto_exit_future = None
        self._auto_exit_retry_not_before_s = 0.0
        self._session_generation = 0
        self._last_state_text = ""
        self._last_warning_times: dict[str, float] = {}
        self._used_memory_frame_fallback = False

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        self.mode_client = self.create_client(SetRobotMode, self.mode_service_name)

        self.cmd_vel_pub = self.create_publisher(Twist, self.cmd_vel_topic, 10)
        self.state_pub = self.create_publisher(String, "~/state", 10)
        self.sport_req_pub = self.create_publisher(UnitreeRequest, self.sport_request_topic, 10)

        self.create_subscription(
            RobotModeState, self.robot_mode_state_topic, self._robot_mode_state_cb, 10
        )
        self.create_subscription(ObjectsStamped, self.objects_topic, self._objects_cb, 10)

        self.control_timer = self.create_timer(
            1.0 / self.control_frequency_hz,
            self._control_timer_cb,
        )

        self._publish_state("IDLE")
        self.get_logger().info(
            "Hello controller ready. "
            f"robot_mode_state_topic={self.robot_mode_state_topic} "
            f"objects_topic={self.objects_topic} "
            f"cmd_vel_topic={self.cmd_vel_topic} "
            f"greet_memory_frame={self.greet_memory_frame} "
            f"mode_service_name={self.mode_service_name} "
            f"max_greetings_per_session={self.max_greetings_per_session}"
        )

    def _robot_mode_state_cb(self, msg: RobotModeState) -> None:
        should_enable = (
            str(msg.task_mode) == "HELLO" and
            str(msg.posture_mode) == "STANDING" and
            bool(msg.motion_enabled)
        )

        if should_enable == self.hello_enabled:
            return

        self.hello_enabled = should_enable
        if self.hello_enabled:
            self._reset_session()
            self._publish_twist(0.0)
            self._publish_state("SEARCHING")
            self.get_logger().info("Hello mode armed by mission supervisor.")
            return

        self._reset_session()
        self._publish_twist(0.0)
        self._publish_state("IDLE")
        self.get_logger().info("Hello mode disabled by mission supervisor.")

    def _objects_cb(self, msg: ObjectsStamped) -> None:
        self.latest_objects = msg
        self.latest_objects_received_mono_s = time.monotonic()

    def _control_timer_cb(self) -> None:
        now_s = time.monotonic()
        self.greeted_targets = prune_greeted_history(
            self.greeted_targets,
            now_s=now_s,
            memory_s=self.control_params.greeted_target_memory_s,
        )

        if not self.hello_enabled:
            return

        if now_s < self.wave_active_until_s:
            self._clear_pending_wave()
            self._publish_twist(0.0)
            self._publish_state("WAVING")
            return

        if self._auto_exit_after_wave:
            self._publish_twist(0.0)
            self._publish_state("RETURNING_IDLE")
            if not self._auto_exit_request_accepted:
                self._maybe_request_idle_return(now_s, reason="greeting_limit_reached")
            return

        candidates = self._build_candidates()
        target = select_hello_candidate(
            candidates,
            self.greeted_targets,
            now_s=now_s,
            params=self.control_params,
        )
        if target is None:
            self._clear_pending_wave()
            self._publish_twist(self.control_params.search_yaw_rate_radps)
            self._publish_state("SEARCHING")
            return

        target_key = greeting_target_key(
            target,
            xy_bin_m=self.control_params.greeted_target_xy_bin_m,
        )
        yaw_rate = compute_centering_yaw_rate(target, self.control_params)
        if abs(yaw_rate) > 1.0e-4:
            self._clear_pending_wave()
            self._publish_twist(yaw_rate)
            self._publish_state("CENTERING")
            return

        should_dispatch_wave, pending_key, pending_ready_at_s = update_wave_dispatch_window(
            target_key,
            self._pending_wave_target_key,
            self._pending_wave_ready_at_s,
            now_s=now_s,
            stop_hold_s=self.pre_wave_stop_s,
        )
        self._pending_wave_target_key = pending_key
        self._pending_wave_ready_at_s = pending_ready_at_s

        self._publish_twist(0.0)
        if not should_dispatch_wave:
            self._publish_state("PRE_WAVE_STOP")
            return

        self.greeted_targets = record_greeted_target(
            self.greeted_targets,
            target,
            now_s=now_s,
            match_radius_m=self.control_params.greeted_target_match_radius_m,
        )
        self.wave_active_until_s = now_s + self.wave_hold_s
        self._greetings_completed_in_session += 1
        self._auto_exit_after_wave = hello_session_limit_reached(
            self._greetings_completed_in_session,
            self.max_greetings_per_session,
        )
        self._clear_pending_wave()
        self._publish_state("WAVING")
        self._send_hello_request()
        greeting_limit_text = (
            "unlimited"
            if self.max_greetings_per_session <= 0
            else str(self.max_greetings_per_session)
        )
        self.get_logger().info(
            "Waving at detected person. "
            f"greeting_count={self._greetings_completed_in_session}/{greeting_limit_text} "
            f"range_m={math.hypot(target.base_x_m, target.base_y_m):.2f} "
            f"bearing_rad={math.atan2(target.base_y_m, target.base_x_m):.2f}"
        )

    def _build_candidates(self) -> list[HelloCandidate]:
        now_s = time.monotonic()
        if self.latest_objects is None:
            return []
        if self.latest_objects_received_mono_s is None:
            return []
        if (now_s - self.latest_objects_received_mono_s) > self.target_timeout_s:
            return []

        source_frame = str(self.latest_objects.header.frame_id)
        if not source_frame:
            self._warn_throttled("hello_missing_frame", "Greeting detections are missing frame_id.")
            return []
        target_time = Time.from_msg(self.latest_objects.header.stamp)

        try:
            base_transform = self.tf_buffer.lookup_transform(
                self.base_frame,
                source_frame,
                target_time,
            )
        except Exception as exc:
            self._warn_throttled(
                "hello_base_transform",
                f"Failed to transform greeting targets into {self.base_frame}: {exc}",
            )
            return []

        memory_transform = None
        if self.greet_memory_frame and self.greet_memory_frame != self.base_frame:
            try:
                memory_transform = self.tf_buffer.lookup_transform(
                    self.greet_memory_frame,
                    source_frame,
                    target_time,
                )
            except Exception as exc:
                if not self._used_memory_frame_fallback:
                    self.get_logger().warn(
                        f"Failed to transform greeting targets into {self.greet_memory_frame}; "
                        f"falling back to {self.base_frame} for greet memory keys: {exc}"
                    )
                    self._used_memory_frame_fallback = True
        candidates: list[HelloCandidate] = []
        for obj in self.latest_objects.objects:
            if not self._object_is_usable(obj):
                continue

            base_point = self._apply_transform_to_point(
                base_transform.transform.translation.x,
                base_transform.transform.translation.y,
                base_transform.transform.translation.z,
                base_transform.transform.rotation.x,
                base_transform.transform.rotation.y,
                base_transform.transform.rotation.z,
                base_transform.transform.rotation.w,
                obj.position[0],
                obj.position[1],
                obj.position[2],
            )

            if memory_transform is None:
                memory_point = base_point
            else:
                memory_point = self._apply_transform_to_point(
                    memory_transform.transform.translation.x,
                    memory_transform.transform.translation.y,
                    memory_transform.transform.translation.z,
                    memory_transform.transform.rotation.x,
                    memory_transform.transform.rotation.y,
                    memory_transform.transform.rotation.z,
                    memory_transform.transform.rotation.w,
                    obj.position[0],
                    obj.position[1],
                    obj.position[2],
                )

            candidates.append(
                HelloCandidate(
                    base_x_m=float(base_point[0]),
                    base_y_m=float(base_point[1]),
                    base_z_m=float(base_point[2]),
                    memory_x_m=float(memory_point[0]),
                    memory_y_m=float(memory_point[1]),
                    confidence=float(obj.confidence),
                    bbox_area_px=float(self._bounding_box_area_px(obj)),
                )
            )

        if self.debug_enable and candidates:
            self.get_logger().info(f"Hello controller built {len(candidates)} candidate(s).")
        return candidates

    def _object_is_usable(self, obj) -> bool:
        if self._normalize_label(str(obj.label)) != self.target_label:
            return False
        if float(obj.confidence) < self.min_target_confidence:
            return False
        if bool(obj.tracking_available) and int(obj.tracking_state) not in {
            TRACKING_STATE_OK,
            TRACKING_STATE_SEARCHING,
        }:
            return False
        return True

    def _publish_twist(self, yaw_rate_radps: float) -> None:
        msg = Twist()
        msg.angular.z = float(yaw_rate_radps)
        self.cmd_vel_pub.publish(msg)

    def _send_hello_request(self) -> None:
        request = UnitreeRequest()
        request.header.identity.api_id = int(ROBOT_SPORT_API_ID_HELLO)
        self.sport_req_pub.publish(request)

    def _maybe_request_idle_return(self, now_s: float, *, reason: str) -> None:
        if self._auto_exit_future is not None and not self._auto_exit_future.done():
            return
        if now_s < self._auto_exit_retry_not_before_s:
            return
        if not self.mode_client.service_is_ready():
            self._auto_exit_retry_not_before_s = now_s + 1.0
            self._warn_throttled(
                "hello_mode_service_unavailable",
                f"Hello controller is waiting for mode service {self.mode_service_name} "
                "to return the robot to IDLE.",
            )
            return

        request = SetRobotMode.Request()
        request.task_mode = "IDLE"
        request.posture_mode = ""
        request.source = "hello_controller"
        request.reason = str(reason)
        request.allow_preempt = True

        session_generation = self._session_generation
        self._auto_exit_retry_not_before_s = now_s + 1.0
        self._auto_exit_future = self.mode_client.call_async(request)
        self._auto_exit_future.add_done_callback(
            lambda future: self._handle_auto_exit_response(future, session_generation)
        )
        self.get_logger().info(
            "Hello session reached its greeting limit; requesting return to IDLE."
        )

    def _handle_auto_exit_response(self, future, session_generation: int) -> None:
        if session_generation != self._session_generation:
            return
        if self._auto_exit_future is future:
            self._auto_exit_future = None

        try:
            response = future.result()
        except Exception as exc:
            self._auto_exit_retry_not_before_s = time.monotonic() + 1.0
            self._warn_throttled(
                "hello_mode_service_call_failed",
                f"Hello controller failed to request IDLE after greeting limit: {exc}",
            )
            return

        if not response.accepted:
            self._auto_exit_retry_not_before_s = time.monotonic() + 1.0
            self._warn_throttled(
                "hello_mode_service_rejected",
                "Hello controller could not return to IDLE after greeting limit: "
                f"{response.message}",
            )
            return

        self._auto_exit_request_accepted = True
        self.get_logger().info(
            "Hello session complete; waiting for mission supervisor to switch back to IDLE."
        )

    def _publish_state(self, state: str) -> None:
        state_text = str(state)
        if state_text == self._last_state_text:
            return
        msg = String()
        msg.data = state_text
        self.state_pub.publish(msg)
        self._last_state_text = state_text

    def _warn_throttled(self, key: str, message: str, period_s: float = 2.0) -> None:
        now_s = time.monotonic()
        last_s = self._last_warning_times.get(key)
        if last_s is not None and (now_s - last_s) < period_s:
            return
        self._last_warning_times[key] = now_s
        self.get_logger().warn(message)

    def _clear_pending_wave(self) -> None:
        self._pending_wave_target_key = None
        self._pending_wave_ready_at_s = 0.0

    def _reset_session(self) -> None:
        self._session_generation += 1
        self.wave_active_until_s = 0.0
        self._clear_pending_wave()
        self._greetings_completed_in_session = 0
        self._auto_exit_after_wave = False
        self._auto_exit_request_accepted = False
        self._auto_exit_future = None
        self._auto_exit_retry_not_before_s = 0.0

    @staticmethod
    def _normalize_label(raw: str) -> str:
        return re.sub(r"[^a-z0-9]+", "_", str(raw).strip().lower()).strip("_")

    @staticmethod
    def _bounding_box_area_px(obj) -> int:
        corners = getattr(getattr(obj, "bounding_box_2d", None), "corners", [])
        if len(corners) != 4:
            return 0
        xs = [int(corner.kp[0]) for corner in corners]
        ys = [int(corner.kp[1]) for corner in corners]
        width = max(xs) - min(xs)
        height = max(ys) - min(ys)
        if width <= 0 or height <= 0:
            return 0
        return width * height

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
        rotation = HelloControllerNode._quaternion_to_rotation_matrix(qx, qy, qz, qw)
        rx = (rotation[0][0] * px) + (rotation[0][1] * py) + (rotation[0][2] * pz)
        ry = (rotation[1][0] * px) + (rotation[1][1] * py) + (rotation[1][2] * pz)
        rz = (rotation[2][0] * px) + (rotation[2][1] * py) + (rotation[2][2] * pz)
        return (tx + rx, ty + ry, tz + rz)

    @staticmethod
    def _quaternion_to_rotation_matrix(
        qx: float,
        qy: float,
        qz: float,
        qw: float,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]:
        norm = math.sqrt((qx * qx) + (qy * qy) + (qz * qz) + (qw * qw))
        if norm <= 1.0e-9:
            return (
                (1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
            )

        x = qx / norm
        y = qy / norm
        z = qz / norm
        w = qw / norm

        return (
            (
                1.0 - (2.0 * ((y * y) + (z * z))),
                2.0 * ((x * y) - (z * w)),
                2.0 * ((x * z) + (y * w)),
            ),
            (
                2.0 * ((x * y) + (z * w)),
                1.0 - (2.0 * ((x * x) + (z * z))),
                2.0 * ((y * z) - (x * w)),
            ),
            (
                2.0 * ((x * z) - (y * w)),
                2.0 * ((y * z) + (x * w)),
                1.0 - (2.0 * ((x * x) + (y * y))),
            ),
        )


def main() -> None:
    rclpy.init()
    node = HelloControllerNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
