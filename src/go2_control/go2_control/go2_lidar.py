#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import Header


class Go2LidarNode(Node):
    def __init__(self):
        super().__init__("go2_lidar")

        self.source_topic = str(self.declare_parameter("source_topic", "/utlidar/cloud_base").value)
        self.output_topic = str(self.declare_parameter("output_topic", "/pointcloud").value)
        self.frame_id = str(self.declare_parameter("frame_id", "base_link").value)
        self.restamp_with_current_time = bool(
            self.declare_parameter("restamp_with_current_time", True).value
        )

        self.go2_lidar_subscriber = self.create_subscription(
            PointCloud2,
            self.source_topic,
            self.go2_lidar_callback,
            qos_profile_sensor_data,
        )
        self.go2_lidar_publisher = self.create_publisher(
            PointCloud2,
            self.output_topic,
            qos_profile_sensor_data,
        )
        self.get_logger().info(
            "go2 lidar relay started: "
            f"{self.source_topic} -> {self.output_topic}, "
            f"frame_id={self.frame_id or '<preserve>'}, "
            f"restamp_with_current_time={self.restamp_with_current_time}"
        )

    def go2_lidar_callback(self, msg):
        new_msg = PointCloud2()
        new_msg.header = Header()
        new_msg.header.frame_id = self.frame_id or msg.header.frame_id
        new_msg.header.stamp = (
            self.get_clock().now().to_msg()
            if self.restamp_with_current_time
            else msg.header.stamp
        )
        new_msg.height = msg.height
        new_msg.width = msg.width
        new_msg.fields = msg.fields
        new_msg.is_bigendian = msg.is_bigendian
        new_msg.point_step = msg.point_step
        new_msg.row_step = msg.row_step
        new_msg.data = msg.data
        new_msg.is_dense = msg.is_dense
        self.go2_lidar_publisher.publish(new_msg)

def main(args=None):
    rclpy.init(args=args)
    node = Go2LidarNode()
    rclpy.spin(node=node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
