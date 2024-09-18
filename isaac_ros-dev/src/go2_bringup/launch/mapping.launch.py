from launch import LaunchDescription
from launch_ros.parameter_descriptions import ParameterValue
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch.substitutions import LaunchConfiguration
import os
from launch.actions import TimerAction
from ament_index_python.packages import get_package_share_directory
from ament_index_python.packages import get_package_share_path

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    urdf_path = os.path.join(get_package_share_path('go2_description'), 
                             'urdf', 'go2_nav2_nvblox.urdf')
    rviz_config_path = os.path.join(get_package_share_path('go2_description'), 
                             'config', 'go2_urdf_config.rviz')
    
    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    robot_state_publisher_node = Node(
        package="robot_state_publisher", 
        executable="robot_state_publisher", 
        parameters=[{'robot_description': robot_description}]     
    )

    rviz2_node = Node(
        package="rviz2", 
        executable="rviz2", 
        arguments=['-d', rviz_config_path]
    )

    state_publisher_node = Node(
        package="go2_control",  
        executable="go2_state", 
        name='go2_state',
        output='screen'
    )

    odom_node = Node(
        package="go2_control",  
        executable="odom_node", 
        name='odom_node',
        output='screen'
    )


    go2_driver_node = Node(
        package="go2_driver",
        executable="go2_driver_node",
        name="go2_driver_node",
        output="screen"
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

    slam_toolbox_config = os.path.join(
        get_package_share_directory('go2_description'),
        'config',
        'mapper_params_online_async.yaml'
    )

    slam_toolbox = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[slam_toolbox_config],
        remappings=[
            ('pose', '/slam_toolbox_pose')
        ]
    )

    nav2_config = os.path.join(
        get_package_share_directory('go2_description'),
        'config',
        'nav2_mppi_controller.yaml'
    )

    robot_localization_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[os.path.join(get_package_share_path('go2_description'), 'config', 'ekf.yaml')],
        remappings=[('/odometry/filtered', '/odom')]
    )

    log_pose_action_server_node = Node(
        package='go2_control',
        executable='log_pose_action_server',
        name='log_pose_action_server',
        output='screen',
        parameters=[{'save_path': 'pose_log.json'}],
    )

    return LaunchDescription([
        base_footprint_to_base_link_tf,
        odom_node,
        robot_localization_node,
        lidar_node,
        robot_state_publisher_node,
        log_pose_action_server_node,
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('nvblox_examples_bringup'), 'launch', 'realsense_example.launch.py')]),
            launch_arguments={
                'mode': 'dynamic',
                'visualization': 'false',
            }.items(),
        ),
        go2_driver_node,
        state_publisher_node,
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'navigation_launch.py')]),
            launch_arguments={
                'params_file': nav2_config,
                'use_sim_time': use_sim_time,
            }.items(),
        ),
        slam_toolbox,
        rviz2_node
    ])
