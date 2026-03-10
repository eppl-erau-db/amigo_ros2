#!/usr/bin/env python3
"""
Go2 • UTLiDAR 3-D • ZED-X Mini •
Nav2 (MPPI) — cleaned wiring and rates
"""

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import AnyLaunchDescriptionSource, PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from ament_index_python.packages import get_package_share_path, get_package_share_directory


def generate_launch_description():
    # ─── 1.  Common launch args ────────────────────────────────────────
    declare_sim_time = DeclareLaunchArgument(
        name="use_sim_time", default_value="false",
        description="Use simulated clock if true"
    )
    declare_odas_enable = DeclareLaunchArgument(
        name="odas_enable", default_value="true",
        description="Include and run odas_ros/odas.launch.xml"
    )
    declare_odas_configuration_path = DeclareLaunchArgument(
        name="odas_configuration_path",
        default_value=os.path.join(
            get_package_share_directory("odas_ros"),
            "config",
            "odas_jetson_respeaker_sep.cfg",
        ),
        description="Path to ODAS configuration file"
    )
    declare_odas_audio_queue_size = DeclareLaunchArgument(
        name="odas_audio_queue_size", default_value="1",
        description="ODAS audio queue size"
    )
    declare_odas_visualization = DeclareLaunchArgument(
        name="odas_visualization", default_value="false",
        description="Enable ODAS visualization node"
    )
    declare_odas_force_publish_tf = DeclareLaunchArgument(
        name="odas_force_publish_tf", default_value="false",
        description="Force ODAS static TF publication"
    )
    declare_odas_use_echo_cancellation = DeclareLaunchArgument(
        name="odas_use_echo_cancellation", default_value="false",
        description="Enable ODAS echo-cancelled audio path"
    )
    declare_odas_echo_cancelled_signal_topic = DeclareLaunchArgument(
        name="odas_echo_cancelled_signal_topic", default_value="ec_signal",
        description="Topic used as ODAS echo-cancelled signal input"
    )
    declare_odas_enable_leak_classifier = DeclareLaunchArgument(
        name="odas_enable_leak_classifier", default_value="true",
        description="Enable ODAS leak classifier node (/leak_detected, /doa_angle)"
    )
    declare_odas_leak_classifier_debug = DeclareLaunchArgument(
        name="odas_leak_classifier_debug", default_value="false",
        description="Enable debug logs in ODAS leak classifier"
    )
    declare_odas_doa_zero_offset_deg = DeclareLaunchArgument(
        name="odas_doa_zero_offset_deg", default_value="129.0",
        description="ODAS DoA zero-offset calibration (degrees)"
    )
    declare_odas_log_level = DeclareLaunchArgument(
        name="odas_log_level", default_value="warn",
        description="ODAS ROS log verbosity (debug, info, warn, error, fatal)"
    )
    declare_voice_control = DeclareLaunchArgument(
        name="voice_control", default_value="false",
        description="Enable voice command node and leak search action server"
    )
    declare_voice_transcript_topic = DeclareLaunchArgument(
        name="voice_transcript_topic", default_value="/voice/transcript",
        description="Transcript topic (std_msgs/String)"
    )
    declare_voice_wake_phrase = DeclareLaunchArgument(
        name="voice_wake_phrase", default_value="hey amigo",
        description="Wake phrase that arms the command parser"
    )
    declare_voice_search_phrase = DeclareLaunchArgument(
        name="voice_search_phrase", default_value="look for a leak",
        description="Phrase that triggers Search action (used in search mode)"
    )
    declare_voice_stand_up_phrase = DeclareLaunchArgument(
        name="voice_stand_up_phrase", default_value="stand up",
        description="Phrase that triggers StandUp sport SDK command (sport_test mode)"
    )
    declare_voice_lay_down_phrase = DeclareLaunchArgument(
        name="voice_lay_down_phrase", default_value="lay down",
        description="Phrase that triggers StandDown sport SDK command (sport_test mode)"
    )
    declare_voice_stt_enable = DeclareLaunchArgument(
        name="voice_stt_enable", default_value="true",
        description="Enable Vosk STT bridge node (AudioFrame -> /voice/transcript)"
    )
    declare_voice_stt_model_path = DeclareLaunchArgument(
        name="voice_stt_model_path", default_value="",
        description="Path to local Vosk model directory"
    )
    declare_voice_stt_audio_topic = DeclareLaunchArgument(
        name="voice_stt_audio_topic", default_value="/sss",
        description="AudioFrame topic used as STT input"
    )
    declare_voice_stt_channel = DeclareLaunchArgument(
        name="voice_stt_channel", default_value="0",
        description="Channel index from AudioFrame for STT"
    )
    declare_voice_stt_channel_strategy = DeclareLaunchArgument(
        name="voice_stt_channel_strategy", default_value="fixed",
        description='STT channel strategy: "fixed" or "max_rms"'
    )
    declare_voice_stt_publish_partial = DeclareLaunchArgument(
        name="voice_stt_publish_partial", default_value="false",
        description="Publish partial STT hypotheses to /voice/partial"
    )
    declare_voice_stt_debug_audio = DeclareLaunchArgument(
        name="voice_stt_debug_audio", default_value="false",
        description="Enable periodic STT audio level/channel debug logs"
    )
    declare_voice_stt_max_alternatives = DeclareLaunchArgument(
        name="voice_stt_max_alternatives", default_value="0",
        description="Vosk max alternatives per final result (0 disables)"
    )
    declare_voice_debug = DeclareLaunchArgument(
        name="voice_debug", default_value="false",
        description="Enable verbose voice pipeline debugging logs"
    )
    declare_voice_command_debug = DeclareLaunchArgument(
        name="voice_command_debug", default_value="false",
        description="Enable voice command decision debug logs"
    )
    declare_voice_command_cooldown_s = DeclareLaunchArgument(
        name="voice_command_cooldown_s", default_value="12.0",
        description="Cooldown between accepted voice commands"
    )
    declare_voice_command_mode = DeclareLaunchArgument(
        name="voice_command_mode", default_value="sport_test",
        description="Voice command behavior mode: search or sport_test"
    )
    use_sim_time = LaunchConfiguration("use_sim_time")
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
    voice_control = LaunchConfiguration("voice_control")
    voice_transcript_topic = LaunchConfiguration("voice_transcript_topic")
    voice_wake_phrase = LaunchConfiguration("voice_wake_phrase")
    voice_search_phrase = LaunchConfiguration("voice_search_phrase")
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
    voice_command_cooldown_s = LaunchConfiguration("voice_command_cooldown_s")
    voice_command_mode = LaunchConfiguration("voice_command_mode")

    # ─── 2.  Package paths / configs ───────────────────────────────────
    pkg_go2_desc = get_package_share_path("go2_description")
    urdf_path    = os.path.join(pkg_go2_desc, "urdf", "go2.urdf.xacro")
    rviz_cfg     = os.path.join(pkg_go2_desc, "config", "nav_nvblox_config.rviz")
    nav2_cfg     = os.path.join(pkg_go2_desc, "config", "nav2_mppi_controller.yaml")
    ekf_cfg      = os.path.join(pkg_go2_desc, "config", "local_odom_ekf.yaml")

    # ─── 3.  Robot description ────────────────────────────────────────
    robot_description = ParameterValue(
        Command([
            "xacro ", str(urdf_path),
            " camera_name:=zed",
            " camera_model:=zedxm",
            " use_zed_localization:=false"
        ]),
        value_type=str
    )

    robot_state_pub = Node(
        package="robot_state_publisher", 
        executable="robot_state_publisher",
        parameters=[{
            "robot_description": robot_description,
            "use_sim_time": use_sim_time
        }]
    )
    
    wit_imu_pub = Node(
        package="wit_ros2_imu",
        executable="wit_ros2_imu",
        name="imu_driver_node",
        output="screen",
        parameters=[{"use_sim_time": use_sim_time}],
        remappings=[("imu/data_raw", "imu/data")]
    )

    # ─── 4.  Go2 low-level stack ───────────────────────────────────────
    state_pub = Node(
        package="go2_control", 
        executable="go2_state",
        name="go2_state", 
        output="screen"
    )
    odom_node = Node(
        package="go2_control", 
        executable="odom_node",
        name="odom_node", 
        output="screen"
    )
    base_tf = Node(
        package="go2_control", 
        executable="base_to_base_tf",
        name="base_to_base_tf", 
        output="screen"
    )
    
    go2_driver = Node(
        package="go2_driver", 
        executable="go2_driver_node",
        name="go2_driver_node", 
        output="screen"
    )
    
    ekf_node = Node(
        package="robot_localization",
        executable="ekf_node",
        name="ekf_filter_node",
        output="screen",
        parameters=[ekf_cfg, {"use_sim_time": use_sim_time}],
        remappings=[("odometry/filtered", "odometry/filtered")],
    )

    # ─── 5.  UTLiDAR publisher ────────────────────────────────────────
    lidar_pub = Node(
        package="go2_control", 
        executable="go2_lidar",
        name="go2_lidar", 
        output="screen"
    )

    # ─── 6-A.  ZED-X Mini camera (let YAMLs own FPS/resolution) ───────
    zed_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory("zed_wrapper"), "launch",
            "zed_camera.launch.py")),
        launch_arguments={
            "camera_name": "zed",
            "camera_model": "zedxm",
            "publish_tf": "false",
            "publish_map_tf": "false",
            "publish_imu_tf": "false"
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
        remappings=[
                ('/laserscan', '/scan')
        ],
    )

    slam_toolbox_config = os.path.join(
        get_package_share_directory('go2_description'),
        'config',
        'mapper_params_online_async.yaml'
    )

    slam_toolbox = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[slam_toolbox_config],
        remappings=[
            ('pose', '/slam_toolbox_pose')
        ]
    )

    # ─── 9.  Nav2 bring-up (MPPI controller) ──────────────────────────
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory("nav2_bringup"), "launch",
            "navigation_launch.py")),
        launch_arguments={
            "params_file": nav2_cfg,
            "use_sim_time": use_sim_time,
            "localization": "false"
        }.items()
    )

    odas_launch = IncludeLaunchDescription(
        AnyLaunchDescriptionSource(os.path.join(
            get_package_share_directory("odas_ros"), "launch", "odas.launch.xml"
        )),
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

    # ─── 10. Extras (pose logger, RViz) ───────────────────────────────
    log_pose_server = Node(
        package="go2_control", executable="log_pose_action_server",
        name="log_pose_action_server", output="screen",
        parameters=[{"save_path": "pose_log.json"}]
    )

    search_action_server = Node(
        package="go2_control",
        executable="search_action_server",
        name="leak_search_server",
        output="screen",
        parameters=[{"use_sim_time": use_sim_time}],
        condition=IfCondition(
            PythonExpression([
                "'", voice_control, "' == 'true' and '", voice_command_mode, "' == 'search'"
            ])
        ),
    )

    voice_stt_vosk_node = Node(
        package="go2_control",
        executable="voice_stt_vosk_node",
        name="voice_stt_vosk_node",
        output="screen",
        parameters=[{
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
            "grammar_phrases": [
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
                "stand up",
                "lay down",
                "lie down",
                "look for a leak",
            ],
        }],
        condition=IfCondition(
            PythonExpression([
                "'", voice_control, "' == 'true' and '", voice_stt_enable, "' == 'true'"
            ])
        ),
    )

    voice_command_node = Node(
        package="go2_control",
        executable="voice_command_node",
        name="voice_command_node",
        output="screen",
        parameters=[{
            "use_sim_time": use_sim_time,
            "transcript_topic": voice_transcript_topic,
            "wake_phrase": voice_wake_phrase,
            "wake_phrases": ["amigo"],
            "search_phrase": voice_search_phrase,
            "stand_up_phrase": voice_stand_up_phrase,
            "lay_down_phrase": voice_lay_down_phrase,
            "lay_down_phrases": ["lie down", "down"],
            "stand_up_phrases": ["get up"],
            "command_mode": voice_command_mode,
            "search_action_name": "search",
            "require_wake_phrase": True,
            "command_cooldown_s": voice_command_cooldown_s,
            "log_transcripts": voice_debug,
            "debug_decisions": voice_command_debug,
        }],
        condition=IfCondition(voice_control),
    )

    rviz2 = Node(package="rviz2", executable="rviz2",
                 arguments=["-d", rviz_cfg])

    # ─── 11. Assemble ─────────────────────────────────────────────────
    return LaunchDescription([
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
        declare_voice_control,
        declare_voice_transcript_topic,
        declare_voice_wake_phrase,
        declare_voice_search_phrase,
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
        robot_state_pub,
        base_tf,
        go2_driver,
        state_pub,
        # wit_imu_pub,
        odom_node, 
        ekf_node,   
        zed_launch,
        lidar_node,
        lidar_pub,
        slam_toolbox,
        nav2_launch,
        odas_launch,
        log_pose_server,
        search_action_server,
        voice_stt_vosk_node,
        voice_command_node,
        rviz2,
    ])
