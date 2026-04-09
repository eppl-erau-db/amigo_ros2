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
ROBOT_SPORT_API_ID_STRETCH = 1017
ROBOT_SPORT_API_ID_POSE = 1028


class VoiceReadyControllerNode(Node):
    def __init__(self) -> None:
        super().__init__("voice_ready_controller_node")

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
            5.0, float(self.declare_parameter("control_frequency_hz", 15.0).value)
        )
        self.nod_down_pitch_rad = math.radians(
            float(self.declare_parameter("nod_down_pitch_deg", 12.0).value)
        )
        self.nod_up_pitch_rad = math.radians(
            float(self.declare_parameter("nod_up_pitch_deg", -12.0).value)
        )
        self.nod_hold_s = max(
            0.1, float(self.declare_parameter("nod_hold_s", 0.35).value)
        )
        self.pose_refresh_period_s = max(
            0.05, float(self.declare_parameter("pose_refresh_period_s", 0.15).value)
        )
        self.stretch_settle_s = max(
            0.0, float(self.declare_parameter("stretch_settle_s", 2.0).value)
        )
        self.enable_pose_control = bool(
            self.declare_parameter("enable_pose_control", True).value
        )
        self.debug_enable = bool(self.declare_parameter("debug_enable", False).value)

        self.sequence_enabled = False
        self._stage = "IDLE"
        self._stage_deadline_s = 0.0
        self._next_pose_refresh_mono_s = 0.0
        self._pose_command_sent = False
        self._pose_reset_sent = False
        self._stretch_sent = False
        self._pending_status = ""
        self._idle_future = None
        self._idle_retry_not_before_s = 0.0
        self._session_generation = 0
        self._last_state_text = ""
        self._last_warning_times: dict[str, float] = {}

        self.mode_client = self.create_client(SetRobotMode, self.mode_service_name)

        self.state_pub = self.create_publisher(String, "~/state", 10)
        self.status_pub = self.create_publisher(String, self.status_topic, 10)
        self.sport_req_pub = self.create_publisher(UnitreeRequest, self.sport_request_topic, 10)

        self.create_subscription(
            RobotModeState, self.robot_mode_state_topic, self._robot_mode_state_cb, 10
        )
        self.create_timer(1.0 / self.control_frequency_hz, self._control_timer_cb)

        self._publish_state("IDLE")
        self.get_logger().info(
            "Voice ready controller ready. "
            f"robot_mode_state_topic={self.robot_mode_state_topic} "
            f"sport_request_topic={self.sport_request_topic} "
            f"status_topic={self.status_topic} "
            f"nod_down_pitch_deg={math.degrees(self.nod_down_pitch_rad):.1f} "
            f"nod_up_pitch_deg={math.degrees(self.nod_up_pitch_rad):.1f} "
            f"nod_hold_s={self.nod_hold_s:.2f} "
            f"stretch_settle_s={self.stretch_settle_s:.2f}"
        )

    def _robot_mode_state_cb(self, msg: RobotModeState) -> None:
        should_enable = (
            str(msg.task_mode) == "READY" and
            str(msg.posture_mode) == "STANDING" and
            bool(msg.motion_enabled)
        )

        if should_enable == self.sequence_enabled:
            return

        self.sequence_enabled = should_enable
        if self.sequence_enabled:
            self._arm_ready_sequence()
            return

        self._disarm_ready_sequence("Ready sequence disabled by mission supervisor.")

    def _arm_ready_sequence(self) -> None:
        now_s = time.monotonic()
        self._reset_session()
        self._start_pitch_stage("NOD_DOWN_1", self.nod_down_pitch_rad, now_s)
        self.get_logger().info(
            "Ready sequence armed. Executing nod-and-stretch acknowledgement."
        )

    def _disarm_ready_sequence(self, log_message: str) -> None:
        self._send_neutral_pose()
        self._reset_session()
        self._publish_state("IDLE")
        self.get_logger().info(log_message)

    def _reset_session(self) -> None:
        self._session_generation += 1
        self._stage = "IDLE"
        self._stage_deadline_s = 0.0
        self._next_pose_refresh_mono_s = 0.0
        self._pose_command_sent = False
        self._pose_reset_sent = False
        self._stretch_sent = False
        self._pending_status = ""
        self._idle_future = None
        self._idle_retry_not_before_s = 0.0

    def _control_timer_cb(self) -> None:
        if not self.sequence_enabled:
            return

        now_s = time.monotonic()

        if self._stage in {"NOD_DOWN_1", "NOD_UP", "NOD_DOWN_2"}:
            pitch = self.nod_down_pitch_rad
            if self._stage == "NOD_UP":
                pitch = self.nod_up_pitch_rad

            if (not self._pose_command_sent) or (now_s >= self._next_pose_refresh_mono_s):
                self._send_pitch_pose(pitch, reason="refresh")

            if now_s < self._stage_deadline_s:
                return

            if self._stage == "NOD_DOWN_1":
                self._start_pitch_stage("NOD_UP", self.nod_up_pitch_rad, now_s)
                return
            if self._stage == "NOD_UP":
                self._start_pitch_stage("NOD_DOWN_2", self.nod_down_pitch_rad, now_s)
                return

            self._begin_stretch(now_s)
            return

        if self._stage == "STRETCHING":
            if now_s < self._stage_deadline_s:
                return
            if not self._pending_status:
                self._pending_status = "ready"
                self._publish_status(self._pending_status)
            self._set_stage("RETURNING_IDLE")

        if self._stage == "RETURNING_IDLE":
            self._maybe_request_idle_return(now_s)

    def _start_pitch_stage(self, stage: str, pitch_rad: float, now_s: float) -> None:
        self._set_stage(stage)
        self._stage_deadline_s = now_s + self.nod_hold_s
        self._send_pitch_pose(pitch_rad, reason="stage")

    def _begin_stretch(self, now_s: float) -> None:
        self._set_stage("STRETCHING")
        self._send_neutral_pose()
        self._send_stretch()
        self._stage_deadline_s = now_s + self.stretch_settle_s

    def _send_pitch_pose(self, pitch_rad: float, *, reason: str) -> None:
        if self.enable_pose_control:
            self._publish_sport_request(ROBOT_SPORT_API_ID_POSE, {"data": True})
        self._publish_sport_request(
            ROBOT_SPORT_API_ID_EULER,
            {"x": 0.0, "y": pitch_rad, "z": 0.0},
        )
        self._next_pose_refresh_mono_s = time.monotonic() + self.pose_refresh_period_s
        self._pose_command_sent = True
        self._pose_reset_sent = False
        if reason == "stage":
            self.get_logger().info(
                f"Ready sequence stage {self._stage} "
                f"(pitch={math.degrees(pitch_rad):.1f} deg)."
            )
        elif self.debug_enable:
            self.get_logger().info(
                f"Reasserted ready-sequence pose for {self._stage} "
                f"(pitch={math.degrees(pitch_rad):.1f} deg)."
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
        self.get_logger().info("Restored neutral pose after ready nod sequence.")

    def _send_stretch(self) -> None:
        if self._stretch_sent:
            return
        self._publish_sport_request(ROBOT_SPORT_API_ID_STRETCH)
        self._stretch_sent = True
        self.get_logger().info("Issued Unitree Stretch command for ready sequence.")

    def _publish_sport_request(
        self,
        api_id: int,
        payload: dict[str, float | bool] | None = None,
    ) -> None:
        request = UnitreeRequest()
        request.header.identity.api_id = int(api_id)
        if payload is not None:
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
                "voice_ready_mode_service_unavailable",
                f"Ready sequence is waiting for mode service {self.mode_service_name} to return to IDLE.",
            )
            return

        request = SetRobotMode.Request()
        request.task_mode = "IDLE"
        request.posture_mode = ""
        request.source = "voice_ready_controller"
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
                "voice_ready_mode_service_call_failed",
                f"Ready sequence failed to request IDLE: {exc}",
            )
            return

        if not response.accepted:
            self._idle_retry_not_before_s = time.monotonic() + 1.0
            self._warn_throttled(
                "voice_ready_mode_service_rejected",
                f"Ready sequence could not return to IDLE: {response.message}",
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
    node = VoiceReadyControllerNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
