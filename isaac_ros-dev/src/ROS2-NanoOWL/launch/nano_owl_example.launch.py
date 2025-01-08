# SPDX-FileCopyrightText: Copyright (c) <year> NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    launch_args = [
        DeclareLaunchArgument(
            'thresholds',
            default_value='0.1',
            description='Threshold for filtering detections'),
        DeclareLaunchArgument(
            'image_encoder_engine',
            default_value='src/ROS2-NanoOWL/data/owl_image_encoder_patch32.engine',
            description='Path to the TensorRT engine for the OWL-ViT vision encoder'),
    ]

    # NanoOWL parameters
    thresholds = LaunchConfiguration('thresholds')
    image_encoder_engine = LaunchConfiguration('image_encoder_engine')

    nanoowl_node = Node(
            package='ros2_nanoowl',
            executable='nano_owl_py',
            parameters=[{
                'model': 'google/owlvit-base-patch32',
                'image_encoder_engine': image_encoder_engine,
                'thresholds':thresholds,
            }]
    )
    
    final_launch_description = launch_args + [nanoowl_node]
    
    return LaunchDescription(final_launch_description)
