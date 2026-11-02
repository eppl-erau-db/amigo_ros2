#!/usr/bin/env python3
from __future__ import annotations

import time

import rclpy
from explore_lite_msgs.msg import ExploreStatus
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from rclpy.task import Future
from std_msgs.msg import Bool

from go2_interfaces.action import ExploreUntilDetected


STATUS_LABELS = {
    str(ExploreStatus.EXPLORATION_STARTED): "exploration_started",
    str(ExploreStatus.EXPLORATION_IN_PROGRESS): "exploring",
    str(ExploreStatus.EXPLORATION_PAUSED): "exploration_paused",
    str(ExploreStatus.EXPLORATION_COMPLETE): "exploration_complete",
    str(ExploreStatus.RETURNING_TO_ORIGIN): "returning_to_origin",
    str(ExploreStatus.RETURNED_TO_ORIGIN): "returned_to_origin",
}


class ExploreUntilDetectedServer(Node):
    def __init__(self) -> None:
        super().__init__("explore_until_detected_server")

        self.action_name = str(
            self.declare_parameter("action_name", "explore_until_detected").value
        )
        self.leak_topic = str(
            self.declare_parameter("leak_topic", "/leak_detected").value
        )
        self.status_topic = str(
            self.declare_parameter("explore_status_topic", "explore/status").value
        )
        self.resume_topic = str(
            self.declare_parameter("explore_resume_topic", "explore/resume").value
        )
        self.feedback_period_s = max(
            0.1, float(self.declare_parameter("feedback_period_s", 0.5).value)
        )

        self._goal_active = False
        self._leak_detected = False
        self._last_status = str(ExploreStatus.EXPLORATION_PAUSED)
        self._last_status_time_mono = 0.0

        self._resume_pub = self.create_publisher(Bool, self.resume_topic, 10)
        self.create_subscription(Bool, self.leak_topic, self._leak_cb, 10)
        self.create_subscription(ExploreStatus, self.status_topic, self._status_cb, 10)

        self._action_server = ActionServer(
            self,
            ExploreUntilDetected,
            self.action_name,
            execute_callback=self.execute_cb,
            goal_callback=self.goal_cb,
            cancel_callback=self.cancel_cb,
        )

        self.get_logger().info(
            "Explore-until-detected action server ready: "
            f'action="{self.action_name}", leak_topic="{self.leak_topic}", '
            f'status_topic="{self.status_topic}", resume_topic="{self.resume_topic}"'
        )

    def _leak_cb(self, msg: Bool) -> None:
        self._leak_detected = bool(msg.data)

    def _status_cb(self, msg: ExploreStatus) -> None:
        self._last_status = STATUS_LABELS.get(str(msg.status), str(msg.status))
        self._last_status_time_mono = time.monotonic()

    def goal_cb(self, goal_request: ExploreUntilDetected.Goal):
        del goal_request
        if self._goal_active:
            self.get_logger().warn(
                "Rejecting ExploreUntilDetected goal because another goal is already active."
            )
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def cancel_cb(self, goal_handle):
        del goal_handle
        self.get_logger().info("ExploreUntilDetected cancel requested.")
        return CancelResponse.ACCEPT

    @staticmethod
    def _make_result(success: bool, reason: str) -> ExploreUntilDetected.Result:
        result = ExploreUntilDetected.Result()
        result.success = bool(success)
        result.reason = str(reason)
        return result

    @staticmethod
    def _make_feedback(stage: str) -> ExploreUntilDetected.Feedback:
        feedback = ExploreUntilDetected.Feedback()
        feedback.stage = str(stage)
        return feedback

    def _publish_resume(self, should_resume: bool) -> None:
        self._resume_pub.publish(Bool(data=bool(should_resume)))

    def _status_label(self) -> str:
        return str(self._last_status)

    async def _sleep_async(self, duration_s: float) -> None:
        if duration_s <= 0.0:
            return

        future: Future = Future()
        timer_box: dict[str, object] = {"timer": None, "done": False}

        def _complete_sleep() -> None:
            if timer_box["done"]:
                return
            timer_box["done"] = True
            if not future.done():
                future.set_result(True)

        timer_box["timer"] = self.create_timer(duration_s, _complete_sleep)
        try:
            await future
        finally:
            timer = timer_box.get("timer")
            if timer is not None:
                timer.cancel()
                self.destroy_timer(timer)

    async def execute_cb(self, goal_handle):
        self._goal_active = True
        leak_rearmed = not self._leak_detected
        self._publish_resume(True)
        self.get_logger().info(
            "ExploreUntilDetected execution started. Exploration resumed. "
            f"leak_initially_detected={self._leak_detected}"
        )

        try:
            while rclpy.ok():
                if goal_handle.is_cancel_requested:
                    self._publish_resume(False)
                    goal_handle.canceled()
                    return self._make_result(False, "canceled")

                if not self._leak_detected:
                    leak_rearmed = True

                if self._leak_detected and leak_rearmed:
                    self._publish_resume(False)
                    self.get_logger().info(
                        "ExploreUntilDetected stopping exploration because a fresh leak detection was observed."
                    )
                    goal_handle.publish_feedback(self._make_feedback("leak_detected"))
                    goal_handle.succeed()
                    return self._make_result(True, "leak_detected")

                stage = self._status_label()
                if self._leak_detected and not leak_rearmed:
                    stage = "waiting_for_fresh_detection"
                goal_handle.publish_feedback(self._make_feedback(stage))

                if self._last_status in (
                    "exploration_complete",
                    "returned_to_origin",
                ):
                    self._publish_resume(False)
                    self.get_logger().info(
                        "ExploreUntilDetected finished because exploration exhausted all frontiers."
                    )
                    goal_handle.succeed()
                    return self._make_result(False, "no_frontiers_remaining")

                await self._sleep_async(self.feedback_period_s)

            goal_handle.abort()
            return self._make_result(False, "ros_shutdown")
        finally:
            self._goal_active = False


def main() -> None:
    rclpy.init()
    node = ExploreUntilDetectedServer()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
