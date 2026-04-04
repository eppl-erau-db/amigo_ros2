#!/usr/bin/env python3
"""
Wake-focused voice identity gate.

Speaker verification is applied only to the wake phrase in this first pass.
After a verified wake, the node waits for an attention acknowledgment sequence
and then opens a short, single-command transcript window.
"""

from __future__ import annotations

import re
import time
from typing import Iterable

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Float32, String


class GateState:
    IDLE_WAIT_WAKE = "IDLE_WAIT_WAKE"
    WAITING_FOR_WAKE_AUTH = "WAITING_FOR_WAKE_AUTH"
    WAITING_FOR_ATTENTION_ACK = "WAITING_FOR_ATTENTION_ACK"
    COMMAND_WINDOW_OPEN = "COMMAND_WINDOW_OPEN"
    COMMAND_HELD = "COMMAND_HELD"


class VoiceIdentityGateNode(Node):
    def __init__(self) -> None:
        super().__init__("voice_identity_gate_node")

        self.input_transcript_topic = str(
            self.declare_parameter("input_transcript_topic", "/voice/transcript").value
        )
        self.output_transcript_topic = str(
            self.declare_parameter(
                "output_transcript_topic", "/voice/authorized_transcript"
            ).value
        )
        self.authorized_topic = str(
            self.declare_parameter("authorized_topic", "/voice/speaker_authorized").value
        )
        self.score_topic = str(
            self.declare_parameter("score_topic", "/voice/speaker_score").value
        )
        self.wake_phrase = str(self.declare_parameter("wake_phrase", "hey amigo").value)
        self._wake_phrases_norm = self._build_phrase_list(
            self.wake_phrase,
            self.declare_parameter("wake_phrases", ["amigo"]).value,
            fallback="hey amigo",
        )
        self.decision_ttl_s = max(
            0.1, float(self.declare_parameter("decision_ttl_s", 2.5).value)
        )
        self.wake_authorization_wait_s = max(
            0.1, float(self.declare_parameter("wake_authorization_wait_s", 1.5).value)
        )
        self.command_window_s = max(
            0.1, float(self.declare_parameter("command_window_s", 2.5).value)
        )
        self.attention_enabled = bool(self.declare_parameter("attention_enabled", True).value)
        self.attention_request_topic = str(
            self.declare_parameter("attention_request_topic", "/voice/attention_request").value
        )
        self.attention_ready_topic = str(
            self.declare_parameter("attention_ready_topic", "/voice/attention_ready").value
        )
        self.attention_state_topic = str(
            self.declare_parameter("attention_state_topic", "/voice/attention/state").value
        )
        self.attention_timeout_s = max(
            0.5, float(self.declare_parameter("attention_timeout_s", 5.0).value)
        )
        self.post_command_hold_s = max(
            0.0, float(self.declare_parameter("post_command_hold_s", 0.6).value)
        )
        self.debug = bool(self.declare_parameter("debug", False).value)

        self._latest_authorized = False
        self._latest_authorized_time = 0.0
        self._latest_score: float | None = None

        self._state = GateState.IDLE_WAIT_WAKE
        self._state_deadline = 0.0
        self._pending_wake_raw = ""
        self._pending_wake_norm = ""
        self._pending_command_raw = ""
        self._pending_command_norm = ""

        self.transcript_pub = self.create_publisher(String, self.output_transcript_topic, 10)
        self.attention_request_pub = self.create_publisher(String, self.attention_request_topic, 10)
        self.attention_state_pub = self.create_publisher(String, self.attention_state_topic, 10)

        self.create_subscription(String, self.input_transcript_topic, self._transcript_cb, 10)
        self.create_subscription(Bool, self.authorized_topic, self._authorized_cb, 10)
        if self.score_topic:
            self.create_subscription(Float32, self.score_topic, self._score_cb, 10)
        if self.attention_enabled:
            self.create_subscription(String, self.attention_ready_topic, self._attention_ready_cb, 10)

        self.create_timer(0.1, self._state_timer_cb)
        self._publish_attention_state()

        self.get_logger().info(
            "Voice identity gate ready. "
            f'state="{self._state}", '
            f'input_transcript_topic="{self.input_transcript_topic}", '
            f'output_transcript_topic="{self.output_transcript_topic}", '
            f'attention_state_topic="{self.attention_state_topic}", '
            f"decision_ttl_s={self.decision_ttl_s:.2f}, "
            f"wake_authorization_wait_s={self.wake_authorization_wait_s:.2f}, "
            f"command_window_s={self.command_window_s:.2f}, "
            f"post_command_hold_s={self.post_command_hold_s:.2f}, "
            f"attention_enabled={self.attention_enabled}."
        )

    @staticmethod
    def _normalize(text: str) -> str:
        lowered = text.lower()
        alnum_spaces_only = re.sub(r"[^a-z0-9 ]+", " ", lowered)
        return re.sub(r"\s+", " ", alnum_spaces_only).strip()

    def _build_phrase_list(self, primary: str, extra: Iterable[str], fallback: str) -> list[str]:
        phrases: list[str] = []
        raw_values = [primary]
        if isinstance(extra, str):
            raw_values.append(extra)
        elif isinstance(extra, (list, tuple)):
            raw_values.extend(str(value) for value in extra)
        for raw in raw_values:
            normalized = self._normalize(str(raw))
            if normalized and normalized not in phrases:
                phrases.append(normalized)
        if not phrases:
            phrases.append(self._normalize(fallback))
        return phrases

    def _authorized_cb(self, msg: Bool) -> None:
        previous_state = self._latest_authorized if self._latest_authorized_time > 0.0 else None
        self._latest_authorized = bool(msg.data)
        self._latest_authorized_time = time.monotonic()

        if self.debug or previous_state is None or previous_state != self._latest_authorized:
            self.get_logger().info(
                "Updated speaker authorization decision: "
                f"authorized={self._latest_authorized}, "
                f"score={self._format_score(self._latest_score)}"
            )

        if self._state == GateState.WAITING_FOR_WAKE_AUTH and self._latest_authorized:
            self._resume_pending_wake_after_authorization(reason="authorized_pending_wake")

    def _score_cb(self, msg: Float32) -> None:
        self._latest_score = float(msg.data)

    def _attention_ready_cb(self, msg: String) -> None:
        if self._state != GateState.WAITING_FOR_ATTENTION_ACK:
            if self.debug:
                self.get_logger().info(
                    f'Ignoring attention-ready while state="{self._state}": "{msg.data}"'
                )
            return

        if self._pending_command_raw:
            now = time.monotonic()
            self._transition_to(
                GateState.COMMAND_HELD,
                deadline=now + self.post_command_hold_s,
                reason="buffered_command_ready",
            )
            if self.debug:
                self.get_logger().info(
                    f'Attention ready arrived with a buffered transcript '
                    f'"{self._pending_command_norm or self._normalize(self._pending_command_raw)}"; '
                    f"holding it for {self.post_command_hold_s:.2f}s before forwarding."
                )
            return

        self._open_command_window(reason="attention_ready")

    def _state_timer_cb(self) -> None:
        if self._state_deadline <= 0.0:
            return

        now = time.monotonic()
        if now <= self._state_deadline:
            return

        if self._state == GateState.WAITING_FOR_WAKE_AUTH:
            self._clear_pending_wake()
            self._clear_pending_command()
            self._transition_to(
                GateState.IDLE_WAIT_WAKE,
                reason="wake_authorization_timeout",
            )
            return

        if self._state == GateState.WAITING_FOR_ATTENTION_ACK:
            self._clear_pending_command()
            self._transition_to(
                GateState.IDLE_WAIT_WAKE,
                reason="attention_timeout",
            )
            return

        if self._state == GateState.COMMAND_WINDOW_OPEN:
            self._clear_pending_command()
            self._transition_to(
                GateState.IDLE_WAIT_WAKE,
                reason="command_window_timeout",
            )
            return

        if self._state == GateState.COMMAND_HELD:
            self._release_pending_command()

    def _transcript_cb(self, msg: String) -> None:
        raw = str(msg.data).strip()
        if not raw:
            return

        transcript = self._normalize(raw)
        if not transcript:
            return

        now = time.monotonic()
        wake_prefix = self._match_wake_prefix(transcript)
        is_exact_wake = wake_prefix is not None and transcript == wake_prefix
        has_wake_prefix = wake_prefix is not None

        if self._state == GateState.IDLE_WAIT_WAKE:
            self._handle_idle_transcript(raw, transcript, now, wake_prefix)
            return

        if self._state == GateState.WAITING_FOR_WAKE_AUTH:
            self._handle_waiting_wake_auth_transcript(raw, transcript, now, wake_prefix)
            return

        if self._state == GateState.WAITING_FOR_ATTENTION_ACK:
            self._handle_waiting_attention_transcript(
                raw, transcript, now, wake_prefix
            )
            return

        if self._state == GateState.COMMAND_WINDOW_OPEN:
            self._handle_command_window_transcript(
                raw, transcript, now, wake_prefix
            )
            return

        if self._state == GateState.COMMAND_HELD:
            self._handle_command_held_transcript(raw, transcript, is_exact_wake, has_wake_prefix)

    def _handle_idle_transcript(
        self,
        raw: str,
        transcript: str,
        now: float,
        wake_prefix: str | None,
    ) -> None:
        is_exact_wake = wake_prefix is not None and transcript == wake_prefix
        has_wake_prefix = wake_prefix is not None
        if is_exact_wake:
            if self._has_fresh_positive_authorization(now):
                self._start_attention_sequence(raw, reason="authorized_wake")
            else:
                self._buffer_pending_wake(raw, transcript)
                self._transition_to(
                    GateState.WAITING_FOR_WAKE_AUTH,
                    deadline=now + self.wake_authorization_wait_s,
                    reason="wake_pending_authorization",
                )
            return

        if has_wake_prefix:
            self._buffer_pending_wake(wake_prefix, wake_prefix)
            self._buffer_pending_command(raw, transcript)
            if self._has_fresh_positive_authorization(now):
                self._start_attention_sequence(
                    wake_prefix,
                    reason="authorized_combined_wake_command",
                    preserve_pending_command=True,
                )
            else:
                self._transition_to(
                    GateState.WAITING_FOR_WAKE_AUTH,
                    deadline=now + self.wake_authorization_wait_s,
                    reason="combined_wake_command_pending_authorization",
                )
            return

        self._log_drop(transcript, "waiting_for_verified_wake")

    def _handle_waiting_wake_auth_transcript(
        self,
        raw: str,
        transcript: str,
        now: float,
        wake_prefix: str | None,
    ) -> None:
        is_exact_wake = wake_prefix is not None and transcript == wake_prefix
        has_wake_prefix = wake_prefix is not None

        if is_exact_wake:
            self._buffer_pending_wake(raw, transcript)
            if self._has_fresh_positive_authorization(now):
                self._resume_pending_wake_after_authorization(
                    reason="authorized_pending_wake_refresh"
                )
            else:
                self._transition_to(
                    GateState.WAITING_FOR_WAKE_AUTH,
                    deadline=now + self.wake_authorization_wait_s,
                    reason="wake_pending_authorization_refresh",
                )
            return

        if has_wake_prefix:
            self._buffer_pending_wake(wake_prefix, wake_prefix)
            self._buffer_pending_command(raw, transcript)
            if self._has_fresh_positive_authorization(now):
                self._start_attention_sequence(
                    wake_prefix,
                    reason="authorized_combined_wake_command",
                    preserve_pending_command=True,
                )
            else:
                self._transition_to(
                    GateState.WAITING_FOR_WAKE_AUTH,
                    deadline=now + self.wake_authorization_wait_s,
                    reason="combined_wake_command_pending_authorization_refresh",
                )
            return

        self._buffer_pending_command(raw, transcript)
        if self.debug:
            self.get_logger().info(
                f'Buffered transcript "{transcript}" while waiting for wake authorization.'
            )

    def _handle_waiting_attention_transcript(
        self,
        raw: str,
        transcript: str,
        now: float,
        wake_prefix: str | None,
    ) -> None:
        is_exact_wake = wake_prefix is not None and transcript == wake_prefix
        has_wake_prefix = wake_prefix is not None
        if is_exact_wake:
            if self._has_fresh_positive_authorization(now):
                self._start_attention_sequence(raw, reason="authorized_wake_restart")
            else:
                self._buffer_pending_wake(raw, transcript)
                self._transition_to(
                    GateState.WAITING_FOR_WAKE_AUTH,
                    deadline=now + self.wake_authorization_wait_s,
                    reason="wake_pending_authorization",
                )
            return

        if has_wake_prefix:
            self._buffer_pending_wake(wake_prefix, wake_prefix)
            self._buffer_pending_command(raw, transcript)
            if self._has_fresh_positive_authorization(now):
                self._start_attention_sequence(
                    wake_prefix,
                    reason="authorized_combined_wake_restart",
                    preserve_pending_command=True,
                )
            else:
                self._transition_to(
                    GateState.WAITING_FOR_WAKE_AUTH,
                    deadline=now + self.wake_authorization_wait_s,
                    reason="combined_wake_command_pending_authorization",
                )
            return

        self._buffer_pending_command(raw, transcript)
        if self.debug:
            self.get_logger().info(
                f'Buffered transcript "{transcript}" while waiting for attention_ready.'
            )

    def _handle_command_window_transcript(
        self,
        raw: str,
        transcript: str,
        now: float,
        wake_prefix: str | None,
    ) -> None:
        is_exact_wake = wake_prefix is not None and transcript == wake_prefix
        has_wake_prefix = wake_prefix is not None
        if self._state_deadline > 0.0 and now > self._state_deadline:
            self._transition_to(GateState.IDLE_WAIT_WAKE, reason="command_window_timeout")
            self._log_drop(transcript, "command_window_expired")
            return

        if is_exact_wake:
            if self._has_fresh_positive_authorization(now):
                self._start_attention_sequence(raw, reason="authorized_wake_restart")
            else:
                self._buffer_pending_wake(raw, transcript)
                self._transition_to(
                    GateState.WAITING_FOR_WAKE_AUTH,
                    deadline=now + self.wake_authorization_wait_s,
                    reason="wake_pending_authorization",
                )
            return

        if has_wake_prefix:
            self._buffer_pending_wake(wake_prefix, wake_prefix)
            self._buffer_pending_command(raw, transcript)
            if self._has_fresh_positive_authorization(now):
                self._start_attention_sequence(
                    wake_prefix,
                    reason="authorized_combined_wake_restart",
                    preserve_pending_command=True,
                )
            else:
                self._transition_to(
                    GateState.WAITING_FOR_WAKE_AUTH,
                    deadline=now + self.wake_authorization_wait_s,
                    reason="combined_wake_command_pending_authorization",
                )
            return

        self._buffer_pending_command(raw, transcript)
        self._transition_to(
            GateState.COMMAND_HELD,
            deadline=now + self.post_command_hold_s,
            reason="command_captured",
        )
        if self.debug:
            self.get_logger().info(
                f'Held single command transcript "{transcript}" for '
                f"{self.post_command_hold_s:.2f}s before forwarding."
            )

    def _handle_command_held_transcript(
        self,
        raw: str,
        transcript: str,
        is_exact_wake: bool,
        has_wake_prefix: bool,
    ) -> None:
        del raw, is_exact_wake, has_wake_prefix
        self._log_drop(transcript, "waiting_for_command_release")

    def _start_attention_sequence(
        self,
        wake_transcript: str,
        reason: str,
        *,
        preserve_pending_command: bool = False,
    ) -> None:
        now = time.monotonic()
        if not preserve_pending_command:
            self._clear_pending_command()
        self._clear_pending_wake()
        self.transcript_pub.publish(String(data=wake_transcript))

        if self.attention_enabled:
            self.attention_request_pub.publish(String(data=wake_transcript))
            self._transition_to(
                GateState.WAITING_FOR_ATTENTION_ACK,
                deadline=now + self.attention_timeout_s,
                reason=reason,
            )
            return

        self._open_command_window(reason=f"{reason}_attention_disabled")

    def _open_command_window(self, reason: str) -> None:
        now = time.monotonic()
        self._transition_to(
            GateState.COMMAND_WINDOW_OPEN,
            deadline=now + self.command_window_s,
            reason=reason,
        )

    def _transition_to(
        self,
        new_state: str,
        *,
        deadline: float = 0.0,
        reason: str,
    ) -> None:
        previous_state = self._state
        self._state = str(new_state)
        self._state_deadline = float(deadline)
        self._publish_attention_state()

        if self.debug or previous_state != new_state:
            deadline_text = (
                "none"
                if self._state_deadline <= 0.0
                else f"{max(0.0, self._state_deadline - time.monotonic()):.2f}s"
            )
            self.get_logger().info(
                f"Gate state transition: {previous_state} -> {new_state} "
                f"(reason={reason}, deadline={deadline_text}, "
                f"score={self._format_score(self._latest_score)})."
            )

    def _has_fresh_positive_authorization(self, now: float) -> bool:
        if not self._latest_authorized:
            return False
        if self._latest_authorized_time <= 0.0:
            return False
        return (now - self._latest_authorized_time) <= self.decision_ttl_s

    def _match_wake_prefix(self, transcript: str) -> str | None:
        for wake_phrase in sorted(self._wake_phrases_norm, key=len, reverse=True):
            if transcript == wake_phrase or transcript.startswith(f"{wake_phrase} "):
                return wake_phrase
        return None

    def _log_drop(self, transcript: str, reason: str) -> None:
        if not self.debug:
            return
        self.get_logger().info(
            "Dropped transcript: "
            f'transcript="{transcript}", state="{self._state}", reason={reason}, '
            f"authorized={self._latest_authorized}, score={self._format_score(self._latest_score)}"
        )

    def _clear_pending_command(self) -> None:
        self._pending_command_raw = ""
        self._pending_command_norm = ""

    def _buffer_pending_wake(self, raw: str, transcript: str) -> None:
        self._pending_wake_raw = raw
        self._pending_wake_norm = transcript

    def _clear_pending_wake(self) -> None:
        self._pending_wake_raw = ""
        self._pending_wake_norm = ""

    def _buffer_pending_command(self, raw: str, transcript: str) -> None:
        self._pending_command_raw = raw
        self._pending_command_norm = transcript

    def _resume_pending_wake_after_authorization(self, *, reason: str) -> None:
        wake_transcript = self._pending_wake_raw or self._pending_wake_norm or self.wake_phrase
        preserve_pending_command = bool(self._pending_command_raw)
        self._start_attention_sequence(
            wake_transcript,
            reason=reason,
            preserve_pending_command=preserve_pending_command,
        )

    def _release_pending_command(self) -> None:
        raw = self._pending_command_raw
        transcript = self._pending_command_norm
        self._clear_pending_command()

        if raw:
            self.transcript_pub.publish(String(data=raw))
            if self.debug:
                self.get_logger().info(
                    f'Forwarded held command transcript "{transcript or self._normalize(raw)}" '
                    "after the post-command hold."
                )

        self._transition_to(
            GateState.IDLE_WAIT_WAKE,
            reason="command_consumed" if raw else "command_release_without_payload",
        )

    def _publish_attention_state(self) -> None:
        self.attention_state_pub.publish(String(data=self._state))

    @staticmethod
    def _format_score(score: float | None) -> str:
        return "n/a" if score is None else f"{score:.4f}"


def main() -> None:
    rclpy.init()
    node = VoiceIdentityGateNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
