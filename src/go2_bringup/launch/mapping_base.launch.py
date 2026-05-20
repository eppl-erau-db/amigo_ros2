#!/usr/bin/env python3
from __future__ import annotations

import os
import sys

from ament_index_python.packages import get_package_prefix
from launch import LaunchDescription
from launch.actions import ExecuteProcess, LogInfo, OpaqueFunction
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from launch_ros.actions import ComposableNodeContainer, Node
from launch_ros.descriptions import ComposableNode
from launch_ros.parameter_descriptions import ParameterValue

sys.path.insert(0, os.path.dirname(__file__))

from _mapping_common import (
    conditional_log_level_arg,
    declare_launch_arguments,
    go2_description_paths,
    with_cyclonedds_warning_filter,
)


ARGUMENT_NAMES = [
    "use_sim_time",
    "debug_odometry",
    "realsense_enable",
    "realsense_camera_name",
    "realsense_serial_no",
    "realsense_device_type",
    "realsense_enable_color",
    "realsense_enable_depth",
    "realsense_enable_infra",
    "realsense_enable_imu",
    "realsense_enable_sync",
    "realsense_align_depth",
    "realsense_pointcloud_enable",
    "realsense_publish_tf",
    "realsense_initial_reset",
    "realsense_color_profile",
    "realsense_depth_profile",
    "realsense_infra_profile",
    "realsense_emitter_enabled",
    "realsense_wait_for_device_timeout",
    "realsense_reconnect_timeout",
    "camera_model",
    "camera_xyz",
    "camera_rpy",
    "vslam_enable",
    "vslam_odom_topic",
    "person_follow_unitree_network_interface",
    "startup_motion_mode",
    "startup_motion_gait",
    "startup_motion_wait_s",
    "startup_motion_retries",
    "startup_motion_retry_interval_s",
]


def _value(context, name: str) -> str:
    return context.perform_substitution(LaunchConfiguration(name)).strip()


def _as_bool(context, name: str) -> bool:
    return _value(context, name).lower() in ("1", "true", "yes", "on")


def _as_int(context, name: str) -> int:
    return int(float(_value(context, name)))


def _as_float(context, name: str) -> float:
    return float(_value(context, name))


def _realsense_component(context) -> ComposableNode:
    camera_name = _value(context, "realsense_camera_name")
    enable_imu = _as_bool(context, "realsense_enable_imu")
    params = {
        "camera_name": camera_name,
        "serial_no": _value(context, "realsense_serial_no"),
        "device_type": _value(context, "realsense_device_type"),
        "enable_color": _as_bool(context, "realsense_enable_color"),
        "enable_depth": _as_bool(context, "realsense_enable_depth"),
        "enable_infra": False,
        "enable_infra1": _as_bool(context, "realsense_enable_infra"),
        "enable_infra2": _as_bool(context, "realsense_enable_infra"),
        "enable_gyro": enable_imu,
        "enable_accel": enable_imu,
        "unite_imu_method": 2 if enable_imu else 0,
        "enable_sync": _as_bool(context, "realsense_enable_sync"),
        "initial_reset": _as_bool(context, "realsense_initial_reset"),
        "publish_tf": _as_bool(context, "realsense_publish_tf"),
        "tf_publish_rate": 0.0,
        "align_depth.enable": _as_bool(context, "realsense_align_depth"),
        "pointcloud.enable": _as_bool(context, "realsense_pointcloud_enable"),
        "depth_module.emitter_enabled": _as_int(context, "realsense_emitter_enabled"),
        "depth_module.enable_auto_exposure": True,
        "rgb_camera.enable_auto_exposure": True,
        "depth_module.depth_profile": _value(context, "realsense_depth_profile"),
        "depth_module.infra_profile": _value(context, "realsense_infra_profile"),
        "rgb_camera.color_profile": _value(context, "realsense_color_profile"),
        "wait_for_device_timeout": _as_float(context, "realsense_wait_for_device_timeout"),
        "reconnect_timeout": _as_float(context, "realsense_reconnect_timeout"),
    }
    return ComposableNode(
        name=camera_name,
        namespace="",
        package="realsense2_camera",
        plugin="realsense2_camera::RealSenseNodeFactory",
        parameters=[params],
        extra_arguments=[{"use_intra_process_comms": True}],
    )


def _vslam_component(context) -> ComposableNode:
    camera_name = _value(context, "realsense_camera_name")
    odom_topic = _value(context, "vslam_odom_topic")
    return ComposableNode(
        name="visual_slam_node",
        package="isaac_ros_visual_slam",
        plugin="nvidia::isaac_ros::visual_slam::VisualSlamNode",
        parameters=[
            {
                "tracking_mode": 0,
                "enable_image_denoising": False,
                "rectified_images": True,
                "image_jitter_threshold_ms": 34.0,
                "map_frame": "map",
                "odom_frame": "odom",
                "base_frame": "base_footprint",
                "publish_map_to_odom_tf": False,
                "publish_odom_to_base_tf": False,
                "enable_slam_visualization": True,
                "enable_landmarks_view": True,
                "enable_observations_view": True,
                "enable_ground_constraint_in_odometry": False,
                "enable_ground_constraint_in_slam": False,
                "enable_localization_n_mapping": True,
                "enable_debug_mode": _as_bool(context, "debug_odometry"),
                "num_cameras": 2,
                "min_num_images": 2,
                "camera_optical_frames": [
                    f"{camera_name}_infra1_optical_frame",
                    f"{camera_name}_infra2_optical_frame",
                ],
            }
        ],
        remappings=[
            ("visual_slam/image_0", f"/{camera_name}/infra1/image_rect_raw"),
            ("visual_slam/camera_info_0", f"/{camera_name}/infra1/camera_info"),
            ("visual_slam/image_1", f"/{camera_name}/infra2/image_rect_raw"),
            ("visual_slam/camera_info_1", f"/{camera_name}/infra2/camera_info"),
            ("visual_slam/tracking/odometry", odom_topic),
        ],
    )


def _camera_stack_setup(context, *args, **kwargs):
    del args, kwargs
    components: list[ComposableNode] = []
    if _as_bool(context, "realsense_enable"):
        components.append(_realsense_component(context))
    if _as_bool(context, "vslam_enable"):
        components.append(_vslam_component(context))
    if not components:
        return [LogInfo(msg="RealSense camera stack disabled by launch arguments.")]
    actions = []
    if _as_bool(context, "debug_odometry"):
        actions.append(
            LogInfo(
                msg=(
                    "[mapping_base] debug_odometry enabled for camera stack; "
                    "visual_slam_node will publish /vslam/odom but EKF fusion is disabled by default"
                )
            )
        )
    actions.append(
        ComposableNodeContainer(
            name="go2_mapping_camera_container",
            namespace="",
            package="rclcpp_components",
            executable="component_container_mt",
            composable_node_descriptions=components,
            output="screen",
            arguments=with_cyclonedds_warning_filter(
                log_levels=[conditional_log_level_arg("visual_slam_node")]
            ),
        )
    )
    return actions


def generate_launch_description():
    launch_dir = os.path.dirname(__file__)
    use_sim_time = LaunchConfiguration("use_sim_time")
    debug_odometry = LaunchConfiguration("debug_odometry")
    debug_odometry_bool = ParameterValue(debug_odometry, value_type=bool)
    person_follow_unitree_network_interface = LaunchConfiguration(
        "person_follow_unitree_network_interface"
    )
    startup_motion_mode = LaunchConfiguration("startup_motion_mode")
    startup_motion_gait = LaunchConfiguration("startup_motion_gait")
    startup_motion_wait_s = LaunchConfiguration("startup_motion_wait_s")
    startup_motion_retries = LaunchConfiguration("startup_motion_retries")
    startup_motion_retry_interval_s = LaunchConfiguration("startup_motion_retry_interval_s")

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
                " camera_name:=",
                LaunchConfiguration("realsense_camera_name"),
                " camera_model:=",
                LaunchConfiguration("camera_model"),
                " camera_xyz:='",
                LaunchConfiguration("camera_xyz"),
                "' camera_rpy:='",
                LaunchConfiguration("camera_rpy"),
                "'",
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
        arguments=with_cyclonedds_warning_filter(),
    )
    state_pub = Node(
        package="go2_control",
        executable="go2_state",
        name="go2_state",
        output="screen",
        arguments=with_cyclonedds_warning_filter(),
    )
    odom_node = Node(
        package="go2_control",
        executable="odom_node",
        name="odom_node",
        output="screen",
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "debug_odometry": debug_odometry_bool,
                "planarize": True,
                "source_odom_topic": "/utlidar/robot_odom",
                "odom_topic": "/utlidar_odom",
                "parent_frame": "odom",
                "child_frame": "base_footprint",
            }
        ],
        arguments=with_cyclonedds_warning_filter(
            log_levels=[conditional_log_level_arg("odom_node")]
        ),
    )
    go2_driver = Node(
        package="go2_driver",
        executable="go2_driver_node",
        name="go2_driver_node",
        output="screen",
        arguments=with_cyclonedds_warning_filter(),
    )
    ekf_node = Node(
        package="robot_localization",
        executable="ekf_node",
        name="ekf_filter_node",
        output="screen",
        parameters=[
            paths["ekf_cfg"],
            {
                "use_sim_time": use_sim_time,
                "print_diagnostics": debug_odometry_bool,
                "debug": debug_odometry_bool,
                "debug_out_file": "/tmp/go2_local_odom_ekf_debug.txt",
            },
        ],
        remappings=[("odometry/filtered", "/odom")],
        arguments=with_cyclonedds_warning_filter(
            log_levels=[conditional_log_level_arg("ekf_filter_node")]
        ),
    )
    lidar_pub = Node(
        package="go2_control",
        executable="go2_lidar",
        name="go2_lidar",
        output="screen",
        arguments=with_cyclonedds_warning_filter(),
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
        arguments=with_cyclonedds_warning_filter(),
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
        condition=IfCondition(
            PythonExpression(
                [
                    "'",
                    startup_motion_mode,
                    "'.lower() not in ['', 'none', 'off', 'skip']",
                ]
            )
        ),
    )

    return LaunchDescription(
        declare_launch_arguments(ARGUMENT_NAMES, launch_dir) +
        [
            LogInfo(
                condition=IfCondition(debug_odometry),
                msg=(
                    "[mapping_base] debug_odometry enabled: robot_state_publisher owns "
                    "base_footprint->base_link, odom_node planarizes /utlidar/robot_odom, "
                    "and EKF publishes /odom plus odom->base_footprint"
                ),
            ),
            robot_state_pub,
            go2_driver,
            startup_motion_switcher,
            state_pub,
            odom_node,
            ekf_node,
            OpaqueFunction(function=_camera_stack_setup),
            lidar_node,
            lidar_pub,
        ]
    )
