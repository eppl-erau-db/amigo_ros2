# Go2 Mapping Launch Commands

This file tracks the current workflow in `src/go2_bringup/launch/mapping.launch.py` and the RealSense YOLOv8 person-follow launcher.

## Setup

Source ROS and the built workspace before launching:

```bash
source /opt/ros/$ROS_DISTRO/setup.bash
source install/setup.bash
```

On the Jetson workspace used during robot runs, the second line is usually whichever built Go2 workspace is active, for example:

```bash
source /home/castej-jetson/workspaces/amigo_ros2_relasense/install/setup.bash
```

For the new YOLOv8 person-follow workflow, also make sure the Isaac ROS workspace has the TensorRT engine:

```bash
ls /home/castej/workspaces/isaac_ros-dev/isaac_ros_assets/models/yolov8/yolov8s.plan
```

If the workspace paths differ on the robot, set `AMIGO_ROS2_WS`, `ISAAC_ROS_WS`, or `YOLO_ENGINE_FILE` before using the startup script below.

## Launch Profiles

`mapping.launch.py` declares all mapping arguments and starts one or both top-level groups based on `launch_profile`.

| Profile | Starts | Use when |
| --- | --- | --- |
| `all` | Mission stack plus RViz/log-pose operator tools | Normal interactive run. This is the default profile. |
| `mission_base` | Mission stack only | Headless robot run or SSH session without RViz. |
| `operator_tools` | RViz plus `log_pose_action_server` only | Mission stack is already running elsewhere. |

## Mapping Workflow

`launch_profile:=all` and `launch_profile:=mission_base` include the mission stack:

1. `mapping_base.launch.py`
   - Publishes the robot description with the RealSense camera mount arguments.
   - Starts `go2_driver_node`, `go2_state`, `odom_node`, `ekf_filter_node`, `sllidar_node`, and `go2_lidar`.
   - Starts the RealSense component container when `realsense_enable:=true`.
   - Optionally starts Isaac Visual SLAM when `vslam_enable:=true`; EKF fusion is still disabled by default.
   - Optionally runs `go2_motion_mode_switcher` when `startup_motion_mode` is not `none`, `off`, or `skip`.

2. `mapping_nav.launch.py`
   - Starts `slam_toolbox`, configures it, then activates it.
   - Starts Nav2 from `nav2_bringup/navigation_launch.py`.
   - Remaps Nav2 `cmd_vel` to `/motion/candidate/nav`.
   - Starts `explore_lite` paused. The search action resumes exploration when the mission begins.

3. `mapping_audio.launch.py`
   - Starts ODAS when `odas_enable:=true`.
   - Starts Vosk STT when `voice_control:=true` and `voice_stt_enable:=true`.
   - Starts `voice_command_node` when `voice_control:=true`.

4. `mapping_behavior.launch.py`
   - Starts the leak search action stack only when `sound_localizer_enable:=true`, `odas_enable:=true`, and `odas_enable_leak_classifier:=true`.
   - Starts `mission_supervisor_node`.
   - Starts person-follow perception and control when `person_follow_enable:=true`.
   - Starts the Unitree follow motion bridge when person-follow is enabled and `person_follow_motion_backend` is not `legacy`.
   - Subscribes person-follow perception to Isaac YOLOv8 detections on `/detections_output`.

YOLOv8 is intentionally launched separately from `mapping.launch.py`. The mapping stack owns the RealSense camera; `yolov8_person_detection.launch.py` only subscribes to the existing `/camera/color/image_raw` and `/camera/color/camera_info` topics and publishes `/detections_output`.

`launch_profile:=all` and `launch_profile:=operator_tools` also start:

- `log_pose_action_server`, saving to `pose_log.json`.
- RViz with `go2_description/config/nav_nvblox_config.rviz`.

## Main Launch Commands

Full mapping mission with voice and RViz:

```bash
ros2 launch go2_bringup mapping.launch.py \
  launch_profile:=all \
  voice_control:=true
```

The same command can omit `launch_profile:=all` because `all` is the default:

```bash
ros2 launch go2_bringup mapping.launch.py voice_control:=true
```

Headless mission stack without RViz/log-pose operator tools:

```bash
ros2 launch src/go2_bringup/launch/mapping.launch.py \
  launch_profile:=mission_base \
  voice_control:=true
```

Recommended full RealSense YOLOv8 person-follow startup from this workspace:

```bash
cd /home/castej/workspaces/amigo_ros2_relasense
scripts/launch_mapping_follow_yolov8.sh \
  launch_profile:=mission_base \
  person_follow_unitree_network_interface:=eno1
```

The script starts two coordinated processes and stops both on shutdown:

- Go2 mapping stack with `person_follow_enable:=true` and `voice_control:=true`.
- Isaac YOLOv8 graph using the existing RealSense color topics and `${ISAAC_ROS_WS}/isaac_ros_assets/models/yolov8/yolov8s.plan`.

Override paths when needed:

```bash
AMIGO_ROS2_WS=/home/castej/workspaces/amigo_ros2_relasense \
ISAAC_ROS_WS=/home/castej/workspaces/isaac_ros-dev \
YOLO_ENGINE_FILE=/home/castej/workspaces/isaac_ros-dev/isaac_ros_assets/models/yolov8/yolov8s.plan \
scripts/launch_mapping_follow_yolov8.sh launch_profile:=mission_base
```

Operator tools only, when the mission stack is already running:

```bash
ros2 launch go2_bringup mapping.launch.py launch_profile:=operator_tools
```

Capture a run log:

```bash
ros2 launch go2_bringup mapping.launch.py \
  launch_profile:=mission_base \
  voice_control:=true \
  2>&1 | tee mission_log.txt
```

## Debug Launch

Use this when tracing odometry, voice parsing, search behavior, or leak classification:

```bash
ros2 launch go2_bringup mapping.launch.py \
  launch_profile:=all \
  voice_control:=true \
  debug_odometry:=true \
  search_debug:=true \
  voice_debug:=true \
  voice_command_debug:=true \
  odas_leak_classifier_debug:=true \
  odas_log_level:=debug
```

## Leak Search

After launch, `explore_lite` starts paused. Start the mission by saying:

```text
hey amigo, look for a leak
```

To test without voice, send the public search action directly:

```bash
ros2 action send_goal /search go2_interfaces/action/Search \
  "{initial_pose: {header: {frame_id: 'map'}, pose: {orientation: {w: 1.0}}}, behavior_tree: ''}"
```

Useful action checks:

```bash
ros2 action info /search
ros2 action info /explore_until_detected
ros2 action info /localize_detected_leak
```

## Person Follow

Person-follow now uses Isaac ROS YOLOv8 detections plus RealSense aligned depth. The mapping stack still launches and owns the RealSense camera; YOLOv8 runs as a separate graph that subscribes to `/camera/color/image_raw` and `/camera/color/camera_info`.

The default Unitree follow backend is `sport`, with `person_follow_unitree_gait:=static_walk`. That matches this workspace's stock startup gait (`startup_motion_gait:=static_walk`) and avoids enabling Unitree `FreeAvoid` when follow mode starts. Use `person_follow_unitree_gait:=economic` if you want the economic gait instead.

Recommended one-command launch:

```bash
cd /home/castej/workspaces/amigo_ros2_relasense
scripts/launch_mapping_follow_yolov8.sh \
  launch_profile:=mission_base \
  person_follow_unitree_network_interface:=eno1
```

After startup, say:

```text
hey amigo, follow me
```

Stop follow mode with:

```text
hey amigo, stop following
```

The follow adapter defaults to YOLOv8 COCO person class `0`:

```bash
ros2 launch go2_bringup mapping.launch.py \
  voice_control:=true \
  person_follow_enable:=true \
  person_follow_target_class_id:=0 \
  person_follow_motion_backend:=sport \
  person_follow_unitree_gait:=static_walk \
  person_follow_unitree_network_interface:=eno1
```

That command only starts mapping/follow control. It must be paired with the YOLOv8 graph below unless you use `scripts/launch_mapping_follow_yolov8.sh`.

Manual two-terminal launch, useful for debugging:

Terminal 1, Go2 mapping stack:

```bash
cd /home/castej/workspaces/amigo_ros2_relasense
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch src/go2_bringup/launch/mapping.launch.py \
  launch_profile:=mission_base \
  voice_control:=true \
  person_follow_enable:=true \
  person_follow_motion_backend:=sport \
  person_follow_unitree_gait:=economic \
  person_follow_unitree_network_interface:=eno1
```

Terminal 2, Isaac YOLOv8 graph:

```bash
cd /home/castej/workspaces/amigo_ros2_relasense
export ISAAC_ROS_WS=/home/castej/workspaces/isaac_ros-dev
source /var/lib/isaac-ros-cli/isaac-ros/bin/activate
source /opt/ros/jazzy/setup.bash
source ${ISAAC_ROS_WS}/install/setup.bash
source install/setup.bash
ros2 launch src/go2_bringup/launch/yolov8_person_detection.launch.py \
  engine_file_path:=${ISAAC_ROS_WS}/isaac_ros_assets/models/yolov8/yolov8s.plan
```

Do not launch Isaac's `realsense_mono_rect` fragment for this workflow; `mapping_base.launch.py` already starts the RealSense node. The startup script and manual debugging commands use launch-file paths instead of `ros2 launch go2_bringup ...` so an Isaac workspace that also contains a `go2_bringup` package cannot shadow this workspace's launch files.

Use the economic gait with the default plain Sport backend:

```bash
scripts/launch_mapping_follow_yolov8.sh \
  launch_profile:=mission_base \
  person_follow_motion_backend:=sport \
  person_follow_unitree_gait:=economic \
  person_follow_unitree_network_interface:=eno1
```

Use Unitree avoidance backends only when you explicitly want them. `sport_free_avoid` calls `SportClient::FreeAvoid(true)` and can change the robot into Unitree's avoidance/AI gait; `obstacles_avoid` uses the Unitree ObstaclesAvoid service.

```bash
scripts/launch_mapping_follow_yolov8.sh \
  launch_profile:=mission_base \
  person_follow_motion_backend:=sport_free_avoid \
  person_follow_unitree_gait:=none \
  person_follow_unitree_network_interface:=eno1
```

Use the legacy local-costmap safety path without the Unitree follow motion bridge:

```bash
scripts/launch_mapping_follow_yolov8.sh \
  launch_profile:=mission_base \
  person_follow_motion_backend:=legacy
```
launch_profile:=mission_base \
Start the base stack in a specific Unitree motion mode/gait before follow is enabled:

```bash
scripts/launch_mapping_follow_yolov8.sh \
  person_follow_unitree_network_interface:=eno1 \
  startup_motion_mode:=normal \
  startup_motion_gait:=economic
```

Supported startup motion modes are `normal`, `sport_mode`, `ai`, `ai_sport`, `release`, and `none`.
Supported startup and follow gaits are `static_walk`, `economic`, `classic_walk`, `free_walk`, `walk_upright`, `trot_run`, and `none`.

## Topics To Watch

Voice and mission:

```bash
ros2 topic echo /voice/transcript
ros2 topic echo /voice/debug
ros2 topic echo /search/_action/status
```

Exploration:

```bash
ros2 topic echo /explore/status
ros2 topic echo /explore/resume
```

Leak detection and localization:

```bash
ros2 topic echo /leak_detected
ros2 topic echo /doa_angle
ros2 topic echo /sound_localizer/estimate_valid
ros2 topic echo /sound_localizer/estimate_stable
ros2 topic echo /sound_localizer/current_estimate
ros2 topic echo /sound_localizer/estimated_locations
ros2 topic echo /sound_localizer/markers
```

Navigation and map:

```bash
ros2 topic echo /map
ros2 topic echo /scan
ros2 topic echo /plan
ros2 topic echo /local_costmap/costmap
ros2 topic echo /global_costmap/costmap
ros2 topic echo /tf
```

Person follow and YOLOv8:

```bash
ros2 topic info /detections_output
ros2 topic echo /detections_output
ros2 topic echo /person_follow_vision_node/target_point
ros2 topic echo /person_follow_vision_node/target_visible
ros2 topic echo /person_follow_vision_node/target_id
ros2 topic echo /person_follow_vision_node/status
ros2 topic echo /person_follow_controller_node/state
ros2 topic echo /person_follow_controller_node/event
ros2 topic echo /person_follow_controller_node/nominal_twist
ros2 topic echo /person_follow_controller_node/debug_twist
ros2 topic echo /person_follow_controller_node/desired_standoff_point
ros2 topic echo /person_follow_controller_node/safety_status
```

## Current Notes

- `voice_control` defaults to `false`; pass `voice_control:=true` for voice commands and Vosk STT.
- `person_follow_enable` defaults to `false`; the startup script passes `person_follow_enable:=true` automatically.
- `person_follow_target_class_id` defaults to `0`, the YOLOv8 COCO person class.
- `person_follow_motion_backend` defaults to `sport`, not `sport_free_avoid`, so follow mode does not enable Unitree FreeAvoid/AI gait by default.
- `person_follow_unitree_gait` defaults to `static_walk`; set it to `economic` for economic gait or `none` to leave the current gait untouched.
- `realsense_enable` defaults to `true`; do not launch a second RealSense source from Isaac examples.
- `odas_enable`, `odas_enable_leak_classifier`, and `sound_localizer_enable` default to `true`.
- ZED-specific arguments such as `zed_follow_params_path` are not part of the current `mapping.launch.py` workflow.
- `voice_speaker_enable` is not declared by the current mapping launch arguments.
