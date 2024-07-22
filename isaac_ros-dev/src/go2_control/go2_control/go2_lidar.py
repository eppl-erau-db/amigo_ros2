#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2

class Go2LidarNode(Node):
    def __init__(self):
        super().__init__("go2_lidar")

        self.go2_lidar = PointCloud2()

        self.go2_lidar_subscriber = self.create_subscription(PointCloud2, "/utlidar/cloud", self.go2_lidar_callback, 10)
        self.go2_lidar_publisher = self.create_publisher(PointCloud2, 'point_cloud2', 10)
        self.get_logger().info("go2 lidar node has started")

    def go2_lidar_callback(self, msg):
        msg.header = Header(frame_id="radar")
        msg.header.stamp = self.get_clock().now().to_msg()
        self.go2_lidar_publisher.publish(msg)




def main(args=None):
    rclpy.init(args=args)
    node = Go2LidarNode()
    rclpy.spin(node=node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
