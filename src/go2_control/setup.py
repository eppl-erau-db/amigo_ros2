# Copyright (c) 2024, RoboVerse community
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import os
from glob import glob
from setuptools import setup
from setuptools import find_packages

package_name = 'go2_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'urdf'), glob(os.path.join('urdf', '*'))),
        (os.path.join('share', package_name, 'dae'), glob(os.path.join('dae', '*'))),
        (os.path.join('share', package_name, 'meshes'), glob(os.path.join('meshes', '*'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*'))),

        
        
    ],
    install_requires=['setuptools', 'tf-transformations'],
    zip_safe=True,
    maintainer='',
    maintainer_email='',
    description='',
    license='BSD-3-Clause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'go2_driver = go2_control.go2_driver:main',
            'odom_node = go2_control.odom_node:main',
            'go2_state = go2_control.go2_state:main',
            'vslam_odom_node = go2_control.vslam_odom_node:main',
            'base_to_base_tf = go2_control.base_to_base_tf:main',
            'initial_pose_set = go2_control.initial_pose_set:main',
            'log_pose_action_client = go2_control.log_pose_action_client:main',
            'log_pose_action_server = go2_control.log_pose_action_server:main',
            'task_nav_path_test = go2_control.task_nav_path_test:main',
            'task_nav_to_pose_test = go2_control.task_nav_to_pose_test:main',
            'go2_velocity_commands = go2_control.go2_velocity_commands:main',
            'go2_lidar = go2_control.go2_lidar:main',
            'map_localizer_client = go2_control.map_localizer_client:main',
            'region_map_service_node = go2_control.region_map_service_node:main',
            'region_map_client_node = go2_control.region_map_client_node:main',
            'occupancy_grid_to_image = go2_control.occupancy_grid_to_image:main',
            'search_action_server = go2_control.search_action_server:main',
            'mod_waypoint_follower = go2_control.mod_waypoint_follower:main',
            'gps_waypoint_logger = go2_control.gps_waypoint_logger:main',
            'picture_taker = go2_control.picture_taker:main',
            'logged_waypoint_follower = go2_control.logged_waypoint_follower:main',
            'rounds_coordinator = go2_control.rounds_coordinator:main',
            'pose_click_logger = go2_control.pose_click_logger:main',
            'dummy_leak_publisher = go2_control.dummy_leak_publisher:main',
            'voice_command_node = go2_control.voice_command_node:main',
            'mission_supervisor_node = go2_control.mission_supervisor_node:main',
            'hello_controller_node = go2_control.hello_controller_node:main',
            'voice_attention_controller_node = go2_control.voice_attention_controller_node:main',
            'voice_ready_controller_node = go2_control.voice_ready_controller_node:main',
            'walk_upright_controller_node = go2_control.walk_upright_controller_node:main',
            'slam_scan_gate_node = go2_control.slam_scan_gate_node:main',
            'person_follow_controller_node = go2_control.person_follow_controller_node:main',
            'voice_stt_vosk_node = go2_control.voice_stt_vosk_node:main',
            'sound_localizer = go2_control.sound_localizer:main',
            'explore_until_detected_action_server = go2_control.explore_until_detected_action_server:main',
            'explore_area_action_server = go2_control.explore_area_action_server:main',
            'explore_area_landmark_report = go2_control.explore_area_landmark_report:main',
            'explore_area_landmark_watch = go2_control.explore_area_landmark_watch:main',
            'localize_detected_leak_action_server = go2_control.localize_detected_leak_action_server:main',
            'voice_speaker_verifier_node = go2_control.voice_speaker_verifier_node:main',
            'create_speaker_reference = go2_control.create_speaker_reference:main',
            'enroll_speaker_node = go2_control.enroll_speaker_node:main',
            'rise_sit_test_node = go2_control.rise_sit_test_node:main',

        ],
    },
)
