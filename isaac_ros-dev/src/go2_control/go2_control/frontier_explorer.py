#!/usr/bin/env python3

import math
import sys
import time
import random
import numpy as np

import rclpy
from rclpy.node import Node

from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import PoseStamped, TransformStamped
from tf2_ros import Buffer, TransformListener
from tf2_geometry_msgs import do_transform_pose


# Nav2 Simple Commander
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

# OPTIONAL: If you want to programmatically save the map using a service call
from nav2_msgs.srv import SaveMap

# ----------------------------------------------------------------------
# Below are the “frontier detection” & grouping logic that we pick
# from your existing code snippet. We only keep the relevant functions
# for frontier detection, grouping, and picking a centroid. We do NOT
# do BFS or A* for actual path planning (Nav2 does that).
# ----------------------------------------------------------------------

def frontierB(matrix):
    """
    Mark frontier cells (value=2) where known=0 neighbors unknown=<0
    """
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0.0:
                if i > 0 and matrix[i-1][j] < 0:
                    matrix[i][j] = 2
                elif i < len(matrix)-1 and matrix[i+1][j] < 0:
                    matrix[i][j] = 2
                elif j > 0 and matrix[i][j-1] < 0:
                    matrix[i][j] = 2
                elif j < len(matrix[i])-1 and matrix[i][j+1] < 0:
                    matrix[i][j] = 2
    return matrix

def assign_groups(matrix):
    group = 1
    groups = {}
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 2:
                group = dfs(matrix, i, j, group, groups)
    return matrix, groups

def dfs(matrix, i, j, group, groups):
    if i < 0 or i >= len(matrix) or j < 0 or j >= len(matrix[0]):
        return group
    if matrix[i][j] != 2:
        return group
    if group not in groups:
        groups[group] = []
    groups[group].append((i, j))

    matrix[i][j] = 0  # Mark visited
    # Explore neighbors (8-directional)
    for nr in [i-1, i, i+1]:
        for nc in [j-1, j, j+1]:
            if (nr, nc) != (i, j):
                group = dfs(matrix, nr, nc, group, groups)
    return group + 1

def fGroups(groups):
    # Sort frontier groups by size, descending
    sorted_groups = sorted(groups.items(), key=lambda x: len(x[1]), reverse=True)
    # Take up to 5 largest frontier groups
    top_five_groups = [g for g in sorted_groups[:5] if len(g[1]) > 2]
    return top_five_groups

def calculate_centroid(x_coords, y_coords):
    n = len(x_coords)
    sum_x = sum(x_coords)
    sum_y = sum(y_coords)
    mean_x = sum_x / n
    mean_y = sum_y / n
    return (int(mean_x), int(mean_y))

def costmap(data, width, height, resolution, expansion_size=0):
    """
    Optionally expand obstacles. For simplicity, you can set expansion_size=0
    or keep your existing logic if desired.
    """
    data = np.array(data).reshape(height, width)
    if expansion_size <= 0:
        return data
    wall = np.where(data == 100)
    for i in range(-expansion_size, expansion_size+1):
        for j in range(-expansion_size, expansion_size+1):
            if i == 0 and j == 0:
                continue
            x = wall[0] + i
            y = wall[1] + j
            x = np.clip(x, 0, height-1)
            y = np.clip(y, 0, width-1)
            data[x, y] = 100
    return data

def find_frontiers_and_pick_centroid(occ_data, width, height, resolution, origin_x, origin_y, robot_row, robot_col):
    """
    The main frontier logic:
    1. Convert data to local 2D array (with optional costmap expansion).
    2. Mark frontiers with '2' using frontierB().
    3. Group them with assign_groups().
    4. Filter / pick up to top 5 groups with fGroups().
    5. Pick the largest group’s centroid (or some other heuristic).
    Returns (map_x, map_y) if found, else None
    """
    # Reshape
    arr = np.array(occ_data).reshape(height, width)
    # We can optionally expand obstacles or keep it simple
    arr = costmap(arr, width, height, resolution, expansion_size=0)

    # Mark the robot’s current cell as free (0) if you like
    if 0 <= robot_row < height and 0 <= robot_col < width:
        arr[robot_row, robot_col] = 0

    # frontierB => mark frontier cells with '2'
    arr = frontierB(arr)
    
    # Group them
    arr, groups = assign_groups(arr)
    groups = fGroups(groups)
    if len(groups) == 0:
        return None

    # Example: pick the FIRST frontier group in the sorted list
    # You could also do more advanced logic
    group_id, frontier_cells = groups[0]

    # Calculate centroid in grid coords
    rx = [fc[0] for fc in frontier_cells]
    ry = [fc[1] for fc in frontier_cells]
    (cent_r, cent_c) = calculate_centroid(rx, ry)

    # Convert back to map coordinates
    # row => Y, col => X
    cent_x = origin_x + (cent_c * resolution)
    cent_y = origin_y + (cent_r * resolution)
    return (cent_x, cent_y)

# ----------------------------------------------------------------------
# Node that orchestrates Frontier Detection + Nav2 Simple Commander
# ----------------------------------------------------------------------
class FrontierExplorer(Node):
    def __init__(self):
        super().__init__('frontier_explorer_nav2')

        # Subscribe to map + odom (for robot pose estimate)
        self.map_sub = self.create_subscription(OccupancyGrid, 'map', self.map_callback, 10)
        # self.odom_sub = self.create_subscription(Odometry, 'odom', self.odom_callback, 10)
        # TF2 buffer + listener for transforms
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.latest_map = None
        # We store map info
        self.latest_map = None
        self.resolution = None
        self.origin_x = 0.0
        self.origin_y = 0.0
        self.width = 0
        self.height = 0
        self.map_data = None
        
        # # Robot pose (roughly from odom)
        # self.robot_x = 0.0
        # self.robot_y = 0.0

        # For exploration loop
        self.is_exploring = False
        self.timer = self.create_timer(2.0, self.exploration_loop)

        # Nav2 Simple Commander
        self.navigator = BasicNavigator()
        self.navigator.waitUntilNav2Active()

        self.get_logger().info("FrontierExplorer node initialized. Waiting for map & odom data...")

    def map_callback(self, msg):
        # Store map data
        self.latest_map = msg
        self.resolution = msg.info.resolution
        self.origin_x = msg.info.origin.position.x
        self.origin_y = msg.info.origin.position.y
        self.width = msg.info.width
        self.height = msg.info.height
        self.map_data = msg.data

    # def odom_callback(self, msg):
    #     # Basic estimate of robot pose from /odom
    #     self.robot_x = msg.pose.pose.position.x
    #     self.robot_y = msg.pose.pose.position.y
    #     # Not strictly needed, but you could also parse orientation if you like

    def exploration_loop(self):
        if not self.latest_map:
            return
        
        # 1) Get the robot's pose in map frame via TF
        try:
            # We'll look up transform from 'map' to 'base_footprint'
            # or vice versa. Usually we want 'map' -> 'base_footprint'.
            # If your base frame is 'base_link', adjust accordingly.
            now = rclpy.time.Time()
            transform = self.tf_buffer.lookup_transform(
                'map',      # target_frame
                'base_footprint',  # source_frame
                rclpy.time.Time(),  # time
                timeout_sec=2.0
            )
            
            # We can create a PoseStamped at the origin of base_footprint
            base_pose = PoseStamped()
            base_pose.header.frame_id = 'base_footprint'
            base_pose.pose.orientation.w = 1.0  # identity rotation

            # Transform that pose into the map frame
            map_pose = do_transform_pose(base_pose, transform)

            # Now map_pose.pose.position.x, .y is the robot in map frame
            robot_x = map_pose.pose.position.x
            robot_y = map_pose.pose.position.y
            
        except Exception as e:
            self.get_logger().warn(f"Could not lookup transform: {str(e)}")
            return

        # Convert robot's (x,y) in map frame => row, col in occupancy grid
        # Be careful with signs or if /odom isn’t aligned with /map exactly
        robot_col = int((robot_x - self.origin_x) / self.resolution)
        robot_row = int((robot_y - self.origin_y) / self.resolution)


        # 1. Find frontier centroid
        frontier = find_frontiers_and_pick_centroid(
            occ_data=self.map_data,
            width=self.width,
            height=self.height,
            resolution=self.resolution,
            origin_x=self.origin_x,
            origin_y=self.origin_y,
            robot_row=robot_row,
            robot_col=robot_col
        )

        if frontier is None:
            self.get_logger().info("No more frontiers found. Exploration complete!")
            # Optionally save the map here:
            self.save_map("/tmp/my_explored_map")
            self.navigator.lifecycleShutdown()
            sys.exit(0)
            return

        # 2. Send a goal to Nav2 (using BasicNavigator)
        (fx, fy) = frontier
        goal_pose = PoseStamped()
        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = self.get_clock().now().to_msg()
        goal_pose.pose.position.x = fx
        goal_pose.pose.position.y = fy
        goal_pose.pose.orientation.w = 1.0  # face forward

        self.get_logger().info(f"Sending robot to frontier: x={fx:.2f}, y={fy:.2f}")
        self.is_exploring = True
        self.navigator.goToPose(goal_pose)

        # Monitor the goal asynchronously; in real code, you might do this in a separate callback
        # or logic that waits for completion
        while not self.navigator.isTaskComplete():
            feedback = self.navigator.getFeedback()
            if feedback:
                est_time = feedback.estimated_time_remaining
                self.get_logger().info(f"Moving to frontier. ETA: {est_time.sec} seconds left.")
            time.sleep(1.0)

        # Check result
        result = self.navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            self.get_logger().info("Arrived at frontier. Will look for next frontier...")
        elif result == TaskResult.FAILED:
            self.get_logger().warn("Navigation to frontier failed. Trying next frontier anyway.")
        elif result == TaskResult.CANCELED:
            self.get_logger().warn("Goal was canceled. Attempting next frontier anyway.")

        # Reset is_exploring so the timer can pick the next frontier
        self.is_exploring = False

    # (Optional) Programmatic way to save the map
    #
    # If you prefer, you can just run the map_saver_cli tool externally:
    #   ros2 run nav2_map_server map_saver_cli -f <map_name>
    #
    # Or call this service in code:
    #
    def save_map(self, map_path):
        client = self.create_client(SaveMap, '/map_saver/save_map')
        if not client.wait_for_service(timeout_sec=10.0):
            self.get_logger().error("Map Saver service not available!")
            return
        req = SaveMap.Request()
        req.map_topic = 'map'
        req.map_url = map_path
        future = client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            self.get_logger().info(f"Map saved to {map_path}")
        else:
            self.get_logger().error("Failed to save the map!")


def main(args=None):
    rclpy.init(args=args)
    node = FrontierExplorer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
