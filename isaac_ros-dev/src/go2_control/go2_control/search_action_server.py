#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, ActionClient
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import OccupancyGrid
from go2_interfaces.action import Search  
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import time
# from go2_interfaces.action import Scan

import time

# Neuron states
UNCOVERED = 0
COVERED = 1
OBSTACLE = -1

class SearchActionServer(Node):
    def __init__(self):
        super().__init__('search_action_server')
        self._action_server = ActionServer(
            self,
            Search,
            'search',
            self.execute_callback
        )
        # Subscribe to the continuously published current region map
        self.region_map_sub = self.create_subscription(
            OccupancyGrid,
            'current_region_map',
            self.region_map_callback,
            10
        )
        self.current_region_map = None
        # Dictionary to store neurons
        # Each neuron is a dict with keys: 'row', 'col', 'x', 'y', 'state'
        self.neurons = []

        self.navigator = BasicNavigator()

    def region_map_callback(self, msg: OccupancyGrid):
        self.current_region_map = msg
        self.get_logger().info("Updated current region map received")
        # Each time a new map arrives, (re)generate neurons.
        self.neurons = self.generate_neurons_from_map(msg)

    def generate_neurons_from_map(self, grid: OccupancyGrid):
        """
        Process the occupancy grid to create a list of neuron cells.
        For simplicity, we assume each grid cell corresponds to a neuron.
        States:
          - If cell value == 0, mark as UNCOVERED (free space)
          - If cell value > 0 (occupied), mark as OBSTACLE.
        The Pose (x, y) is computed from grid indices.
        """
        neurons = []
        width = grid.info.width
        height = grid.info.height
        resolution = grid.info.resolution
        origin_x = grid.info.origin.position.x
        origin_y = grid.info.origin.position.y

        # OccupancyGrid.data is a flat list in row-major order.
        for row in range(height):
            for col in range(width):
                index = row * width + col
                cell_val = grid.data[index]
                # In ROS occupancy grid, 0 is free, 100 is occupied, -1 unknown.
                if cell_val == 0:
                    state = UNCOVERED
                else:
                    state = OBSTACLE
                # Calculate the cell's center position.
                x = origin_x + (col + 0.5) * resolution
                y = origin_y + (row + 0.5) * resolution
                neuron = {
                    'row': row,
                    'col': col,
                    'x': x,
                    'y': y,
                    'state': state
                }
                neurons.append(neuron)
        self.get_logger().info(f"Generated {len(neurons)} neurons from costmap")
        return neurons

    def has_uncovered_neuron(self):
        """Check if there is any neuron in the list with state UNCOVERED."""
        for neuron in self.neurons:
            if neuron['state'] == UNCOVERED:
                return True
        return False

    def select_next_neuron(self):
        """Select the next uncovered neuron. (Here, simply the first one.)"""
        for neuron in self.neurons:
            if neuron['state'] == UNCOVERED:
                return neuron
        return None

    def neuron_to_pose(self, neuron):
        """Convert a neuron dictionary to a PoseStamped message."""
        pose = PoseStamped()
        pose.header.frame_id = "map"
        # Use the neuron's center as the target position.
        pose.pose.position.x = neuron['x']
        pose.pose.position.y = neuron['y']
        pose.pose.orientation.w = 1.0  # No rotation for simplicity
        return pose

    def send_nav_goal(self, target_pose: PoseStamped):
        """
        Send a navigation goal using BasicNavigator.
        This function uses BasicNavigator's goToPose() and waits until the task is complete.
        Returns True if navigation succeeded, False otherwise.
        """
        self.get_logger().info(
            f"Sending navigation goal to ({target_pose.pose.position.x:.2f}, {target_pose.pose.position.y:.2f}) using BasicNavigator"
        )
        self.navigator.goToPose(target_pose)
        # Wait until the navigator reports that the task is complete.
        while not self.navigator.isTaskComplete():
            # Optionally, process feedback here (for example, update action feedback).
            _ = self.navigator.getFeedback()
            time.sleep(0.5)
        result = self.navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            self.get_logger().info("Navigation goal reached!")
            return True
        else:
            self.get_logger().error("Navigation goal failed!")
            return False

    def perform_scanning_action(self):
        """
        Stub for scanning action.
        In a full implementation, this would call an action server
        that drives the stepper motors and processes the camera feed.
        Here we simulate a delay and return dummy scan data.
        """
        self.get_logger().info("Starting scanning action...")
        # Simulate scanning delay (replace with actual action call)
        time.sleep(3.0)
        self.get_logger().info("Scanning complete; objects detected: []")
        # Return dummy data (for example, an empty list)
        return []

    def update_neuron_state(self, neuron):
        """Mark the given neuron as COVERED (visited)."""
        neuron['state'] = COVERED
        self.get_logger().info(f"Neuron at ({neuron['x']:.2f}, {neuron['y']:.2f}) marked as COVERED")

    def execute_callback(self, goal_handle):
        self.get_logger().info("Starting neural search action...")

        # Wait until a current region map is available.
        timeout = 10.0  # seconds
        start_time = self.get_clock().now().nanoseconds / 1e9
        while self.current_region_map is None:
            rclpy.spin_once(self, timeout_sec=0.5)
            current_time = self.get_clock().now().nanoseconds / 1e9
            if (current_time - start_time) > timeout:
                self.get_logger().error("Timeout waiting for region map!")
                goal_handle.abort()
                return Search.Result()

        # Main iterative search loop: continue while there is an uncovered neuron.
        while self.has_uncovered_neuron():
            next_neuron = self.select_next_neuron()
            if next_neuron is None:
                self.get_logger().info("No uncovered neuron found; ending search.")
                break

            target_pose = self.neuron_to_pose(next_neuron)
            # Navigate to the selected neuron
            nav_success = self.send_nav_goal(target_pose)
            if not nav_success:
                self.get_logger().error("Navigation to neuron failed; aborting search loop.")
                break

            # Once arrived, perform the scanning action.
            scan_result = self.perform_scanning_action()
            # (scan_result could be processed further to update a map or report object positions)

            # Mark the neuron as covered.
            self.update_neuron_state(next_neuron)
            # Optionally, update neurons based on new scan data (e.g., mark adjacent cells as covered).

            # Check if the action has been cancelled.
            if goal_handle.is_cancel_requested:
                self.get_logger().info("Search action cancelled by client.")
                goal_handle.canceL()
                break

        goal_handle.succeed()
        result = Search.Result()
        # You could attach summary data in the result if desired.
        result.final_message = "Neural search completed."
        return result

def main(args=None):
    rclpy.init(args=args)
    node = SearchActionServer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
