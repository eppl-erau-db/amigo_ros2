import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_path, get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    # Declare the launch arguments
    mode_arg = DeclareLaunchArgument(
        'mode',
        default_value='pose_collection',
        description='Mode to run: mapping or pose_collection'
    )

    map_file_arg = DeclareLaunchArgument(
        'map_name',
        default_value='lab.yaml',
        description='Name of the map file to load from the maps directory'
    )

    use_rviz_arg = DeclareLaunchArgument(
        'use_rviz',
        default_value='false',
        description='Whether to launch RViz'
    )

    visualization_arg = DeclareLaunchArgument(
        'visualization',
        default_value='false',
        description='Whether to use visualization in realsense_example.launch.py'
    )

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time'
    )

    poses_save_path_arg = DeclareLaunchArgument(
        'poses_save_path',
        default_value='pose_log.json',
        description='Path to save the pose log'
    )

    # Access the values of the launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_rviz = LaunchConfiguration('use_rviz')
    visualization = LaunchConfiguration('visualization')
    mode = LaunchConfiguration('mode')
    map_name = LaunchConfiguration('map_name')
    poses_save_path = LaunchConfiguration('poses_save_path')

    # Paths to necessary files
    urdf_path = os.path.join(get_package_share_path('go2_description'), 'urdf', 'go2_nav2_nvblox.urdf')
    nav2_config = os.path.join(get_package_share_path('go2_description'), 'config', 'nav2_nvblox_params.yaml')
    slam_toolbox_config = os.path.join(get_package_share_path('go2_description'), 'config', 'slam_toolbox_params.yaml')
    
    # Conditional paths for rviz config
    rviz_config_path_mapping = os.path.join(get_package_share_path('go2_description'), 'config', 'go2_urdf_config.rviz')
    rviz_config_path_pose_collection = os.path.join(get_package_share_path('go2_description'), 'config', 'nav_nvblox_config.rviz')

    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    # Nodes
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
        output='screen'
    )

    rviz2_node_pose = Node(
        condition=IfCondition(LaunchConfiguration('use_rviz')) & IfCondition(mode=='pose_collection'),
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config_path_pose_collection],
        output='screen'
    )

    rviz2_node_map = Node(
        condition=IfCondition(LaunchConfiguration('use_rviz')) & IfCondition(mode=='mapping'),
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config_path_mapping],
        output='screen'
    )

    state_publisher_node = Node(
        package='go2_control',
        executable='go2_state',
        name='go2_state',
        output='screen'
    )

    go2_driver_node = Node(
        package='go2_driver',
        executable='go2_driver_node',
        name='go2_driver_node',
        output='screen'
    )

    cam_imu_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="cam_imu",
        arguments=["0", "0", "0", "0", "0", "0", "camera_gyro_optical_frame", "camera_imu_optical_frame"]
    )

    base_footprint_to_base_link_tf = Node(
        package='go2_control',
        executable='base_to_base_tf',
        name='base_to_base_tf',
        output='screen'
    )

    lidar_node = Node(
        name='rplidar_composition',
        package='rplidar_ros',
        executable='rplidar_composition',
        output='screen',
        parameters=[{
            'serial_port': '/dev/ttyUSB0',
            'serial_baudrate': 115200,
            'frame_id': 'laser',
            'inverted': False,
            'angle_compensate': True,
        }],
    )

    robot_localization_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[os.path.join(get_package_share_path('go2_description'), 'config', 'ekf.yaml')],
        remappings=[('/odometry/filtered', '/odom')]
    )

    set_initial_pose = Node(
        package='go2_control',
        executable='initial_pose_set',
        name='initial_pose_set',
        output='screen',
        condition=IfCondition(mode == 'pose_collection')
    )

    log_pose_action_server_node = Node(
        package='go2_control',
        executable='log_pose_action_server',
        name='log_pose_action_server',
        output='screen',
        parameters=[{'save_path': poses_save_path}],
        condition=IfCondition(mode == 'pose_collection')
    )

    map_file = PathJoinSubstitution([
        get_package_share_path('go2_description'),
        'maps',
        map_name
    ])

    # IncludeLaunchDescription for realsense_example.launch.py
    realsense_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('nvblox_examples_bringup'), 'launch', 'realsense_example.launch.py')]),
        launch_arguments={
            'mode': 'dynamic',
            'visualization': visualization,
        }.items(),
    )

    # Conditional Launch for Navigation and SLAM
    navigation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_path('nav2_bringup'), 'launch', 'navigation_launch.py')]),
        launch_arguments={
            'params_file': nav2_config,
            'use_sim_time': use_sim_time,
        }.items(),
        condition=IfCondition(mode == 'mapping')
    )

    slam_toolbox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_path('slam_toolbox'), 'launch', 'online_async_launch.py')]),
        launch_arguments={
            'params_file': slam_toolbox_config, 
            'use_sim_time': use_sim_time,
        }.items(),
        condition=IfCondition(mode == 'mapping')
    )

    pose_collection_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_path('nav2_bringup'), 'launch', 'bringup_launch.py')]),
        launch_arguments={
            'params_file': nav2_config,
            'use_sim_time': use_sim_time,
            'map': map_file,
        }.items(),
        condition=IfCondition(mode == 'pose_collection')
    )

    return LaunchDescription([
        # Add launch arguments
        mode_arg,
        map_file_arg,
        use_rviz_arg,
        visualization_arg,
        use_sim_time_arg,
        poses_save_path_arg,

        # Add nodes and include launch descriptions
        robot_state_publisher_node,
        rviz2_node_pose,
        rviz2_node_map,
        state_publisher_node,
        go2_driver_node,
        cam_imu_tf,
        base_footprint_to_base_link_tf,
        lidar_node,
        robot_localization_node,
        set_initial_pose,
        log_pose_action_server_node,
        realsense_launch,
        navigation_launch,
        slam_toolbox_launch,
        pose_collection_launch,
    ])
