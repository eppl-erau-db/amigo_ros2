#!/usr/bin/env python3
"""
Speaker verification node for the Go2 voice pipeline.

Subscribes to an AudioFrame topic, keeps a rolling mono audio buffer, runs
WeSpeaker embedding inference on fixed windows, and publishes a similarity
score plus an authorization boolean for downstream transcript gating.
"""

from __future__ import annotations

import math
import os
import time
from collections import deque
from typing import Any

import numpy as np
import rclpy
import torch
from audio_utils_msgs.msg import AudioFrame
from rclpy.node import Node
from std_msgs.msg import Bool, Float32
from wespeaker.cli.speaker import load_model


class VoiceSpeakerVerifierNode(Node):
    def __init__(self) -> None:
        super().__init__("voice_speaker_verifier_node")

        self.audio_topic = str(self.declare_parameter("audio_topic", "/sss").value)
        self.model_name_or_path = str(
            self.declare_parameter("model_name_or_path", "english").value
        ).strip() or "english"
        self.reference_embedding_path = str(
            self.declare_parameter("reference_embedding_path", "").value
        ).strip()
        self.threshold = float(self.declare_parameter("threshold", 0.68).value)
        self.sample_rate = int(self.declare_parameter("sample_rate", 16000).value)
        self.channel_index = int(self.declare_parameter("channel_index", 0).value)
        self.channel_strategy = str(
            self.declare_parameter("channel_strategy", "max_rms").value
        ).strip().lower()
        self.window_duration_s = max(
            0.25, float(self.declare_parameter("window_duration_s", 2.0).value)
        )
        self.eval_period_s = max(
            0.1, float(self.declare_parameter("eval_period_s", 0.5).value)
        )
        self.min_dbfs = float(self.declare_parameter("min_dbfs", -50.0).value)
        self.debug = bool(self.declare_parameter("debug", False).value)
        self.score_topic = str(
            self.declare_parameter("score_topic", "/voice/speaker_score").value
        )
        self.authorized_topic = str(
            self.declare_parameter("authorized_topic", "/voice/speaker_authorized").value
        )

        self._expected_audio_format = "signed_16"
        self._speaker = None
        self._reference_embedding: torch.Tensor | None = None
        self._ready = False

        self._window_samples = max(1, int(round(self.window_duration_s * self.sample_rate)))
        overlap_samples = max(1, int(round(self.eval_period_s * self.sample_rate)))
        self._max_buffer_samples = self._window_samples + overlap_samples
        self._mono_chunks: deque[np.ndarray] = deque()
        self._buffered_samples = 0

        self._format_warned = False
        self._rate_warned = False
        self._invalid_channel_warned = False

        self._last_score: float | None = None
        self._last_authorized: bool | None = None
        self._last_decision_monotonic = 0.0
        self._last_decision_stamp_ns: int | None = None

        if self.channel_strategy not in ("fixed", "max_rms"):
            self.get_logger().warn(
                f'Unknown channel_strategy="{self.channel_strategy}". Falling back to "fixed".'
            )
            self.channel_strategy = "fixed"

        if self.threshold < 0.0 or self.threshold > 1.0:
            clamped = min(1.0, max(0.0, self.threshold))
            self.get_logger().warn(
                f"threshold={self.threshold:.4f} is outside [0, 1]. Clamping to {clamped:.4f}."
            )
            self.threshold = clamped

        self.score_pub = self.create_publisher(Float32, self.score_topic, 10)
        self.authorized_pub = self.create_publisher(Bool, self.authorized_topic, 10)
        self.create_subscription(AudioFrame, self.audio_topic, self._audio_cb, 10)
        self.create_timer(self.eval_period_s, self._evaluate_current_window)

        self._try_initialize()

    def _try_initialize(self) -> None:
        try:
            self._speaker = load_model(self.model_name_or_path)
        except Exception as exc:
            self.get_logger().error(
                "Failed to load WeSpeaker model "
                f'"{self.model_name_or_path}". Verification will fail closed: {exc}'
            )
            return

        try:
            self._reference_embedding = self._load_reference_embedding(
                self.reference_embedding_path
            )
        except Exception as exc:
            self.get_logger().error(
                "Failed to load enrolled reference embedding "
                f'from "{self.reference_embedding_path}". Verification will fail closed: {exc}'
            )
            return

        self._ready = True
        self.get_logger().info(
            "Speaker verifier ready. "
            f'audio_topic="{self.audio_topic}", '
            f'model="{self.model_name_or_path}", '
            f'reference="{os.path.abspath(os.path.expanduser(self.reference_embedding_path))}", '
            f"threshold={self.threshold:.3f}, "
            f"window_duration_s={self.window_duration_s:.2f}, "
            f"eval_period_s={self.eval_period_s:.2f}, "
            f"sample_rate={self.sample_rate}, "
            f'channel_strategy="{self.channel_strategy}", '
            f"channel_index={self.channel_index}."
        )

    def _audio_cb(self, msg: AudioFrame) -> None:
        msg_format = str(msg.format).strip().lower()
        if msg_format != self._expected_audio_format:
            if not self._format_warned:
                self.get_logger().warn(
                    f'Unexpected AudioFrame format "{msg_format}" '
                    f'(expected "{self._expected_audio_format}"). Ignoring.'
                )
                self._format_warned = True
            return

        if int(msg.sampling_frequency) != self.sample_rate:
            if not self._rate_warned:
                self.get_logger().warn(
                    f"Unexpected sample rate {msg.sampling_frequency} Hz "
                    f"(expected {self.sample_rate} Hz). Ignoring."
                )
                self._rate_warned = True
            return

        channel_count = int(msg.channel_count)
        if channel_count <= 0:
            return

        try:
            pcm = np.frombuffer(msg.data, dtype=np.int16)
        except Exception as exc:
            self.get_logger().warn(f"Failed to decode AudioFrame data: {exc}")
            return

        if pcm.size == 0:
            return

        frame_count = pcm.size // channel_count
        if frame_count <= 0:
            return

        reshaped = pcm[: frame_count * channel_count].reshape(frame_count, channel_count)
        channel_rms = None
        if self.channel_strategy == "max_rms" or self.debug:
            channel_rms = np.sqrt(
                np.mean(np.square(reshaped.astype(np.float32)), axis=0)
            )

        if self.channel_strategy == "max_rms":
            selected_channel = int(np.argmax(channel_rms)) if channel_rms is not None else 0
        else:
            selected_channel = self.channel_index
            if selected_channel < 0 or selected_channel >= channel_count:
                if not self._invalid_channel_warned:
                    self.get_logger().warn(
                        f"Invalid channel_index={selected_channel} for channel_count={channel_count}."
                    )
                    self._invalid_channel_warned = True
                return

        mono = reshaped[:, selected_channel].astype(np.float32, copy=False)
        self._append_chunk(mono)

        if self.debug and channel_rms is not None:
            dbfs = [self._rms_to_dbfs(float(value)) for value in channel_rms.tolist()]
            self.get_logger().debug(
                f"Buffered audio chunk from channel {selected_channel}; "
                f'channel_dbfs={",".join(f"{value:.1f}" for value in dbfs)}'
            )

    def _append_chunk(self, chunk: np.ndarray) -> None:
        if chunk.size == 0:
            return

        stored = np.ascontiguousarray(chunk, dtype=np.float32)
        self._mono_chunks.append(stored)
        self._buffered_samples += int(stored.size)

        while self._buffered_samples > self._max_buffer_samples and self._mono_chunks:
            excess = self._buffered_samples - self._max_buffer_samples
            oldest = self._mono_chunks[0]
            if oldest.size <= excess:
                self._mono_chunks.popleft()
                self._buffered_samples -= int(oldest.size)
                continue
            self._mono_chunks[0] = oldest[excess:]
            self._buffered_samples -= excess
            break

    def _latest_window(self) -> np.ndarray | None:
        if self._buffered_samples < self._window_samples:
            return None

        needed = self._window_samples
        pieces: list[np.ndarray] = []
        for chunk in reversed(self._mono_chunks):
            if needed <= 0:
                break
            if chunk.size <= needed:
                pieces.append(chunk)
                needed -= int(chunk.size)
            else:
                pieces.append(chunk[-needed:])
                needed = 0

        if needed > 0:
            return None

        return np.ascontiguousarray(np.concatenate(list(reversed(pieces))))

    def _evaluate_current_window(self) -> None:
        if not self._ready or self._speaker is None or self._reference_embedding is None:
            self._publish_decision(0.0, False, reason="not_ready")
            return

        window = self._latest_window()
        if window is None or window.size < self._window_samples:
            if self.debug:
                self.get_logger().info(
                    f"Skipping speaker verification: buffered_samples={self._buffered_samples}, "
                    f"required_samples={self._window_samples}."
                )
            return

        rms = float(np.sqrt(np.mean(np.square(window))))
        dbfs = self._rms_to_dbfs(rms)
        if dbfs < self.min_dbfs:
            if self.debug:
                self.get_logger().info(
                    f"Skipping speaker verification: window too quiet ({dbfs:.1f} dBFS < "
                    f"{self.min_dbfs:.1f} dBFS)."
                )
            return

        try:
            pcm = torch.from_numpy(window).unsqueeze(0)
            embedding = self._speaker.extract_embedding_from_pcm(pcm, self.sample_rate)
        except Exception as exc:
            self.get_logger().warn(f"WeSpeaker inference failed; failing closed: {exc}")
            self._publish_decision(0.0, False, reason="inference_error", dbfs=dbfs)
            return

        if embedding is None:
            self.get_logger().warn(
                "WeSpeaker returned an empty embedding for the current window; failing closed."
            )
            self._publish_decision(0.0, False, reason="empty_embedding", dbfs=dbfs)
            return

        try:
            normalized_embedding = self._normalize_embedding(embedding, "current window")
        except Exception as exc:
            self.get_logger().warn(f"Invalid embedding from WeSpeaker; failing closed: {exc}")
            self._publish_decision(0.0, False, reason="invalid_embedding", dbfs=dbfs)
            return

        try:
            score = self._normalized_similarity(normalized_embedding, self._reference_embedding)
        except Exception as exc:
            self.get_logger().warn(f"Speaker similarity computation failed; failing closed: {exc}")
            self._publish_decision(0.0, False, reason="similarity_error", dbfs=dbfs)
            return
        authorized = score >= self.threshold
        self._publish_decision(score, authorized, dbfs=dbfs)

    def _publish_decision(
        self,
        score: float,
        authorized: bool,
        reason: str | None = None,
        dbfs: float | None = None,
    ) -> None:
        previous_authorized = self._last_authorized
        previous_score = self._last_score

        self._last_score = float(score)
        self._last_authorized = bool(authorized)
        self._last_decision_monotonic = time.monotonic()
        self._last_decision_stamp_ns = self.get_clock().now().nanoseconds

        self.score_pub.publish(Float32(data=float(score)))
        self.authorized_pub.publish(Bool(data=bool(authorized)))

        should_log = self.debug
        if previous_authorized is None or previous_authorized != authorized:
            should_log = True
        if previous_score is None or abs(previous_score - score) >= 0.05:
            should_log = True

        if should_log:
            detail_parts = [
                f"score={score:.4f}",
                f"threshold={self.threshold:.4f}",
                f"authorized={authorized}",
            ]
            if dbfs is not None:
                detail_parts.append(f"dbfs={dbfs:.1f}")
            if reason:
                detail_parts.append(f"reason={reason}")
            self.get_logger().info("Speaker decision: " + ", ".join(detail_parts))

    @staticmethod
    def _load_reference_embedding(path: str) -> torch.Tensor:
        cleaned_path = os.path.abspath(os.path.expanduser(path.strip()))
        if not path.strip():
            raise ValueError("reference_embedding_path is empty")
        if not os.path.isfile(cleaned_path):
            raise FileNotFoundError(cleaned_path)

        suffix = os.path.splitext(cleaned_path)[1].lower()
        if suffix == ".npy":
            raw_embedding: Any = np.load(cleaned_path, allow_pickle=False)
        elif suffix == ".pt":
            raw_embedding = torch.load(cleaned_path, map_location="cpu")
        else:
            raise ValueError("reference embedding must be a .pt or .npy file")

        return VoiceSpeakerVerifierNode._normalize_embedding(
            raw_embedding, f'reference file "{cleaned_path}"'
        )

    @staticmethod
    def _normalize_embedding(raw_embedding: Any, label: str) -> torch.Tensor:
        if isinstance(raw_embedding, dict):
            for key in ("embedding", "reference_embedding", "embeddings"):
                if key in raw_embedding:
                    return VoiceSpeakerVerifierNode._normalize_embedding(raw_embedding[key], label)
            if len(raw_embedding) == 1:
                return VoiceSpeakerVerifierNode._normalize_embedding(
                    next(iter(raw_embedding.values())), label
                )
            raise ValueError(f"{label} did not contain a recognizable embedding tensor")

        if isinstance(raw_embedding, torch.Tensor):
            tensor = raw_embedding.detach().cpu().to(dtype=torch.float32).flatten()
        elif isinstance(raw_embedding, np.ndarray):
            tensor = torch.from_numpy(
                np.asarray(raw_embedding, dtype=np.float32)
            ).flatten()
        elif isinstance(raw_embedding, (list, tuple)):
            tensor = torch.tensor(raw_embedding, dtype=torch.float32).flatten()
        else:
            raise TypeError(f"unsupported embedding type: {type(raw_embedding).__name__}")

        if tensor.numel() == 0:
            raise ValueError(f"{label} is empty")
        if not torch.isfinite(tensor).all():
            raise ValueError(f"{label} contains non-finite values")

        norm = float(torch.norm(tensor).item())
        if norm <= 1e-12:
            raise ValueError(f"{label} has near-zero norm")

        return tensor / norm

    @staticmethod
    def _normalized_similarity(
        embedding_a: torch.Tensor,
        embedding_b: torch.Tensor,
    ) -> float:
        if embedding_a.shape != embedding_b.shape:
            raise ValueError(
                f"embedding shape mismatch: {tuple(embedding_a.shape)} != {tuple(embedding_b.shape)}"
            )
        cosine = float(torch.dot(embedding_a, embedding_b).item())
        cosine = max(-1.0, min(1.0, cosine))
        return (cosine + 1.0) / 2.0

    @staticmethod
    def _rms_to_dbfs(rms: float) -> float:
        if rms <= 1e-6:
            return -120.0
        return 20.0 * math.log10(rms / 32768.0)


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
