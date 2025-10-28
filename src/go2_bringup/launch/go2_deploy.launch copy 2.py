#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Go2 • VLP-16 + ZED-X Mini • RTAB-Map SLAM + Nav2 (Navigation) — ROS 2 Humble
────────────────────────────────────────────────────────────────────────────
 * ZED camera + rgbd_sync (like mapping) + VLP-16 scans.
 * icp_odometry (LiDAR) with guess from base_link; RTAB-Map consumes ICP odom.
 * RTAB-Map publishes a 2-D occupancy grid; we relay **/rtabmap/grid_map → /map**.
 * Optional bridge: /cmd_vel_nav → /cmd_vel (harmless if source doesn't exist).

Args:
  use_sim_time [false]   – use /clock if sim
  imu_topic    [/zed/zed_node/imu/data]
"""

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration
from ament_index_python.packages import get_package_share_path, get_package_share_directory


def generate_launch_description():
    # ── Launch-time args ─────────────────────────────────────────────
    use_sim_time = LaunchConfiguration("use_sim_time")
    imu_topic    = LaunchConfiguration("imu_topic")
    declare_sim_time = DeclareLaunchArgument("use_sim_time", default_value="false")
    declare_imu_arg  = DeclareLaunchArgument("imu_topic", default_value="/zed/zed_node/imu/data")

    # ── Paths ────────────────────────────────────────────────────────
    pkg_desc = get_package_share_path("go2_description")
    urdf     = os.path.join(pkg_desc, "urdf", "go2.urdf.xacro")
    nav2_cfg = os.path.join(pkg_desc, "config", "nav2_mppi_controller.yaml")
    ekf_cfg  = os.path.join(pkg_desc, "config", "ekf.yaml")
    rviz_cfg = os.path.join(pkg_desc, "config", "go2_urdf_config.rviz")

    # ── Robot description ────────────────────────────────────────────
    robot_description = ParameterValue(Command([
        "xacro ", str(urdf),
        " camera_name:=zed",
        " camera_model:=zedxm",
        " use_zed_localization:=false"
    ]), value_type=str)

    robot_state_pub = Node(
        package="robot_state_publisher", executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description, "use_sim_time": use_sim_time}],
        output="screen")

    # ── Go2 base stack ───────────────────────────────────────────────
    state_pub = Node(package="go2_control", executable="go2_state",
                     name="go2_state", output="screen")
    odom_node = Node(package="go2_control", executable="odom_node",
                     name="odom_node", output="screen")
    base_tf   = Node(package="go2_control", executable="base_to_base_tf",
                     name="base_to_base_tf", output="screen")
    go2_driver = Node(package="go2_driver", executable="go2_driver_node",
                      name="go2_driver_node", output="screen")

    ekf_node = Node(
        package="robot_localization", executable="ekf_node",
        name="ekf_filter_node", output="screen",
        parameters=[ekf_cfg, {"use_sim_time": use_sim_time}],
        remappings=[("/odometry/filtered", "/odom")])

    # ── ZED-X Mini camera (like mapping) ─────────────────────────────
    zed_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory("zed_wrapper"), "launch", "zed_camera.launch.py")),
        launch_arguments={
            "camera_name": "zed",
            "camera_model": "zedxm",
            "grab_resolution": "HD720",
            "frame_rate": "15",
            "point_cloud_rate": "10",
            "depth_mode": "ULTRA",
            "publish_tf": "false",
            "publish_map_tf": "false",
            "publish_imu_tf": "false",
            "imu_fusion": "true",
            "sensors_fusion": "true",
        }.items())

    rgbd_sync = Node(
        package="rtabmap_sync", executable="rgbd_sync", output="screen",
        name="rgbd_sync",
        parameters=[{"approx_sync": True, "approx_sync_max_interval": 0.05, "qos": 1}],
        remappings=[
            ("rgb/image",       "/zed/zed_node/rgb/image_rect_color"),
            ("rgb/camera_info", "/zed/zed_node/rgb/camera_info"),
            ("depth/image",     "/zed/zed_node/depth/depth_registered"),
        ])

    # ── Velodyne VLP-16 ──────────────────────────────────────────────
    velodyne_driver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory("velodyne_driver"),
            "launch", "velodyne_driver_node-VLP16-launch.py")))
    velodyne_tf = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory("velodyne_pointcloud"),
            "launch", "velodyne_transform_node-VLP16-launch.py")),
        launch_arguments={"fixed_frame": "odom"}.items())

    # ── ICP LiDAR odometry ───────────────────────────────────────────
    icp_odometry = Node(
        package="rtabmap_odom", executable="icp_odometry", name="icp_odometry", output="screen",
        parameters=[{
            "use_sim_time": use_sim_time,
            "frame_id": "velodyne",
            "odom_frame_id": "odom",
            "guess_frame_id": "base_link",
            "publish_tf": False,
            "expected_update_rate": 15.0,
            "imu_topic": imu_topic,
            # prefilter for indoor nav
            "scan_range_min": 1.0,
            "scan_range_max": 30.0,
            "scan_voxel_size": 0.05,
            "subscribe_scan": False
        }],
        arguments=[
            "Icp/Deskewing", "true",
            "Icp/PointToPlane", "true",
            "Icp/PointToPlaneK", "10",
            "Icp/Iterations", "10",
            "Icp/MaxCorrespondenceDistance", "0.4",
            "Odom/ScanKeyFrameThr", "0.4",
            "OdomF2M/ScanSubtractRadius", "0.05",
            "OdomF2M/MaxTranslation", "0.40",
            "--ros-args"
        ],
        remappings=[("scan_cloud", "/velodyne_points")])

    # ── RTAB-Map (RGB-D + scan_cloud like mapping) ───────────────────
    rtabmap_node = Node(
        package="rtabmap_slam", executable="rtabmap", name="rtabmap", output="screen",
        parameters=[{
            "frame_id": "velodyne",
            "map_frame_id": "map",
            "odom_frame_id": "odom",

            # Subscriptions (mirror mapping setup)
            "subscribe_rgbd": True,
            "subscribe_scan_cloud": True,
            "subscribe_scan": False,
            "approx_sync": True,
            "sync_queue_size": 30,
            "topic_queue_size": 30,
            "qos_scan_cloud": 1,

            "delete_db_on_start": True,   # avoid old BoW dict mismatches
            "publish_tf": True,
            "use_sim_time": use_sim_time
        }],
        arguments=[
            # Occupancy grid for Nav2 (indoor)
            "RGBD/CreateOccupancyGrid","true",
            "Grid/3D","true",

            # Ground extraction tuned for LiDAR @0.64m
            "Grid/NormalsSegmentation","true",
            "Grid/MaxGroundAngle","25.0",
            "Grid/MinGroundHeight","-1.2",
            "Grid/MaxGroundHeight","0.3",

            # Range gating
            "Grid/RangeMin","1.0",
            "Grid/RangeMax","30.0",

            # Resolution & obstacle limits
            "Grid/Resolution","0.05",
            "Grid/MaxObstacleHeight","1.2",

            # Conservative occupancy tuning
            "Grid/OccupiedK","2.0",
            "Grid/ProbHit","0.9",
            "Grid/ProbOccupiedThr","0.55",

            # Ensure visual registration is enabled when RGB-D is used
            "Reg/Strategy","1",
            "--ros-args"
        ],
        remappings=[
            ("scan_cloud", "/velodyne_points"),
            ("odom",       "icp_odom")   # RTAB-Map consumes ICP odom
        ])

    # ── Map relay (grid with free space) ─────────────────────────────
    map_relay = Node(
        package="topic_tools", executable="relay",
        name="grid_map_relay", output="screen",
        arguments=["/rtabmap/grid_map", "/map"])

    # ── Nav2 bring-up ────────────────────────────────────────────────
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory("nav2_bringup"),
            "launch", "navigation_launch.py")),
        launch_arguments={
            "params_file": nav2_cfg,        # ensure floats for width/height/resolution
            "use_sim_time": use_sim_time,
            "map": "",
            "localization": "false",
            "autostart": "true"
        }.items())

    # Optional: bridge controller output if remapped to /cmd_vel_nav
    bridge_cmd = Node(
        package="topic_tools", executable="relay",
        name="bridge_cmd_vel_nav_to_cmd_vel", output="screen",
        arguments=["/cmd_vel_nav", "/cmd_vel"])

    # ── Viz / tools ──────────────────────────────────────────────────
    rtabmap_viz = Node(
        package="rtabmap_viz", executable="rtabmap_viz", output="screen",
        parameters=[{'frame_id': 'velodyne', 'use_sim_time': use_sim_time}],
        remappings=[('odom', 'icp_odom')])

    rviz2 = Node(package="rviz2", executable="rviz2",
                 arguments=["-d", rviz_cfg], output="screen")

    log_pose = Node(
        package="go2_control", executable="log_pose_action_server",
        name="log_pose_action_server", output="screen",
        parameters=[{"save_path": "pose_log.json"}])

    # (optional) your auxiliary publisher
    lidar_pub = Node(package="go2_control", executable="go2_lidar",
                     name="go2_lidar", output="screen")

    # ── Assemble ─────────────────────────────────────────────────────
    return LaunchDescription([
        declare_sim_time, declare_imu_arg,

        # Robot
        robot_state_pub, state_pub, go2_driver, base_tf, odom_node, ekf_node,

        # Sensors
        zed_launch, rgbd_sync,
        velodyne_driver, velodyne_tf,

        # SLAM
        icp_odometry, rtabmap_node, map_relay,

        # Nav2
        nav2_launch, bridge_cmd,

        # Tools / Viz
        rtabmap_viz, rviz2, log_pose, lidar_pub,
    ])
