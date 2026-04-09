#!/usr/bin/env python3
"""
Speaker enrollment node that records from the ODAS /sss topic.

Records audio clips from the same source-separated audio stream that the live
speaker verifier uses, ensuring embedding compatibility.

Usage (while ODAS is running):
    ros2 run go2_control enroll_speaker_node \
        --ros-args -p output_path:=models/speaker_ref.npy -p clip_count:=6
"""

from __future__ import annotations

import sys
import threading
from pathlib import Path

import numpy as np
import rclpy
from rclpy.node import Node
from audio_utils_msgs.msg import AudioFrame

# Must match the normalization in voice_speaker_verifier_node.py
_TARGET_RMS = 0.10


def _normalize_audio(audio: np.ndarray, target_rms: float = _TARGET_RMS) -> np.ndarray:
    """Normalize audio to a target RMS level."""
    rms = float(np.sqrt(np.mean(np.square(audio))))
    if rms < 1e-8:
        return audio
    return audio * (target_rms / rms)


class EnrollSpeakerNode(Node):
    def __init__(self) -> None:
        super().__init__("enroll_speaker_node")

        self.output_path = str(
            self.declare_parameter("output_path", "speaker_ref.npy").value
        ).strip()
        self.model_name_or_path = str(
            self.declare_parameter("model_name_or_path", "eres2net").value
        )
        self.audio_topic = str(
            self.declare_parameter("audio_topic", "/sss").value
        )
        self.clip_count = int(
            self.declare_parameter("clip_count", 6).value
        )
        self.window_duration_s = float(
            self.declare_parameter("window_duration_s", 3.0).value
        )
        self.sample_rate = int(
            self.declare_parameter("sample_rate", 16000).value
        )
        self.channel_strategy = str(
            self.declare_parameter("channel_strategy", "max_rms").value
        ).strip().lower()
        self.min_rms = float(
            self.declare_parameter("min_rms", 0.005).value
        )

        self._window_samples = int(self.window_duration_s * self.sample_rate)
        self._audio_buffer = np.zeros(0, dtype=np.float32)
        self._lock = threading.Lock()
        self._format_warned = False

        # Load WeSpeaker model
        self.get_logger().info(f'Loading WeSpeaker model: "{self.model_name_or_path}" ...')
        try:
            from wespeaker.cli.speaker import load_model
            self._model = load_model(self.model_name_or_path)
            self.get_logger().info("WeSpeaker model loaded.")
        except Exception as exc:
            self.get_logger().error(f"Failed to load WeSpeaker model: {exc}")
            raise SystemExit(1)

        # Subscribe to audio
        self.create_subscription(AudioFrame, self.audio_topic, self._audio_cb, 10)

        self.get_logger().info(
            f'Enrollment node ready. Listening on "{self.audio_topic}".\n'
            f"  Clips to collect: {self.clip_count}\n"
            f"  Window duration:  {self.window_duration_s}s\n"
            f"  Output path:      {self.output_path}\n"
        )

        # Run the interactive prompt in a background thread
        self._prompt_thread = threading.Thread(target=self._interactive_loop, daemon=True)
        self._prompt_thread.start()

    def _extract_mono(self, msg: AudioFrame) -> np.ndarray | None:
        """Extract mono float32 audio from AudioFrame (same logic as verifier)."""
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
            selected = 0

        mono = reshaped[:, selected].astype(np.float32) / 32768.0
        return mono

    def _audio_cb(self, msg: AudioFrame) -> None:
        mono = self._extract_mono(msg)
        if mono is None:
            return
        with self._lock:
            # Always buffer a little so we can detect the stream is alive,
            # but only accumulate fully when recording.
            if getattr(self, "_recording", False):
                self._audio_buffer = np.concatenate([self._audio_buffer, mono])
            else:
                # Keep a tiny buffer just to confirm audio is flowing
                self._audio_buffer = np.concatenate([self._audio_buffer, mono])
                if len(self._audio_buffer) > self.sample_rate:
                    self._audio_buffer = self._audio_buffer[-self.sample_rate:]

    def _start_recording(self) -> None:
        """Clear the buffer and start capturing fresh audio."""
        with self._lock:
            self._audio_buffer = np.zeros(0, dtype=np.float32)
            self._recording = True

    def _stop_recording(self) -> np.ndarray | None:
        """Stop recording and return whatever was captured."""
        with self._lock:
            self._recording = False
            if len(self._audio_buffer) == 0:
                return None
            return self._audio_buffer.copy()

    def _extract_embedding(self, audio: np.ndarray) -> np.ndarray | None:
        """Extract embedding using the same method as the live verifier."""
        import torch

        rms = float(np.sqrt(np.mean(np.square(audio))))
        if rms < self.min_rms:
            self.get_logger().warn(
                f"Window too quiet (rms={rms:.5f}). Speak louder or move closer."
            )
            return None

        # Normalize to target RMS — must match the verifier's normalization
        normalized = _normalize_audio(audio)
        waveform = torch.from_numpy(normalized).unsqueeze(0)  # (1, samples)
        emb = self._model.extract_embedding_from_pcm(waveform, sample_rate=self.sample_rate)

        if isinstance(emb, torch.Tensor):
            emb = emb.detach().cpu().numpy()

        emb = emb.flatten().astype(np.float32)
        norm = np.linalg.norm(emb)
        if norm < 1e-8:
            return None
        return emb / norm

    def _interactive_loop(self) -> None:
        """Interactive prompt loop running in a background thread."""
        import time

        self._recording = False

        # Give audio buffer time to fill
        print("\nWaiting for audio stream to start...")
        time.sleep(3.0)

        with self._lock:
            buf_len = len(self._audio_buffer)
        if buf_len == 0:
            print(f'ERROR: No audio received on "{self.audio_topic}" after 3s.')
            print("Make sure ODAS is running and publishing to this topic.")
            rclpy.shutdown()
            return

        print(f"\n{'='*60}")
        print("SPEAKER ENROLLMENT")
        print(f"{'='*60}")
        print(f"Collect {self.clip_count} voice clips from the ODAS audio stream.")
        print()
        print("Instructions:")
        print("  1. Press Enter to START recording")
        print("  2. Speak a phrase (e.g. 'hey amigo', 'amigo follow me')")
        print("  3. Press Enter to STOP recording")
        print("  4. Repeat for each clip")
        print("  Type 'q' then Enter at any prompt to quit early")
        print(f"{'='*60}\n")

        embeddings: list[np.ndarray] = []

        for i in range(self.clip_count):
            # --- Wait for user to start recording ---
            try:
                response = input(
                    f"Clip {i+1}/{self.clip_count} — press Enter to START recording (q to quit): "
                )
            except (EOFError, KeyboardInterrupt):
                print("\nInterrupted.")
                break

            if response.strip().lower() == "q":
                print("Stopping enrollment.")
                break

            self._start_recording()
            print("  *** RECORDING — speak now! ***")

            # --- Wait for user to stop recording ---
            try:
                response = input("  Press Enter to STOP recording (q to quit): ")
            except (EOFError, KeyboardInterrupt):
                print("\nInterrupted.")
                break

            audio = self._stop_recording()

            if response.strip().lower() == "q":
                print("Stopping enrollment.")
                break

            if audio is None or len(audio) == 0:
                print("  No audio captured. Try again.")
                continue

            duration_s = len(audio) / self.sample_rate
            print(f"  Captured {duration_s:.1f}s of audio. Extracting embedding...")

            emb = self._extract_embedding(audio)
            if emb is None:
                print("  Failed to extract embedding. Try speaking louder.")
                continue

            embeddings.append(emb)
            rms = float(np.sqrt(np.mean(np.square(audio))))
            print(f"  Captured clip {len(embeddings)} (rms={rms:.4f}, emb_norm=1.0)")

        if len(embeddings) < 1:
            print("\nERROR: No embeddings collected. Cannot save reference.")
            rclpy.shutdown()
            return

        if len(embeddings) < 3:
            print(f"\nWARNING: Only {len(embeddings)} clip(s). 3+ recommended for robust reference.")

        # Average and normalize
        avg = np.mean(np.stack(embeddings), axis=0).astype(np.float32)
        avg_norm = np.linalg.norm(avg)
        if avg_norm < 1e-8:
            print("ERROR: Averaged embedding has near-zero norm.")
            rclpy.shutdown()
            return
        reference = avg / avg_norm

        # Save
        output_path = Path(self.output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        np.save(str(output_path), reference)
        print(f"\nSaved reference embedding:")
        print(f"  Path:  {output_path.resolve()}")
        print(f"  Shape: {reference.shape}")
        print(f"  Norm:  {np.linalg.norm(reference):.6f}")
        print(f"  From {len(embeddings)} clip(s).")
        print("\nDone! You can now use this reference with the speaker verifier.")

        rclpy.shutdown()


def main() -> None:
    rclpy.init()
    node = EnrollSpeakerNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
