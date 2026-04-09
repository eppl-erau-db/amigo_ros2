#!/usr/bin/env python3
"""
GPS waypoint follower that uses Nav2’s FollowWaypoints BT.

* Reads lat/lon/yaw waypoints from a YAML file (same format you use now).
* Converts each waypoint to a map‑frame PoseStamped through /fromLL.
* Sends the whole list to BasicNavigator.followWaypoints().
* Monitors progress and retries intelligently on failure.

Author: <you>
"""

import os
import sys
import time
import yaml
import rclpy
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory

from robot_localization.srv import FromLL
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from go2_control.utils.gps_utils import latLonYaw2Geopose


# --------------------------------------------------------------------------- #
# Waypoint utilities
# --------------------------------------------------------------------------- #
class YamlWaypointParser:
    """Parse a YAML file into a list of geographic_msgs/GeoPose objects."""

    def __init__(self, wps_file_path: str) -> None:
        with open(wps_file_path, "r") as f:
            self.wps_dict = yaml.safe_load(f)

    def to_geoposes(self):
        geoposes = []
        for wp in self.wps_dict["waypoints"]:
            geoposes.append(
                latLonYaw2Geopose(wp["latitude"], wp["longitude"], wp["yaw"])
            )
        return geoposes


# --------------------------------------------------------------------------- #
# Navigation helper for retries
# --------------------------------------------------------------------------- #
def handle_task_failure(navigator: BasicNavigator,
                        remaining_wps: list[PoseStamped],
                        max_retries: int = 6) -> TaskResult:
    """
    Retry the remaining waypoint list up to max_retries; if it still fails,
    switch to assisted teleop and then try again until success or cancel.

    Returns the final TaskResult.
    """
    retry_count = 0
    while retry_count < max_retries:
        print(f"[Retry] Attempt {retry_count + 1}/{max_retries}")
        retry_count += 1

        navigator.followWaypoints(remaining_wps)
        while not navigator.isTaskComplete():
            _ = navigator.getFeedback()
            time.sleep(0.5)

        result = navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            return result
        elif result == TaskResult.CANCELED:
            print("Retry was canceled by operator.")
            return result
        else:
            print("Retry failed.")

    # All automatic retries exhausted: engage assisted tele‑op
    print("[Retry] Max retries reached — starting assisted tele‑operation.")
    while True:
        navigator.assistedTeleop(time_allowance=5)
        while not navigator.isTaskComplete():
            time.sleep(0.2)

        print("Assisted tele‑op finished, attempting waypoints again...")
        navigator.followWaypoints(remaining_wps)
        while not navigator.isTaskComplete():
            _ = navigator.getFeedback()
            time.sleep(0.5)

        result = navigator.getResult()
        if result in (TaskResult.SUCCEEDED, TaskResult.CANCELED):
            return result
        print("Assisted tele‑op retry failed; repeating…")


# --------------------------------------------------------------------------- #
# Main commander class
# --------------------------------------------------------------------------- #
class GpsWaypointCommander(Node):
    """
    A thin node that:
    1. Converts GPS coordinates to map poses with /fromLL.
    2. Hands those poses to Nav2’s waypoint follower.
    """

    def __init__(self, wps_file_path: str):
        super().__init__("gps_wp_commander")

        # --- Nav2 navigator -------------------------------------------------- #
        self.navigator = BasicNavigator()          # leave default BT node name
        self.navigator.waitUntilNav2Active(localizer="robot_localization")
        self.get_logger().info("Nav2 stack is active.")

        # --- Waypoints ------------------------------------------------------- #
        self.waypoints_geo = YamlWaypointParser(wps_file_path).to_geoposes()

        # --- /fromLL service client ----------------------------------------- #
        self.localizer = self.create_client(FromLL, "/fromLL")
        while not self.localizer.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("/fromLL service unavailable, waiting…")

        # Convert immediately so that failures happen before we begin moving
        self.waypoints_map = self._convert_all_to_map()

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #
    def _convert_all_to_map(self) -> list[PoseStamped]:
        """Convert each GeoPose in self.waypoints_geo to a map PoseStamped."""
        map_poses: list[PoseStamped] = []

        for idx, wp in enumerate(self.waypoints_geo):
            req = FromLL.Request()
            req.ll_point.longitude = wp.position.longitude
            req.ll_point.latitude = wp.position.latitude
            req.ll_point.altitude = wp.position.altitude

            self.get_logger().info(
                f"[LL→map] #{idx:02d}: "
                f"lon={req.ll_point.longitude:.8f}, "
                f"lat={req.ll_point.latitude:.8f}"
            )

            future = self.localizer.call_async(req)
            rclpy.spin_until_future_complete(self, future)

            pose = PoseStamped()
            pose.header.frame_id = "map"
            pose.header.stamp = self.get_clock().now().to_msg()
            pose.pose.position = future.result().map_point
            pose.pose.orientation = wp.orientation  # preserve desired yaw

            map_poses.append(pose)

            self.get_logger().info(
                f"[LL→map]    ↳ x={pose.pose.position.x:.3f}, "
                f"y={pose.pose.position.y:.3f}"
            )

        return map_poses

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def execute(self):
        """Send all waypoints and monitor progress / handle failures."""
        wps_all = self.waypoints_map

        self.get_logger().info(f"Dispatching {len(wps_all)} waypoints…")
        self.navigator.followWaypoints(wps_all)

        last_feedback = None
        while not self.navigator.isTaskComplete():
            fb = self.navigator.getFeedback()
            if fb:                            # fb.current_waypoint is int
                last_feedback = fb
                self.get_logger().info(
                    f"Currently at waypoint #{fb.current_waypoint}"
                )
            time.sleep(0.5)

        result = self.navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            self.get_logger().info("All waypoints reached successfully 🎉")
            return

        # --- Failure handling ------------------------------------------------ #
        if result == TaskResult.FAILED:
            self.get_logger().warn("Waypoint following failed!")

            # Determine where to resume
            if last_feedback:
                resume_index = last_feedback.current_waypoint
                resume_index = max(resume_index, 0)
            else:
                resume_index = 0

            remaining = wps_all[resume_index:]
            self.get_logger().info(
                f"Retrying from waypoint #{resume_index} "
                f"({len(remaining)} remaining)."
            )

            retry_result = handle_task_failure(self.navigator, remaining)
            if retry_result == TaskResult.SUCCEEDED:
                self.get_logger().info("Retry succeeded 🚀")
            else:
                self.get_logger().error("Retry gave up 😞")

        elif result == TaskResult.CANCELED:
            self.get_logger().warn("Waypoint following was canceled!")


# --------------------------------------------------------------------------- #
# main()
# --------------------------------------------------------------------------- #
def main():
    rclpy.init()

    default_yaml = os.path.join(
        get_package_share_directory("go2_control"),
        "config",
        "demo_waypoints.yaml",
    )
    yaml_path = sys.argv[1] if len(sys.argv) > 1 else default_yaml

    commander = GpsWaypointCommander(yaml_path)
    commander.execute()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
