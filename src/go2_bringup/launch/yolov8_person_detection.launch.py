#!/usr/bin/env python3
from __future__ import annotations

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode


def generate_launch_description():
    isaac_ros_ws = EnvironmentVariable(
        "ISAAC_ROS_WS",
        default_value="/home/castej/workspaces/isaac_ros-dev",
    )
    default_engine_path = PathJoinSubstitution(
        [
            isaac_ros_ws,
            "isaac_ros_assets",
            "models",
            "yolov8",
            "yolov8s.plan",
        ]
    )
    image_input_topic = LaunchConfiguration("image_input_topic")
    camera_info_input_topic = LaunchConfiguration("camera_info_input_topic")
    input_image_width = LaunchConfiguration("input_image_width")
    input_image_height = LaunchConfiguration("input_image_height")
    network_image_width = LaunchConfiguration("network_image_width")
    network_image_height = LaunchConfiguration("network_image_height")
    input_encoding = LaunchConfiguration("input_encoding")
    image_mean = LaunchConfiguration("image_mean")
    image_stddev = LaunchConfiguration("image_stddev")
    input_qos = LaunchConfiguration("input_qos")
    output_qos = LaunchConfiguration("output_qos")
    enable_padding = LaunchConfiguration("enable_padding")
    keep_aspect_ratio = LaunchConfiguration("keep_aspect_ratio")
    crop_mode = LaunchConfiguration("crop_mode")
    model_file_path = LaunchConfiguration("model_file_path")
    engine_file_path = LaunchConfiguration("engine_file_path")
    input_tensor_names = LaunchConfiguration("input_tensor_names")
    input_binding_names = LaunchConfiguration("input_binding_names")
    output_tensor_names = LaunchConfiguration("output_tensor_names")
    output_binding_names = LaunchConfiguration("output_binding_names")
    verbose = LaunchConfiguration("verbose")
    force_engine_update = LaunchConfiguration("force_engine_update")
    confidence_threshold = LaunchConfiguration("confidence_threshold")
    nms_threshold = LaunchConfiguration("nms_threshold")
    num_classes = LaunchConfiguration("num_classes")

    encoder_dir = get_package_share_directory("isaac_ros_dnn_image_encoder")
    yolov8_encoder_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(encoder_dir, "launch", "dnn_image_encoder.launch.py")]
        ),
        launch_arguments={
            "input_image_width": input_image_width,
            "input_image_height": input_image_height,
            "network_image_width": network_image_width,
            "network_image_height": network_image_height,
            "image_mean": image_mean,
            "image_stddev": image_stddev,
            "input_qos": input_qos,
            "output_qos": output_qos,
            "input_encoding": input_encoding,
            "encoding_desired": input_encoding,
            "enable_padding": enable_padding,
            "keep_aspect_ratio": keep_aspect_ratio,
            "crop_mode": crop_mode,
            "attach_to_shared_component_container": "True",
            "component_container_name": "/yolov8_container",
            "dnn_image_encoder_namespace": "yolov8_encoder",
            "image_input_topic": image_input_topic,
            "camera_info_input_topic": camera_info_input_topic,
            "tensor_output_topic": "/tensor_pub",
        }.items(),
    )

    tensor_rt_node = ComposableNode(
        name="tensor_rt",
        package="isaac_ros_tensor_rt",
        plugin="nvidia::isaac_ros::dnn_inference::TensorRTNode",
        parameters=[
            {
                "model_file_path": model_file_path,
                "engine_file_path": engine_file_path,
                "output_binding_names": output_binding_names,
                "output_tensor_names": output_tensor_names,
                "input_tensor_names": input_tensor_names,
                "input_binding_names": input_binding_names,
                "verbose": verbose,
                "force_engine_update": force_engine_update,
            }
        ],
    )
    yolov8_decoder_node = ComposableNode(
        name="yolov8_decoder_node",
        package="isaac_ros_yolov8",
        plugin="nvidia::isaac_ros::yolov8::YoloV8DecoderNode",
        parameters=[
            {
                "confidence_threshold": confidence_threshold,
                "nms_threshold": nms_threshold,
                "num_classes": num_classes,
            }
        ],
    )
    yolov8_container = ComposableNodeContainer(
        name="yolov8_container",
        namespace="",
        package="rclcpp_components",
        executable="component_container_mt",
        composable_node_descriptions=[tensor_rt_node, yolov8_decoder_node],
        arguments=["--ros-args", "--log-level", "INFO"],
        output="screen",
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "image_input_topic",
                default_value="/camera/color/image_raw",
                description="RealSense color image topic consumed by YOLOv8.",
            ),
            DeclareLaunchArgument(
                "camera_info_input_topic",
                default_value="/camera/color/camera_info",
                description="RealSense color camera info topic consumed by YOLOv8.",
            ),
            DeclareLaunchArgument(
                "input_image_width",
                default_value="640",
                description="Width of the RealSense source image before YOLO preprocessing.",
            ),
            DeclareLaunchArgument(
                "input_image_height",
                default_value="360",
                description="Height of the RealSense source image before YOLO preprocessing.",
            ),
            DeclareLaunchArgument(
                "network_image_width",
                default_value="640",
                description="YOLOv8 network input width.",
            ),
            DeclareLaunchArgument(
                "network_image_height",
                default_value="640",
                description="YOLOv8 network input height.",
            ),
            DeclareLaunchArgument("input_encoding", default_value="rgb8"),
            DeclareLaunchArgument("image_mean", default_value="[0.0, 0.0, 0.0]"),
            DeclareLaunchArgument("image_stddev", default_value="[1.0, 1.0, 1.0]"),
            DeclareLaunchArgument("input_qos", default_value="SENSOR_DATA"),
            DeclareLaunchArgument("output_qos", default_value="DEFAULT"),
            DeclareLaunchArgument("enable_padding", default_value="True"),
            DeclareLaunchArgument("keep_aspect_ratio", default_value="True"),
            DeclareLaunchArgument("crop_mode", default_value="CENTER"),
            DeclareLaunchArgument("model_file_path", default_value=""),
            DeclareLaunchArgument("engine_file_path", default_value=default_engine_path),
            DeclareLaunchArgument("input_tensor_names", default_value='["input_tensor"]'),
            DeclareLaunchArgument("input_binding_names", default_value='["images"]'),
            DeclareLaunchArgument("output_tensor_names", default_value='["output_tensor"]'),
            DeclareLaunchArgument("output_binding_names", default_value='["output0"]'),
            DeclareLaunchArgument("verbose", default_value="False"),
            DeclareLaunchArgument("force_engine_update", default_value="False"),
            DeclareLaunchArgument("confidence_threshold", default_value="0.25"),
            DeclareLaunchArgument("nms_threshold", default_value="0.45"),
            DeclareLaunchArgument("num_classes", default_value="80"),
            yolov8_container,
            yolov8_encoder_launch,
        ]
    )
