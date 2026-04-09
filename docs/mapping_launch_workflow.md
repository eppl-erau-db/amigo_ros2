# `mapping.launch.py` Workflow Guide

This guide explains how `src/go2_bringup/launch/mapping.launch.py` works, what it can do, which files implement each part of the system, which launch commands are useful in practice, and which topics/actions/services are worth watching when you debug it.

This write-up is based on the launch files, nodes, configs, and supporting code currently in this workspace.

## 1. What `mapping.launch.py` is for

`mapping.launch.py` is the main mission bringup for:

- Go2 base bringup on real hardware
- SLAM-based mapping
- Nav2 path planning and frontier exploration
- Acoustic leak detection and leak localization
- Optional voice control and optional speaker verification
- Person-follow behavior
- Operator tools like RViz and pose logging

At a high level it combines four mission subsystems plus an operator tools group:

```text
mapping.launch.py
|
+- mission_base_group
|  |
|  +- mapping_base.launch.py
|  +- mapping_nav.launch.py
|  +- mapping_audio.launch.py
|  +- mapping_behavior.launch.py
|
+- operator_tools_group
   |
   +- log_pose_action_server
   +- rviz2
```

The top-level launch file uses `launch_profile` to decide which groups run:

- `launch_profile:=all`
  Runs mission base plus operator tools
- `launch_profile:=mission_base`
  Runs only the mission stack
- `launch_profile:=operator_tools`
  Runs only RViz plus pose logging

## 2. The main capabilities

When launched with defaults, the stack is capable of:

- Publishing the robot model and joint state so TF and RViz work
- Running the Unitree Go2 base driver
- Bridging raw Go2 state, lidar, and odometry into the topics expected by the rest of the stack
- Fusing odometry and IMU with `robot_localization`
- Running the ZED camera with person detection enabled
- Running 2D lidar into `/scan`
- Running `slam_toolbox` in mapping mode
- Running Nav2 with the Go2-specific MPPI controller config
- Running `explore_lite`, but starting exploration paused until the mission logic resumes it
- Running ODAS for source separation / direction-of-arrival estimation
- Classifying leak-like sounds and publishing `/leak_detected` plus `/doa_angle`
- Converting leak bearings into map-frame location estimates via `sound_localizer`
- Executing a two-phase leak search action:
  exploration until a leak is detected, then baseline motion until a stable estimate is available
- Running mission supervision for task mode, posture mode, search control, and motion routing
- Running person-follow perception and follow control
- Optionally running offline Vosk speech-to-text
- Optionally parsing voice commands into supervisor commands
- Optionally gating voice commands with WeSpeaker speaker verification

Important default behavior:

- Voice is off by default because `voice_control:=false`
- ODAS and leak search are on by default because `odas_enable:=true`, `odas_enable_leak_classifier:=true`, and `sound_localizer_enable:=true`
- Person-follow is on by default because `person_follow_enable:=true`
- Operator tools are on by default because `launch_profile:=all`

## 3. Launch-tree walkthrough

### 3.1 `mapping.launch.py`

File:

- `src/go2_bringup/launch/mapping.launch.py`

What it does:

- Declares all shared launch arguments from `_mapping_common.py`
- Includes the four sub-launch files
- Creates the `operator_tools_group`
- Starts `rviz2` with the Go2 RViz config from `go2_description`
- Starts `log_pose_action_server`

### 3.2 `_mapping_common.py`

File:

- `src/go2_bringup/launch/_mapping_common.py`

What it does:

- Defines the complete top-level argument catalog
- Resolves default config paths from package shares
- Locates the Vosk model directory if one is bundled in the workspace
- Parses the Nav2 config to derive:
  `allow_unknown`, `clearance_radius_m`, `local_inflation_radius_m`, and `global_inflation_radius_m`
- Builds the `launch_profile` conditions used by the top-level launch

This file matters because the leak-localization action server does not hardcode its clearance behavior. It derives that behavior from `go2_description/config/nav2_mppi_controller.yaml`, which keeps localization motion consistent with the actual Nav2 footprint and inflation settings.

### 3.3 `mapping_base.launch.py`

File:

- `src/go2_bringup/launch/mapping_base.launch.py`

What it launches:

- `robot_state_publisher`
- `go2_control/base_to_base_tf`
- `go2_driver/go2_driver_node`
- `go2_control/go2_state`
- `go2_control/odom_node`
- `robot_localization/ekf_node`
- `zed_wrapper/zed_camera.launch.py`
- `sllidar_ros2/sllidar_node`
- `go2_control/go2_lidar`
- `go2_motion_mode_switcher` as a one-shot startup process

Why it exists:

- It brings up the physical robot interfaces and the sensor/TF skeleton that the rest of the mission stack depends on.

Important supporting code:

- `src/go2_control/go2_control/go2_state.py`
  Converts Unitree `lowstate` into `joint_states`
- `src/go2_control/go2_control/odom_node.py`
  Republishes `/utlidar/robot_odom` as `/utlidar_odom`
- `src/go2_control/go2_control/base_to_base_tf.py`
  Publishes `base_footprint -> base_link`
- `src/go2_control/go2_control/go2_lidar.py`
  Republishes `/utlidar/cloud` as `pointcloud`
- `src/go2_description/config/local_odom_ekf.yaml`
  Fuses `utlidar_odom`, ZED odometry, raw IMU, and ZED IMU
- `src/go2_bringup/config/zed_follow_person.yaml`
  Turns on ZED object detection and tracking for person-follow
- `src/go2_driver/src/go2_motion_mode_switcher.cpp`
  Supports startup motion modes and gaits

Motion switcher notes:

- Valid `startup_motion_mode` values include `none`, `normal`, `sport_mode`, `ai`, `ai_sport`, and `release`
- Valid `startup_motion_gait` values include `static_walk`, `economic`, `classic_walk`, `free_walk`, `walk_upright`, `trot_run`, and `none`

### 3.4 `mapping_nav.launch.py`

File:

- `src/go2_bringup/launch/mapping_nav.launch.py`

What it launches:

- `slam_toolbox/async_slam_toolbox_node`
- `nav2_bringup/navigation_launch.py`
- `explore_lite/explore`

Key behavior:

- `slam_toolbox` runs in mapping mode and remaps `pose` to `/slam_toolbox_pose`
- Nav2 `cmd_vel` is remapped to `/motion/candidate/nav`
  so Nav2 does not directly command the robot
- `explore_lite` starts with `start_paused:=True`
- `explore_lite` publishes status on `explore/status`
- `explore_lite` listens on `explore/resume`

Important custom behavior:

The copy of `explore_lite` in this workspace has been customized so exploration can be started and stopped by the leak search stack:

- `src/m-explore-ros2/explore/src/explore.cpp`
- `src/m-explore-ros2/explore/include/explore/explore.h`

That customization is what makes `ExploreUntilDetected` possible.

Important configs:

- `src/go2_description/config/mapper_params_online_async.yaml`
  `slam_toolbox` mapping config
- `src/go2_description/config/nav2_mppi_controller.yaml`
  Nav2 config with Go2 footprint, local/global costmaps, and MPPI controller

Notable Nav2 config facts:

- Planner `allow_unknown: true`
- Local footprint:
  `[[0.360, 0.200], [0.360, -0.200], [-0.800, -0.200], [-0.800, 0.200]]`
- Local inflation radius: `0.55`
- Global robot radius: `0.30`
- Global footprint padding: `0.2`
- Global inflation radius: `0.55`
- Nav motion is routed through `/motion/candidate/nav`

### 3.5 `mapping_audio.launch.py`

File:

- `src/go2_bringup/launch/mapping_audio.launch.py`

What it launches:

- ODAS launch include, conditionally
- `voice_stt_vosk_node`, conditionally
- `voice_command_node`, conditionally
- `voice_speaker_verifier_node`, conditionally

How it works:

- If `odas_enable:=true`, it includes `odas_ros/launch/odas.launch.xml`
- If `voice_control:=true` and `voice_stt_enable:=true`, it runs Vosk STT on ODAS-separated audio
- If `voice_control:=true`, it runs the voice command parser
- If `voice_control:=true` and `voice_verifier_enable:=true`, it runs speaker verification

Important supporting code:

- `src/go2_control/go2_control/voice_stt_vosk_node.py`
  Offline streaming STT from `AudioFrame` to `/voice/transcript`
- `src/go2_control/go2_control/voice_command_node.py`
  Wake-phrase, dedupe, intent matching, and publishing `/voice/command`
- `src/go2_control/go2_control/voice_speaker_verifier_node.py`
  WeSpeaker embedding comparison and `/voice/speaker_verified` gate
- `src/odas_ros/odas_ros/launch/odas.launch.xml`
  ODAS bringup
- `src/odas_ros/odas_ros/odas_ros/lib_odas_server_node.py`
  Publishes ODAS ROS topics like `ssl`, `sst`, `sst_raw`, and `sss`
- `src/odas_ros/odas_ros/scripts/odas_leak_classifier_node.py`
  Publishes `/leak_detected` and `/doa_angle`

Voice command model:

- STT publishes `/voice/transcript`
- Command parser consumes the transcript
- Parser publishes normalized tokens on `/voice/command`
- The mission supervisor consumes `/voice/command`

Default voice command groups:

- `search`
- `follow`
- `sport_test`

Default command tokens:

- `search`
- `follow_me`
- `stop_follow`
- `shake_hand`
- `stand_up`
- `lay_down`

Important caveat:

- `voice_speaker_verifier_node.py` currently subscribes to `doa_topic` as `std_msgs/Float32`
- The ODAS leak classifier publishes `/doa_angle` as `std_msgs/Int32`
- So if `doa_topic:=/doa_angle` is left as-is, `/voice/speaker_direction` will not get data from the leak classifier unless another compatible publisher exists

### 3.6 `mapping_behavior.launch.py`

File:

- `src/go2_bringup/launch/mapping_behavior.launch.py`

What it launches:

- `explore_until_detected_action_server`
- `localize_detected_leak_action_server`
- `search_action_server`
- `sound_localizer`
- `mission_supervisor_node`
- `person_follow_vision_node`
- `person_follow_controller_node`
- `person_follow_motion_bridge_node`, conditionally

Conditional behavior:

- The leak stack only launches when:
  `sound_localizer_enable:=true`, `odas_enable:=true`, and `odas_enable_leak_classifier:=true`
- The Unitree follow motion bridge only launches when:
  `person_follow_enable:=true` and `person_follow_motion_backend!=legacy`

Important supporting code:

- `src/go2_control/go2_control/mission_supervisor_node.py`
- `src/go2_control/go2_control/mission_supervisor_core.py`
- `src/go2_control/go2_control/behavior_registry.py`
- `src/go2_control/go2_control/search_action_server.py`
- `src/go2_control/go2_control/explore_until_detected_action_server.py`
- `src/go2_control/go2_control/localize_detected_leak_action_server.py`
- `src/go2_control/go2_control/sound_localizer.py`
- `src/go2_control/go2_control/person_follow_controller_node.py`
- `src/go2_control/go2_control/person_follow_controller_core.py`
- `src/go2_person_follow/src/person_follow_vision_node.cpp`
- `src/go2_driver/src/person_follow_motion_bridge_node.cpp`

## 4. The actual mission workflows

### 4.1 Base bringup workflow

1. `robot_state_publisher` publishes the URDF and TF tree.
2. `go2_driver_node` talks to the robot.
3. `go2_state` converts `lowstate` into `joint_states`.
4. `odom_node` republishes lidar odometry into `/utlidar_odom`.
5. `ekf_node` fuses odometry and IMU into a cleaner local state estimate.
6. ZED and 2D lidar come up.
7. `go2_motion_mode_switcher` optionally selects a starting motion mode and gait.

### 4.2 Mapping workflow

1. `slam_toolbox` subscribes to `/scan` and builds `/map`.
2. Nav2 starts in mapping mode with localization disabled.
3. Nav2 candidate velocity goes to `/motion/candidate/nav` instead of directly to the base.
4. `explore_lite` starts paused and waits for `explore/resume`.
5. The mission stack decides when exploration should actually run.

### 4.3 Leak search workflow

1. ODAS publishes separated sound sources and source tracks.
2. `odas_leak_classifier_node` analyzes `sst_raw` and `sss`.
3. When it latches a leak, it publishes:
   `/leak_detected=true` and `/doa_angle=<bearing>`
4. `sound_localizer` combines `/doa_angle` with robot pose in `map`.
5. It stores multiple robot/bearing samples and intersects bearing lines.
6. Once several consecutive estimates are spatially consistent, it publishes:
   `/sound_localizer/estimate_stable=true`
7. The mission supervisor can request the `search` action.
8. `search_action_server` decides which phase to run:
   `exploring` or `localizing`
9. `explore_until_detected_action_server` resumes `explore_lite` until a fresh leak is seen.
10. `localize_detected_leak_action_server` waits for map, TF, leak, and a fresh bearing.
11. It plans baseline moves approximately perpendicular to the first bearing.
12. It ranks candidates by achieved perpendicular baseline and path length.
13. It commands Nav2 to execute the best baseline goal.
14. If a stable estimate appears, localization succeeds.
15. If localization fails to stabilize, the mission coordinator can return to exploration and try again.

### 4.4 Mission supervisor workflow

`mission_supervisor_node` is the orchestrator.

It owns:

- Task mode:
  `IDLE`, `FOLLOW`, `SEARCH`
- Posture mode:
  `STANDING`, `LAYING`, transitional states
- Motion routing
- Search start/cancel
- Stand-up / lay-down / hello gestures
- Voice command cooldowns

Routing behavior:

- In `SEARCH`, motion comes from `/motion/candidate/nav`
- In `FOLLOW` with backend `legacy`, follow motion is routed directly to base motion
- In `FOLLOW` with backend `sport_free_avoid` or `obstacles_avoid`, the supervisor routes follow output into `/person_follow/cmd_vel`, and the Unitree motion bridge talks to the SDK backend

### 4.5 Voice workflow

1. ODAS publishes `sss`
2. `voice_stt_vosk_node` turns `sss` into `/voice/transcript`
3. `voice_command_node` applies:
   normalization, wake phrases, dedupe, optional speaker gate, and command matching
4. It publishes `/voice/command`
5. `mission_supervisor_node` accepts or rejects the command and updates robot mode

Wake behavior:

- `hey amigo` and `amigo` arm the parser
- Some commands bypass wake gating:
  stop-style commands and stand-up

### 4.6 Person-follow workflow

1. ZED object detection publishes tracked objects
2. `person_follow_vision_node` chooses a usable person target
3. It publishes:
   target point, visibility, target ID, and status
4. `person_follow_controller_node` transforms the target into the base frame
5. It computes the nominal follow command
6. It optionally runs a local costmap safety oracle
7. It publishes candidate follow motion
8. The supervisor allows that motion only when task mode is `FOLLOW`
9. If backend is non-legacy, `person_follow_motion_bridge_node` sends the result to the Unitree backend

## 5. Accompanying code map

These are the main files you should read if you want to understand the full stack end-to-end:

- `src/go2_bringup/launch/mapping.launch.py`
  Top-level orchestration
- `src/go2_bringup/launch/_mapping_common.py`
  Shared arguments, path resolution, Nav2-derived settings
- `src/go2_bringup/launch/mapping_base.launch.py`
  Base hardware, TF, ZED, lidar, EKF
- `src/go2_bringup/launch/mapping_nav.launch.py`
  SLAM, Nav2, frontier exploration
- `src/go2_bringup/launch/mapping_audio.launch.py`
  ODAS, STT, voice parser, speaker verification
- `src/go2_bringup/launch/mapping_behavior.launch.py`
  Search, sound localization, mission supervisor, follow stack
- `src/go2_control/go2_control/mission_supervisor_node.py`
  Runtime orchestration and motion routing
- `src/go2_control/go2_control/mission_supervisor_core.py`
  Supervisor state machine and transition rules
- `src/go2_control/go2_control/behavior_registry.py`
  Declarative behavior metadata
- `src/go2_control/go2_control/search_action_server.py`
  Explore/localize mission coordinator
- `src/go2_control/go2_control/explore_until_detected_action_server.py`
  Pauses/resumes `explore_lite` based on leak detection
- `src/go2_control/go2_control/localize_detected_leak_action_server.py`
  Baseline-motion leak localization using Nav2
- `src/go2_control/go2_control/sound_localizer.py`
  Map-frame bearing intersection and stability logic
- `src/go2_control/go2_control/voice_stt_vosk_node.py`
  Offline STT
- `src/go2_control/go2_control/voice_command_node.py`
  Transcript-to-command parser
- `src/go2_control/go2_control/voice_speaker_verifier_node.py`
  Speaker verification gate
- `src/go2_control/go2_control/person_follow_controller_node.py`
  Follow control runtime
- `src/go2_control/go2_control/person_follow_controller_core.py`
  Follow math and safety oracle
- `src/go2_person_follow/src/person_follow_vision_node.cpp`
  Person target acquisition from ZED detections
- `src/go2_driver/src/person_follow_motion_bridge_node.cpp`
  Unitree follow backend bridge
- `src/m-explore-ros2/explore/src/explore.cpp`
  Patched frontier exploration control
- `src/odas_ros/odas_ros/launch/odas.launch.xml`
  ODAS launch surface
- `src/odas_ros/odas_ros/odas_ros/lib_odas_server_node.py`
  ODAS publishers
- `src/odas_ros/odas_ros/scripts/odas_leak_classifier_node.py`
  Leak classification and DoA publication
- `src/go2_description/config/nav2_mppi_controller.yaml`
  Nav2 controller, planner, costmap, and planner settings
- `src/go2_description/config/mapper_params_online_async.yaml`
  `slam_toolbox` config
- `src/go2_description/config/local_odom_ekf.yaml`
  EKF config
- `src/go2_bringup/config/zed_follow_person.yaml`
  ZED object-detection config for follow
- `src/go2_control/go2_control/log_pose_action_server.py`
  Pose logging for the operator tools profile

## 6. Copy-paste launch commands

These assume you are running from the workspace root.

### 6.1 Environment setup

```bash
cd /home/castej-jetson/workspaces/amigo_ros2
source /opt/ros/humble/setup.bash
source install/setup.bash
```

If `ros2 launch` complains about a read-only `.ros/log` directory, use:

```bash
export ROS_HOME=/tmp/ros_home
mkdir -p "$ROS_HOME"
```

### 6.2 Most useful launch commands

Default full stack:

```bash
ros2 launch go2_bringup mapping.launch.py
```

Mission stack only, no RViz / operator tools:

```bash
ros2 launch go2_bringup mapping.launch.py launch_profile:=mission_base
```

Operator tools only:

```bash
ros2 launch go2_bringup mapping.launch.py launch_profile:=operator_tools
```

Show the full launch-argument surface:

```bash
ros2 launch go2_bringup mapping.launch.py --show-args
```

Voice-enabled stack:

```bash
ros2 launch go2_bringup mapping.launch.py voice_control:=true
```

Voice-enabled stack with only search commands:

```bash
ros2 launch go2_bringup mapping.launch.py voice_control:=true voice_command_mode:=search
```

Voice-enabled stack with search, follow, and sport-test commands:

```bash
ros2 launch go2_bringup mapping.launch.py voice_control:=true voice_command_mode:=all
```

Voice plus speaker verification:

```bash
ros2 launch go2_bringup mapping.launch.py \
  voice_control:=true \
  voice_verifier_enable:=true \
  speaker_verification_enabled:=true \
  voice_verifier_reference_embedding_path:=/home/castej-jetson/workspaces/amigo_ros2/reference_speaker.npy
```

Debug-heavy mission run:

```bash
ros2 launch go2_bringup mapping.launch.py \
  launch_profile:=mission_base \
  voice_control:=true \
  voice_debug:=true \
  voice_command_debug:=true \
  voice_stt_debug_audio:=true \
  search_debug:=true \
  odas_leak_classifier_debug:=true \
  person_follow_debug:=true \
  odas_visualization:=true \
  odas_log_level:=info
```

Mapping with audio stack disabled:

```bash
ros2 launch go2_bringup mapping.launch.py odas_enable:=false voice_control:=false
```

Mapping with follow disabled:

```bash
ros2 launch go2_bringup mapping.launch.py person_follow_enable:=false
```

Mapping with leak stack disabled but follow kept on:

```bash
ros2 launch go2_bringup mapping.launch.py \
  odas_enable:=false \
  odas_enable_leak_classifier:=false \
  sound_localizer_enable:=false
```

Follow backend set to legacy:

```bash
ros2 launch go2_bringup mapping.launch.py person_follow_motion_backend:=legacy
```

Follow backend set to Unitree `sport_free_avoid`:

```bash
ros2 launch go2_bringup mapping.launch.py person_follow_motion_backend:=sport_free_avoid
```

Follow backend set to Unitree `obstacles_avoid`:

```bash
ros2 launch go2_bringup mapping.launch.py person_follow_motion_backend:=obstacles_avoid
```

Use sim time:

```bash
ros2 launch go2_bringup mapping.launch.py use_sim_time:=true
```

Select a startup motion mode and gait:

```bash
ros2 launch go2_bringup mapping.launch.py \
  startup_motion_mode:=normal \
  startup_motion_gait:=static_walk
```

Alternate startup gait example:

```bash
ros2 launch go2_bringup mapping.launch.py \
  startup_motion_mode:=normal \
  startup_motion_gait:=trot_run
```

Custom Vosk model:

```bash
ros2 launch go2_bringup mapping.launch.py \
  voice_control:=true \
  voice_stt_model_path:=/home/castej-jetson/workspaces/amigo_ros2/models/vosk-model-small-en-us-0.15
```

Custom ZED follow-person params:

```bash
ros2 launch go2_bringup mapping.launch.py \
  zed_follow_params_path:=/home/castej-jetson/workspaces/amigo_ros2/src/go2_bringup/config/zed_follow_person.yaml
```

Custom ODAS config:

```bash
ros2 launch go2_bringup mapping.launch.py \
  odas_configuration_path:=/home/castej-jetson/workspaces/amigo_ros2/install/odas_ros/share/odas_ros/config/odas_jetson_respeaker_sep.cfg
```

### 6.3 Useful runtime control commands

Watch the nodes:

```bash
ros2 node list | sort
```

Watch the actions:

```bash
ros2 action list -t
```

Watch the services:

```bash
ros2 service list | sort
```

Request search through the supervisor:

```bash
ros2 service call /mission_supervisor_node/set_mode go2_interfaces/srv/SetRobotMode "{task_mode: 'SEARCH', posture_mode: '', source: 'cli', reason: 'manual_search', allow_preempt: true}"
```

Request follow through the supervisor:

```bash
ros2 service call /mission_supervisor_node/set_mode go2_interfaces/srv/SetRobotMode "{task_mode: 'FOLLOW', posture_mode: '', source: 'cli', reason: 'manual_follow', allow_preempt: true}"
```

Return to idle:

```bash
ros2 service call /mission_supervisor_node/set_mode go2_interfaces/srv/SetRobotMode "{task_mode: 'IDLE', posture_mode: '', source: 'cli', reason: 'manual_idle', allow_preempt: true}"
```

Lay the robot down:

```bash
ros2 service call /mission_supervisor_node/set_mode go2_interfaces/srv/SetRobotMode "{task_mode: 'IDLE', posture_mode: 'LAYING', source: 'cli', reason: 'manual_lay', allow_preempt: true}"
```

Stand the robot up:

```bash
ros2 service call /mission_supervisor_node/set_mode go2_interfaces/srv/SetRobotMode "{task_mode: 'IDLE', posture_mode: 'STANDING', source: 'cli', reason: 'manual_stand', allow_preempt: true}"
```

Log the current SLAM pose:

```bash
ros2 action send_goal /log_pose go2_interfaces/action/LogPose "{task_type: 'manual_marker'}"
```

## 7. Important launch arguments

These are the direct top-level arguments declared by `_mapping_common.py`.

### 7.1 Core

- `launch_profile`
  Default: `all`
- `use_sim_time`
  Default: `false`

### 7.2 Audio / ODAS

- `odas_enable`
  Default: `true`
- `odas_configuration_path`
  Default: `odas_ros/config/odas_jetson_respeaker_sep.cfg`
- `odas_audio_queue_size`
  Default: `1`
- `odas_visualization`
  Default: `false`
- `odas_force_publish_tf`
  Default: `false`
- `odas_use_echo_cancellation`
  Default: `false`
- `odas_echo_cancelled_signal_topic`
  Default: `ec_signal`
- `odas_enable_leak_classifier`
  Default: `true`
- `odas_leak_classifier_debug`
  Default: `false`
- `odas_doa_zero_offset_deg`
  Default: `129.0`
- `odas_log_level`
  Default: `warn`

### 7.3 Voice

- `voice_control`
  Default: `false`
- `voice_transcript_topic`
  Default: `/voice/transcript`
- `voice_wake_phrase`
  Default: `hey amigo`
- `voice_shake_hand_phrase`
  Default: `hello amigo`
- `voice_search_phrase`
  Default: `look for a leak`
- `voice_follow_phrase`
  Default: `follow me`
- `voice_stop_follow_phrase`
  Default: `stay`
- `voice_stand_up_phrase`
  Default: `stand up`
- `voice_lay_down_phrase`
  Default: `lay down`
- `voice_stt_enable`
  Default: `true`
- `voice_stt_model_path`
  Default: auto-detected bundled Vosk path if present
- `voice_stt_audio_topic`
  Default: `/sss`
- `voice_stt_channel`
  Default: `0`
- `voice_stt_channel_strategy`
  Default: `max_rms`
- `voice_stt_publish_partial`
  Default: `false`
- `voice_stt_debug_audio`
  Default: `false`
- `voice_stt_max_alternatives`
  Default: `3`
- `voice_debug`
  Default: `false`
- `voice_command_debug`
  Default: `false`
- `voice_command_cooldown_s`
  Default: `3.0`
- `voice_command_mode`
  Default: `all`
- `voice_command_topic`
  Default: `/voice/command`
- `speaker_verification_enabled`
  Default: `false`
- `speaker_verification_topic`
  Default: `/voice/speaker_verified`
- `speaker_verification_window_s`
  Default: `10.0`
- `voice_verifier_enable`
  Default: `false`
- `voice_verifier_model_name_or_path`
  Default: `eres2net`
- `voice_verifier_reference_embedding_path`
  Default: empty string
- `voice_verifier_threshold`
  Default: `0.55`
- `voice_verifier_window_duration_s`
  Default: `2.0`
- `voice_verifier_eval_period_s`
  Default: `0.5`
- `voice_verifier_debug`
  Default: `false`

### 7.4 Person follow

- `person_follow_enable`
  Default: `true`
- `person_follow_distance_m`
  Default: `0.75`
- `person_follow_distance_band_m`
  Default: `0.10`
- `person_follow_max_vx_mps`
  Default: `0.60`
- `person_follow_max_vy_mps`
  Default: `0.30`
- `person_follow_max_wz_radps`
  Default: `1.20`
- `person_follow_use_strafe`
  Default: `false`
- `person_follow_candidate_horizon_s`
  Default: `0.80`
- `person_follow_reacquire_timeout_s`
  Default: `1.50`
- `person_follow_sit_on_loss_timeout_s`
  Default: `3.00`
- `person_follow_debug`
  Default: `false`
- `person_follow_motion_backend`
  Default: `sport_free_avoid`
- `person_follow_unitree_cmd_vel_topic`
  Default: `/person_follow/cmd_vel`
- `person_follow_unitree_network_interface`
  Default: empty string
- `person_follow_unitree_command_timeout_s`
  Default: `0.5`
- `zed_follow_params_path`
  Default: `go2_bringup/config/zed_follow_person.yaml`

### 7.5 Mission / search

- `sound_localizer_enable`
  Default: `true`
- `search_debug`
  Default: `false`
- `search_allow_unknown`
  Default: `true`
  Note: deprecated in favor of Nav2-derived settings
- `startup_motion_mode`
  Default: `none`
- `startup_motion_gait`
  Default: `static_walk`
- `startup_motion_wait_s`
  Default: `2.0`
- `startup_motion_retries`
  Default: `10`
- `startup_motion_retry_interval_s`
  Default: `2.0`

There are also inherited arguments from:

- `zed_wrapper/zed_camera.launch.py`
- `nav2_bringup/navigation_launch.py`
- `odas_ros/odas.launch.xml`

For the complete combined surface, use:

```bash
ros2 launch go2_bringup mapping.launch.py --show-args
```

## 8. Topics, actions, and services to debug

This is the most useful operational section if you are trying to figure out why the stack is or is not behaving correctly.

### 8.1 Base / state estimation

- `lowstate`
- `joint_states`
- `/utlidar/robot_pose`
- `/utlidar/robot_odom`
- `/utlidar_odom`
- `/odometry/filtered`
- `/zed/zed_node/odom`
- `imu/data_raw`
- `/zed/zed_node/imu/data`
- `/scan`
- `pointcloud`
- `/tf`
- `/tf_static`

Copy-paste checks:

```bash
ros2 topic hz /scan
ros2 topic echo /utlidar_odom
ros2 topic echo /zed/zed_node/odom
ros2 topic echo /odometry/filtered
```

### 8.2 Mapping / navigation / exploration

- `/map`
- `/map_updates`
- `/slam_toolbox_pose`
- `/motion/candidate/nav`
- `explore/status`
- `explore/resume`
- `/local_costmap/costmap`
- `/global_costmap/costmap`
- `/plan`

Copy-paste checks:

```bash
ros2 topic echo /map --once
ros2 topic echo /slam_toolbox_pose
ros2 topic echo /motion/candidate/nav
ros2 topic echo /local_costmap/costmap --once
ros2 topic echo /global_costmap/costmap --once
ros2 topic echo /explore/status
```

### 8.3 ODAS / audio / leak detection

- `/ssl`
- `/sst`
- `/sst_raw`
- `/sss`
- `/raw`
- `/leak_detected`
- `/doa_angle`
- `/voice/debug`

Why these matter:

- `sst_raw`
  Keeps ODAS source ordering, which the leak classifier uses to align tracked sources with separated audio channels
- `sss`
  Is the separated audio stream used by both STT and speaker verification
- `/leak_detected`
  Is the main trigger that switches the search mission from exploration to localization
- `/doa_angle`
  Is the main leak bearing used by both localization and sound-localizer estimation

Copy-paste checks:

```bash
ros2 topic echo /leak_detected
ros2 topic echo /doa_angle
ros2 topic hz /sss
ros2 topic echo /voice/debug
```

### 8.4 Sound localization

- `/sound_localizer/estimate_valid`
- `/sound_localizer/estimate_stable`
- `/sound_localizer/current_estimate`
- `/sound_localizer/estimated_locations`
- `/sound_localizer/approach_waypoints`
- `/sound_localizer/markers`

Copy-paste checks:

```bash
ros2 topic echo /sound_localizer/estimate_valid
ros2 topic echo /sound_localizer/estimate_stable
ros2 topic echo /sound_localizer/current_estimate
```

### 8.5 Voice pipeline

- `/voice/transcript`
- `/voice/partial`
- `/voice/command`
- `/voice/debug`
- `/voice/speaker_verified`
- `/voice/speaker_score`
- `/voice/speaker_direction`

Copy-paste checks:

```bash
ros2 topic echo /voice/transcript
ros2 topic echo /voice/partial
ros2 topic echo /voice/command
ros2 topic echo /voice/speaker_verified
ros2 topic echo /voice/speaker_score
ros2 topic echo /voice/speaker_direction
```

### 8.6 Mission supervisor and search actions

- `/robot_mode_state`
- `/mission_supervisor_node/event`
- `/motion/candidate/nav`
- `/motion/candidate/follow`
- `/person_follow/cmd_vel`
- `/api/sport/request`

Actions:

- `/search`
- `/explore_until_detected`
- `/localize_detected_leak`
- `/log_pose`

Services:

- `/mission_supervisor_node/set_mode`

Copy-paste checks:

```bash
ros2 topic echo /robot_mode_state
ros2 topic echo /mission_supervisor_node/event
ros2 action list -t
ros2 action info /search
ros2 action info /explore_until_detected
ros2 action info /localize_detected_leak
ros2 service type /mission_supervisor_node/set_mode
```

### 8.7 Person-follow

- `/person_follow_vision_node/target_point`
- `/person_follow_vision_node/target_visible`
- `/person_follow_vision_node/target_id`
- `/person_follow_vision_node/status`
- `/person_follow_vision_node/annotated_image`
- `/person_follow_controller_node/state`
- `/person_follow_controller_node/event`
- `/person_follow_controller_node/debug_twist`
- `/person_follow_controller_node/nominal_twist`
- `/person_follow_controller_node/desired_standoff_point`
- `/person_follow_controller_node/safety_status`
- `/motion/candidate/follow`
- `/person_follow/cmd_vel`
- `/zed/zed_node/obj_det/objects`
- `/zed/zed_node/rgb/image_rect_color`

Copy-paste checks:

```bash
ros2 topic echo /person_follow_vision_node/status
ros2 topic echo /person_follow_vision_node/target_visible
ros2 topic echo /person_follow_vision_node/target_point
ros2 topic echo /person_follow_controller_node/state
ros2 topic echo /person_follow_controller_node/event
ros2 topic echo /person_follow_controller_node/safety_status
ros2 topic echo /motion/candidate/follow
ros2 topic echo /person_follow/cmd_vel
```

### 8.8 Operator tools

- `/slam_toolbox_pose`
- action `/log_pose`
- file `pose_log.json`

Copy-paste checks:

```bash
ros2 action send_goal /log_pose go2_interfaces/action/LogPose "{task_type: 'debug_marker'}"
tail -n 50 pose_log.json
```

## 9. Fast debug playbooks

### 9.1 "The robot maps but never searches for a leak"

Check:

```bash
ros2 topic echo /leak_detected
ros2 topic echo /doa_angle
ros2 action list -t
ros2 topic echo /mission_supervisor_node/event
```

Likely causes:

- `odas_enable:=false`
- `odas_enable_leak_classifier:=false`
- `sound_localizer_enable:=false`
- Search was never requested via voice or service
- `search` action server is not up

### 9.2 "Search starts but never leaves exploration"

Check:

```bash
ros2 topic echo /leak_detected
ros2 topic echo /doa_angle
ros2 topic echo /explore/status
ros2 topic echo /voice/debug
```

Likely causes:

- Leak classifier never latches `/leak_detected`
- `/doa_angle` never updates
- `explore_lite` is not resuming properly

### 9.3 "Localization starts but never stabilizes"

Check:

```bash
ros2 topic echo /sound_localizer/estimate_valid
ros2 topic echo /sound_localizer/estimate_stable
ros2 topic echo /sound_localizer/current_estimate
ros2 topic echo /map --once
ros2 topic echo /robot_mode_state
```

Likely causes:

- No fresh `/doa_angle`
- Bad TF from `map` to `base_link`
- Map unavailable or Nav2 path checks failing
- Baseline motion cannot find reachable goals
- Estimate spread never becomes tight enough

### 9.4 "Voice transcripts appear but commands do not"

Check:

```bash
ros2 topic echo /voice/transcript
ros2 topic echo /voice/command
ros2 topic echo /voice/debug
ros2 topic echo /voice/speaker_verified
```

Likely causes:

- `voice_control:=false`
- Wake phrase not matched
- Command not in the enabled `voice_command_mode`
- Duplicate transcript deduped
- Speaker verification gate is active and not passing

### 9.5 "Follow sees a person but the robot does not move"

Check:

```bash
ros2 topic echo /robot_mode_state
ros2 topic echo /person_follow_vision_node/status
ros2 topic echo /person_follow_controller_node/state
ros2 topic echo /person_follow_controller_node/safety_status
ros2 topic echo /motion/candidate/follow
ros2 topic echo /person_follow/cmd_vel
```

Likely causes:

- Supervisor is not in `FOLLOW`
- Person-follow controller is blocked by the safety oracle
- Follow target is stale or visibility is false
- Non-legacy backend bridge is not enabled

## 10. Bottom line

The shortest mental model is:

- `mapping_base.launch.py` makes the robot and sensors usable
- `mapping_nav.launch.py` makes mapping, planning, and frontier exploration usable
- `mapping_audio.launch.py` makes acoustic sensing and optional voice usable
- `mapping_behavior.launch.py` makes search, supervisor control, sound localization, and follow usable
- `mapping.launch.py` is the composition point that ties them together

If you only remember five debug topics, use these first:

```bash
ros2 topic echo /robot_mode_state
ros2 topic echo /leak_detected
ros2 topic echo /doa_angle
ros2 topic echo /sound_localizer/current_estimate
ros2 topic echo /voice/debug
```
