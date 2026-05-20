#!/usr/bin/env python3
"""
Go2 mission bringup for mapping, exploration, and leak localization.
"""

from __future__ import annotations

import os
import sys

from launch import LaunchDescription
from launch.actions import GroupAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

sys.path.insert(0, os.path.dirname(__file__))

from _mapping_common import (
    ALL_ARGUMENT_NAMES,
    declare_launch_arguments,
    go2_description_paths,
    launch_argument_mapping,
    profile_condition,
    with_cyclonedds_warning_filter,
)


def _include_launch(launch_dir: str, filename: str, argument_names: list[str]) -> IncludeLaunchDescription:
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(launch_dir, filename)),
        launch_arguments=launch_argument_mapping(argument_names).items(),
    )


def generate_launch_description():
    launch_dir = os.path.dirname(__file__)
    launch_profile = LaunchConfiguration("launch_profile")
    paths = go2_description_paths()

    mission_base_group = GroupAction(
        condition=profile_condition(launch_profile, ["all", "mission_base"]),
        actions=[
            _include_launch(
                launch_dir,
                "mapping_base.launch.py",
                [
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
                ],
            ),
            _include_launch(
                launch_dir,
                "mapping_nav.launch.py",
                ["use_sim_time", "debug_odometry"],
            ),
            _include_launch(
                launch_dir,
                "mapping_audio.launch.py",
                [
                    "odas_enable",
                    "odas_configuration_path",
                    "odas_audio_queue_size",
                    "odas_visualization",
                    "odas_force_publish_tf",
                    "odas_use_echo_cancellation",
                    "odas_echo_cancelled_signal_topic",
                    "odas_enable_leak_classifier",
                    "odas_leak_classifier_debug",
                    "odas_doa_zero_offset_deg",
                    "odas_log_level",
                    "voice_control",
                    "voice_transcript_topic",
                    "voice_wake_phrase",
                    "voice_shake_hand_phrase",
                    "voice_search_phrase",
                    "voice_follow_phrase",
                    "voice_stop_follow_phrase",
                    "voice_stand_up_phrase",
                    "voice_lay_down_phrase",
                    "voice_stt_enable",
                    "voice_stt_model_path",
                    "voice_stt_audio_topic",
                    "voice_stt_channel",
                    "voice_stt_channel_strategy",
                    "voice_stt_publish_partial",
                    "voice_stt_debug_audio",
                    "voice_stt_max_alternatives",
                    "voice_debug",
                    "voice_command_debug",
                    "voice_command_cooldown_s",
                    "voice_command_mode",
                    "voice_command_topic",
                ],
            ),
            _include_launch(
                launch_dir,
                "mapping_behavior.launch.py",
                [
                    "use_sim_time",
                    "odas_enable",
                    "odas_enable_leak_classifier",
                    "sound_localizer_enable",
                    "search_debug",
                    "search_allow_unknown",
                    "voice_command_cooldown_s",
                    "voice_command_topic",
                    "person_follow_enable",
                    "person_follow_distance_m",
                    "person_follow_distance_band_m",
                    "person_follow_max_vx_mps",
                    "person_follow_max_vy_mps",
                    "person_follow_max_wz_radps",
                    "person_follow_use_strafe",
                    "person_follow_candidate_horizon_s",
                    "person_follow_reacquire_timeout_s",
                    "person_follow_sit_on_loss_timeout_s",
                    "person_follow_debug",
                    "person_follow_motion_backend",
                    "person_follow_unitree_cmd_vel_topic",
                    "person_follow_unitree_network_interface",
                    "person_follow_unitree_command_timeout_s",
                    "person_follow_detections_topic",
                    "person_follow_color_topic",
                    "person_follow_depth_topic",
                    "person_follow_camera_info_topic",
                    "person_follow_target_label",
                    "startup_motion_mode",
                    "startup_motion_gait",
                    "startup_motion_wait_s",
                    "startup_motion_retries",
                    "startup_motion_retry_interval_s",
                ],
            ),
        ],
    )

    log_pose_server = Node(
        package="go2_control",
        executable="log_pose_action_server",
        name="log_pose_action_server",
        output="screen",
        parameters=[{"save_path": "pose_log.json"}],
        arguments=with_cyclonedds_warning_filter(),
    )
    rviz2 = Node(
        package="rviz2",
        executable="rviz2",
        arguments=with_cyclonedds_warning_filter(["-d", paths["rviz_cfg"]]),
    )
    operator_tools_group = GroupAction(
        condition=profile_condition(launch_profile, ["all", "operator_tools"]),
        actions=[log_pose_server, rviz2],
    )

    return LaunchDescription(
        declare_launch_arguments(ALL_ARGUMENT_NAMES, launch_dir) +
        [
            mission_base_group,
            operator_tools_group,
        ]
    )
