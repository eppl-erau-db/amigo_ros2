#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import Header

class Go2LidarNode(Node):
    def __init__(self):
        super().__init__("go2_lidar")

        self.go2_lidar_subscriber = self.create_subscription(PointCloud2, "/utlidar/cloud", self.go2_lidar_callback, 10)
        self.go2_lidar_publisher = self.create_publisher(PointCloud2, 'pointcloud', 10)
        self.get_logger().info("go2 lidar node has started")

    def go2_lidar_callback(self, msg):
        new_msg = PointCloud2()
        new_msg.header = Header()
        new_msg.header.frame_id = "radar"
        new_msg.header.stamp = self.get_clock().now().to_msg()
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
