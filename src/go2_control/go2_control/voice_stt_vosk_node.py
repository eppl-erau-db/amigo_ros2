#!/usr/bin/env python3
"""
Lightweight offline STT bridge using Vosk.

Subscribes to an AudioFrame topic (e.g. ODAS /sss), runs streaming STT, and
publishes transcripts as std_msgs/String for downstream command parsing.
"""

import json
import math
import os
import time

import numpy as np
import rclpy
from rclpy.node import Node
from audio_utils_msgs.msg import AudioFrame
from std_msgs.msg import String


class VoiceSttVoskNode(Node):
    def __init__(self) -> None:
        super().__init__('voice_stt_vosk_node')

        self.audio_topic = str(self.declare_parameter(
            'audio_topic', '/sss').value)
        self.transcript_topic = str(self.declare_parameter(
            'transcript_topic', '/voice/transcript').value)
        self.partial_topic = str(self.declare_parameter(
            'partial_topic', '/voice/partial').value)
        self.model_path = str(self.declare_parameter(
            'model_path', '').value).strip()
        self.audio_format = str(self.declare_parameter(
            'audio_format', 'signed_16').value).strip().lower()
        self.sample_rate = int(self.declare_parameter(
            'sample_rate', 16000).value)
        self.channel_index = int(self.declare_parameter(
            'channel_index', 0).value)
        self.channel_strategy = str(self.declare_parameter(
            'channel_strategy', 'fixed').value).strip().lower()
        self.publish_partial = bool(self.declare_parameter(
            'publish_partial', False).value)
        self.log_partial_hypotheses = bool(self.declare_parameter(
            'log_partial_hypotheses', False).value)
        self.log_empty_results = bool(self.declare_parameter(
            'log_empty_results', False).value)
        self.log_raw_results = bool(self.declare_parameter(
            'log_raw_results', False).value)
        self.debug_audio_stats = bool(self.declare_parameter(
            'debug_audio_stats', False).value)
        self.audio_stats_period_s = float(self.declare_parameter(
            'audio_stats_period_s', 1.0).value)
        self.max_alternatives = int(self.declare_parameter(
            'max_alternatives', 0).value)
        self.log_word_details = bool(self.declare_parameter(
            'log_word_details', False).value)
        self.min_text_chars = int(self.declare_parameter(
            'min_text_chars', 2).value)
        self.dedupe_window_s = float(self.declare_parameter(
            'dedupe_window_s', 1.5).value)
        self.vosk_log_level = int(self.declare_parameter(
            'vosk_log_level', -1).value)
        # Use a string-array default so launch overrides with string arrays
        # do not fail ROS2 type checking.
        raw_grammar = self.declare_parameter('grammar_phrases', ['']).value
        self.grammar_phrases = self._normalize_grammar(raw_grammar)

        self._ready = False
        self._recognizer = None
        self._last_transcript = ''
        self._last_transcript_time = 0.0
        self._last_partial = ''
        self._last_audio_stats_time = 0.0
        self._format_warned = False
        self._rate_warned = False
        self._invalid_channel_warned = False

        if self.channel_strategy not in ('fixed', 'max_rms'):
            self.get_logger().warn(
                f'Unknown channel_strategy="{self.channel_strategy}". '
                'Falling back to "fixed".'
            )
            self.channel_strategy = 'fixed'
        if self.audio_stats_period_s <= 0.0:
            self.audio_stats_period_s = 1.0

        self.transcript_pub = self.create_publisher(String, self.transcript_topic, 10)
        self.partial_pub = self.create_publisher(String, self.partial_topic, 10)
        self.create_subscription(AudioFrame, self.audio_topic, self._audio_cb, 10)

        self._try_init_vosk()

    @staticmethod
    def _normalize_grammar(raw_grammar) -> list[str]:
        if isinstance(raw_grammar, str):
            cleaned = raw_grammar.strip()
            return [cleaned] if cleaned else []
        if isinstance(raw_grammar, (list, tuple)):
            phrases = [str(item).strip() for item in raw_grammar]
            return [p for p in phrases if p]
        return []

    def _try_init_vosk(self) -> None:
        try:
            from vosk import KaldiRecognizer, Model, SetLogLevel  # type: ignore
        except Exception as exc:
            self.get_logger().error(
                'vosk import failed. Install with: `pip3 install vosk`. '
                f'Import error: {exc}'
            )
            return

        SetLogLevel(self.vosk_log_level)

        if not self.model_path:
            self.get_logger().error(
                'Parameter `model_path` is empty. Set it to a local Vosk model directory.'
            )
            return

        if not os.path.isdir(self.model_path):
            self.get_logger().error(
                f'Vosk model_path does not exist or is not a directory: "{self.model_path}"'
            )
            return

        model = Model(self.model_path)
        if self.grammar_phrases:
            grammar = json.dumps([*self.grammar_phrases, "[unk]"])
            self._recognizer = KaldiRecognizer(model, float(self.sample_rate), grammar)
            self.get_logger().info(
                f'Loaded Vosk model with grammar filter: {self.grammar_phrases}'
            )
        else:
            self._recognizer = KaldiRecognizer(model, float(self.sample_rate))
            self.get_logger().info('Loaded Vosk model without grammar filter.')

        if self._recognizer is not None:
            if self.max_alternatives > 0:
                try:
                    self._recognizer.SetMaxAlternatives(self.max_alternatives)
                except Exception as exc:
                    self.get_logger().warn(f'Failed to set max_alternatives: {exc}')
            if self.log_word_details or self.max_alternatives > 0:
                try:
                    self._recognizer.SetWords(True)
                except Exception as exc:
                    self.get_logger().warn(f'Failed to enable word details: {exc}')

        self._ready = True
        self.get_logger().info(
            f'Vosk STT ready. audio_topic="{self.audio_topic}", '
            f'transcript_topic="{self.transcript_topic}", '
            f'sample_rate={self.sample_rate}, channel_index={self.channel_index}, '
            f'channel_strategy="{self.channel_strategy}", '
            f'max_alternatives={self.max_alternatives}.'
        )

    def _audio_cb(self, msg: AudioFrame) -> None:
        if not self._ready or self._recognizer is None:
            return

        msg_format = str(msg.format).strip().lower()
        if msg_format != self.audio_format:
            if not self._format_warned:
                self.get_logger().warn(
                    f'Unexpected AudioFrame format "{msg_format}" '
                    f'(expected "{self.audio_format}"). Ignoring.'
                )
                self._format_warned = True
            return

        if int(msg.sampling_frequency) != self.sample_rate:
            if not self._rate_warned:
                self.get_logger().warn(
                    f'Unexpected sample rate {msg.sampling_frequency} Hz '
                    f'(expected {self.sample_rate} Hz). Ignoring.'
                )
                self._rate_warned = True
            return

        channel_count = int(msg.channel_count)
        if channel_count <= 0:
            return

        try:
            pcm = np.frombuffer(msg.data, dtype=np.int16)
        except Exception as exc:
            self.get_logger().warn(f'Failed to decode AudioFrame data: {exc}')
            return

        if pcm.size == 0:
            return

        frame_count = pcm.size // channel_count
        if frame_count <= 0:
            return

        reshaped = pcm[:frame_count * channel_count].reshape(frame_count, channel_count)
        channel_rms = None
        if self.channel_strategy == 'max_rms' or self.debug_audio_stats:
            channel_rms = np.sqrt(
                np.mean(np.square(reshaped.astype(np.float32)), axis=0)
            )

        if self.channel_strategy == 'max_rms':
            selected_channel = int(np.argmax(channel_rms)) if channel_rms is not None else 0
        else:
            selected_channel = self.channel_index
            if selected_channel < 0 or selected_channel >= channel_count:
                if not self._invalid_channel_warned:
                    self.get_logger().warn(
                        f'Invalid channel_index={selected_channel} for '
                        f'channel_count={channel_count}.'
                    )
                    self._invalid_channel_warned = True
                return

        if self.debug_audio_stats:
            now_mono = time.monotonic()
            if now_mono - self._last_audio_stats_time >= self.audio_stats_period_s:
                self._last_audio_stats_time = now_mono
                if channel_rms is None:
                    channel_rms = np.sqrt(
                        np.mean(np.square(reshaped.astype(np.float32)), axis=0)
                    )
                dbfs = [self._rms_to_dbfs(float(v)) for v in channel_rms.tolist()]
                self.get_logger().info(
                    f'AudioStats: selected_ch={selected_channel}, '
                    f'dbfs={",".join(f"{v:.1f}" for v in dbfs)}'
                )

        mono = reshaped[:, selected_channel]
        chunk = mono.tobytes()

        try:
            if self._recognizer.AcceptWaveform(chunk):
                result = json.loads(self._recognizer.Result())
                if self.log_raw_results:
                    self.get_logger().info(
                        f'FinalResultRaw: {json.dumps(result, ensure_ascii=True)}'
                    )
                text = self._extract_text(result)
                if not text and self.log_empty_results:
                    self.get_logger().info('FinalResult was empty text.')
                self._publish_transcript_if_fresh(text)
            else:
                partial = json.loads(self._recognizer.PartialResult()).get('partial', '')
                partial_text = str(partial).strip()
                if partial_text:
                    if self.publish_partial:
                        self.partial_pub.publish(String(data=partial_text))
                    if self.log_partial_hypotheses and partial_text != self._last_partial:
                        self._last_partial = partial_text
                        self.get_logger().info(f'Partial: "{partial_text}"')
        except Exception as exc:
            self.get_logger().warn(f'Vosk recognition error: {exc}')

    def _publish_transcript_if_fresh(self, text: str) -> None:
        if len(text) < self.min_text_chars:
            return

        now = time.monotonic()
        if text == self._last_transcript and (now - self._last_transcript_time) < self.dedupe_window_s:
            return

        self._last_transcript = text
        self._last_transcript_time = now
        self.transcript_pub.publish(String(data=text))
        self.get_logger().info(f'Transcript: "{text}"')

    @staticmethod
    def _rms_to_dbfs(rms: float) -> float:
        if rms <= 1e-6:
            return -120.0
        return 20.0 * math.log10(rms / 32768.0)

    @staticmethod
    def _extract_text(result: dict) -> str:
        """Handle Vosk final-result formats with and without alternatives."""
        text = str(result.get('text', '')).strip()
        if text:
            return text

        alternatives = result.get('alternatives')
        if isinstance(alternatives, list):
            for alt in alternatives:
                if isinstance(alt, dict):
                    alt_text = str(alt.get('text', '')).strip()
                    if alt_text:
                        return alt_text

        return ''


def main() -> None:
    rclpy.init()
    node = VoiceSttVoskNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
