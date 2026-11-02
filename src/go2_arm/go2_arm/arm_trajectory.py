"""
Pure-Python helpers for recording / replaying CubeMars arm trajectories.

These functions carry no ROS or CAN dependencies so they can be unit-tested
directly and reused by both the replay node (hardware) and dry-run mode (fakes).

CSV format (one row per motor per timestep):
    timestamp, motor_id, position_rad, velocity_rad_s
"""
from __future__ import annotations

import csv
import time
from collections import defaultdict
from typing import Callable


def load_frames(path: str) -> list[tuple[float, dict[int, tuple[float, float]]]]:
    """Return a time-sorted list of ``(timestamp, {motor_id: (pos_rad, vel_rad_s)})``.

    Rows with non-finite position/velocity are skipped. Raises ``ValueError`` if
    the file has no usable frames.
    """
    frames: dict[float, dict[int, tuple[float, float]]] = defaultdict(dict)
    with open(path, newline="") as handle:
        for row in csv.DictReader(handle):
            try:
                t = float(row["timestamp"])
                mid = int(row["motor_id"])
                pos = float(row["position_rad"])
                vel = float(row["velocity_rad_s"])
            except (KeyError, ValueError, TypeError):
                continue
            if pos != pos or vel != vel:  # NaN guard
                continue
            frames[t][mid] = (pos, vel)
    if not frames:
        raise ValueError(f"No usable trajectory frames found in '{path}'.")
    return sorted(frames.items())


def trajectory_duration(frames: list[tuple[float, dict]]) -> float:
    """Wall-clock span of the recorded trajectory in seconds."""
    if not frames:
        return 0.0
    return float(frames[-1][0] - frames[0][0])


def motor_ids_in(frames: list[tuple[float, dict]]) -> set[int]:
    ids: set[int] = set()
    for _t, states in frames:
        ids.update(states.keys())
    return ids


def replay_frames(
    frames: list[tuple[float, dict[int, tuple[float, float]]]],
    send_position: Callable[[int, float, float, float], None],
    *,
    speed: float = 1.0,
    acc_limit: float = 2.0,
    min_vel: float = 0.05,
    sleep_fn: Callable[[float], None] = time.sleep,
    monotonic_fn: Callable[[], float] = time.monotonic,
    should_continue: Callable[[], bool] | None = None,
) -> dict[int, float]:
    """Replay ``frames`` at (scaled) recorded timing.

    ``send_position(motor_id, pos_rad, vel_limit, acc_limit)`` is invoked for each
    motor in each frame. Timing is preserved relative to the first frame, scaled
    by ``speed`` (>1 plays faster). ``should_continue`` is polled once per frame;
    returning False stops the replay early (cancellation).

    Returns ``{motor_id: last_commanded_pos_rad}`` so the caller can hold the
    final pose. Decoupled from hardware via the injected callables for testing.
    """
    if not frames:
        return {}
    speed = speed if speed and speed > 0.0 else 1.0
    stride = max(1, round(speed))
    csv_t0 = frames[0][0]
    t_start = monotonic_fn()
    last_pos: dict[int, float] = {}

    for csv_t, states in frames[::stride]:
        if should_continue is not None and not should_continue():
            break
        wait = (t_start + (csv_t - csv_t0) / speed) - monotonic_fn()
        if wait > 0:
            sleep_fn(wait)
        for mid, (pos, vel) in states.items():
            send_position(mid, pos, max(abs(vel), min_vel), acc_limit)
            last_pos[mid] = pos
    return last_pos
