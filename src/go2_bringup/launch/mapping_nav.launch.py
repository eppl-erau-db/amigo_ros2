#!/usr/bin/env python3
from __future__ import annotations

import os
import sys

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import EmitEvent, GroupAction, IncludeLaunchDescription, LogInfo, RegisterEventHandler
from launch.conditions import IfCondition
from launch.events import matches_action
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LifecycleNode, Node, SetRemap
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.event_handlers import OnStateTransition
from launch_ros.events.lifecycle import ChangeState
from lifecycle_msgs.msg import Transition

sys.path.insert(0, os.path.dirname(__file__))

from _mapping_common import (
    RMW_CYCLONEDDS_LOG_LEVEL,
    conditional_log_level_arg,
    declare_launch_arguments,
    go2_description_paths,
    with_cyclonedds_warning_filter,
)


ARGUMENT_NAMES = [
    "use_sim_time",
    "debug_odometry",
]


def generate_launch_description():
    launch_dir = os.path.dirname(__file__)
    use_sim_time = LaunchConfiguration("use_sim_time")
    debug_odometry = LaunchConfiguration("debug_odometry")
    debug_odometry_bool = ParameterValue(debug_odometry, value_type=bool)
    paths = go2_description_paths()

    slam_toolbox = LifecycleNode(
        package="slam_toolbox",
        executable="async_slam_toolbox_node",
        name="slam_toolbox",
        namespace="",
        output="screen",
        parameters=[
            paths["slam_toolbox_config"],
            {
                "use_lifecycle_manager": False,
                "use_sim_time": use_sim_time,
                "debug_logging": debug_odometry_bool,
            },
        ],
        remappings=[("pose", "/slam_toolbox_pose")],
        arguments=with_cyclonedds_warning_filter(
            log_levels=[conditional_log_level_arg("slam_toolbox")]
        ),
    )
    configure_slam_toolbox = EmitEvent(
        event=ChangeState(
            lifecycle_node_matcher=matches_action(slam_toolbox),
            transition_id=Transition.TRANSITION_CONFIGURE,
        )
    )
    activate_slam_toolbox = RegisterEventHandler(
        OnStateTransition(
            target_lifecycle_node=slam_toolbox,
            start_state="configuring",
            goal_state="inactive",
            entities=[
                LogInfo(msg="[mapping_nav] Activating slam_toolbox lifecycle node"),
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
                    "log_level": RMW_CYCLONEDDS_LOG_LEVEL,
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
        arguments=with_cyclonedds_warning_filter(),
    )

    return LaunchDescription(
        declare_launch_arguments(ARGUMENT_NAMES, launch_dir) +
        [
            LogInfo(
                condition=IfCondition(debug_odometry),
                msg=(
                    "[mapping_nav] debug_odometry enabled: slam_toolbox debug_logging is on; "
                    "Nav2 still consumes EKF /odom and TF map->odom->base_footprint"
                ),
            ),
            slam_toolbox,
            configure_slam_toolbox,
            activate_slam_toolbox,
            nav2_launch,
            explore_lite_node,
        ]
    )
