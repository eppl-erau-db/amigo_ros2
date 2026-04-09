"""
Behavior Registry — Single source of truth for all Amigo robot behaviors.

This module declares metadata for every behavior the mission supervisor can
orchestrate.  It is intentionally **declarative and informational**: the
registry does not execute behaviors — it describes them so that the supervisor,
voice pipeline, and future coding agents all agree on the contract.

Quick-start for coding agents
-----------------------------
See ``ADDING_BEHAVIORS.md`` in this package root for the full step-by-step
guide.  The short version:

1. Add a ``BehaviorDescriptor`` to ``BUILTIN_BEHAVIORS`` below.
2. Add a ``TaskModes.YOUR_MODE`` constant in ``mission_supervisor_core.py``.
3. Add ``SupervisorOps.START_YOUR_BEHAVIOR`` (and CANCEL if needed).
4. Wire transition rules in ``mission_supervisor_core._request_task()``.
5. Wire operation handler in ``mission_supervisor_node._execute_operation()``.
6. Create the behavior ROS 2 node (action server or controller).
7. Register voice phrases in ``voice_command_node.py`` and the launch grammar.
8. Add the node to ``mapping_behavior.launch.py`` and ``setup.py``.
9. Add tests in ``test/test_mission_supervisor_core.py``.
"""

from __future__ import annotations

from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Descriptor
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class BehaviorDescriptor:
    """Metadata that fully describes a behavior from the supervisor's
    perspective.

    Fields
    ------
    name : str
        Short unique identifier (e.g. ``"follow"``).
    task_mode : str | None
        The ``TaskModes`` constant this behavior activates, or ``None`` for
        instant gestures that do not occupy a task mode.
    voice_command : str
        Normalized command token emitted by ``voice_command_node``
        (e.g. ``"follow_me"``).
    voice_phrases : tuple[str, ...]
        Natural-language phrases the STT / command node should match.
    voice_group : str
        Which ``command_mode`` group gates this command
        (``"follow"``, ``"search"``, ``"sport_test"``, or ``"any"``).
    requires_posture : str | None
        Posture that must be active (e.g. ``"STANDING"``), or ``None``.
    requires_idle : bool
        ``True`` if the robot must be in IDLE task mode to activate.
    is_preemptible : bool
        ``True`` if another behavior can cancel this one mid-execution.
    operations : tuple[str, ...]
        ``SupervisorOps`` constants executed on activation.
    deactivation_ops : tuple[str, ...]
        ``SupervisorOps`` constants executed when leaving this behavior.
    motion_source : str | None
        Motion routing key: ``"nav"``, ``"follow"``, ``"hello"``, or ``None``.
    cooldown_exempt : bool
        ``True`` to skip the per-command voice cooldown timer.
    description : str
        One-line human-readable summary shown in logs / diagnostics.
    """

    name: str
    task_mode: str | None
    voice_command: str
    voice_phrases: tuple[str, ...]
    voice_group: str
    requires_posture: str | None
    requires_idle: bool
    is_preemptible: bool
    operations: tuple[str, ...]
    deactivation_ops: tuple[str, ...]
    motion_source: str | None
    cooldown_exempt: bool
    description: str = ""


# ---------------------------------------------------------------------------
# Built-in behaviors
# ---------------------------------------------------------------------------

# Infrastructure note: voice_speaker_verifier_node publishes
# std_msgs/Bool on /voice/speaker_verified and std_msgs/Float32
# on /voice/speaker_score and /voice/speaker_direction.
# It is not a behavior — it gates voice_command_node when enabled.

BUILTIN_BEHAVIORS: tuple[BehaviorDescriptor, ...] = (
    BehaviorDescriptor(
        name="wake_attention",
        task_mode="ATTEND",
        voice_command="wake_attention",
        voice_phrases=("hey amigo", "amigo"),
        voice_group="any",
        requires_posture="STANDING",
        requires_idle=False,
        is_preemptible=True,
        operations=("publish_zero_motion",),
        deactivation_ops=("publish_zero_motion",),
        motion_source="attention",
        cooldown_exempt=True,
        description="Pitches up briefly to acknowledge the wake phrase and open the follow-up command window.",
    ),
    BehaviorDescriptor(
        name="ready",
        task_mode="READY",
        voice_command="ready",
        voice_phrases=("ready", "get ready"),
        voice_group="sport_test",
        requires_posture="STANDING",
        requires_idle=False,
        is_preemptible=True,
        operations=("publish_zero_motion",),
        deactivation_ops=("publish_zero_motion",),
        motion_source=None,
        cooldown_exempt=False,
        description="Nods yes, stretches, and reopens the short command window for the next sport command.",
    ),
    BehaviorDescriptor(
        name="upright",
        task_mode="UPRIGHT",
        voice_command="walk_upright",
        voice_phrases=("up", "upright", "walk upright"),
        voice_group="sport_test",
        requires_posture="STANDING",
        requires_idle=False,
        is_preemptible=True,
        operations=("publish_zero_motion",),
        deactivation_ops=("publish_zero_motion",),
        motion_source=None,
        cooldown_exempt=False,
        description="Stands up on the hind legs using the Unitree WalkUpright sport mode.",
    ),
    BehaviorDescriptor(
        name="follow",
        task_mode="FOLLOW",
        voice_command="follow_me",
        voice_phrases=("follow me", "track me", "come with me"),
        voice_group="follow",
        requires_posture="STANDING",
        requires_idle=False,
        is_preemptible=True,
        operations=("publish_zero_motion",),
        deactivation_ops=("publish_zero_motion",),
        motion_source="follow",
        cooldown_exempt=False,
        description="Person-following mode using ZED camera detection.",
    ),
    BehaviorDescriptor(
        name="stop_follow",
        task_mode=None,
        voice_command="stop_follow",
        voice_phrases=(
            "stay",
            "stop following",
            "stop follow me",
            "cancel follow",
            "stop tracking me",
            "stop search",
            "stop searching",
            "stop saying hello",
            "stop greeting",
            "return to idle",
        ),
        voice_group="any",
        requires_posture=None,
        requires_idle=False,
        is_preemptible=False,
        operations=("publish_zero_motion",),
        deactivation_ops=(),
        motion_source=None,
        cooldown_exempt=True,
        description="Returns the robot to IDLE, canceling follow/search/hello if active.",
    ),
    BehaviorDescriptor(
        name="search",
        task_mode="SEARCH",
        voice_command="search",
        voice_phrases=("look for a leak",),
        voice_group="search",
        requires_posture="STANDING",
        requires_idle=False,
        is_preemptible=True,
        operations=("publish_zero_motion", "start_search"),
        deactivation_ops=("publish_zero_motion", "cancel_search"),
        motion_source="nav",
        cooldown_exempt=False,
        description="Autonomous leak search: explore frontiers then localize.",
    ),
    BehaviorDescriptor(
        name="explore_area",
        task_mode="EXPLORE",
        voice_command="explore_area",
        voice_phrases=("can you explore the area", "explore the area", "explore"),
        voice_group="search",
        requires_posture="STANDING",
        requires_idle=False,
        is_preemptible=True,
        operations=("publish_zero_motion", "start_explore_area"),
        deactivation_ops=("publish_zero_motion", "cancel_explore_area"),
        motion_source="nav",
        cooldown_exempt=False,
        description="Frontier exploration mission that maps the area, discovers ArUco landmarks, and saves the resulting artifacts.",
    ),
    BehaviorDescriptor(
        name="say_hello",
        task_mode="HELLO",
        voice_command="say_hello",
        voice_phrases=("say hello", "can you say hello", "can you greet people", "greet people"),
        voice_group="sport_test",
        requires_posture="STANDING",
        requires_idle=False,
        is_preemptible=True,
        operations=("publish_zero_motion",),
        deactivation_ops=("publish_zero_motion",),
        motion_source="hello",
        cooldown_exempt=False,
        description="Rotate to find people, wave once, and keep scanning until canceled.",
    ),
    BehaviorDescriptor(
        name="hello_amigo",
        task_mode=None,
        voice_command="hello_amigo",
        voice_phrases=("hello amigo",),
        voice_group="sport_test",
        requires_posture="STANDING",
        requires_idle=True,
        is_preemptible=False,
        operations=("publish_zero_motion", "send_hello_if_person_visible"),
        deactivation_ops=(),
        motion_source=None,
        cooldown_exempt=True,
        description="Idle-only one-shot hello that waves only when a visible person is present.",
    ),
    BehaviorDescriptor(
        name="stand_up",
        task_mode=None,
        voice_command="stand_up",
        voice_phrases=("stand up", "get up"),
        voice_group="sport_test",
        requires_posture="LAYING",
        requires_idle=False,
        is_preemptible=False,
        operations=("publish_zero_motion", "send_stand_up"),
        deactivation_ops=(),
        motion_source=None,
        cooldown_exempt=True,
        description="Posture transition: LAYING -> STANDING.",
    ),
    BehaviorDescriptor(
        name="lay_down",
        task_mode=None,
        voice_command="lay_down",
        voice_phrases=("lay down", "lie down", "down"),
        voice_group="sport_test",
        requires_posture="STANDING",
        requires_idle=False,
        is_preemptible=False,
        operations=("publish_zero_motion", "send_stand_down"),
        deactivation_ops=(),
        motion_source=None,
        cooldown_exempt=True,
        description="Posture transition: STANDING -> LAYING.",
    ),
)


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------

def get_behavior(name: str) -> BehaviorDescriptor | None:
    """Return the descriptor with the given *name*, or ``None``."""
    for b in BUILTIN_BEHAVIORS:
        if b.name == name:
            return b
    return None


def get_behavior_by_voice_command(command: str) -> BehaviorDescriptor | None:
    """Return the descriptor whose *voice_command* matches, or ``None``."""
    for b in BUILTIN_BEHAVIORS:
        if b.voice_command == command:
            return b
    return None


def all_voice_phrases() -> dict[str, tuple[str, ...]]:
    """Return ``{voice_command: voice_phrases}`` for every behavior."""
    return {b.voice_command: b.voice_phrases for b in BUILTIN_BEHAVIORS}


def all_task_modes() -> set[str]:
    """Return the set of non-``None`` task modes across all behaviors."""
    return {b.task_mode for b in BUILTIN_BEHAVIORS if b.task_mode is not None}
