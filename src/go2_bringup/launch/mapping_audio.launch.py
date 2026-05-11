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

from _mapping_common import (
    AUDIO_ARGUMENT_NAMES,
    VOICE_ARGUMENT_NAMES,
    declare_launch_arguments,
)


ARGUMENT_NAMES = AUDIO_ARGUMENT_NAMES + VOICE_ARGUMENT_NAMES


def generate_launch_description():
    launch_dir = os.path.dirname(__file__)
    voice_control = LaunchConfiguration("voice_control")
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
    voice_debug = LaunchConfiguration("voice_debug")
    voice_command_debug = LaunchConfiguration("voice_command_debug")
    voice_command_mode = LaunchConfiguration("voice_command_mode")
    voice_command_topic = LaunchConfiguration("voice_command_topic")

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
                        "hey amigo stay",
                        "amigo stay",
                        "hey amigo stop follow me",
                        "amigo stop follow me",
                        "stand up",
                        "lay down",
                        "lie down",
                        "follow me",
                        "track me",
                        "stay",
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
    voice_command_node = Node(
        package="go2_control",
        executable="voice_command_node",
        name="voice_command_node",
        output="screen",
        parameters=[
            {
                "transcript_topic": voice_transcript_topic,
                "wake_phrase": voice_wake_phrase,
                "wake_phrases": ["amigo"],
                "shake_hand_phrase": voice_shake_hand_phrase,
                "search_phrase": voice_search_phrase,
                "search_phrases": ["look for a leak"],
                "follow_phrase": voice_follow_phrase,
                "follow_phrases": ["track me", "come with me"],
                "stop_follow_phrase": voice_stop_follow_phrase,
                "stop_follow_phrases": [
                    "stop follow me",
                    "cancel follow",
                    "stop tracking me",
                    "stay",
                ],
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
            voice_command_node,
        ]
    )
