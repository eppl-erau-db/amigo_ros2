#!/usr/bin/env python3

import yaml
import time
from copy import deepcopy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy
from go2_control.go2_velocity_commands import WirelessControl
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

def main():
    rclpy.init()

    navigator = BasicNavigator()
    map_data = load_map_info()
    current_map = "Base"

    while current_map:
        print(f"Processing map: {current_map}")
        pose_log = load_pose_log(current_map)

        initial_pose = PoseStamped()
        initial_pose.header.stamp = navigator.get_clock().now().to_msg()
        initial_pose.header.frame_id = 'map'
        initial_pose.pose.position.x = 0.0
        initial_pose.pose.position.y = 0.0
        initial_pose.pose.orientation.z = 0.0
        initial_pose.pose.orientation.w = 1.0
        navigator.setInitialPose(initial_pose)

        navigator.waitUntilNav2Active()

        path_segment = []
        pose = PoseStamped()
        
        map_changed = False  # Flag to detect map change

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

                if entry["task_type"] == 'map_change':
                    task_pose = deepcopy(pose)
                    print('starting Navigation to map_change')
                    navigator.goToPose(task_pose)
                    while not navigator.isTaskComplete():
                        feedback = navigator.getFeedback()
                        time.sleep(0.2)
                    result = navigator.getResult()
                    if result == TaskResult.SUCCEEDED:
                        print('Navigation to map_change pose succeeded')
                        map_name = entry.get('switch_to_map')
                        if not map_name or map_name not in map_data:
                            print(f"Unknown or missing map name: {map_name}")
                            continue
                        map_info = map_data[map_name]
                        map_file_path = map_info.get("filepath")
                        navigator.changeMap(map_file_path)
                        while not navigator.isTaskComplete():
                            feedback = navigator.getFeedback()
                            time.sleep(0.2)
                        result = navigator.getResult()
                        if result == TaskResult.SUCCEEDED:
                            print('Map change succeeded')
                            current_map = map_name
                            map_changed = True  # Set the flag to True
                            break  # Exit the for loop to restart the while loop
                        elif result == TaskResult.CANCELED:
                            print('map change canceled')
                        elif result == TaskResult.FAILED:
                            print('map change failed')
                    elif result == TaskResult.CANCELED:
                        print('Navigation to task pose was canceled')
                    elif result == TaskResult.FAILED:
                        print('Navigation to task pose failed')
                        result = handle_task_failure(navigator, task_pose)
                        if result == TaskResult.SUCCEEDED:
                            print('Navigation to task pose succeeded')
                            map_name = entry.get('switch_to_map')
                            if not map_name or map_name not in map_data:
                                print(f"Unknown or missing map name: {map_name}")
                                continue
                            map_info = map_data[map_name]
                            map_file_path = map_info.get("filepath")
                            navigator.changeMap(map_file_path)
                            while not navigator.isTaskComplete():
                                feedback = navigator.getFeedback()
                                time.sleep(0.2)
                            result = navigator.getResult()
                            if result == TaskResult.SUCCEEDED:
                                print('Map change succeeded')
                                current_map = map_name
                                map_changed = True  # Set the flag to True
                                break  # Exit the for loop to restart the while loop
                            elif result == TaskResult.CANCELED:
                                print('map change canceled')
                            elif result == TaskResult.FAILED:
                                print('map change failed')
                        else:
                            print('Retry failed!')
                    else:
                        print('Navigation to task pose has an invalid return status')

                else:
                    print('Task type invalid')

        # Restart while loop if map change occurred
        if map_changed:
            continue

        if path_segment:
            navigator.goThroughPoses(path_segment)
            # i = 0
            while not navigator.isTaskComplete():
                # i += 1
                feedback = navigator.getFeedback()
            #     if feedback and i % 5 == 0:
            #         print(
            #             'Estimated distance remaining to goal position: '
            #             + '{0:.3f}'.format(feedback.distance_remaining)
            #         )
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

        initial_pose.header.stamp = navigator.get_clock().now().to_msg()
        navigator.goToPose(initial_pose)
        while not navigator.isTaskComplete():
            time.sleep(0.2)
            pass

        rclpy.shutdown()

if __name__ == '__main__':
    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)
    main()
