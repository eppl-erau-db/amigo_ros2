#!/usr/bin/env python3

import json
import time
from copy import deepcopy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy
from rclpy.action import ActionClient
from go2_interfaces.action import Search


def perform_task_at_pose(task_pose, search_client_node):
    # Trigger the "search" action.
    action_client = ActionClient(search_client_node, Search, 'search')
    if not action_client.wait_for_server(timeout_sec=5.0):
        print("Search action server not available!")
        return

    goal_msg = Search.Goal()
    goal_msg.initial_pose = task_pose 
    goal_msg.behavior_tree = ""  # no behavior tree is used

    send_goal_future = action_client.send_goal_async(goal_msg)
    rclpy.spin_until_future_complete(search_client_node, send_goal_future)
    goal_handle = send_goal_future.result()
    if not goal_handle.accepted:
        print("Search goal rejected!")
        return

    get_result_future = goal_handle.get_result_async()
    rclpy.spin_until_future_complete(search_client_node, get_result_future)
    result = get_result_future.result().result
    print("Search action complete!")


def handle_task_failure(navigator, task_pose):
    retry_count = 0
    max_retries = 6

    while retry_count < max_retries:
        print(f"Task failed. Retrying task ({retry_count + 1}/{max_retries}).")
        retry_count += 1
        navigator.goToPose(task_pose)
        while not navigator.isTaskComplete():
            _ = navigator.getFeedback()
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
            _ = navigator.getFeedback()
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

    # Create the navigator and a separate node for the search action client.
    navigator = BasicNavigator()
    search_client_node = rclpy.create_node('search_client_node')

    # Load the pose log from JSON file.
    with open('pose_log.json', 'r') as f:
        pose_log = json.load(f)

    # Set our demo's initial pose.
    initial_pose = PoseStamped()
    initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    initial_pose.header.frame_id = 'map'
    initial_pose.pose.position.x = 0.0
    initial_pose.pose.position.y = 0.0
    initial_pose.pose.orientation.z = 0.0
    initial_pose.pose.orientation.w = 1.0
    navigator.setInitialPose(initial_pose)

    # Wait for navigation to fully activate.
    navigator.waitUntilNav2Active()

    # Initialize a variable to hold the path segment.
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
                # Navigate through the poses.
                navigator.goThroughPoses(path_segment)
                while not navigator.isTaskComplete():
                    _ = navigator.getFeedback()
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

            # Handle the task pose.
            if entry["task_type"] == "task":
                task_pose = deepcopy(pose)
                navigator.goToPose(task_pose)
                while not navigator.isTaskComplete():
                    _ = navigator.getFeedback()
                    time.sleep(0.2)
                result = navigator.getResult()
                if result == TaskResult.SUCCEEDED:
                    print('Navigation to task pose succeeded')
                    perform_task_at_pose(task_pose, search_client_node)
                elif result == TaskResult.CANCELED:
                    print('Navigation to task pose was canceled')
                elif result == TaskResult.FAILED:
                    print('Navigation to task pose failed')
                    result = handle_task_failure(navigator, task_pose)
                    if result == TaskResult.SUCCEEDED:
                        print('Retry succeeded!')
                        perform_task_at_pose(task_pose, search_client_node)
                    else:
                        print('Retry failed!')
                else:
                    print('Navigation to task pose has an invalid return status')
            else:
                print('Task type invalid')

    # Follow any remaining path segment.
    if path_segment:
        navigator.goThroughPoses(path_segment)
        while not navigator.isTaskComplete():
            _ = navigator.getFeedback()
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

    # Go back to start.
    initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    navigator.goToPose(initial_pose)
    while not navigator.isTaskComplete():
        time.sleep(0.2)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
