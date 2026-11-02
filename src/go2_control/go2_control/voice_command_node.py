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
from std_msgs.msg import String


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

        self._wake_phrases_norm = self._build_phrase_list(
            self.wake_phrase,
            self.declare_parameter("wake_phrases", ["amigo"]).value,
            fallback="hey amigo",
        )
        self._shake_hand_phrases_norm = self._build_phrase_list(
            self.declare_parameter("shake_hand_phrase", "hello amigo").value,
            self.declare_parameter("shake_hand_phrases", [""]).value,
            fallback="hello amigo",
        )
        self._search_phrases_norm = self._build_phrase_list(
            self.declare_parameter("search_phrase", "look for a leak").value,
            self.declare_parameter("search_phrases", [""]).value,
            fallback="look for a leak",
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
            self.declare_parameter("stop_follow_phrase", "stop following").value,
            self.declare_parameter(
                "stop_follow_phrases",
                ["stop follow me", "cancel follow", "stop tracking me", "stay"],
            ).value,
            fallback="stop following",
        )
        self._wake_free_stop_follow_phrases_norm = self._build_phrase_list(
            self.declare_parameter("wake_free_stop_follow_phrase", "stay").value,
            self.declare_parameter("wake_free_stop_follow_phrases", [""]).value,
            fallback="stay",
        )
        self._explore_phrases_norm = self._build_phrase_list(
            self.declare_parameter("explore_phrase", "explore the area").value,
            self.declare_parameter(
                "explore_phrases", ["lets explore the area", "let s explore the area"]
            ).value,
            fallback="explore the area",
        )
        self._done_exploring_phrases_norm = self._build_phrase_list(
            self.declare_parameter("done_exploring_phrase", "done exploring").value,
            self.declare_parameter(
                "done_exploring_phrases", ["we are done exploring", "were done exploring"]
            ).value,
            fallback="done exploring",
        )
        self._deliver_phrases_norm = self._build_phrase_list(
            self.declare_parameter("deliver_phrase", "deliver swag").value,
            self.declare_parameter("deliver_phrases", ["deliver the swag"]).value,
            fallback="deliver swag",
        )
        self._handoff_done_phrases_norm = self._build_phrase_list(
            self.declare_parameter("handoff_done_phrase", "all done").value,
            self.declare_parameter("handoff_done_phrases", ["all finished", "we are all done"]).value,
            fallback="all done",
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
        self._last_transcript_norm = ""
        self._last_transcript_time = 0.0

        self.command_pub = self.create_publisher(String, self.command_topic, 10)
        self.debug_pub = self.create_publisher(String, self.debug_topic, 10)
        self.create_subscription(String, self.transcript_topic, self._transcript_cb, 10)

        self.get_logger().info(
            f'Voice command parser ready. mode="{self.command_mode}", '
            f'enabled_groups={sorted(self._enabled_command_groups)}, '
            f'transcript_topic="{self.transcript_topic}", command_topic="{self.command_topic}".'
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
                enabled_groups.update(
                    {"search", "sport_test", "follow", "explore", "deliver"}
                )
            elif token == "search":
                enabled_groups.add("search")
            elif token in {"sport", "sport_test"}:
                enabled_groups.add("sport_test")
            elif token in {"follow", "follow_me", "person_follow"}:
                enabled_groups.add("follow")
            elif token in {"explore", "mapping"}:
                enabled_groups.add("explore")
            elif token in {"deliver", "delivery", "deliver_swag"}:
                enabled_groups.add("deliver")
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

    def _is_awake(self, now_mono: float) -> bool:
        if not self.require_wake_phrase:
            return True
        return now_mono <= self._awake_until

    @staticmethod
    def _has_wake_phrase(transcript: str, wake_phrases: Iterable[str]) -> bool:
        for wake in wake_phrases:
            if transcript == wake or transcript.startswith(f"{wake} "):
                return True
        return False

    @staticmethod
    def _match_intent_phrase(transcript: str, phrase_list: Iterable[str]) -> str | None:
        for phrase in phrase_list:
            if phrase in transcript:
                return phrase
        return None

    @staticmethod
    def _match_exact_phrase(transcript: str, phrase_list: Iterable[str]) -> str | None:
        for phrase in phrase_list:
            if transcript == phrase:
                return phrase
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

        if "follow" in self._enabled_command_groups:
            matched_phrase = self._match_exact_phrase(
                transcript,
                self._wake_free_stop_follow_phrases_norm,
            )
            if matched_phrase is not None:
                self._publish_command("stop_follow", transcript, matched_phrase)
                return

        if "sport_test" in self._enabled_command_groups:
            matched_phrase = self._match_exact_phrase(transcript, self._shake_hand_phrases_norm)
            if matched_phrase is not None:
                self._publish_command("shake_hand", transcript, matched_phrase)
                return

        if self._has_wake_phrase(transcript, self._wake_phrases_norm):
            self._awake_until = now + self.wake_window_s
            self._emit_debug_event(
                "wake_detected",
                transcript=transcript,
                wake_window_s=self.wake_window_s,
            )

        if not self._is_awake(now):
            if self.debug_decisions:
                self.get_logger().info(f'Debug: ignored transcript while asleep: "{transcript}"')
            self._emit_debug_event(
                "transcript_ignored",
                reason="asleep",
                transcript=transcript,
            )
            return

        if "sport_test" in self._enabled_command_groups:
            matched_phrase = self._match_intent_phrase(transcript, self._stand_up_phrases_norm)
            if matched_phrase is not None:
                self._publish_command("stand_up", transcript, matched_phrase)
                return

            matched_phrase = self._match_intent_phrase(transcript, self._lay_down_phrases_norm)
            if matched_phrase is not None:
                self._publish_command("lay_down", transcript, matched_phrase)
                return

        if "follow" in self._enabled_command_groups:
            matched_phrase = self._match_intent_phrase(transcript, self._stop_follow_phrases_norm)
            if matched_phrase is not None:
                self._publish_command("stop_follow", transcript, matched_phrase)
                return

            matched_phrase = self._match_intent_phrase(transcript, self._follow_phrases_norm)
            if matched_phrase is not None:
                self._publish_command("follow_me", transcript, matched_phrase)
                return

        if "search" in self._enabled_command_groups:
            matched_phrase = self._match_intent_phrase(transcript, self._search_phrases_norm)
            if matched_phrase is not None:
                self._publish_command("search", transcript, matched_phrase)
                return

        if "explore" in self._enabled_command_groups:
            # Match the more specific "done exploring" before "explore the area".
            matched_phrase = self._match_intent_phrase(transcript, self._done_exploring_phrases_norm)
            if matched_phrase is not None:
                self._publish_command("done_exploring", transcript, matched_phrase)
                return
            matched_phrase = self._match_intent_phrase(transcript, self._explore_phrases_norm)
            if matched_phrase is not None:
                self._publish_command("explore", transcript, matched_phrase)
                return

        if "deliver" in self._enabled_command_groups:
            matched_phrase = self._match_intent_phrase(transcript, self._handoff_done_phrases_norm)
            if matched_phrase is not None:
                self._publish_command("handoff_done", transcript, matched_phrase)
                return
            matched_phrase = self._match_intent_phrase(transcript, self._deliver_phrases_norm)
            if matched_phrase is not None:
                self._publish_command("deliver_swag", transcript, matched_phrase)
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
