#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from typing import List

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import AnyLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

sys.path.insert(0, os.path.dirname(__file__))

from _mapping_common import AUDIO_ARGUMENT_NAMES, VOICE_ARGUMENT_NAMES, declare_launch_arguments


ARGUMENT_NAMES = AUDIO_ARGUMENT_NAMES + VOICE_ARGUMENT_NAMES + [
    "person_follow_enable",
    "person_follow_motion_backend",
    "person_follow_unitree_network_interface",
    "startup_motion_gait",
]


def generate_launch_description():
    launch_dir = os.path.dirname(__file__)
    voice_control = LaunchConfiguration("voice_control")
    person_follow_enable = LaunchConfiguration("person_follow_enable")
    person_follow_motion_backend = LaunchConfiguration("person_follow_motion_backend")
    person_follow_unitree_network_interface = LaunchConfiguration(
        "person_follow_unitree_network_interface"
    )
    startup_motion_gait = LaunchConfiguration("startup_motion_gait")
    odas_enable = LaunchConfiguration("odas_enable")
    odas_configuration_path = LaunchConfiguration("odas_configuration_path")
    odas_audio_queue_size = LaunchConfiguration("odas_audio_queue_size")
    odas_visualization = LaunchConfiguration("odas_visualization")
    odas_force_publish_tf = LaunchConfiguration("odas_force_publish_tf")
    odas_use_echo_cancellation = LaunchConfiguration("odas_use_echo_cancellation")
    odas_echo_cancelled_signal_topic = LaunchConfiguration("odas_echo_cancelled_signal_topic")
    odas_enable_leak_classifier = LaunchConfiguration("odas_enable_leak_classifier")
    odas_leak_classifier_debug = LaunchConfiguration("odas_leak_classifier_debug")
    odas_doa_zero_offset_deg = LaunchConfiguration("odas_doa_zero_offset_deg")
    odas_log_level = LaunchConfiguration("odas_log_level")
    voice_transcript_topic = LaunchConfiguration("voice_transcript_topic")
    voice_authorized_transcript_topic = LaunchConfiguration("voice_authorized_transcript_topic")
    voice_wake_phrase = LaunchConfiguration("voice_wake_phrase")
    voice_shake_hand_phrase = LaunchConfiguration("voice_shake_hand_phrase")
    voice_search_phrase = LaunchConfiguration("voice_search_phrase")
    voice_follow_phrase = LaunchConfiguration("voice_follow_phrase")
    voice_stop_follow_phrase = LaunchConfiguration("voice_stop_follow_phrase")
    voice_stand_up_phrase = LaunchConfiguration("voice_stand_up_phrase")
    voice_lay_down_phrase = LaunchConfiguration("voice_lay_down_phrase")
    voice_stt_enable = LaunchConfiguration("voice_stt_enable")
    voice_stt_model_path = LaunchConfiguration("voice_stt_model_path")
    voice_stt_audio_topic = LaunchConfiguration("voice_stt_audio_topic")
    voice_stt_channel = LaunchConfiguration("voice_stt_channel")
    voice_stt_channel_strategy = LaunchConfiguration("voice_stt_channel_strategy")
    voice_stt_publish_partial = LaunchConfiguration("voice_stt_publish_partial")
    voice_stt_debug_audio = LaunchConfiguration("voice_stt_debug_audio")
    voice_stt_max_alternatives = LaunchConfiguration("voice_stt_max_alternatives")
    voice_verifier_enable = LaunchConfiguration("voice_verifier_enable")
    voice_verifier_audio_topic = LaunchConfiguration("voice_verifier_audio_topic")
    voice_verifier_model_name_or_path = LaunchConfiguration("voice_verifier_model_name_or_path")
    voice_verifier_reference_embedding_path = LaunchConfiguration(
        "voice_verifier_reference_embedding_path"
    )
    voice_verifier_threshold = LaunchConfiguration("voice_verifier_threshold")
    voice_verifier_score_topic = LaunchConfiguration("voice_verifier_score_topic")
    voice_verifier_authorized_topic = LaunchConfiguration("voice_verifier_authorized_topic")
    voice_verifier_decision_ttl_s = LaunchConfiguration("voice_verifier_decision_ttl_s")
    voice_verifier_debug = LaunchConfiguration("voice_verifier_debug")
    voice_verifier_window_duration_s = LaunchConfiguration("voice_verifier_window_duration_s")
    voice_verifier_eval_period_s = LaunchConfiguration("voice_verifier_eval_period_s")
    voice_verifier_channel = LaunchConfiguration("voice_verifier_channel")
    voice_verifier_channel_strategy = LaunchConfiguration("voice_verifier_channel_strategy")
    voice_verifier_min_dbfs = LaunchConfiguration("voice_verifier_min_dbfs")
    voice_command_window_s = LaunchConfiguration("voice_command_window_s")
    voice_attention_enable = LaunchConfiguration("voice_attention_enable")
    voice_attention_request_topic = LaunchConfiguration("voice_attention_request_topic")
    voice_attention_ready_topic = LaunchConfiguration("voice_attention_ready_topic")
    voice_attention_motion_cmd_topic = LaunchConfiguration("voice_attention_motion_cmd_topic")
    voice_attention_motion_reassert_topic = LaunchConfiguration(
        "voice_attention_motion_reassert_topic"
    )
    voice_attention_motion_backend = LaunchConfiguration("voice_attention_motion_backend")
    voice_attention_motion_network_interface = LaunchConfiguration(
        "voice_attention_motion_network_interface"
    )
    voice_attention_motion_gait = LaunchConfiguration("voice_attention_motion_gait")
    voice_attention_motion_command_timeout_s = LaunchConfiguration(
        "voice_attention_motion_command_timeout_s"
    )
    voice_attention_motion_gait_reassert_period_s = LaunchConfiguration(
        "voice_attention_motion_gait_reassert_period_s"
    )
    voice_attention_doa_topic = LaunchConfiguration("voice_attention_doa_topic")
    voice_attention_doa_ttl_s = LaunchConfiguration("voice_attention_doa_ttl_s")
    voice_attention_turn_tolerance_deg = LaunchConfiguration("voice_attention_turn_tolerance_deg")
    voice_attention_turn_timeout_s = LaunchConfiguration("voice_attention_turn_timeout_s")
    voice_attention_turn_kp = LaunchConfiguration("voice_attention_turn_kp")
    voice_attention_max_turn_rate_radps = LaunchConfiguration(
        "voice_attention_max_turn_rate_radps"
    )
    voice_attention_visual_refine_enable = LaunchConfiguration(
        "voice_attention_visual_refine_enable"
    )
    voice_attention_visual_target_point_topic = LaunchConfiguration(
        "voice_attention_visual_target_point_topic"
    )
    voice_attention_visual_target_visible_topic = LaunchConfiguration(
        "voice_attention_visual_target_visible_topic"
    )
    voice_attention_visual_target_status_topic = LaunchConfiguration(
        "voice_attention_visual_target_status_topic"
    )
    voice_attention_visual_objects_topic = LaunchConfiguration(
        "voice_attention_visual_objects_topic"
    )
    voice_attention_visual_refine_timeout_s = LaunchConfiguration(
        "voice_attention_visual_refine_timeout_s"
    )
    voice_attention_visual_target_ttl_s = LaunchConfiguration(
        "voice_attention_visual_target_ttl_s"
    )
    voice_attention_visual_center_tolerance_rad = LaunchConfiguration(
        "voice_attention_visual_center_tolerance_rad"
    )
    voice_attention_visual_turn_kp = LaunchConfiguration("voice_attention_visual_turn_kp")
    voice_attention_visual_max_turn_rate_radps = LaunchConfiguration(
        "voice_attention_visual_max_turn_rate_radps"
    )
    voice_attention_pitch_rad = LaunchConfiguration("voice_attention_pitch_rad")
    voice_attention_pitch_hold_s = LaunchConfiguration("voice_attention_pitch_hold_s")
    voice_attention_return_to_neutral = LaunchConfiguration("voice_attention_return_to_neutral")
    voice_attention_reassert_gait_after_pitch = LaunchConfiguration(
        "voice_attention_reassert_gait_after_pitch"
    )
    voice_attention_gait_reassert_settle_s = LaunchConfiguration(
        "voice_attention_gait_reassert_settle_s"
    )
    voice_attention_debug = LaunchConfiguration("voice_attention_debug")
    voice_debug = LaunchConfiguration("voice_debug")
    voice_command_debug = LaunchConfiguration("voice_command_debug")
    voice_command_mode = LaunchConfiguration("voice_command_mode")
    voice_command_topic = LaunchConfiguration("voice_command_topic")
    voice_verifier_condition = IfCondition(
        PythonExpression(
            ["'", voice_control, "' == 'true' and '", voice_verifier_enable, "' == 'true'"]
        )
    )
    voice_attention_condition = IfCondition(
        PythonExpression(
            [
                "'",
                voice_control,
                "' == 'true' and '",
                voice_verifier_enable,
                "' == 'true' and '",
                voice_attention_enable,
                "' == 'true'",
            ]
        )
    )
    voice_command_transcript_topic = PythonExpression(
        [
            "'",
            voice_authorized_transcript_topic,
            "' if '",
            voice_verifier_enable,
            "' == 'true' else '",
            voice_transcript_topic,
            "'",
        ]
    )
    voice_attention_motion_bridge_env = {"RMW_IMPLEMENTATION": "rmw_fastrtps_cpp"}

    odas_launch = IncludeLaunchDescription(
        AnyLaunchDescriptionSource(
            os.path.join(get_package_share_directory("odas_ros"), "launch", "odas.launch.xml")
        ),
        launch_arguments={
            "configuration_path": odas_configuration_path,
            "audio_queue_size": odas_audio_queue_size,
            "visualization": odas_visualization,
            "force_publish_tf": odas_force_publish_tf,
            "use_echo_cancellation": odas_use_echo_cancellation,
            "echo_cancelled_signal_topic": odas_echo_cancelled_signal_topic,
            "enable_leak_classifier": odas_enable_leak_classifier,
            "leak_classifier_debug": odas_leak_classifier_debug,
            "doa_zero_offset_deg": odas_doa_zero_offset_deg,
            "log_level": odas_log_level,
        }.items(),
        condition=IfCondition(odas_enable),
    )
    voice_stt_vosk_node = Node(
        package="go2_control",
        executable="voice_stt_vosk_node",
        name="voice_stt_vosk_node",
        output="screen",
        parameters=[
            {
                "audio_topic": voice_stt_audio_topic,
                "transcript_topic": voice_transcript_topic,
                "model_path": voice_stt_model_path,
                "channel_index": voice_stt_channel,
                "channel_strategy": voice_stt_channel_strategy,
                "sample_rate": 16000,
                "audio_format": "signed_16",
                "publish_partial": voice_stt_publish_partial,
                "log_partial_hypotheses": voice_debug,
                "log_empty_results": voice_debug,
                "log_raw_results": voice_debug,
                "debug_audio_stats": voice_stt_debug_audio,
                "audio_stats_period_s": 1.0,
                "max_alternatives": voice_stt_max_alternatives,
                "log_word_details": voice_debug,
                "grammar_phrases": ParameterValue(
                    [
                        [voice_shake_hand_phrase],
                        "hey amigo",
                        "amigo",
                        "hey amigo stand up",
                        "amigo stand up",
                        "hey amigo lay down",
                        "amigo lay down",
                        "hey amigo can you stand up",
                        "amigo can you stand up",
                        "hey amigo can you get up",
                        "amigo can you get up",
                        "hey amigo can you lay down",
                        "amigo can you lay down",
                        "hey amigo can you lie down",
                        "amigo can you lie down",
                        "hey amigo can you look for a leak",
                        "amigo can you look for a leak",
                        "hey amigo follow me",
                        "amigo follow me",
                        "hey amigo can you follow me",
                        "amigo can you follow me",
                        "hey amigo track me",
                        "amigo track me",
                        "hey amigo stop following",
                        "amigo stop following",
                        "hey amigo stop follow me",
                        "amigo stop follow me",
                        "stand up",
                        "lay down",
                        "lie down",
                        "follow me",
                        "track me",
                        "stop following",
                        "stop follow me",
                        "look for a leak",
                    ],
                    value_type=List[str],
                ),
            }
        ],
        condition=IfCondition(
            PythonExpression(
                ["'", voice_control, "' == 'true' and '", voice_stt_enable, "' == 'true'"]
            )
        ),
    )
    voice_speaker_verifier_node = Node(
        package="go2_control",
        executable="voice_speaker_verifier_node",
        name="voice_speaker_verifier_node",
        output="screen",
        parameters=[
            {
                "audio_topic": voice_verifier_audio_topic,
                "model_name_or_path": voice_verifier_model_name_or_path,
                "reference_embedding_path": voice_verifier_reference_embedding_path,
                "threshold": voice_verifier_threshold,
                "sample_rate": 16000,
                "channel_index": voice_verifier_channel,
                "channel_strategy": voice_verifier_channel_strategy,
                "window_duration_s": voice_verifier_window_duration_s,
                "eval_period_s": voice_verifier_eval_period_s,
                "min_dbfs": voice_verifier_min_dbfs,
                "debug": voice_verifier_debug,
                "score_topic": voice_verifier_score_topic,
                "authorized_topic": voice_verifier_authorized_topic,
            }
        ],
        condition=voice_verifier_condition,
    )
    voice_identity_gate_node = Node(
        package="go2_control",
        executable="voice_identity_gate_node",
        name="voice_identity_gate_node",
        output="screen",
        parameters=[
            {
                "input_transcript_topic": voice_transcript_topic,
                "output_transcript_topic": voice_authorized_transcript_topic,
                "authorized_topic": voice_verifier_authorized_topic,
                "score_topic": voice_verifier_score_topic,
                "wake_phrase": voice_wake_phrase,
                "wake_phrases": ["amigo"],
                "decision_ttl_s": voice_verifier_decision_ttl_s,
                "command_window_s": voice_command_window_s,
                "attention_enabled": voice_attention_enable,
                "attention_request_topic": voice_attention_request_topic,
                "attention_ready_topic": voice_attention_ready_topic,
                "post_command_hold_s": voice_attention_pitch_hold_s,
                "debug": voice_verifier_debug,
            }
        ],
        condition=voice_verifier_condition,
    )
    voice_attention_ack_node = Node(
        package="go2_control",
        executable="voice_attention_ack_node",
        name="voice_attention_ack_node",
        output="screen",
        parameters=[
            {
                "request_topic": voice_attention_request_topic,
                "ready_topic": voice_attention_ready_topic,
                "turn_cmd_topic": voice_attention_motion_cmd_topic,
                "gait_reassert_topic": voice_attention_motion_reassert_topic,
                "doa_topic": voice_attention_doa_topic,
                "sst_topic": "/sst",
                "doa_ttl_s": voice_attention_doa_ttl_s,
                "doa_zero_offset_deg": odas_doa_zero_offset_deg,
                "turn_tolerance_deg": voice_attention_turn_tolerance_deg,
                "turn_timeout_s": voice_attention_turn_timeout_s,
                "turn_kp": voice_attention_turn_kp,
                "max_turn_rate_radps": voice_attention_max_turn_rate_radps,
                "person_follow_enable": person_follow_enable,
                "visual_refine_enable": voice_attention_visual_refine_enable,
                "visual_target_point_topic": voice_attention_visual_target_point_topic,
                "visual_target_visible_topic": voice_attention_visual_target_visible_topic,
                "visual_target_status_topic": voice_attention_visual_target_status_topic,
                "visual_objects_topic": voice_attention_visual_objects_topic,
                "visual_refine_timeout_s": voice_attention_visual_refine_timeout_s,
                "visual_target_ttl_s": voice_attention_visual_target_ttl_s,
                "visual_center_tolerance_rad": voice_attention_visual_center_tolerance_rad,
                "visual_turn_kp": voice_attention_visual_turn_kp,
                "visual_max_turn_rate_radps": voice_attention_visual_max_turn_rate_radps,
                "pitch_rad": voice_attention_pitch_rad,
                "pitch_hold_s": voice_attention_pitch_hold_s,
                "return_to_neutral": voice_attention_return_to_neutral,
                "reassert_gait_after_pitch": voice_attention_reassert_gait_after_pitch,
                "gait_reassert_settle_s": voice_attention_gait_reassert_settle_s,
                "debug": voice_attention_debug,
            }
        ],
        condition=voice_attention_condition,
    )
    voice_attention_motion_bridge_node = Node(
        package="go2_driver",
        executable="voice_attention_motion_bridge_node",
        name="voice_attention_motion_bridge_node",
        output="screen",
        parameters=[
            {
                "backend": voice_attention_motion_backend,
                "network_interface": voice_attention_motion_network_interface,
                "desired_gait": voice_attention_motion_gait,
                "cmd_vel_topic": voice_attention_motion_cmd_topic,
                "reassert_gait_topic": voice_attention_motion_reassert_topic,
                "command_timeout_s": voice_attention_motion_command_timeout_s,
                "gait_reassert_period_s": voice_attention_motion_gait_reassert_period_s,
                "debug": voice_attention_debug,
            }
        ],
        additional_env=voice_attention_motion_bridge_env,
        condition=voice_attention_condition,
    )
    voice_command_node = Node(
        package="go2_control",
        executable="voice_command_node",
        name="voice_command_node",
        output="screen",
        parameters=[
            {
                "transcript_topic": ParameterValue(voice_command_transcript_topic, value_type=str),
                "wake_phrase": voice_wake_phrase,
                "wake_phrases": ["amigo"],
                "shake_hand_phrase": voice_shake_hand_phrase,
                "search_phrase": voice_search_phrase,
                "search_phrases": ["look for a leak"],
                "follow_phrase": voice_follow_phrase,
                "follow_phrases": ["track me", "come with me"],
                "stop_follow_phrase": voice_stop_follow_phrase,
                "stop_follow_phrases": ["stop follow me", "cancel follow", "stop tracking me"],
                "stand_up_phrase": voice_stand_up_phrase,
                "stand_up_phrases": ["get up"],
                "lay_down_phrase": voice_lay_down_phrase,
                "lay_down_phrases": ["lie down", "down"],
                "command_mode": voice_command_mode,
                "command_topic": voice_command_topic,
                "log_transcripts": voice_debug,
                "debug_decisions": voice_command_debug,
                "debug_topic": "/voice/debug",
                "publish_debug_topic": True,
            }
        ],
        condition=IfCondition(voice_control),
    )

    return LaunchDescription(
        declare_launch_arguments(ARGUMENT_NAMES, launch_dir) +
        [
            odas_launch,
            voice_stt_vosk_node,
            voice_speaker_verifier_node,
            voice_identity_gate_node,
            voice_attention_ack_node,
            voice_attention_motion_bridge_node,
            voice_command_node,
        ]
    )
