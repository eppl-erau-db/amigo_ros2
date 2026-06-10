#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import sys
import tempfile
from typing import List

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, LogInfo, OpaqueFunction
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


def _detect_respeaker_card():
    """Return the ALSA card index whose name matches the ReSpeaker, else None.

    ALSA card indices are NOT stable across reboots / USB re-enumeration: the
    Jetson onboard audio (APE/HDA) and the USB ReSpeaker can swap numbers (we have
    seen the ReSpeaker on card 0 and on card 2). So we look it up by name at launch
    time instead of trusting the hardcoded `card = N;` in the ODAS .cfg.
    """
    try:
        with open("/proc/asound/cards", encoding="utf-8") as handle:
            cards = handle.read()
    except OSError:
        return None
    for line in cards.splitlines():
        # e.g. " 2 [ArrayUAC10     ]: USB-Audio - ReSpeaker 4 Mic Array (UAC1.0)"
        if "ReSpeaker" in line or "ArrayUAC10" in line:
            match = re.match(r"\s*(\d+)\s", line)
            if match:
                return int(match.group(1))
    return None


def _odas_cfg_with_card(cfg_path, card):
    """Write a temp copy of the ODAS cfg with the soundcard `card = N;` set to the
    detected ReSpeaker index, and return its path. Returns cfg_path unchanged if the
    card is unknown, the cfg has no soundcard line, or anything goes wrong.
    """
    if card is None:
        return cfg_path
    try:
        with open(cfg_path, encoding="utf-8") as handle:
            text = handle.read()
        # The raw/soundcard `interface` block is the only `card = N;` in the cfg
        # (socket sinks use `port`), so a single first-match replace is safe.
        patched, count = re.subn(r"card\s*=\s*\d+\s*;", f"card = {card};", text, count=1)
        if count == 0:
            return cfg_path
        out_path = os.path.join(tempfile.gettempdir(), "odas_respeaker_runtime.cfg")
        with open(out_path, "w", encoding="utf-8") as handle:
            handle.write(patched)
        return out_path
    except OSError:
        return cfg_path


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
    odas_leak_classifier_params_file = LaunchConfiguration("odas_leak_classifier_params_file")
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

    # Resolve the ReSpeaker's ALSA card at launch time (it is not stable across
    # reboots) and feed ODAS a cfg patched to match, instead of a hardcoded card.
    def _odas_actions(context):
        cfg_path = odas_configuration_path.perform(context)
        card = _detect_respeaker_card()
        resolved_path = _odas_cfg_with_card(cfg_path, card)
        if card is not None:
            info = f"[ODAS] ReSpeaker on ALSA card {card}; using {resolved_path}"
        else:
            info = (
                "[ODAS] ReSpeaker NOT found in /proc/asound/cards (check `arecord -l`); "
                f"falling back to hardcoded card in {cfg_path}"
            )
        return [
            LogInfo(msg=info),
            IncludeLaunchDescription(
                AnyLaunchDescriptionSource(
                    os.path.join(get_package_share_directory("odas_ros"), "launch", "odas.launch.xml")
                ),
                launch_arguments={
                    "configuration_path": resolved_path,
                    "audio_queue_size": odas_audio_queue_size,
                    "visualization": odas_visualization,
                    "force_publish_tf": odas_force_publish_tf,
                    "use_echo_cancellation": odas_use_echo_cancellation,
                    "echo_cancelled_signal_topic": odas_echo_cancelled_signal_topic,
                    "enable_leak_classifier": odas_enable_leak_classifier,
                    "leak_classifier_debug": odas_leak_classifier_debug,
                    "leak_classifier_params_file": odas_leak_classifier_params_file,
                    "doa_zero_offset_deg": odas_doa_zero_offset_deg,
                    "log_level": odas_log_level,
                }.items(),
                condition=IfCondition(odas_enable),
            ),
        ]

    odas_launch = OpaqueFunction(function=_odas_actions)
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
                        "hey amigo lets explore the area",
                        "amigo lets explore the area",
                        "lets explore the area",
                        "hey amigo explore the area",
                        "amigo explore the area",
                        "explore the area",
                        "hey amigo we are done exploring",
                        "amigo we are done exploring",
                        "we are done exploring",
                        "done exploring",
                        "hey amigo deliver swag",
                        "amigo deliver swag",
                        "deliver swag",
                        "deliver the swag",
                        "hey amigo all done",
                        "amigo all done",
                        "all done",
                        "all finished",
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
                "explore_phrase": "explore the area",
                "explore_phrases": ["lets explore the area", "let s explore the area"],
                "done_exploring_phrase": "done exploring",
                "done_exploring_phrases": ["we are done exploring", "were done exploring"],
                "deliver_phrase": "deliver swag",
                "deliver_phrases": ["deliver the swag"],
                "handoff_done_phrase": "all done",
                "handoff_done_phrases": ["all finished", "we are all done"],
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
