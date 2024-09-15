#!/usr/bin/env python3

import yaml
import time
from copy import deepcopy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy
from go2_control.go2_velocity_commands import WirelessControl

def load_map_info():
    # Load map_info.yaml
    try:
        with open('map_info.yaml', 'r') as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        print("map_info.yaml not found.")
        return {}

def load_pose_log(current_map):
    # Load the corresponding pose log based on the current map
    pose_log_filename = f"{current_map}_poses.yaml"
    try:
        with open(pose_log_filename, 'r') as f:
            return yaml.safe_load(f) or []
    except FileNotFoundError:
        print(f"Pose log file '{pose_log_filename}' not found.")
        return []

def perform_task_at_pose(task_pose):
    # Placeholder for performing the task
    print(f"Performing task at pose: ({task_pose.pose.position.x}, {task_pose.pose.position.y})")
    time.sleep(5)  # Simulate task execution with a 5-second delay
    print("Task completed")

def handle_task_failure(navigator, task_pose):
    retry_count = 0
    max_retries = 6

    while retry_count < max_retries:
        print(f"Task failed. Retrying task ({retry_count + 1}/{max_retries}).")
        retry_count += 1
        navigator.goToPose(task_pose)
        while not navigator.isTaskComplete():
            feedback = navigator.getFeedback()
            time.sleep(0.5)
        result = navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            return TaskResult.SUCCEEDED
        elif result == TaskResult.CANCELED:
            print('Retry was canceled!')
            break
        elif result == TaskResult.FAILED:
            print('Retry failed!')

    print("Maximum retries reached. Initiating assisted teleop.")
    while True:
        navigator.assistedTeleop(time_allowance=5)
        while not navigator.isTaskComplete():
            time.sleep(0.2)
        print("Assisted teleop complete. Retrying task.")
        retry_count = 0  # Reset retry counter after assisted teleop
        navigator.goToPose(task_pose)
        while not navigator.isTaskComplete():
            feedback = navigator.getFeedback()
            time.sleep(0.5)
        result = navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            return TaskResult.SUCCEEDED
        elif result == TaskResult.CANCELED:
            print('Retry was canceled!')
            break
        elif result == TaskResult.FAILED:
            print('Retry failed!')

def main():
    rclpy.init()

    navigator = BasicNavigator()

    # Load map info
    map_data = load_map_info()

    # Assume the initial map name is "Base"
    current_map = "Base"

    while current_map:
        print(f"Processing map: {current_map}")

        # Load the corresponding pose log
        pose_log = load_pose_log(current_map)

        # Set initial pose
        initial_pose = PoseStamped()
        initial_pose.header.stamp = navigator.get_clock().now().to_msg()
        initial_pose.header.frame_id = 'map'
        initial_pose.pose.position.x = 0.0
        initial_pose.pose.position.y = 0.0
        initial_pose.pose.orientation.z = 0.0
        initial_pose.pose.orientation.w = 1.0
        navigator.setInitialPose(initial_pose)

        # Wait for navigation to fully activate
        navigator.waitUntilNav2Active()

        # Initialize a variable to hold the path segment
        path_segment = []
        pose = PoseStamped()

        for entry in pose_log:
            pose.header.stamp = navigator.get_clock().now().to_msg()
            pose.header.frame_id = 'map'
            pose.pose.position.x = entry["position"]["x"]
            pose.pose.position.y = entry["position"]["y"]
            pose.pose.position.z = entry["position"]["z"]
            pose.pose.orientation.x = entry["orientation"]["x"]
            pose.pose.orientation.y = entry["orientation"]["y"]
            pose.pose.orientation.z = entry["orientation"]["z"]
            pose.pose.orientation.w = entry["orientation"]["w"]

            if entry["task_type"] == "normal":
                path_segment.append(deepcopy(pose))
            else:
                if path_segment:
                    navigator.goThroughPoses(path_segment)
                    while not navigator.isTaskComplete():
                        feedback = navigator.getFeedback()
                        time.sleep(0.5)
                    result = navigator.getResult()
                    if result == TaskResult.SUCCEEDED:
                        print('Goal succeeded!')
                    elif result == TaskResult.CANCELED:
                        print('Goal was canceled!')
                    elif result == TaskResult.FAILED:
                        print('Goal failed!')
                        result = handle_task_failure(navigator, path_segment[-1])
                        if result == TaskResult.SUCCEEDED:
                            print('Retry succeeded!')
                        else:
                            print('Retry has failed')
                    else:
                        print('Goal has an invalid return status!')
                    path_segment = []

                # Handle the task pose
                if entry["task_type"] == "task":
                    task_pose = deepcopy(pose)
                    navigator.goToPose(task_pose)
                    while not navigator.isTaskComplete():
                        feedback = navigator.getFeedback()
                        time.sleep(0.2)
                    result = navigator.getResult()
                    if result == TaskResult.SUCCEEDED:
                        print('Navigation to task pose succeeded')
                        perform_task_at_pose(task_pose)
                    elif result == TaskResult.CANCELED:
                        print('Navigation to task pose was canceled')
                    elif result == TaskResult.FAILED:
                        print('Navigation to task pose failed')
                        result = handle_task_failure(navigator, task_pose)
                        if result == TaskResult.SUCCEEDED:
                            print('Retry succeeded!')
                            perform_task_at_pose(task_pose)
                        else:
                            print('Retry failed!')
                    else:
                        print('Navigation to task pose has an invalid return status')

                # Handle the map change pose
                if entry["task_type"] == 'map_change':
                    task_pose = deepcopy(pose)
                    map_name = entry.get('switch_to_map')
                    if not map_name or map_name not in map_data:
                        print(f"Unknown or missing map name: {map_name}")
                        continue

                    map_info = map_data[map_name]
                    map_file_path = map_info.get("filepath")
                    if not map_file_path:
                        print(f"No 'filepath' found for map '{map_name}' in map_info.yaml.")
                        continue

                    navigator.goToPose(task_pose)
                    while not navigator.isTaskComplete():
                        feedback = navigator.getFeedback()
                        time.sleep(0.2)
                    result = navigator.getResult()
                    if result == TaskResult.SUCCEEDED:
                        print('Navigation to task pose succeeded')
                        navigator.changeMap(map_file_path)
                        initial_pose.header.stamp = navigator.get_clock().now().to_msg()
                        navigator.setInitialPose(initial_pose)
                        time.sleep(2)

                        # Update current map to the new map
                        current_map = map_name
                        break  # Exit the loop to load the new map
                    elif result == TaskResult.CANCELED:
                        print('Navigation to task pose was canceled')
                    elif result == TaskResult.FAILED:
                        print('Navigation to task pose failed')
                        result = handle_task_failure(navigator, task_pose)
                        if result == TaskResult.SUCCEEDED:
                            print('Retry succeeded!')
                            navigator.changeMap(map_file_path)
                            initial_pose.header.stamp = navigator.get_clock().now().to_msg()
                            navigator.setInitialPose(initial_pose)
                            time.sleep(2)

                            # Update current map to the new map
                            current_map = map_name
                            break  # Exit the loop to load the new map
                        else:
                            print('Retry failed!')
                    else:
                        print('Navigation to task pose has an invalid return status')
            
                else:
                    print('Task type invalid')

        # If we completed the loop without changing the map, exit
        if entry["task_type"] != 'map_change':
            break

    # Go back to start
    initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    navigator.goToPose(initial_pose)
    while not navigator.isTaskComplete():
        time.sleep(0.2)

    rclpy.shutdown()

if __name__ == '__main__':
    main()
