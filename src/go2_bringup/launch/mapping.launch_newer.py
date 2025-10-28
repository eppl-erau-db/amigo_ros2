#!/usr/bin/env python3
"""
Go2 • UTLiDAR 3-D • ZED-X Mini • RTAB-Map SLAM  (ROS 2 Humble)
----------------------------------------------------------------
 * LiDAR odometry  -> icp_odometry       (radar → icp_odom TF)
 * Global graph    -> rtabmap_slam/rtabmap
 * 2-D grid for Nav2 comes from RTAB-Map’s /proj_map  (relayed to /map)
"""

import os, math
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory, get_package_share_path

# ───────────────────────────── generate ────────────────────────────────
def generate_launch_description():

    # ─── 1.  Common launch args ────────────────────────────────────────
    declare_sim_time = DeclareLaunchArgument(
        name="use_sim_time", default_value="false",
        description="Use simulated clock if true")

    use_sim_time = LaunchConfiguration("use_sim_time")

    # ─── 2.  Package paths / configs ───────────────────────────────────
    pkg_go2_desc = get_package_share_path("go2_description")
    urdf_path    = os.path.join(pkg_go2_desc, "urdf", "go2.urdf.xacro")
    rviz_cfg     = os.path.join(pkg_go2_desc, "config", "go2_urdf_config.rviz")
    nav2_cfg     = os.path.join(pkg_go2_desc, "config", "nav2_mppi_controller.yaml")
    ekf_cfg      = os.path.join(pkg_go2_desc, "config", "ekf.yaml")

    # ─── 3.  Robot description ────────────────────────────────────────
    robot_description = ParameterValue(
        Command([
            "xacro ", str(urdf_path),
            " camera_name:=zed",
            " camera_model:=zedxm",
            " use_zed_localization:=false"
        ]), value_type=str)

    robot_state_pub = Node(
        package="robot_state_publisher", executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description,
                     "use_sim_time": use_sim_time}])

    # ─── 4.  Go2 low-level stack ───────────────────────────────────────
    state_pub  = Node(package="go2_control", executable="go2_state",
                      name="go2_state",  output="screen")
    odom_node  = Node(package="go2_control", executable="odom_node",
                      name="odom_node",  output="screen")
    base_tf    = Node(package="go2_control", executable="base_to_base_tf",
                      name="base_to_base_tf", output="screen")
    go2_driver = Node(package="go2_driver", executable="go2_driver_node",
                      name="go2_driver_node", output="screen")

    ekf_node = Node(
        package="robot_localization", executable="ekf_node",
        name="ekf_filter_node", output="screen",
        parameters=[ekf_cfg, {"use_sim_time": use_sim_time}],
        remappings=[("/odometry/filtered", "/odom")])

    # ─── 5.  UTLiDAR publisher (already deskewed & RELIABLE) ───────────
    lidar_pub = Node(package="go2_control", executable="go2_lidar",
                     name="go2_lidar", output="screen")

    # ─── 6.  ZED-X Mini camera ─────────────────────────────────────────
    zed_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory("zed_wrapper"), "launch",
            "zed_camera.launch.py")),
        launch_arguments={
            "camera_name":  "zed",
            "camera_model": "zedxm",
            "grab_resolution": "SVGA",
            "publish_tf": "false",
            "publish_map_tf": "false",
        }.items())

    # ─── 7-A.  RGB-D sync (ZED) ────────────────────────────────────────
    rgbd_sync = Node(
        package="rtabmap_sync", executable="rgbd_sync", output="screen",
        name="rgbd_sync",
        parameters=[{"approx_sync": True, "qos": 1}],
        remappings=[
            ("rgb/image",       "/zed/zed_node/rgb/image_rect_color"),
            ("rgb/camera_info", "/zed/zed_node/rgb/camera_info"),
            ("depth/image",     "/zed/zed_node/depth/depth_registered")
        ])

    # ─── 7-B.  ICP LiDAR odometry  ─────────────────────────────────────
    voxel = "0.10"                       # 10 cm voxels (indoor)
    icp_odometry = Node(
        package="rtabmap_odom", executable="icp_odometry", output="screen",
        parameters=[{
            "use_sim_time":         use_sim_time,
            "frame_id":             "radar",
            "odom_frame_id":        "odom",
            "guess_frame_id":       "odom",
            "publish_tf": False,          # optional EKF hint
            "expected_update_rate": 15.0           # Hz
        }],
        arguments=[
            # ---- internal ICP params ----
            "Icp/VoxelSize",                 voxel,
            "Icp/PointToPlane","true",
            "Icp/Iterations","10",
            "Icp/MaxCorrespondenceDistance", str(float(voxel)*10.0),
            "Odom/ScanKeyFrameThr","0.4",
            "OdomF2M/ScanSubtractRadius",    voxel,
            "OdomF2M/MaxTranslation",        "0.40",
            "--ros-args"
        ],
        remappings=[
            ("scan_cloud", "/pointcloud"),
            ("imu",        "imu_not_used")   # replace with real IMU if desired
        ])

    # ─── 7-C.  RTAB-Map core ───────────────────────────────────────────
    rtabmap_node = Node(
        package="rtabmap_slam", executable="rtabmap", name="rtabmap",
        output="screen",
        parameters=[{
            "frame_id":          "radar",
            "map_frame_id":      "map",
            "odom_frame_id":     "odom",
            "subscribe_rgbd":    True,
            "subscribe_scan_cloud": True,
            "approx_sync":       True,
            "sync_queue_size":   30,
            "topic_queue_size":  30,
            "qos_scan_cloud":    1,
            "delete_db_on_start": True,
            "publish_tf":        True,
            "use_sim_time":      use_sim_time
        }],
        arguments=[
            # ---- grid map for Nav2 (2-D) ----
            "RGBD/CreateOccupancyGrid","true",
            "Grid/3D","false",
            "Grid/Sensor","0",
            "Grid/RangeMin","0.05",
            "Grid/RangeMax","30.0",
            "Grid/Resolution","0.05",
            "Grid/MaxObstacleHeight","0.55",
            "--ros-args"
        ],
        remappings=[
            ("scan_cloud", "/pointcloud"),
            ("odom",       "odom")
        ])

    rtabmap_viz = Node(
        package="rtabmap_viz", executable="rtabmap_viz", output="screen",
        parameters=[{'frame_id':'radar', 'use_sim_time': use_sim_time}],
        remappings=[('odom','icp_odom')])

    # ─── 8.  Relay /proj_map → /map for Nav2 static layer ──────────────
    map_relay = Node(package="topic_tools", executable="relay",
                     name="proj_map_relay", output="screen",
                     arguments=["/rtabmap/proj_map", "/map"])

    # ─── 9.  Nav2 bring-up (MPPI controller) ───────────────────────────
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory("nav2_bringup"), "launch",
            "navigation_launch.py")),
        launch_arguments={
            "params_file": nav2_cfg,
            "use_sim_time": use_sim_time,
            "localization": "false"     # RTAB-Map supplies the map
        }.items())

    # ─── 10.  Extras (pose logger, RViz) ───────────────────────────────
    log_pose_server = Node(
        package="go2_control", executable="log_pose_action_server",
        name="log_pose_action_server", output="screen",
        parameters=[{"save_path":"pose_log.json"}])

    rviz2 = Node(package="rviz2", executable="rviz2",
                 arguments=["-d", rviz_cfg])

    # ─── 11.  Assemble launch description ─────────────────────────────
    return LaunchDescription([
        declare_sim_time,

        #  ─ Sensors
        zed_launch,
        lidar_pub,

        #  ─ Core state estimation
        state_pub, go2_driver, base_tf,
        odom_node, ekf_node,

        #  ─ SLAM
        rgbd_sync,
        icp_odometry,
        rtabmap_node,
        map_relay,

        #  ─ Robot description
        robot_state_pub,

        #  ─ Navigation
        nav2_launch,

        #  ─ Tools / visualisation
        log_pose_server,
        rtabmap_viz,
        rviz2,
    ])


