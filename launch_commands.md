# Amigo (Go2) — launch & debug cheat-sheet

> Source the env first: `source ~/workspaces/amigo_ros2/setup_robot.sh`
> Then the quiet wrapper `amigo_launch` (= `ros2 launch go2_bringup mapping.launch.py …` with the
> harmless DDS type-hash spam filtered). `amigo_log` also tees a clean `./amigo_run.log`.

---

## 1. Normal launch

```bash
amigo_launch                       # full stack + RViz (launch_profile defaults to "all")
```

Equivalent explicit form:

```bash
ros2 launch go2_bringup mapping.launch.py launch_profile:=all voice_control:=true
```

Profiles:

```bash
# full mission stack WITHOUT RViz / log-pose tools:
ros2 launch go2_bringup mapping.launch.py launch_profile:=mission_base voice_control:=true
# RViz + operator tools only (mission stack already running elsewhere):
ros2 launch go2_bringup mapping.launch.py launch_profile:=operator_tools
```

Defaults already on: `voice_control:=true`, `person_follow_enable:=true`, `swag_enable:=true`,
`arm_enable:=true`, `arm_dry_run:=true`, `command_mode:=all` (every voice group enabled).

---

## 2. Voice commands (all wake-gated by "hey amigo" / "amigo")

| Say | Does |
|---|---|
| hey amigo, stand up / lay down | posture |
| hello amigo | wave (shake hand) |
| hey amigo, follow me  /  stop following ("stay") | person-follow on/off |
| hey amigo, look for a leak | autonomous leak search |
| **hey amigo, let's explore the area** | start a manual-drive mapping session (drive with the remote) |
| **hey amigo, we are done exploring** | save map + ArUco markers, return to idle |
| **hey amigo, deliver swag** | run the pickup → deliver → dropoff mission |
| **hey amigo, all done** | (during a delivery) hand-off finished → go return/drop-off the basket |

Short forms without the verb also work: "explore the area", "done exploring", "deliver swag",
"all done". You can say "hey amigo" then the phrase within ~8 s, or both together.

---

## 3. Explore + deliver swag — full flow

**Same session (simplest):**
1. `amigo_launch`
2. "hey amigo, let's explore the area" → drive the venue with the Unitree remote so the ZED sees
   each ArUco marker.
3. "hey amigo, we are done exploring" → saves `~/amigo_maps/venue.{yaml,pgm,posegraph,data}` +
   `~/amigo_maps/venue.aruco.yaml`.
4. "hey amigo, deliver swag" → robot navigates to the pickup marker, fine-aligns, runs the pickup
   arm script, goes to the delivery marker, runs the deliver script, then waits.
5. "hey amigo, all done" → robot returns to the pickup marker and runs the dropoff script.

**Cross-session (after a reboot / fresh launch):**
```bash
amigo_launch slam_map_file:=~/amigo_maps/venue
# set the initial pose once in RViz (2D Pose Estimate), then "hey amigo, deliver swag"
```

**Where things are saved:** `~/amigo_maps/` (arg `swag_maps_dir`), base name `venue`
(arg `swag_map_name`).

### Testing the delivery WITHOUT the arm mounted
Skip the arm entirely — the mission waits ~3 s at each pickup/deliver/dropoff step instead of
calling the arm — so you can verify nav + alignment + the whole flow first:

```bash
amigo_launch deliver_use_arm:=false swag_debug:=true        # optionally arm_enable:=false too
```

Flip back to `deliver_use_arm:=true` (default) once the arm is on the dog. Adjust the wait with
`deliver_arm_stub_wait_s:=3.0`.

### Before the first REAL run (integration)
- Print **DICT_6X6_100** markers; set the measured size and ids:
  ```bash
  amigo_launch aruco_marker_size_m:=0.15 deliver_pickup_marker_id:=0 deliver_delivery_marker_id:=1
  ```
- Record the three arm trajectories (needs `pip install gs_usb` + the CAN dongle):
  ```bash
  ros2 run go2_arm arm_record --name pickup  --dir ~/amigo_arm_scripts
  ros2 run go2_arm arm_record --name deliver --dir ~/amigo_arm_scripts
  ros2 run go2_arm arm_record --name dropoff --dir ~/amigo_arm_scripts
  ```
- Keep `arm_dry_run:=true` (default) to rehearse the whole mission with the arm simulated, then
  flip `arm_dry_run:=false` to drive the real arm.

Full guide: [`docs/EXPLORE_DELIVER_SWAG.md`](docs/EXPLORE_DELIVER_SWAG.md).

---

## 4. Debug launch flags

```bash
amigo_launch \
  swag_debug:=true \              # verbose logs from aruco detector, recorder, deliver server, arm
  search_debug:=true \
  voice_debug:=true \
  voice_command_debug:=true \
  odas_leak_classifier_debug:=true
```

Other handy swag/deliver overrides (defaults in parentheses):

```bash
amigo_launch \
  aruco_image_topic:=/zed/zed_node/rgb/image_rect_color \   # (verify your wrapper's topic)
  aruco_camera_info_topic:=/zed/zed_node/rgb/camera_info \
  aruco_detect_rate_hz:=5.0 \
  swag_map_name:=venue \
  swag_maps_dir:=~/amigo_maps
```

Deliver-server tuning is on the node (servo gains/tolerances, standoffs, timeouts):
`ros2 param list /deliver_swag_action_server`.

---

## 5. Topics / actions / services to watch

### Explore + deliver
```bash
ros2 topic echo /voice/command                      # the parsed command token
ros2 topic echo /voice/debug                         # supervisor + voice JSON events (explore_started,
                                                     #   deliver_dispatch_*, explore_save_complete, handoff_*)
ros2 topic echo /robot_mode_state                    # task_mode flips to EXPLORE / DELIVER
ros2 topic echo /aruco/markers_map                   # detected markers in the MAP frame (recording/staging)
ros2 topic echo /aruco/markers_base                  # detected markers in the BASE frame (the live servo)
ros2 action list | grep deliver_swag
ros2 action info /deliver_swag                       # feedback .stage = nav_to_pickup / aligning_* / arm_* / await_handoff
ros2 service list | grep -E "play_script|save_map|handoff"
```

RViz: add a **MarkerArray** display on `/aruco/markers_map` to see where markers were detected,
and `/aruco/markers_base` to watch the live alignment target. The `aruco_<id>` TF frames also show.

### Direct (no-voice) testing
```bash
# Save the explore map/markers without saying "done exploring":
ros2 service call /explore/save_map go2_interfaces/srv/SaveExploreMap "{map_name: 'venue'}"

# Trigger the arm directly (dry-run by default):
ros2 service call /arm/play_script go2_interfaces/srv/PlayArmScript "{script: 'pickup', speed: 0.0}"

# Run the delivery mission without voice:
ros2 action send_goal /deliver_swag go2_interfaces/action/DeliverSwag "{map_name: ''}" --feedback

# Signal hand-off without voice:
ros2 service call /deliver/handoff_done std_srvs/srv/Trigger
```

### Navigation / map (shared)
```bash
ros2 topic echo /map            # SLAM occupancy grid
ros2 run tf2_ros tf2_echo map base_link    # confirm the robot is localized in the map
ros2 topic echo /local_costmap/costmap
ros2 topic echo /plan
```

### Leak search (existing)
```bash
ros2 topic echo /voice/debug
ros2 topic echo /leak_detected
ros2 topic echo /doa_angle
ros2 topic echo /sound_localizer/current_estimate
ros2 action info /search
```
Run the leak search without voice:
```bash
ros2 action send_goal /search go2_interfaces/action/Search \
  "{initial_pose: {header: {frame_id: 'map'}, pose: {orientation: {w: 1.0}}}, behavior_tree: ''}"
```

### Person-follow (existing)
```bash
ros2 topic echo /person_follow_vision_node/target_point
ros2 topic echo /person_follow_vision_node/target_visible
ros2 topic echo /person_follow_controller_node/state
ros2 topic echo /person_follow_controller_node/debug_twist
ros2 topic echo /person_follow_controller_node/safety_status
```
Backends:
```bash
amigo_launch person_follow_motion_backend:=obstacles_avoid person_follow_unitree_network_interface:=enP2p1s0
amigo_launch person_follow_motion_backend:=sport_free_avoid
amigo_launch person_follow_motion_backend:=legacy
```

---

## 6. Build

```bash
source setup_robot.sh
# first time / after adding interfaces or new console_scripts:
colcon build --packages-select go2_interfaces go2_arm go2_control --symlink-install
# editing EXISTING python nodes / launch / Vosk grammar is live on next launch (symlink-install).
colcon test --packages-select go2_control go2_arm --event-handlers console_direct+
```

---

## 7. Notes & TODO (pre-existing, kept for reference)

- Wanted launch defaults: `voice_control:=true` ✅, `person_follow_enable:=true` ✅, RViz on by
  default ✅ (`launch_profile:=all` includes operator_tools), non-AI gait at startup.
- **AI gait stutter / weak yaw** (open): the new AI gait stutters and seems to lack the force to
  yaw in place — sticks trying to turn. Keep `startup_motion_gait:=static_walk` (or economic) for
  now; the static/endurance gait is the reliable one. (Still TODO: research a fix / give it more
  yaw authority.)
- `person_follow_unitree_network_interface` is `enP2p1s0` on the Jetson Thor (was `eno1`/`enp*` on
  older hosts).
- This file supersedes `launch_commands.txt` (kept as a backup).
