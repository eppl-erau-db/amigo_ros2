#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from unitree_api.msg import Request as UnitreeRequest

from go2_interfaces.msg import RobotModeState
from go2_interfaces.srv import SetRobotMode


ROBOT_SPORT_API_ID_EULER = 1007
ROBOT_SPORT_API_ID_POSE = 1028


class VoiceAttentionControllerNode(Node):
    def __init__(self) -> None:
        super().__init__("voice_attention_controller_node")

        self.robot_mode_state_topic = str(
            self.declare_parameter("robot_mode_state_topic", "/robot_mode_state").value
        )
        self.status_topic = str(
            self.declare_parameter("status_topic", "/voice/attention/status").value
        )
        self.sport_request_topic = str(
            self.declare_parameter("sport_request_topic", "/api/sport/request").value
        )
        self.mode_service_name = str(
            self.declare_parameter("mode_service_name", "/mission_supervisor_node/set_mode").value
        )
        self.control_frequency_hz = max(
            2.0, float(self.declare_parameter("control_frequency_hz", 10.0).value)
        )
        self.acknowledgement_pitch_rad = math.radians(
            float(self.declare_parameter("acknowledgement_pitch_deg", -12.0).value)
        )
        self.command_window_s = max(
            0.25, float(self.declare_parameter("command_window_s", 8.0).value)
        )
        self.pose_refresh_period_s = max(
            0.1, float(self.declare_parameter("pose_refresh_period_s", 0.25).value)
        )
        self.enable_pose_control = bool(
            self.declare_parameter("enable_pose_control", True).value
        )
        self.debug_enable = bool(self.declare_parameter("debug_enable", False).value)

        self.attention_enabled = False
        self._ack_started_mono_s = 0.0
        self._command_window_deadline_s = 0.0
        self._next_pose_refresh_mono_s = 0.0
        self._pose_command_sent = False
        self._pose_reset_sent = False
        self._pending_status = ""
        self._idle_future = None
        self._idle_retry_not_before_s = 0.0
        self._session_generation = 0
        self._stage = "IDLE"
        self._last_state_text = ""
        self._last_warning_times: dict[str, float] = {}

        self.mode_client = self.create_client(SetRobotMode, self.mode_service_name)

        self.state_pub = self.create_publisher(String, "~/state", 10)
        self.status_pub = self.create_publisher(String, self.status_topic, 10)
        self.sport_req_pub = self.create_publisher(UnitreeRequest, self.sport_request_topic, 10)

        self.create_subscription(
            RobotModeState, self.robot_mode_state_topic, self._robot_mode_state_cb, 10
        )
        self.control_timer = self.create_timer(
            1.0 / self.control_frequency_hz,
            self._control_timer_cb,
        )

        self._publish_state("IDLE")
        self.get_logger().info(
            "Voice attention controller ready. "
            f"robot_mode_state_topic={self.robot_mode_state_topic} "
            f"sport_request_topic={self.sport_request_topic} "
            f"status_topic={self.status_topic} "
            f"acknowledgement_pitch_deg={math.degrees(self.acknowledgement_pitch_rad):.1f} "
            f"command_window_s={self.command_window_s:.2f} "
            f"pose_refresh_period_s={self.pose_refresh_period_s:.2f}"
        )

    def _robot_mode_state_cb(self, msg: RobotModeState) -> None:
        should_enable = (
            str(msg.task_mode) == "ATTEND" and
            str(msg.posture_mode) == "STANDING" and
            bool(msg.motion_enabled)
        )

        if should_enable == self.attention_enabled:
            return

        self.attention_enabled = should_enable
        if self.attention_enabled:
            self._arm_attention_mode()
            return

        self._disarm_attention_mode("Wake attention mode disabled by mission supervisor.")

    def _arm_attention_mode(self) -> None:
        self._reset_session()
        self._set_stage("ACKNOWLEDGING")
        self._ack_started_mono_s = time.monotonic()
        self._command_window_deadline_s = self._ack_started_mono_s + self.command_window_s
        self._next_pose_refresh_mono_s = self._ack_started_mono_s
        self._send_acknowledgement_pose(reason="arm")
        self._pending_status = "ready"
        self._publish_status(self._pending_status)
        self.get_logger().info(
            "Wake attention mode armed by mission supervisor. "
            f"Holding acknowledgement pose for up to {self.command_window_s:.2f}s."
        )

    def _disarm_attention_mode(self, log_message: str) -> None:
        self._send_neutral_pose()
        held_duration_s = 0.0
        if self._ack_started_mono_s > 0.0:
            held_duration_s = max(0.0, time.monotonic() - self._ack_started_mono_s)
        self._reset_session()
        self._publish_state("IDLE")
        self.get_logger().info(f"{log_message} Pose hold duration was {held_duration_s:.2f}s.")

    def _reset_session(self) -> None:
        self._session_generation += 1
        self._ack_started_mono_s = 0.0
        self._command_window_deadline_s = 0.0
        self._next_pose_refresh_mono_s = 0.0
        self._pose_command_sent = False
        self._pose_reset_sent = False
        self._pending_status = ""
        self._idle_future = None
        self._idle_retry_not_before_s = 0.0
        self._stage = "IDLE"

    def _control_timer_cb(self) -> None:
        if not self.attention_enabled:
            return

        now_s = time.monotonic()
        if self._stage == "ACKNOWLEDGING":
            if (not self._pose_command_sent) or (now_s >= self._next_pose_refresh_mono_s):
                self._send_acknowledgement_pose(reason="refresh")
            if now_s < self._command_window_deadline_s:
                return
            self._set_stage("RETURNING_IDLE")

        if self._stage == "RETURNING_IDLE":
            self._send_neutral_pose()
            self._maybe_request_idle_return(now_s)

    def _send_acknowledgement_pose(self, *, reason: str) -> None:
        if self.enable_pose_control:
            self._publish_sport_request(ROBOT_SPORT_API_ID_POSE, {"data": True})
        self._publish_sport_request(
            ROBOT_SPORT_API_ID_EULER,
            {"x": 0.0, "y": self.acknowledgement_pitch_rad, "z": 0.0},
        )
        self._next_pose_refresh_mono_s = time.monotonic() + self.pose_refresh_period_s
        self._pose_command_sent = True
        self._pose_reset_sent = False
        if reason == "arm":
            self.get_logger().info(
                "Issued wake acknowledgement pose command "
                f"(pitch={math.degrees(self.acknowledgement_pitch_rad):.1f} deg)."
            )
        elif self.debug_enable:
            self.get_logger().info(
                "Reasserted wake acknowledgement pose command "
                f"(pitch={math.degrees(self.acknowledgement_pitch_rad):.1f} deg)."
            )

    def _send_neutral_pose(self) -> None:
        if not self._pose_command_sent or self._pose_reset_sent:
            return
        self._publish_sport_request(
            ROBOT_SPORT_API_ID_EULER,
            {"x": 0.0, "y": 0.0, "z": 0.0},
        )
        if self.enable_pose_control:
            self._publish_sport_request(ROBOT_SPORT_API_ID_POSE, {"data": False})
        self._pose_reset_sent = True
        self.get_logger().info("Restored neutral pose after wake acknowledgement.")

    def _publish_sport_request(self, api_id: int, payload: dict[str, float | bool]) -> None:
        request = UnitreeRequest()
        request.header.identity.api_id = int(api_id)
        request.parameter = json.dumps(payload, separators=(",", ":"))
        self.sport_req_pub.publish(request)

    def _maybe_request_idle_return(self, now_s: float) -> None:
        if not self._pending_status:
            return
        if self._idle_future is not None and not self._idle_future.done():
            return
        if now_s < self._idle_retry_not_before_s:
            return
        if not self.mode_client.service_is_ready():
            self._idle_retry_not_before_s = now_s + 1.0
            self._warn_throttled(
                "voice_attention_mode_service_unavailable",
                f"Wake attention is waiting for mode service {self.mode_service_name} to return to IDLE.",
            )
            return

        request = SetRobotMode.Request()
        request.task_mode = "IDLE"
        request.posture_mode = ""
        request.source = "voice_attention_controller"
        request.reason = self._pending_status
        request.allow_preempt = True

        session_generation = self._session_generation
        self._idle_retry_not_before_s = now_s + 1.0
        self._idle_future = self.mode_client.call_async(request)
        self._idle_future.add_done_callback(
            lambda future: self._handle_idle_response(future, session_generation)
        )

    def _handle_idle_response(self, future, session_generation: int) -> None:
        if session_generation != self._session_generation:
            return
        if self._idle_future is future:
            self._idle_future = None

        try:
            response = future.result()
        except Exception as exc:
            self._idle_retry_not_before_s = time.monotonic() + 1.0
            self._warn_throttled(
                "voice_attention_mode_service_call_failed",
                f"Wake attention failed to request IDLE: {exc}",
            )
            return

        if not response.accepted:
            self._idle_retry_not_before_s = time.monotonic() + 1.0
            self._warn_throttled(
                "voice_attention_mode_service_rejected",
                f"Wake attention could not return to IDLE: {response.message}",
            )
            return

        self._pending_status = ""

    def _publish_status(self, status: str) -> None:
        msg = String()
        msg.data = str(status)
        self.status_pub.publish(msg)

    def _set_stage(self, stage: str) -> None:
        self._stage = str(stage)
        self._publish_state(self._stage)

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


def main() -> None:
    rclpy.init()
    node = VoiceAttentionControllerNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
