from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from go2_control.voice_command_node import VoiceCommandNode  # noqa: E402


# ---------------------------------------------------------------------------
# _normalize
# ---------------------------------------------------------------------------

def test_normalize_lowercases_and_strips_punctuation() -> None:
    assert VoiceCommandNode._normalize("Hello, World!") == "hello world"


def test_normalize_collapses_whitespace() -> None:
    assert VoiceCommandNode._normalize("  hey   amigo  ") == "hey amigo"


def test_normalize_removes_special_characters() -> None:
    assert VoiceCommandNode._normalize("it's a test—right?") == "it s a test right"


def test_normalize_empty_string() -> None:
    assert VoiceCommandNode._normalize("") == ""


def test_normalize_preserves_digits() -> None:
    assert VoiceCommandNode._normalize("channel 3 test") == "channel 3 test"


# ---------------------------------------------------------------------------
# _has_wake_phrase
# ---------------------------------------------------------------------------

def test_has_wake_phrase_exact_match() -> None:
    assert VoiceCommandNode._has_wake_phrase("hey amigo", ["hey amigo"]) is True


def test_has_wake_phrase_prefix_with_trailing_words() -> None:
    assert VoiceCommandNode._has_wake_phrase("hey amigo follow me", ["hey amigo"]) is True


def test_has_wake_phrase_no_match() -> None:
    assert VoiceCommandNode._has_wake_phrase("hello world", ["hey amigo"]) is False


def test_has_wake_phrase_partial_overlap_not_matched() -> None:
    # "hey amigo" embedded but not at start
    assert VoiceCommandNode._has_wake_phrase("oh hey amigo", ["hey amigo"]) is False


def test_has_wake_phrase_multiple_phrases() -> None:
    assert VoiceCommandNode._has_wake_phrase("amigo follow", ["hey amigo", "amigo"]) is True


# ---------------------------------------------------------------------------
# _match_intent_phrase
# ---------------------------------------------------------------------------

def test_match_intent_phrase_finds_substring() -> None:
    result = VoiceCommandNode._match_intent_phrase(
        "please follow me now", ["follow me"]
    )
    assert result == "follow me"


def test_match_intent_phrase_returns_none_when_absent() -> None:
    result = VoiceCommandNode._match_intent_phrase("hello world", ["follow me"])
    assert result is None


def test_match_intent_phrase_first_match_wins() -> None:
    result = VoiceCommandNode._match_intent_phrase(
        "stand up and get up", ["stand up", "get up"]
    )
    assert result == "stand up"


def test_match_intent_phrase_requires_word_boundaries() -> None:
    result = VoiceCommandNode._match_intent_phrase("staying put", ["stay"])
    assert result is None


# ---------------------------------------------------------------------------
# _match_exact_phrase
# ---------------------------------------------------------------------------

def test_match_exact_phrase_matches_exactly() -> None:
    result = VoiceCommandNode._match_exact_phrase(
        "hello amigo", ["hello amigo"]
    )
    assert result == "hello amigo"


def test_match_exact_phrase_rejects_substring() -> None:
    result = VoiceCommandNode._match_exact_phrase(
        "say hello amigo now", ["hello amigo"]
    )
    assert result is None


def test_should_trigger_wake_attention_for_exact_wake_phrase() -> None:
    result = VoiceCommandNode._should_trigger_wake_attention(
        "hey amigo",
        ["hey amigo", "amigo"],
        require_wake_phrase=True,
    )
    assert result == "hey amigo"


def test_should_not_trigger_wake_attention_for_prefixed_command() -> None:
    result = VoiceCommandNode._should_trigger_wake_attention(
        "hey amigo follow me",
        ["hey amigo", "amigo"],
        require_wake_phrase=True,
    )
    assert result is None


def test_should_not_trigger_wake_attention_when_wake_phrase_disabled() -> None:
    result = VoiceCommandNode._should_trigger_wake_attention(
        "hey amigo",
        ["hey amigo", "amigo"],
        require_wake_phrase=False,
    )
    assert result is None


# ---------------------------------------------------------------------------
# _match_wake_bypass_command
# ---------------------------------------------------------------------------

def test_match_wake_bypass_command_allows_stand_up_without_wake_phrase() -> None:
    result = VoiceCommandNode._match_wake_bypass_command(
        "stand up",
        {"sport_test"},
        ["stand up", "get up"],
        ["stay", "stop searching"],
    )
    assert result == ("stand_up", "stand up")


def test_match_wake_bypass_command_allows_idle_alias_in_search_mode() -> None:
    result = VoiceCommandNode._match_wake_bypass_command(
        "stop searching",
        {"search"},
        ["stand up", "get up"],
        ["stay", "stop searching"],
    )
    assert result == ("stop_follow", "stop searching")


def test_match_wake_bypass_command_allows_stop_in_sport_mode() -> None:
    result = VoiceCommandNode._match_wake_bypass_command(
        "stop greeting",
        {"sport_test"},
        ["stand up", "get up"],
        ["stay", "stop greeting"],
    )
    assert result == ("stop_follow", "stop greeting")


def test_should_allow_upright_exit_bypass_only_in_upright_mode() -> None:
    assert VoiceCommandNode._should_allow_upright_exit_bypass("UPRIGHT") is True
    assert VoiceCommandNode._should_allow_upright_exit_bypass("upright") is True
    assert VoiceCommandNode._should_allow_upright_exit_bypass("IDLE") is False
    assert VoiceCommandNode._should_allow_upright_exit_bypass("") is False


# ---------------------------------------------------------------------------
# _parse_command_mode
# ---------------------------------------------------------------------------

def test_parse_command_mode_all_enables_all_groups() -> None:
    groups, unknown = VoiceCommandNode._parse_command_mode("all")
    assert groups == {"search", "sport_test", "follow"}
    assert unknown == []


def test_parse_command_mode_single_group() -> None:
    groups, unknown = VoiceCommandNode._parse_command_mode("search")
    assert groups == {"search"}
    assert unknown == []


def test_parse_command_mode_comma_separated() -> None:
    groups, unknown = VoiceCommandNode._parse_command_mode("search,follow")
    assert groups == {"search", "follow"}
    assert unknown == []


def test_parse_command_mode_unknown_token() -> None:
    groups, unknown = VoiceCommandNode._parse_command_mode("search,fly")
    assert groups == {"search"}
    assert unknown == ["fly"]


def test_parse_command_mode_sport_alias() -> None:
    groups, _ = VoiceCommandNode._parse_command_mode("sport")
    assert "sport_test" in groups


def test_parse_command_mode_follow_aliases() -> None:
    for alias in ("follow", "follow_me", "person_follow"):
        groups, _ = VoiceCommandNode._parse_command_mode(alias)
        assert "follow" in groups, f"Alias '{alias}' should enable 'follow' group"
