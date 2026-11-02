#!/usr/bin/env python3
# Dummy leak detector: publishes Bool on /leak_detected,
# value controlled by a ROS 2 parameter `leak`.

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool


class DummyLeakPublisher(Node):
    def __init__(self):
        super().__init__('dummy_leak_publisher')

        # Declare a parameter to control the leak state
        # You can toggle it at runtime via `ros2 param set`.
        self.declare_parameter('leak', True)

        # Publisher on /leak_detected (std_msgs/Bool)
        self.pub = self.create_publisher(Bool, '/leak_detected', 10)

        # Publish at 5 Hz
        self.timer = self.create_timer(0.2, self.timer_callback)

        self.get_logger().info(
            'Dummy leak publisher started. '
            'Use "ros2 param set /dummy_leak_publisher leak true|false" to toggle.'
        )

    def timer_callback(self):
        # Read the current parameter value each tick
        leak_param = self.get_parameter('leak').get_parameter_value().bool_value
        msg = Bool()
        msg.data = leak_param
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = DummyLeakPublisher()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
