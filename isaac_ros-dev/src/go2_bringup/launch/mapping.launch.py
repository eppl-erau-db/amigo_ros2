#!/usr/bin/env python3
"""
Launch: Go2 mapping with 3-D UTLiDAR + RTAB-Map (2-D projection grid)
"""

from launch import LaunchDescription
from launch_ros.parameter_descriptions import ParameterValue
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory, get_package_share_path
import os

def generate_launch_description():

    declare_sim_time = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='false',
        description='Use simulated clock if true'
    ) 
    # --- common paths ---------------------------------------------------
    pkg_go2_desc   = get_package_share_path('go2_description')
    urdf_path      = os.path.join(pkg_go2_desc, 'urdf', 'go2_nav2_nvblox.urdf')
    rviz_config    = os.path.join(pkg_go2_desc, 'config', 'go2_urdf_config.rviz')
    nav2_config    = os.path.join(pkg_go2_desc, 'config', 'nav2_mppi_controller.yaml')
    ekf_config     = os.path.join(pkg_go2_desc, 'config', 'ekf.yaml')
    # create a small RTAB-Map YAML inside the same package (see §2)
    rtabmap_params = os.path.join(pkg_go2_desc, 'config', 'rtabmap_utlidar.yaml')

    use_sim_time   = LaunchConfiguration('use_sim_time')

    # --- URDF -----------------------------------------------------------
    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)
    robot_state_pub   = Node(
        package    = "robot_state_publisher",
        executable = "robot_state_publisher",
        parameters = [{'robot_description': robot_description}]
    )

    # --- core Go2 / TF / odom nodes ------------------------------------
    base_tf = Node(
        package='go2_control', executable='base_to_base_tf',
        name='base_to_base_tf', output='screen'
    )
    state_pub = Node(
        package='go2_control', executable='go2_state',
        name='go2_state', output='screen'
    )
    odom_node = Node(                                     # wheel/IMU odom
        package='go2_control', executable='odom_node',
        name='odom_node', output='screen'
    )
    go2_driver = Node(
        package='go2_driver', executable='go2_driver_node',
        name='go2_driver_node', output='screen'
    )
    ekf_node = Node(
        package='robot_localization', executable='ekf_node',
        name='ekf_filter_node', output='screen',
        parameters=[ekf_config],
        remappings=[('/odometry/filtered', '/odom')]
    )

    # --- (optional) PointCloud2 frame-ID fixer -------------------------
    # keep if you still need to rewrite /utlidar/cloud ➜ /pointcloud
    lidar_repub = Node(
        package='go2_control', executable='go2_lidar',  # your python node
        name='go2_lidar', output='screen'
    )

    # --- RTAB-Map SLAM --------------------------------------------------
    rtabmap_node = Node(
        package='rtabmap_slam',
        executable='rtabmap',
        name='rtabmap',
        output='screen',
        parameters=[{'frame_id': 'radar',
                    'subscribe_scan_cloud': True,
                    'subscribe_depth': False,
                    'subscribe_rgb': False,
                    'approx_sync': True,
                    'sync_queue_size': 30,
                    'topic_queue_size': 30,
                    'wait_for_transform': 0.3,
                    'publish_tf': True,
                    'map_frame_id': 'map',
                    'odom_frame_id': 'odom',
                    "delete_db_on_start": True,
                    'use_sim_time': LaunchConfiguration('use_sim_time')}],
        remappings=[('scan_cloud', '/pointcloud'),
                    ('odom', '/odom')],
        # ---- every parameter that contains “/” goes here ↓ ----
        arguments=[
            # ICP / registration
            'Reg/Strategy', '1',
            'Icp/PointToPlane', 'true',
            'Icp/VoxelSize', '0.05',
            'Icp/Iterations', '30',
            'Icp/MaxCorrespondenceDistance', '0.5',
            # Occupancy-grid
            'RGBD/CreateOccupancyGrid', 'true',
            'Grid/3D', 'false',
            'Grid/RangeMax', '12',
            'Grid/Resolution', '0.07',
            # Memory / performance
            # 'Mem/STMSize', '30',
            # 'Mem/NotLinkedNodesKept', 'false',
            '--ros-args'        # keep this at the end
        ])
    # )

    # rtabmap_node = Node(
    #     package='rtabmap_slam',
    #     executable='rtabmap',
    #     name='rtabmap',
    #     output='screen',
    #     parameters=[rtabmap_params,
    #                 {'use_sim_time': use_sim_time}],
    #     remappings=[('scan_cloud', '/pointcloud'),
    #                 ('odom', '/odom')]
    # )

    # Relay 2-D proj map to the latched /map topic that Nav2’s static-layer expects
    map_relay = Node(
        package='topic_tools', executable='relay',
        arguments=['/rtabmap/proj_map', '/map'],
        name='proj_map_relay',
        output='screen'
    )

    # --- RViz -----------------------------------------------------------
    rviz2 = Node(
        package='rviz2', executable='rviz2',
        arguments=['-d', rviz_config]
    )

    # --- Nav2 bring-up (unchanged) -------------------------------------
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(get_package_share_directory('nav2_bringup'),
                          'launch', 'navigation_launch.py')]
        ),
        launch_arguments={
            'params_file' : nav2_config,
            'use_sim_time': use_sim_time,
            'localization': 'false', #stops launch file from using amcl tf
            # leave 'slam' unset (False) because RTAB-Map handles mapping
        }.items(),
    )

    log_pose_server = Node(
        package='go2_control',
        executable='log_pose_action_server',
        name='log_pose_action_server',
        output='screen',
        parameters=[{'save_path': 'pose_log.json'}],
    )

    # --- nvblox example (unchanged) ------------------------------------
    # nvblox_launch = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         [os.path.join(get_package_share_directory('nvblox_examples_bringup'),
    #                      'launch', 'realsense_example.launch.py')]
    #     ),
    #     launch_arguments={'mode':'dynamic', 'visualization':'false'}.items(),
    # )

    return LaunchDescription([
        declare_sim_time,
        base_tf,
        odom_node,
        ekf_node,
        lidar_repub, 
        rtabmap_node,              
        robot_state_pub,
        log_pose_server,
        go2_driver,
        state_pub,
        # nvblox_launch,
        map_relay,
        nav2_launch,
        rviz2,
    ])
