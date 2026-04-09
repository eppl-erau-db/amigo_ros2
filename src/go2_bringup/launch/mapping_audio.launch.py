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
    voice_instant_hello_phrase = LaunchConfiguration("voice_instant_hello_phrase")
    voice_shake_hand_phrase = LaunchConfiguration("voice_shake_hand_phrase")
    voice_ready_phrase = LaunchConfiguration("voice_ready_phrase")
    voice_upright_phrase = LaunchConfiguration("voice_upright_phrase")
    voice_search_phrase = LaunchConfiguration("voice_search_phrase")
    voice_explore_area_phrase = LaunchConfiguration("voice_explore_area_phrase")
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
    voice_wake_window_s = LaunchConfiguration("voice_wake_window_s")
    voice_command_mode = LaunchConfiguration("voice_command_mode")
    voice_command_topic = LaunchConfiguration("voice_command_topic")
    speaker_verification_enabled = LaunchConfiguration("speaker_verification_enabled")
    speaker_verification_topic = LaunchConfiguration("speaker_verification_topic")
    speaker_verification_window_s = LaunchConfiguration("speaker_verification_window_s")
    voice_verifier_enable = LaunchConfiguration("voice_verifier_enable")
    voice_verifier_model_name_or_path = LaunchConfiguration("voice_verifier_model_name_or_path")
    voice_verifier_reference_embedding_path = LaunchConfiguration("voice_verifier_reference_embedding_path")
    voice_verifier_threshold = LaunchConfiguration("voice_verifier_threshold")
    voice_verifier_window_duration_s = LaunchConfiguration("voice_verifier_window_duration_s")
    voice_verifier_eval_period_s = LaunchConfiguration("voice_verifier_eval_period_s")
    voice_verifier_debug = LaunchConfiguration("voice_verifier_debug")

    def _prefixed_phrase(prefix, phrase):
        return [prefix, " ", phrase]

    def _polite_phrase(prefix, phrase):
        return [prefix, " can you ", phrase]

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
                        voice_instant_hello_phrase,
                        voice_shake_hand_phrase,
                        voice_ready_phrase,
                        voice_upright_phrase,
                        "get ready",
                        "upright",
                        "walk upright",
                        "can you say hello",
                        "can you greet people",
                        "greet people",
                        voice_wake_phrase,
                        "amigo",
                        _prefixed_phrase(voice_wake_phrase, voice_shake_hand_phrase),
                        _prefixed_phrase("amigo", voice_shake_hand_phrase),
                        _polite_phrase(voice_wake_phrase, voice_shake_hand_phrase),
                        _polite_phrase("amigo", voice_shake_hand_phrase),
                        _prefixed_phrase(voice_wake_phrase, voice_stand_up_phrase),
                        _prefixed_phrase("amigo", voice_stand_up_phrase),
                        _prefixed_phrase(voice_wake_phrase, voice_lay_down_phrase),
                        _prefixed_phrase("amigo", voice_lay_down_phrase),
                        _prefixed_phrase(voice_wake_phrase, voice_ready_phrase),
                        _prefixed_phrase("amigo", voice_ready_phrase),
                        "hey amigo get ready",
                        "amigo get ready",
                        _prefixed_phrase(voice_wake_phrase, voice_upright_phrase),
                        _prefixed_phrase("amigo", voice_upright_phrase),
                        "hey amigo upright",
                        "amigo upright",
                        "hey amigo walk upright",
                        "amigo walk upright",
                        _polite_phrase(voice_wake_phrase, voice_stand_up_phrase),
                        _polite_phrase("amigo", voice_stand_up_phrase),
                        "hey amigo can you get up",
                        "amigo can you get up",
                        _polite_phrase(voice_wake_phrase, voice_lay_down_phrase),
                        _polite_phrase("amigo", voice_lay_down_phrase),
                        "hey amigo can you lie down",
                        "amigo can you lie down",
                        _polite_phrase(voice_wake_phrase, voice_search_phrase),
                        _polite_phrase("amigo", voice_search_phrase),
                        _prefixed_phrase(voice_wake_phrase, voice_explore_area_phrase),
                        _prefixed_phrase("amigo", voice_explore_area_phrase),
                        _polite_phrase(voice_wake_phrase, voice_explore_area_phrase),
                        _polite_phrase("amigo", voice_explore_area_phrase),
                        "hey amigo explore",
                        "amigo explore",
                        _prefixed_phrase(voice_wake_phrase, voice_follow_phrase),
                        _prefixed_phrase("amigo", voice_follow_phrase),
                        _polite_phrase(voice_wake_phrase, voice_follow_phrase),
                        _polite_phrase("amigo", voice_follow_phrase),
                        "hey amigo track me",
                        "amigo track me",
                        "hey amigo come with me",
                        "amigo come with me",
                        _prefixed_phrase(voice_wake_phrase, voice_stop_follow_phrase),
                        _prefixed_phrase("amigo", voice_stop_follow_phrase),
                        "hey amigo stop following",
                        "amigo stop following",
                        "hey amigo stop follow me",
                        "amigo stop follow me",
                        "hey amigo stop searching",
                        "amigo stop searching",
                        "hey amigo stop search",
                        "amigo stop search",
                        voice_stand_up_phrase,
                        voice_lay_down_phrase,
                        "get up",
                        "lie down",
                        "down",
                        voice_follow_phrase,
                        "track me",
                        "come with me",
                        voice_stop_follow_phrase,
                        "stay",
                        "stop following",
                        "stop follow me",
                        "cancel follow",
                        "stop tracking me",
                        "stop searching",
                        "stop search",
                        "stop saying hello",
                        "stop greeting",
                        "return to idle",
                        voice_search_phrase,
                        voice_explore_area_phrase,
                        "can you explore the area",
                        "explore",
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
                "instant_hello_phrase": voice_instant_hello_phrase,
                "instant_hello_phrases": [""],
                "say_hello_phrase": voice_shake_hand_phrase,
                "say_hello_phrases": ["can you say hello", "can you greet people", "greet people"],
                "ready_phrase": voice_ready_phrase,
                "ready_phrases": ["get ready"],
                "upright_phrase": voice_upright_phrase,
                "upright_phrases": ["upright", "walk upright"],
                "search_phrase": voice_search_phrase,
                "search_phrases": ["look for a leak"],
                "explore_area_phrase": voice_explore_area_phrase,
                "explore_area_phrases": ["can you explore the area", "explore"],
                "follow_phrase": voice_follow_phrase,
                "follow_phrases": ["track me", "come with me"],
                "stop_follow_phrase": voice_stop_follow_phrase,
                "stop_follow_phrases": [
                    "stop following",
                    "stop follow me",
                    "cancel follow",
                    "stop tracking me",
                    "stop searching",
                    "stop search",
                    "stop saying hello",
                    "stop greeting",
                    "return to idle",
                ],
                "stand_up_phrase": voice_stand_up_phrase,
                "stand_up_phrases": ["get up"],
                "lay_down_phrase": voice_lay_down_phrase,
                "lay_down_phrases": ["lie down", "down"],
                "wake_window_s": voice_wake_window_s,
                "command_mode": voice_command_mode,
                "command_topic": voice_command_topic,
                "robot_mode_state_topic": "/robot_mode_state",
                "wake_attention_command": "wake_attention",
                "wake_attention_status_topic": "/voice/attention/status",
                "log_transcripts": voice_debug,
                "debug_decisions": voice_command_debug,
                "debug_topic": "/voice/debug",
                "publish_debug_topic": True,
                "speaker_verification_enabled": PythonExpression([
                    "'", speaker_verification_enabled, "' == 'true' or '",
                    voice_verifier_enable, "' == 'true'"
                ]),
                "speaker_verification_topic": speaker_verification_topic,
                "speaker_verification_window_s": speaker_verification_window_s,
            }
        ],
        condition=IfCondition(voice_control),
    )

    voice_speaker_verifier_node = Node(
        package="go2_control",
        executable="voice_speaker_verifier_node",
        name="voice_speaker_verifier_node",
        output="screen",
        parameters=[
            {
                "audio_topic": voice_stt_audio_topic,
                "model_name_or_path": voice_verifier_model_name_or_path,
                "reference_embedding_path": voice_verifier_reference_embedding_path,
                "threshold": voice_verifier_threshold,
                "sample_rate": 16000,
                "channel_index": voice_stt_channel,
                "channel_strategy": voice_stt_channel_strategy,
                "window_duration_s": voice_verifier_window_duration_s,
                "eval_period_s": voice_verifier_eval_period_s,
                "min_rms": 0.01,
                "debug": voice_verifier_debug,
                "score_topic": "/voice/speaker_score",
                "authorized_topic": speaker_verification_topic,
                "doa_topic": "/doa_angle",
                "direction_topic": "/voice/speaker_direction",
            }
        ],
        condition=IfCondition(
            PythonExpression(
                ["'", voice_control, "' == 'true' and '", voice_verifier_enable, "' == 'true'"]
            )
        ),
    )

    return LaunchDescription(
        declare_launch_arguments(ARGUMENT_NAMES, launch_dir) +
        [
            odas_launch,
            voice_stt_vosk_node,
            voice_command_node,
            voice_speaker_verifier_node,
        ]
    )
