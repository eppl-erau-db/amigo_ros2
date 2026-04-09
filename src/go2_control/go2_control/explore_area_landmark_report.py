#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def rpy_from_quaternion_xyzw(quaternion: list[float]) -> tuple[float, float, float]:
    x, y, z, w = quaternion

    t0 = 2.0 * (w * x + y * z)
    t1 = 1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(t0, t1)

    t2 = 2.0 * (w * y - z * x)
    t2 = max(min(t2, 1.0), -1.0)
    pitch = math.asin(t2)

    t3 = 2.0 * (w * z + x * y)
    t4 = 1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(t3, t4)
    return roll, pitch, yaw


def _pose_to_xyz_quat_rpy(pose_dict: dict[str, Any]) -> tuple[list[float], list[float], list[float]]:
    position = pose_dict["position"]
    orientation = pose_dict["orientation"]
    xyz = [
        float(position["x"]),
        float(position["y"]),
        float(position["z"]),
    ]
    quat = [
        float(orientation["x"]),
        float(orientation["y"]),
        float(orientation["z"]),
        float(orientation["w"]),
    ]
    rpy = list(rpy_from_quaternion_xyzw(quat))
    return xyz, quat, rpy


def _format_vector(values: list[float]) -> str:
    return "[" + ", ".join(f"{value:.4f}" for value in values) + "]"


def _print_landmark(marker_id: str, entry: dict[str, Any], *, pose_key: str) -> None:
    pose_dict = entry.get(pose_key)
    if not isinstance(pose_dict, dict):
        print(f"Marker {marker_id}: no pose data under {pose_key!r}")
        return

    xyz, quat, rpy = _pose_to_xyz_quat_rpy(pose_dict)
    role_name = entry.get("role_name") or f"aruco_{marker_id}"
    print(f"Marker {marker_id} ({role_name})")
    print(f"  observations: {entry.get('observations', 0)}")
    print(f"  pose source: {pose_key}")
    print(f"  position xyz [m]: {_format_vector(xyz)}")
    print(f"  orientation quaternion [xyzw]: {_format_vector(quat)}")
    print(f"  orientation rpy [rad]: {_format_vector(rpy)}")

    configured = entry.get("configured_map_pose")
    if isinstance(configured, dict):
        configured_xyz, _, configured_rpy = _pose_to_xyz_quat_rpy(configured)
        print(f"  configured xyz [m]: {_format_vector(configured_xyz)}")
        print(f"  configured rpy [rad]: {_format_vector(configured_rpy)}")

    print("  YAML snippet:")
    print(f"    {role_name}:")
    print(f"      aruco_id: {int(entry['aruco_id'])}")
    print("      fixed_map_pose:")
    print(f"        position: {_format_vector(xyz)}")
    print(f"        orientation: {_format_vector(rpy)}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print observed or reference ArUco landmark poses from explore_area landmarks.json."
    )
    parser.add_argument(
        "landmarks_json",
        nargs="?",
        default="artifacts/explore_area/landmarks.json",
        help="Path to landmarks.json (default: artifacts/explore_area/landmarks.json)",
    )
    parser.add_argument(
        "--marker-id",
        help="Only print one marker id, e.g. 43",
    )
    parser.add_argument(
        "--pose-source",
        choices=["marker_pose", "reference_marker_pose"],
        default="marker_pose",
        help="Which saved pose to print (default: marker_pose)",
    )
    args = parser.parse_args()

    report_path = Path(args.landmarks_json).expanduser()
    if not report_path.is_file():
        raise SystemExit(f"landmarks.json not found: {report_path}")

    payload = json.loads(report_path.read_text(encoding="utf-8"))
    landmarks = payload.get("landmarks", {})
    if not isinstance(landmarks, dict) or not landmarks:
        raise SystemExit(
            "No landmarks found in "
            f"{report_path}. This usually means the mission has not been canceled/completed "
            "since the last detection, or this file is stale from an older run."
        )

    marker_filter = str(args.marker_id).strip() if args.marker_id is not None else ""

    print(f"Report: {report_path}")
    print(f"Map YAML: {payload.get('map_yaml_path', '')}")
    print()

    printed_any = False
    for marker_id, entry in sorted(landmarks.items(), key=lambda item: int(item[0])):
        if marker_filter and marker_id != marker_filter:
            continue
        if not isinstance(entry, dict):
            continue
        _print_landmark(marker_id, entry, pose_key=args.pose_source)
        printed_any = True

    if not printed_any:
        raise SystemExit(
            f"No matching landmarks found in {report_path} for marker_id={marker_filter or 'ALL'}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
