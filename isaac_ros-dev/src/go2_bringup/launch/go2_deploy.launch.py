import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, LogInfo
from launch.conditions import IfCondition
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_path, get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    urdf_path = os.path.join(get_package_share_path('go2_description'), 'urdf', 'go2_nav2_nvblox.urdf')
    rviz_config_path = os.path.join(get_package_share_path('go2_description'), 'config', 'nav_nvblox_config.rviz')
    map_file = LaunchConfiguration('map_file', default=os.path.join(get_package_share_path('go2_description'), 'maps', 'first_floor_coas.yaml'))
    rviz = LaunchConfiguration('rviz', default='false')
    visualization = LaunchConfiguration('visualization', default='true')
    
    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    declare_map_file_cmd = DeclareLaunchArgument(
        'map_file',
        default_value=os.path.join(get_package_share_path('go2_description'), 'maps', 'first_floor_coas.yaml'),
        description='Full path to the map file to load'
    )

    declare_rviz_cmd = DeclareLaunchArgument(
        'rviz',
        default_value='false',
        description='Whether to start RViz'
    )

    declare_visualization_cmd = DeclareLaunchArgument(
        'visualization',
        default_value='true',
        description='Enable or disable visualization.'
    )

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
        output='log'
    )

    lidar_node = Node(
        name='rplidar_composition',
        package='rplidar_ros',
        executable='rplidar_composition',
        output='log',
        parameters=[{
            'serial_port': '/dev/ttyUSB0',
            'serial_baudrate': 115200,
            'frame_id': 'laser',
            'inverted': False,
            'angle_compensate': True,
        }],
    )

    nav2_config = os.path.join(
        get_package_share_path('go2_description'),
        'config',
        'nav2_nvblox_params.yaml'
    )

    robot_localization_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='log',
        parameters=[os.path.join(get_package_share_path('go2_description'), 'config', 'ekf.yaml')],
        remappings=[('/odometry/filtered', '/odom')]
    )

    set_initial_pose = Node(
        package='go2_control',
        executable='initial_pose_set',
        name='initial_pose_set',
        output='log'
    )

    return LaunchDescription([
        declare_map_file_cmd,
        declare_rviz_cmd,
        declare_visualization_cmd,
        base_footprint_to_base_link_tf,
        cam_imu_tf,
        robot_state_publisher_node,
        robot_localization_node,
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('nvblox_examples_bringup'), 'launch', 'realsense_example.launch.py')]),
            launch_arguments={
                'mode': 'dynamic',
                'visualization': visualization,
            }.items(),
        ),
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
        rviz2_node,
        # set_initial_pose,
    ])
