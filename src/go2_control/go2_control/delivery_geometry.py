"""
Pure geometry helpers for the swag-delivery mission (no ROS dependency).

* ``staging_pose`` — given a marker's map-frame pose, compute a Nav2 goal pose
  standing ``standoff_m`` in front of the marker (on its outward normal) and
  facing it.
* ``servo_command`` — given the marker's pose in the robot BASE frame (from a
  live detection), compute the (vx, wz) diff-drive command + an "aligned" flag to
  trim the robot to ``standoff_m`` squarely facing the marker.

These are unit-testable in isolation.
"""
from __future__ import annotations

import math


def yaw_from_quat(qx: float, qy: float, qz: float, qw: float) -> float:
    siny_cosp = 2.0 * (qw * qz + qx * qy)
    cosy_cosp = 1.0 - 2.0 * (qy * qy + qz * qz)
    return math.atan2(siny_cosp, cosy_cosp)


def quat_from_yaw(yaw: float) -> tuple[float, float, float, float]:
    return (0.0, 0.0, math.sin(yaw / 2.0), math.cos(yaw / 2.0))


def marker_outward_normal_xy(qx: float, qy: float, qz: float, qw: float) -> tuple[float, float]:
    """Project the marker frame's +z axis (out of its face) into the XY plane.

    For a wall-mounted ArUco this is the horizontal direction pointing away from
    the wall toward where the robot should stand. Returns a unit (nx, ny); falls
    back to the marker's yaw-forward if the normal is near-vertical.
    """
    n = math.sqrt(qx * qx + qy * qy + qz * qz + qw * qw) or 1.0
    qx, qy, qz, qw = qx / n, qy / n, qz / n, qw / n
    # Third column of the rotation matrix = marker +z axis in the parent frame.
    zx = 2.0 * (qx * qz + qy * qw)
    zy = 2.0 * (qy * qz - qx * qw)
    norm = math.hypot(zx, zy)
    if norm < 1e-6:
        # Normal is ~vertical; use the marker's x-axis (yaw forward) instead.
        yaw = yaw_from_quat(qx, qy, qz, qw)
        return math.cos(yaw), math.sin(yaw)
    return zx / norm, zy / norm


def staging_pose(
    marker_x: float, marker_y: float,
    qx: float, qy: float, qz: float, qw: float,
    standoff_m: float,
) -> tuple[float, float, float]:
    """Return ``(x, y, yaw)`` for a base pose ``standoff_m`` in front of the
    marker (along its outward normal), oriented to face the marker."""
    nx, ny = marker_outward_normal_xy(qx, qy, qz, qw)
    sx = marker_x + standoff_m * nx
    sy = marker_y + standoff_m * ny
    # Face back toward the marker (opposite the outward normal).
    yaw = math.atan2(-ny, -nx)
    return sx, sy, yaw


def servo_command(
    marker_x_base: float, marker_y_base: float,
    standoff_m: float,
    *,
    kv: float = 0.6, kw: float = 1.2,
    vx_max: float = 0.25, wz_max: float = 0.8,
    pos_tol_m: float = 0.05, yaw_tol_rad: float = 0.06,
    face_first_rad: float = 0.35,
) -> tuple[float, float, bool]:
    """Diff-drive fine-alignment command toward a marker seen at (x, y) in the
    base frame (x forward, y left).

    Strategy: turn to put the marker dead-ahead (bearing -> 0), then drive forward
    until the range equals ``standoff_m``. Returns ``(vx, wz, aligned)``.
    """
    rng = math.hypot(marker_x_base, marker_y_base)
    bearing = math.atan2(marker_y_base, marker_x_base)
    range_err = rng - standoff_m

    aligned = abs(range_err) <= pos_tol_m and abs(bearing) <= yaw_tol_rad
    if aligned:
        return 0.0, 0.0, True

    wz = max(-wz_max, min(wz_max, kw * bearing))
    # Only drive forward once roughly facing the marker, to keep the approach on
    # the marker normal instead of cutting the corner.
    if abs(bearing) <= face_first_rad:
        vx = max(-vx_max, min(vx_max, kv * range_err))
    else:
        vx = 0.0
    return vx, wz, False
