# Explore-the-area + Deliver-swag behaviors

Two voice behaviors added to Amigo:

- **"hey amigo, let's explore the area"** — a manual-drive SLAM mapping session that also
  records where ArUco markers are. **"hey amigo, we are done exploring"** saves the map + the
  marker table.
- **"hey amigo, deliver swag"** — autonomous mission: navigate to the pick-up ArUco marker,
  fine-align, run the arm pick-up script, navigate to the delivery marker, run the deliver
  script, wait for **"hey amigo, all done"**, then return and run the drop-off script.

The robot has a 3-motor CubeMars AK45 arm on a gs_usb CAN bus; the arm replays pre-recorded
trajectories on request.

---

## Voice commands

| Phrase (wake-gated by "hey amigo" / "amigo") | Command | Effect |
|---|---|---|
| "let's explore the area" / "explore the area" | `explore` | Enter EXPLORE (manual mapping) |
| "we are done exploring" / "done exploring" | `done_exploring` | Save map + markers → IDLE |
| "deliver swag" / "deliver the swag" | `deliver_swag` | Start the delivery mission |
| "all done" / "all finished" | `handoff_done` | Tell the in-progress delivery the hand-off is done |

All four are in the Vosk grammar (`mapping_audio.launch.py`) and matched in `voice_command_node.py`
under the new `explore` / `deliver` command groups (enabled by `command_mode:=all`, the default).

---

## How it works

```
                 ZED RGB + camera_info
                          │
                  aruco_detector_node            (cv2.aruco DICT_6X6_100, solvePnP)
                  │                 │
   /aruco/markers_map (map frame)   /aruco/markers_base (base frame)
                  │                                 │
   ┌──────────────┴──────────┐          ┌───────────┴───────────────┐
   │ map_marker_recorder_node │          │ deliver_swag_action_server │
   │  (records during EXPLORE) │          │  Nav2 staging + servo align │
   │  SaveExploreMap →         │          │  → /arm/play_script svc     │
   │  slam save_map+serialize  │          │  → BalanceStand lock        │
   │  + <map>.aruco.yaml       │          └───────────┬───────────────┘
   └───────────────────────────┘                      │
                                              /arm/play_script (PlayArmScript)
                                                       │
                                               arm_replay_node (go2_arm)
                                                       │
                                          gs_usb CAN → CubeMars AK45 ×3
```

- The **mission supervisor** owns state as always: `TaskModes.EXPLORE` and `TaskModes.DELIVER`
  were added alongside FOLLOW/SEARCH. EXPLORE publishes **no** motion (you drive with the Unitree
  handheld remote); DELIVER routes `/motion/candidate/nav → cmd_vel` exactly like SEARCH.
- **Fine alignment**: Nav2 drives to a staging pose on the marker's outward normal
  (`delivery_geometry.staging_pose`), then the server cancels Nav2 and publishes its own Twist to
  `/motion/candidate/nav` to visual-servo the live `/aruco/markers_base` detection to a precise
  standoff (`delivery_geometry.servo_command`).
- **Map session ("Both")**: explore always saves to disk; deliver loads markers from
  `<maps_dir>/<map>.aruco.yaml` if present, else from the live `/aruco/markers_map` stream
  (same-session). For a fresh session, relaunch with `slam_map_file:=<maps_dir>/<map>` so
  slam_toolbox loads the saved posegraph and localizes on it.

---

## Before the first real run (integration checklist)

1. **Print ArUco markers** from `DICT_6X6_100`. Measure the side length precisely and set
   `aruco_marker_size_m:=<meters>` (default 0.16). Put one at the pick-up station and a different
   id at the delivery station.
2. **Assign marker ids**: `deliver_pickup_marker_id:=<id>` and `deliver_delivery_marker_id:=<id>`
   (defaults 0 and 1).
3. **Verify the ZED image topic** the detector subscribes to actually exists:
   `ros2 topic list | grep rgb`. Override `aruco_image_topic` / `aruco_camera_info_topic` if your
   wrapper publishes `rgb/color/rect/image` instead of `rgb/image_rect_color`.
4. **Record the arm trajectories** by hand-guiding the arm:
   ```bash
   ros2 run go2_arm arm_record --name pickup  --dir ~/amigo_arm_scripts
   ros2 run go2_arm arm_record --name deliver --dir ~/amigo_arm_scripts
   ros2 run go2_arm arm_record --name dropoff --dir ~/amigo_arm_scripts
   ```
   (requires `pip install gs_usb` and the CAN dongle attached). The delivery mission calls scripts
   named `pickup`, `deliver`, `dropoff`.
5. **No arm mounted yet?** Launch with `deliver_use_arm:=false` — the mission skips the arm service
   entirely and just waits `deliver_arm_stub_wait_s` (default 3 s) at each pickup/deliver/dropoff
   step, so you can validate nav + alignment + the full flow before the arm exists. Set
   `deliver_use_arm:=true` (default) once it's on the dog.
6. **Keep `arm_dry_run:=true` until you trust the alignment.** With the arm enabled, dry-run
   validates + time-simulates each trajectory (no CAN). Flip to `arm_dry_run:=false` to move the
   real arm. (Note: dry-run still needs the CSVs to exist; for a totally arm-free test use
   `deliver_use_arm:=false` above.)
7. **Pick-up verification** is currently a stub (`_verify_pickup_stub` always True). Replace it with
   a real check (motor torque/current, weight, or a vision confirmation) when ready.

---

## Running it

Same launch as always:

```bash
source setup_robot.sh
ros2 launch go2_bringup mapping.launch.py            # explore + deliver enabled by default
```

Same-session demo:
1. "hey amigo, let's explore the area" → drive the venue with the remote (markers get recorded as
   the ZED sees them) → "hey amigo, we are done exploring" (saves `~/amigo_maps/venue.*`).
2. "hey amigo, deliver swag" → robot picks up, delivers, waits → "hey amigo, all done" → robot
   returns and drops off the basket.

Cross-session (after a relaunch/reboot):
```bash
ros2 launch go2_bringup mapping.launch.py slam_map_file:=~/amigo_maps/venue
# set the initial pose in RViz (2D Pose Estimate) so SLAM localizes, then "deliver swag".
```

---

## Key launch args (all in `_mapping_common.py`)

| Arg | Default | Meaning |
|---|---|---|
| `swag_enable` | true | Launch the explore/deliver stack |
| `aruco_marker_size_m` | 0.16 | Printed marker side length (must match reality) |
| `aruco_dictionary` | DICT_6X6_100 | OpenCV ArUco dictionary |
| `aruco_image_topic` | /zed/zed_node/rgb/image_rect_color | RGB image into the detector |
| `aruco_camera_info_topic` | /zed/zed_node/rgb/camera_info | Intrinsics |
| `swag_maps_dir` | ~/amigo_maps | Where map + `.aruco.yaml` are saved/loaded |
| `swag_map_name` | venue | Base name for the map + marker table |
| `arm_enable` | true | Launch `arm_replay_node` |
| `arm_dry_run` | true | Simulate the arm (no CAN). Set false for the real arm |
| `arm_scripts_dir` | ~/amigo_arm_scripts | Recorded trajectory CSVs |
| `deliver_use_arm` | true | false → skip the arm and just wait at each arm step (armless testing) |
| `deliver_arm_stub_wait_s` | 3.0 | Wait per arm step when `deliver_use_arm:=false` |
| `deliver_pickup_marker_id` | 0 | Pick-up station marker id |
| `deliver_delivery_marker_id` | 1 | Delivery station marker id |
| `slam_map_file` | "" | Saved posegraph base path to load (cross-session) |

Tuning params (servo gains/tolerances, standoffs, timeouts) live on `deliver_swag_action_server`
— see `ros2 param list /deliver_swag_action_server`.
