#!/usr/bin/env python3
"""
arm_record — capture a CubeMars arm trajectory to a CSV that ``arm_replay_node``
can later play back.

This is the gs_usb-driver port of the project's ``position_tracker.py`` with the
NeuroLocoMiddleware / SocketCAN dependencies removed (plain timed loop). It is a
standalone CLI (no ROS spin needed); it just streams motor feedback to a CSV.

Usage:
    ros2 run go2_arm arm_record --name pickup
    ros2 run go2_arm arm_record --name deliver --dir ~/amigo_arm_scripts --rate 100

Back-drive / lead-through the arm by hand, then Ctrl-C (or --duration) to stop.
Output: <dir>/<name>.csv with columns: timestamp, motor_id, position_rad, velocity_rad_s
"""
from __future__ import annotations

import argparse
import csv
import os
import time


def main() -> None:
    parser = argparse.ArgumentParser(description="Record a CubeMars arm trajectory to CSV.")
    parser.add_argument("--name", required=True, help="trajectory name, e.g. 'pickup' (-> <dir>/<name>.csv)")
    parser.add_argument("--dir", default=os.path.expanduser("~/amigo_arm_scripts"),
                        help="output directory (default: ~/amigo_arm_scripts)")
    parser.add_argument("--motors", default="1,2,3", help="comma-separated motor CAN IDs")
    parser.add_argument("--rate", type=float, default=100.0, help="sample rate Hz (default 100)")
    parser.add_argument("--duration", type=float, default=0.0, help="auto-stop after N seconds (0 = until Ctrl-C)")
    parser.add_argument("--bitrate", type=int, default=1_000_000, help="CAN bitrate")
    args = parser.parse_args()

    from go2_arm.ak45_motor import AK45Motor, MotorBus

    motor_ids = [int(x) for x in args.motors.split(",") if x.strip()]
    os.makedirs(args.dir, exist_ok=True)
    out_path = os.path.join(args.dir, args.name if args.name.endswith(".csv") else f"{args.name}.csv")
    dt = 1.0 / max(1.0, args.rate)

    motors = [AK45Motor(mid, 0.0, None) for mid in motor_ids]
    with MotorBus(motors=motors, bitrate=args.bitrate) as bus:
        for m in motors:
            m.bus = bus
        time.sleep(0.1)  # let first feedback frames arrive

        print(f"Recording motors {motor_ids} -> {out_path} at {args.rate:.0f} Hz. Ctrl-C to stop.")
        t0 = time.monotonic()
        rows = 0
        with open(out_path, "w", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["timestamp", "motor_id", "position_rad", "velocity_rad_s"])
            try:
                while True:
                    t = time.monotonic() - t0
                    for m in motors:
                        s = m.get_state()
                        if s.position == s.position and s.velocity == s.velocity:  # not NaN
                            writer.writerow([t, m.can_id, s.position, s.velocity])
                            rows += 1
                    print("\r" + " | ".join(
                        f"ID:{m.can_id} pos:{m.get_state().position:+.3f} vel:{m.get_state().velocity:+.3f}"
                        for m in motors
                    ), end="", flush=True)
                    if args.duration > 0.0 and t >= args.duration:
                        break
                    time.sleep(dt)
            except KeyboardInterrupt:
                pass
        print(f"\nSaved {rows} rows to {out_path}.")


if __name__ == "__main__":
    main()
