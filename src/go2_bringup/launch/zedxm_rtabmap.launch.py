#!/usr/bin/env python3
"""
Launch ZED-X Mini + RTAB-Map on ROS 2 Humble
--------------------------------------------
Example:

  ros2 launch my_zedxm_launch zedxm_rtabmap.launch.py           \
        camera_model:=zedxm                                     \
        resolution:=VGA                                          # VGA/HD720/HD1080/HD2K
  # If CPU/GPU is tight, reuse the ZED’s own odometry:
        use_zed_odometry:=true

Dependencies
------------
* stereolabs/zed-ros2-wrapper   (>= v4.0, built against ZED SDK 4.2+)
* rtabmap_ros                  (built from source or Humble binaries)
"""

import os, tempfile
from launch import LaunchDescription, LaunchContext
from launch.actions import DeclareLaunchArgument, OpaqueFunction, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.conditions import UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


# ──────────────────────────── launch_setup ────────────────────────────
def _launch_setup(context: LaunchContext, *args, **kwargs):

    # ── 1.  Override a few ZED-wrapper parameters at runtime ──────────
    resolution = LaunchConfiguration("resolution").perform(context)
    with tempfile.NamedTemporaryFile(mode="w+t", delete=False) as cfg:
        cfg.write(f"""---
/**:
  ros__parameters:
    general:
      grab_resolution: '{resolution}'
""")
        override_path = cfg.name

    # ── 2.  Common RTAB-Map parameters ────────────────────────────────
    common_params = [{
        "frame_id":        LaunchConfiguration("frame_id").perform(context),
        "subscribe_rgbd":  True,               # expect /rgbd_image from the sync node
        "approx_sync":     LaunchConfiguration("approx_sync").perform(context).lower() == "true",
        "wait_imu_to_init": True
    }]

    # IMU always comes from ZED
    remaps = [("imu", "/zed/zed_node/imu/data")]

    # ── 3.  Decide whether we rely on ZED SDK odometry ────────────────
    if LaunchConfiguration("use_zed_odometry").perform(context).lower() in ("true", "1"):
        remaps.append(("odom", "/zed/zed_node/odom"))
        publish_tf = "true"    # let wrapper broadcast odom→base
    else:
        common_params[0]["subscribe_odom_info"] = True
        publish_tf = "false"

    # ── 4.  Assemble launch entities ──────────────────────────────────
    nodes = [

        # 4-A  ZED camera driver
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(
                get_package_share_directory("zed_wrapper"), "launch", "zed_camera.launch.py")),
            launch_arguments={
                "camera_model":           LaunchConfiguration("camera_model"),
                "ros_params_override_path": override_path,
                "publish_tf":             publish_tf,
                "publish_map_tf":         "false",
                "publish_imu_tf":         "true"
            }.items(),
        ),

        # 4-B  Synchronise RGB, depth and camera-info
        Node(
            package="rtabmap_sync", executable="rgbd_sync", output="screen",
            parameters=common_params,
            remappings=[
                ("rgb/image",       "/zed/zed_node/rgb/image_rect_color"),
                ("rgb/camera_info", "/zed/zed_node/rgb/camera_info"),
                ("depth/image",     "/zed/zed_node/depth/depth_registered")
            ]
        ),

        # 4-C  RTAB-Map RGB-D Odometry (skip if we reuse ZED odom)
        Node(
            package="rtabmap_odom", executable="rgbd_odometry", output="screen",
            parameters=common_params,
            remappings=remaps,
            condition=UnlessCondition(LaunchConfiguration("use_zed_odometry")),
        ),

        # 4-D  RTAB-Map SLAM core
        Node(
            package="rtabmap_slam", executable="rtabmap", output="screen",
            parameters=common_params,
            remappings=remaps,
            arguments=["-d", "--delete_db_on_start"]         # start with a fresh DB
        ),

        # 4-E  RTAB-Map GUI
        Node(
            package="rtabmap_viz", executable="rtabmap_viz", output="screen",
            parameters=common_params,
            remappings=remaps
        )
    ]
    return nodes


# ───────────────────────── generate_launch_description ─────────────────
def generate_launch_description() -> LaunchDescription:

    return LaunchDescription([

        # -------- Launch-time arguments --------------------------------
        DeclareLaunchArgument( "camera_model",      default_value="zedxm",
            description="ZED model: zed|zed2|zed2i|zedx|zedxm|virtual" ),

        DeclareLaunchArgument( "resolution",        default_value="HD720",
            description="grab_resolution: SVGA|HD1080|HD1200" ),

        DeclareLaunchArgument( "use_zed_odometry",  default_value="false",
            description="true: use /zed/zed_node/odom  |  false: run RTAB-Map RGB-D odom" ),

        DeclareLaunchArgument( "approx_sync",       default_value="true",
            description="true: tolerate small stamp differences between streams" ),

        DeclareLaunchArgument( "frame_id",          default_value="zed_camera_link",
            description="Base frame published by the ZED wrapper" ),

        # -------- Build launch tree at runtime -------------------------
        OpaqueFunction(function=_launch_setup)
    ])
