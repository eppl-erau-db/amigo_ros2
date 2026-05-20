#!/usr/bin/env python3
import rclpy
from geometry_msgs.msg import TransformStamped
from rclpy.node import Node
from tf2_ros import TransformBroadcaster


class BaseToBaseTfNode(Node):
    def __init__(self):
        super().__init__("base_to_base_tf")

        self.parent_frame = str(self.declare_parameter("parent_frame", "base_footprint").value)
        self.child_frame = str(self.declare_parameter("child_frame", "base_link").value)
        self.publish_tf = bool(self.declare_parameter("publish_tf", True).value)
        self.debug_odometry = bool(self.declare_parameter("debug_odometry", False).value)
        publish_rate_hz = float(self.declare_parameter("publish_rate_hz", 1.0).value)

        self.broadcaster = TransformBroadcaster(self, qos=10)
        self._last_debug_log_ns = 0
        if self.publish_tf:
            self.timer = self.create_timer(1.0 / max(publish_rate_hz, 0.1), self.publish_base_to_base_tf)
            self.get_logger().info(
                f"base_to_base_tf started: publishing planar identity {self.parent_frame}->{self.child_frame}"
            )
            if self.debug_odometry:
                self.get_logger().info(
                    "debug_odometry enabled: base_link z/roll/pitch are forced to zero"
                )
        else:
            self.timer = None
            self.get_logger().info("base_to_base_tf disabled by publish_tf parameter")

    def publish_base_to_base_tf(self):
        base_tf = TransformStamped()
        base_tf.header.stamp = self.get_clock().now().to_msg()
        base_tf.header.frame_id = self.parent_frame
        base_tf.child_frame_id = self.child_frame
        base_tf.transform.translation.x = 0.0
        base_tf.transform.translation.y = 0.0
        base_tf.transform.translation.z = 0.0
        base_tf.transform.rotation.x = 0.0
        base_tf.transform.rotation.y = 0.0
        base_tf.transform.rotation.z = 0.0
        base_tf.transform.rotation.w = 1.0
        self.broadcaster.sendTransform(base_tf)
        if self.debug_odometry:
            now_ns = self.get_clock().now().nanoseconds
            if now_ns - self._last_debug_log_ns >= 5_000_000_000:
                self._last_debug_log_ns = now_ns
                self.get_logger().debug(
                    f"published planar identity TF {self.parent_frame}->{self.child_frame}"
                )


def main(args=None):
    rclpy.init(args=args)
    node = BaseToBaseTfNode()
    try:
        rclpy.spin(node=node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
