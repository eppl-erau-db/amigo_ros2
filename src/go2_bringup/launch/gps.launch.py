#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Launch Go2 base nodes + GPS-enabled Nav2 + Mapviz/RViz."""

import os

from ament_index_python.packages import get_package_share_directory, get_package_share_path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from nav2_common.launch import RewrittenYaml


def generate_launch_description():
    #
    # ──────────────── Launch-time arguments ────────────────
    #
    use_sim_time   = LaunchConfiguration("use_sim_time",   default="false")

    # Keep original toggles (RViz for local debugging, visual markers, initial pose)
    rviz_local     = LaunchConfiguration("rviz",           default="false")
    visualization  = LaunchConfiguration("visualization",  default="true")
    initial_pose   = LaunchConfiguration("initial_pose",   default="false")

    # GPS demo toggles
    use_rviz       = LaunchConfiguration("use_rviz",   default="false")   # demo RViz
    use_mapviz     = LaunchConfiguration("use_mapviz", default="false")

    declare_rviz_local_cmd  = DeclareLaunchArgument("rviz",  default_value="false",
                                                    description="Start old RViz config?")
    declare_vis_cmd         = DeclareLaunchArgument("visualization", default_value="true",
                                                    description="Enable markers in rviz_local config")
    declare_initial_pose_cmd = DeclareLaunchArgument("initial_pose", default_value="false",
                                                     description="Send an /initialpose message at start")

    declare_use_rviz_cmd   = DeclareLaunchArgument("use_rviz",   default_value="false",
                                                   description="Start GPS-demo RViz config")
    declare_use_mapviz_cmd = DeclareLaunchArgument("use_mapviz", default_value="false",
                                                   description="Start Mapviz")

    #
    # ──────────────── Paths & common files ────────────────
    #
    go2_desc_share   = get_package_share_path("go2_description")
    urdf_path        = os.path.join(go2_desc_share, "urdf", "go2.urdf.xacro")
    rviz_local_cfg   = os.path.join(go2_desc_share, "config", "nav_nvblox_config.rviz")

    # Nav2 GPS demo package provides params/launch files we’ll re-use
    gps_launch_dir   = os.path.join(get_package_share_path("robot_localization"), "launch")

    nav2_params_yaml = os.path.join(go2_desc_share, "config", "nav2_no_map.yaml")

    # Re-write that YAML on the fly if the user passes extra overrides
    nav2_configured_params = RewrittenYaml(
        source_file=nav2_params_yaml,
        root_key="",
        param_rewrites={},
        convert_types=True,
    )

    #
    # ──────────────── Core robot description / tf ────────────────
    #
    robot_description = ParameterValue(Command(["xacro", " ", urdf_path]), value_type=str)

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}],
        output="log",
    )

    base_footprint_to_base_link_tf = Node(
        package="go2_control",
        executable="base_to_base_tf",
        name="base_to_base_tf",
        output="log",
    )

    #
    # ──────────────── Go2 drivers & odometry ────────────────
    #
    go2_driver_node = Node(
        package="go2_driver",
        executable="go2_driver_node",
        name="go2_driver_node",
        output="log",
    )

    go2_state_publisher = Node(
        package="go2_control",
        executable="go2_state",
        name="go2_state",
        output="log",
    )

    odom_node = Node(
        package="go2_control",
        executable="odom_node",
        name="odom_node",
        output="screen",
    )

    start_go2_lidar = Node(
        package="go2_control",
        executable="go2_lidar",
        name="go2_lidar",
        output="log",
    )

    start_teleop_node = Node(
        package="go2_control",
        executable="go2_velocity_commands",
        name="go2_velocity_commands",
        output="log",
    )

    #
    # ──────────────── Optional helpers ────────────────
    #
    rviz_local_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", rviz_local_cfg],
        condition=IfCondition(rviz_local),
        output="log",
    )

    set_initial_pose = Node(
        package="go2_control",
        executable="initial_pose_set",
        name="initial_pose_set",
        output="log",
        condition=IfCondition(initial_pose),
    )

    #
    # ──────────────── Robot_localization (dual EKF + NavSat) ────────────────
    # Commented out 11/14 to test Dual EKF + Navsat separately
    dual_ekf_navsat_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gps_launch_dir, "dual_ekf_navsat_example.launch.py")
        ),
        launch_arguments={"use_sim_time": use_sim_time}.items(),
    )

    #
    # ──────────────── Nav2 stack (GPS/no-map mode) ────────────────
    #
    nav2_bringup_share = get_package_share_directory("nav2_bringup")
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_share, "launch", "navigation_launch.py")
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
            "params_file": nav2_configured_params,
            "autostart": "true",
        }.items(),
    )

    #
    # ──────────────── Visualization: RViz (demo) + Mapviz ────────────────
    #
    rviz_demo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_share, "launch", "rviz_launch.py")
        ),
        condition=IfCondition(use_rviz),
    )

    mapviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_path("mapviz"), "launch", "mapviz.launch.py")
        ),
        condition=IfCondition(use_mapviz),
    )

    #
    # ──────────────── Assemble & return LaunchDescription ────────────────
    #
    ld = LaunchDescription()

    # Declare all CLI arguments first (so `ros2 launch --show-arguments` works)
    ld.add_action(declare_rviz_local_cmd)
    ld.add_action(declare_vis_cmd)
    ld.add_action(declare_initial_pose_cmd)
    ld.add_action(declare_use_rviz_cmd)
    ld.add_action(declare_use_mapviz_cmd)

    # Core robot stack
    ld.add_action(robot_state_publisher)
    ld.add_action(base_footprint_to_base_link_tf)              
    ld.add_action(go2_driver_node)
    ld.add_action(go2_state_publisher)
    ld.add_action(odom_node)
    ld.add_action(start_go2_lidar)
    ld.add_action(start_teleop_node)
    # ld.add_action(start_teleop_node)
    # Optional helpers
    ld.add_action(rviz_local_node)
    # ld.add_action(set_initial_pose)

    # Localization + Nav2 + Visualization
    ld.add_action(dual_ekf_navsat_launch)
    # ld.add_action(nav2_launch)
    ld.add_action(rviz_demo_launch)
    # ld.add_action(mapviz_launch)

    return ld

