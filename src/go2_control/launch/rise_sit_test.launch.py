#!/usr/bin/env python3
from __future__ import annotations

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    startup_delay_s = LaunchConfiguration('startup_delay_s')
    sit_hold_s = LaunchConfiguration('sit_hold_s')
    auto_shutdown = LaunchConfiguration('auto_shutdown')
    shutdown_delay_s = LaunchConfiguration('shutdown_delay_s')
    sport_request_topic = LaunchConfiguration('sport_request_topic')

    return LaunchDescription([
        DeclareLaunchArgument('startup_delay_s', default_value='1.0'),
        DeclareLaunchArgument('sit_hold_s', default_value='10.0'),
        DeclareLaunchArgument('auto_shutdown', default_value='true'),
        DeclareLaunchArgument('shutdown_delay_s', default_value='1.0'),
        DeclareLaunchArgument('sport_request_topic', default_value='/api/sport/request'),
        Node(
            package='go2_control',
            executable='rise_sit_test_node',
            name='rise_sit_test_node',
            output='screen',
            parameters=[{
                'startup_delay_s': startup_delay_s,
                'sit_hold_s': sit_hold_s,
                'auto_shutdown': auto_shutdown,
                'shutdown_delay_s': shutdown_delay_s,
                'sport_request_topic': sport_request_topic,
            }],
        ),
    ])
