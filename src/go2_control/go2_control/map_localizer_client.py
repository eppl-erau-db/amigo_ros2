#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from functools import partial
from std_srvs.srv import Empty


class MapLocalizerClientNode(Node):
    def __init__(self):
        super().__init__("map_localizer_client")
        self.timer_period = 30.0  # seconds
        self.timer = self.create_timer(self.timer_period, self.call_map_localizer_server)
        self.client = self.create_client(Empty, "trigger_grid_search_localization")
        self.get_logger().info("MapLocalizerClientNode has started")

    def call_map_localizer_server(self):
        if not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn("Waiting for Map Localizer...")
            return

        request = Empty.Request()

        future = self.client.call_async(request)
        future.add_done_callback(partial(self.callback_call_map_localizer))

    def callback_call_map_localizer(self, future):
        try:
            response = future.result()
            self.get_logger().info("Service call succeeded")
        except Exception as e:
            self.get_logger().error("Service call failed: %r" % (e,))


def main(args=None):
    rclpy.init(args=args)
    node = MapLocalizerClientNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
