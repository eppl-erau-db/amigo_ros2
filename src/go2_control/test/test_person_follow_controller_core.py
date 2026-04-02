from __future__ import annotations

import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from go2_control.person_follow_controller_core import (  # noqa: E402
    FollowControlParams,
    FollowStateMachine,
    FollowStates,
    GridMap2D,
    Pose2D,
    SafetyOracleParams,
    compute_nominal_follow_command,
    select_safe_command,
)


def _make_grid(
    width: int = 80,
    height: int = 80,
    resolution: float = 0.05,
    origin_x: float = -2.0,
    origin_y: float = -2.0,
) -> GridMap2D:
    return GridMap2D(
        resolution=resolution,
        width=width,
        height=height,
        origin_x=origin_x,
        origin_y=origin_y,
        data=tuple(0 for _ in range(width * height)),
    )


def _with_obstacle_band(
    grid: GridMap2D,
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    value: int = 100,
) -> GridMap2D:
    data = list(grid.data)
    for my in range(grid.height):
        world_y = grid.origin_y + ((my + 0.5) * grid.resolution)
        if not (y_min <= world_y <= y_max):
            continue
        for mx in range(grid.width):
            world_x = grid.origin_x + ((mx + 0.5) * grid.resolution)
            if x_min <= world_x <= x_max:
                data[(my * grid.width) + mx] = value
    return GridMap2D(
        resolution=grid.resolution,
        width=grid.width,
        height=grid.height,
        origin_x=grid.origin_x,
        origin_y=grid.origin_y,
        data=tuple(data),
    )


def test_centered_target_far_away_drives_forward() -> None:
    params = FollowControlParams()
    command = compute_nominal_follow_command(1.60, 0.0, params)

    assert command.vx > 0.20
    assert command.vy == pytest.approx(0.0)
    assert command.wz == pytest.approx(0.0)


def test_target_inside_standoff_band_holds_position() -> None:
    params = FollowControlParams()
    command = compute_nominal_follow_command(0.80, 0.03, params)

    assert command.vx == pytest.approx(0.0)
    assert command.vy == pytest.approx(0.0)
    assert command.wz == pytest.approx(0.0)


def test_target_too_close_allows_backing_up() -> None:
    params = FollowControlParams()
    command = compute_nominal_follow_command(0.25, 0.0, params)

    assert command.vx < 0.0
    assert command.vy == pytest.approx(0.0)


def test_large_bearing_prioritizes_fov_over_translation() -> None:
    params = FollowControlParams()
    command = compute_nominal_follow_command(1.20, 1.20, params)

    assert abs(command.wz) > 0.40
    assert abs(command.vx) < 0.05
    assert command.vy == pytest.approx(0.0)


def test_too_close_side_target_still_backs_up_while_turning() -> None:
    params = FollowControlParams()
    command = compute_nominal_follow_command(0.35, 0.30, params)

    assert command.vx < -0.05
    assert abs(command.wz) > 0.20
    assert command.vy == pytest.approx(0.0)


def test_blocked_forward_path_chooses_stop_over_collision() -> None:
    params = FollowControlParams()
    safety = SafetyOracleParams(horizon_s=0.8, sim_dt_s=0.1, occupied_threshold=55)
    nominal = compute_nominal_follow_command(1.60, 0.0, params)
    grid = _with_obstacle_band(_make_grid(), 0.52, 1.20, -0.35, 0.35)

    selected, safe = select_safe_command(nominal, Pose2D(), grid, safety)

    assert safe is True
    assert selected.vx == pytest.approx(0.0)
    assert selected.vy == pytest.approx(0.0)
    assert selected.wz == pytest.approx(0.0)


def test_brief_occlusion_enters_reacquire_without_sitting() -> None:
    machine = FollowStateMachine(reacquire_timeout_s=1.5, sit_on_loss_timeout_s=3.0)

    machine.handle_follow_command(0.0)
    machine.note_target_seen(0.2)
    state = machine.update(1.0, has_fresh_target=False)

    assert state == FollowStates.REACQUIRE
    assert machine.reacquire_motion_enabled(1.0) is True
    assert machine.update(2.8, has_fresh_target=False) == FollowStates.REACQUIRE


def test_sustained_loss_transitions_to_lost_sit() -> None:
    machine = FollowStateMachine(reacquire_timeout_s=1.5, sit_on_loss_timeout_s=3.0)

    machine.handle_follow_command(0.0)
    machine.note_target_seen(0.1)
    machine.update(0.8, has_fresh_target=False)

    assert machine.update(3.2, has_fresh_target=False) == FollowStates.LOST_SIT
