#! /usr/bin/env python3

import json
import time
from copy import deepcopy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy
from rclpy.action import ActionClient
from nav2_msgs.action import Spin
from builtin_interfaces.msg import Duration
import math


def perform_task_at_pose(task_pose):
    # Placeholder for performing the task
    # Implement the actual task logic here
    print(f"Performing task at pose: ({task_pose.pose.position.x}, {task_pose.pose.position.y})")
    time.sleep(5)  # Simulate task execution with a 5-second delay
    print("Task completed")


def spin_robot(navigator, yaw_degrees=180, time_allowance_sec=30):
    action_client = ActionClient(navigator, Spin, 'spin')

    if not action_client.wait_for_server(timeout_sec=10.0):
        navigator.get_logger().error('Spin action server not available')
        return

    goal_msg = Spin.Goal()
    goal_msg.target_yaw = math.radians(yaw_degrees)  # Convert degrees to radians
    goal_msg.time_allowance = Duration(sec=time_allowance_sec)

    future = action_client.send_goal_async(goal_msg)
    rclpy.spin_until_future_complete(navigator, future)

    if future.result() is not None:
        navigator.get_logger().info('Spin action goal accepted.')
        result_future = future.result().get_result_async()
        rclpy.spin_until_future_complete(navigator, result_future)
        return result_future.result().status
    else:
        navigator.get_logger().error('Spin action goal rejected.')
        return None


def main():
    rclpy.init()

    navigator = BasicNavigator()
    
    # Load the pose log from JSON file
    with open('pose_log.json', 'r') as f:
        pose_log = json.load(f)

    # Set our demo's initial pose
    initial_pose = PoseStamped()
    initial_pose.header.frame_id = 'map'
    initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    initial_pose.pose.position.x = 0.0
    initial_pose.pose.position.y = 0.0
    initial_pose.pose.orientation.z = 0.0
    initial_pose.pose.orientation.w = 1.0
    # navigator.setInitialPose(initial_pose)

    # Wait for navigation to fully activate
    navigator.waitUntilNav2Active()

    # Set up all poses (waypoints and task poses)
    all_poses = []
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

        all_poses.append(deepcopy(pose))

    # Follow all poses in order, handling tasks when encountered
    for pose in all_poses:
        print(f"Going to pose: {pose.pose.position.x}, {pose.pose.position.y}")
        navigator.goToPose(pose)
        while not navigator.isTaskComplete():
            feedback = navigator.getFeedback()
            if feedback:
                print('Navigating to pose, distance remaining: {:.3f}'.format(feedback.distance_remaining))

        result = navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            print('Reached pose successfully')
            # Perform task if this pose is a task pose
            for entry in pose_log:
                if entry["position"]["x"] == pose.pose.position.x and entry["position"]["y"] == pose.pose.position.y:
                    if entry["task_type"] == "task":
                        perform_task_at_pose(pose)
                        spin_result = spin_robot(navigator)
                        if spin_result is not None and spin_result == TaskResult.SUCCEEDED:
                            print('Spin succeeded')
                        else:
                            print('Spin failed or was rejected')
        elif result == TaskResult.CANCELED:
            print('Navigation to pose was canceled')
        elif result == TaskResult.FAILED:
            print('Navigation to pose failed')
        else:
            print('Navigation to pose has an invalid return status')

    # Go back to start
    initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    navigator.goToPose(initial_pose)
    while not navigator.isTaskComplete():
        pass

    rclpy.shutdown()

    exit(0)


if __name__ == '__main__':
    main()
