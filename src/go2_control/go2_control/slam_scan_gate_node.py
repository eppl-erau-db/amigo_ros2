#!/usr/bin/env python3
from __future__ import annotations

import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

from go2_interfaces.msg import RobotModeState


class SlamScanGateNode(Node):
    def __init__(self) -> None:
        super().__init__("slam_scan_gate_node")

        self.input_scan_topic = str(
            self.declare_parameter("input_scan_topic", "/scan").value
        )
        self.output_scan_topic = str(
            self.declare_parameter("output_scan_topic", "/scan_slam").value
        )
        self.robot_mode_state_topic = str(
            self.declare_parameter("robot_mode_state_topic", "/robot_mode_state").value
        )
        self.blocked_task_modes = {
            str(mode).strip().upper()
            for mode in self.declare_parameter("blocked_task_modes", ["UPRIGHT"]).value
            if str(mode).strip()
        }
        self.resume_delay_s = max(
            0.0, float(self.declare_parameter("resume_delay_s", 1.0).value)
        )
        self.debug_enable = bool(self.declare_parameter("debug_enable", False).value)

        self._current_task_mode = ""
        self._task_mode_blocked = False
        self._blocked_until_mono_s = 0.0
        self._last_warning_times: dict[str, float] = {}

        self.scan_pub = self.create_publisher(LaserScan, self.output_scan_topic, 10)
        self.create_subscription(LaserScan, self.input_scan_topic, self._scan_cb, 10)
        self.create_subscription(
            RobotModeState, self.robot_mode_state_topic, self._robot_mode_state_cb, 10
        )

        self.get_logger().info(
            "SLAM scan gate ready. "
            f'input_scan_topic="{self.input_scan_topic}" '
            f'output_scan_topic="{self.output_scan_topic}" '
            f'robot_mode_state_topic="{self.robot_mode_state_topic}" '
            f"blocked_task_modes={sorted(self.blocked_task_modes)} "
            f"resume_delay_s={self.resume_delay_s:.2f}"
        )

    def _robot_mode_state_cb(self, msg: RobotModeState) -> None:
        now_s = time.monotonic()
        task_mode = str(msg.task_mode or "").strip().upper()
        is_blocked = task_mode in self.blocked_task_modes
        was_blocked = self._task_mode_blocked

        self._current_task_mode = task_mode
        self._task_mode_blocked = is_blocked

        if is_blocked and not was_blocked:
            self._blocked_until_mono_s = 0.0
            self.get_logger().info(
                f'SLAM scan gate is blocking scans while task_mode="{task_mode}".'
            )
            return

        if (not is_blocked) and was_blocked:
            self._blocked_until_mono_s = now_s + self.resume_delay_s
            self.get_logger().info(
                f'SLAM scan gate will resume scans in {self.resume_delay_s:.2f}s after leaving task_mode="{task_mode or "UNKNOWN"}".'
            )

    def _scan_cb(self, msg: LaserScan) -> None:
        if self._should_block_scan(time.monotonic()):
            if self.debug_enable:
                self._warn_throttled(
                    "slam_scan_gate_blocked",
                    "Dropping /scan for slam_toolbox while the SLAM gate is blocked.",
                    period_s=1.0,
                )
            return
        self.scan_pub.publish(msg)

    def _should_block_scan(self, now_s: float) -> bool:
        if self._task_mode_blocked:
            return True
        return now_s < self._blocked_until_mono_s

    def _warn_throttled(self, key: str, message: str, period_s: float = 2.0) -> None:
        now_s = time.monotonic()
        last_s = self._last_warning_times.get(key)
        if last_s is not None and (now_s - last_s) < period_s:
            return
        self._last_warning_times[key] = now_s
        self.get_logger().warn(message)


def main() -> None:
    rclpy.init()
    node = SlamScanGateNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
