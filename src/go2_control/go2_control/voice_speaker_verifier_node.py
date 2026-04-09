#!/usr/bin/env python3
"""
Speaker verification node using WeSpeaker embeddings.

Subscribes to an AudioFrame topic (e.g. ODAS /sss), extracts speaker embeddings
with WeSpeaker, compares against a pre-enrolled reference, and publishes
verification results on /voice/speaker_verified for the existing gate in
voice_command_node.

Key improvements over the naive single-window threshold approach:
  1. Audio normalization — ODAS source-separated audio is very quiet; normalizing
     to a consistent RMS level before embedding extraction ensures the model
     operates within its trained amplitude range.
  2. EMA score smoothing — a single cosine similarity score per window is noisy;
     an exponential moving average (EMA) provides temporal smoothing so that a
     brief dip doesn't cause a false rejection.
  3. Silence-aware gating — the EMA is only updated when the window contains
     actual speech (above min_rms). During silence the smoothed score decays
     toward zero so stale verifications don't persist.

When disabled (not launched), voice_command_node works exactly as before.
"""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np
import rclpy
from rclpy.node import Node
from audio_utils_msgs.msg import AudioFrame
from std_msgs.msg import Bool, Float32

# Target RMS for audio normalization before embedding extraction.
# WeSpeaker was trained on normal-level speech; ODAS /sss outputs very quiet
# audio (RMS ~0.01). Normalizing to 0.10 puts the signal in a range the
# model was trained on.
_TARGET_RMS = 0.10


def _normalize_audio(audio: np.ndarray, target_rms: float = _TARGET_RMS) -> np.ndarray:
    """Normalize audio to a target RMS level."""
    rms = float(np.sqrt(np.mean(np.square(audio))))
    if rms < 1e-8:
        return audio
    return audio * (target_rms / rms)


class VoiceSpeakerVerifierNode(Node):
    def __init__(self) -> None:
        super().__init__("voice_speaker_verifier_node")

        # -- Parameters --
        self.audio_topic = str(
            self.declare_parameter("audio_topic", "/sss").value
        )
        self.model_name_or_path = str(
            self.declare_parameter("model_name_or_path", "eres2net").value
        )
        self.reference_embedding_path = str(
            self.declare_parameter("reference_embedding_path", "").value
        ).strip()
        self.threshold = float(
            self.declare_parameter("threshold", 0.55).value
        )
        self.sample_rate = int(
            self.declare_parameter("sample_rate", 16000).value
        )
        self.channel_index = int(
            self.declare_parameter("channel_index", 0).value
        )
        self.channel_strategy = str(
            self.declare_parameter("channel_strategy", "max_rms").value
        ).strip().lower()
        self.window_duration_s = float(
            self.declare_parameter("window_duration_s", 2.0).value
        )
        self.eval_period_s = float(
            self.declare_parameter("eval_period_s", 0.5).value
        )
        self.min_rms = float(
            self.declare_parameter("min_rms", 0.01).value
        )
        self.debug = bool(
            self.declare_parameter("debug", False).value
        )
        self.score_topic = str(
            self.declare_parameter("score_topic", "/voice/speaker_score").value
        )
        self.authorized_topic = str(
            self.declare_parameter("authorized_topic", "/voice/speaker_verified").value
        )
        self.doa_topic = str(
            self.declare_parameter("doa_topic", "/doa_angle").value
        )
        self.direction_topic = str(
            self.declare_parameter("direction_topic", "/voice/speaker_direction").value
        )

        # EMA smoothing factor (0..1). Higher = more weight on the latest score,
        # more responsive but noisier. Lower = smoother but slower to react.
        self.ema_alpha = float(
            self.declare_parameter("ema_alpha", 0.4).value
        )
        # Per-evaluation-period decay applied to the smoothed score during
        # silence (when RMS < min_rms). This prevents stale verifications
        # from lingering after the enrolled speaker stops talking.
        self.silence_decay = float(
            self.declare_parameter("silence_decay", 0.85).value
        )

        if self.channel_strategy not in ("fixed", "max_rms"):
            self.get_logger().warn(
                f'Unknown channel_strategy="{self.channel_strategy}". '
                'Falling back to "max_rms".'
            )
            self.channel_strategy = "max_rms"

        # -- State --
        self._model = None
        self._reference_embedding: np.ndarray | None = None
        self._audio_buffer = np.zeros(0, dtype=np.float32)
        self._window_samples = int(self.window_duration_s * self.sample_rate)
        self._eval_samples = int(self.eval_period_s * self.sample_rate)
        self._samples_since_eval = 0
        self._ready = False
        self._format_warned = False
        self._rate_warned = False
        self._invalid_channel_warned = False
        self._latest_doa_deg: float | None = None

        # EMA-smoothed score
        self._smoothed_score: float = 0.0

        # -- Load model and reference --
        self._try_load_model()
        self._try_load_reference()

        if not self._ready:
            self.get_logger().error(
                "Speaker verifier NOT ready. Will never publish True. "
                "Check model and reference_embedding_path parameters."
            )

        # -- Publishers --
        self.score_pub = self.create_publisher(Float32, self.score_topic, 10)
        self.auth_pub = self.create_publisher(Bool, self.authorized_topic, 10)
        self.direction_pub = self.create_publisher(Float32, self.direction_topic, 10)

        # -- Subscribers --
        self.create_subscription(AudioFrame, self.audio_topic, self._audio_cb, 10)
        self.create_subscription(Float32, self.doa_topic, self._doa_cb, 10)

        self.get_logger().info(
            f"Speaker verifier initialized. "
            f'audio_topic="{self.audio_topic}", threshold={self.threshold}, '
            f"window={self.window_duration_s}s, eval_period={self.eval_period_s}s, "
            f"ema_alpha={self.ema_alpha}, silence_decay={self.silence_decay}, "
            f"audio_normalization=enabled (target_rms={_TARGET_RMS}), "
            f'ready={self._ready}.'
        )

    # ------------------------------------------------------------------
    # Initialization helpers
    # ------------------------------------------------------------------

    def _try_load_model(self) -> None:
        try:
            from wespeaker.cli.speaker import load_model
            self._model = load_model(self.model_name_or_path)
            self.get_logger().info(
                f'WeSpeaker model loaded: "{self.model_name_or_path}".'
            )
        except Exception as exc:
            self.get_logger().error(f"Failed to load WeSpeaker model: {exc}")
            self._model = None

    def _try_load_reference(self) -> None:
        if not self.reference_embedding_path:
            self.get_logger().error(
                "reference_embedding_path is empty. Speaker verifier disabled."
            )
            return

        ref_path = Path(self.reference_embedding_path)
        if not ref_path.is_file():
            self.get_logger().error(
                f'Reference embedding not found: "{ref_path}". '
                "Speaker verifier disabled."
            )
            return

        try:
            emb = np.load(str(ref_path))
            norm = np.linalg.norm(emb)
            if norm < 1e-8:
                self.get_logger().error("Reference embedding has near-zero norm.")
                return
            self._reference_embedding = (emb / norm).astype(np.float32).flatten()
            self._ready = self._model is not None
            self.get_logger().info(
                f"Reference embedding loaded: shape={emb.shape}, "
                f"norm={norm:.4f}."
            )
        except Exception as exc:
            self.get_logger().error(f"Failed to load reference embedding: {exc}")

    # ------------------------------------------------------------------
    # Channel extraction (mirrors voice_stt_vosk_node logic)
    # ------------------------------------------------------------------

    def _extract_mono(self, msg: AudioFrame) -> np.ndarray | None:
        msg_format = str(msg.format).strip().lower()
        if msg_format != "signed_16":
            if not self._format_warned:
                self.get_logger().warn(
                    f'Unexpected AudioFrame format "{msg_format}" '
                    '(expected "signed_16"). Ignoring.'
                )
                self._format_warned = True
            return None

        if int(msg.sampling_frequency) != self.sample_rate:
            if not self._rate_warned:
                self.get_logger().warn(
                    f"Unexpected sample rate {msg.sampling_frequency} Hz "
                    f"(expected {self.sample_rate} Hz). Ignoring."
                )
                self._rate_warned = True
            return None

        channel_count = int(msg.channel_count)
        if channel_count <= 0:
            return None

        try:
            pcm = np.frombuffer(msg.data, dtype=np.int16)
        except Exception:
            return None

        if pcm.size == 0:
            return None

        frame_count = pcm.size // channel_count
        if frame_count <= 0:
            return None

        reshaped = pcm[: frame_count * channel_count].reshape(frame_count, channel_count)

        if self.channel_strategy == "max_rms":
            channel_rms = np.sqrt(
                np.mean(np.square(reshaped.astype(np.float32)), axis=0)
            )
            selected = int(np.argmax(channel_rms))
        else:
            selected = self.channel_index
            if selected < 0 or selected >= channel_count:
                if not self._invalid_channel_warned:
                    self.get_logger().warn(
                        f"Invalid channel_index={selected} for "
                        f"channel_count={channel_count}."
                    )
                    self._invalid_channel_warned = True
                return None

        # Convert int16 -> float32 normalized to [-1, 1]
        mono = reshaped[:, selected].astype(np.float32) / 32768.0
        return mono

    # ------------------------------------------------------------------
    # DoA callback
    # ------------------------------------------------------------------

    def _doa_cb(self, msg: Float32) -> None:
        self._latest_doa_deg = float(msg.data)

    # ------------------------------------------------------------------
    # Audio callback + windowed evaluation
    # ------------------------------------------------------------------

    def _audio_cb(self, msg: AudioFrame) -> None:
        mono = self._extract_mono(msg)
        if mono is None:
            return

        # Append to rolling buffer
        self._audio_buffer = np.concatenate([self._audio_buffer, mono])
        self._samples_since_eval += len(mono)

        # Trim buffer to max window size
        if len(self._audio_buffer) > self._window_samples:
            self._audio_buffer = self._audio_buffer[-self._window_samples:]

        # Only evaluate every eval_period_s worth of samples
        if self._samples_since_eval < self._eval_samples:
            return
        self._samples_since_eval = 0

        if not self._ready:
            return

        # Need at least a full window
        if len(self._audio_buffer) < self._window_samples:
            return

        window = self._audio_buffer[-self._window_samples:]

        # Silence gate — decay the smoothed score during silence
        rms = float(np.sqrt(np.mean(np.square(window))))
        if rms < self.min_rms:
            self._smoothed_score *= self.silence_decay
            if self.debug:
                self.get_logger().debug(
                    f"Silence (rms={rms:.5f} < {self.min_rms}). "
                    f"Decayed smoothed_score={self._smoothed_score:.4f}"
                )
            return

        # Normalize audio to target RMS before embedding extraction
        normalized_window = _normalize_audio(window)

        # Compute embedding and raw score
        raw_score = self._compute_score(normalized_window)
        if raw_score is None:
            return

        # Update EMA-smoothed score
        self._smoothed_score = (
            self.ema_alpha * raw_score
            + (1.0 - self.ema_alpha) * self._smoothed_score
        )

        verified = self._smoothed_score >= self.threshold

        # Publish smoothed score
        score_msg = Float32()
        score_msg.data = float(self._smoothed_score)
        self.score_pub.publish(score_msg)

        # Publish verification result
        auth_msg = Bool()
        auth_msg.data = verified
        self.auth_pub.publish(auth_msg)

        # Publish direction when verified
        if verified and self._latest_doa_deg is not None:
            dir_msg = Float32()
            dir_msg.data = float(self._latest_doa_deg)
            self.direction_pub.publish(dir_msg)

        if self.debug:
            self.get_logger().info(
                f"raw={raw_score:.4f}, smoothed={self._smoothed_score:.4f}, "
                f"threshold={self.threshold}, verified={verified}, rms={rms:.4f}"
                + (
                    f", doa={self._latest_doa_deg:.1f}deg"
                    if verified and self._latest_doa_deg is not None
                    else ""
                )
            )

    def _compute_score(self, window: np.ndarray) -> float | None:
        """Compute cosine similarity between window embedding and reference."""
        try:
            import torch

            waveform = torch.from_numpy(window).unsqueeze(0)  # (1, samples)

            emb = self._model.extract_embedding_from_pcm(
                waveform, sample_rate=self.sample_rate
            )

            if isinstance(emb, torch.Tensor):
                emb = emb.detach().cpu().numpy()

            emb = emb.flatten().astype(np.float32)
            norm = np.linalg.norm(emb)
            if norm < 1e-8:
                return None
            emb = emb / norm

            # Cosine similarity (both unit-normed), stays in [-1, 1]
            score = float(np.dot(emb, self._reference_embedding))
            return score

        except Exception as exc:
            self.get_logger().warn(f"Embedding computation failed: {exc}")
            return None


def main() -> None:
    rclpy.init()
    node = VoiceSpeakerVerifierNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
