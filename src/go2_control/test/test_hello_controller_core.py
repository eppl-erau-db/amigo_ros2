from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from go2_control.hello_controller_core import (  # noqa: E402
    GreetedTargetRecord,
    HelloCandidate,
    HelloControlParams,
    compute_centering_yaw_rate,
    greeting_target_key,
    hello_session_limit_reached,
    record_greeted_target,
    select_hello_candidate,
    update_wave_dispatch_window,
)


def test_greeting_target_key_uses_memory_frame_position() -> None:
    candidate = HelloCandidate(
        base_x_m=1.0,
        base_y_m=0.0,
        base_z_m=0.0,
        memory_x_m=2.1,
        memory_y_m=-0.6,
        confidence=75.0,
        bbox_area_px=12000.0,
    )

    assert greeting_target_key(candidate, xy_bin_m=0.5) == (4, -1)


def test_select_hello_candidate_skips_recently_greeted_target() -> None:
    params = HelloControlParams(
        greeted_target_memory_s=30.0,
        greeted_target_xy_bin_m=0.75,
        greeted_target_match_radius_m=1.25,
    )
    greeted = HelloCandidate(
        base_x_m=1.0,
        base_y_m=0.0,
        base_z_m=0.0,
        memory_x_m=2.0,
        memory_y_m=1.0,
        confidence=90.0,
        bbox_area_px=14000.0,
    )
    fresh = HelloCandidate(
        base_x_m=1.3,
        base_y_m=0.2,
        base_z_m=0.0,
        memory_x_m=3.5,
        memory_y_m=-0.5,
        confidence=65.0,
        bbox_area_px=9000.0,
    )

    selected = select_hello_candidate(
        [greeted, fresh],
        [
            GreetedTargetRecord(
                memory_x_m=greeted.memory_x_m,
                memory_y_m=greeted.memory_y_m,
                greeted_at_s=100.0,
            )
        ],
        now_s=105.0,
        params=params,
    )

    assert selected == fresh


def test_select_hello_candidate_allows_same_area_after_memory_expires() -> None:
    params = HelloControlParams(
        greeted_target_memory_s=10.0,
        greeted_target_xy_bin_m=0.75,
        greeted_target_match_radius_m=1.25,
    )
    candidate = HelloCandidate(
        base_x_m=1.1,
        base_y_m=0.0,
        base_z_m=0.0,
        memory_x_m=2.0,
        memory_y_m=1.0,
        confidence=80.0,
        bbox_area_px=12000.0,
    )

    selected = select_hello_candidate(
        [candidate],
        [
            GreetedTargetRecord(
                memory_x_m=candidate.memory_x_m,
                memory_y_m=candidate.memory_y_m,
                greeted_at_s=100.0,
            )
        ],
        now_s=111.0,
        params=params,
    )

    assert selected == candidate


def test_select_hello_candidate_skips_same_person_despite_position_jitter() -> None:
    params = HelloControlParams(
        greeted_target_memory_s=30.0,
        greeted_target_match_radius_m=1.25,
    )
    jittered_same_person = HelloCandidate(
        base_x_m=1.0,
        base_y_m=0.1,
        base_z_m=0.0,
        memory_x_m=2.7,
        memory_y_m=1.4,
        confidence=88.0,
        bbox_area_px=13500.0,
    )

    selected = select_hello_candidate(
        [jittered_same_person],
        [
            GreetedTargetRecord(
                memory_x_m=2.0,
                memory_y_m=1.0,
                greeted_at_s=100.0,
            )
        ],
        now_s=105.0,
        params=params,
    )

    assert selected is None


def test_compute_centering_yaw_rate_respects_deadband_and_clamp() -> None:
    params = HelloControlParams(target_yaw_deadband_rad=0.10, yaw_gain=2.0, max_yaw_rate_radps=0.5)
    centered = HelloCandidate(
        base_x_m=1.0,
        base_y_m=0.05,
        base_z_m=0.0,
        memory_x_m=0.0,
        memory_y_m=0.0,
    )
    off_center = HelloCandidate(
        base_x_m=1.0,
        base_y_m=1.0,
        base_z_m=0.0,
        memory_x_m=0.0,
        memory_y_m=0.0,
    )

    assert compute_centering_yaw_rate(centered, params) == 0.0
    assert compute_centering_yaw_rate(off_center, params) == 0.5


def test_update_wave_dispatch_window_requires_a_stop_hold_before_dispatch() -> None:
    should_dispatch, pending_key, ready_at = update_wave_dispatch_window(
        (2, 3),
        None,
        0.0,
        now_s=10.0,
        stop_hold_s=0.75,
    )
    assert should_dispatch is False
    assert pending_key == (2, 3)
    assert ready_at == 10.75

    should_dispatch, pending_key, ready_at = update_wave_dispatch_window(
        (2, 3),
        pending_key,
        ready_at,
        now_s=10.80,
        stop_hold_s=0.75,
    )
    assert should_dispatch is True
    assert pending_key == (2, 3)
    assert ready_at == 10.75


def test_record_greeted_target_replaces_nearby_record() -> None:
    candidate = HelloCandidate(
        base_x_m=1.0,
        base_y_m=0.0,
        base_z_m=0.0,
        memory_x_m=2.4,
        memory_y_m=1.2,
        confidence=80.0,
        bbox_area_px=10000.0,
    )

    updated = record_greeted_target(
        [
            GreetedTargetRecord(memory_x_m=2.0, memory_y_m=1.0, greeted_at_s=100.0),
            GreetedTargetRecord(memory_x_m=5.0, memory_y_m=5.0, greeted_at_s=100.0),
        ],
        candidate,
        now_s=110.0,
        match_radius_m=1.0,
    )

    assert len(updated) == 2
    assert any(record.greeted_at_s == 110.0 for record in updated)
    assert any(record.memory_x_m == 5.0 and record.memory_y_m == 5.0 for record in updated)


def test_hello_session_limit_reached_at_maximum() -> None:
    assert hello_session_limit_reached(3, 3) is True
    assert hello_session_limit_reached(2, 3) is False


def test_hello_session_limit_reached_ignores_non_positive_limit() -> None:
    assert hello_session_limit_reached(3, 0) is False
    assert hello_session_limit_reached(10, -1) is False
