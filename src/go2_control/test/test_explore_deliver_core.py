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
    complete_deliver,
    request_voice_command,
    select_motion_routing,
)


def _standing_idle() -> SupervisorState:
    return SupervisorState(task_mode=TaskModes.IDLE, posture_mode=PostureModes.STANDING)


# --------------------------------------------------------------------- explore
def test_explore_from_idle_accepts_without_zero_motion() -> None:
    d = request_voice_command(_standing_idle(), "explore")
    assert d.accepted is True
    assert d.state.task_mode == TaskModes.EXPLORE
    assert d.state.motion_enabled is False
    assert SupervisorOps.START_EXPLORE in d.operations
    # Manual remote driving: the supervisor must NOT publish zero motion.
    assert SupervisorOps.PUBLISH_ZERO_MOTION not in d.operations


def test_explore_requires_standing() -> None:
    d = request_voice_command(SupervisorState(posture_mode=PostureModes.LAYING), "explore")
    assert d.accepted is False


def test_explore_does_not_route_motion() -> None:
    routing = select_motion_routing(
        SupervisorState(task_mode=TaskModes.EXPLORE, motion_enabled=False))
    assert routing == MotionRouting()


def test_done_exploring_saves_and_returns_idle() -> None:
    explore = request_voice_command(_standing_idle(), "explore").state
    d = request_voice_command(explore, "done_exploring")
    assert d.accepted is True
    assert d.state.task_mode == TaskModes.IDLE
    assert SupervisorOps.SAVE_EXPLORE_MAP in d.operations


def test_done_exploring_rejected_when_not_exploring() -> None:
    d = request_voice_command(_standing_idle(), "done_exploring")
    assert d.accepted is False


# --------------------------------------------------------------------- deliver
def test_deliver_from_idle_accepts_and_starts() -> None:
    d = request_voice_command(_standing_idle(), "deliver_swag")
    assert d.accepted is True
    assert d.state.task_mode == TaskModes.DELIVER
    assert d.state.motion_enabled is True
    assert SupervisorOps.START_DELIVER in d.operations


def test_deliver_routes_through_nav() -> None:
    routing = select_motion_routing(
        SupervisorState(task_mode=TaskModes.DELIVER, motion_enabled=True))
    assert routing == MotionRouting(base_source="nav")


def test_deliver_requires_standing() -> None:
    d = request_voice_command(SupervisorState(posture_mode=PostureModes.LAYING), "deliver_swag")
    assert d.accepted is False


def test_deliver_already_active_is_rejected() -> None:
    active = SupervisorState(task_mode=TaskModes.DELIVER, motion_enabled=True)
    d = request_voice_command(active, "deliver_swag")
    assert d.accepted is False


def test_idle_cancels_active_delivery() -> None:
    active = SupervisorState(task_mode=TaskModes.DELIVER, motion_enabled=True)
    d = request_voice_command(active, "stay")  # stop_follow -> IDLE
    assert d.accepted is True
    assert SupervisorOps.CANCEL_DELIVER in d.operations
    assert d.state.pending_task_mode == TaskModes.IDLE
    # complete_deliver then lands in IDLE.
    assert complete_deliver(d.state).task_mode == TaskModes.IDLE


def test_follow_preempts_delivery_then_completes_to_follow() -> None:
    active = SupervisorState(task_mode=TaskModes.DELIVER, motion_enabled=True)
    d = request_voice_command(active, "follow_me")
    assert d.accepted is True
    assert SupervisorOps.CANCEL_DELIVER in d.operations
    assert d.state.pending_task_mode == TaskModes.FOLLOW
    final = complete_deliver(d.state)
    assert final.task_mode == TaskModes.FOLLOW
    assert final.motion_enabled is True


def test_lay_down_cancels_active_delivery() -> None:
    active = SupervisorState(task_mode=TaskModes.DELIVER, motion_enabled=True)
    d = request_voice_command(active, "lay_down")
    assert d.accepted is True
    assert SupervisorOps.CANCEL_DELIVER in d.operations
    assert d.state.posture_mode == PostureModes.TRANSITION_TO_LAY


def test_complete_deliver_default_returns_idle() -> None:
    active = SupervisorState(task_mode=TaskModes.DELIVER, motion_enabled=True)
    assert complete_deliver(active).task_mode == TaskModes.IDLE


# ----------------------------------------------------------------- handoff
def test_handoff_done_while_delivering_signals_without_mode_change() -> None:
    active = SupervisorState(task_mode=TaskModes.DELIVER, motion_enabled=True)
    d = request_voice_command(active, "handoff_done")
    assert d.accepted is True
    assert d.state.task_mode == TaskModes.DELIVER  # stays DELIVER
    assert SupervisorOps.SIGNAL_HANDOFF_DONE in d.operations


def test_handoff_done_rejected_when_not_delivering() -> None:
    d = request_voice_command(_standing_idle(), "handoff_done")
    assert d.accepted is False


# ----------------------------------------------------- cross-task exclusivity
def test_deliver_rejected_while_search_active() -> None:
    search = SupervisorState(task_mode=TaskModes.SEARCH, motion_enabled=True)
    assert request_voice_command(search, "deliver_swag").accepted is False


def test_search_rejected_while_delivery_active() -> None:
    deliver = SupervisorState(task_mode=TaskModes.DELIVER, motion_enabled=True)
    assert request_voice_command(deliver, "search").accepted is False


def test_explore_rejected_while_delivery_active() -> None:
    deliver = SupervisorState(task_mode=TaskModes.DELIVER, motion_enabled=True)
    assert request_voice_command(deliver, "explore").accepted is False


# ------------------------------------------------- existing behavior intact
def test_existing_follow_still_works() -> None:
    d = request_voice_command(_standing_idle(), "follow_me")
    assert d.accepted is True and d.state.task_mode == TaskModes.FOLLOW


def test_existing_search_still_works() -> None:
    d = request_voice_command(_standing_idle(), "search")
    assert d.accepted is True and d.state.task_mode == TaskModes.SEARCH
    assert SupervisorOps.START_SEARCH in d.operations
