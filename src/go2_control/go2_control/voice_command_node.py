#!/usr/bin/env python3
"""
Voice command parser for Go2 voice-triggered actions.

- Subscribes to a transcript topic (`std_msgs/String`)
- Uses a wake phrase to arm commands for a short window
- Publishes normalized legacy command tokens on `/voice/command`
"""

from __future__ import annotations

import json
import re
import time
from typing import Iterable

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, String

from go2_interfaces.msg import RobotModeState


class VoiceCommandNode(Node):
    def __init__(self) -> None:
        super().__init__("voice_command_node")

        self.transcript_topic = str(
            self.declare_parameter("transcript_topic", "/voice/transcript").value
        )
        self.require_wake_phrase = bool(
            self.declare_parameter("require_wake_phrase", True).value
        )
        self.wake_phrase = str(self.declare_parameter("wake_phrase", "hey amigo").value)
        self.command_mode = str(self.declare_parameter("command_mode", "all").value).strip().lower()
        self.command_topic = str(self.declare_parameter("command_topic", "/voice/command").value)
        self.robot_mode_state_topic = str(
            self.declare_parameter("robot_mode_state_topic", "/robot_mode_state").value
        )
        self.wake_attention_command = str(
            self.declare_parameter("wake_attention_command", "wake_attention").value
        ).strip()
        self.wake_attention_status_topic = str(
            self.declare_parameter("wake_attention_status_topic", "/voice/attention/status").value
        )
        self.debug_topic = str(self.declare_parameter("debug_topic", "/voice/debug").value)
        self.publish_debug_topic = bool(
            self.declare_parameter("publish_debug_topic", True).value
        )
        self.wake_window_s = max(
            0.0, float(self.declare_parameter("wake_window_s", 8.0).value)
        )
        self.dedupe_window_s = max(
            0.1, float(self.declare_parameter("dedupe_window_s", 1.5).value)
        )
        self.log_transcripts = bool(
            self.declare_parameter("log_transcripts", False).value
        )
        self.debug_decisions = bool(
            self.declare_parameter("debug_decisions", False).value
        )

        self.speaker_verification_enabled = bool(
            self.declare_parameter("speaker_verification_enabled", False).value
        )
        self.speaker_verification_topic = str(
            self.declare_parameter(
                "speaker_verification_topic", "/voice/speaker_verified"
            ).value
        )
        self.speaker_verification_window_s = max(
            0.0,
            float(self.declare_parameter("speaker_verification_window_s", 10.0).value),
        )

        self._wake_phrases_norm = self._build_phrase_list(
            self.wake_phrase,
            self.declare_parameter("wake_phrases", ["amigo"]).value,
            fallback="hey amigo",
        )
        self._instant_hello_phrases_norm = self._build_phrase_list(
            self.declare_parameter("instant_hello_phrase", "hello amigo").value,
            self.declare_parameter("instant_hello_phrases", [""]).value,
            fallback="hello amigo",
        )
        self._say_hello_phrases_norm = self._build_phrase_list(
            self.declare_parameter("say_hello_phrase", "say hello").value,
            self.declare_parameter(
                "say_hello_phrases",
                ["can you say hello", "can you greet people", "greet people"],
            ).value,
            fallback="say hello",
        )
        self._ready_phrases_norm = self._build_phrase_list(
            self.declare_parameter("ready_phrase", "ready").value,
            self.declare_parameter("ready_phrases", ["get ready"]).value,
            fallback="ready",
        )
        self._upright_phrases_norm = self._build_phrase_list(
            self.declare_parameter("upright_phrase", "up").value,
            self.declare_parameter("upright_phrases", ["upright", "walk upright"]).value,
            fallback="up",
        )
        self._search_phrases_norm = self._build_phrase_list(
            self.declare_parameter("search_phrase", "look for a leak").value,
            self.declare_parameter("search_phrases", [""]).value,
            fallback="look for a leak",
        )
        self._explore_area_phrases_norm = self._build_phrase_list(
            self.declare_parameter("explore_area_phrase", "explore the area").value,
            self.declare_parameter(
                "explore_area_phrases",
                ["can you explore the area", "explore"],
            ).value,
            fallback="explore the area",
        )
        self._stand_up_phrases_norm = self._build_phrase_list(
            self.declare_parameter("stand_up_phrase", "stand up").value,
            self.declare_parameter("stand_up_phrases", ["get up"]).value,
            fallback="stand up",
        )
        self._lay_down_phrases_norm = self._build_phrase_list(
            self.declare_parameter("lay_down_phrase", "lay down").value,
            self.declare_parameter("lay_down_phrases", ["lie down", "down"]).value,
            fallback="lay down",
        )
        self._follow_phrases_norm = self._build_phrase_list(
            self.declare_parameter("follow_phrase", "follow me").value,
            self.declare_parameter("follow_phrases", ["track me", "come with me"]).value,
            fallback="follow me",
        )
        self._stop_follow_phrases_norm = self._build_phrase_list(
            self.declare_parameter("stop_follow_phrase", "stay").value,
            self.declare_parameter(
                "stop_follow_phrases",
                [
                    "stop following",
                    "stop follow me",
                    "cancel follow",
                    "stop tracking me",
                    "stop search",
                    "stop searching",
                    "stop saying hello",
                    "stop greeting",
                    "return to idle",
                ],
            ).value,
            fallback="stay",
        )

        self._enabled_command_groups, unknown_groups = self._parse_command_mode(self.command_mode)
        if unknown_groups:
            self.get_logger().warn(
                f"Unknown command_mode token(s)={unknown_groups}. "
                'Supported values include "search", "sport_test", "follow", and "all".'
            )
        if not self._enabled_command_groups:
            self.get_logger().warn(
                f'command_mode="{self.command_mode}" enabled no valid command groups. '
                'Falling back to "search".'
            )
            self._enabled_command_groups = {"search"}

        self._awake_until = 0.0
        self._speaker_verified_until = 0.0
        self._waiting_for_wake_attention = False
        self._last_transcript_norm = ""
        self._last_transcript_time = 0.0
        self._current_task_mode = "IDLE"

        self.command_pub = self.create_publisher(String, self.command_topic, 10)
        self.debug_pub = self.create_publisher(String, self.debug_topic, 10)
        self.create_subscription(String, self.transcript_topic, self._transcript_cb, 10)
        self.create_subscription(
            RobotModeState,
            self.robot_mode_state_topic,
            self._robot_mode_state_cb,
            10,
        )
        self.create_subscription(
            String,
            self.wake_attention_status_topic,
            self._wake_attention_status_cb,
            10,
        )
        if self.speaker_verification_enabled:
            self.create_subscription(
                Bool,
                self.speaker_verification_topic,
                self._speaker_verified_cb,
                10,
            )

        self.get_logger().info(
            f'Voice command parser ready. mode="{self.command_mode}", '
            f'enabled_groups={sorted(self._enabled_command_groups)}, '
            f'transcript_topic="{self.transcript_topic}", command_topic="{self.command_topic}", '
            f'robot_mode_state_topic="{self.robot_mode_state_topic}", '
            f'speaker_verification={"enabled" if self.speaker_verification_enabled else "disabled"}.'
        )

    @staticmethod
    def _normalize(text: str) -> str:
        lower = text.lower()
        alnum_spaces_only = re.sub(r"[^a-z0-9 ]+", " ", lower)
        return re.sub(r"\s+", " ", alnum_spaces_only).strip()

    def _build_phrase_list(self, primary: str, extra: Iterable[str], fallback: str) -> list[str]:
        phrases: list[str] = []
        raw_values = [primary]
        if isinstance(extra, str):
            raw_values.append(extra)
        elif isinstance(extra, (list, tuple)):
            raw_values.extend(str(value) for value in extra)
        for raw in raw_values:
            norm = self._normalize(str(raw))
            if norm and norm not in phrases:
                phrases.append(norm)
        if not phrases:
            phrases.append(self._normalize(fallback))
        return phrases

    @staticmethod
    def _parse_command_mode(raw_mode: str) -> tuple[set[str], list[str]]:
        enabled_groups: set[str] = set()
        unknown_groups: list[str] = []

        for token in re.split(r"[\s,]+", str(raw_mode).strip().lower()):
            if not token:
                continue
            if token in {"all", "multi", "hybrid"}:
                enabled_groups.update({"search", "sport_test", "follow"})
            elif token == "search":
                enabled_groups.add("search")
            elif token in {"sport", "sport_test"}:
                enabled_groups.add("sport_test")
            elif token in {"follow", "follow_me", "person_follow"}:
                enabled_groups.add("follow")
            else:
                unknown_groups.append(token)

        return enabled_groups, unknown_groups

    def _emit_debug_event(self, event: str, **payload) -> None:
        if not self.publish_debug_topic:
            return
        message = String()
        event_payload = {
            "source": "voice_command_node",
            "event": str(event),
            "timestamp_ns": self.get_clock().now().nanoseconds,
        }
        event_payload.update(payload)
        message.data = json.dumps(event_payload, separators=(",", ":"), sort_keys=True)
        self.debug_pub.publish(message)

    def _is_speaker_verified(self, now_mono: float) -> bool:
        if not self.speaker_verification_enabled:
            return True
        return now_mono <= self._speaker_verified_until

    def _speaker_verified_cb(self, msg: Bool) -> None:
        if msg.data:
            now = time.monotonic()
            self._speaker_verified_until = now + self.speaker_verification_window_s
            self._emit_debug_event(
                "speaker_verified",
                window_s=self.speaker_verification_window_s,
            )

    def _robot_mode_state_cb(self, msg: RobotModeState) -> None:
        self._current_task_mode = str(msg.task_mode).strip().upper() or "IDLE"

    def _is_awake(self, now_mono: float) -> bool:
        if not self.require_wake_phrase:
            return True
        return now_mono <= self._awake_until

    @staticmethod
    def _should_allow_upright_exit_bypass(task_mode: str | None) -> bool:
        return str(task_mode or "").strip().upper() == "UPRIGHT"

    @staticmethod
    def _has_wake_phrase(transcript: str, wake_phrases: Iterable[str]) -> bool:
        for wake in wake_phrases:
            if transcript == wake or transcript.startswith(f"{wake} "):
                return True
        return False

    @staticmethod
    def _should_trigger_wake_attention(
        transcript: str,
        wake_phrases: Iterable[str],
        *,
        require_wake_phrase: bool,
    ) -> str | None:
        if not require_wake_phrase:
            return None
        return VoiceCommandNode._match_exact_phrase(transcript, wake_phrases)

    @staticmethod
    def _match_intent_phrase(transcript: str, phrase_list: Iterable[str]) -> str | None:
        for phrase in phrase_list:
            if transcript == phrase or f" {phrase} " in f" {transcript} ":
                return phrase
        return None

    @staticmethod
    def _match_exact_phrase(transcript: str, phrase_list: Iterable[str]) -> str | None:
        for phrase in phrase_list:
            if transcript == phrase:
                return phrase
        return None

    @staticmethod
    def _match_wake_bypass_command(
        transcript: str,
        enabled_groups: Iterable[str],
        stand_up_phrases: Iterable[str],
        stop_phrases: Iterable[str],
    ) -> tuple[str, str] | None:
        enabled = set(enabled_groups)

        if "sport_test" in enabled:
            matched_phrase = VoiceCommandNode._match_intent_phrase(
                transcript,
                stand_up_phrases,
            )
            if matched_phrase is not None:
                return ("stand_up", matched_phrase)

        if enabled.intersection({"follow", "search", "sport_test"}):
            matched_phrase = VoiceCommandNode._match_intent_phrase(
                transcript,
                stop_phrases,
            )
            if matched_phrase is not None:
                return ("stop_follow", matched_phrase)

        return None

    def _publish_command(self, command_label: str, transcript: str, matched_phrase: str) -> None:
        msg = String()
        msg.data = command_label
        self.command_pub.publish(msg)
        if self.require_wake_phrase:
            self._awake_until = 0.0
        self._emit_debug_event(
            "command_published",
            command=command_label,
            transcript=transcript,
            matched_phrase=matched_phrase,
            topic=self.command_topic,
        )
        self.get_logger().info(
            f'Published voice command "{command_label}" to "{self.command_topic}".'
        )

    def _wake_attention_status_cb(self, msg: String) -> None:
        status = self._normalize(str(msg.data))
        if not status:
            return

        if status == "ready":
            self._waiting_for_wake_attention = False
            self._awake_until = time.monotonic() + self.wake_window_s
            self._emit_debug_event(
                "wake_attention_ready",
                status=status,
                wake_window_s=self.wake_window_s,
                topic=self.wake_attention_status_topic,
            )
            return

        if status.startswith("failed") or status in {"aborted", "idle"}:
            self._waiting_for_wake_attention = False
            self._awake_until = 0.0
            self._emit_debug_event(
                "wake_attention_closed",
                status=status,
                topic=self.wake_attention_status_topic,
            )

    def _transcript_cb(self, msg: String) -> None:
        raw = str(msg.data).strip()
        if not raw:
            return

        now = time.monotonic()
        transcript = self._normalize(raw)
        if not transcript:
            return

        if self.log_transcripts:
            self.get_logger().info(f'Transcript: "{transcript}"')
        self._emit_debug_event(
            "transcript_received",
            raw=raw,
            transcript=transcript,
            awake=self._is_awake(now),
        )

        if (
            transcript == self._last_transcript_norm and
            (now - self._last_transcript_time) <= self.dedupe_window_s
        ):
            self._emit_debug_event(
                "transcript_dropped",
                reason="duplicate",
                transcript=transcript,
            )
            return
        self._last_transcript_norm = transcript
        self._last_transcript_time = now

        if not self._is_speaker_verified(now):
            if self.debug_decisions:
                self.get_logger().info(
                    f'Debug: ignored transcript (speaker not verified): "{transcript}"'
                )
            self._emit_debug_event(
                "transcript_ignored",
                reason="speaker_not_verified",
                transcript=transcript,
            )
            return

        exact_wake_phrase = self._should_trigger_wake_attention(
            transcript,
            self._wake_phrases_norm,
            require_wake_phrase=self.require_wake_phrase,
        )
        if exact_wake_phrase is not None:
            if self._waiting_for_wake_attention:
                self._emit_debug_event(
                    "transcript_ignored",
                    reason="wake_attention_pending",
                    transcript=transcript,
                )
                return

            self._waiting_for_wake_attention = True
            self._awake_until = 0.0
            self._publish_command(
                self.wake_attention_command,
                transcript,
                exact_wake_phrase,
            )
            self._emit_debug_event(
                "wake_attention_requested",
                transcript=transcript,
                matched_phrase=exact_wake_phrase,
                command=self.wake_attention_command,
            )
            return

        if self._has_wake_phrase(transcript, self._wake_phrases_norm):
            self._awake_until = now + self.wake_window_s
            self._emit_debug_event(
                "wake_detected",
                transcript=transcript,
                wake_window_s=self.wake_window_s,
            )

        if self._waiting_for_wake_attention:
            self._emit_debug_event(
                "transcript_ignored",
                reason="wake_attention_pending",
                transcript=transcript,
            )
            return

        if "sport_test" in self._enabled_command_groups:
            matched_phrase = self._match_exact_phrase(transcript, self._instant_hello_phrases_norm)
            if matched_phrase is not None:
                self._publish_command("hello_amigo", transcript, matched_phrase)
                return

        wake_bypass_match = self._match_wake_bypass_command(
            transcript,
            self._enabled_command_groups,
            self._stand_up_phrases_norm,
            self._stop_follow_phrases_norm,
        )
        if wake_bypass_match is not None:
            command_label, matched_phrase = wake_bypass_match
            self._publish_command(command_label, transcript, matched_phrase)
            return

        if self._should_allow_upright_exit_bypass(self._current_task_mode):
            matched_phrase = self._match_intent_phrase(transcript, self._lay_down_phrases_norm)
            if matched_phrase is not None:
                self._publish_command("lay_down", transcript, matched_phrase)
                return

        if not self._is_awake(now):
            if self.debug_decisions:
                self.get_logger().info(f'Debug: ignored transcript while asleep: "{transcript}"')
            self._emit_debug_event(
                "transcript_ignored",
                reason="asleep",
                transcript=transcript,
            )
            return

        if self._enabled_command_groups.intersection({"follow", "search", "sport_test"}):
            matched_phrase = self._match_intent_phrase(transcript, self._stop_follow_phrases_norm)
            if matched_phrase is not None:
                self._publish_command("stop_follow", transcript, matched_phrase)
                return

        if "sport_test" in self._enabled_command_groups:
            matched_phrase = self._match_intent_phrase(transcript, self._say_hello_phrases_norm)
            if matched_phrase is not None:
                self._publish_command("say_hello", transcript, matched_phrase)
                return

            matched_phrase = self._match_intent_phrase(transcript, self._stand_up_phrases_norm)
            if matched_phrase is not None:
                self._publish_command("stand_up", transcript, matched_phrase)
                return

            matched_phrase = self._match_intent_phrase(transcript, self._lay_down_phrases_norm)
            if matched_phrase is not None:
                self._publish_command("lay_down", transcript, matched_phrase)
                return

            matched_phrase = self._match_intent_phrase(transcript, self._ready_phrases_norm)
            if matched_phrase is not None:
                self._publish_command("ready", transcript, matched_phrase)
                return

            matched_phrase = self._match_intent_phrase(transcript, self._upright_phrases_norm)
            if matched_phrase is not None:
                self._publish_command("walk_upright", transcript, matched_phrase)
                return

        if "follow" in self._enabled_command_groups:
            matched_phrase = self._match_intent_phrase(transcript, self._follow_phrases_norm)
            if matched_phrase is not None:
                self._publish_command("follow_me", transcript, matched_phrase)
                return

        if "search" in self._enabled_command_groups:
            matched_phrase = self._match_intent_phrase(transcript, self._explore_area_phrases_norm)
            if matched_phrase is not None:
                self._publish_command("explore_area", transcript, matched_phrase)
                return

            matched_phrase = self._match_intent_phrase(transcript, self._search_phrases_norm)
            if matched_phrase is not None:
                self._publish_command("search", transcript, matched_phrase)
                return

        if self.debug_decisions:
            self.get_logger().info(
                f'Debug: no command intent match for "{transcript}". '
                f"enabled_groups={sorted(self._enabled_command_groups)}."
            )
        self._emit_debug_event(
            "transcript_ignored",
            reason="no_intent_match",
            transcript=transcript,
            enabled_groups=sorted(self._enabled_command_groups),
        )


def main() -> None:
    rclpy.init()
    node = VoiceCommandNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
