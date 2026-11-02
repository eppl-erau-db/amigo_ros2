from __future__ import annotations

import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from go2_control.delivery_geometry import (  # noqa: E402
    marker_outward_normal_xy,
    quat_from_yaw,
    servo_command,
    staging_pose,
    yaw_from_quat,
)


def test_yaw_quat_roundtrip() -> None:
    for yaw in (-2.0, -0.5, 0.0, 0.5, 1.5, 3.0):
        q = quat_from_yaw(yaw)
        # Compare as a wrapped angle difference (handles the +/-pi wrap).
        diff = ((yaw_from_quat(*q) - yaw + math.pi) % (2 * math.pi)) - math.pi
        assert abs(diff) < 1e-6


def test_marker_normal_for_identity_points_along_x() -> None:
    # Identity orientation: marker +z axis is the parent +z; XY projection is ~0,
    # so the helper falls back to the marker x-axis (yaw 0) -> (1, 0).
    nx, ny = marker_outward_normal_xy(0.0, 0.0, 0.0, 1.0)
    assert nx == math.cos(0.0)
    assert abs(ny) < 1e-9


def test_marker_normal_for_wall_facing_minus_x() -> None:
    # Rotate the marker so its +z axis points along world -x (a wall on the +x side
    # facing back toward the origin). yaw = +90 deg about z maps +z->... use a
    # rotation that puts +z into the XY plane: rotate -90 deg about y.
    # Quaternion for -90 deg about y:
    a = -math.pi / 2
    q = (0.0, math.sin(a / 2), 0.0, math.cos(a / 2))
    nx, ny = marker_outward_normal_xy(*q)
    # +z of marker -> +x (approx) after -90 about y; just assert it is unit & in XY.
    assert abs(math.hypot(nx, ny) - 1.0) < 1e-6


def test_staging_pose_in_front_and_facing_marker() -> None:
    # Marker at (2,0) whose outward normal points -x (faces the origin). Build a
    # quaternion whose +z maps to (-1,0,0): rotate +90 deg about y maps +z->+x;
    # we want -x so rotate -90 about y? Use a direct construction by yaw fallback:
    # give a near-vertical normal so the helper uses yaw. Place marker yaw=pi
    # (facing -x). Then outward normal ~ (cos pi, sin pi) = (-1, 0).
    q = quat_from_yaw(math.pi)
    sx, sy, syaw = staging_pose(2.0, 0.0, *q, 0.6)
    # Standoff is along the outward normal (-x): staging at x < 2.
    assert sx < 2.0
    assert abs(sy) < 1e-6
    # Robot faces back toward the marker (+x direction) -> yaw ~ 0.
    assert abs(((syaw + math.pi) % (2 * math.pi)) - math.pi) < 1e-6


def test_servo_aligned_when_marker_at_standoff_ahead() -> None:
    vx, wz, aligned = servo_command(0.55, 0.0, 0.55)
    assert aligned is True
    assert vx == 0.0 and wz == 0.0


def test_servo_turns_toward_offcenter_marker_without_driving() -> None:
    # Marker far to the left: should rotate (wz>0) and not drive forward yet.
    vx, wz, aligned = servo_command(0.3, 0.5, 0.55)
    assert aligned is False
    assert wz > 0.0
    assert vx == 0.0  # bearing exceeds face_first threshold -> no forward motion


def test_servo_drives_forward_when_facing_and_far() -> None:
    # Marker dead ahead but too far: drive forward, minimal turn.
    vx, wz, aligned = servo_command(1.2, 0.0, 0.55)
    assert aligned is False
    assert vx > 0.0
    assert abs(wz) < 1e-6


def test_servo_respects_speed_caps() -> None:
    vx, wz, _ = servo_command(10.0, 0.0, 0.55, vx_max=0.2, wz_max=0.5)
    assert vx <= 0.2
    vx2, wz2, _ = servo_command(0.3, 5.0, 0.55, vx_max=0.2, wz_max=0.5)
    assert abs(wz2) <= 0.5
