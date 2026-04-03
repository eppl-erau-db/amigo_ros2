#!/usr/bin/env python3
from __future__ import annotations

import os
import sys

from ament_index_python.packages import get_package_prefix, get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

sys.path.insert(0, os.path.dirname(__file__))

from _mapping_common import declare_launch_arguments, go2_description_paths


ARGUMENT_NAMES = [
    "use_sim_time",
    "person_follow_unitree_network_interface",
    "startup_motion_mode",
    "startup_motion_gait",
    "startup_motion_wait_s",
    "startup_motion_retries",
    "startup_motion_retry_interval_s",
    "zed_follow_params_path",
]


def generate_launch_description():
    launch_dir = os.path.dirname(__file__)
    use_sim_time = LaunchConfiguration("use_sim_time")
    person_follow_unitree_network_interface = LaunchConfiguration(
        "person_follow_unitree_network_interface"
    )
    startup_motion_mode = LaunchConfiguration("startup_motion_mode")
    startup_motion_gait = LaunchConfiguration("startup_motion_gait")
    startup_motion_wait_s = LaunchConfiguration("startup_motion_wait_s")
    startup_motion_retries = LaunchConfiguration("startup_motion_retries")
    startup_motion_retry_interval_s = LaunchConfiguration("startup_motion_retry_interval_s")
    zed_follow_params_path = LaunchConfiguration("zed_follow_params_path")

    paths = go2_description_paths()
    motion_mode_switcher_executable = os.path.join(
        get_package_prefix("go2_driver"),
        "lib",
        "go2_driver",
        "go2_motion_mode_switcher",
    )

    robot_description = ParameterValue(
        Command(
            [
                "xacro ",
                paths["urdf_path"],
                " camera_name:=zed",
                " camera_model:=zedxm",
                " use_zed_localization:=false",
            ]
        ),
        value_type=str,
    )

    robot_state_pub = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": use_sim_time,
            }
        ],
    )
    state_pub = Node(
        package="go2_control",
        executable="go2_state",
        name="go2_state",
        output="screen",
    )
    odom_node = Node(
        package="go2_control",
        executable="odom_node",
        name="odom_node",
        output="screen",
    )
    base_tf = Node(
        package="go2_control",
        executable="base_to_base_tf",
        name="base_to_base_tf",
        output="screen",
    )
    go2_driver = Node(
        package="go2_driver",
        executable="go2_driver_node",
        name="go2_driver_node",
        output="screen",
    )
    ekf_node = Node(
        package="robot_localization",
        executable="ekf_node",
        name="ekf_filter_node",
        output="screen",
        parameters=[paths["ekf_cfg"], {"use_sim_time": use_sim_time}],
        remappings=[("odometry/filtered", "odometry/filtered")],
    )
    lidar_pub = Node(
        package="go2_control",
        executable="go2_lidar",
        name="go2_lidar",
        output="screen",
    )
    zed_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("zed_wrapper"), "launch", "zed_camera.launch.py")
        ),
        launch_arguments={
            "camera_name": "zed",
            "camera_model": "zedxm",
            "publish_tf": "false",
            "publish_map_tf": "false",
            "publish_imu_tf": "false",
            "ros_params_override_path": zed_follow_params_path,
        }.items(),
    )
    lidar_node = Node(
        name="sllidar_node",
        package="sllidar_ros2",
        executable="sllidar_node",
        output="screen",
        parameters=[
            {
                "channel_type": "serial",
                "serial_port": "/dev/ttyUSB0",
                "serial_baudrate": 256000,
                "frame_id": "laser",
                "inverted": False,
                "angle_compensate": True,
                "scan_mode": "Sensitivity",
            }
        ],
        remappings=[("/laserscan", "/scan")],
    )
    startup_motion_switcher = ExecuteProcess(
        cmd=[
            motion_mode_switcher_executable,
            "--network-interface",
            person_follow_unitree_network_interface,
            "--motion-mode",
            startup_motion_mode,
            "--gait",
            startup_motion_gait,
            "--wait",
            startup_motion_wait_s,
            "--retries",
            startup_motion_retries,
            "--retry-interval",
            startup_motion_retry_interval_s,
        ],
        output="screen",
    )

    return LaunchDescription(
        declare_launch_arguments(ARGUMENT_NAMES, launch_dir) +
        [
            robot_state_pub,
            base_tf,
            go2_driver,
            startup_motion_switcher,
            state_pub,
            odom_node,
            ekf_node,
            zed_launch,
            lidar_node,
            lidar_pub,
        ]
    )
