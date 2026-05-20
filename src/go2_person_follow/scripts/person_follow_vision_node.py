#!/usr/bin/env python3
from __future__ import annotations

import rclpy
from geometry_msgs.msg import PointStamped
from rclpy.node import Node
from std_msgs.msg import Bool, Int32, String


class PersonFollowVisionStub(Node):
    def __init__(self) -> None:
        super().__init__("person_follow_vision_node")
        self.declare_parameter("robot_mode_state_topic", "/robot_mode_state")
        self.declare_parameter("detections_topic", "/detections_output")
        self.declare_parameter("color_image_topic", "/camera/color/image_raw")
        self.declare_parameter("depth_image_topic", "/camera/aligned_depth_to_color/image_raw")
        self.declare_parameter("camera_info_topic", "/camera/color/camera_info")
        self.declare_parameter("target_label", "person")
        self.target_point_pub = self.create_publisher(PointStamped, "~/target_point", 10)
        self.target_visible_pub = self.create_publisher(Bool, "~/target_visible", 10)
        self.target_id_pub = self.create_publisher(Int32, "~/target_id", 10)
        self.status_pub = self.create_publisher(String, "~/status", 10)
        self.create_timer(1.0, self._publish_unavailable)
        self._publish_unavailable()
        self.get_logger().warn(
            "Person-follow perception is a no-detector stub in this RealSense workflow; "
            "target_visible will remain false until a detector adapter is installed."
        )

    def _publish_unavailable(self) -> None:
        self.target_visible_pub.publish(Bool(data=False))
        self.target_id_pub.publish(Int32(data=-1))
        self.status_pub.publish(String(data="detector_unavailable"))


def main() -> None:
    rclpy.init()
    node = PersonFollowVisionStub()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
