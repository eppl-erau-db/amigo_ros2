#!/usr/bin/env python3
from __future__ import annotations

import os
import sys

from launch import LaunchDescription
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

sys.path.insert(0, os.path.dirname(__file__))

from _mapping_common import (
    FOLLOW_ARGUMENT_NAMES,
    MISSION_ARGUMENT_NAMES,
    AUDIO_ARGUMENT_NAMES,
    VOICE_ARGUMENT_NAMES,
    declare_launch_arguments,
    derive_nav2_settings,
    go2_description_paths,
    with_cyclonedds_warning_filter,
)


ARGUMENT_NAMES = ["use_sim_time"] + FOLLOW_ARGUMENT_NAMES + MISSION_ARGUMENT_NAMES + AUDIO_ARGUMENT_NAMES + VOICE_ARGUMENT_NAMES


def generate_launch_description():
    launch_dir = os.path.dirname(__file__)
    use_sim_time = LaunchConfiguration("use_sim_time")
    odas_enable = LaunchConfiguration("odas_enable")
    odas_enable_leak_classifier = LaunchConfiguration("odas_enable_leak_classifier")
    sound_localizer_enable = LaunchConfiguration("sound_localizer_enable")
    search_debug = LaunchConfiguration("search_debug")
    voice_command_cooldown_s = LaunchConfiguration("voice_command_cooldown_s")
    voice_command_topic = LaunchConfiguration("voice_command_topic")
    person_follow_enable = LaunchConfiguration("person_follow_enable")
    person_follow_distance_m = LaunchConfiguration("person_follow_distance_m")
    person_follow_distance_band_m = LaunchConfiguration("person_follow_distance_band_m")
    person_follow_max_vx_mps = LaunchConfiguration("person_follow_max_vx_mps")
    person_follow_max_vy_mps = LaunchConfiguration("person_follow_max_vy_mps")
    person_follow_max_wz_radps = LaunchConfiguration("person_follow_max_wz_radps")
    person_follow_use_strafe = LaunchConfiguration("person_follow_use_strafe")
    person_follow_candidate_horizon_s = LaunchConfiguration("person_follow_candidate_horizon_s")
    person_follow_reacquire_timeout_s = LaunchConfiguration("person_follow_reacquire_timeout_s")
    person_follow_sit_on_loss_timeout_s = LaunchConfiguration("person_follow_sit_on_loss_timeout_s")
    person_follow_debug = LaunchConfiguration("person_follow_debug")
    person_follow_motion_backend = LaunchConfiguration("person_follow_motion_backend")
    person_follow_unitree_cmd_vel_topic = LaunchConfiguration("person_follow_unitree_cmd_vel_topic")
    person_follow_unitree_network_interface = LaunchConfiguration(
        "person_follow_unitree_network_interface"
    )
    person_follow_unitree_command_timeout_s = LaunchConfiguration(
        "person_follow_unitree_command_timeout_s"
    )
    person_follow_unitree_gait = LaunchConfiguration("person_follow_unitree_gait")
    person_follow_detections_topic = LaunchConfiguration("person_follow_detections_topic")
    person_follow_color_topic = LaunchConfiguration("person_follow_color_topic")
    person_follow_depth_topic = LaunchConfiguration("person_follow_depth_topic")
    person_follow_camera_info_topic = LaunchConfiguration("person_follow_camera_info_topic")
    person_follow_target_class_id = LaunchConfiguration("person_follow_target_class_id")
    person_follow_target_label = LaunchConfiguration("person_follow_target_label")
    startup_motion_mode = LaunchConfiguration("startup_motion_mode")
    startup_motion_gait = LaunchConfiguration("startup_motion_gait")
    startup_motion_wait_s = LaunchConfiguration("startup_motion_wait_s")
    startup_motion_retries = LaunchConfiguration("startup_motion_retries")
    startup_motion_retry_interval_s = LaunchConfiguration("startup_motion_retry_interval_s")

    paths = go2_description_paths()
    nav2_settings = derive_nav2_settings(paths["nav2_cfg"])
    person_follow_motion_bridge_env = {"RMW_IMPLEMENTATION": "rmw_fastrtps_cpp"}

    voice_stand_up_recovery_motion_mode_value = ParameterValue(
        startup_motion_mode,
        value_type=str,
    )
    person_follow_target_class_id_value = ParameterValue(
        person_follow_target_class_id,
        value_type=str,
    )
    person_follow_use_local_costmap_safety_value = ParameterValue(
        PythonExpression([
            "'",
            person_follow_motion_backend,
            "'.strip().lower() in ['legacy', 'sport', 'unitree_sport']",
        ]),
        value_type=bool,
    )
    person_follow_unitree_backend_condition = IfCondition(
        PythonExpression(
            [
                "'",
                person_follow_enable,
                "' == 'true' and '",
                person_follow_motion_backend,
                "' != 'legacy'",
            ]
        )
    )
    leak_stack_condition = IfCondition(
        PythonExpression(
            [
                "'",
                sound_localizer_enable,
                "' == 'true' and '",
                odas_enable,
                "' == 'true' and '",
                odas_enable_leak_classifier,
                "' == 'true'",
            ]
        )
    )

    explore_phase_server = Node(
        package="go2_control",
        executable="explore_until_detected_action_server",
        name="explore_until_detected_server",
        output="screen",
        parameters=[{"use_sim_time": use_sim_time}],
        arguments=with_cyclonedds_warning_filter(),
        condition=leak_stack_condition,
    )
    localize_phase_server = Node(
        package="go2_control",
        executable="localize_detected_leak_action_server",
        output="screen",
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "debug_search": search_debug,
                "allow_unknown": nav2_settings["allow_unknown"],
                "clearance_radius_m": nav2_settings["clearance_radius_m"],
                "local_inflation_radius_m": nav2_settings["local_inflation_radius_m"],
                "global_inflation_radius_m": nav2_settings["global_inflation_radius_m"],
            }
        ],
        arguments=with_cyclonedds_warning_filter(),
        condition=leak_stack_condition,
    )
    search_action_server = Node(
        package="go2_control",
        executable="search_action_server",
        name="leak_search_server",
        output="screen",
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "debug_topic": "/voice/debug",
                "publish_debug_events": True,
                "explore_action_name": "explore_until_detected",
                "localize_action_name": "localize_detected_leak",
            }
        ],
        arguments=with_cyclonedds_warning_filter(),
        condition=leak_stack_condition,
    )
    sound_localizer_node = Node(
        package="go2_control",
        executable="sound_localizer",
        name="sound_localizer",
        output="screen",
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "min_baseline_m": 0.10,
                "stable_min_baseline_m": 0.50,
                "stable_min_bearing_separation_deg": 10.0,
                "stable_required_consecutive_estimates": 3,
                "stable_centroid_radius_m": 0.20,
                "stable_max_doa_age_s": 1.0,
                "intersection_method": "geometric",
                "use_absolute_x_positions": False,
                "publish_waypoints": False,
                "num_waypoints": 0,
                "enable_reasonableness_filter": False,
            }
        ],
        arguments=with_cyclonedds_warning_filter(),
        condition=leak_stack_condition,
    )
    mission_supervisor_node = Node(
        package="go2_control",
        executable="mission_supervisor_node",
        name="mission_supervisor_node",
        output="screen",
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "voice_command_topic": voice_command_topic,
                "debug_topic": "/voice/debug",
                "base_cmd_vel_topic": "cmd_vel",
                "nav_candidate_topic": "/motion/candidate/nav",
                "follow_candidate_topic": "/motion/candidate/follow",
                "follow_command_topic": person_follow_unitree_cmd_vel_topic,
                "follow_event_topic": "/person_follow_controller_node/event",
                "follow_motion_backend": person_follow_motion_backend,
                "search_action_name": "search",
                "sport_request_topic": "/api/sport/request",
                "command_cooldown_s": voice_command_cooldown_s,
                "stand_up_recovery_enabled": True,
                "stand_up_recovery_delay_s": 1.0,
                "stand_up_recovery_motion_mode": voice_stand_up_recovery_motion_mode_value,
                "stand_up_recovery_gait": startup_motion_gait,
                "stand_up_recovery_wait_s": 0.0,
                "stand_up_recovery_retries": 4,
                "stand_up_recovery_retry_interval_s": 0.75,
                "stand_up_recovery_network_interface": person_follow_unitree_network_interface,
                "lay_down_settle_s": 2.5,
                "stand_up_settle_s": 2.5,
            }
        ],
        arguments=with_cyclonedds_warning_filter(),
    )
    person_follow_node = Node(
        package="go2_person_follow",
        executable="person_follow_vision_node",
        name="person_follow_vision_node",
        output="screen",
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "robot_mode_state_topic": "/robot_mode_state",
                "detections_topic": person_follow_detections_topic,
                "color_image_topic": person_follow_color_topic,
                "depth_image_topic": person_follow_depth_topic,
                "camera_info_topic": person_follow_camera_info_topic,
                "target_class_id": person_follow_target_class_id_value,
                "target_label": person_follow_target_label,
            }
        ],
        arguments=with_cyclonedds_warning_filter(),
        condition=IfCondition(person_follow_enable),
    )
    person_follow_controller_node = Node(
        package="go2_control",
        executable="person_follow_controller_node",
        name="person_follow_controller_node",
        output="screen",
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "robot_mode_state_topic": "/robot_mode_state",
                "target_point_topic": "/person_follow_vision_node/target_point",
                "target_visible_topic": "/person_follow_vision_node/target_visible",
                "target_status_topic": "/person_follow_vision_node/status",
                "local_costmap_topic": "/local_costmap/costmap",
                "cmd_vel_topic": "/motion/candidate/follow",
                "desired_distance_m": person_follow_distance_m,
                "distance_band_m": person_follow_distance_band_m,
                "max_forward_speed_mps": person_follow_max_vx_mps,
                "max_lateral_speed_mps": person_follow_max_vy_mps,
                "max_yaw_rate_radps": person_follow_max_wz_radps,
                "use_strafe": person_follow_use_strafe,
                "candidate_horizon_s": person_follow_candidate_horizon_s,
                "reacquire_timeout_s": person_follow_reacquire_timeout_s,
                "sit_on_loss_timeout_s": person_follow_sit_on_loss_timeout_s,
                "debug_enable": person_follow_debug,
                "use_local_costmap_safety": person_follow_use_local_costmap_safety_value,
            }
        ],
        arguments=with_cyclonedds_warning_filter(),
        condition=IfCondition(person_follow_enable),
    )
    person_follow_motion_bridge_node = Node(
        package="go2_driver",
        executable="person_follow_motion_bridge_node",
        name="person_follow_motion_bridge_node",
        output="screen",
        parameters=[
            {
                "backend": person_follow_motion_backend,
                "cmd_vel_topic": person_follow_unitree_cmd_vel_topic,
                "robot_mode_state_topic": "/robot_mode_state",
                "network_interface": person_follow_unitree_network_interface,
                "command_timeout_s": person_follow_unitree_command_timeout_s,
                "follow_gait": person_follow_unitree_gait,
            }
        ],
        arguments=with_cyclonedds_warning_filter(),
        additional_env=person_follow_motion_bridge_env,
        condition=person_follow_unitree_backend_condition,
    )

    return LaunchDescription(
        declare_launch_arguments(ARGUMENT_NAMES, launch_dir) +
        [
            explore_phase_server,
            localize_phase_server,
            search_action_server,
            sound_localizer_node,
            mission_supervisor_node,
            person_follow_node,
            person_follow_controller_node,
            person_follow_motion_bridge_node,
        ]
    )
