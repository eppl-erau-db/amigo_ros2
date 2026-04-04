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
    "voice_authorized_transcript_topic",
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
    "voice_verifier_enable",
    "voice_verifier_audio_topic",
    "voice_verifier_model_name_or_path",
    "voice_verifier_reference_embedding_path",
    "voice_verifier_threshold",
    "voice_verifier_score_topic",
    "voice_verifier_authorized_topic",
    "voice_verifier_decision_ttl_s",
    "voice_verifier_debug",
    "voice_verifier_window_duration_s",
    "voice_verifier_eval_period_s",
    "voice_verifier_channel",
    "voice_verifier_channel_strategy",
    "voice_verifier_min_dbfs",
    "voice_command_window_s",
    "voice_attention_enable",
    "voice_attention_request_topic",
    "voice_attention_ready_topic",
    "voice_attention_motion_cmd_topic",
    "voice_attention_motion_reassert_topic",
    "voice_attention_motion_backend",
    "voice_attention_motion_network_interface",
    "voice_attention_motion_gait",
    "voice_attention_motion_command_timeout_s",
    "voice_attention_motion_gait_reassert_period_s",
    "voice_attention_doa_topic",
    "voice_attention_doa_ttl_s",
    "voice_attention_turn_tolerance_deg",
    "voice_attention_turn_timeout_s",
    "voice_attention_turn_kp",
    "voice_attention_max_turn_rate_radps",
    "voice_attention_visual_refine_enable",
    "voice_attention_visual_target_point_topic",
    "voice_attention_visual_target_visible_topic",
    "voice_attention_visual_target_status_topic",
    "voice_attention_visual_objects_topic",
    "voice_attention_visual_refine_timeout_s",
    "voice_attention_visual_target_ttl_s",
    "voice_attention_visual_center_tolerance_rad",
    "voice_attention_visual_turn_kp",
    "voice_attention_visual_max_turn_rate_radps",
    "voice_attention_pitch_rad",
    "voice_attention_pitch_hold_s",
    "voice_attention_return_to_neutral",
    "voice_attention_reassert_gait_after_pitch",
    "voice_attention_gait_reassert_settle_s",
    "voice_attention_debug",
    "voice_debug",
    "voice_command_debug",
    "voice_command_cooldown_s",
    "voice_command_mode",
    "voice_command_topic",
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


def build_argument_specs(launch_dir: str) -> dict[str, tuple[object, str]]:
    default_voice_audio_topic = "/sss"
    default_voice_channel = "0"
    default_voice_channel_strategy = "max_rms"

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
        "voice_control": (
            "false",
            "Enable voice command node and leak search action server",
        ),
        "voice_transcript_topic": (
            "/voice/transcript",
            "Transcript topic (std_msgs/String)",
        ),
        "voice_authorized_transcript_topic": (
            "/voice/authorized_transcript",
            "Transcript topic after speaker-identity gating",
        ),
        "voice_wake_phrase": ("hey amigo", "Wake phrase that arms the command parser"),
        "voice_shake_hand_phrase": (
            "hello amigo",
            "Phrase that triggers the Go2 hello/shake-hand sport action",
        ),
        "voice_search_phrase": (
            "look for a leak",
            "Phrase that triggers Search action",
        ),
        "voice_follow_phrase": (
            "follow me",
            "Phrase that enables person-follow mode",
        ),
        "voice_stop_follow_phrase": (
            "stop following",
            "Phrase that disables person-follow mode",
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
        "voice_stt_audio_topic": (
            default_voice_audio_topic,
            "AudioFrame topic used as STT input",
        ),
        "voice_stt_channel": (
            default_voice_channel,
            "Channel index from AudioFrame for STT",
        ),
        "voice_stt_channel_strategy": (
            default_voice_channel_strategy,
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
        "voice_verifier_enable": (
            "false",
            "Enable speaker verification and transcript identity gating",
        ),
        "voice_verifier_audio_topic": (
            [LaunchConfiguration("voice_stt_audio_topic")],
            "AudioFrame topic used as speaker verification input",
        ),
        "voice_verifier_model_name_or_path": (
            "english",
            "WeSpeaker model name or local path for speaker verification",
        ),
        "voice_verifier_reference_embedding_path": (
            "",
            "Path to enrolled speaker reference embedding (.pt or .npy)",
        ),
        "voice_verifier_threshold": (
            "0.68",
            "Minimum normalized speaker similarity required to authorize transcripts",
        ),
        "voice_verifier_score_topic": (
            "/voice/speaker_score",
            "Speaker verification score topic (std_msgs/Float32)",
        ),
        "voice_verifier_authorized_topic": (
            "/voice/speaker_authorized",
            "Speaker authorization topic (std_msgs/Bool)",
        ),
        "voice_verifier_decision_ttl_s": (
            "2.5",
            "How long the latest speaker authorization decision remains fresh for wake authorization",
        ),
        "voice_verifier_debug": (
            "false",
            "Enable verbose speaker verification and gate debug logs",
        ),
        "voice_verifier_window_duration_s": (
            "2.0",
            "Rolling audio window duration used for speaker verification",
        ),
        "voice_verifier_eval_period_s": (
            "0.5",
            "How often to evaluate speaker similarity from the rolling audio buffer",
        ),
        "voice_verifier_channel": (
            [LaunchConfiguration("voice_stt_channel")],
            "Channel index from AudioFrame for speaker verification",
        ),
        "voice_verifier_channel_strategy": (
            [LaunchConfiguration("voice_stt_channel_strategy")],
            'Speaker verification channel strategy: "fixed" or "max_rms"',
        ),
        "voice_verifier_min_dbfs": (
            "-50.0",
            "Minimum rolling-window level required before attempting speaker verification",
        ),
        "voice_command_window_s": (
            "2.5",
            "How long the single post-acknowledgment command window remains open",
        ),
        "voice_attention_enable": (
            "true",
            "Enable the voice attention acknowledgment sequence before opening the command window",
        ),
        "voice_attention_request_topic": (
            "/voice/attention_request",
            "Attention request topic published by the voice identity gate",
        ),
        "voice_attention_ready_topic": (
            "/voice/attention_ready",
            "Attention-ready topic published once attention pitch is engaged and the command window may open",
        ),
        "voice_attention_motion_cmd_topic": (
            "/voice/attention/cmd_vel",
            "Yaw-only attention motion topic consumed by the Unitree SDK attention bridge",
        ),
        "voice_attention_motion_reassert_topic": (
            "/voice/attention/reassert_gait",
            "Topic used to reassert the desired Unitree gait after the attention acknowledgment",
        ),
        "voice_attention_motion_backend": (
            [LaunchConfiguration("person_follow_motion_backend")],
            "Unitree SDK backend used by the attention motion bridge",
        ),
        "voice_attention_motion_network_interface": (
            [LaunchConfiguration("person_follow_unitree_network_interface")],
            "Optional network interface passed to the attention motion bridge",
        ),
        "voice_attention_motion_gait": (
            [LaunchConfiguration("startup_motion_gait")],
            "Desired Unitree gait to reassert around attention turning",
        ),
        "voice_attention_motion_command_timeout_s": (
            "0.35",
            "How long the attention motion bridge waits before sending a stop and disabling the backend",
        ),
        "voice_attention_motion_gait_reassert_period_s": (
            "0.5",
            "How often the attention motion bridge may reassert the desired gait while turning",
        ),
        "voice_attention_doa_topic": (
            "/doa_angle",
            "DOA topic used for rough attention turning",
        ),
        "voice_attention_doa_ttl_s": (
            "2.5",
            "How long a DOA sample remains fresh for rough turning",
        ),
        "voice_attention_turn_tolerance_deg": (
            "15.0",
            "Rough-turn stop tolerance in degrees",
        ),
        "voice_attention_turn_timeout_s": (
            "1.5",
            "Timeout for the rough DOA turn stage",
        ),
        "voice_attention_turn_kp": (
            "0.8",
            "Proportional gain for the rough DOA turn stage",
        ),
        "voice_attention_max_turn_rate_radps": (
            "0.5",
            "Maximum yaw rate used during the rough DOA turn stage",
        ),
        "voice_attention_visual_refine_enable": (
            "true",
            "Enable visual yaw-centering refinement before the pitch acknowledgment",
        ),
        "voice_attention_visual_target_point_topic": (
            "/person_follow_vision_node/target_point",
            "Preferred visual target-point topic for attention refinement",
        ),
        "voice_attention_visual_target_visible_topic": (
            "/person_follow_vision_node/target_visible",
            "Preferred visual target-visible topic for attention refinement",
        ),
        "voice_attention_visual_target_status_topic": (
            "/person_follow_vision_node/status",
            "Preferred visual target-status topic for attention refinement diagnostics",
        ),
        "voice_attention_visual_objects_topic": (
            "/zed/zed_node/obj_det/objects",
            "Raw ZED objects topic used as a fallback when person-follow target outputs are unavailable",
        ),
        "voice_attention_visual_refine_timeout_s": (
            "2.0",
            "Timeout for the visual yaw-centering refinement stage",
        ),
        "voice_attention_visual_target_ttl_s": (
            "1.0",
            "How long a visual target sample remains fresh during refinement",
        ),
        "voice_attention_visual_center_tolerance_rad": (
            "0.15",
            "Yaw error tolerance for visual centering in radians",
        ),
        "voice_attention_visual_turn_kp": (
            "0.8",
            "Proportional gain for visual yaw-centering refinement",
        ),
        "voice_attention_visual_max_turn_rate_radps": (
            "0.35",
            "Maximum yaw rate used during visual yaw-centering refinement",
        ),
        "voice_attention_pitch_rad": (
            "-0.15",
            "Pitch acknowledgment magnitude in radians; negative is the default because this hardware responds inverted to positive pitch",
        ),
        "voice_attention_pitch_hold_s": (
            "0.6",
            "How long to hold the acknowledgment after the command is captured before releasing it and returning to neutral",
        ),
        "voice_attention_return_to_neutral": (
            "true",
            "Return to a neutral Euler pose after the pitch acknowledgment",
        ),
        "voice_attention_reassert_gait_after_pitch": (
            "true",
            "Reassert the desired Unitree gait after the pitch acknowledgment completes",
        ),
        "voice_attention_gait_reassert_settle_s": (
            "0.2",
            "How long the attention node waits after requesting gait reassertion following the pitch acknowledgment",
        ),
        "voice_attention_debug": (
            "false",
            "Enable verbose attention acknowledgment logs",
        ),
        "voice_debug": ("false", "Enable verbose voice pipeline debugging logs"),
        "voice_command_debug": (
            "false",
            "Enable voice command decision debug logs",
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
                default_value=default_value,
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
