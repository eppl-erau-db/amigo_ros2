import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_path, get_package_share_directory
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    urdf_path = os.path.join(get_package_share_path('go2_description'), 'urdf', 'go2.urdf.xacro')
    rviz_config_path = os.path.join(get_package_share_path('go2_description'),
                                    'config', 'nav_nvblox_config.rviz')

    # NOTE: map_file is no longer used by Nav2 when we run slam_toolbox localization.
    # You can still keep this argument around if other tooling expects it.
    map_file = LaunchConfiguration(
        'map_file',
        default=os.path.join(get_package_share_path('go2_description'),
                             'maps', 'demo_map.yaml')
    )

    rviz = LaunchConfiguration('rviz', default='false')
    initial_pose = LaunchConfiguration('initial_pose', default='false')

    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    declare_map_file_cmd = DeclareLaunchArgument(
        'map_file',
        default_value=os.path.join(get_package_share_path('go2_description'),
                                   'maps', 'demo_map.yaml'),
        description='(Unused by Nav2 when using slam_toolbox localization; kept for compatibility)'
    )

    declare_rviz_cmd = DeclareLaunchArgument(
        'rviz',
        default_value='false',
        description='Whether to start RViz'
    )

    declare_initial_pose_cmd = DeclareLaunchArgument(
        'initial_pose',
        default_value='false',
        description='Enable or disable initial pose publisher node.'
    )

    # ───────────────── Robot & sensors ─────────────────

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
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

    nav2_config = os.path.join(
        get_package_share_path('go2_description'),
        'config',
        'nav2_mppi_controller.yaml'
    )

    robot_localization_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='log',
        parameters=[os.path.join(get_package_share_path('go2_description'),
                                 'config', 'ekf.yaml')],
        remappings=[
            ('/odometry/filtered', '/odom'),
            ('/set_pose', '/initialpose')
        ],
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

    start_go2_lidar = Node(
        package='go2_control',
        executable='go2_lidar',
        name='go2_lidar',
        output='log',
    )

    start_teleop_node = Node(
        package='go2_control',
        executable='go2_velocity_commands',
        name='go2_velocity_commands',
        output='log'
    )

    search_action_server_node = Node(
        package='go2_control',
        executable='search_action_server',
        name='leak_search_server',
        parameters=[{'use_sim_time': use_sim_time}],
        output='log'
    )

    rounds_coordinator_node = Node(
        package='go2_control',
        executable='rounds_coordinator',
        name='rounds_coordinator',
        parameters=[{'use_sim_time': use_sim_time}],
        output='log'
    )

    # ───────────────── slam_toolbox in localization mode ─────────────────

    slam_params = os.path.join(
        get_package_share_path('go2_description'),
        'config',
        'slam_toolbox_localization.yaml'
    )

    slam_toolbox_node = Node(
        package='slam_toolbox',
        executable='localization_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[
            slam_params,
            {'use_sim_time': use_sim_time}
        ],
        remappings=[
            # Already using /scan, so no remap needed; this is explicit
            ('/scan', '/scan'),
            # slam_toolbox subscribes to /initialpose like AMCL, no change needed
        ],
    )

    # ───────────────── Nav2 core only (no map_server, no AMCL) ─────────────────

    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    nav2_navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, 'launch', 'navigation_launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'params_file': nav2_config,
            # autostart, use_composition, etc. will use defaults from nav2_bringup
        }.items(),
    )

    return LaunchDescription([
        declare_map_file_cmd,
        declare_rviz_cmd,
        declare_initial_pose_cmd,
        robot_state_publisher_node,
        base_footprint_to_base_link_tf,
        go2_driver_node,
        state_publisher_node,
        odom_node,
        robot_localization_node,
        lidar_node,
        start_go2_lidar,
        slam_toolbox_node,
        nav2_navigation,
        rviz2_node,
        # set_initial_pose,  # enable if you want automatic initial pose on startup
        search_action_server_node,
        rounds_coordinator_node,
    ])
