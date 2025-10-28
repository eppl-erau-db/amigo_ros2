#!/usr/bin/env python3
"""
Go2 • UTLiDAR 3‑D • ZED‑X Mini • RTAB‑Map SLAM  (ROS 2 Humble)
----------------------------------------------------------------
 * LiDAR odometry   -> icp_odometry        (velodyne → icp_odom TF)
 * Global graph     -> rtabmap_slam/rtabmap
 * 2‑D grid for Nav2 comes from RTAB‑Map’s /proj_map  (relayed to /map)

 Tweaks applied after field testing (2025‑07‑20):
 ───────────────────────────────────────────────────────────────
 1. Static TF  odom → velodyne  so ICP can seed from TF again.
 2. ICP tuned for indoor VLP‑16:
      • Voxel = 0.05 m   • MaxCorrDist = 0.4 m   • PointToPlaneK = 10
 3. rgbd_sync allows ±50 ms skew.
 4. ZED‑X reduced to 720p @ 15 Hz, point‑cloud 10 Hz, depth mode ULTRA.
 5. Occupancy‑grid capped at 15 m range and 1.2 m obstacle‑height.
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
    """Generate the full launch description."""

    # ─── 1.  Common launch args ────────────────────────────────────────
    declare_sim_time = DeclareLaunchArgument(
        name="use_sim_time", default_value="false",
        description="Use simulated clock if true")

    use_sim_time = LaunchConfiguration("use_sim_time")

    # ─── 2.  Package paths / configs ───────────────────────────────────
    pkg_go2_desc = get_package_share_path("go2_description")
    urdf_path = os.path.join(pkg_go2_desc, "urdf", "go2.urdf.xacro")
    rviz_cfg = os.path.join(pkg_go2_desc, "config", "go2_urdf_config.rviz")
    nav2_cfg = os.path.join(pkg_go2_desc, "config", "nav2_mppi_controller.yaml")
    ekf_cfg = os.path.join(pkg_go2_desc, "config", "ekf.yaml")

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

    # ─── 4.  Go2 low‑level stack ───────────────────────────────────────
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
        remappings=[("/odometry/filtered", "/odom")])

    # ─── 5.  UTLiDAR publisher ────────────────────────────────────────
    lidar_pub = Node(package="go2_control", executable="go2_lidar",
                     name="go2_lidar", output="screen")

    # ─── 6‑A.  ZED‑X Mini camera ──────────────────────────────────────
    zed_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory("zed_wrapper"), "launch",
            "zed_camera.launch.py")),
        launch_arguments={
            "camera_name": "zed",
            "camera_model": "zedxm",
            # Tweaks for lower latency
            "grab_resolution": "HD720",
            "frame_rate": "15",           # Hz
            "point_cloud_rate": "10",     # Hz
            "depth_mode": "ULTRA",
            "publish_tf": "false",
            "publish_map_tf": "false",
            "publish_imu_tf": "false",
            "imu_fusion": "true",
            "sensors_fusion": "true",
        }.items())

    # ─── 6‑B.  Velodyne VLP‑16 ─────────────────────────────────────────
    velodyne_driver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory("velodyne_driver"),
                         "launch",
                         "velodyne_driver_node-VLP16-launch.py")]),)

    velodyne_deskew = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory("velodyne_pointcloud"),
                         "launch",
                         "velodyne_transform_node-VLP16-launch.py")]),
        launch_arguments={
            "fixed_frame": "odom"  # deskew against odom→base_link TF
        }.items())

    # ─── 6‑C.  Static TF  odom → velodyne  (for ICP guess) ────────────
    static_tf_velodyne = Node(
        package="tf2_ros", executable="static_transform_publisher",
        name="odom_to_velodyne_tf",
        arguments=["0", "0", "0", "0", "0", "0", "odom", "velodyne"],
        output="log")

    # ─── 7‑A.  RGB‑D sync (ZED) ───────────────────────────────────────
    rgbd_sync = Node(
        package="rtabmap_sync", executable="rgbd_sync", output="screen",
        name="rgbd_sync",
        parameters=[{"approx_sync": True,
                     "approx_sync_max_interval": 0.05,   # 50 ms
                     "qos": 1}],
        remappings=[
            ("rgb/image", "/zed/zed_node/rgb/image_rect_color"),
            ("rgb/camera_info", "/zed/zed_node/rgb/camera_info"),
            ("depth/image", "/zed/zed_node/depth/depth_registered")
        ])

    # ─── 7‑B.  ICP LiDAR odometry  ────────────────────────────────────
    voxel = "0.05"  # 5 cm voxels (sharper indoor maps)
    icp_odometry = Node(
        package="rtabmap_odom", executable="icp_odometry", output="screen",
        parameters=[{
            "use_sim_time": use_sim_time,
            "frame_id": "velodyne",
            "odom_frame_id": "odom",
            "guess_frame_id": "odom",
            "publish_tf": False,        # EKF publishes the global TF
            "expected_update_rate": 15.0,
            "imu_topic": "/zed/zed_node/imu/data",
        }],
        arguments=[
            # ---- internal ICP params ----
            "Icp/Deskewing", "true",
            "Icp/VoxelSize", voxel,
            "Icp/PointToPlane", "true",
            "Icp/PointToPlaneK", "10",
            "Icp/Iterations", "10",
            "Icp/MaxCorrespondenceDistance", "0.4",
            "Odom/ScanKeyFrameThr", "0.4",
            "OdomF2M/ScanSubtractRadius", voxel,
            "OdomF2M/MaxTranslation", "0.40",
            "--ros-args"
        ],
        remappings=[
            ("scan_cloud", "/velodyne_points"),
        ])

    # ─── 7‑C.  RTAB‑Map core ──────────────────────────────────────────
    rtabmap_node = Node(
        package="rtabmap_slam", executable="rtabmap", name="rtabmap",
        output="screen",
        parameters=[{
            "frame_id": "velodyne",
            "map_frame_id": "map",
            "odom_frame_id": "odom",
            "subscribe_rgbd": True,
            "subscribe_scan_cloud": True,
            "approx_sync": True,
            "sync_queue_size": 30,
            "topic_queue_size": 30,
            "qos_scan_cloud": 1,
            "delete_db_on_start": True,
            "publish_tf": True,
            "use_sim_time": use_sim_time
        }],
        arguments=[
            # ---- grid map for Nav2 (2‑D) ----
            "RGBD/CreateOccupancyGrid", "true",
            "Grid/3D", "false",
            "Grid/Sensor", "1",
            "Grid/RangeMin", "0.05",
            "Grid/RangeMax", "15.0",
            "Grid/Resolution", "0.05",
            # --- added these from old copy
            "Grid/NormalsSegmentation",
            "false",
            "Grid/MinGroundHeight",
            "-0.15",
            "Grid/MaxGroundHeight",
            "0.15",
            "Grid/MaxGroundAngle",
            "30.0",
            # ------------------------------
            "Grid/MaxObstacleHeight", "1.2",
            # added these as well -------------------------------
            "Grid/OccupiedK",
            "1.0",  # need as few as 1 hit to count as occupied
            "Grid/ProbHit",
            "0.9",  # stronger evidence per hit
            "Grid/ProbOccupiedThr",
            "0.55",  # lower threshold so sparse walls survive
            # -------------------------------------------------
            "--ros-args"
        ],
        remappings=[
            ("scan_cloud", "/velodyne_points"),
            ("odom", "odom")
        ])

    rtabmap_viz = Node(
        package="rtabmap_viz", executable="rtabmap_viz", output="screen",
        parameters=[{'frame_id': 'velodyne', 'use_sim_time': use_sim_time}],
        remappings=[('odom', 'icp_odom')])

    # ─── 8.  Relay /proj_map → /map  for Nav2 static layer ────────────
    map_relay = Node(package="topic_tools", executable="relay",
                     name="proj_map_relay", output="screen",
                     arguments=["/rtabmap/proj_map", "/map"])

    # ─── 9.  Nav2 bring‑up (MPPI controller) ──────────────────────────
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory("nav2_bringup"), "launch",
            "navigation_launch.py")),
        launch_arguments={
            "params_file": nav2_cfg,
            "use_sim_time": use_sim_time,
            "localization": "false"  # RTAB‑Map supplies the map
        }.items())

    # ─── 10. Extras (pose logger, RViz) ───────────────────────────────
    log_pose_server = Node(
        package="go2_control", executable="log_pose_action_server",
        name="log_pose_action_server", output="screen",
        parameters=[{"save_path": "pose_log.json"}])

    rviz2 = Node(package="rviz2", executable="rviz2",
                 arguments=["-d", rviz_cfg])

    # ─── 11. Assemble launch description ──────────────────────────────
    return LaunchDescription([
        declare_sim_time,

        #  ─ Sensors
        zed_launch,
        velodyne_driver,
        velodyne_deskew,
        lidar_pub,
        static_tf_velodyne,   # <-- new static TF publisher

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
