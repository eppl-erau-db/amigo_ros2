from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from go2_control.behavior_registry import (  # noqa: E402
    BUILTIN_BEHAVIORS,
    BehaviorDescriptor,
    all_task_modes,
    all_voice_phrases,
    get_behavior,
    get_behavior_by_voice_command,
)


def test_all_behavior_names_are_unique() -> None:
    names = [b.name for b in BUILTIN_BEHAVIORS]
    assert len(names) == len(set(names)), f"Duplicate names: {names}"


def test_all_voice_commands_are_unique() -> None:
    commands = [b.voice_command for b in BUILTIN_BEHAVIORS]
    assert len(commands) == len(set(commands)), f"Duplicate commands: {commands}"


def test_get_behavior_returns_correct_descriptor() -> None:
    follow = get_behavior("follow")
    assert follow is not None
    assert follow.voice_command == "follow_me"
    assert follow.task_mode == "FOLLOW"


def test_get_behavior_returns_none_for_unknown() -> None:
    assert get_behavior("nonexistent_behavior") is None


def test_get_behavior_by_voice_command_returns_correct_descriptor() -> None:
    search = get_behavior_by_voice_command("search")
    assert search is not None
    assert search.name == "search"
    assert search.task_mode == "SEARCH"


def test_get_behavior_by_voice_command_returns_none_for_unknown() -> None:
    assert get_behavior_by_voice_command("fly_away") is None


def test_all_voice_phrases_returns_mapping_for_every_behavior() -> None:
    phrases = all_voice_phrases()
    assert isinstance(phrases, dict)
    for b in BUILTIN_BEHAVIORS:
        assert b.voice_command in phrases
        assert phrases[b.voice_command] == b.voice_phrases


def test_all_task_modes_excludes_none() -> None:
    modes = all_task_modes()
    assert None not in modes
    assert "ATTEND" in modes
    assert "READY" in modes
    assert "UPRIGHT" in modes
    assert "FOLLOW" in modes
    assert "SEARCH" in modes
    assert "EXPLORE" in modes
    assert "HELLO" in modes


def test_wake_attention_behavior_metadata() -> None:
    wake_attention = get_behavior("wake_attention")
    assert wake_attention is not None
    assert wake_attention.task_mode == "ATTEND"
    assert wake_attention.cooldown_exempt is True
    assert wake_attention.motion_source == "attention"
    assert "hey amigo" in wake_attention.voice_phrases


def test_follow_behavior_metadata() -> None:
    follow = get_behavior("follow")
    assert follow is not None
    assert follow.requires_posture == "STANDING"
    assert follow.is_preemptible is True
    assert follow.motion_source == "follow"
    assert "follow me" in follow.voice_phrases


def test_ready_behavior_metadata() -> None:
    ready = get_behavior("ready")
    assert ready is not None
    assert ready.task_mode == "READY"
    assert ready.requires_posture == "STANDING"
    assert ready.voice_group == "sport_test"
    assert "ready" in ready.voice_phrases


def test_upright_behavior_metadata() -> None:
    upright = get_behavior("upright")
    assert upright is not None
    assert upright.task_mode == "UPRIGHT"
    assert upright.voice_command == "walk_upright"
    assert upright.requires_posture == "STANDING"
    assert "up" in upright.voice_phrases


def test_say_hello_behavior_metadata() -> None:
    hello = get_behavior("say_hello")
    assert hello is not None
    assert hello.requires_idle is False
    assert hello.task_mode == "HELLO"
    assert hello.motion_source == "hello"
    assert hello.voice_group == "sport_test"
    assert "can you say hello" in hello.voice_phrases
    assert "hello amigo" not in hello.voice_phrases


def test_explore_area_behavior_metadata() -> None:
    explore_area = get_behavior("explore_area")
    assert explore_area is not None
    assert explore_area.task_mode == "EXPLORE"
    assert explore_area.voice_command == "explore_area"
    assert explore_area.voice_group == "search"
    assert explore_area.motion_source == "nav"
    assert "explore the area" in explore_area.voice_phrases


def test_hello_amigo_behavior_metadata() -> None:
    hello_amigo = get_behavior("hello_amigo")
    assert hello_amigo is not None
    assert hello_amigo.requires_idle is True
    assert hello_amigo.task_mode is None
    assert hello_amigo.cooldown_exempt is True
    assert hello_amigo.operations == ("publish_zero_motion", "send_hello_if_person_visible")


def test_stop_follow_is_cooldown_exempt() -> None:
    stop = get_behavior("stop_follow")
    assert stop is not None
    assert stop.cooldown_exempt is True
    assert "stay" in stop.voice_phrases
    assert "stop searching" in stop.voice_phrases
    assert "stop saying hello" in stop.voice_phrases


def test_stand_up_requires_laying_posture() -> None:
    stand = get_behavior("stand_up")
    assert stand is not None
    assert stand.requires_posture == "LAYING"


def test_lay_down_requires_standing_posture() -> None:
    lay = get_behavior("lay_down")
    assert lay is not None
    assert lay.requires_posture == "STANDING"
