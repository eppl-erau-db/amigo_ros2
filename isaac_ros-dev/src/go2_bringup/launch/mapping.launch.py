from launch import LaunchDescription
from launch_ros.parameter_descriptions import ParameterValue
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch.substitutions import LaunchConfiguration
import os
from ament_index_python.packages import get_package_share_directory
from ament_index_python.packages import get_package_share_path

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    urdf_path = os.path.join(get_package_share_path('go2_description'), 
                             'urdf', 'go2_nav2_nvblox.urdf')
    # rviz_config_path = os.path.join(get_package_share_path('go2_description'), 
    #                          'config', 'go2_urdf_config.rviz')
    
    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    robot_state_publisher_node = Node(
        package="robot_state_publisher", 
        executable="robot_state_publisher", 
        parameters=[{'robot_description': robot_description}]     
    )

    # rviz2_node = Node(
    #     package="rviz2", 
    #     executable="rviz2", 
    #     arguments=['-d', rviz_config_path]
    # )

    state_publisher_node = Node(
        package="go2_control",  
        executable="go2_state", 
        name='go2_state',
        output='screen'
    )

    go2_driver_node = Node(
        package="go2_control",
        executable="go2_driver",
        name="go2_driver",
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

    slam_toolbox_config = os.path.join(
        get_package_share_directory('go2_description'),
        'config',
        'mapper_params_online_async.yaml'
    )

    nav2_config = os.path.join(
        get_package_share_directory('go2_description'),
        'config',
        'nav2_nvblox_params.yaml'
    )

    robot_localization_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[os.path.join(get_package_share_path('go2_description'), 'config', 'ekf.yaml')],
        remappings=[('/odometry/filtered', '/odom')]
    )

    return LaunchDescription([
        base_footprint_to_base_link_tf,
        cam_imu_tf,
        robot_state_publisher_node,
        robot_localization_node,
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('nvblox_examples_bringup'), 'launch', 'realsense_example.launch.py')]),
            launch_arguments={
                'mode': 'dynamic',
                'visualization': 'true'
                # 'people_segmentation': 'peoplesemsegnet_shuffleseg',
            }.items(),
        ),
        state_publisher_node,
        go2_driver_node,
        lidar_node,

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'navigation_launch.py')]),
            launch_arguments={
                'params_file': nav2_config,
                'use_sim_time': use_sim_time,
            }.items(),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('slam_toolbox'), 'launch', 'online_async_launch.py')]),
            launch_arguments={
                'params_file': slam_toolbox_config, 
                'use_sim_time': use_sim_time,
            }.items(),
        ),

        # rviz2_node
    ])