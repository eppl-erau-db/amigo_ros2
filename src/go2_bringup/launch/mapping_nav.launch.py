#!/usr/bin/env python3
from __future__ import annotations

import os
import sys

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import GroupAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, SetRemap

sys.path.insert(0, os.path.dirname(__file__))

from _mapping_common import declare_launch_arguments, go2_description_paths


ARGUMENT_NAMES = [
    "use_sim_time",
]


def generate_launch_description():
    launch_dir = os.path.dirname(__file__)
    use_sim_time = LaunchConfiguration("use_sim_time")
    paths = go2_description_paths()

    slam_toolbox = Node(
        package="slam_toolbox",
        executable="async_slam_toolbox_node",
        name="slam_toolbox",
        output="screen",
        parameters=[paths["slam_toolbox_config"]],
        remappings=[("pose", "/slam_toolbox_pose")],
    )
    nav2_launch = GroupAction(
        actions=[
            SetRemap(src="cmd_vel", dst="/motion/candidate/nav"),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(
                        get_package_share_directory("nav2_bringup"),
                        "launch",
                        "navigation_launch.py",
                    )
                ),
                launch_arguments={
                    "params_file": paths["nav2_cfg"],
                    "use_sim_time": use_sim_time,
                    "localization": "false",
                }.items(),
            ),
        ]
    )
    explore_lite_node = Node(
        package="explore_lite",
        executable="explore",
        name="explore_node",
        output="screen",
        parameters=[
            paths["explore_cfg"],
            {
                "use_sim_time": use_sim_time,
                "start_paused": True,
                "return_to_init": False,
                "costmap_topic": "map",
                "costmap_updates_topic": "map_updates",
            },
        ],
    )

    return LaunchDescription(
        declare_launch_arguments(ARGUMENT_NAMES, launch_dir) +
        [
            slam_toolbox,
            nav2_launch,
            explore_lite_node,
        ]
    )
