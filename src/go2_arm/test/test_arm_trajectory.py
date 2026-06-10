"""Unit tests for go2_arm.arm_trajectory (CSV load + hardware-free replay loop)."""
import os
import tempfile

import pytest

from go2_arm.arm_trajectory import (
    load_frames,
    motor_ids_in,
    replay_frames,
    trajectory_duration,
)


def _write_csv(rows: list[str]) -> str:
    fd, path = tempfile.mkstemp(suffix=".csv")
    os.close(fd)
    with open(path, "w") as handle:
        handle.write("timestamp,motor_id,position_rad,velocity_rad_s\n")
        for row in rows:
            handle.write(row + "\n")
    return path


def test_load_frames_groups_by_timestamp_and_sorts():
    path = _write_csv([
        "0.02,1,0.5,0.1",
        "0.00,1,0.0,0.0",
        "0.00,2,1.0,0.0",
        "0.02,2,1.2,0.1",
    ])
    frames = load_frames(path)
    os.remove(path)
    assert [t for t, _ in frames] == [0.0, 0.02]
    assert frames[0][1] == {1: (0.0, 0.0), 2: (1.0, 0.0)}
    assert motor_ids_in(frames) == {1, 2}
    assert trajectory_duration(frames) == pytest.approx(0.02)


def test_load_frames_skips_nan_and_bad_rows():
    path = _write_csv([
        "0.00,1,nan,0.0",
        "0.00,1,0.3,0.0",
        "0.01,1,0.4,nan",
        "0.01,1,0.4,0.2",
    ])
    frames = load_frames(path)
    os.remove(path)
    # NaN position dropped on first row (overwritten by valid 0.3); NaN velocity row dropped.
    assert frames[0][1][1] == (0.3, 0.0)
    assert frames[1][1][1] == (0.4, 0.2)


def test_load_frames_empty_raises():
    path = _write_csv([])
    with pytest.raises(ValueError):
        load_frames(path)
    os.remove(path)


def test_replay_frames_sends_each_motor_and_returns_last_pos():
    frames = [
        (0.0, {1: (0.0, 0.0), 2: (1.0, 0.0)}),
        (0.1, {1: (0.5, 0.2), 2: (1.5, 0.2)}),
    ]
    sent = []
    last = replay_frames(
        frames,
        lambda mid, pos, vl, al: sent.append((mid, pos, vl, al)),
        speed=1.0,
        acc_limit=2.0,
        min_vel=0.05,
        sleep_fn=lambda _s: None,
        monotonic_fn=lambda: 0.0,
    )
    assert last == {1: 0.5, 2: 1.5}
    # min_vel floor applied to the first (zero-velocity) frame.
    assert (1, 0.0, 0.05, 2.0) in sent
    assert (1, 0.5, 0.2, 2.0) in sent


def test_replay_frames_should_continue_stops_early():
    frames = [(float(i) * 0.1, {1: (float(i), 0.0)}) for i in range(10)]
    calls = {"n": 0}

    def cont():
        calls["n"] += 1
        return calls["n"] <= 3

    sent = []
    replay_frames(
        frames,
        lambda mid, pos, vl, al: sent.append(pos),
        sleep_fn=lambda _s: None,
        monotonic_fn=lambda: 0.0,
        should_continue=cont,
    )
    # Stops after 3 successful frames (4th should_continue returns False).
    assert sent == [0.0, 1.0, 2.0]
