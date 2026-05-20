#!/usr/bin/env python3
import math

import rclpy
from geometry_msgs.msg import PoseStamped, TransformStamped
from nav_msgs.msg import Odometry
from rclpy.node import Node
from tf2_ros import TransformBroadcaster


def _yaw_from_quaternion(q) -> float:
    return math.atan2(
        2.0 * ((q.w * q.z) + (q.x * q.y)),
        1.0 - (2.0 * ((q.y * q.y) + (q.z * q.z))),
    )


class VslamOdomNode(Node):
    def __init__(self):
        super().__init__("vslam_odom_node")

        self.pose_topic = str(
            self.declare_parameter("source_pose_topic", "/visual_slam/tracking/vo_pose").value
        )
        self.source_odom_topic = str(
            self.declare_parameter("source_odom_topic", "/visual_slam/tracking/odometry").value
        )
        self.odom_topic = str(self.declare_parameter("odom_topic", "/vslam/odom").value)
        self.parent_frame = str(self.declare_parameter("parent_frame", "odom").value)
        self.child_frame = str(self.declare_parameter("child_frame", "base_footprint").value)
        self.planarize = bool(self.declare_parameter("planarize", True).value)
        self.publish_tf = bool(self.declare_parameter("publish_tf", False).value)
        self.debug_odometry = bool(self.declare_parameter("debug_odometry", False).value)

        self.pose_subscriber = self.create_subscription(PoseStamped, self.pose_topic, self.pose_callback, 10)
        self.odom_subscriber = self.create_subscription(
            Odometry,
            self.source_odom_topic,
            self.odom_callback,
            10,
        )
        self.odometry_publisher = self.create_publisher(Odometry, self.odom_topic, 10)
        self.pose_publisher = self.create_publisher(PoseStamped, "pose", 10)
        self.transform_publisher = self.create_publisher(TransformStamped, "transform", 10)
        self.broadcaster = TransformBroadcaster(self, qos=10)
        self._last_debug_log_ns = 0

        mode = "planarized" if self.planarize else "passthrough"
        tf_mode = "publishing TF" if self.publish_tf else "not publishing TF"
        self.get_logger().info(
            f"vslam odom node started: {self.source_odom_topic} -> {self.odom_topic} "
            f"({self.parent_frame}->{self.child_frame}, {mode}, {tf_mode})"
        )

    def pose_callback(self, msg: PoseStamped):
        if not self.planarize:
            self.pose_publisher.publish(msg)
            return
        pose_msg = PoseStamped()
        pose_msg.header = msg.header
        pose_msg.pose.position.x = msg.pose.position.x
        pose_msg.pose.position.y = msg.pose.position.y
        pose_msg.pose.position.z = 0.0
        yaw = _yaw_from_quaternion(msg.pose.orientation)
        half_yaw = 0.5 * yaw
        pose_msg.pose.orientation.z = math.sin(half_yaw)
        pose_msg.pose.orientation.w = math.cos(half_yaw)
        self.pose_publisher.publish(pose_msg)

    def odom_callback(self, msg: Odometry):
        odom_msg = Odometry()
        odom_msg.header.stamp = self._stamp_or_now(msg)
        odom_msg.header.frame_id = self.parent_frame
        odom_msg.child_frame_id = self.child_frame
        odom_msg.pose.pose.position.x = msg.pose.pose.position.x
        odom_msg.pose.pose.position.y = msg.pose.pose.position.y
        odom_msg.pose.pose.position.z = 0.0 if self.planarize else msg.pose.pose.position.z

        yaw = _yaw_from_quaternion(msg.pose.pose.orientation)
        if self.planarize:
            half_yaw = 0.5 * yaw
            odom_msg.pose.pose.orientation.z = math.sin(half_yaw)
            odom_msg.pose.pose.orientation.w = math.cos(half_yaw)
        else:
            odom_msg.pose.pose.orientation = msg.pose.pose.orientation

        odom_msg.pose.covariance = msg.pose.covariance
        odom_msg.twist.twist.linear.x = msg.twist.twist.linear.x
        odom_msg.twist.twist.linear.y = msg.twist.twist.linear.y
        odom_msg.twist.twist.linear.z = 0.0 if self.planarize else msg.twist.twist.linear.z
        odom_msg.twist.twist.angular.x = 0.0 if self.planarize else msg.twist.twist.angular.x
        odom_msg.twist.twist.angular.y = 0.0 if self.planarize else msg.twist.twist.angular.y
        odom_msg.twist.twist.angular.z = msg.twist.twist.angular.z
        odom_msg.twist.covariance = msg.twist.covariance

        self.odometry_publisher.publish(odom_msg)
        if self.publish_tf:
            transform_msg = self._to_transform(odom_msg)
            self.broadcaster.sendTransform(transform_msg)
            self.transform_publisher.publish(transform_msg)
        if self.debug_odometry:
            now_ns = self.get_clock().now().nanoseconds
            if now_ns - self._last_debug_log_ns >= 1_000_000_000:
                self._last_debug_log_ns = now_ns
                self.get_logger().debug(
                    f"vslam odom sample: x={odom_msg.pose.pose.position.x:.3f} "
                    f"y={odom_msg.pose.pose.position.y:.3f} z={odom_msg.pose.pose.position.z:.3f} yaw={yaw:.3f}"
                )

    def _stamp_or_now(self, msg: Odometry):
        if msg.header.stamp.sec == 0 and msg.header.stamp.nanosec == 0:
            return self.get_clock().now().to_msg()
        return msg.header.stamp

    def _to_transform(self, msg: Odometry) -> TransformStamped:
        transform_msg = TransformStamped()
        transform_msg.header = msg.header
        transform_msg.child_frame_id = msg.child_frame_id
        transform_msg.transform.translation.x = msg.pose.pose.position.x
        transform_msg.transform.translation.y = msg.pose.pose.position.y
        transform_msg.transform.translation.z = msg.pose.pose.position.z
        transform_msg.transform.rotation = msg.pose.pose.orientation
        return transform_msg


def main(args=None):
    rclpy.init(args=args)
    node = VslamOdomNode()
    try:
        rclpy.spin(node=node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
