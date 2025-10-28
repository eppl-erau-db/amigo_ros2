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

    z_band_filter = Node(
        package="go2_driver", executable="z_band_filter_node",
        name="z_band_filter", output="screen",
        parameters=[{
            "input": "/velodyne_points",
            "output": "/velodyne_points_global_band",
            "target_frame": "odom",     # gravity-aligned frame
            "min_z": 1.3,
            "max_z": 20.0,
            "tf_timeout": 0.05,
            "use_latest_tf": True
        }]
    )

    # ─── 6-B.  Velodyne VLP-16 ─────────────────────────────────────────
    velodyne_driver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory("velodyne_driver"),
                         "launch", "velodyne_driver_node-VLP16-launch.py")])
    )

    velodyne_deskew = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory("velodyne_pointcloud"),
                         "launch", "velodyne_transform_node-VLP16-launch.py")]),
        launch_arguments={"fixed_frame": "odom"}.items()
    )

    # ─── 7-A.  RGB-D sync (ZED) ───────────────────────────────────────
    rgbd_sync = Node(
        package="rtabmap_sync", executable="rgbd_sync", output="screen",
        name="rgbd_sync",
        parameters=[{"approx_sync": True,
                     "approx_sync_max_interval": 0.05,
                     "qos": 1}],
        remappings=[
            ("rgb/image",        "/zed/zed_node/rgb/image_rect_color"),
            ("rgb/camera_info",  "/zed/zed_node/rgb/camera_info"),
            ("depth/image",      "/zed/zed_node/depth/depth_registered"),
            ("rgbd_image",       "/rgbd_image")
        ]
    )

    # ─── 7-B.  ICP LiDAR odometry  ────────────────────────────────────
    icp_odometry = Node(
        package="rtabmap_odom", executable="icp_odometry", output="screen",
        parameters=[{
            "use_sim_time": use_sim_time,
            "frame_id": "velodyne",
            "odom_frame_id": "odom",
            "guess_frame_id": "base_link",
            "publish_tf": False,               # TF comes from EKF
            "expected_update_rate": 0.0,       # disable strict rate gate
            "scan_range_max": 80.0,
            "scan_range_min": 0.05,
            "scan_voxel_size": 0.08,
            "imu_topic": "/zed/zed_node/imu/data",
        }],
        arguments=[
            "Icp/PointToPlane", "true",
            "Icp/PointToPlaneK", "8",
            "Icp/Iterations", "6",
            "Icp/MaxCorrespondenceDistance", "0.35",
            "Odom/ScanKeyFrameThr", "0.5",
            "OdomF2M/ScanSubtractRadius", "0.07",
            "OdomF2M/MaxTranslation", "0.40",
            "--ros-args"
        ],
        remappings=[
            ("scan_cloud", "/velodyne_points"),
            ("odom",       "/icp_odom"),
            ("odom_info",  "/icp_odom_info")
        ]
    )

    # ─── 7-C.  RTAB-Map core ──────────────────────────────────────────
    rtabmap_node = Node(
        package="rtabmap_slam", executable="rtabmap", name="rtabmap",
        output="screen",
        parameters=[{
            "frame_id": "base_footprint",          # OK since TF velodyne↔base_link exists
            "map_frame_id": "map",
            "odom_frame_id": "odom",
            "subscribe_rgbd": True,
            "subscribe_scan_cloud": True,
            "approx_sync": True,
            "sync_queue_size": 20,
            "topic_queue_size": 20,
            "qos_scan_cloud": 1,
            "delete_db_on_start": True,
            "publish_tf": True,
            "use_sim_time": use_sim_time
        }],
        arguments=[
            "Grid/Sensor", "2",
            "Grid/3D","false",
            "Grid/RayTracing", "true",
            "Grid/NormalsSegmentation","true",
            "Grid/FootprintLength","0.5",
            "Grid/FootprintWidth","0.1",
            "Grid/MaxGroundAngle","45.0",
            "Grid/MinGroundHeight","-0.05",
            "Grid/MaxGroundHeight","0.05",
            "Grid/MinClusterSize", "15",
            "Grid/ClusterRadius","0.15",
            "Grid/RangeMin","1.0",
            "Grid/RangeMax","30.0",
            "Grid/Resolution","0.05",
            "Grid/MaxObstacleHeight","5.0",
            "Grid/OccupiedK","2.0",
            "Grid/ProbHit","0.7",
            "Grid/ProbMiss","0.47",
            "GridGlobal/FootprintRadius","0.30",
            "Grid/ProbOccupiedThr","0.55",
            "Rtabmap/DetectionRate","5.0",
            "Kp/DetectorStrategy","6",
            "Kp/MaxFeatures","400",
            "RGBD/LinearUpdate","0.15",
            "RGBD/AngularUpdate","0.15",
            "RGBD/CreateOccupancyGrid","true",
            "--ros-args"
        ],
        remappings=[
            # ("scan_cloud", "/velodyne_points_global_band"),
            ("scan_cloud", "/velodyne_points"),
            ("odom",       "/odom")  # consume EKF-fused odom
        ]
    )

    rtabmap_viz = Node(
        package="rtabmap_viz", executable="rtabmap_viz", output="screen",
        parameters=[{'frame_id': 'base_footprint', 'use_sim_time': use_sim_time}],
        # Let it subscribe to /odom (EKF). Remove the bogus remap to /icp_odom.
        # remappings=[('odom', 'icp_odom')]
    )

    # ─── 8.  Relay /rtabmap/grid_map → /map  for Nav2 static layer ────
    map_relay = Node(package="topic_tools", executable="relay",
                     name="grid_map_relay", output="screen",
                     arguments=["/rtabmap/grid_map", "/map"])

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
        velodyne_driver,
        velodyne_deskew,
        lidar_pub,
        # z_band_filter,

        # State estimation
        state_pub, go2_driver, base_tf,
        odom_node, ekf_node,

        # SLAM + grid
        rgbd_sync,
        icp_odometry,
        rtabmap_node,
        map_relay,

        # Robot description
        robot_state_pub,

        # Nav2
        nav2_launch,

        # Tools / viz
        log_pose_server,
        rtabmap_viz,
        rviz2,
    ])
