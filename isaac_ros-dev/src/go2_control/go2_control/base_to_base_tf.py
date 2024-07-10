#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped, PoseStamped
from tf2_ros import TransformBroadcaster


class OdomNode(Node):
    def __init__(self):
        super().__init__("base_to_base_tf")

        self.robot_pose = PoseStamped()

        self.pose_subscriber = self.create_subscription(PoseStamped, "/utlidar/robot_pose", self.pose_callback, 10)
        self.broadcaster = TransformBroadcaster(self, qos=10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info("base_footprint to base_link tf has started")

    def pose_callback(self, msg):
        self.robot_pose = msg

    def timer_callback(self):
        self.publish_base_to_base_tf()

    def publish_base_to_base_tf(self):
        if self.robot_pose:
            odom_trans = TransformStamped()
            odom_trans.header.stamp = self.get_clock().now().to_msg()
            odom_trans.header.frame_id = 'base_footprint'
            odom_trans.child_frame_id = 'base_link'
            odom_trans.transform.translation.x = 0.0
            odom_trans.transform.translation.y = 0.0
            odom_trans.transform.translation.z = self.robot_pose.pose.position.z
            odom_trans.transform.rotation.x = 0.0
            odom_trans.transform.rotation.y = 0.0
            odom_trans.transform.rotation.z = 0.0
            odom_trans.transform.rotation.w = 1.0
            self.broadcaster.sendTransform(odom_trans)

def main(args=None):
    rclpy.init(args=args)
    node = OdomNode()
    rclpy.spin(node=node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
