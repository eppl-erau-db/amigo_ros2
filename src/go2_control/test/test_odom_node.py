from __future__ import annotations

import pathlib
import sys

import rclpy
from nav_msgs.msg import Odometry

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from go2_control.odom_node import OdomNode  # noqa: E402


class _CapturePublisher:
    def __init__(self) -> None:
        self.messages: list[Odometry] = []

    def publish(self, msg: Odometry) -> None:
        self.messages.append(msg)


def _source_odom(sec: int = 10, nanosec: int = 20) -> Odometry:
    msg = Odometry()
    msg.header.stamp.sec = sec
    msg.header.stamp.nanosec = nanosec
    msg.pose.pose.orientation.w = 1.0
    return msg


def test_odom_node_preserves_source_stamp_by_default() -> None:
    started_context = False
    if not rclpy.ok():
        rclpy.init()
        started_context = True

    node = OdomNode()
    capture = _CapturePublisher()
    original_publisher = node.odometry_publisher

    try:
        node.odometry_publisher = capture
        node.odom_callback(_source_odom())
    finally:
        node.odometry_publisher = original_publisher
        node.destroy_node()
        if started_context and rclpy.ok():
            rclpy.shutdown()

    assert len(capture.messages) == 1
    assert capture.messages[0].header.stamp.sec == 10
    assert capture.messages[0].header.stamp.nanosec == 20


def test_odom_node_can_restamp_with_current_ros_time() -> None:
    started_context = False
    if not rclpy.ok():
        rclpy.init()
        started_context = True

    node = OdomNode()
    capture = _CapturePublisher()
    original_publisher = node.odometry_publisher

    try:
        node.restamp_with_current_time = True
        node.odometry_publisher = capture
        node.odom_callback(_source_odom())
    finally:
        node.odometry_publisher = original_publisher
        node.destroy_node()
        if started_context and rclpy.ok():
            rclpy.shutdown()

    assert len(capture.messages) == 1
    assert capture.messages[0].header.stamp.sec != 10
