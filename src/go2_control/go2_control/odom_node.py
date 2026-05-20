#!/usr/bin/env python3
import math

import rclpy
from nav_msgs.msg import Odometry
from rclpy.node import Node


def _yaw_from_quaternion(q) -> float:
    return math.atan2(
        2.0 * ((q.w * q.z) + (q.x * q.y)),
        1.0 - (2.0 * ((q.y * q.y) + (q.z * q.z))),
    )


def _normalize_angle(angle: float) -> float:
    while angle > math.pi:
        angle -= 2.0 * math.pi
    while angle < -math.pi:
        angle += 2.0 * math.pi
    return angle


class OdomNode(Node):
    def __init__(self):
        super().__init__("odom_node")

        self.source_odom_topic = str(
            self.declare_parameter("source_odom_topic", "/utlidar/robot_odom").value
        )
        self.odom_topic = str(self.declare_parameter("odom_topic", "/utlidar_odom").value)
        self.parent_frame = str(self.declare_parameter("parent_frame", "odom").value)
        self.child_frame = str(self.declare_parameter("child_frame", "base_footprint").value)
        self.planarize = bool(self.declare_parameter("planarize", True).value)
        self.debug_odometry = bool(self.declare_parameter("debug_odometry", False).value)
        self.debug_interval_s = float(self.declare_parameter("debug_interval_s", 1.0).value)
        self.warn_pose_jump_m = float(self.declare_parameter("warn_pose_jump_m", 1.0).value)
        self.warn_yaw_jump_rad = float(self.declare_parameter("warn_yaw_jump_rad", 1.0).value)

        self._last_debug_log_ns = 0
        self._last_pose: tuple[float, float, float, float] | None = None

        self.odom_subscriber = self.create_subscription(
            Odometry,
            self.source_odom_topic,
            self.odom_callback,
            10,
        )
        self.odometry_publisher = self.create_publisher(Odometry, self.odom_topic, 10)

        mode = "planarized" if self.planarize else "passthrough"
        self.get_logger().info(
            f"odom_node started: {self.source_odom_topic} -> {self.odom_topic} "
            f"({self.parent_frame}->{self.child_frame}, {mode})"
        )
        if self.debug_odometry:
            self.get_logger().info(
                "debug_odometry enabled: logging planar odometry samples and jump warnings"
            )

    def odom_callback(self, msg: Odometry):
        odom_msg = Odometry()
        odom_msg.header.stamp = self._stamp_or_now(msg)
        odom_msg.header.frame_id = self.parent_frame
        odom_msg.child_frame_id = self.child_frame

        source_pose = msg.pose.pose
        odom_msg.pose.pose.position.x = source_pose.position.x
        odom_msg.pose.pose.position.y = source_pose.position.y
        odom_msg.pose.pose.position.z = 0.0 if self.planarize else source_pose.position.z

        source_yaw = _yaw_from_quaternion(source_pose.orientation)
        if self.planarize:
            half_yaw = 0.5 * source_yaw
            odom_msg.pose.pose.orientation.x = 0.0
            odom_msg.pose.pose.orientation.y = 0.0
            odom_msg.pose.pose.orientation.z = math.sin(half_yaw)
            odom_msg.pose.pose.orientation.w = math.cos(half_yaw)
        else:
            odom_msg.pose.pose.orientation = source_pose.orientation

        odom_msg.pose.covariance = msg.pose.covariance
        odom_msg.twist.twist.linear.x = msg.twist.twist.linear.x
        odom_msg.twist.twist.linear.y = msg.twist.twist.linear.y
        odom_msg.twist.twist.linear.z = 0.0 if self.planarize else msg.twist.twist.linear.z
        odom_msg.twist.twist.angular.x = 0.0 if self.planarize else msg.twist.twist.angular.x
        odom_msg.twist.twist.angular.y = 0.0 if self.planarize else msg.twist.twist.angular.y
        odom_msg.twist.twist.angular.z = msg.twist.twist.angular.z
        odom_msg.twist.covariance = msg.twist.covariance

        self.odometry_publisher.publish(odom_msg)
        self._log_debug_sample(msg, odom_msg, source_yaw)

    def _stamp_or_now(self, msg: Odometry):
        if msg.header.stamp.sec == 0 and msg.header.stamp.nanosec == 0:
            return self.get_clock().now().to_msg()
        return msg.header.stamp

    def _log_debug_sample(self, source_msg: Odometry, odom_msg: Odometry, source_yaw: float) -> None:
        x = odom_msg.pose.pose.position.x
        y = odom_msg.pose.pose.position.y
        yaw = _yaw_from_quaternion(odom_msg.pose.pose.orientation)
        stamp = odom_msg.header.stamp.sec + (odom_msg.header.stamp.nanosec * 1.0e-9)

        if self._last_pose is not None:
            last_x, last_y, last_yaw, last_stamp = self._last_pose
            distance_delta = math.hypot(x - last_x, y - last_y)
            yaw_delta = abs(_normalize_angle(yaw - last_yaw))
            time_delta = stamp - last_stamp
            if distance_delta > self.warn_pose_jump_m or yaw_delta > self.warn_yaw_jump_rad:
                self.get_logger().warning(
                    "large odom delta from source: "
                    f"distance={distance_delta:.3f}m yaw={yaw_delta:.3f}rad dt={time_delta:.3f}s"
                )
        else:
            distance_delta = 0.0
            yaw_delta = 0.0
            time_delta = 0.0

        self._last_pose = (x, y, yaw, stamp)
        if not self.debug_odometry:
            return

        now_ns = self.get_clock().now().nanoseconds
        if now_ns - self._last_debug_log_ns < int(self.debug_interval_s * 1.0e9):
            return
        self._last_debug_log_ns = now_ns
        self.get_logger().debug(
            "odom sample: "
            f"source_frame={source_msg.header.frame_id or '<empty>'} "
            f"out_frame={odom_msg.header.frame_id}->{odom_msg.child_frame_id} "
            f"x={x:.3f} y={y:.3f} z={odom_msg.pose.pose.position.z:.3f} "
            f"source_yaw={source_yaw:.3f} out_yaw={yaw:.3f} "
            f"delta={distance_delta:.3f}m yaw_delta={yaw_delta:.3f}rad dt={time_delta:.3f}s"
        )


def main(args=None):
    rclpy.init(args=args)
    node = OdomNode()
    try:
        rclpy.spin(node=node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
