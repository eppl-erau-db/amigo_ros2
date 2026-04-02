#!/usr/bin/env python3
"""
Go2 mission bringup for mapping, exploration, and leak localization.
"""

import ast
import math
import os

import yaml
from ament_index_python.packages import get_package_share_directory, get_package_share_path
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import AnyLaunchDescriptionSource, PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def _load_yaml(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as handle:
        return yaml.safe_load(handle) or {}


def _deep_get(mapping: dict, keys: list[str], default=None):
    current = mapping
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def _parse_footprint(raw_value) -> list[tuple[float, float]]:
    if raw_value in (None, '', []):
        return []
    value = raw_value
    if isinstance(raw_value, str):
        value = ast.literal_eval(raw_value)
    points: list[tuple[float, float]] = []
    for item in value:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            points.append((float(item[0]), float(item[1])))
    return points


def _distance_point_to_segment(px: float, py: float, ax: float, ay: float, bx: float, by: float) -> float:
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
    radius = float('inf')
    wrapped = points[1:] + points[:1]
    for (ax, ay), (bx, by) in zip(points, wrapped):
        radius = min(radius, _distance_point_to_segment(0.0, 0.0, ax, ay, bx, by))
    return 0.0 if math.isinf(radius) else radius


def _derive_nav2_settings(nav2_cfg_path: str) -> dict:
    data = _load_yaml(nav2_cfg_path)
    planner_params = _deep_get(data, ['planner_server', 'ros__parameters', 'GridBased'], {}) or {}
    local_params = _deep_get(data, ['local_costmap', 'local_costmap', 'ros__parameters'], {}) or {}
    global_params = _deep_get(data, ['global_costmap', 'global_costmap', 'ros__parameters'], {}) or {}

    local_footprint = _parse_footprint(local_params.get('footprint'))
    local_padding = float(local_params.get('footprint_padding', 0.0) or 0.0)
    local_robot_radius = float(local_params.get('robot_radius', 0.0) or 0.0)
    local_body_radius = max(
        _inscribed_radius(local_footprint) + local_padding,
        local_robot_radius + local_padding,
    )

    global_padding = float(global_params.get('footprint_padding', 0.0) or 0.0)
    global_robot_radius = float(global_params.get('robot_radius', 0.0) or 0.0)
    global_body_radius = global_robot_radius + global_padding

    local_inflation = float(
        _deep_get(local_params, ['inflation_layer', 'inflation_radius'], 0.0) or 0.0
    )
    global_inflation = float(
        _deep_get(global_params, ['inflation_layer', 'inflation_radius'], 0.0) or 0.0
    )

    return {
        'allow_unknown': bool(planner_params.get('allow_unknown', True)),
        'clearance_radius_m': max(local_body_radius, global_body_radius),
        'local_inflation_radius_m': local_inflation,
        'global_inflation_radius_m': global_inflation,
    }


def _profile_condition(profile_config: LaunchConfiguration, allowed_profiles: list[str]) -> IfCondition:
    expression_parts: list[str] = []
    for index, profile_name in enumerate(allowed_profiles):
        if index:
            expression_parts.append(' or ')
        expression_parts.extend(["'", profile_config, "' == '", profile_name, "'"])
    return IfCondition(PythonExpression(expression_parts))


def generate_launch_description():
    default_vosk_model_path = os.environ.get('VOSK_MODEL_PATH', '').strip()
    if not default_vosk_model_path:
        launch_dir = os.path.dirname(__file__)
        candidate_roots = [
            os.path.abspath(os.path.join(launch_dir, '../../..')),
            os.path.abspath(os.path.join(launch_dir, '../../../../..')),
            os.getcwd(),
        ]
        for root in candidate_roots:
            bundled_vosk_model_path = os.path.join(
                root, 'models', 'vosk-model-small-en-us-0.15'
            )
            if os.path.isdir(bundled_vosk_model_path):
                default_vosk_model_path = bundled_vosk_model_path
                break

    declare_launch_profile = DeclareLaunchArgument(
        name='launch_profile',
        default_value='all',
        description='Launch profile: all, mission_base, or operator_tools',
    )
    declare_sim_time = DeclareLaunchArgument(
        name='use_sim_time', default_value='false',
        description='Use simulated clock if true'
    )
    declare_odas_enable = DeclareLaunchArgument(
        name='odas_enable', default_value='true',
        description='Include and run odas_ros/odas.launch.xml'
    )
    declare_odas_configuration_path = DeclareLaunchArgument(
        name='odas_configuration_path',
        default_value=os.path.join(
            get_package_share_directory('odas_ros'),
            'config',
            'odas_jetson_respeaker_sep.cfg',
        ),
        description='Path to ODAS configuration file'
    )
    declare_odas_audio_queue_size = DeclareLaunchArgument(
        name='odas_audio_queue_size', default_value='1',
        description='ODAS audio queue size'
    )
    declare_odas_visualization = DeclareLaunchArgument(
        name='odas_visualization', default_value='false',
        description='Enable ODAS visualization node'
    )
    declare_odas_force_publish_tf = DeclareLaunchArgument(
        name='odas_force_publish_tf', default_value='false',
        description='Force ODAS static TF publication'
    )
    declare_odas_use_echo_cancellation = DeclareLaunchArgument(
        name='odas_use_echo_cancellation', default_value='false',
        description='Enable ODAS echo-cancelled audio path'
    )
    declare_odas_echo_cancelled_signal_topic = DeclareLaunchArgument(
        name='odas_echo_cancelled_signal_topic', default_value='ec_signal',
        description='Topic used as ODAS echo-cancelled signal input'
    )
    declare_odas_enable_leak_classifier = DeclareLaunchArgument(
        name='odas_enable_leak_classifier', default_value='true',
        description='Enable ODAS leak classifier node (/leak_detected, /doa_angle)'
    )
    declare_odas_leak_classifier_debug = DeclareLaunchArgument(
        name='odas_leak_classifier_debug', default_value='false',
        description='Enable debug logs in ODAS leak classifier'
    )
    declare_odas_doa_zero_offset_deg = DeclareLaunchArgument(
        name='odas_doa_zero_offset_deg', default_value='129.0',
        description='ODAS DoA zero-offset calibration (degrees)'
    )
    declare_odas_log_level = DeclareLaunchArgument(
        name='odas_log_level', default_value='warn',
        description='ODAS ROS log verbosity (debug, info, warn, error, fatal)'
    )
    declare_sound_localizer_enable = DeclareLaunchArgument(
        name='sound_localizer_enable', default_value='true',
        description='Enable the map-frame sound localization node'
    )
    declare_search_debug = DeclareLaunchArgument(
        name='search_debug', default_value='false',
        description='Enable verbose leak-search diagnostics'
    )
    declare_search_allow_unknown = DeclareLaunchArgument(
        name='search_allow_unknown', default_value='true',
        description='Deprecated: leak localization now derives unknown-space policy from nav2_mppi_controller.yaml'
    )
    declare_voice_control = DeclareLaunchArgument(
        name='voice_control', default_value='false',
        description='Enable voice command node and leak search action server'
    )
    declare_voice_transcript_topic = DeclareLaunchArgument(
        name='voice_transcript_topic', default_value='/voice/transcript',
        description='Transcript topic (std_msgs/String)'
    )
    declare_voice_wake_phrase = DeclareLaunchArgument(
        name='voice_wake_phrase', default_value='hey amigo',
        description='Wake phrase that arms the command parser'
    )
    declare_voice_search_phrase = DeclareLaunchArgument(
        name='voice_search_phrase', default_value='look for a leak',
        description='Phrase that triggers Search action (used in search mode)'
    )
    declare_voice_follow_phrase = DeclareLaunchArgument(
        name='voice_follow_phrase', default_value='follow me',
        description='Phrase that enables person-follow perception mode'
    )
    declare_voice_stop_follow_phrase = DeclareLaunchArgument(
        name='voice_stop_follow_phrase', default_value='stop following',
        description='Phrase that disables person-follow perception mode'
    )
    declare_voice_stand_up_phrase = DeclareLaunchArgument(
        name='voice_stand_up_phrase', default_value='stand up',
        description='Phrase that triggers StandUp sport SDK command (sport_test mode)'
    )
    declare_voice_lay_down_phrase = DeclareLaunchArgument(
        name='voice_lay_down_phrase', default_value='lay down',
        description='Phrase that triggers StandDown sport SDK command (sport_test mode)'
    )
    declare_voice_stt_enable = DeclareLaunchArgument(
        name='voice_stt_enable', default_value='true',
        description='Enable Vosk STT bridge node (AudioFrame -> /voice/transcript)'
    )
    declare_voice_stt_model_path = DeclareLaunchArgument(
        name='voice_stt_model_path', default_value=default_vosk_model_path,
        description='Path to local Vosk model directory (auto-detected from repo when available)'
    )
    declare_voice_stt_audio_topic = DeclareLaunchArgument(
        name='voice_stt_audio_topic', default_value='/sss',
        description='AudioFrame topic used as STT input'
    )
    declare_voice_stt_channel = DeclareLaunchArgument(
        name='voice_stt_channel', default_value='0',
        description='Channel index from AudioFrame for STT'
    )
    declare_voice_stt_channel_strategy = DeclareLaunchArgument(
        name='voice_stt_channel_strategy', default_value='max_rms',
        description='STT channel strategy: "fixed" or "max_rms"'
    )
    declare_voice_stt_publish_partial = DeclareLaunchArgument(
        name='voice_stt_publish_partial', default_value='false',
        description='Publish partial STT hypotheses to /voice/partial'
    )
    declare_voice_stt_debug_audio = DeclareLaunchArgument(
        name='voice_stt_debug_audio', default_value='false',
        description='Enable periodic STT audio level/channel debug logs'
    )
    declare_voice_stt_max_alternatives = DeclareLaunchArgument(
        name='voice_stt_max_alternatives', default_value='3',
        description='Vosk max alternatives per final result (0 disables)'
    )
    declare_voice_debug = DeclareLaunchArgument(
        name='voice_debug', default_value='false',
        description='Enable verbose voice pipeline debugging logs'
    )
    declare_voice_command_debug = DeclareLaunchArgument(
        name='voice_command_debug', default_value='false',
        description='Enable voice command decision debug logs'
    )
    declare_voice_command_cooldown_s = DeclareLaunchArgument(
        name='voice_command_cooldown_s', default_value='12.0',
        description='Cooldown between accepted voice commands'
    )
    declare_voice_command_mode = DeclareLaunchArgument(
        name='voice_command_mode', default_value='all',
        description='Voice command behavior mode: search, sport_test, follow, or all'
    )
    declare_voice_command_topic = DeclareLaunchArgument(
        name='voice_command_topic', default_value='/voice/command',
        description='Topic where parsed voice commands are published'
    )
    declare_person_follow_enable = DeclareLaunchArgument(
        name='person_follow_enable', default_value='true',
        description='Enable the person-follow perception pipeline'
    )
    declare_person_follow_distance_m = DeclareLaunchArgument(
        name='person_follow_distance_m', default_value='0.75',
        description='Desired person-follow standoff distance in meters'
    )
    declare_person_follow_distance_band_m = DeclareLaunchArgument(
        name='person_follow_distance_band_m', default_value='0.10',
        description='Allowed standoff band around the desired follow distance in meters'
    )
    declare_person_follow_max_vx_mps = DeclareLaunchArgument(
        name='person_follow_max_vx_mps', default_value='0.60',
        description='Maximum forward follow speed in meters per second'
    )
    declare_person_follow_max_vy_mps = DeclareLaunchArgument(
        name='person_follow_max_vy_mps', default_value='0.30',
        description='Maximum lateral follow speed in meters per second'
    )
    declare_person_follow_max_wz_radps = DeclareLaunchArgument(
        name='person_follow_max_wz_radps', default_value='1.20',
        description='Maximum follow yaw rate in radians per second'
    )
    declare_person_follow_use_strafe = DeclareLaunchArgument(
        name='person_follow_use_strafe', default_value='false',
        description='Allow strafing in follow mode instead of rotate-first centering'
    )
    declare_person_follow_candidate_horizon_s = DeclareLaunchArgument(
        name='person_follow_candidate_horizon_s', default_value='0.80',
        description='Short-horizon safety simulation window for follow controller commands'
    )
    declare_person_follow_reacquire_timeout_s = DeclareLaunchArgument(
        name='person_follow_reacquire_timeout_s', default_value='1.50',
        description='How long to actively yaw-search after a target loss before holding position'
    )
    declare_person_follow_sit_on_loss_timeout_s = DeclareLaunchArgument(
        name='person_follow_sit_on_loss_timeout_s', default_value='3.00',
        description='How long to wait after sustained target loss before sending StandDown'
    )
    declare_person_follow_debug = DeclareLaunchArgument(
        name='person_follow_debug', default_value='false',
        description='Enable extra person-follow controller debug logging'
    )
    declare_zed_follow_params_path = DeclareLaunchArgument(
        name='zed_follow_params_path',
        default_value=os.path.join(
            get_package_share_directory('go2_bringup'),
            'config',
            'zed_follow_person.yaml',
        ),
        description='ROS params override YAML for the ZED follow-person object-detection pipeline'
    )

    launch_profile = LaunchConfiguration('launch_profile')
    use_sim_time = LaunchConfiguration('use_sim_time')
    odas_enable = LaunchConfiguration('odas_enable')
    odas_configuration_path = LaunchConfiguration('odas_configuration_path')
    odas_audio_queue_size = LaunchConfiguration('odas_audio_queue_size')
    odas_visualization = LaunchConfiguration('odas_visualization')
    odas_force_publish_tf = LaunchConfiguration('odas_force_publish_tf')
    odas_use_echo_cancellation = LaunchConfiguration('odas_use_echo_cancellation')
    odas_echo_cancelled_signal_topic = LaunchConfiguration('odas_echo_cancelled_signal_topic')
    odas_enable_leak_classifier = LaunchConfiguration('odas_enable_leak_classifier')
    odas_leak_classifier_debug = LaunchConfiguration('odas_leak_classifier_debug')
    odas_doa_zero_offset_deg = LaunchConfiguration('odas_doa_zero_offset_deg')
    odas_log_level = LaunchConfiguration('odas_log_level')
    sound_localizer_enable = LaunchConfiguration('sound_localizer_enable')
    search_debug = LaunchConfiguration('search_debug')
    voice_control = LaunchConfiguration('voice_control')
    voice_transcript_topic = LaunchConfiguration('voice_transcript_topic')
    voice_wake_phrase = LaunchConfiguration('voice_wake_phrase')
    voice_search_phrase = LaunchConfiguration('voice_search_phrase')
    voice_follow_phrase = LaunchConfiguration('voice_follow_phrase')
    voice_stop_follow_phrase = LaunchConfiguration('voice_stop_follow_phrase')
    voice_stand_up_phrase = LaunchConfiguration('voice_stand_up_phrase')
    voice_lay_down_phrase = LaunchConfiguration('voice_lay_down_phrase')
    voice_stt_enable = LaunchConfiguration('voice_stt_enable')
    voice_stt_model_path = LaunchConfiguration('voice_stt_model_path')
    voice_stt_audio_topic = LaunchConfiguration('voice_stt_audio_topic')
    voice_stt_channel = LaunchConfiguration('voice_stt_channel')
    voice_stt_channel_strategy = LaunchConfiguration('voice_stt_channel_strategy')
    voice_stt_publish_partial = LaunchConfiguration('voice_stt_publish_partial')
    voice_stt_debug_audio = LaunchConfiguration('voice_stt_debug_audio')
    voice_stt_max_alternatives = LaunchConfiguration('voice_stt_max_alternatives')
    voice_debug = LaunchConfiguration('voice_debug')
    voice_command_debug = LaunchConfiguration('voice_command_debug')
    voice_command_cooldown_s = LaunchConfiguration('voice_command_cooldown_s')
    voice_command_mode = LaunchConfiguration('voice_command_mode')
    voice_command_topic = LaunchConfiguration('voice_command_topic')
    person_follow_enable = LaunchConfiguration('person_follow_enable')
    person_follow_distance_m = LaunchConfiguration('person_follow_distance_m')
    person_follow_distance_band_m = LaunchConfiguration('person_follow_distance_band_m')
    person_follow_max_vx_mps = LaunchConfiguration('person_follow_max_vx_mps')
    person_follow_max_vy_mps = LaunchConfiguration('person_follow_max_vy_mps')
    person_follow_max_wz_radps = LaunchConfiguration('person_follow_max_wz_radps')
    person_follow_use_strafe = LaunchConfiguration('person_follow_use_strafe')
    person_follow_candidate_horizon_s = LaunchConfiguration('person_follow_candidate_horizon_s')
    person_follow_reacquire_timeout_s = LaunchConfiguration('person_follow_reacquire_timeout_s')
    person_follow_sit_on_loss_timeout_s = LaunchConfiguration('person_follow_sit_on_loss_timeout_s')
    person_follow_debug = LaunchConfiguration('person_follow_debug')
    zed_follow_params_path = LaunchConfiguration('zed_follow_params_path')

    pkg_go2_desc = get_package_share_path('go2_description')
    urdf_path = os.path.join(pkg_go2_desc, 'urdf', 'go2.urdf.xacro')
    rviz_cfg = os.path.join(pkg_go2_desc, 'config', 'nav_nvblox_config.rviz')
    nav2_cfg = os.path.join(pkg_go2_desc, 'config', 'nav2_mppi_controller.yaml')
    ekf_cfg = os.path.join(pkg_go2_desc, 'config', 'local_odom_ekf.yaml')
    slam_toolbox_config = os.path.join(
        get_package_share_directory('go2_description'),
        'config',
        'mapper_params_online_async.yaml'
    )
    explore_cfg = os.path.join(
        get_package_share_directory('explore_lite'), 'config', 'params.yaml'
    )
    nav2_settings = _derive_nav2_settings(nav2_cfg)

    robot_description = ParameterValue(
        Command([
            'xacro ', str(urdf_path),
            ' camera_name:=zed',
            ' camera_model:=zedxm',
            ' use_zed_localization:=false'
        ]),
        value_type=str
    )

    robot_state_pub = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': use_sim_time
        }]
    )

    state_pub = Node(
        package='go2_control',
        executable='go2_state',
        name='go2_state',
        output='screen'
    )
    odom_node = Node(
        package='go2_control',
        executable='odom_node',
        name='odom_node',
        output='screen'
    )
    base_tf = Node(
        package='go2_control',
        executable='base_to_base_tf',
        name='base_to_base_tf',
        output='screen'
    )
    go2_driver = Node(
        package='go2_driver',
        executable='go2_driver_node',
        name='go2_driver_node',
        output='screen'
    )
    ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[ekf_cfg, {'use_sim_time': use_sim_time}],
        remappings=[('odometry/filtered', 'odometry/filtered')],
    )
    lidar_pub = Node(
        package='go2_control',
        executable='go2_lidar',
        name='go2_lidar',
        output='screen'
    )
    zed_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('zed_wrapper'), 'launch', 'zed_camera.launch.py')),
        launch_arguments={
            'camera_name': 'zed',
            'camera_model': 'zedxm',
            'publish_tf': 'false',
            'publish_map_tf': 'false',
            'publish_imu_tf': 'false',
            'ros_params_override_path': zed_follow_params_path,
        }.items()
    )
    lidar_node = Node(
        name='sllidar_node',
        package='sllidar_ros2',
        executable='sllidar_node',
        output='screen',
        parameters=[{
            'channel_type': 'serial',
            'serial_port': '/dev/ttyUSB0',
            'serial_baudrate': 256000,
            'frame_id': 'laser',
            'inverted': False,
            'angle_compensate': True,
            'scan_mode': 'Sensitivity',
        }],
        remappings=[('/laserscan', '/scan')],
    )
    slam_toolbox = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[slam_toolbox_config],
        remappings=[('pose', '/slam_toolbox_pose')],
    )
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('nav2_bringup'), 'launch', 'navigation_launch.py')),
        launch_arguments={
            'params_file': nav2_cfg,
            'use_sim_time': use_sim_time,
            'localization': 'false'
        }.items()
    )
    explore_lite_node = Node(
        package='explore_lite',
        executable='explore',
        name='explore_node',
        output='screen',
        parameters=[
            explore_cfg,
            {
                'use_sim_time': use_sim_time,
                'start_paused': True,
                'return_to_init': False,
                'costmap_topic': 'map',
                'costmap_updates_topic': 'map_updates',
            },
        ],
    )
    odas_launch = IncludeLaunchDescription(
        AnyLaunchDescriptionSource(os.path.join(
            get_package_share_directory('odas_ros'), 'launch', 'odas.launch.xml'
        )),
        launch_arguments={
            'configuration_path': odas_configuration_path,
            'audio_queue_size': odas_audio_queue_size,
            'visualization': odas_visualization,
            'force_publish_tf': odas_force_publish_tf,
            'use_echo_cancellation': odas_use_echo_cancellation,
            'echo_cancelled_signal_topic': odas_echo_cancelled_signal_topic,
            'enable_leak_classifier': odas_enable_leak_classifier,
            'leak_classifier_debug': odas_leak_classifier_debug,
            'doa_zero_offset_deg': odas_doa_zero_offset_deg,
            'log_level': odas_log_level,
        }.items(),
        condition=IfCondition(odas_enable),
    )

    leak_stack_condition = IfCondition(
        PythonExpression([
            "'", sound_localizer_enable, "' == 'true' and '",
            odas_enable, "' == 'true' and '",
            odas_enable_leak_classifier, "' == 'true'"
        ])
    )

    explore_phase_server = Node(
        package='go2_control',
        executable='explore_until_detected_action_server',
        name='explore_until_detected_server',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        condition=leak_stack_condition,
    )
    localize_phase_server = Node(
        package='go2_control',
        executable='localize_detected_leak_action_server',
        name='localize_detected_leak_server',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'debug_search': search_debug,
            'allow_unknown': nav2_settings['allow_unknown'],
            'clearance_radius_m': nav2_settings['clearance_radius_m'],
            'local_inflation_radius_m': nav2_settings['local_inflation_radius_m'],
            'global_inflation_radius_m': nav2_settings['global_inflation_radius_m'],
        }],
        condition=leak_stack_condition,
    )
    search_action_server = Node(
        package='go2_control',
        executable='search_action_server',
        name='leak_search_server',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'debug_topic': '/voice/debug',
            'publish_debug_events': True,
            'explore_action_name': 'explore_until_detected',
            'localize_action_name': 'localize_detected_leak',
        }],
        condition=leak_stack_condition,
    )
    sound_localizer_node = Node(
        package='go2_control',
        executable='sound_localizer',
        name='sound_localizer',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'min_baseline_m': 0.10,
            'stable_min_baseline_m': 0.50,
            'stable_min_bearing_separation_deg': 10.0,
            'stable_required_consecutive_estimates': 3,
            'stable_centroid_radius_m': 0.20,
            'stable_max_doa_age_s': 1.0,
            'intersection_method': 'geometric',
            'use_absolute_x_positions': False,
            'publish_waypoints': False,
            'num_waypoints': 0,
            'enable_reasonableness_filter': False,
        }],
        condition=leak_stack_condition,
    )
    voice_stt_vosk_node = Node(
        package='go2_control',
        executable='voice_stt_vosk_node',
        name='voice_stt_vosk_node',
        output='screen',
        parameters=[{
            'audio_topic': voice_stt_audio_topic,
            'transcript_topic': voice_transcript_topic,
            'model_path': voice_stt_model_path,
            'channel_index': voice_stt_channel,
            'channel_strategy': voice_stt_channel_strategy,
            'sample_rate': 16000,
            'audio_format': 'signed_16',
            'publish_partial': voice_stt_publish_partial,
            'log_partial_hypotheses': voice_debug,
            'log_empty_results': voice_debug,
            'log_raw_results': voice_debug,
            'debug_audio_stats': voice_stt_debug_audio,
            'audio_stats_period_s': 1.0,
            'max_alternatives': voice_stt_max_alternatives,
            'log_word_details': voice_debug,
            'grammar_phrases': [
                'hey amigo',
                'amigo',
                'hey amigo stand up',
                'amigo stand up',
                'hey amigo lay down',
                'amigo lay down',
                'hey amigo can you stand up',
                'amigo can you stand up',
                'hey amigo can you get up',
                'amigo can you get up',
                'hey amigo can you lay down',
                'amigo can you lay down',
                'hey amigo can you lie down',
                'amigo can you lie down',
                'hey amigo can you look for a leak',
                'amigo can you look for a leak',
                'hey amigo follow me',
                'amigo follow me',
                'hey amigo can you follow me',
                'amigo can you follow me',
                'hey amigo track me',
                'amigo track me',
                'hey amigo stop following',
                'amigo stop following',
                'hey amigo stop follow me',
                'amigo stop follow me',
                'stand up',
                'lay down',
                'lie down',
                'follow me',
                'track me',
                'stop following',
                'stop follow me',
                'look for a leak',
            ],
        }],
        condition=IfCondition(
            PythonExpression([
                "'", voice_control, "' == 'true' and '", voice_stt_enable, "' == 'true'"
            ])
        ),
    )
    voice_command_node = Node(
        package='go2_control',
        executable='voice_command_node',
        name='voice_command_node',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'transcript_topic': voice_transcript_topic,
            'wake_phrase': voice_wake_phrase,
            'wake_phrases': ['amigo'],
            'search_phrase': voice_search_phrase,
            'follow_phrase': voice_follow_phrase,
            'follow_phrases': ['track me', 'come with me'],
            'stop_follow_phrase': voice_stop_follow_phrase,
            'stop_follow_phrases': ['stop follow me', 'cancel follow', 'stop tracking me'],
            'stand_up_phrase': voice_stand_up_phrase,
            'lay_down_phrase': voice_lay_down_phrase,
            'lay_down_phrases': ['lie down', 'down'],
            'stand_up_phrases': ['get up'],
            'command_mode': voice_command_mode,
            'command_topic': voice_command_topic,
            'search_action_name': 'search',
            'require_wake_phrase': True,
            'command_cooldown_s': voice_command_cooldown_s,
            'log_transcripts': voice_debug,
            'debug_decisions': voice_command_debug,
            'debug_topic': '/voice/debug',
            'publish_debug_topic': True,
        }],
        condition=IfCondition(voice_control),
    )
    person_follow_node = Node(
        package='go2_person_follow',
        executable='person_follow_vision_node',
        name='person_follow_vision_node',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'command_topic': voice_command_topic,
            'image_topic': '/zed/zed_node/rgb/image_rect_color',
            'objects_topic': '/zed/zed_node/obj_det/objects',
        }],
        condition=IfCondition(person_follow_enable),
    )
    person_follow_controller_node = Node(
        package='go2_control',
        executable='person_follow_controller_node',
        name='person_follow_controller_node',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'command_topic': voice_command_topic,
            'target_point_topic': '/person_follow_vision_node/target_point',
            'target_visible_topic': '/person_follow_vision_node/target_visible',
            'target_status_topic': '/person_follow_vision_node/status',
            'local_costmap_topic': '/local_costmap/costmap',
            'desired_distance_m': person_follow_distance_m,
            'distance_band_m': person_follow_distance_band_m,
            'max_forward_speed_mps': person_follow_max_vx_mps,
            'max_lateral_speed_mps': person_follow_max_vy_mps,
            'max_yaw_rate_radps': person_follow_max_wz_radps,
            'use_strafe': person_follow_use_strafe,
            'candidate_horizon_s': person_follow_candidate_horizon_s,
            'reacquire_timeout_s': person_follow_reacquire_timeout_s,
            'sit_on_loss_timeout_s': person_follow_sit_on_loss_timeout_s,
            'debug_enable': person_follow_debug,
        }],
        condition=IfCondition(person_follow_enable),
    )

    log_pose_server = Node(
        package='go2_control',
        executable='log_pose_action_server',
        name='log_pose_action_server',
        output='screen',
        parameters=[{'save_path': 'pose_log.json'}]
    )
    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_cfg],
    )

    mission_base_group = GroupAction(
        condition=_profile_condition(launch_profile, ['all', 'mission_base']),
        actions=[
            robot_state_pub,
            base_tf,
            go2_driver,
            state_pub,
            odom_node,
            ekf_node,
            zed_launch,
            lidar_node,
            lidar_pub,
            slam_toolbox,
            nav2_launch,
            explore_lite_node,
            odas_launch,
            sound_localizer_node,
            explore_phase_server,
            localize_phase_server,
            search_action_server,
            voice_stt_vosk_node,
            voice_command_node,
            person_follow_node,
            person_follow_controller_node,
        ],
    )
    operator_tools_group = GroupAction(
        condition=_profile_condition(launch_profile, ['all', 'operator_tools']),
        actions=[
            log_pose_server,
            rviz2,
        ],
    )

    return LaunchDescription([
        declare_launch_profile,
        declare_sim_time,
        declare_odas_enable,
        declare_odas_configuration_path,
        declare_odas_audio_queue_size,
        declare_odas_visualization,
        declare_odas_force_publish_tf,
        declare_odas_use_echo_cancellation,
        declare_odas_echo_cancelled_signal_topic,
        declare_odas_enable_leak_classifier,
        declare_odas_leak_classifier_debug,
        declare_odas_doa_zero_offset_deg,
        declare_odas_log_level,
        declare_sound_localizer_enable,
        declare_search_debug,
        declare_search_allow_unknown,
        declare_voice_control,
        declare_voice_transcript_topic,
        declare_voice_wake_phrase,
        declare_voice_search_phrase,
        declare_voice_follow_phrase,
        declare_voice_stop_follow_phrase,
        declare_voice_stand_up_phrase,
        declare_voice_lay_down_phrase,
        declare_voice_stt_enable,
        declare_voice_stt_model_path,
        declare_voice_stt_audio_topic,
        declare_voice_stt_channel,
        declare_voice_stt_channel_strategy,
        declare_voice_stt_publish_partial,
        declare_voice_stt_debug_audio,
        declare_voice_stt_max_alternatives,
        declare_voice_debug,
        declare_voice_command_debug,
        declare_voice_command_cooldown_s,
        declare_voice_command_mode,
        declare_voice_command_topic,
        declare_person_follow_enable,
        declare_person_follow_distance_m,
        declare_person_follow_distance_band_m,
        declare_person_follow_max_vx_mps,
        declare_person_follow_max_vy_mps,
        declare_person_follow_max_wz_radps,
        declare_person_follow_use_strafe,
        declare_person_follow_candidate_horizon_s,
        declare_person_follow_reacquire_timeout_s,
        declare_person_follow_sit_on_loss_timeout_s,
        declare_person_follow_debug,
        declare_zed_follow_params_path,
        mission_base_group,
        operator_tools_group,
    ])
