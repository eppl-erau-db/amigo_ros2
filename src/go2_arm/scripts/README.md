# Arm trajectory scripts

`arm_replay_node` plays back pre-recorded CubeMars-arm trajectories by name. By
default it looks in `~/amigo_arm_scripts/` (the `scripts_dir` parameter). Drop the
recorded CSVs there:

- `pickup.csv`   — pick the basket up at the swag pick-up marker
- `deliver.csv`  — present the basket at the delivery marker
- `dropoff.csv`  — set the empty basket back down at the pick-up marker

Record one by hand-guiding the arm:

```bash
ros2 run go2_arm arm_record --name pickup --dir ~/amigo_arm_scripts
```

CSV columns: `timestamp, motor_id, position_rad, velocity_rad_s` (one row per
motor per timestep, ~100 Hz). The replay re-sends the recorded positions at the
original timing and holds the final pose.

This directory (installed to the package `share/`) is just documentation; the
runtime trajectories live in `scripts_dir`.
