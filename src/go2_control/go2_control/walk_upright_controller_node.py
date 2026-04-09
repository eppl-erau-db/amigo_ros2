#!/usr/bin/env python3
from __future__ import annotations

import json
import time

from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
import rclpy
from rclpy.node import Node
from robot_localization.srv import SetPose as SetEkfPose
from unitree_api.msg import Request as UnitreeRequest

from go2_interfaces.msg import RobotModeState
from go2_interfaces.srv import SetRobotMode


ROBOT_SPORT_API_ID_WALKUPRIGHT = 2050


class WalkUprightControllerNode(Node):
    def __init__(self) -> None:
        super().__init__("walk_upright_controller_node")

        self.robot_mode_state_topic = str(
            self.declare_parameter("robot_mode_state_topic", "/robot_mode_state").value
        )
        self.sport_request_topic = str(
            self.declare_parameter("sport_request_topic", "/api/sport/request").value
        )
        self.mode_service_name = str(
            self.declare_parameter("mode_service_name", "/mission_supervisor_node/set_mode").value
        )
        self.control_frequency_hz = max(
            2.0, float(self.declare_parameter("control_frequency_hz", 5.0).value)
        )
        self.auto_exit_timeout_s = max(
            0.0, float(self.declare_parameter("auto_exit_timeout_s", 8.0).value)
        )
        self.restore_localization_on_exit = bool(
            self.declare_parameter("restore_localization_on_exit", True).value
        )
        self.filtered_odom_topic = str(
            self.declare_parameter("filtered_odom_topic", "/odometry/filtered").value
        )
        self.localization_restore_service_name = str(
            self.declare_parameter("localization_restore_service_name", "/set_pose").value
        )
        self.localization_restore_delay_s = max(
            0.0, float(self.declare_parameter("localization_restore_delay_s", 1.0).value)
        )
        self.localization_snapshot_max_age_s = max(
            0.0, float(self.declare_parameter("localization_snapshot_max_age_s", 1.0).value)
        )
        self.debug_enable = bool(self.declare_parameter("debug_enable", False).value)

        self._upright_enabled = False
        self._upright_started_mono_s = 0.0
        self._idle_future = None
        self._idle_retry_not_before_s = 0.0
        self._session_generation = 0
        self._latest_filtered_odom: Odometry | None = None
        self._latest_filtered_odom_received_mono_s = 0.0
        self._saved_restore_pose: PoseWithCovarianceStamped | None = None
        self._restore_due_mono_s = 0.0
        self._restore_future = None
        self._restore_retry_not_before_s = 0.0
        self._restore_pending_generation = 0
        self._last_warning_times: dict[str, float] = {}

        self.mode_client = self.create_client(SetRobotMode, self.mode_service_name)
        self.localization_restore_client = self.create_client(
            SetEkfPose, self.localization_restore_service_name
        )
        self.sport_req_pub = self.create_publisher(UnitreeRequest, self.sport_request_topic, 10)
        self.create_subscription(
            RobotModeState, self.robot_mode_state_topic, self._robot_mode_state_cb, 10
        )
        self.create_subscription(Odometry, self.filtered_odom_topic, self._filtered_odom_cb, 10)
        self.create_timer(1.0 / self.control_frequency_hz, self._control_timer_cb)

        self.get_logger().info(
            "Walk upright controller ready. "
            f"robot_mode_state_topic={self.robot_mode_state_topic} "
            f"sport_request_topic={self.sport_request_topic} "
            f'mode_service_name="{self.mode_service_name}" '
            f"auto_exit_timeout_s={self.auto_exit_timeout_s:.2f} "
            f"restore_localization_on_exit={self.restore_localization_on_exit} "
            f'filtered_odom_topic="{self.filtered_odom_topic}" '
            f'localization_restore_service_name="{self.localization_restore_service_name}" '
            f"localization_restore_delay_s={self.localization_restore_delay_s:.2f}"
        )

    def _filtered_odom_cb(self, msg: Odometry) -> None:
        self._latest_filtered_odom = msg
        self._latest_filtered_odom_received_mono_s = time.monotonic()

    def _robot_mode_state_cb(self, msg: RobotModeState) -> None:
        should_enable = (
            str(msg.task_mode) == "UPRIGHT" and
            str(msg.posture_mode) == "STANDING" and
            bool(msg.motion_enabled)
        )

        if should_enable == self._upright_enabled:
            return

        now_s = time.monotonic()
        self._upright_enabled = should_enable
        if self._upright_enabled:
            self._session_generation += 1
            self._upright_started_mono_s = now_s
            self._idle_future = None
            self._idle_retry_not_before_s = 0.0
            self._restore_due_mono_s = 0.0
            self._restore_future = None
            self._restore_retry_not_before_s = 0.0
            self._restore_pending_generation = 0
            self._capture_localization_snapshot(now_s)
            self._send_walk_upright(True)
            self.get_logger().info("Enabled Unitree WalkUpright mode.")
        else:
            self._upright_started_mono_s = 0.0
            self._idle_future = None
            self._idle_retry_not_before_s = 0.0
            self._send_walk_upright(False)
            self._schedule_localization_restore(now_s)
            self.get_logger().info("Disabled Unitree WalkUpright mode.")

    def _control_timer_cb(self) -> None:
        now_s = time.monotonic()
        if self._upright_enabled and self.auto_exit_timeout_s > 0.0:
            if self._upright_started_mono_s <= 0.0:
                self._upright_started_mono_s = now_s
            elif (now_s - self._upright_started_mono_s) >= self.auto_exit_timeout_s:
                self._maybe_request_idle_return(now_s)

        if self._restore_due_mono_s > 0.0 and now_s >= self._restore_due_mono_s:
            self._maybe_request_localization_restore(now_s)

    def _send_walk_upright(self, enabled: bool) -> None:
        request = UnitreeRequest()
        request.header.identity.api_id = int(ROBOT_SPORT_API_ID_WALKUPRIGHT)
        request.parameter = json.dumps({"data": bool(enabled)}, separators=(",", ":"))
        self.sport_req_pub.publish(request)
        if self.debug_enable:
            self.get_logger().info(f"Published WalkUpright(data={enabled}).")

    def _maybe_request_idle_return(self, now_s: float) -> None:
        if self._idle_future is not None and not self._idle_future.done():
            return
        if now_s < self._idle_retry_not_before_s:
            return
        if not self.mode_client.service_is_ready():
            self._idle_retry_not_before_s = now_s + 1.0
            self._warn_throttled(
                "walk_upright_mode_service_unavailable",
                f"Walk upright controller is waiting for mode service {self.mode_service_name} to return to IDLE.",
            )
            return

        request = SetRobotMode.Request()
        request.task_mode = "IDLE"
        request.posture_mode = ""
        request.source = "walk_upright_controller"
        request.reason = "upright_timeout"
        request.allow_preempt = True

        session_generation = self._session_generation
        self._idle_retry_not_before_s = now_s + 1.0
        self._idle_future = self.mode_client.call_async(request)
        self._idle_future.add_done_callback(
            lambda future: self._handle_idle_response(future, session_generation)
        )
        self.get_logger().info(
            f"WalkUpright timeout reached ({self.auto_exit_timeout_s:.2f}s). Requesting IDLE."
        )

    def _capture_localization_snapshot(self, now_s: float) -> None:
        if not self.restore_localization_on_exit:
            self._saved_restore_pose = None
            return

        if self._latest_filtered_odom is None:
            self._saved_restore_pose = None
            self._warn_throttled(
                "walk_upright_restore_snapshot_missing",
                "Walk upright controller could not capture an EKF snapshot before entering UPRIGHT because no filtered odometry has arrived yet.",
            )
            return

        age_s = max(0.0, now_s - self._latest_filtered_odom_received_mono_s)
        if (
            self.localization_snapshot_max_age_s > 0.0 and
            age_s > self.localization_snapshot_max_age_s
        ):
            self._saved_restore_pose = None
            self._warn_throttled(
                "walk_upright_restore_snapshot_stale",
                "Walk upright controller skipped EKF snapshot capture because the latest filtered odometry is stale.",
            )
            return

        pose = PoseWithCovarianceStamped()
        pose.header = self._latest_filtered_odom.header
        pose.pose = self._latest_filtered_odom.pose
        self._saved_restore_pose = pose
        if self.debug_enable:
            self.get_logger().info(
                f'Captured EKF restore snapshot in frame "{pose.header.frame_id}".'
            )

    def _schedule_localization_restore(self, now_s: float) -> None:
        if not self.restore_localization_on_exit:
            return
        if self._saved_restore_pose is None:
            self._warn_throttled(
                "walk_upright_restore_snapshot_unavailable",
                "Walk upright controller had no saved EKF snapshot to restore after leaving UPRIGHT.",
            )
            return

        self._restore_due_mono_s = now_s + self.localization_restore_delay_s
        self._restore_future = None
        self._restore_retry_not_before_s = 0.0
        self._restore_pending_generation = self._session_generation
        self.get_logger().info(
            f"Scheduled EKF pose restore in {self.localization_restore_delay_s:.2f}s after exiting UPRIGHT."
        )

    def _maybe_request_localization_restore(self, now_s: float) -> None:
        if self._saved_restore_pose is None:
            self._restore_due_mono_s = 0.0
            return
        if self._restore_future is not None and not self._restore_future.done():
            return
        if now_s < self._restore_retry_not_before_s:
            return
        if not self.localization_restore_client.service_is_ready():
            self._restore_retry_not_before_s = now_s + 1.0
            self._warn_throttled(
                "walk_upright_restore_service_unavailable",
                f"Walk upright controller is waiting for localization restore service {self.localization_restore_service_name}.",
            )
            return

        request = SetEkfPose.Request()
        request.pose = self._build_restore_pose_request()
        restore_generation = self._restore_pending_generation
        self._restore_retry_not_before_s = now_s + 1.0
        self._restore_future = self.localization_restore_client.call_async(request)
        self._restore_future.add_done_callback(
            lambda future: self._handle_localization_restore_response(future, restore_generation)
        )
        self.get_logger().info(
            f'Requesting EKF pose restore via "{self.localization_restore_service_name}".'
        )

    def _build_restore_pose_request(self) -> PoseWithCovarianceStamped:
        assert self._saved_restore_pose is not None
        pose = PoseWithCovarianceStamped()
        pose.header.frame_id = str(self._saved_restore_pose.header.frame_id)
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose = self._saved_restore_pose.pose
        return pose

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
                "walk_upright_mode_service_call_failed",
                f"Walk upright controller failed to request IDLE: {exc}",
            )
            return

        if not response.accepted:
            self._idle_retry_not_before_s = time.monotonic() + 1.0
            self._warn_throttled(
                "walk_upright_mode_service_rejected",
                f"Walk upright controller could not return to IDLE: {response.message}",
            )

    def _handle_localization_restore_response(self, future, restore_generation: int) -> None:
        if self._restore_future is future:
            self._restore_future = None

        try:
            future.result()
        except Exception as exc:
            self._restore_retry_not_before_s = time.monotonic() + 1.0
            self._warn_throttled(
                "walk_upright_restore_service_call_failed",
                f"Walk upright controller failed to restore the EKF pose: {exc}",
            )
            return

        if restore_generation != self._restore_pending_generation:
            return

        restored_frame = (
            str(self._saved_restore_pose.header.frame_id)
            if self._saved_restore_pose is not None
            else "unknown"
        )
        self._restore_due_mono_s = 0.0
        self._restore_retry_not_before_s = 0.0
        self._restore_pending_generation = 0
        self._saved_restore_pose = None
        self.get_logger().info(
            f'Restored EKF pose from the pre-upright snapshot in frame "{restored_frame}".'
        )

    def _warn_throttled(self, key: str, message: str, period_s: float = 2.0) -> None:
        now_s = time.monotonic()
        last_s = self._last_warning_times.get(key)
        if last_s is not None and (now_s - last_s) < period_s:
            return
        self._last_warning_times[key] = now_s
        self.get_logger().warn(message)


def main() -> None:
    rclpy.init()
    node = WalkUprightControllerNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
