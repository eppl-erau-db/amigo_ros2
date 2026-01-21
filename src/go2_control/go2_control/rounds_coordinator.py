#!/usr/bin/env python3
"""
Rounds coordinator with interruptible search.
- Runs poses from pose_log.json (normal/task)
- At task poses: perform a placeholder local task (sleep 5 s)
- If /leak_detected transitions False -> True at any time, cancel current Nav2
  motion, run the Search action once, then resume from the same JSON index.

Robot Operating System (ROS 2) Humble
"""

import json
import time
from copy import deepcopy
from dataclasses import dataclass

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Bool
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

from go2_interfaces.action import Search  # your existing action definition


# ---------------- Config ----------------
DETECT_TOPIC = '/leak_detected'  # std_msgs/Bool (True => whistle present)
SEARCH_ACTION_NAME = 'search'    # go2_interfaces/action/Search
SEARCH_COOLDOWN_S = 10.0         # minimum time between *separate* searches (s)
TASK_PLACEHOLDER_SECONDS = 5.0   # "do sensors" placeholder at task poses
# ----------------------------------------


@dataclass
class PoseEntry:
    x: float; y: float; z: float
    ox: float; oy: float; oz: float; ow: float
    task_type: str  # "normal" or "task"


class RoundsCoordinator(Node):
    def __init__(self):
        super().__init__('rounds_coordinator')

        # Nav2 helper
        self.navigator = BasicNavigator()

        # Action client to the search server
        self.search_client = ActionClient(self, Search, SEARCH_ACTION_NAME)

        # Detection subscription (interrupt trigger)
        # Rising-edge tracking:
        self._detected = False          # current leak flag
        self._last_det_state = False    # previous leak flag
        self._pending_search = False    # latched event on False -> True
        self._last_search_time = 0.0    # last time a search actually ran

        self.create_subscription(Bool, DETECT_TOPIC, self._det_cb, 10)

        # State
        self._search_in_progress = False

    # ----- subscriptions -----
    def _det_cb(self, msg: Bool):
        """Detection callback with rising-edge detection.

        We want exactly one search per False->True transition on /leak_detected.
        """
        new_state = bool(msg.data)

        # Rising edge: went from False -> True
        if new_state and not self._last_det_state:
            self._pending_search = True

        self._detected = new_state
        self._last_det_state = new_state

    # ----- helpers -----
    def _spin_once(self):
        # let subscriptions/action states process without blocking
        rclpy.spin_once(self, timeout_sec=0.0)

    def _make_pose(self, entry: PoseEntry) -> PoseStamped:
        ps = PoseStamped()
        ps.header.stamp = self.navigator.get_clock().now().to_msg()
        ps.header.frame_id = 'map'
        ps.pose.position.x = entry.x
        ps.pose.position.y = entry.y
        ps.pose.position.z = entry.z
        ps.pose.orientation.x = entry.ox
        ps.pose.orientation.y = entry.oy
        ps.pose.orientation.z = entry.oz
        ps.pose.orientation.w = entry.ow
        return ps

    def _should_interrupt_for_search(self) -> bool:
        """Return True exactly once per rising edge on /leak_detected.

        Logic:
        - If a search is already in progress, do nothing.
        - Only trigger when _pending_search is True (set on False->True).
        - Enforce SEARCH_COOLDOWN_S between searches.
        - When we decide to trigger, clear _pending_search so we don't re-trigger
          while /leak_detected stays True.
        """
        if self._search_in_progress:
            return False

        # Only act on a latched rising-edge event
        if not self._pending_search:
            return False

        now = time.time()
        if (now - self._last_search_time) < SEARCH_COOLDOWN_S:
            return False

        # Consume the pending event: we will run exactly one search for this edge
        self._pending_search = False
        return True

    def _run_search_action_blocking(self, initial_pose: PoseStamped) -> bool:
        """Cancel any current nav task (already done by caller), send Search goal, wait for result."""
        # Ensure server is present
        if not self.search_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().warn("Search action server not available!")
            return False

        goal = Search.Goal()
        goal.initial_pose = initial_pose
        goal.behavior_tree = ""  # not using BT

        send_fut = self.search_client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, send_fut)
        goal_handle = send_fut.result()
        if not goal_handle or not goal_handle.accepted:
            self.get_logger().warn("Search goal rejected.")
            return False

        result_fut = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_fut)
        _ = result_fut.result()  # Search.Result (fields optional)
        self.get_logger().info("Search action complete.")
        return True

    def _interruptible_nav_to_pose(self, pose: PoseStamped, time_allowance: float = 60.0) -> TaskResult:
        """Drive to a single pose, watching for detection to interrupt."""
        self.navigator.goToPose(pose)
        start = time.time()
        while not self.navigator.isTaskComplete():
            self._spin_once()
            time.sleep(0.1)

            # interrupt if detection fired (rising-edge, once)
            if self._should_interrupt_for_search():
                self.get_logger().info("Detection fired: canceling current Nav2 task to run search.")
                try:
                    self.navigator.cancelTask()
                    self.get_logger().info("Canceling current task.")
                except Exception:
                    pass

                # current world pose as initial hint for Search
                try:
                    init_pose = self.navigator.getCurrentPose()
                except Exception:
                    init_pose = pose

                self._search_in_progress = True
                ok = self._run_search_action_blocking(init_pose)
                self._last_search_time = time.time()
                self._search_in_progress = False

                # After search, return FAILED so caller can retry/resume this same index
                return TaskResult.FAILED

            # time allowance guard
            if (time.time() - start) > time_allowance:
                self.get_logger().warn("Time allowance exceeded; canceling current Nav2 task.")
                try:
                    self.navigator.cancelTask()
                except Exception:
                    pass
                break

        return self.navigator.getResult()

    def _handle_task_failure(self, pose: PoseStamped) -> TaskResult:
        """Adapted from your original handle_task_failure, but single-pose."""
        retry_count = 0
        max_retries = 6

        while retry_count < max_retries:
            self.get_logger().info(f"Retrying pose ({retry_count + 1}/{max_retries}).")
            retry_count += 1
            result = self._interruptible_nav_to_pose(pose)
            if result == TaskResult.SUCCEEDED:
                return TaskResult.SUCCEEDED
            elif result == TaskResult.CANCELED:
                self.get_logger().warn('Retry was canceled!')
                break
            elif result == TaskResult.FAILED:
                self.get_logger().warn('Retry failed!')
                # If failure was due to an interrupting search, return FAILED to re-attempt same pose
                if self._search_in_progress is False and self._detected:
                    return TaskResult.FAILED

        self.get_logger().info("Max retries reached. Entering assisted teleop loop.")
        while rclpy.ok():
            self.navigator.assistedTeleop(time_allowance=5)
            while not self.navigator.isTaskComplete():
                self._spin_once()
                time.sleep(0.1)
            self.get_logger().info("Assisted teleop complete. Retrying the pose.")
            result = self._interruptible_nav_to_pose(pose)
            if result == TaskResult.SUCCEEDED:
                return TaskResult.SUCCEEDED
            elif result == TaskResult.CANCELED:
                self.get_logger().warn('Retry was canceled!')
                break
            elif result == TaskResult.FAILED:
                self.get_logger().warn('Retry failed!')
        return TaskResult.FAILED

    def _do_task_placeholder_interruptible(self, seconds: float) -> None:
        """Simulated sensor task that can be interrupted by search."""
        t0 = time.time()
        while (time.time() - t0) < seconds and rclpy.ok():
            self._spin_once()
            time.sleep(0.1)
            if self._should_interrupt_for_search():
                self.get_logger().info("Detection fired during task: running search.")
                # Run search with current pose
                try:
                    init_pose = self.navigator.getCurrentPose()
                except Exception:
                    init_pose = PoseStamped()
                    init_pose.header.frame_id = 'map'
                    init_pose.pose.orientation.w = 1.0

                self._search_in_progress = True
                self._run_search_action_blocking(init_pose)
                self._last_search_time = time.time()
                self._search_in_progress = False
                # After search, continue the remaining task time
                t0 = time.time()  # or comment this to resume where it left off

    # ----- main routine -----
    def run(self, pose_log_path: str = 'pose_log.json'):
        # Initial pose for localization (slam_toolbox listens to /initialpose)
        init = PoseStamped()
        init.header.stamp = self.navigator.get_clock().now().to_msg()
        init.header.frame_id = 'map'
        init.pose.orientation.w = 1.0
        self.get_logger().info("Publishing Initial Pose")
        self.navigator.setInitialPose(init)

        # Wait for Nav2 core to be active.
        # Use 'robot_localization' magic keyword so BasicNavigator
        # does NOT wait for a lifecycle localizer node like AMCL.
        # slam_toolbox is non-lifecycle and is already running.
        self.navigator.waitUntilNav2Active(localizer='robot_localization')
        self.get_logger().info("Nav2 is ready for use!")

        # Load pose log
        with open(pose_log_path, 'r') as f:
            raw = json.load(f)

        entries = []
        for e in raw:
            entries.append(PoseEntry(
                x=e["position"]["x"], y=e["position"]["y"], z=e["position"]["z"],
                ox=e["orientation"]["x"], oy=e["orientation"]["y"],
                oz=e["orientation"]["z"], ow=e["orientation"]["w"],
                task_type=e["task_type"]
            ))

        # Index-based loop so we can resume after interrupts
        idx = 0
        while idx < len(entries) and rclpy.ok():
            entry = entries[idx]
            pose = self._make_pose(entry)

            # Navigate to pose (interruptible)
            self.get_logger().info(
                f'Navigating to goal: {pose.pose.position.x} {pose.pose.position.y}...'
            )
            nav_result = self._interruptible_nav_to_pose(pose, time_allowance=120.0)
            if nav_result == TaskResult.SUCCEEDED:
                self.get_logger().info(f'Arrived at index {idx} ({entry.task_type}).')

                if entry.task_type == "task":
                    # Perform the local task (interruptible placeholder)
                    self._do_task_placeholder_interruptible(TASK_PLACEHOLDER_SECONDS)

                # Move to next entry
                idx += 1

            elif nav_result == TaskResult.CANCELED:
                self.get_logger().warn('Goal was canceled; retrying same index.')
                # retry same idx (maybe after search)
                continue

            elif nav_result == TaskResult.FAILED:
                self.get_logger().warn('Goal failed; handling failure.')
                # If failure due to search interrupt, retry same index; else run failure handler
                if self._should_interrupt_for_search():
                    # If a fresh rising-edge event just latched, let the outer
                    # loop reattempt this same index after search.
                    continue
                result = self._handle_task_failure(pose)
                if result == TaskResult.SUCCEEDED:
                    if entry.task_type == "task":
                        self._do_task_placeholder_interruptible(TASK_PLACEHOLDER_SECONDS)
                    idx += 1
                else:
                    self.get_logger().error(
                        'Failure handler did not recover; advancing to next to avoid deadlock.'
                    )
                    idx += 1
            else:
                self.get_logger().warn('Invalid result; retrying same index.')

        # Return to start
        init.header.stamp = self.navigator.get_clock().now().to_msg()
        self.navigator.goToPose(init)
        while not self.navigator.isTaskComplete():
            self._spin_once()
            time.sleep(0.1)
        self.get_logger().info("Rounds complete; returned to start.")


def main():
    rclpy.init()
    node = RoundsCoordinator()
    try:
        node.run(pose_log_path='pose_log.json')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
