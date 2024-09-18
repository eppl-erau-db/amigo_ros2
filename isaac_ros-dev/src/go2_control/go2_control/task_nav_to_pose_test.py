#!/usr/bin/env python3

import yaml
import time
from copy import deepcopy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy
import signal

def signal_handler(sig, frame):
    print("Script interrupted by user (Ctrl+C). Cleaning up...")
    rclpy.shutdown()
    exit(0)

def load_map_info():
    try:
        with open('map_info.yaml', 'r') as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        print("map_info.yaml not found.")
        return {}

def load_pose_log(current_map):
    pose_log_filename = f"{current_map}_poses.yaml"
    try:
        with open(pose_log_filename, 'r') as f:
            return yaml.safe_load(f) or []
    except FileNotFoundError:
        print(f"Pose log file '{pose_log_filename}' not found.")
        return []

def perform_task_at_pose(task_pose):
    print(f"Performing task at pose: ({task_pose.pose.position.x}, {task_pose.pose.position.y})")
    time.sleep(5)
    print("Task completed")

def handle_nav_failure(navigator, task_pose):
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
        retry_count = 0
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

def set_initial_pose(navigator):
    initial_pose = PoseStamped()
    initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    initial_pose.header.frame_id = 'map'
    initial_pose.pose.position.x = 0.0
    initial_pose.pose.position.y = 0.0
    initial_pose.pose.orientation.z = 0.0
    initial_pose.pose.orientation.w = 1.0
    navigator.setInitialPose(initial_pose)
    return initial_pose

def create_pose_from_entry(navigator, entry):
    pose = PoseStamped()
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.header.frame_id = 'map'
    pose.pose.position.x = entry["position"]["x"]
    pose.pose.position.y = entry["position"]["y"]
    pose.pose.position.z = entry["position"]["z"]
    pose.pose.orientation.x = entry["orientation"]["x"]
    pose.pose.orientation.y = entry["orientation"]["y"]
    pose.pose.orientation.z = entry["orientation"]["z"]
    pose.pose.orientation.w = entry["orientation"]["w"]
    return pose

def process_path_segment(navigator, path_segment):
    if not path_segment:
        return
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
        result = handle_nav_failure(navigator, path_segment[-1])
        if result == TaskResult.SUCCEEDED:
            print('Retry succeeded!')
        else:
            print('Retry has failed')
    else:
        print('Goal has an invalid return status!')
    path_segment.clear()

def navigate_to_pose(navigator, pose):
    navigator.goToPose(pose)
    while not navigator.isTaskComplete():
        feedback = navigator.getFeedback()
        time.sleep(0.2)
    return navigator.getResult()

def process_task_entry(navigator, entry, pose, map_data):
    task_type = entry["task_type"]
    if task_type == "task":
        task_pose = deepcopy(pose)
        result = navigate_to_pose(navigator, task_pose)
        if result == TaskResult.SUCCEEDED:
            print('Navigation to task pose succeeded')
            perform_task_at_pose(task_pose)
        elif result == TaskResult.CANCELED:
            print('Navigation to task pose was canceled')
        elif result == TaskResult.FAILED:
            print('Navigation to task pose failed')
            result = handle_nav_failure(navigator, task_pose)
            if result == TaskResult.SUCCEEDED:
                print('Retry succeeded!')
                perform_task_at_pose(task_pose)
            else:
                print('Retry failed!')
        else:
            print('Navigation to task pose has an invalid return status')
        return False, None  # map_changed, current_map

    elif task_type == 'map_change':
        task_pose = deepcopy(pose)
        print('Starting navigation to map_change')
        result = navigate_to_pose(navigator, task_pose)
        if result == TaskResult.SUCCEEDED:
            print('Navigation to map_change pose succeeded')
            map_name = entry.get('switch_to_map')
            if not map_name or map_name not in map_data:
                print(f"Unknown or missing map name: {map_name}")
                return False, None
            return True, map_name  # Indicate that map has changed
        elif result == TaskResult.CANCELED:
            print('Navigation to map_change pose was canceled')
        elif result == TaskResult.FAILED:
            print('Navigation to map_change pose failed')
            result = handle_nav_failure(navigator, task_pose)
            if result == TaskResult.SUCCEEDED:
                print('Retry succeeded!')
                map_name = entry.get('switch_to_map')
                if not map_name or map_name not in map_data:
                    print(f"Unknown or missing map name: {map_name}")
                    return False, None
                return True, map_name
            else:
                print('Retry failed!')
        else:
            print('Navigation to map_change pose has an invalid return status')
        return False, None
    else:
        print('Task type invalid')
        return False, None

def return_to_initial_pose(navigator, initial_pose):
    initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    navigator.goToPose(initial_pose)
    while not navigator.isTaskComplete():
        time.sleep(0.2)

def main():
    rclpy.init()

    navigator = BasicNavigator()
    map_data = load_map_info()
    current_map = "Base"
    map_changed = False

    # Start Nav2 lifecycle since autostart is False
    navigator.lifecycleStartup()
    navigator.waitUntilNav2Active()

    # Set the initial pose
    initial_pose = set_initial_pose(navigator)

    while current_map:
        print(f"Processing map: {current_map}")
        pose_log = load_pose_log(current_map)

        path_segment = []

        for entry in pose_log:
            pose = create_pose_from_entry(navigator, entry)

            if entry["task_type"] == "normal":
                path_segment.append(deepcopy(pose))
            else:
                process_path_segment(navigator, path_segment)
                map_changed, new_map = process_task_entry(navigator, entry, pose, map_data)
                if map_changed:
                    current_map = new_map
                    # Shut down Nav2 before changing the map
                    navigator.lifecycleShutdown()
                    time.sleep(2)
                    # Change the map
                    map_info = map_data[current_map]
                    map_file_path = map_info.get("filepath")
                    navigator.changeMap(map_file_path)
                    # Restart Nav2 lifecycle
                    navigator.lifecycleStartup()
                    navigator.waitUntilNav2Active()
                    # Set initial pose after Nav2 is active
                    initial_pose = set_initial_pose(navigator)
                    # Clear costmaps if necessary
                    navigator.clearAllCostmaps()
                    break  # Break the for loop and restart while loop

        if map_changed:
            continue

        process_path_segment(navigator, path_segment)
        return_to_initial_pose(navigator, initial_pose)

    # Shut down Nav2 lifecycle when done
    navigator.lifecycleShutdown()
    rclpy.shutdown()

if __name__ == '__main__':
    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)
    main()
