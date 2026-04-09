#!/usr/bin/env python3
import math
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped, Quaternion
from nav_msgs.msg import OccupancyGrid
from go2_interfaces.action import Search
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult


def quaternion_to_yaw(q: Quaternion) -> float:
    """Convert a quaternion into a yaw angle (in radians)."""
    siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny_cosp, cosy_cosp)


class SearchActionServer(Node):
    def __init__(self):
        super().__init__('search_action_server')
        self._action_server = ActionServer(
            self,
            Search,
            'search',
            self.execute_callback
        )
        # Subscribe to the region map published by your region map service node.
        self.create_subscription(
            OccupancyGrid,
            'current_region_map',
            self.region_map_callback,
            10
        )
        # Subscribe to the robot's current pose.
        self.create_subscription(
            PoseWithCovarianceStamped,
            '/amcl_pose',
            self.pose_callback,
            10
        )
        self.current_region_map = None
        self.current_pose = None

        # Create BasicNavigator instance for navigation.
        self.navigator = BasicNavigator()
        self.log_info("Waiting for Nav2 to become active...")
        # self.navigator.waitUntilNav2Active()  # Uncomment if you need to wait.
        self.log_info("Nav2 is active.")

    def log_info(self, message: str):
        """Helper to log info messages and write them to a file."""
        self.get_logger().info(message)
        with open("search_action.log", "a") as f:
            f.write(f"[INFO] {message}\n")

    def log_error(self, message: str):
        """Helper to log error messages and write them to a file."""
        self.get_logger().error(message)
        with open("search_action.log", "a") as f:
            f.write(f"[ERROR] {message}\n")

    def region_map_callback(self, msg: OccupancyGrid):
        self.current_region_map = msg
        # self.log_info("Region map updated.")

    def pose_callback(self, msg: PoseWithCovarianceStamped):
        pose_stamped = PoseStamped()
        pose_stamped.header = msg.header
        pose_stamped.pose = msg.pose.pose
        self.current_pose = pose_stamped

    def compute_waypoint(self) -> PoseStamped:
        """
        Compute a waypoint 2 meters ahead of the current robot position.
        The waypoint is stamped using the navigator's clock and set in the 'map' frame.
        """
        waypoint = PoseStamped()
        waypoint.header.stamp = self.navigator.get_clock().now().to_msg()
        waypoint.header.frame_id = 'map'

        # Get current pose and compute yaw.
        x = self.current_pose.pose.position.x
        y = self.current_pose.pose.position.y
        z = self.current_pose.pose.position.z  # likely 0
        yaw = quaternion_to_yaw(self.current_pose.pose.orientation)

        # For demonstration, here we are not moving ahead (multiply by 0.0).
        # You can change the multiplier (e.g., 2.0 for 2 meters ahead).
        waypoint.pose.position.x = x + 0.1 * math.cos(yaw)
        waypoint.pose.position.y = y + 0.1 * math.sin(yaw)
        waypoint.pose.position.z = z  # assume same z
        waypoint.pose.orientation = self.current_pose.pose.orientation

        self.log_info(f"Computed waypoint at ({waypoint.pose.position.x:.2f}, "
                      f"{waypoint.pose.position.y:.2f}, {waypoint.pose.position.z:.2f})")
        return waypoint

    def send_nav_goal(self, target_pose: PoseStamped) -> bool:
        """
        Sends a navigation goal using BasicNavigator.
        Calls goToPose() and waits until the task is complete.
        """
        self.log_info(f"Navigating to waypoint at ({target_pose.pose.position.x:.2f}, "
                      f"{target_pose.pose.position.y:.2f}, {target_pose.pose.position.z:.2f})")
        task_pose = target_pose  # Already properly set up.
        self.navigator.goToPose(task_pose)
        while not self.navigator.isTaskComplete():
            _ = self.navigator.getFeedback()
            time.sleep(0.2)
        result = self.navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            self.log_info("Navigation to task pose succeeded")
            return True
        elif result == TaskResult.CANCELED:
            self.log_error("Navigation to task pose was canceled")
            return False
        elif result == TaskResult.FAILED:
            self.log_error("Navigation to task pose failed")
            return False
        return False

    def simulate_search(self):
        """
        Simulate a search (scanning) action.
        This function waits for a few seconds to mimic scanning.
        """
        self.log_info("Simulating search (scanning)...")
        time.sleep(3.0)
        self.log_info("Search simulation complete.")

    def execute_callback(self, goal_handle):
        self.log_info("Starting search action...")

        # Wait until both the region map and robot pose are available.
        timeout = 10.0
        start_time = self.get_clock().now().nanoseconds / 1e9
        while self.current_region_map is None or self.current_pose is None:
            rclpy.spin_once(self, timeout_sec=0.5)
            if (self.get_clock().now().nanoseconds / 1e9 - start_time) > timeout:
                self.log_error("Timeout waiting for region map and robot pose!")
                goal_handle.abort()
                return Search.Result()

        # Compute a waypoint.
        waypoint = self.compute_waypoint()

        # Send the navigation goal.
        if not self.send_nav_goal(waypoint):
            self.log_error("Navigation failed. Aborting search action.")
            goal_handle.abort()
            return Search.Result()

        # Simulate the search (scanning) action.
        self.simulate_search()

        # Publish feedback (dummy object info).
        feedback_msg = Search.Feedback()
        feedback_msg.object_class = "dummy_object"
        feedback_msg.object_location = waypoint  # For simulation, use the waypoint.
        feedback_msg.search_complete = True
        goal_handle.publish_feedback(feedback_msg)

        goal_handle.succeed()
        result = Search.Result()
        result.final_message = "Search complete."
        self.log_info("Search action completed successfully.")
        return result


def main(args=None):
    rclpy.init(args=args)
    node = SearchActionServer()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
