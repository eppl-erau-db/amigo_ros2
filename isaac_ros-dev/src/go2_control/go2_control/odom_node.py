#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped, PoseStamped
from tf2_ros import TransformBroadcaster
from nav_msgs.msg import Odometry

class OdomNode(Node):
    def __init__(self):
        super().__init__("odom_node")

        self.robot_pose = PoseStamped()
        self.robot_odom = Odometry()

        self.pose_subscriber = self.create_subscription(PoseStamped, "/utlidar/robot_pose", self.pose_callback, 10)
        self.odom_subscriber = self.create_subscription(Odometry, "/utlidar/robot_odom", self.odom_callback, 10)
        self.odometry_publisher = self.create_publisher(Odometry, 'odom', 10)
        self.broadcaster = TransformBroadcaster(self, qos=10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info("odom has started")

    def pose_callback(self, msg):
        self.robot_pose = msg

    def odom_callback(self, msg):
        self.robot_odom = msg

    def timer_callback(self):
        self.publish_odom_to_base_tf()
        self.publish_odom_topic()


    def publish_odom_to_base_tf(self):
        if self.robot_pose:
            odom_trans = TransformStamped()
            odom_trans.header.stamp = self.get_clock().now().to_msg()
            odom_trans.header.frame_id = 'odom'
            odom_trans.child_frame_id = 'base_footprint'
            odom_trans.transform.translation.x = self.robot_pose.pose.position.x
            odom_trans.transform.translation.y = self.robot_pose.pose.position.y
            odom_trans.transform.translation.z = 0.0
            odom_trans.transform.rotation = self.robot_pose.pose.orientation
            self.broadcaster.sendTransform(odom_trans)

    def publish_odom_topic(self):
        if self.robot_odom:
            odom_msg = Odometry()
            odom_msg.header.stamp = self.get_clock().now().to_msg()
            odom_msg.header.frame_id = 'odom'
            odom_msg.child_frame_id = 'base_footprint'
            odom_msg.pose.pose.position.x = self.robot_odom.pose.pose.position.x
            odom_msg.pose.pose.position.y = self.robot_odom.pose.pose.position.y
            odom_msg.pose.pose.position.z = self.robot_odom.pose.pose.position.z
            odom_msg.pose.pose.orientation = self.robot_odom.pose.pose.orientation
            odom_msg.pose.covariance = self.robot_odom.pose.covariance
            odom_msg.twist.twist = self.robot_odom.twist.twist
            self.odometry_publisher.publish(odom_msg)

def main(args=None):
    rclpy.init(args=args)
    node = OdomNode()
    rclpy.spin(node=node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
