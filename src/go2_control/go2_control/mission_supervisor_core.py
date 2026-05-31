from __future__ import annotations

from dataclasses import dataclass, replace

from go2_control.behavior_registry import BUILTIN_BEHAVIORS


class TaskModes:
    IDLE = "IDLE"
    FOLLOW = "FOLLOW"
    SEARCH = "SEARCH"


class PostureModes:
    STANDING = "STANDING"
    LAYING = "LAYING"
    TRANSITION_TO_STAND = "TRANSITION_TO_STAND"
    TRANSITION_TO_LAY = "TRANSITION_TO_LAY"


class VoiceCommands:
    FOLLOW = "follow_me"
    STOP_FOLLOW = "stop_follow"
    SEARCH = "search"
    SHAKE_HAND = "shake_hand"
    LAY_DOWN = "lay_down"
    STAND_UP = "stand_up"


class SupervisorOps:
    PUBLISH_ZERO_MOTION = "publish_zero_motion"
    START_SEARCH = "start_search"
    CANCEL_SEARCH = "cancel_search"
    SEND_HELLO = "send_hello"
    SEND_STAND_DOWN = "send_stand_down"
    SEND_STAND_UP = "send_stand_up"


@dataclass(frozen=True)
class SupervisorState:
    task_mode: str = TaskModes.IDLE
    posture_mode: str = PostureModes.STANDING
    motion_enabled: bool = False
    transition_id: int = 0
    source: str = ""
    detail: str = ""
    pending_task_mode: str | None = None
    faulted: bool = False


@dataclass(frozen=True)
class TransitionDecision:
    accepted: bool
    state: SupervisorState
    operations: tuple[str, ...]
    message: str


@dataclass(frozen=True)
class MotionRouting:
    base_source: str | None = None
    follow_bridge_source: str | None = None


def normalize_task_mode(raw_mode: str | None) -> str | None:
    if raw_mode is None:
        return None
    token = str(raw_mode).strip().upper()
    if not token:
        return None
    if token in {"IDLE", "STOP"}:
        return TaskModes.IDLE
    if token in {"FOLLOW", "FOLLOW_ME", "PERSON_FOLLOW"}:
        return TaskModes.FOLLOW
    if token in {"SEARCH"}:
        return TaskModes.SEARCH
    return token


def normalize_posture_mode(raw_mode: str | None) -> str | None:
    if raw_mode is None:
        return None
    token = str(raw_mode).strip().upper()
    if not token:
        return None
    if token in {"STANDING", "STAND", "UP"}:
        return PostureModes.STANDING
    if token in {"LAYING", "LYING", "LAY", "DOWN"}:
        return PostureModes.LAYING
    return token


def normalize_voice_command(raw_command: str | None) -> str:
    if raw_command is None:
        return ""
    token = str(raw_command).strip().lower()
    if not token:
        return ""
    if token in {"follow", "follow_me", "person_follow"}:
        return VoiceCommands.FOLLOW
    if token in {"stop_follow", "stop", "stay"}:
        return VoiceCommands.STOP_FOLLOW
    if token in {"search", "look_for_a_leak"}:
        return VoiceCommands.SEARCH
    if token in {"shake_hand", "shake hand", "hello", "say_hello", "say hello"}:
        return VoiceCommands.SHAKE_HAND
    if token in {"lay_down", "lie_down"}:
        return VoiceCommands.LAY_DOWN
    if token in {"stand_up", "get_up"}:
        return VoiceCommands.STAND_UP
    return token


def _accepted(
    state: SupervisorState,
    source: str,
    detail: str,
    operations: tuple[str, ...],
    message: str,
) -> TransitionDecision:
    return TransitionDecision(
        accepted=True,
        state=replace(
            state,
            transition_id=state.transition_id + 1,
            source=source,
            detail=detail,
        ),
        operations=operations,
        message=message,
    )


def _rejected(state: SupervisorState, message: str) -> TransitionDecision:
    return TransitionDecision(
        accepted=False,
        state=state,
        operations=(),
        message=message,
    )


def request_voice_command(
    state: SupervisorState,
    command: str,
    *,
    source: str = "voice",
    allow_preempt: bool = True,
) -> TransitionDecision:
    normalized = normalize_voice_command(command)
    if normalized == VoiceCommands.FOLLOW:
        return request_mode_change(
            state,
            requested_task_mode=TaskModes.FOLLOW,
            source=source,
            allow_preempt=allow_preempt,
        )
    if normalized == VoiceCommands.STOP_FOLLOW:
        return request_mode_change(
            state,
            requested_task_mode=TaskModes.IDLE,
            source=source,
            allow_preempt=allow_preempt,
        )
    if normalized == VoiceCommands.SEARCH:
        return request_mode_change(
            state,
            requested_task_mode=TaskModes.SEARCH,
            source=source,
            allow_preempt=allow_preempt,
        )
    if normalized == VoiceCommands.SHAKE_HAND:
        return _request_shake_hand(state, source)
    if normalized == VoiceCommands.LAY_DOWN:
        return request_mode_change(
            state,
            requested_posture_mode=PostureModes.LAYING,
            source=source,
            allow_preempt=allow_preempt,
        )
    if normalized == VoiceCommands.STAND_UP:
        return request_mode_change(
            state,
            requested_posture_mode=PostureModes.STANDING,
            source=source,
            allow_preempt=allow_preempt,
        )
    return _rejected(state, f'Unsupported voice command "{command}".')


def request_mode_change(
    state: SupervisorState,
    *,
    requested_task_mode: str | None = None,
    requested_posture_mode: str | None = None,
    source: str = "external",
    allow_preempt: bool = True,
) -> TransitionDecision:
    if state.faulted:
        return _rejected(state, "Supervisor is faulted and cannot accept new requests.")

    task_mode = normalize_task_mode(requested_task_mode)
    posture_mode = normalize_posture_mode(requested_posture_mode)

    if task_mode and posture_mode:
        if posture_mode == PostureModes.LAYING and task_mode == TaskModes.IDLE:
            return _request_posture(state, posture_mode, source, allow_preempt)
        if posture_mode == PostureModes.STANDING and task_mode == TaskModes.IDLE:
            return _request_posture(state, posture_mode, source, allow_preempt)
        return _rejected(
            state,
            (
                "Combined task/posture requests are only supported for "
                "IDLE+LAYING and IDLE+STANDING in phase 1."
            ),
        )

    if posture_mode:
        return _request_posture(state, posture_mode, source, allow_preempt)
    if task_mode:
        return _request_task(state, task_mode, source, allow_preempt)

    return _rejected(state, "No task_mode or posture_mode was requested.")


def _request_shake_hand(
    state: SupervisorState,
    source: str,
) -> TransitionDecision:
    if state.faulted:
        return _rejected(state, "Supervisor is faulted and cannot accept new requests.")

    if state.posture_mode != PostureModes.STANDING:
        return _rejected(
            state,
            "Shake-hand is only allowed while the robot is standing.",
        )

    if state.pending_task_mode is not None:
        return _rejected(
            state,
            "Shake-hand is unavailable while a task transition is pending.",
        )

    if state.task_mode != TaskModes.IDLE or state.motion_enabled:
        return _rejected(
            state,
            "Shake-hand requires the robot to be idle.",
        )

    return _accepted(
        replace(
            state,
            task_mode=TaskModes.IDLE,
            motion_enabled=False,
            pending_task_mode=None,
        ),
        source,
        "shake_hand_requested",
        (
            SupervisorOps.PUBLISH_ZERO_MOTION,
            SupervisorOps.SEND_HELLO,
        ),
        "Executing shake-hand gesture.",
    )


def _request_task(
    state: SupervisorState,
    task_mode: str,
    source: str,
    allow_preempt: bool,
) -> TransitionDecision:
    if task_mode not in {TaskModes.IDLE, TaskModes.FOLLOW, TaskModes.SEARCH}:
        return _rejected(state, f'Unsupported task mode "{task_mode}".')

    if task_mode == TaskModes.IDLE:
        if state.task_mode == TaskModes.SEARCH:
            if not allow_preempt:
                return _rejected(state, "Search is active and preemption is disabled.")
            return _accepted(
                replace(state, motion_enabled=False, pending_task_mode=TaskModes.IDLE),
                source,
                "canceling_search_for_idle",
                (
                    SupervisorOps.PUBLISH_ZERO_MOTION,
                    SupervisorOps.CANCEL_SEARCH,
                ),
                "Canceling Search and returning to IDLE.",
            )

        if state.task_mode == TaskModes.IDLE and state.pending_task_mode is None and not state.motion_enabled:
            return _rejected(state, "Robot is already idle.")

        return _accepted(
            replace(
                state,
                task_mode=TaskModes.IDLE,
                motion_enabled=False,
                pending_task_mode=None,
            ),
            source,
            "idle_active",
            (SupervisorOps.PUBLISH_ZERO_MOTION,),
            "Robot task mode is now IDLE.",
        )

    if state.posture_mode != PostureModes.STANDING:
        return _rejected(
            state,
            f"Task mode {task_mode} requires posture {PostureModes.STANDING}.",
        )

    if task_mode == TaskModes.FOLLOW:
        if state.task_mode == TaskModes.FOLLOW and state.pending_task_mode is None and state.motion_enabled:
            return _rejected(state, "Follow mode is already active.")

        if state.task_mode == TaskModes.SEARCH:
            if not allow_preempt:
                return _rejected(state, "Search is active and preemption is disabled.")
            return _accepted(
                replace(
                    state,
                    motion_enabled=False,
                    pending_task_mode=TaskModes.FOLLOW,
                ),
                source,
                "canceling_search_for_follow",
                (
                    SupervisorOps.PUBLISH_ZERO_MOTION,
                    SupervisorOps.CANCEL_SEARCH,
                ),
                "Canceling Search before enabling Follow.",
            )

        return _accepted(
            replace(
                state,
                task_mode=TaskModes.FOLLOW,
                motion_enabled=True,
                pending_task_mode=None,
            ),
            source,
            "follow_active",
            (SupervisorOps.PUBLISH_ZERO_MOTION,),
            "Follow mode is now active.",
        )

    if state.task_mode == TaskModes.SEARCH and state.pending_task_mode is None and state.motion_enabled:
        return _rejected(state, "Search mode is already active.")

    return _accepted(
        replace(
            state,
            task_mode=TaskModes.SEARCH,
            motion_enabled=True,
            pending_task_mode=None,
        ),
        source,
        "search_active",
        (
            SupervisorOps.PUBLISH_ZERO_MOTION,
            SupervisorOps.START_SEARCH,
        ),
        "Search mode is now active.",
    )


def _request_posture(
    state: SupervisorState,
    posture_mode: str,
    source: str,
    allow_preempt: bool,
) -> TransitionDecision:
    if posture_mode not in {PostureModes.STANDING, PostureModes.LAYING}:
        return _rejected(state, f'Unsupported posture mode "{posture_mode}".')

    if posture_mode == PostureModes.LAYING:
        if state.posture_mode == PostureModes.LAYING and state.task_mode == TaskModes.IDLE:
            return _rejected(state, "Robot is already laying down.")

        operations = [SupervisorOps.PUBLISH_ZERO_MOTION]
        if state.task_mode == TaskModes.SEARCH and allow_preempt:
            operations.append(SupervisorOps.CANCEL_SEARCH)

        operations.append(SupervisorOps.SEND_STAND_DOWN)

        return _accepted(
            replace(
                state,
                task_mode=TaskModes.IDLE,
                posture_mode=PostureModes.TRANSITION_TO_LAY,
                motion_enabled=False,
                pending_task_mode=None,
            ),
            source,
            "lay_down_requested",
            tuple(operations),
            "Transitioning to LAYING.",
        )

    if (
        state.posture_mode == PostureModes.STANDING
        and state.task_mode == TaskModes.IDLE
        and not state.motion_enabled
        and state.pending_task_mode is None
    ):
        return _accepted(
            replace(
                state,
                task_mode=TaskModes.IDLE,
                posture_mode=PostureModes.TRANSITION_TO_STAND,
                motion_enabled=False,
                pending_task_mode=None,
            ),
            source,
            "stand_up_recovery_requested",
            (
                SupervisorOps.PUBLISH_ZERO_MOTION,
                SupervisorOps.SEND_STAND_UP,
            ),
            "Reissuing stand-up command.",
        )

    if state.posture_mode != PostureModes.LAYING:
        return _rejected(
            state,
            "Stand-up is only allowed while the robot is laying down.",
        )

    return _accepted(
        replace(
            state,
            task_mode=TaskModes.IDLE,
            posture_mode=PostureModes.TRANSITION_TO_STAND,
            motion_enabled=False,
            pending_task_mode=None,
        ),
        source,
        "stand_up_requested",
        (
            SupervisorOps.PUBLISH_ZERO_MOTION,
            SupervisorOps.SEND_STAND_UP,
        ),
        "Transitioning to STANDING.",
    )


def complete_search(state: SupervisorState, *, detail: str = "") -> SupervisorState:
    if state.faulted:
        return state

    if state.pending_task_mode == TaskModes.FOLLOW:
        return replace(
            state,
            task_mode=TaskModes.FOLLOW,
            motion_enabled=state.posture_mode == PostureModes.STANDING,
            pending_task_mode=None,
            transition_id=state.transition_id + 1,
            detail=detail or "follow_active_after_search_cancel",
        )

    if state.pending_task_mode == TaskModes.IDLE:
        return replace(
            state,
            task_mode=TaskModes.IDLE,
            motion_enabled=False,
            pending_task_mode=None,
            transition_id=state.transition_id + 1,
            detail=detail or "idle_after_search_cancel",
        )

    if state.task_mode != TaskModes.SEARCH:
        return state

    return replace(
        state,
        task_mode=TaskModes.IDLE,
        motion_enabled=False,
        transition_id=state.transition_id + 1,
        detail=detail or "search_finished",
    )


def complete_posture_transition(
    state: SupervisorState,
    *,
    success: bool,
    detail: str = "",
) -> SupervisorState:
    if state.posture_mode == PostureModes.TRANSITION_TO_LAY:
        if success:
            return replace(
                state,
                posture_mode=PostureModes.LAYING,
                task_mode=TaskModes.IDLE,
                motion_enabled=False,
                transition_id=state.transition_id + 1,
                detail=detail or "robot_is_laying",
            )
        return enter_fault(state, detail or "lay_down_transition_failed")

    if state.posture_mode == PostureModes.TRANSITION_TO_STAND:
        if success:
            return replace(
                state,
                posture_mode=PostureModes.STANDING,
                task_mode=TaskModes.IDLE,
                motion_enabled=False,
                transition_id=state.transition_id + 1,
                detail=detail or "robot_is_standing",
            )
        return enter_fault(state, detail or "stand_up_transition_failed")

    return state


def sync_observed_posture(
    state: SupervisorState,
    posture_mode: str,
    *,
    source: str = "robot_state",
    detail: str = "",
) -> SupervisorState:
    observed_posture = normalize_posture_mode(posture_mode)
    if observed_posture not in {PostureModes.STANDING, PostureModes.LAYING}:
        return state

    if state.posture_mode in {
        PostureModes.TRANSITION_TO_LAY,
        PostureModes.TRANSITION_TO_STAND,
    }:
        return state

    if state.posture_mode == observed_posture:
        return state

    next_task_mode = state.task_mode
    next_motion_enabled = state.motion_enabled
    next_pending_task_mode = state.pending_task_mode
    if observed_posture == PostureModes.LAYING:
        next_task_mode = TaskModes.IDLE
        next_motion_enabled = False
        next_pending_task_mode = None

    return replace(
        state,
        task_mode=next_task_mode,
        posture_mode=observed_posture,
        motion_enabled=next_motion_enabled,
        pending_task_mode=next_pending_task_mode,
        transition_id=state.transition_id + 1,
        source=source,
        detail=detail or f"observed_posture_{observed_posture.lower()}",
    )


def enter_fault(state: SupervisorState, detail: str) -> SupervisorState:
    return replace(
        state,
        task_mode=TaskModes.IDLE,
        motion_enabled=False,
        pending_task_mode=None,
        transition_id=state.transition_id + 1,
        detail=detail,
        faulted=True,
    )


def select_motion_routing(
    state: SupervisorState,
    *,
    follow_backend: str = "legacy",
) -> MotionRouting:
    if state.faulted:
        return MotionRouting()
    if state.posture_mode != PostureModes.STANDING:
        return MotionRouting()
    if not state.motion_enabled:
        return MotionRouting()

    if state.task_mode == TaskModes.SEARCH:
        return MotionRouting(base_source="nav")

    if state.task_mode == TaskModes.FOLLOW:
        if str(follow_backend).strip().lower() == "legacy":
            return MotionRouting(base_source="follow")
        return MotionRouting(follow_bridge_source="follow")

    return MotionRouting()


# ---------------------------------------------------------------------------
# Registry-aware helpers
# ---------------------------------------------------------------------------

KNOWN_TASK_MODES: set[str] = {TaskModes.IDLE} | {
    b.task_mode for b in BUILTIN_BEHAVIORS if b.task_mode is not None
}


def normalize_voice_command_from_registry(raw_command: str | None) -> str:
    """Normalize a raw voice command using the behavior registry.

    Falls back to the legacy ``normalize_voice_command`` for any command
    not found in the registry.  This allows new behaviors to be recognized
    purely by adding a ``BehaviorDescriptor``.
    """
    if raw_command is None:
        return ""
    token = str(raw_command).strip().lower()
    if not token:
        return ""
    for behavior in BUILTIN_BEHAVIORS:
        if token == behavior.voice_command or token == behavior.name:
            return behavior.voice_command
    return normalize_voice_command(raw_command)
