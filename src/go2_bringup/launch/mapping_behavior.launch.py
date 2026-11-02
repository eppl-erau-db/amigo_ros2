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
    SWAG_ARGUMENT_NAMES,
    declare_launch_arguments,
    derive_nav2_settings,
    go2_description_paths,
)


ARGUMENT_NAMES = (
    ["use_sim_time"]
    + FOLLOW_ARGUMENT_NAMES
    + MISSION_ARGUMENT_NAMES
    + AUDIO_ARGUMENT_NAMES
    + VOICE_ARGUMENT_NAMES
    + SWAG_ARGUMENT_NAMES
)


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
    startup_motion_mode = LaunchConfiguration("startup_motion_mode")
    startup_motion_gait = LaunchConfiguration("startup_motion_gait")
    startup_motion_wait_s = LaunchConfiguration("startup_motion_wait_s")
    startup_motion_retries = LaunchConfiguration("startup_motion_retries")
    startup_motion_retry_interval_s = LaunchConfiguration("startup_motion_retry_interval_s")
    zed_follow_params_path = LaunchConfiguration("zed_follow_params_path")
    swag_enable = LaunchConfiguration("swag_enable")
    swag_debug = LaunchConfiguration("swag_debug")
    aruco_marker_size_m = LaunchConfiguration("aruco_marker_size_m")
    aruco_dictionary = LaunchConfiguration("aruco_dictionary")
    aruco_image_topic = LaunchConfiguration("aruco_image_topic")
    aruco_camera_info_topic = LaunchConfiguration("aruco_camera_info_topic")
    aruco_detect_rate_hz = LaunchConfiguration("aruco_detect_rate_hz")
    swag_maps_dir = LaunchConfiguration("swag_maps_dir")
    swag_map_name = LaunchConfiguration("swag_map_name")
    arm_enable = LaunchConfiguration("arm_enable")
    arm_dry_run = LaunchConfiguration("arm_dry_run")
    arm_scripts_dir = LaunchConfiguration("arm_scripts_dir")
    deliver_use_arm = LaunchConfiguration("deliver_use_arm")
    deliver_arm_stub_wait_s = LaunchConfiguration("deliver_arm_stub_wait_s")
    deliver_pickup_marker_id = LaunchConfiguration("deliver_pickup_marker_id")
    deliver_delivery_marker_id = LaunchConfiguration("deliver_delivery_marker_id")
    deliver_approach_standoff_m = LaunchConfiguration("deliver_approach_standoff_m")
    deliver_align_standoff_m = LaunchConfiguration("deliver_align_standoff_m")

    paths = go2_description_paths()
    nav2_settings = derive_nav2_settings(paths["nav2_cfg"])
    person_follow_motion_bridge_env = {"RMW_IMPLEMENTATION": "rmw_fastrtps_cpp"}

    voice_stand_up_recovery_motion_mode_value = ParameterValue(
        startup_motion_mode,
        value_type=str,
    )
    person_follow_use_local_costmap_safety_value = ParameterValue(
        PythonExpression(["'", person_follow_motion_backend, "' == 'legacy'"]),
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
        condition=leak_stack_condition,
    )
    localize_phase_server = Node(
        package="go2_control",
        executable="localize_detected_leak_action_server",
        name="localize_detected_leak_server",
        output="screen",
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "debug_search": search_debug,
                "allow_unknown": nav2_settings["allow_unknown"],
                "clearance_radius_m": nav2_settings["clearance_radius_m"],
                "local_inflation_radius_m": nav2_settings["local_inflation_radius_m"],
                "global_inflation_radius_m": nav2_settings["global_inflation_radius_m"],
                # Final-approach standoff from the locked leak estimate. The robot
                # footprint reaches 0.36 m AHEAD of base_link (footprint half-length,
                # nav2_mppi_controller.yaml), so a goal closer than ~0.46 m
                # (0.36 + collision_margin 0.10) puts the footprint ON the leak
                # source. MPPI's ObstaclesCritic (consider_footprint:true) then sees
                # every goal-reaching trajectory as in-collision against the L1-fed
                # LOCAL costmap and commands ~0 -> "Failed to make progress" forever
                # (the action server only clearance-checks the GLOBAL /map, which is
                # why it looks like free space). The radii clamp to
                # approach_goal_tolerance_m, and _select_approach_goal prefers the
                # LARGEST reachable radius (shortest path), so this stops the dog a
                # footprint-safe ~0.6 m from the source.
                "approach_goal_tolerance_m": 0.60,
                "approach_radius_candidates_m": [0.45, 0.50, 0.55, 0.60],
                # Sampling-based perpendicular baseline selection (doc eqs. 9-13).
                "local_costmap_topic": "/local_costmap/costmap",
                "local_costmap_occupied_threshold": 50,
                "perp_baseline_target_m": 0.5,
                "weak_geometry_min_m": 0.25,
                "sample_num": 80,
                "max_path_checks_per_leg": 20,
                "sample_radius_m": 1.5,
                "sample_min_radius_m": 0.4,
                "costmap_clear_enabled": True,
                "costmap_repopulate_wait_s": 1.0,
                # Leak-found Sit hold + recovery (RiseSit -> BalanceStand -> gait).
                "found_pose_hold_duration_s": 3.0,
                "rise_sit_settle_s": 1.5,
                "balance_settle_s": 1.0,
                "gait_restore_enabled": True,
                "gait_restore_network_interface": person_follow_unitree_network_interface,
                "gait_restore_motion_mode": voice_stand_up_recovery_motion_mode_value,
                "gait_restore_gait": startup_motion_gait,
                "gait_restore_retries": 4,
                "gait_restore_retry_interval_s": 0.75,
            }
        ],
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
                "deliver_action_name": "deliver_swag",
                "save_map_service_name": "/explore/save_map",
                "handoff_service_name": "/deliver/handoff_done",
                "explore_map_name": swag_map_name,
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
                "image_topic": "/zed/zed_node/rgb/color/rect/image",
                "objects_topic": "/zed/zed_node/obj_det/objects",
            }
        ],
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
            }
        ],
        additional_env=person_follow_motion_bridge_env,
        condition=person_follow_unitree_backend_condition,
    )

    # --- "explore the area" + "deliver swag" stack ------------------------------
    swag_condition = IfCondition(swag_enable)
    aruco_marker_size_value = ParameterValue(aruco_marker_size_m, value_type=float)
    aruco_detect_rate_value = ParameterValue(aruco_detect_rate_hz, value_type=float)
    pickup_marker_id_value = ParameterValue(deliver_pickup_marker_id, value_type=int)
    delivery_marker_id_value = ParameterValue(deliver_delivery_marker_id, value_type=int)
    arm_dry_run_value = ParameterValue(arm_dry_run, value_type=bool)
    swag_debug_value = ParameterValue(swag_debug, value_type=bool)
    deliver_use_arm_value = ParameterValue(deliver_use_arm, value_type=bool)
    deliver_arm_stub_wait_value = ParameterValue(deliver_arm_stub_wait_s, value_type=float)
    deliver_approach_standoff_value = ParameterValue(deliver_approach_standoff_m, value_type=float)
    deliver_align_standoff_value = ParameterValue(deliver_align_standoff_m, value_type=float)

    aruco_detector_node = Node(
        package="go2_control",
        executable="aruco_detector_node",
        name="aruco_detector_node",
        output="screen",
        # PYTHONNOUSERSITE=1 so this node ignores ~/.local (which carries a numpy 2.x that
        # is ABI-incompatible with the apt cv2/4.6 + numpy 1.26 the detector needs -> otherwise
        # `import cv2` crashes at startup). Targeted to this node; other nodes are unaffected.
        additional_env={"PYTHONNOUSERSITE": "1"},
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "image_topic": aruco_image_topic,
                "camera_info_topic": aruco_camera_info_topic,
                "dictionary": aruco_dictionary,
                "marker_size_m": aruco_marker_size_value,
                "detect_rate_hz": aruco_detect_rate_value,
                "map_frame": "map",
                "base_frame": "base_link",
                "markers_map_topic": "/aruco/markers_map",
                "markers_base_topic": "/aruco/markers_base",
                "debug": swag_debug_value,
            }
        ],
        condition=swag_condition,
    )
    map_marker_recorder_node = Node(
        package="go2_control",
        executable="map_marker_recorder_node",
        name="map_marker_recorder_node",
        output="screen",
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "robot_mode_state_topic": "/robot_mode_state",
                "markers_topic": "/aruco/markers_map",
                "maps_dir": swag_maps_dir,
                "default_map_name": swag_map_name,
                "save_service_name": "/explore/save_map",
                "debug": swag_debug_value,
            }
        ],
        condition=swag_condition,
    )
    deliver_swag_action_server = Node(
        package="go2_control",
        executable="deliver_swag_action_server",
        name="deliver_swag_action_server",
        output="screen",
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "action_name": "deliver_swag",
                "maps_dir": swag_maps_dir,
                "default_map_name": swag_map_name,
                "markers_base_topic": "/aruco/markers_base",
                "markers_map_topic": "/aruco/markers_map",
                "nav_candidate_topic": "/motion/candidate/nav",
                "sport_request_topic": "/api/sport/request",
                "arm_service_name": "/arm/play_script",
                "handoff_service_name": "/deliver/handoff_done",
                "pickup_marker_id": pickup_marker_id_value,
                "delivery_marker_id": delivery_marker_id_value,
                "use_arm": deliver_use_arm_value,
                "arm_stub_wait_s": deliver_arm_stub_wait_value,
                "approach_standoff_m": deliver_approach_standoff_value,
                "align_standoff_m": deliver_align_standoff_value,
                "debug": swag_debug_value,
            }
        ],
        condition=swag_condition,
    )
    arm_replay_node = Node(
        package="go2_arm",
        executable="arm_replay_node",
        name="arm_replay_node",
        output="screen",
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "service_name": "/arm/play_script",
                "scripts_dir": arm_scripts_dir,
                "dry_run": arm_dry_run_value,
                "debug": swag_debug_value,
            }
        ],
        condition=IfCondition(arm_enable),
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
            aruco_detector_node,
            map_marker_recorder_node,
            deliver_swag_action_server,
            arm_replay_node,
        ]
    )
