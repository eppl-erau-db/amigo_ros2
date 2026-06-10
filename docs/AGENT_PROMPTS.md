# Onboarding prompts for AI coding agents (Amigo / Go2)

Copy one of the prompts below into a **fresh Claude Code (or other coding-agent) session** to get
it up to speed on this robot before you ask it to do anything. Fill in the `<...>` placeholder at
the bottom of whichever prompt you use.

- **Prompt 1 — Debugging / solving issues:** for diagnosing a symptom (no voice, won't navigate,
  map won't build, a node crashes, etc.).
- **Prompt 2 — Adding capabilities / behaviors:** for building a new voice-triggered behavior. Pairs
  with [`../src/go2_control/ADDING_BEHAVIORS.md`](../src/go2_control/ADDING_BEHAVIORS.md), the
  canonical step-by-step guide.

> **These prompts are living documents.** If, while working, an agent learns something broadly
> useful for *future* agents — a new gotcha, a pipeline/topic fact, a build nuance, a hardware quirk
> — it should **append it to the relevant prompt below** (and, for durable facts, to the auto-memory
> at `~/.claude/projects/-home-castej-workspaces-amigo-ros2/memory/`). Keep them tight: add real,
> verified context, prune anything that turns out wrong.

---

## Prompt 1 — Debugging / solving issues

```
You are debugging "Amigo," a voice-controlled Unitree Go2 quadruped. Stack: ROS 2 Jazzy on a
Jetson Thor AGX (Ubuntu 24.04, Python 3.12, aarch64). It runs Nav2 (MPPI controller +
SmacPlanner2D + behavior/collision servers), slam_toolbox (2D SLAM), explore_lite (frontier
exploration), an ODAS mic-array + Vosk voice pipeline, and a ZED 2i camera. A mission_supervisor
state machine turns voice commands into behaviors (stand/lay/wave/follow, and "look for a leak" =
autonomous explore + sound-source localization). Workspace: /home/castej/workspaces/amigo_ros2.

BEFORE YOU START
- Your MEMORY.md index is auto-loaded. OPEN the files it links — especially
  next-steps-debugging.md (active resume point + past root causes), jetson-thor-hardware.md
  (hardware quirks), robot-launch-setup.md, mapping-launch-workflow.md. They hold hard-won
  context. As you learn non-obvious facts or fix things, UPDATE these memory files.
- Run `source setup_robot.sh` to set the ROS environment.

BUILD / ITERATION MODEL (important)
- colcon --symlink-install. Launch files (src/go2_bringup/launch/*), YAML/cfg
  (src/go2_description/config/*, src/odas_ros/.../config/*), and Python nodes (src/go2_control/*
  via egg-link) are LIVE on the next launch — NO rebuild. Confirm with
  `readlink -f install/<pkg>/share/.../<file>`.
- Only these need `colcon build`: C++ (src/go2_driver), changed interfaces (src/go2_interfaces),
  and NEW setup.py console_scripts.

YOU CANNOT RUN THE ROBOT — the user does. Propose changes, then have the user relaunch
(`ros2 launch go2_bringup mapping.launch.py odas_log_level:=info odas_leak_classifier_debug:=true`)
and share the log (saved to nav2_test.txt). Verify against real logs/topics; never assume a fix works.

READING THE LOG (~2 MB, ~90% benign noise)
- Denoise first: sed -E 's/\x1b\[[0-9;]*m//g' nav2_test.txt | grep -avE "Failed to parse type hash" > /tmp/clean.txt
  (the cyclonedds "Failed to parse type hash" lines are harmless Unitree-DDS spam.)
- Get the run's time span, then grep \[(WARN|ERROR|FATAL)\]. "process has died ... exit code -2"
  is SIGINT from the user's Ctrl-C (benign); exit -11/-6 MID-run are real crashes; at shutdown
  they're usually benign teardown.

LAUNCH STRUCTURE: mapping.launch.py includes mapping_base (drivers, EKF, the two lidars, ZED),
mapping_nav (nav2 + slam_toolbox + explore_lite), mapping_audio (ODAS + Vosk STT + voice_command),
mapping_behavior (mission_supervisor + behavior nodes). _mapping_common.py defines all launch args.

PIPELINES & KNOWN GOTCHAS (check per symptom)
- No voice → audio chain: ReSpeaker → ODAS → /sss → voice_stt_vosk_node → /voice/transcript →
  voice_command_node → /voice/command → mission_supervisor. The ReSpeaker's ALSA card index is
  UNSTABLE across reboots (`arecord -l`; the launch auto-detects it by name). Check /sss & /sst_raw
  flowing, leak_classifier ACQUIRE lines, and Transcript: lines.
- Won't move / hits obstacles → costmaps + controller (nav2_mppi_controller.yaml). LOCAL costmap =
  /scan ObstacleLayer + a 3D STVL `lidar3d_layer` fed by the **Unitree L1 raw `/utlidar/cloud_base`**
  (source `front3d_go2`, frame base_link; `update_footprint_enabled:true` clears the self-returns).
  GLOBAL = static_layer from the SLAM /map only (camera/3D-lidar are NOT global sources — depth noise
  would leave permanent phantom walls in the persistent map). GOTCHAs: footprint_padding STACKS on
  robot_radius = the inscribed (hard-blocking) radius (inflation_radius is only a soft gradient); MPPI
  must be motion_model: DiffDrive (the Go2 doesn't strafe under Nav2 Twist); reverse is ENABLED
  (vx_min -0.25, mirrored in velocity_smoother min_velocity), guarded by the 360° /scan.
- "Failed to make progress" loop while the planner SUCCEEDS = LOCAL costmap / MPPI, not the planner.
  Signature: controller logs "Passing new path" ~1/s but the robot doesn't move, then "Failed to make
  progress"→"Optimizer reset"→"Aborting handle" on a ~15s cycle (= progress_checker
  movement_time_allowance). Zero planner failures → the global route is fine; the robot is boxed in
  the LOCAL costmap. Confirm via bt_navigator "current location" deltas (stuck = crawls <~1.3m;
  healthy = advances metres). ROOT CAUSE seen 2026-06-05: the L1 STVL layer painted a PHANTOM OBSTACLE
  RING (floor returns leaking in during the trot pitch + slow voxel decay accumulating them) → MPPI
  ObstaclesCritic (consider_footprint, collision_cost 10000) found no forward path. FIXED by STVL
  TUNING, not removal: voxel_decay 1.0, observation_persistence 0.0, min_z/min_obstacle_height 0.10,
  tight obstacle_range. DEBUG: lidar3d_layer publish_voxel_map:true → watch /local_costmap/voxel_grid
  in RViz for a lethal ring in open space.
- collision_monitor (nav2_mppi_controller.yaml) watches `/scan` AND the L1 `/utlidar/cloud_base`
  (source `l1_cloud`, **type: "pointcloud"** — NOT "PointCloud2"; that's the costmap's data_type field
  and a wrong type here ABORTS the whole Nav2 bringup). The L1 catches LOW/close obstacles the high 2D
  /scan misses; min_height 0.10 drops the floor (base_footprint is level so no pitch-phantoms).
  IMPORTANT: feed it a cloud whose self-returns are gone — raw `/utlidar/cloud_base` works because the
  Unitree firmware already excludes the body/legs (visually confirmed); collision_monitor has NO
  footprint-clearing, so a cloud WITH legs would latch a permanent self-collision (that was the role of
  the now-unused go2_lidar.py self-box). Only an `approach` polygon (SLOWS, never hard-stops);
  "Robot to approach"↔"continue normal operation" pairs are normal, and a high count is a SYMPTOM of
  dwelling near walls, not a cause. Benign one-shot startup noise to ignore: planner "Inflation layer
  ... non-circular collision checking" (global costmap is CIRCULAR via robot_radius → Smac uses radius
  checking; do NOT lower global cost_scaling_factor to silence it — reopens the doorway-closing
  regression); bt_navigator "Error_code parameters were not set"; controller "No current_goal/progress
  checker specified".
- Map won't build → slam_toolbox rejecting scans ("LaserRangeScan contains N ... expected M") =
  variable-length scans from angle_compensate:False; SLAM needs fixed-length (True). Two lidars:
  RPLidar /scan (frame laser, drives SLAM); Unitree L1 /utlidar/cloud_base (frame base_link, firmware
  self-excluded) used DIRECTLY for 3D obstacles in the local costmap + collision_monitor (the
  go2_lidar.py republisher is unused).
- TF chain: map→odom (slam) → base_footprint (EKF) → base_link (base_to_base_tf) → sensors. A red
  RobotModel in RViz is usually a missing mesh — cosmetic.
- Motion routing: Nav2 cmd_vel → /motion/candidate/nav → mission_supervisor arbitration → cmd_vel
  → go2_driver.

METHOD: reproduce the symptom in the denoised log → trace the relevant pipeline → confirm with the
actual params/topics/TF/source (cite file:line + exact log lines) → for broad or uncertain
investigations, fan out Explore subagents or a Workflow and ADVERSARIALLY VERIFY the root cause
before committing (a header check overturned a wrong nav2 assumption once) → propose a minimal fix →
give concrete on-robot verification steps. Use AskUserQuestion for genuine either/or decisions;
confirm before anything destructive or outward-facing. After a confirmed fix, update memory.

KEEP THIS PROMPT FRESH: if you discover something broadly useful for future debugging sessions
(a new gotcha, topic, build nuance, hardware quirk), append it to this prompt in
docs/AGENT_PROMPTS.md so the next agent inherits it.

MY ISSUE: <describe the symptom; point to the latest nav2_test.txt>
```

---

## Prompt 2 — Adding capabilities / behaviors

```
You are adding a new capability/behavior to "Amigo," a voice-controlled Unitree Go2 quadruped
(ROS 2 Jazzy, Jetson Thor AGX). Pipeline: voice → Vosk STT → voice_command_node →
mission_supervisor state machine → behavior nodes → robot. The supervisor owns ALL state; behavior
nodes are passive and act only when enabled via RobotModeState or action goals. Workspace:
/home/castej/workspaces/amigo_ros2.

START HERE
- READ src/go2_control/ADDING_BEHAVIORS.md FIRST. It is the canonical guide: full step-by-step
  checklist (behavior_registry → mission_supervisor_core → mission_supervisor_node →
  voice_command_node → behavior node → launch wiring → setup.py entry point → tests) plus a Robot
  Capabilities Reference (motion, Sport API IDs, perception, TF). Follow its checklist exactly.
- Your MEMORY.md index is auto-loaded. OPEN the files it links — especially
  mapping-launch-workflow.md (where behaviors plug into the launch), jetson-thor-hardware.md,
  robot-launch-setup.md. Update memory as you learn.
- Run `source setup_robot.sh`.

KEY FILES (single source of truth = the registry)
- go2_control/behavior_registry.py — declarative metadata for every behavior; add a
  BehaviorDescriptor here first.
- go2_control/mission_supervisor_core.py — pure-Python state machine (TaskModes, SupervisorOps,
  transitions, normalize_voice_command, select_motion_routing). No ROS deps → unit-testable.
- go2_control/mission_supervisor_node.py — ROS node; operation handlers (_start_*/_cancel_*),
  action clients, Sport API calls.
- go2_control/voice_command_node.py — transcript → normalized command token (wake-phrase gated).
- go2_bringup/launch/mapping_audio.launch.py — Vosk grammar_phrases (Vosk ONLY recognizes phrases
  in this list — add yours, with and without the "amigo" wake prefix) + voice_command_node params.
- go2_bringup/launch/mapping_behavior.launch.py — launches behavior nodes + supervisor;
  _mapping_common.py for args; mapping.launch.py forwards args.
- go2_interfaces/action/*.action — for action-based behaviors. go2_control/setup.py — console_scripts.
- Node patterns to copy: search_action_server.py (action-based, discrete tasks) or
  person_follow_controller_node.py (controller, continuous velocity on /motion/candidate/<name>).

BUILD MODEL (important): editing EXISTING go2_control Python nodes + launch + Vosk grammar is LIVE
on the next launch (symlink-install). BUT a NEW behavior needs `colcon build --packages-select
go2_control` to register its new setup.py console_script, and if you add a new action/msg, build
go2_interfaces first. `source setup_robot.sh` rebuilds + re-sources.

YOU CANNOT RUN THE ROBOT — the user does. Before they test on hardware, run the state-machine unit
tests yourself: `colcon test --packages-select go2_control` (or pytest
src/go2_control/test/test_mission_supervisor_core.py). ALL EXISTING BEHAVIORS MUST KEEP WORKING —
add new branches, don't modify their logic.

CAPABILITY ACCESS (see ADDING_BEHAVIORS.md "Robot Capabilities Reference"): Nav2 via
/motion/candidate/nav; direct velocity via your own /motion/candidate/<name> (supervisor routes it
to cmd_vel when your mode is active); Unitree Sport API via unitree_api/Request on /api/sport/request
(1004 stand, 1005 lay, 1016 hello); gait via go2_motion_mode_switcher; perception from the ZED;
robot state from /robot_mode_state.

COMMANDING THE DOG — UNITREE SDK (sport / gait / posture API)
Two equivalent paths reach the Go2; both send the SAME Sport API IDs:
  (A) ROS 2 — PREFERRED for behaviors (matches Amigo): publish a unitree_api/Request to
      /api/sport/request. mission_supervisor_node.py already does this (_send_sport_request:
      `req.header.identity.api_id = <ID>` then publish). For commands that take arguments, ALSO set
      `req.parameter = json.dumps({...})`. Subscribe to /api/sport/response (match on
      header.identity.api_id) only if you need a return value.
  (B) Native C++ — for go2_driver nodes / low-level: link unitree_sdk2, init ChannelFactory with the
      network interface (enP2p1s0 — see jetson-thor-hardware.md), use
      unitree::robot::go2::SportClient / MotionSwitcherClient / RobotStateClient. In-repo example:
      go2_driver/src/go2_motion_mode_switcher.cpp (uses MotionSwitcherClient to set gait/mode).

THE API MAP — READ THESE (source of truth; identical IDs on both paths):
  - src/unitree_ros2/example/src/include/common/ros2_sport_client.h  +  .../src/common/ros2_sport_client.cpp
      → the ROS 2 SportClient: every motion expressed as (api_id, JSON parameter). COPY ITS ENCODING.
  - src/unitree_ros2/example/src/src/go2/go2_sport_client.cpp        → ROS 2 usage (StandUp/Move/Sit/...).
  - src/unitree_ros2/example/src/src/go2/go2_robot_state_client.cpp  → enable/disable onboard services.
  - sdk/unitree_sdk2/example/go2/                                    → native C++ examples: go2_sport_client.cpp
      (high-level sport), go2_low_level.cpp (per-motor LowCmd), go2_stand_example.cpp,
      go2_trajectory_follow.cpp, go2_robot_state_client.cpp, go2_vui_client.cpp (LEDs/audio), go2_video_client.cpp.
  - sdk/unitree_sdk2/include/unitree/robot/go2/sport/sport_client.hpp → native SportClient (same IDs).
  - sdk/unitree_sdk2/include/unitree/dds_wrapper/robots/go2/ (go2.h, go2_pub.h, go2_sub.h, defines.h)
      → thin DDS pub/sub helpers if you go native.
  - sdk/unitree_sdk2/include/unitree/idl/go2/ → raw DDS message structs (SportModeCmd_, SportModeState_,
      LowCmd_, LowState_, IMUState_, ...). Their ROS 2 equivalents are unitree_go/msg/* and unitree_api/msg/*.

KEY SPORT API IDs (from ros2_sport_client.h): 1001 Damp, 1002 BalanceStand, 1003 StopMove, 1004 StandUp,
  1005 StandDown, 1006 RecoveryStand, 1007 Euler, 1008 Move, 1009 Sit, 1010 RiseSit, 1015 SpeedLevel,
  1016 Hello, 1017 Stretch, 1022/1023 Dance1/2, 1028 Pose, 1036 Heart, 1061 StaticWalk, 1062 TrotRun,
  1063 EconomicGait, 2041 LeftFlip, 2043 BackFlip, 2044 HandStand, 2045 FreeWalk, 2048 FreeAvoid,
  2050 WalkUpright. PARAMETER ENCODINGS (req.parameter = a JSON string):
    Move → {"x": vx, "y": vy, "z": vyaw}  (m/s, m/s, rad/s)
    Euler → {"x": roll, "y": pitch, "z": yaw}
    SpeedLevel → {"data": level};  toggle moves (Pose, HandStand, FreeAvoid, ClassicWalk, ...) → {"data": true|false}
    no-arg moves (StandUp, Sit, Hello, Damp, BalanceStand, StopMove, ...) → NO parameter, just the api_id.

FEEDBACK FROM THE DOG: subscribe to lf/sportmodestate (unitree_go/msg/SportModeState) for the high state
  — position[3], velocity[3], yaw_speed, imu_state.rpy[3], foot force/position, mode, gait, body_height.
  (This is the dog's own estimator; Amigo also fuses /utlidar odom + ZED via EKF — see the TF chain.)

SERVICES / MODES: high-level sport commands need the onboard `sport_mode` service ON (default); per-motor
  LowCmd control needs it OFF. Toggle via go2_motion_mode_switcher (preferred, already in repo) or
  RobotStateClient.ServiceSwitch("sport_mode", 0|1) (see go2_robot_state_client.cpp).

RULES: (1) DON'T bypass the state machine — wrap a new sport move as a mission_supervisor operation/behavior
  (add ROBOT_SPORT_API_ID_* constants + a _send_sport_request call in mission_supervisor_node.py, dispatched
  from _execute_operation) so posture/idle preconditions and cooldowns are enforced. (2) Dynamic moves
  (flips, jumps, handstand, dance) need flat ground, clearance, and the dog already standing
  (StandUp/BalanceStand first) — gate them on PostureModes.STANDING. (3) For navigation prefer Nav2 via
  /motion/candidate/<name> (keeps the supervisor + collision_monitor in the loop); raw Move (1008) is the
  manual-velocity escape hatch.

PROCESS: follow the ADDING_BEHAVIORS.md checklist end-to-end; add unit tests; use AskUserQuestion
for design choices (preemption rules, motion source, posture requirements); for a large multi-file
behavior, draft a plan first. When it works, update ADDING_BEHAVIORS.md with anything you discovered
and update memory.

KEEP THIS PROMPT FRESH: if you discover something broadly useful for future behavior work (a new
pattern, capability, build nuance, or pitfall), append it to this prompt in docs/AGENT_PROMPTS.md
so the next agent inherits it.

THE BEHAVIOR I WANT: <trigger phrase; what the robot should do; task vs gesture vs posture; motion
source; preemption rules>
```

---

## Addendum — lessons from building "explore the area" + "deliver swag" (2026-06)

Verified facts and patterns for future behavior work (full guide:
[`EXPLORE_DELIVER_SWAG.md`](EXPLORE_DELIVER_SWAG.md); capabilities:
[`../src/go2_control/ADDING_BEHAVIORS.md`](../src/go2_control/ADDING_BEHAVIORS.md)):

- **OpenCV here is 4.6.0 (apt), numpy 1.26.4** — use the *legacy* ArUco API
  (`cv2.aruco.getPredefinedDictionary` + `detectMarkers`), NOT `ArucoDetector` (4.7+). Prefer
  `cv2.solvePnP(SOLVEPNP_IPPE_SQUARE)` over the deprecated `estimatePoseSingleMarkers`. The user's
  `~/.local` has numpy 2.x that shadows cv2 — run tooling with `PYTHONNOUSERSITE=1`.
- **The ZED `zed_aruco_localization` example is a red herring for marker work** — it only resets the
  ZED's own pose via `set_pose` from hard-coded marker world-poses; it never publishes a detected
  marker's pose. Build a small detector node instead (cv_bridge/OpenCV are already go2_control deps).
- **ZED topic names are NITROS-renamed (2026-06-06)** — the source-built zed-ros2-wrapper with
  `disable_nitros:false` (default) publishes the rectified color stream as
  `/zed/zed_node/rgb/color/rect/image` (a PLAIN sensor_msgs/Image; `…/image/nitros` is the negotiated
  variant) + camera_info `/zed/zed_node/rgb/color/rect/camera_info`. The OLD stereolabs names
  `/zed/zed_node/rgb/image_rect_color` and `/zed/zed_node/rgb/camera_info` are GONE. A node hard-wired
  to the old names gets NOTHING and the ZED never even starts the stream (it lazy-publishes only to a
  compatible subscriber), so the symptom is a forever "waiting for camera_info" / "waiting for image"
  with no QoS error and no crash. This bit `aruco_detector_node` AND `person_follow_vision_node` (and
  the standalone `picture_taker*.py`). When a ZED consumer goes silent, FIRST diff the node's
  subscribed topic against `grep "Advertised on topic" nav2_test.txt` — don't assume QoS.
- **ZED publishes RELIABLE, not BEST_EFFORT** — its image/camera_info QoS is `rclcpp::QoS(10)` =
  RELIABLE depth 10 (verified in wrapper source). A BEST_EFFORT (`qos_profile_sensor_data`) subscriber
  is still compatible (BE-sub accepts a RELIABLE-pub), so subscribing BEST_EFFORT is the safe universal
  choice — but a "no data" symptom is far more likely a topic-NAME mismatch than QoS. (`ros2 topic echo`
  auto-negotiates, so echo "working" does NOT prove your node's topic name is right.)
- **`tf2_ros.Buffer.lookup_transform(target, source, rclpy.time.Time())` (zero time) means "latest
  available", not "transform at t=0"** — it is the correct, extrapolation-safe idiom; do not "fix" it
  to pass the message stamp (that reintroduces extrapolation failures).
- **slam_toolbox has runtime save** (`save_map` + `serialize_map` services) and can **load a saved
  posegraph at launch** via the `map_file_name` param (added as the `slam_map_file` launch arg) — no
  separate localization-mode launch needed for same-binary cross-session map reuse.
- **The arm is gs_usb CAN, not ROS** — wrap the user's record/replay scripts in a node that hosts a
  service and keep a `dry_run` mode (guard the `gs_usb` import) so the whole mission is testable
  before the hardware is wired. `gs_usb` is pip-installed and has no rosdep key (document, don't
  `<depend>`).
- **New voice command groups need three edits**: a `voice_group` on the registry descriptor, the
  group added to `_parse_command_mode` (incl. the `all` set) in `voice_command_node.py`, and the
  phrases added to the Vosk `grammar_phrases` list in `mapping_audio.launch.py` (Vosk only hears
  phrases in that list). Watch phrase-substring collisions (match the more specific phrase first;
  e.g. "done exploring" before "explore", and drop ambiguous handoff phrases like "we are done").
- **A blocking actuator service is fine to call from an async action**: poll `future.done()` in the
  execute coroutine with `_sleep_async` + cancel checks rather than a bare `await`, so the mission
  stays cancelable during a long arm replay.
- **Nav2-heavy nodes (BasicNavigator) must run on a dedicated `SingleThreadedExecutor`** (it nests
  rclpy spins) — copy the `main()` from `localize_detected_leak_action_server.py`.
- **rclpy throttled logging is keyed on the CALL-SITE, not the message** (`rcutils_logger.py`
  `CallerId` = function+file+line). A debug helper that funnels many messages through ONE
  `get_logger().info(msg, throttle_duration_sec=X)` line and passes a *different* X between calls
  CRASHES the node with `ValueError: Logging filter parameters cannot be changed between calls`
  (severity/name/filter-set changes raise the same family of error). This killed
  `aruco_detector_node` ~2s into a run whenever `debug:=true` (see [[aruco-recorder-debug]]). Safe
  patterns: either give each message its own call-site with a CONSTANT throttle value, or throttle
  manually (clock + per-key dict) and call `.info()` unfiltered. A node "dying silently right after
  startup with no obvious cause" + an empty downstream artifact (0 markers, no detections) → grep the
  log for that ValueError; it only shows when the debug arg is on.
- **go2_control python nodes are HARDLINKED into `build/` (egg-link → `build/go2_control`), so src
  edits are live on relaunch with NO `colcon build`** — but the running file is imported from
  `build/<pkg>/<pkg>/`. Confirm an edit propagated with `stat -c %i` (src and build must share one
  inode) since an editor that does atomic-rename could break the link; if it breaks, rebuild.
- **ArUco predefined dicts of the same bit-size are nested in OpenCV 4.6** — `DICT_6X6_100`
  byte-patterns are a strict subset of `DICT_6X6_1000` (first 100 ids identical), so a marker printed
  from either dict (ids <100) detects under the other. The swag stack runs `DICT_6X6_1000` (the
  `aruco_dictionary` launch default; a stale doc table says `DICT_6X6_100`). Don't chase a dict
  mismatch for low ids — verify empirically via `getPredefinedDictionary(...).bytesList`.
- **The aruco_detector_node runs with `additional_env PYTHONNOUSERSITE=1`** so it uses apt cv2 4.6 +
  numpy 1.26 and ignores `~/.local` numpy 2.4.6 (ABI-incompatible — bare `import cv2` crashes). Any
  standalone aruco/cv2 python you run for debugging needs `PYTHONNOUSERSITE=1` too.
