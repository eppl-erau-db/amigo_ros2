#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_path, get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    # ─── 1.  Common launch args ────────────────────────────────────────
    pkg_go2_desc = get_package_share_path("go2_description")

    declare_sim_time = DeclareLaunchArgument(
        name="use_sim_time", default_value="false",
        description="Use simulated clock if true")

    use_sim_time = LaunchConfiguration("use_sim_time")

    map_file = DeclareLaunchArgument(
        name="map_file", default_value=os.path.join(pkg_go2_desc, "maps", "mylab.yaml"),
        description="Full path to the map file to load")
    
    map_file = LaunchConfiguration('map_file', default=os.path.join(pkg_go2_desc, "maps", "mylab.yaml"))

    # ─── 2.  Package paths / configs ───────────────────────────────────
    urdf_path = os.path.join(pkg_go2_desc, "urdf", "go2.urdf.xacro")
    rviz_cfg = os.path.join(pkg_go2_desc, "config", "nav_nvblox_config.rviz")
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

    declare_rviz_cmd = DeclareLaunchArgument('rviz', default_value='true', description='Whether to start RViz')
    declare_visualization_cmd = DeclareLaunchArgument('visualization', default_value='false', description='Enable or disable visualization.')
    declare_initial_pose_cmd = DeclareLaunchArgument('initial_pose', default_value='false', description='Enable or disable initial pose.')

    # ───── New args for toggles ─────────────────────────────────────────────────
    rtabmap_db = LaunchConfiguration('rtabmap_db', default='src/go2_description/maps/mylab.db')  # prebuilt map DB for localization
    declare_rtabmap_db_cmd = DeclareLaunchArgument('rtabmap_db', default_value='src/go2_description/maps/mylab.db', description='Path to RTAB-Map database to localize against')
  
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

    set_initial_pose = Node(
        package='go2_control',
        executable='initial_pose_set',
        name='initial_pose_set',
        output='log',
        condition=IfCondition(initial_pose)
    )

    # ─── 6‑A.  ZED‑X Mini camera ──────────────────────────────────────
    zed_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory("zed_wrapper"), "launch",
            "zed_camera.launch.py")),
        launch_arguments={
            "camera_name": "zed",
            "camera_model": "zedxm",
            # Tweaks for lower latency
            "grab_resolution": "SVGA",
            "frame_rate": "15",           # Hz
            "point_cloud_rate": "10",     # Hz
            "depth_mode": "NEURAL_LIGHT",
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
    icp_odometry = Node(
        package="rtabmap_odom", executable="icp_odometry", output="screen",
        parameters=[{
            "use_sim_time": use_sim_time,
            "frame_id": "velodyne",
            "odom_frame_id": "odom",
            "guess_frame_id": "base_link",
            "publish_tf": False,        # EKF publishes the global TF
            "expected_update_rate": 15.0,
            "scan_range_max": 30.0,
            "scan_range_min": 1.0,
            "scan_voxel_size": 0.05,
            "imu_topic": "/zed/zed_node/imu/data",
        }],
        arguments=[
            # ---- internal ICP params ----
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
            # 2-D grid with free space for Nav2
            #"Grid/Sensor", "0",
            "RGBD/CreateOccupancyGrid","true",
            "Grid/3D","true",

            # Ground extraction tuned for 0.64 m sensor height
            "Grid/NormalsSegmentation","true",
            "Grid/MaxGroundAngle","25.0",     # tolerate walking gait & slight slopes
            "Grid/MinGroundHeight","-1.2",    # meters in LiDAR frame (covers floor at ~-0.64 m)
            "Grid/MaxGroundHeight","0.3",

            # Range gating (indoor)
            "Grid/RangeMin","1.0",
            "Grid/RangeMax","30.0",

            # Resolution & obstacle limits
            "Grid/Resolution","0.05",
            "Grid/MaxObstacleHeight","1.2",

            # Conservative occupancy tuning (keeps thin walls)
            "Grid/OccupiedK","2.0",
            "Grid/ProbHit","0.9",
            "Grid/ProbOccupiedThr","0.55",
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
                     name="grid_map_relay", output="screen",
                     arguments=["/rtabmap/grid_map", "/map"])

    # ───── Nav2 bringup (kept; use AMCL but don’t broadcast TF) ─────────────────
    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_path('nav2_bringup'), 'launch', 'bringup_launch.py')]),
        launch_arguments={
            'params_file': nav2_cfg,
            'use_sim_time': use_sim_time,
            'map': map_file,   # still load YAML for the static layer
        }.items(),
    )
    rviz2 = Node(package="rviz2", executable="rviz2",
                 arguments=["-d", rviz_cfg])

    # ───── Assemble ─────────────────────────────────────────────────────────────
    return LaunchDescription([
        # args
        declare_sim_time,
        declare_rviz_cmd,
        declare_visualization_cmd,
        declare_initial_pose_cmd,
                #  ─ Sensors
        zed_launch,
        velodyne_driver,
        velodyne_deskew,
        lidar_pub,

        state_pub, go2_driver, base_tf,
        odom_node, ekf_node,

        #  ─ SLAM
        rgbd_sync,
        icp_odometry,
        rtabmap_node,
        map_relay,
        robot_state_pub,
        # nav2
        nav2_bringup,

        # viz / misc
        set_initial_pose,
        rtabmap_viz,
        rviz2,
    ])
