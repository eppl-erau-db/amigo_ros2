#!/usr/bin/env python3
from __future__ import annotations

import ast
import math
import os

import yaml
from ament_index_python.packages import get_package_share_directory, get_package_share_path
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression


CORE_ARGUMENT_NAMES = [
    "launch_profile",
    "use_sim_time",
]

AUDIO_ARGUMENT_NAMES = [
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
]

VOICE_ARGUMENT_NAMES = [
    "voice_control",
    "voice_transcript_topic",
    "voice_wake_phrase",
    "voice_instant_hello_phrase",
    "voice_shake_hand_phrase",
    "voice_ready_phrase",
    "voice_upright_phrase",
    "voice_search_phrase",
    "voice_explore_area_phrase",
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
    "voice_wake_window_s",
    "voice_command_cooldown_s",
    "voice_command_mode",
    "voice_command_topic",
    "speaker_verification_enabled",
    "speaker_verification_topic",
    "speaker_verification_window_s",
    "voice_verifier_enable",
    "voice_verifier_model_name_or_path",
    "voice_verifier_reference_embedding_path",
    "voice_verifier_threshold",
    "voice_verifier_window_duration_s",
    "voice_verifier_eval_period_s",
    "voice_verifier_debug",
]

FOLLOW_ARGUMENT_NAMES = [
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
    "zed_follow_params_path",
]

MISSION_ARGUMENT_NAMES = [
    "sound_localizer_enable",
    "search_debug",
    "search_allow_unknown",
    "explore_area_debug",
    "explore_area_landmark_config_path",
    "explore_area_artifact_root",
    "explore_area_park_at_home_on_complete",
    "startup_motion_mode",
    "startup_motion_gait",
    "startup_motion_wait_s",
    "startup_motion_retries",
    "startup_motion_retry_interval_s",
]

ALL_ARGUMENT_NAMES = (
    CORE_ARGUMENT_NAMES +
    AUDIO_ARGUMENT_NAMES +
    VOICE_ARGUMENT_NAMES +
    FOLLOW_ARGUMENT_NAMES +
    MISSION_ARGUMENT_NAMES
)


def _default_vosk_model_path(launch_dir: str) -> str:
    explicit = os.environ.get("VOSK_MODEL_PATH", "").strip()
    if explicit:
        return explicit

    candidate_roots = [
        os.path.abspath(os.path.join(launch_dir, "../../..")),
        os.path.abspath(os.path.join(launch_dir, "../../../../..")),
        os.getcwd(),
    ]
    for root in candidate_roots:
        bundled_path = os.path.join(root, "models", "vosk-model-small-en-us-0.15")
        if os.path.isdir(bundled_path):
            return bundled_path
    return ""


def build_argument_specs(launch_dir: str) -> dict[str, tuple[str, str]]:
    return {
        "launch_profile": ("all", "Launch profile: all, mission_base, or operator_tools"),
        "use_sim_time": ("false", "Use simulated clock if true"),
        "odas_enable": ("true", "Include and run odas_ros/odas.launch.xml"),
        "odas_configuration_path": (
            os.path.join(
                get_package_share_directory("odas_ros"),
                "config",
                "odas_jetson_respeaker_sep.cfg",
            ),
            "Path to ODAS configuration file",
        ),
        "odas_audio_queue_size": ("1", "ODAS audio queue size"),
        "odas_visualization": ("false", "Enable ODAS visualization node"),
        "odas_force_publish_tf": ("false", "Force ODAS static TF publication"),
        "odas_use_echo_cancellation": ("false", "Enable ODAS echo-cancelled audio path"),
        "odas_echo_cancelled_signal_topic": (
            "ec_signal",
            "Topic used as ODAS echo-cancelled signal input",
        ),
        "odas_enable_leak_classifier": (
            "true",
            "Enable ODAS leak classifier node (/leak_detected, /doa_angle)",
        ),
        "odas_leak_classifier_debug": (
            "false",
            "Enable debug logs in ODAS leak classifier",
        ),
        "odas_doa_zero_offset_deg": (
            "129.0",
            "ODAS DoA zero-offset calibration (degrees)",
        ),
        "odas_log_level": (
            "warn",
            "ODAS ROS log verbosity (debug, info, warn, error, fatal)",
        ),
        "sound_localizer_enable": ("true", "Enable the map-frame sound localization node"),
        "search_debug": ("false", "Enable verbose leak-search diagnostics"),
        "search_allow_unknown": (
            "true",
            "Deprecated: leak localization now derives unknown-space policy from nav2_mppi_controller.yaml",
        ),
        "explore_area_debug": (
            "false",
            "Enable verbose explore-area mission diagnostics and publish /explore_area/debug events",
        ),
        "explore_area_landmark_config_path": (
            "",
            "Optional override path for the explore-area ArUco landmark config YAML",
        ),
        "explore_area_artifact_root": (
            "artifacts/explore_area",
            "Directory where explore-area map and landmark artifacts are written",
        ),
        "explore_area_park_at_home_on_complete": (
            "false",
            "If true, visit the home_dock landmark and call its parking hook after frontier exploration completes",
        ),
        "voice_control": (
            "false",
            "Enable voice command node and leak search action server",
        ),
        "voice_transcript_topic": (
            "/voice/transcript",
            "Transcript topic (std_msgs/String)",
        ),
        "voice_wake_phrase": ("hey amigo", "Wake phrase that arms the command parser"),
        "voice_instant_hello_phrase": (
            "hello amigo",
            "Exact no-wake phrase for the idle-only visible-person hello gesture",
        ),
        "voice_shake_hand_phrase": (
            "say hello",
            "Phrase that triggers the stateful hello greeting behavior",
        ),
        "voice_ready_phrase": (
            "ready",
            "Phrase that triggers the nod-and-stretch ready sequence",
        ),
        "voice_upright_phrase": (
            "up",
            "Phrase that enables the hind-leg upright stance",
        ),
        "voice_search_phrase": (
            "look for a leak",
            "Phrase that triggers Search action",
        ),
        "voice_explore_area_phrase": (
            "explore the area",
            "Phrase that triggers the area exploration mission",
        ),
        "voice_follow_phrase": (
            "follow me",
            "Phrase that enables person-follow mode",
        ),
        "voice_stop_follow_phrase": (
            "stay",
            "Phrase that returns the robot to IDLE and cancels follow/search",
        ),
        "voice_stand_up_phrase": (
            "stand up",
            "Phrase that requests a stand-up posture transition",
        ),
        "voice_lay_down_phrase": (
            "lay down",
            "Phrase that requests a lay-down posture transition",
        ),
        "voice_stt_enable": (
            "true",
            "Enable Vosk STT bridge node (AudioFrame -> /voice/transcript)",
        ),
        "voice_stt_model_path": (
            _default_vosk_model_path(launch_dir),
            "Path to local Vosk model directory",
        ),
        "voice_stt_audio_topic": ("/sss", "AudioFrame topic used as STT input"),
        "voice_stt_channel": ("0", "Channel index from AudioFrame for STT"),
        "voice_stt_channel_strategy": (
            "max_rms",
            'STT channel strategy: "fixed" or "max_rms"',
        ),
        "voice_stt_publish_partial": (
            "false",
            "Publish partial STT hypotheses to /voice/partial",
        ),
        "voice_stt_debug_audio": (
            "false",
            "Enable periodic STT audio level/channel debug logs",
        ),
        "voice_stt_max_alternatives": (
            "3",
            "Vosk max alternatives per final result (0 disables)",
        ),
        "voice_debug": ("false", "Enable verbose voice pipeline debugging logs"),
        "voice_command_debug": (
            "false",
            "Enable voice command decision debug logs",
        ),
        "voice_wake_window_s": (
            "8.0",
            "How long the wake-command window remains open after the wake acknowledgment",
        ),
        "voice_command_cooldown_s": (
            "3.0",
            "Per-command cooldown between accepted supervisor voice commands",
        ),
        "voice_command_mode": (
            "all",
            "Voice command behavior mode: search, sport_test, follow, or all",
        ),
        "voice_command_topic": (
            "/voice/command",
            "Topic where parsed voice commands are published",
        ),
        "speaker_verification_enabled": (
            "false",
            "Gate voice commands on speaker identity verification",
        ),
        "speaker_verification_topic": (
            "/voice/speaker_verified",
            "Topic (std_msgs/Bool) published by a speaker verification node",
        ),
        "speaker_verification_window_s": (
            "10.0",
            "How long a speaker verification confirmation remains valid",
        ),
        "voice_verifier_enable": (
            "false",
            "Launch the WeSpeaker speaker verification node",
        ),
        "voice_verifier_model_name_or_path": (
            "eres2net",
            "WeSpeaker model name or filesystem path (eres2net=55M params, best accuracy)",
        ),
        "voice_verifier_reference_embedding_path": (
            "",
            "Path to .npy reference speaker embedding (required when verifier enabled)",
        ),
        "voice_verifier_threshold": (
            "0.55",
            "Cosine similarity threshold for speaker verification (EMA-smoothed score)",
        ),
        "voice_verifier_window_duration_s": (
            "2.0",
            "Audio window duration in seconds for speaker embedding",
        ),
        "voice_verifier_eval_period_s": (
            "0.5",
            "How often (seconds) to evaluate the audio window",
        ),
        "voice_verifier_debug": (
            "false",
            "Enable debug logging in the speaker verifier node",
        ),
        "person_follow_enable": (
            "true",
            "Enable the person-follow perception and control stack",
        ),
        "person_follow_distance_m": (
            "0.75",
            "Desired person-follow standoff distance in meters",
        ),
        "person_follow_distance_band_m": (
            "0.10",
            "Allowed standoff band around the desired follow distance in meters",
        ),
        "person_follow_max_vx_mps": (
            "0.60",
            "Maximum forward follow speed in meters per second",
        ),
        "person_follow_max_vy_mps": (
            "0.30",
            "Maximum lateral follow speed in meters per second",
        ),
        "person_follow_max_wz_radps": (
            "1.20",
            "Maximum follow yaw rate in radians per second",
        ),
        "person_follow_use_strafe": (
            "false",
            "Allow strafing in follow mode instead of rotate-first centering",
        ),
        "person_follow_candidate_horizon_s": (
            "0.80",
            "Short-horizon safety simulation window for follow controller commands",
        ),
        "person_follow_reacquire_timeout_s": (
            "1.50",
            "How long to actively yaw-search after a target loss before holding position",
        ),
        "person_follow_sit_on_loss_timeout_s": (
            "3.00",
            "How long to wait after sustained target loss before emitting a timeout event",
        ),
        "person_follow_debug": (
            "false",
            "Enable extra person-follow controller debug logging",
        ),
        "person_follow_motion_backend": (
            "sport_free_avoid",
            "Follow motion backend: legacy, sport_free_avoid, or obstacles_avoid",
        ),
        "person_follow_unitree_cmd_vel_topic": (
            "/person_follow/cmd_vel",
            "Velocity topic consumed by the Unitree follow-motion bridge",
        ),
        "person_follow_unitree_network_interface": (
            "",
            "Optional network interface passed to Unitree SDK2 clients",
        ),
        "person_follow_unitree_command_timeout_s": (
            "0.5",
            "How long the Unitree follow-motion bridge waits before sending a stop command",
        ),
        "startup_motion_mode": (
            "none",
            "Optional Unitree motion service to select at launch",
        ),
        "startup_motion_gait": (
            "static_walk",
            "Unitree gait to apply at launch",
        ),
        "startup_motion_wait_s": (
            "2.0",
            "How long the one-shot Unitree startup motion switcher waits before attempting mode and gait selection",
        ),
        "startup_motion_retries": (
            "10",
            "How many times the startup motion switcher retries mode and gait selection",
        ),
        "startup_motion_retry_interval_s": (
            "2.0",
            "Delay between startup motion switcher retry attempts",
        ),
        "zed_follow_params_path": (
            os.path.join(
                get_package_share_directory("go2_bringup"),
                "config",
                "zed_follow_person.yaml",
            ),
            "ROS params override YAML for the ZED follow-person object-detection pipeline",
        ),
    }


def declare_launch_arguments(names: list[str], launch_dir: str) -> list[DeclareLaunchArgument]:
    specs = build_argument_specs(launch_dir)
    actions: list[DeclareLaunchArgument] = []
    for name in names:
        default_value, description = specs[name]
        actions.append(
            DeclareLaunchArgument(
                name=name,
                default_value=str(default_value),
                description=description,
            )
        )
    return actions


def launch_argument_mapping(names: list[str]) -> dict[str, LaunchConfiguration]:
    return {name: LaunchConfiguration(name) for name in names}


def _load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def _deep_get(mapping: dict, keys: list[str], default=None):
    current = mapping
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def _parse_footprint(raw_value) -> list[tuple[float, float]]:
    if raw_value in (None, "", []):
        return []
    value = raw_value
    if isinstance(raw_value, str):
        value = ast.literal_eval(raw_value)
    points: list[tuple[float, float]] = []
    for item in value:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            points.append((float(item[0]), float(item[1])))
    return points


def _distance_point_to_segment(
    px: float,
    py: float,
    ax: float,
    ay: float,
    bx: float,
    by: float,
) -> float:
    abx = bx - ax
    aby = by - ay
    denom = (abx * abx) + (aby * aby)
    if denom <= 0.0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, (((px - ax) * abx) + ((py - ay) * aby)) / denom))
    proj_x = ax + (t * abx)
    proj_y = ay + (t * aby)
    return math.hypot(px - proj_x, py - proj_y)


def _inscribed_radius(points: list[tuple[float, float]]) -> float:
    if len(points) < 2:
        return 0.0
    radius = float("inf")
    wrapped = points[1:] + points[:1]
    for (ax, ay), (bx, by) in zip(points, wrapped):
        radius = min(radius, _distance_point_to_segment(0.0, 0.0, ax, ay, bx, by))
    return 0.0 if math.isinf(radius) else radius


def derive_nav2_settings(nav2_cfg_path: str) -> dict[str, float | bool]:
    data = _load_yaml(nav2_cfg_path)
    planner_params = _deep_get(data, ["planner_server", "ros__parameters", "GridBased"], {}) or {}
    local_params = _deep_get(data, ["local_costmap", "local_costmap", "ros__parameters"], {}) or {}
    global_params = _deep_get(data, ["global_costmap", "global_costmap", "ros__parameters"], {}) or {}

    local_footprint = _parse_footprint(local_params.get("footprint"))
    local_padding = float(local_params.get("footprint_padding", 0.0) or 0.0)
    local_robot_radius = float(local_params.get("robot_radius", 0.0) or 0.0)
    local_body_radius = max(
        _inscribed_radius(local_footprint) + local_padding,
        local_robot_radius + local_padding,
    )

    global_padding = float(global_params.get("footprint_padding", 0.0) or 0.0)
    global_robot_radius = float(global_params.get("robot_radius", 0.0) or 0.0)
    global_body_radius = global_robot_radius + global_padding

    local_inflation = float(
        _deep_get(local_params, ["inflation_layer", "inflation_radius"], 0.0) or 0.0
    )
    global_inflation = float(
        _deep_get(global_params, ["inflation_layer", "inflation_radius"], 0.0) or 0.0
    )

    return {
        "allow_unknown": bool(planner_params.get("allow_unknown", True)),
        "clearance_radius_m": max(local_body_radius, global_body_radius),
        "local_inflation_radius_m": local_inflation,
        "global_inflation_radius_m": global_inflation,
    }


def profile_condition(profile_config: LaunchConfiguration, allowed_profiles: list[str]) -> IfCondition:
    expression_parts: list[str] = []
    for index, profile_name in enumerate(allowed_profiles):
        if index:
            expression_parts.append(" or ")
        expression_parts.extend(["'", profile_config, "' == '", profile_name, "'"])
    return IfCondition(PythonExpression(expression_parts))


def go2_description_paths() -> dict[str, str]:
    pkg_go2_desc = get_package_share_path("go2_description")
    return {
        "pkg_go2_desc": str(pkg_go2_desc),
        "urdf_path": os.path.join(pkg_go2_desc, "urdf", "go2.urdf.xacro"),
        "rviz_cfg": os.path.join(pkg_go2_desc, "config", "nav_nvblox_config.rviz"),
        "nav2_cfg": os.path.join(pkg_go2_desc, "config", "nav2_mppi_controller.yaml"),
        "ekf_cfg": os.path.join(pkg_go2_desc, "config", "local_odom_ekf.yaml"),
        "slam_toolbox_config": os.path.join(
            get_package_share_directory("go2_description"),
            "config",
            "mapper_params_online_async.yaml",
        ),
        "explore_cfg": os.path.join(
            get_package_share_directory("explore_lite"),
            "config",
            "params.yaml",
        ),
    }
