from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from go2_control.mission_supervisor_core import (  # noqa: E402
    PostureModes,
    SupervisorOps,
    SupervisorState,
    TaskModes,
    complete_posture_transition,
    complete_search,
    request_voice_command,
    select_motion_routing,
)


def test_follow_then_lay_down_sequence_stops_motion_and_ends_laying() -> None:
    follow = request_voice_command(SupervisorState(), "follow_me")
    assert follow.accepted is True
    assert select_motion_routing(follow.state).base_source == "follow"

    lay_down = request_voice_command(follow.state, "lay_down")
    assert lay_down.accepted is True
    assert lay_down.state.posture_mode == PostureModes.TRANSITION_TO_LAY
    assert lay_down.state.motion_enabled is False
    assert SupervisorOps.PUBLISH_ZERO_MOTION in lay_down.operations
    assert SupervisorOps.SEND_STAND_DOWN in lay_down.operations
    assert select_motion_routing(lay_down.state).base_source is None

    final_state = complete_posture_transition(
        lay_down.state,
        success=True,
        detail="robot_is_laying",
    )
    assert final_state.posture_mode == PostureModes.LAYING
    assert final_state.task_mode == TaskModes.IDLE


def test_search_then_follow_waits_for_search_completion() -> None:
    search = request_voice_command(SupervisorState(), "search")
    assert search.accepted is True
    assert search.state.task_mode == TaskModes.SEARCH

    follow = request_voice_command(search.state, "follow_me", allow_preempt=True)
    assert follow.accepted is True
    assert follow.state.task_mode == TaskModes.SEARCH
    assert follow.state.pending_task_mode == TaskModes.FOLLOW
    assert follow.state.motion_enabled is False
    assert SupervisorOps.CANCEL_SEARCH in follow.operations

    completed = complete_search(follow.state, detail="search_canceled_for_follow")
    assert completed.task_mode == TaskModes.FOLLOW
    assert completed.motion_enabled is True


def test_search_then_lay_down_cancels_search_and_ignores_late_result() -> None:
    search = request_voice_command(SupervisorState(), "search")
    assert search.accepted is True

    lay_down = request_voice_command(search.state, "lay_down", allow_preempt=True)
    assert lay_down.accepted is True
    assert lay_down.state.task_mode == TaskModes.IDLE
    assert lay_down.state.posture_mode == PostureModes.TRANSITION_TO_LAY
    assert SupervisorOps.CANCEL_SEARCH in lay_down.operations

    final_state = complete_posture_transition(
        lay_down.state,
        success=True,
        detail="robot_is_laying",
    )
    late_search_result = complete_search(final_state, detail="late_search_result")
    assert late_search_result.posture_mode == PostureModes.LAYING
    assert late_search_result.task_mode == TaskModes.IDLE


def test_search_then_shake_hand_is_rejected_until_robot_returns_idle() -> None:
    search = request_voice_command(SupervisorState(), "search")
    assert search.accepted is True

    shake_hand = request_voice_command(search.state, "shake_hand", allow_preempt=True)
    assert shake_hand.accepted is False
    assert shake_hand.state == search.state
