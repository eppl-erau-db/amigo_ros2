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
    # ───── Existing args (unchanged) ─────────────────────────────────────────────
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    urdf_path = os.path.join(get_package_share_path('go2_description'), 'urdf', 'go2.urdf.xacro')  # ← do not change
    rviz_config_path = os.path.join(get_package_share_path('go2_description'), 'config', 'nav_nvblox_config.rviz')
    map_file = LaunchConfiguration('map_file', default=os.path.join(get_package_share_path('go2_description'), 'maps', 'mylab.yaml'))
    rviz = LaunchConfiguration('rviz', default='false')
    visualization = LaunchConfiguration('visualization', default='false')
    initial_pose = LaunchConfiguration('initial_pose', default='false')
    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    declare_map_file_cmd = DeclareLaunchArgument(
        'map_file',
        default_value=os.path.join(get_package_share_path('go2_description'), 'maps', 'mylab.yaml'),
        description='Full path to the map file to load'
    )
    declare_rviz_cmd = DeclareLaunchArgument('rviz', default_value='false', description='Whether to start RViz')
    declare_visualization_cmd = DeclareLaunchArgument('visualization', default_value='true', description='Enable or disable visualization.')
    declare_initial_pose_cmd = DeclareLaunchArgument('initial_pose', default_value='false', description='Enable or disable initial pose.')

    # ───── New args for toggles ─────────────────────────────────────────────────
    use_rgbd = LaunchConfiguration('use_rgbd', default='true')          # camera+LiDAR (true) vs LiDAR-only (false)
    use_velodyne = LaunchConfiguration('use_velodyne', default='true')  # VLP-16 driver/transform
    rtabmap_db = LaunchConfiguration('rtabmap_db', default='src/go2_description/maps/mylab.db')  # prebuilt map DB for localization
    start_teleop = LaunchConfiguration('start_teleop', default='false')           # avoid TTY errors when launching
    start_go2_2d_scan = LaunchConfiguration('start_go2_2d_scan', default='false') # prevents /scan conflicts

    declare_use_rgbd_cmd = DeclareLaunchArgument('use_rgbd', default_value='true', description='Use camera (RGB-D) with LiDAR for RTAB-Map localization')
    declare_use_velodyne_cmd = DeclareLaunchArgument('use_velodyne', default_value='true', description='Start Velodyne VLP-16 driver and transform nodes')
    declare_rtabmap_db_cmd = DeclareLaunchArgument('rtabmap_db', default_value='src/go2_description/maps/mylab.db', description='Path to RTAB-Map database to localize against')
    declare_start_teleop_cmd = DeclareLaunchArgument('start_teleop', default_value='false', description='Start keyboard teleop in this launch (not recommended)')
    declare_start_go2_2d_scan_cmd = DeclareLaunchArgument('start_go2_2d_scan', default_value='false', description='Start go2 2D scan publisher (avoid if using VLP-16 with ICP)')

    # ───── Core robot description / state (unchanged) ───────────────────────────
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description, 'use_sim_time': use_sim_time}],
        output='log'
    )

    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config_path],
        output='log',
        condition=IfCondition(rviz)
    )

    state_publisher_node = Node(
        package='go2_control',
        executable='go2_state',
        name='go2_state',
        output='log'
    )

    go2_driver_node = Node(
        package='go2_driver',
        executable='go2_driver_node',
        name='go2_driver_node',
        output='log'
    )

    base_footprint_to_base_link_tf = Node(
        package='go2_control',
        executable='base_to_base_tf',
        name='base_to_base_tf',
        output='log'
    )

    # (Keep existing EKF/odom nodes intact)
    nav2_config = os.path.join(get_package_share_path('go2_description'), 'config', 'nav2_mppi_controller.yaml')

    robot_localization_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='log',
        parameters=[os.path.join(get_package_share_path('go2_description'), 'config', 'ekf.yaml'),
                    {'use_sim_time': use_sim_time}],
        remappings=[('/odometry/filtered', '/odom'),
                    ('/set_pose', '/initialpose')]
    )

    odom_node = Node(
        package="go2_control",
        executable="odom_node",
        name='odom_node',
        output='screen'
    )

    set_initial_pose = Node(
        package='go2_control',
        executable='initial_pose_set',
        name='initial_pose_set',
        output='log',
        condition=IfCondition(initial_pose)
    )

    # Optional: 2-D scan helper — keep OFF by default to avoid /scan conflicts
    start_go2_lidar = Node(
        package='go2_control',
        executable='go2_lidar',
        name='go2_lidar',
        output='log',
        condition=IfCondition(start_go2_2d_scan)
    )

    # Optional: teleop — run in a separate terminal normally
    start_teleop_node = Node(
        package='go2_control',
        executable='go2_velocity_commands',
        name='go2_velocity_commands',
        output='log',
        condition=IfCondition(start_teleop)
    )

    # ───── Sensors: ZED (optional) and Velodyne VLP-16 ──────────────────────────
    zed_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('zed_wrapper'), 'launch', 'zed_camera.launch.py')
        ]),
        # Disable TF so ZED doesn't fight RTAB-Map/AMCL over TF
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
        }.items(),
        condition=IfCondition(use_rgbd)
    )

    # Velodyne driver → raw packets; transform → /velodyne_points
    velodyne_driver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('velodyne_driver'),
                         'launch', 'velodyne_driver_node-VLP16-launch.py')
        ]),
        condition=IfCondition(use_velodyne)
    )

    velodyne_transform = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('velodyne_pointcloud'),
                         'launch', 'velodyne_transform_node-VLP16-launch.py')
        ]),
        launch_arguments={'fixed_frame': 'odom'}.items(),
        condition=IfCondition(use_velodyne)
    )

    # ───── RTAB-Map: RGB-D sync (only if using camera) ──────────────────────────
    rgbd_sync = Node(
        package='rtabmap_sync',
        executable='rgbd_sync',
        name='rgbd_sync',
        output='screen',
        parameters=[{
            'approx_sync': True,
            'approx_sync_max_interval': 0.05,  # 50 ms
            'qos': 1,
            'use_sim_time': use_sim_time
        }],
        remappings=[
            ('rgb/image', '/zed/zed_node/rgb/image_rect_color'),
            ('rgb/camera_info', '/zed/zed_node/rgb/camera_info'),
            ('depth/image', '/zed/zed_node/depth/depth_registered')
        ],
        condition=IfCondition(use_rgbd)
    )

    # ───── RTAB-Map: LiDAR odometry (ICP) on /velodyne_points ───────────────────
    icp_odometry = Node(
        package='rtabmap_odom',
        executable='icp_odometry',
        name='icp_odometry',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'frame_id': 'velodyne',
            'odom_frame_id': 'odom',
            'guess_frame_id': 'base_link',
            'publish_tf': False,             # EKF/RTAB-Map handle TF
            'expected_update_rate': 15.0,
            'scan_range_max': 30.0,
            'scan_range_min': 1.0,
            'scan_voxel_size': 0.05,
            # For 3-D LiDAR only:
            'subscribe_scan_cloud': True,
            'subscribe_scan': False,
            # IMU optional for deskewing if you later wire it
            'imu_topic': '/zed/zed_node/imu/data'
        }],
        arguments=[
            'Icp/Deskewing', 'true',
            'Icp/PointToPlane', 'true',
            'Icp/PointToPlaneK', '10',
            'Icp/Iterations', '10',
            'Icp/MaxCorrespondenceDistance', '0.4',
            'Odom/ScanKeyFrameThr', '0.4',
            'OdomF2M/ScanSubtractRadius', '0.05',
            'OdomF2M/MaxTranslation', '0.40',
            '--ros-args'
        ],
        remappings=[('scan_cloud', '/velodyne_points')]
    )

    # ───── RTAB-Map: Localization against a prebuilt database ───────────────────
    rtabmap_node = Node(
        package='rtabmap_slam',
        executable='rtabmap',
        name='rtabmap',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'database_path': rtabmap_db,
            'frame_id': 'velodyne',
            'map_frame_id': 'map',
            'odom_frame_id': 'odom',
            'subscribe_scan_cloud': True,
            'subscribe_rgbd': use_rgbd,
            'approx_sync': True,
            'sync_queue_size': 30,
            'topic_queue_size': 30,
            'qos_scan_cloud': 1,
            'publish_tf': True,
            'delete_db_on_start': True
        }],
        arguments=[
            'Mem/IncrementalMemory', 'false',  # localization-only
            '--ros-args'
        ],
        remappings=[
            ('scan_cloud', '/velodyne_points'),
            ('odom', 'odom')
        ]
    )

    # ───── Nav2 bringup (kept; use AMCL but don’t broadcast TF) ─────────────────
    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_path('nav2_bringup'), 'launch', 'bringup_launch.py')]),
        launch_arguments={
            'params_file': nav2_config,
            'use_sim_time': use_sim_time,
            'map': map_file,   # still load YAML for the static layer
        }.items(),
    )

    # ───── rtabmap_viz for quick inspection ─────────────────────────────────────
    rtabmap_viz = Node(
        package="rtabmap_viz", executable="rtabmap_viz", output="screen",
        parameters=[{'frame_id': 'velodyne', 'use_sim_time': use_sim_time}],
        # Listen to EKF/ICP odom on /odom (don’t remap to /icp_odom)
        remappings=[('odom', '/odom')]
    )

    # ───── Assemble ─────────────────────────────────────────────────────────────
    return LaunchDescription([
        # args
        declare_map_file_cmd,
        declare_rviz_cmd,
        declare_visualization_cmd,
        declare_initial_pose_cmd,
        declare_use_rgbd_cmd,
        declare_use_velodyne_cmd,
        declare_rtabmap_db_cmd,
        declare_start_teleop_cmd,
        declare_start_go2_2d_scan_cmd,

        # base
        base_footprint_to_base_link_tf,
        odom_node,
        robot_localization_node,
        robot_state_publisher_node,
        go2_driver_node,
        state_publisher_node,

        # sensors
        zed_include,
        velodyne_driver,
        velodyne_transform,
        start_go2_lidar,

        # rtabmap stack
        rgbd_sync,
        icp_odometry,
        rtabmap_node,

        # nav2
        nav2_bringup,

        # viz / misc
        rviz2_node,
        set_initial_pose,
        start_teleop_node,
        rtabmap_viz,
    ])
