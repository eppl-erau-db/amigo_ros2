#!/usr/bin/env python3
from __future__ import annotations

import time

import rclpy
from rclpy.node import Node
from unitree_api.msg import Request as UnitreeRequest


ROBOT_SPORT_API_ID_STANDUP = 1004
ROBOT_SPORT_API_ID_SIT = 1009


class RiseSitTestNode(Node):
    def __init__(self) -> None:
        super().__init__('rise_sit_test_node')

        self.sport_request_topic = str(
            self.declare_parameter('sport_request_topic', '/api/sport/request').value
        )
        self.startup_delay_s = max(
            0.0, float(self.declare_parameter('startup_delay_s', 1.0).value)
        )
        self.sit_hold_s = max(
            0.0, float(self.declare_parameter('sit_hold_s', 3.0).value)
        )
        self.auto_shutdown = bool(
            self.declare_parameter('auto_shutdown', True).value
        )
        self.shutdown_delay_s = max(
            0.0, float(self.declare_parameter('shutdown_delay_s', 1.0).value)
        )

        self._stage = 'WAITING'
        self._stage_deadline_s = time.monotonic() + self.startup_delay_s
        self._sent_sit = False
        self._sent_stand_up = False

        self.sport_req_pub = self.create_publisher(
            UnitreeRequest, self.sport_request_topic, 10
        )
        self.control_timer = self.create_timer(0.05, self._control_timer_cb)

        self.get_logger().info(
            'Sit test node ready. '
            f'sport_request_topic={self.sport_request_topic} '
            f'startup_delay_s={self.startup_delay_s:.2f} '
            f'sit_hold_s={self.sit_hold_s:.2f} '
            f'auto_shutdown={self.auto_shutdown}'
        )

    def _publish_sport_request(self, api_id: int, label: str) -> None:
        request = UnitreeRequest()
        request.header.identity.api_id = int(api_id)
        self.sport_req_pub.publish(request)
        self.get_logger().info(f'Published {label} sport request (api_id={api_id}).')

    def _control_timer_cb(self) -> None:
        now_s = time.monotonic()

        if self._stage == 'WAITING':
            if now_s < self._stage_deadline_s:
                return
            self._publish_sport_request(ROBOT_SPORT_API_ID_SIT, 'Sit')
            self._sent_sit = True
            self._stage = 'HOLDING'
            self._stage_deadline_s = now_s + self.sit_hold_s
            return

        if self._stage == 'HOLDING':
            if now_s < self._stage_deadline_s:
                return

            self._publish_sport_request(ROBOT_SPORT_API_ID_STANDUP, 'StandUp')
            self._sent_stand_up = True
            self._stage = 'DONE'
            self._stage_deadline_s = now_s + self.shutdown_delay_s
            if not self.auto_shutdown:
                self.get_logger().info('Sequence complete. Leaving node alive for inspection.')
            return

        if self._stage == 'DONE' and self.auto_shutdown and now_s >= self._stage_deadline_s:
            self.get_logger().info('Sequence complete. Shutting down test node.')
            self.control_timer.cancel()
            self.destroy_timer(self.control_timer)
            if rclpy.ok():
                rclpy.shutdown()


def main() -> None:
    rclpy.init()
    node = RiseSitTestNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
