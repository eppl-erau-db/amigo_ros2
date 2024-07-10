import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_path
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    urdf_path = os.path.join(get_package_share_path('go2_description'), 'urdf', 'go2_nav2.urdf')
    rviz_config_path = os.path.join(get_package_share_path('go2_description'), 'config', 'nav_config.rviz')
    
    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description, 'use_sim_time': use_sim_time}],
        output='screen'
    )

    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config_path],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    map_to_odom_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="map_to_odom",
        arguments=["0", "0", "0", "0", "0", "0", "map", "odom"]
    )

    base_footprint_to_baselink_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="base_footprint_to_baselink",
        arguments=["0", "0", "0.35", "0", "0", "0", "base_footprint", "base_link"]
    )

    odometry_node = Node(
        package='go2_control',
        executable='odom_node',
        name='odom_node',
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    state_publisher_node = Node(
        package='go2_control',
        executable='go2_state',
        name='go2_state',
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    go2_driver_node = Node(
        package='go2_driver',
        executable='go2_driver_node',
        name='go2_driver_node',
        parameters=[{'use_sim_time': use_sim_time}],
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
            'use_sim_time': use_sim_time,
        }],
    )

    nav2_config = os.path.join(
        get_package_share_path('go2_description'),
        'config',
        'nav2_params.yaml'
    )

    map_file_arg = DeclareLaunchArgument(
        'map_file',
        default_value=os.path.join(
            get_package_share_path('go2_description'),
            'maps',
            'lab.yaml'
        ),
        description='Full path to the map file to load'
    )

    map_file = LaunchConfiguration('map_file')

    return LaunchDescription([
        map_file_arg,
        map_to_odom_tf,
        odometry_node,
        base_footprint_to_baselink_tf,
        robot_state_publisher_node,
        state_publisher_node,
        go2_driver_node,
        lidar_node,

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(get_package_share_path('nav2_bringup'), 'launch', 'bringup_launch.py')]),
            launch_arguments={
                'params_file': nav2_config,
                'use_sim_time': use_sim_time,
                'map': map_file,
            }.items(),
        ),

        rviz2_node
    ])
