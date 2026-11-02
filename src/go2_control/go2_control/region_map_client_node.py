import rclpy
from rclpy.node import Node
from go2_interfaces.srv import RegionMap

class RegionMapClientNode(Node):
    def __init__(self):
        super().__init__('region_map_client_node')
        # Create client
        self.cli = self.create_client(RegionMap, 'region_map_service')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('RegionMap service not available, waiting...')

    def call_region_map_service(self, command_str):
        req = RegionMap.Request()
        req.command = command_str
        future = self.cli.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        return future.result()

def main(args=None):
    rclpy.init(args=args)
    node = SomeClientNode()

    response = node.call_region_map_service("GET_CURRENT_REGION_MAP")
    if response and response.success:
        node.get_logger().info(
            f"Got region map! Robot in region {response.current_region_id}, "
            f"Message: {response.message}"
        )
    else:
        node.get_logger().info("Failed to get region map or service call unsuccessful.")

    rclpy.shutdown()

if __name__ == '__main__':
    main()
