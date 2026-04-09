# Adding Behaviors to Amigo — Coding Agent Guide

This document explains the Amigo robot's behavior architecture and provides
step-by-step checklists for adding new behaviors.  It is written for both
human developers and AI coding agents.

---

## Architecture Overview

```
                        +-----------------------+
  Microphone (ODAS) --> | voice_stt_vosk_node   | --> /voice/transcript
                        +-----------------------+
                                  |
                        +-----------------------+
                        | voice_command_node    |  wake phrase + intent match
                        +-----------------------+
                                  |
                            /voice/command  (e.g. "follow_me", "search")
                                  |
                        +-----------------------+
                        | mission_supervisor    |  state machine + operation dispatch
                        |   _node               |
                        +-----------------------+
                          |        |         |
                    +-----+   +---+---+   +--+--+
                    |Follow|  |Search |  | Sport|  (behavior nodes)
                    |Ctrl  |  |Action |  | API  |
                    +------+  +-------+  +------+
                          \       |       /
                           \      |      /
                        +------------------+
                        |   Robot (Go2)    |
                        +------------------+
```

**Flow:** Audio -> STT -> command parser (wake phrase gated) -> mission
supervisor (state machine validates + dispatches) -> behavior nodes execute.

The **mission supervisor** owns all state.  Behavior nodes are passive — they
only act when the supervisor enables them via `RobotModeState` or action goals.

---

## Key Files

| File | Purpose |
|------|---------|
| `go2_control/behavior_registry.py` | Declarative metadata for all behaviors (single source of truth) |
| `go2_control/mission_supervisor_core.py` | Pure-Python state machine logic (no ROS dependencies) |
| `go2_control/mission_supervisor_node.py` | ROS 2 node wrapping the state machine; executes operations |
| `go2_control/voice_command_node.py` | Transcript -> normalized command; wake phrase + speaker verification |
| `go2_bringup/launch/mapping_behavior.launch.py` | Launches behavior nodes + supervisor |
| `go2_bringup/launch/mapping_audio.launch.py` | Launches STT + voice command nodes |
| `go2_bringup/launch/_mapping_common.py` | Shared launch argument definitions |
| `go2_control/test/test_mission_supervisor_core.py` | Unit tests for state machine transitions |

---

## Behavior Taxonomy

### 1. Task Behaviors (FOLLOW, SEARCH, HELLO)

- Occupy a `TaskMode` slot — only one can be active at a time.
- Have a lifecycle: activation -> running -> deactivation/completion.
- Own a motion source (e.g. `"nav"` for search, `"follow"` for person-follow).
- May be preemptible (another task can cancel them).
- Typically implemented as a **ROS 2 action server** or a **controller node**
  that publishes velocity commands on a candidate topic.

### 2. Instant Gestures

- Fire-and-forget: no persistent state, no TaskMode change.
- Require IDLE + STANDING.
- Implemented via a single Sport API call or short action.

### 3. Posture Transitions (STAND_UP, LAY_DOWN)

- Managed by the posture subsystem in `mission_supervisor_core.py`.
- Use `PostureModes` (STANDING, LAYING, TRANSITION_TO_STAND, TRANSITION_TO_LAY).
- You should rarely need to add a new posture — extend this only for
  fundamentally new body configurations.

---

## Adding a New Task Behavior — Full Checklist

Use this checklist when adding a behavior like "patrol", "dance", "inspect",
etc.  Each step references the exact file and pattern to follow.

### Step 1: Register the behavior

**File:** `go2_control/behavior_registry.py`

Add a `BehaviorDescriptor` to `BUILTIN_BEHAVIORS`:

```python
BehaviorDescriptor(
    name="patrol",
    task_mode="PATROL",
    voice_command="patrol",
    voice_phrases=("patrol the area", "start patrolling"),
    voice_group="patrol",               # or add to existing group
    requires_posture="STANDING",
    requires_idle=False,
    is_preemptible=True,
    operations=("publish_zero_motion", "start_patrol"),
    deactivation_ops=("publish_zero_motion", "cancel_patrol"),
    motion_source="nav",                # uses Nav2 for movement
    cooldown_exempt=False,
    description="Autonomous waypoint patrol behavior.",
)
```

### Step 2: Add constants

**File:** `go2_control/mission_supervisor_core.py`

```python
class TaskModes:
    IDLE = "IDLE"
    FOLLOW = "FOLLOW"
    SEARCH = "SEARCH"
    PATROL = "PATROL"          # <-- add

class SupervisorOps:
    ...
    START_PATROL = "start_patrol"      # <-- add
    CANCEL_PATROL = "cancel_patrol"    # <-- add
```

### Step 3: Add transition rules

**File:** `go2_control/mission_supervisor_core.py` — `_request_task()`

Add a branch for PATROL after the existing SEARCH handling. Follow the
same pattern: check preconditions, build operations tuple, call `_accepted()`.

Key considerations:
- Can PATROL be preempted by FOLLOW? (probably yes)
- Can FOLLOW be preempted by PATROL? (decide and implement)
- What happens when PATROL completes? (use `complete_patrol()` like
  `complete_search()`)

Also add PATROL to `normalize_task_mode()`:
```python
if token in {"PATROL"}:
    return TaskModes.PATROL
```

And add a `complete_patrol()` function following the `complete_search()` pattern.

### Step 4: Add voice command normalization

**File:** `go2_control/mission_supervisor_core.py` — `normalize_voice_command()`

```python
if token in {"patrol", "start_patrol"}:
    return VoiceCommands.PATROL     # add VoiceCommands.PATROL = "patrol"
```

Or — if using the registry — it will be picked up automatically by
`normalize_voice_command_from_registry()`.

### Step 5: Add operation handlers

**File:** `go2_control/mission_supervisor_node.py` — `_execute_operation()`

```python
if operation == SupervisorOps.START_PATROL:
    self._start_patrol()
    return
if operation == SupervisorOps.CANCEL_PATROL:
    self._cancel_patrol("supervisor_preempt")
    return
```

Implement `_start_patrol()` and `_cancel_patrol()`.  For an action-based
behavior, follow the `_start_search()` / `_cancel_search()` pattern:
- Create an `ActionClient` in `__init__`
- Send goal in `_start_patrol()`
- Handle result in callback, call `complete_patrol()` on the state

### Step 6: Add motion routing (if needed)

**File:** `go2_control/mission_supervisor_core.py` — `select_motion_routing()`

```python
if state.task_mode == TaskModes.PATROL:
    return MotionRouting(base_source="nav")
```

### Step 7: Create the behavior node

Create a new Python file (e.g. `go2_control/patrol_action_server.py`).

**For action-based behaviors** (recommended), follow `search_action_server.py`:
- Implement a ROS 2 action server
- Define a `.action` file in `go2_interfaces/action/`
- Subscribe to `RobotModeState` to know when you're active
- Publish feedback during execution
- Handle cancellation gracefully

**For controller-based behaviors** (continuous), follow
`person_follow_controller_node.py`:
- Subscribe to `RobotModeState` to arm/disarm
- Publish velocity on `/motion/candidate/your_behavior`
- The supervisor routes this to `cmd_vel` when your mode is active

### Step 8: Wire voice phrases

**File:** `go2_control/voice_command_node.py`

Add phrase parameters and matching logic in `__init__` and `_transcript_cb`:
```python
self._patrol_phrases_norm = self._build_phrase_list(
    self.declare_parameter("patrol_phrase", "patrol the area").value,
    self.declare_parameter("patrol_phrases", ["start patrolling"]).value,
    fallback="patrol the area",
)
```

Add matching in `_transcript_cb` under the appropriate command group:
```python
if "patrol" in self._enabled_command_groups:
    matched = self._match_intent_phrase(transcript, self._patrol_phrases_norm)
    if matched is not None:
        self._publish_command("patrol", transcript, matched)
        return
```

**File:** `go2_bringup/launch/mapping_audio.launch.py`

Add the phrases to the `grammar_phrases` list for Vosk:
```python
"hey amigo patrol the area",
"amigo patrol the area",
"patrol the area",
"start patrolling",
```

Also pass the phrase parameters to voice_command_node's parameters dict.

### Step 9: Add to launch files

**File:** `go2_bringup/launch/mapping_behavior.launch.py`

Add your node (conditionally if appropriate):
```python
patrol_action_server = Node(
    package="go2_control",
    executable="patrol_action_server",
    name="patrol_action_server",
    output="screen",
    parameters=[...],
)
```

**File:** `go2_bringup/launch/_mapping_common.py`

Add any new launch arguments to the appropriate `*_ARGUMENT_NAMES` list
and to `build_argument_specs()`.

**File:** `go2_bringup/launch/mapping.launch.py`

Forward new argument names to the appropriate sub-launch.

### Step 10: Register the entry point

**File:** `go2_control/setup.py`

Add to `console_scripts`:
```python
"patrol_action_server = go2_control.patrol_action_server:main",
```

### Step 11: Add tests

**File:** `go2_control/test/test_mission_supervisor_core.py`

Test at minimum:
- IDLE -> PATROL transition succeeds when STANDING
- PATROL -> IDLE transition succeeds
- PATROL rejected when LAYING
- PATROL preemption by FOLLOW (if allowed)
- `complete_patrol()` returns to correct state

---

## Adding an Instant Gesture — Simplified Checklist

For fire-and-forget gestures:

1. Add `BehaviorDescriptor` to `behavior_registry.py` with `task_mode=None`
2. Add voice command constant to `VoiceCommands` in `mission_supervisor_core.py`
3. Add handling in `request_voice_command()` with a dedicated validation helper or direct mode request
4. Add operation handler in `mission_supervisor_node.py`
5. Add voice phrases to `voice_command_node.py` and launch grammar
6. Add tests

---

## Robot Capabilities Reference

When implementing a behavior node, here is how to access the robot's
capabilities:

### Motion Control
- **Nav2 navigation:** Publish goals to Nav2 action servers; nav commands are
  routed through `/motion/candidate/nav` (remapped from `cmd_vel` in
  `mapping_nav.launch.py`).
- **Direct velocity:** Publish `Twist` to your candidate topic
  (e.g. `/motion/candidate/your_behavior`).  The supervisor routes it to
  `cmd_vel` when your mode is active via `select_motion_routing()`.
- **Unitree Sport API:** Publish `unitree_api.msg.Request` to
  `/api/sport/request` with the appropriate API ID.  Common IDs:
  - 1004: Stand up
  - 1005: Lay down
  - 1016: Hello gesture
- **Gait control:** Use `go2_motion_mode_switcher` executable from
  `go2_driver` package for motion mode and gait changes.

### Camera / Perception
- **ZED camera:** Launched in `mapping_base.launch.py`.  Provides RGB,
  depth, and object detection.  Person detection uses the ZED body tracking
  SDK (configured via `zed_follow_params_path`).
- **Custom detection:** Subscribe to ZED image/depth topics and run your
  own detector node.

### Audio / Sound
- **ODAS microphone array:** Provides direction-of-arrival (DoA) and
  separated audio streams.  Leak detection uses the ODAS leak classifier.
- **Sound localization:** The `sound_localizer` node provides map-frame
  pose estimates for detected sound sources.

### Transforms
- Key frames: `map` -> `odom` -> `base_link`
- Use `tf2_ros` to look up transforms between frames.

### Robot State
- Subscribe to `/robot_mode_state` (`go2_interfaces/msg/RobotModeState`)
  to know the current task mode, posture, and whether motion is enabled.

---

## Speaker Verification (Future Hook)

The voice command node supports an optional speaker verification gate:
- Set `speaker_verification_enabled:=true` in the launch
- A future `speaker_verify_node` should publish `std_msgs/Bool(True)` to
  `/voice/speaker_verified` when it recognizes an authorized speaker
- The verification window (`speaker_verification_window_s`, default 10s)
  works like the wake phrase window — commands are only processed while
  the speaker is verified
- When disabled (default), all speakers are accepted

---

## Voice Pipeline Integration

Phrase flow for a new behavior:

1. **Vosk grammar** (`mapping_audio.launch.py` `grammar_phrases`): Add all
   natural-language phrases so Vosk can recognize them.  Include variants
   with/without wake phrase prefix.
2. **Command node** (`voice_command_node.py`): Match transcript against your
   phrase list and publish a normalized command token (e.g. `"patrol"`).
3. **Supervisor core** (`mission_supervisor_core.py`): `normalize_voice_command()`
   maps the token to a `VoiceCommands` constant.  `request_voice_command()`
   routes it to the appropriate transition function.
4. **Supervisor node** (`mission_supervisor_node.py`): Receives the command on
   `/voice/command`, validates cooldown, calls the core, and executes operations.

---

## Prompt for Coding Agents

Copy the section below and provide it to a coding agent when asking it to
add a new behavior:

```
You are adding a new behavior to the Amigo ROS 2 robot.  Read
src/go2_control/ADDING_BEHAVIORS.md for the full architecture guide and
step-by-step checklist.  Key files to read first:

- go2_control/behavior_registry.py (behavior metadata registry)
- go2_control/mission_supervisor_core.py (state machine logic)
- go2_control/mission_supervisor_node.py (ROS 2 supervisor node)
- go2_control/voice_command_node.py (voice command parsing)
- go2_bringup/launch/mapping_behavior.launch.py (behavior node launching)
- go2_bringup/launch/mapping_audio.launch.py (voice + STT launching)

Follow the "Adding a New Task Behavior" checklist in ADDING_BEHAVIORS.md.
All existing behaviors must continue to work — do not modify their logic.
Run tests in go2_control/test/test_mission_supervisor_core.py after changes.
```
