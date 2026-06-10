#!/usr/bin/env python3
from __future__ import annotations

import os
import sys

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    EmitEvent,
    GroupAction,
    IncludeLaunchDescription,
    LogInfo,
    RegisterEventHandler,
)
from launch.events import matches_action
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LifecycleNode, Node, SetRemap
from launch_ros.event_handlers import OnStateTransition
from launch_ros.events.lifecycle import ChangeState
from lifecycle_msgs.msg import Transition

sys.path.insert(0, os.path.dirname(__file__))

from _mapping_common import declare_launch_arguments, go2_description_paths


ARGUMENT_NAMES = [
    "use_sim_time",
    "slam_map_file",
]


def generate_launch_description():
    launch_dir = os.path.dirname(__file__)
    use_sim_time = LaunchConfiguration("use_sim_time")
    slam_map_file = LaunchConfiguration("slam_map_file")
    paths = go2_description_paths()

    # slam_toolbox is a managed (lifecycle) node on Jazzy. Launched as a plain
    # Node it stays UNCONFIGURED forever (prints "Node using stack size" then
    # nothing) and never publishes map->odom. We must explicitly drive it
    # CONFIGURE -> ACTIVATE, mirroring slam_toolbox's own online_async_launch.py.
    slam_toolbox = LifecycleNode(
        package="slam_toolbox",
        executable="async_slam_toolbox_node",
        name="slam_toolbox",
        namespace="",
        output="screen",
        parameters=[
            paths["slam_toolbox_config"],
            {"use_lifecycle_manager": False, "use_sim_time": use_sim_time},
            # Cross-session "deliver swag": when slam_map_file is non-empty,
            # slam_toolbox deserializes that saved posegraph at startup and
            # continues/localizes on it. Empty (default) = fresh map (mapping).
            {"map_file_name": slam_map_file},
        ],
        remappings=[("pose", "/slam_toolbox_pose")],
    )
    slam_configure_event = EmitEvent(
        event=ChangeState(
            lifecycle_node_matcher=matches_action(slam_toolbox),
            transition_id=Transition.TRANSITION_CONFIGURE,
        )
    )
    slam_activate_event = RegisterEventHandler(
        OnStateTransition(
            target_lifecycle_node=slam_toolbox,
            start_state="configuring",
            goal_state="inactive",
            entities=[
                LogInfo(msg="[LifecycleLaunch] slam_toolbox is activating."),
                EmitEvent(
                    event=ChangeState(
                        lifecycle_node_matcher=matches_action(slam_toolbox),
                        transition_id=Transition.TRANSITION_ACTIVATE,
                    )
                ),
            ],
        )
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
            slam_activate_event,
            slam_toolbox,
            slam_configure_event,
            nav2_launch,
            explore_lite_node,
        ]
    )
