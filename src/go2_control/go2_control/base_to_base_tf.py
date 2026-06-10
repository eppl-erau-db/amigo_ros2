#!/usr/bin/env python3
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped, PoseStamped
from tf2_ros import TransformBroadcaster


def roll_pitch_only_quaternion(q):
    """Return (x, y, z, w) carrying only q's roll and pitch (yaw removed).

    base_footprint is the yaw-aligned ground projection of base_link, so the
    base_footprint -> base_link transform must carry the body's roll/pitch (and z)
    but NO yaw -- the EKF already owns yaw on odom -> base_footprint. Re-deriving
    yaw here would double-count it.
    """
    # quaternion (x,y,z,w) -> roll, pitch  (REP-103 / tf RPY, sxyz)
    sinr_cosp = 2.0 * (q.w * q.x + q.y * q.z)
    cosr_cosp = 1.0 - 2.0 * (q.x * q.x + q.y * q.y)
    roll = math.atan2(sinr_cosp, cosr_cosp)
    sinp = 2.0 * (q.w * q.y - q.z * q.x)
    sinp = max(-1.0, min(1.0, sinp))
    pitch = math.asin(sinp)
    # recompose with yaw = 0
    cr, sr = math.cos(roll * 0.5), math.sin(roll * 0.5)
    cp, sp = math.cos(pitch * 0.5), math.sin(pitch * 0.5)
    return (sr * cp, cr * sp, -sr * sp, cr * cp)


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
            # Carry the body's roll/pitch (yaw removed) so the rigidly-mounted laser
            # tilts with the quadruped instead of being held perfectly level. With
            # the previous identity rotation + EKF two_d_mode, tilted 2D scans were
            # integrated as level -> smeared/duplicated walls + phantom obstacles.
            qx, qy, qz, qw = roll_pitch_only_quaternion(self.robot_pose.pose.orientation)
            odom_trans.transform.rotation.x = qx
            odom_trans.transform.rotation.y = qy
            odom_trans.transform.rotation.z = qz
            odom_trans.transform.rotation.w = qw
            self.broadcaster.sendTransform(odom_trans)

def main(args=None):
    rclpy.init(args=args)
    node = OdomNode()
    rclpy.spin(node=node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
