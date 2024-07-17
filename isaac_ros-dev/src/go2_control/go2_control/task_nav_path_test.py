#!/usr/bin/env python3

import json
import time
from copy import deepcopy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy


def perform_task_at_pose(task_pose):
    # Placeholder for performing the task
    # Implement the actual task logic here
    print(f"Performing task at pose: ({task_pose.pose.position.x}, {task_pose.pose.position.y})")
    time.sleep(5)  # Simulate task execution with a 5-second delay
    print("Task completed")


def main():
    rclpy.init()

    navigator = BasicNavigator()

    # Load the pose log from JSON file
    with open('pose_log.json', 'r') as f:
        pose_log = json.load(f)

    # Set our demo's initial pose
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
                # Use getPathThroughPoses to get the path
                path = navigator.getPathThroughPoses(initial_pose, path_segment, use_start=False)
                if path:
                    # Use smoothPath to smooth the path
                    smoothed_path = navigator.smoothPath(path, check_for_collision=True)
                    if smoothed_path:
                        print(f"Following smoothed path segment with {len(smoothed_path.poses)} poses.")
                        navigator.followPath(smoothed_path)
                        i = 0
                        while not navigator.isTaskComplete():
                            i += 1
                            feedback = navigator.getFeedback()
                            if feedback and i % 5 == 0:
                                print(
                                    'Estimated distance remaining to goal position: '
                                    + '{0:.3f}'.format(feedback.distance_to_goal)
                                    + '\nCurrent speed of the robot: '
                                    + '{0:.3f}'.format(feedback.speed)
                                )
                        result = navigator.getResult()
                        if result == TaskResult.SUCCEEDED:
                            print('Goal succeeded!')
                        elif result == TaskResult.CANCELED:
                            print('Goal was canceled!')
                        elif result == TaskResult.FAILED:
                            print('Goal failed!')
                        else:
                            print('Goal has an invalid return status!')
                path_segment = []

            # Handle the task pose
            if entry["task_type"] == "task":
                task_pose = deepcopy(pose)
                navigator.goToPose(task_pose)
                while not navigator.isTaskComplete():
                    feedback = navigator.getFeedback()
                    if feedback:
                        print('Executing task at pose, distance remaining: {:.3f}'.format(feedback.distance_remaining))
                result = navigator.getResult()
                if result == TaskResult.SUCCEEDED:
                    print('Navigation to task pose succeeded')
                    perform_task_at_pose(task_pose)
                elif result == TaskResult.CANCELED:
                    print('Navigation to task pose was canceled')
                elif result == TaskResult.FAILED:
                    print('Navigation to task pose failed')
                else:
                    print('Navigation to task pose has an invalid return status')
            elif entry["task_type"] == "exit_pose":
                exit_pose = deepcopy(pose)
                navigator.goToPose(exit_pose)
                while not navigator.isTaskComplete():
                    feedback = navigator.getFeedback()
                    if feedback:
                        print('Executing task at exit pose, distance remaining: {:.3f}'.format(feedback.distance_remaining))
                result = navigator.getResult()
                if result == TaskResult.SUCCEEDED:
                    print('Navigation to exit pose succeeded')
                elif result == TaskResult.CANCELED:
                    print('Navigation to exit pose was canceled')
                elif result == TaskResult.FAILED:
                    print('Navigation to exit pose failed')
                else:
                    print('Navigation to exit pose has an invalid return status')
            else:
                print('Task type invalid')
    # Follow any remaining path segment
    if path_segment:
        path = navigator.getPathThroughPoses(initial_pose, path_segment, use_start=False)
        if path:
            smoothed_path = navigator.smoothPath(path, check_for_collision=False)
            if smoothed_path:
                print(f"Following final smoothed path segment with {len(smoothed_path.poses)} poses.")
                navigator.followPath(smoothed_path)
                i = 0
                while not navigator.isTaskComplete():
                    i += 1
                    feedback = navigator.getFeedback()
                    if feedback and i % 5 == 0:
                        print(
                            'Estimated distance remaining to goal position: '
                            + '{0:.3f}'.format(feedback.distance_to_goal)
                            + '\nCurrent speed of the robot: '
                            + '{0:.3f}'.format(feedback.speed)
                        )
                result = navigator.getResult()
                if result == TaskResult.SUCCEEDED:
                    print('Goal succeeded!')
                elif result == TaskResult.CANCELED:
                    print('Goal was canceled!')
                elif result == TaskResult.FAILED:
                    print('Goal failed!')
                else:
                    print('Goal has an invalid return status!')

    # Go back to start
    initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    navigator.goToPose(initial_pose)
    while not navigator.isTaskComplete():
        pass

    rclpy.shutdown()

    exit(0)

if __name__ == '__main__':
    main()
