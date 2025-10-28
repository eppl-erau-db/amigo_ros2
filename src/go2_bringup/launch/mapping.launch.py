#!/usr/bin/env python3
"""
Go2 • UTLiDAR 3-D • ZED-X Mini • RTAB-Map SLAM  (ROS 2 Humble)
Nav2 (MPPI) — cleaned wiring and rates
"""

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration
from ament_index_python.packages import get_package_share_path, get_package_share_directory


def generate_launch_description():
    # ─── 1.  Common launch args ────────────────────────────────────────
    declare_sim_time = DeclareLaunchArgument(
        name="use_sim_time", default_value="false",
        description="Use simulated clock if true"
    )
    use_sim_time = LaunchConfiguration("use_sim_time")

    # ─── 2.  Package paths / configs ───────────────────────────────────
    pkg_go2_desc = get_package_share_path("go2_description")
    urdf_path    = os.path.join(pkg_go2_desc, "urdf", "go2.urdf.xacro")
    rviz_cfg     = os.path.join(pkg_go2_desc, "config", "nav_nvblox_config.rviz")
    nav2_cfg     = os.path.join(pkg_go2_desc, "config", "nav2_mppi_controller.yaml")
    ekf_cfg      = os.path.join(pkg_go2_desc, "config", "ekf.yaml")

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
        package="robot_state_publisher", executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description,
                     "use_sim_time": use_sim_time}]
    )

    # ─── 4.  Go2 low-level stack ───────────────────────────────────────
    state_pub = Node(package="go2_control", executable="go2_state",
                     name="go2_state", output="screen")
    odom_node = Node(package="go2_control", executable="odom_node",
                     name="odom_node", output="screen")
    base_tf = Node(package="go2_control", executable="base_to_base_tf",
                   name="base_to_base_tf", output="screen")
    go2_driver = Node(package="go2_driver", executable="go2_driver_node",
                      name="go2_driver_node", output="screen")

    ekf_node = Node(
        package="robot_localization", executable="ekf_node",
        name="ekf_filter_node", output="screen",
        parameters=[ekf_cfg, {"use_sim_time": use_sim_time}],
        remappings=[("/odometry/filtered", "/odom")]  # EKF publishes /odom
    )

    # ─── 5.  UTLiDAR publisher ────────────────────────────────────────
    lidar_pub = Node(package="go2_control", executable="go2_lidar",
                     name="go2_lidar", output="screen")

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

    # ─── 10. Extras (pose logger, RViz) ───────────────────────────────
    log_pose_server = Node(
        package="go2_control", executable="log_pose_action_server",
        name="log_pose_action_server", output="screen",
        parameters=[{"save_path": "pose_log.json"}]
    )

    rviz2 = Node(package="rviz2", executable="rviz2",
                 arguments=["-d", rviz_cfg])

    # ─── 11. Assemble ─────────────────────────────────────────────────
    return LaunchDescription([
        declare_sim_time,

        # Sensors
        zed_launch,
        lidar_node,
        lidar_pub,
        # z_band_filter,

        # State estimation
        state_pub, go2_driver, base_tf,
        odom_node, ekf_node,

        # SLAM + grid
        slam_toolbox,
  

        # Robot description
        robot_state_pub,

        # Nav2
        nav2_launch,

        # Tools / viz
        log_pose_server,

        rviz2,
    ])
