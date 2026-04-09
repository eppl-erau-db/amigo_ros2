from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from go2_control.mission_supervisor_core import (  # noqa: E402
    PostureModes,
    SupervisorOps,
    SupervisorState,
    TaskModes,
    complete_explore_area,
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


def test_explore_then_follow_waits_for_explore_completion() -> None:
    explore = request_voice_command(SupervisorState(), "explore_area")
    assert explore.accepted is True
    assert explore.state.task_mode == TaskModes.EXPLORE

    follow = request_voice_command(explore.state, "follow_me", allow_preempt=True)
    assert follow.accepted is True
    assert follow.state.task_mode == TaskModes.EXPLORE
    assert follow.state.pending_task_mode == TaskModes.FOLLOW
    assert follow.state.motion_enabled is False
    assert SupervisorOps.CANCEL_EXPLORE_AREA in follow.operations

    completed = complete_explore_area(follow.state, detail="explore_canceled_for_follow")
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


def test_search_then_say_hello_waits_for_search_completion() -> None:
    search = request_voice_command(SupervisorState(), "search")
    assert search.accepted is True

    hello = request_voice_command(search.state, "say_hello", allow_preempt=True)
    assert hello.accepted is True
    assert hello.state.task_mode == TaskModes.SEARCH
    assert hello.state.pending_task_mode == TaskModes.HELLO
    assert hello.state.motion_enabled is False
    assert SupervisorOps.CANCEL_SEARCH in hello.operations

    completed = complete_search(hello.state, detail="search_canceled_for_hello")
    assert completed.task_mode == TaskModes.HELLO
    assert completed.motion_enabled is True


def test_search_then_wake_attention_waits_for_search_completion() -> None:
    search = request_voice_command(SupervisorState(), "search")
    assert search.accepted is True

    wake_attention = request_voice_command(search.state, "wake_attention", allow_preempt=True)
    assert wake_attention.accepted is True
    assert wake_attention.state.task_mode == TaskModes.SEARCH
    assert wake_attention.state.pending_task_mode == TaskModes.ATTEND
    assert wake_attention.state.motion_enabled is False
    assert SupervisorOps.CANCEL_SEARCH in wake_attention.operations

    completed = complete_search(wake_attention.state, detail="search_canceled_for_attention")
    assert completed.task_mode == TaskModes.ATTEND
    assert completed.motion_enabled is True


def test_search_then_ready_waits_for_search_completion() -> None:
    search = request_voice_command(SupervisorState(), "search")
    assert search.accepted is True

    ready = request_voice_command(search.state, "ready", allow_preempt=True)
    assert ready.accepted is True
    assert ready.state.task_mode == TaskModes.SEARCH
    assert ready.state.pending_task_mode == TaskModes.READY
    assert ready.state.motion_enabled is False
    assert SupervisorOps.CANCEL_SEARCH in ready.operations

    completed = complete_search(ready.state, detail="search_canceled_for_ready")
    assert completed.task_mode == TaskModes.READY
    assert completed.motion_enabled is True


def test_search_then_upright_waits_for_search_completion() -> None:
    search = request_voice_command(SupervisorState(), "search")
    assert search.accepted is True

    upright = request_voice_command(search.state, "walk_upright", allow_preempt=True)
    assert upright.accepted is True
    assert upright.state.task_mode == TaskModes.SEARCH
    assert upright.state.pending_task_mode == TaskModes.UPRIGHT
    assert upright.state.motion_enabled is False
    assert SupervisorOps.CANCEL_SEARCH in upright.operations

    completed = complete_search(upright.state, detail="search_canceled_for_upright")
    assert completed.task_mode == TaskModes.UPRIGHT
    assert completed.motion_enabled is True


def test_follow_then_say_hello_switches_immediately() -> None:
    follow = request_voice_command(SupervisorState(), "follow_me")
    assert follow.accepted is True

    hello = request_voice_command(follow.state, "say_hello", allow_preempt=True)
    assert hello.accepted is True
    assert hello.state.task_mode == TaskModes.HELLO
    assert hello.state.motion_enabled is True


def test_search_then_stay_cancels_search_and_returns_idle() -> None:
    search = request_voice_command(SupervisorState(), "search")
    assert search.accepted is True

    stay = request_voice_command(search.state, "stay", allow_preempt=True)
    assert stay.accepted is True
    assert stay.state.task_mode == TaskModes.SEARCH
    assert stay.state.pending_task_mode == TaskModes.IDLE
    assert stay.state.motion_enabled is False
    assert SupervisorOps.CANCEL_SEARCH in stay.operations

    completed = complete_search(stay.state, detail="search_canceled_for_stay")
    assert completed.task_mode == TaskModes.IDLE
    assert completed.motion_enabled is False


def test_say_hello_then_stay_returns_idle() -> None:
    hello = request_voice_command(SupervisorState(), "say_hello")
    assert hello.accepted is True

    stay = request_voice_command(hello.state, "stay", allow_preempt=True)
    assert stay.accepted is True
    assert stay.state.task_mode == TaskModes.IDLE
    assert stay.state.motion_enabled is False


def test_ready_then_upright_switches_immediately() -> None:
    ready = request_voice_command(SupervisorState(), "ready")
    assert ready.accepted is True

    upright = request_voice_command(ready.state, "up", allow_preempt=True)
    assert upright.accepted is True
    assert upright.state.task_mode == TaskModes.UPRIGHT
    assert upright.state.motion_enabled is True


def test_upright_then_stay_returns_idle() -> None:
    upright = request_voice_command(SupervisorState(), "walk_upright")
    assert upright.accepted is True

    stay = request_voice_command(upright.state, "stay", allow_preempt=True)
    assert stay.accepted is True
    assert stay.state.task_mode == TaskModes.IDLE
    assert stay.state.motion_enabled is False


def test_upright_then_down_returns_idle_instead_of_laying() -> None:
    upright = request_voice_command(SupervisorState(), "walk_upright")
    assert upright.accepted is True

    down = request_voice_command(upright.state, "lay_down", allow_preempt=True)
    assert down.accepted is True
    assert down.state.task_mode == TaskModes.IDLE
    assert down.state.posture_mode == PostureModes.STANDING
    assert down.state.motion_enabled is False


def test_hello_amigo_is_rejected_while_search_is_active() -> None:
    search = request_voice_command(SupervisorState(), "search")
    assert search.accepted is True

    hello_amigo = request_voice_command(search.state, "hello_amigo", allow_preempt=True)
    assert hello_amigo.accepted is False
    assert hello_amigo.state == search.state
