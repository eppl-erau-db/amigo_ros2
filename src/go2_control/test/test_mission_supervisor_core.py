from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from go2_control.mission_supervisor_core import (  # noqa: E402
    MotionRouting,
    PostureModes,
    SupervisorOps,
    SupervisorState,
    TaskModes,
    complete_explore_area,
    complete_posture_transition,
    complete_search,
    request_mode_change,
    request_voice_command,
    select_motion_routing,
)


def test_follow_request_from_idle_is_accepted() -> None:
    decision = request_voice_command(SupervisorState(), "follow_me")

    assert decision.accepted is True
    assert decision.state.task_mode == TaskModes.FOLLOW
    assert decision.state.posture_mode == PostureModes.STANDING
    assert decision.state.motion_enabled is True
    assert SupervisorOps.PUBLISH_ZERO_MOTION in decision.operations


def test_follow_request_while_laying_is_rejected() -> None:
    state = SupervisorState(posture_mode=PostureModes.LAYING)
    decision = request_voice_command(state, "follow_me")

    assert decision.accepted is False
    assert decision.state == state


def test_wake_attention_request_from_idle_is_accepted() -> None:
    decision = request_voice_command(SupervisorState(), "wake_attention")

    assert decision.accepted is True
    assert decision.state.task_mode == TaskModes.ATTEND
    assert decision.state.posture_mode == PostureModes.STANDING
    assert decision.state.motion_enabled is True
    assert SupervisorOps.PUBLISH_ZERO_MOTION in decision.operations


def test_ready_request_from_idle_is_accepted() -> None:
    decision = request_voice_command(SupervisorState(), "ready")

    assert decision.accepted is True
    assert decision.state.task_mode == TaskModes.READY
    assert decision.state.posture_mode == PostureModes.STANDING
    assert decision.state.motion_enabled is True
    assert SupervisorOps.PUBLISH_ZERO_MOTION in decision.operations


def test_walk_upright_request_from_idle_is_accepted() -> None:
    decision = request_voice_command(SupervisorState(), "walk_upright")

    assert decision.accepted is True
    assert decision.state.task_mode == TaskModes.UPRIGHT
    assert decision.state.posture_mode == PostureModes.STANDING
    assert decision.state.motion_enabled is True
    assert SupervisorOps.PUBLISH_ZERO_MOTION in decision.operations


def test_walk_upright_request_while_laying_is_rejected() -> None:
    state = SupervisorState(posture_mode=PostureModes.LAYING)
    decision = request_voice_command(state, "up")

    assert decision.accepted is False
    assert decision.state == state


def test_stand_up_request_only_allowed_while_laying() -> None:
    standing_reject = request_voice_command(SupervisorState(), "stand_up")
    laying_accept = request_voice_command(
        SupervisorState(posture_mode=PostureModes.LAYING),
        "stand_up",
    )

    assert standing_reject.accepted is False
    assert laying_accept.accepted is True
    assert laying_accept.state.posture_mode == PostureModes.TRANSITION_TO_STAND
    assert SupervisorOps.SEND_STAND_UP in laying_accept.operations


def test_say_hello_request_from_idle_is_accepted() -> None:
    decision = request_voice_command(SupervisorState(), "say_hello")

    assert decision.accepted is True
    assert decision.state.task_mode == TaskModes.HELLO
    assert decision.state.posture_mode == PostureModes.STANDING
    assert decision.state.motion_enabled is True
    assert SupervisorOps.PUBLISH_ZERO_MOTION in decision.operations


def test_explore_request_from_idle_is_accepted() -> None:
    decision = request_voice_command(SupervisorState(), "explore_area")

    assert decision.accepted is True
    assert decision.state.task_mode == TaskModes.EXPLORE
    assert decision.state.posture_mode == PostureModes.STANDING
    assert decision.state.motion_enabled is True
    assert SupervisorOps.START_EXPLORE_AREA in decision.operations


def test_hello_amigo_request_from_idle_is_accepted_as_one_shot() -> None:
    decision = request_voice_command(SupervisorState(), "hello_amigo")

    assert decision.accepted is True
    assert decision.state.task_mode == TaskModes.IDLE
    assert decision.state.posture_mode == PostureModes.STANDING
    assert decision.state.motion_enabled is False
    assert SupervisorOps.PUBLISH_ZERO_MOTION in decision.operations
    assert SupervisorOps.SEND_HELLO_IF_PERSON_VISIBLE in decision.operations


def test_say_hello_request_while_laying_is_rejected() -> None:
    state = SupervisorState(
        posture_mode=PostureModes.LAYING,
    )
    decision = request_voice_command(state, "say_hello")

    assert decision.accepted is False
    assert decision.state == state


def test_hello_amigo_request_while_following_is_rejected() -> None:
    state = SupervisorState(
        task_mode=TaskModes.FOLLOW,
        posture_mode=PostureModes.STANDING,
        motion_enabled=True,
    )
    decision = request_voice_command(state, "hello_amigo")

    assert decision.accepted is False
    assert decision.state == state


def test_select_motion_routing_for_legacy_follow_uses_base_cmd_vel() -> None:
    routing = select_motion_routing(
        SupervisorState(task_mode=TaskModes.FOLLOW, motion_enabled=True),
        follow_backend="legacy",
    )

    assert routing == MotionRouting(base_source="follow")


def test_select_motion_routing_for_unitree_follow_uses_bridge_topic() -> None:
    routing = select_motion_routing(
        SupervisorState(task_mode=TaskModes.FOLLOW, motion_enabled=True),
        follow_backend="sport_free_avoid",
    )

    assert routing == MotionRouting(follow_bridge_source="follow")


def test_select_motion_routing_for_hello_uses_base_cmd_vel() -> None:
    routing = select_motion_routing(
        SupervisorState(task_mode=TaskModes.HELLO, motion_enabled=True),
        follow_backend="sport_free_avoid",
    )

    assert routing == MotionRouting(base_source="hello")


def test_select_motion_routing_for_explore_uses_base_cmd_vel() -> None:
    routing = select_motion_routing(
        SupervisorState(task_mode=TaskModes.EXPLORE, motion_enabled=True),
        follow_backend="sport_free_avoid",
    )

    assert routing == MotionRouting(base_source="nav")


def test_select_motion_routing_for_attention_uses_base_cmd_vel() -> None:
    routing = select_motion_routing(
        SupervisorState(task_mode=TaskModes.ATTEND, motion_enabled=True),
        follow_backend="sport_free_avoid",
    )

    assert routing == MotionRouting(base_source="attention")


def test_select_motion_routing_for_ready_and_upright_uses_no_base_cmd_vel() -> None:
    ready_routing = select_motion_routing(
        SupervisorState(task_mode=TaskModes.READY, motion_enabled=True),
        follow_backend="sport_free_avoid",
    )
    upright_routing = select_motion_routing(
        SupervisorState(task_mode=TaskModes.UPRIGHT, motion_enabled=True),
        follow_backend="sport_free_avoid",
    )

    assert ready_routing == MotionRouting()
    assert upright_routing == MotionRouting()
