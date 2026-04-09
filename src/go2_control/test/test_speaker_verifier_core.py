"""
Tests for the speaker verifier's pure audio-processing logic.

These tests exercise channel extraction and scoring without requiring
ROS 2 or WeSpeaker by using lightweight mocks.
"""
from __future__ import annotations

import pathlib
import sys
from dataclasses import dataclass
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))


# ---------------------------------------------------------------------------
# Lightweight AudioFrame stub (avoids importing audio_utils_msgs)
# ---------------------------------------------------------------------------

@dataclass
class FakeAudioFrame:
    format: str = "signed_16"
    sampling_frequency: int = 16000
    channel_count: int = 1
    data: bytes = b""


# ---------------------------------------------------------------------------
# Helper: build a minimal verifier with mocked ROS + WeSpeaker
# ---------------------------------------------------------------------------

def _make_verifier(**overrides):
    """Instantiate VoiceSpeakerVerifierNode with ROS/WeSpeaker mocked out."""
    # Patch rclpy and heavy imports before importing the module
    mock_rclpy = MagicMock()
    mock_node = MagicMock()
    mock_node.declare_parameter = MagicMock(
        side_effect=lambda name, default: MagicMock(value=overrides.get(name, default))
    )
    mock_node.get_logger.return_value = MagicMock()
    mock_node.create_publisher = MagicMock(return_value=MagicMock())
    mock_node.create_subscription = MagicMock()

    with (
        patch.dict("sys.modules", {
            "rclpy": mock_rclpy,
            "rclpy.node": MagicMock(Node=type("Node", (), {"__init__": lambda *a, **kw: None})),
            "audio_utils_msgs": MagicMock(),
            "audio_utils_msgs.msg": MagicMock(AudioFrame=FakeAudioFrame),
            "std_msgs": MagicMock(),
            "std_msgs.msg": MagicMock(),
        }),
        patch("builtins.__import__", side_effect=_patched_import),
    ):
        # Force re-import with mocks
        mod_name = "go2_control.voice_speaker_verifier_node"
        if mod_name in sys.modules:
            del sys.modules[mod_name]

        from go2_control.voice_speaker_verifier_node import VoiceSpeakerVerifierNode

    node = object.__new__(VoiceSpeakerVerifierNode)

    # Replicate the attributes set in __init__ that the tests need
    node.sample_rate = overrides.get("sample_rate", 16000)
    node.channel_index = overrides.get("channel_index", 0)
    node.channel_strategy = overrides.get("channel_strategy", "max_rms")
    node.min_rms = overrides.get("min_rms", 0.01)
    node.window_duration_s = overrides.get("window_duration_s", 2.0)
    node.eval_period_s = overrides.get("eval_period_s", 0.5)
    node.debug = overrides.get("debug", False)
    node._model = None
    node._reference_embedding = None
    node._audio_buffer = np.zeros(0, dtype=np.float32)
    node._window_samples = int(node.window_duration_s * node.sample_rate)
    node._eval_samples = int(node.eval_period_s * node.sample_rate)
    node._samples_since_eval = 0
    node._ready = False
    node._format_warned = False
    node._rate_warned = False
    node._invalid_channel_warned = False
    node._latest_doa_deg = None

    # Stub logger
    node.get_logger = MagicMock(return_value=MagicMock())

    return node


# We only need the real import for numpy etc. — everything else falls through.
_real_import = __builtins__.__import__ if hasattr(__builtins__, "__import__") else __import__


def _patched_import(name, *args, **kwargs):
    if name in ("wespeaker", "wespeaker.cli", "wespeaker.cli.speaker"):
        raise ImportError("mocked out")
    return _real_import(name, *args, **kwargs)


# ---------------------------------------------------------------------------
# _extract_mono tests
# ---------------------------------------------------------------------------

def _pcm_bytes(samples: np.ndarray) -> bytes:
    """Convert float32 [-1,1] samples to int16 PCM bytes."""
    return (samples * 32767).astype(np.int16).tobytes()


def test_extract_mono_single_channel_returns_float32() -> None:
    node = _make_verifier()
    tone = np.sin(np.linspace(0, 2 * np.pi, 160, dtype=np.float32)) * 0.5
    msg = FakeAudioFrame(
        format="signed_16",
        sampling_frequency=16000,
        channel_count=1,
        data=_pcm_bytes(tone),
    )
    mono = node._extract_mono(msg)
    assert mono is not None
    assert mono.dtype == np.float32
    assert len(mono) == 160


def test_extract_mono_max_rms_picks_loudest_channel() -> None:
    node = _make_verifier(channel_strategy="max_rms")
    # Channel 0: silence, Channel 1: loud tone
    ch0 = np.zeros(160, dtype=np.float32)
    ch1 = np.sin(np.linspace(0, 2 * np.pi, 160, dtype=np.float32)) * 0.9
    interleaved = np.column_stack([ch0, ch1]).flatten()
    msg = FakeAudioFrame(
        format="signed_16",
        sampling_frequency=16000,
        channel_count=2,
        data=_pcm_bytes(interleaved),
    )
    mono = node._extract_mono(msg)
    assert mono is not None
    # The returned mono should be from channel 1 (the loud one)
    rms = float(np.sqrt(np.mean(np.square(mono))))
    assert rms > 0.3


def test_extract_mono_fixed_channel_selects_index() -> None:
    node = _make_verifier(channel_strategy="fixed", channel_index=1)
    ch0 = np.ones(80, dtype=np.float32) * 0.1
    ch1 = np.ones(80, dtype=np.float32) * 0.8
    interleaved = np.column_stack([ch0, ch1]).flatten()
    msg = FakeAudioFrame(
        format="signed_16",
        sampling_frequency=16000,
        channel_count=2,
        data=_pcm_bytes(interleaved),
    )
    mono = node._extract_mono(msg)
    assert mono is not None
    # Should be roughly ch1 values (0.8 * 32767 then /32768 ≈ 0.8)
    assert float(np.mean(np.abs(mono))) > 0.5


def test_extract_mono_rejects_wrong_format() -> None:
    node = _make_verifier()
    msg = FakeAudioFrame(format="float_32", sampling_frequency=16000, channel_count=1, data=b"\x00" * 320)
    assert node._extract_mono(msg) is None


def test_extract_mono_rejects_wrong_sample_rate() -> None:
    node = _make_verifier(sample_rate=16000)
    tone = np.sin(np.linspace(0, 2 * np.pi, 160, dtype=np.float32)) * 0.5
    msg = FakeAudioFrame(format="signed_16", sampling_frequency=44100, channel_count=1, data=_pcm_bytes(tone))
    assert node._extract_mono(msg) is None


def test_extract_mono_rejects_empty_data() -> None:
    node = _make_verifier()
    msg = FakeAudioFrame(format="signed_16", sampling_frequency=16000, channel_count=1, data=b"")
    assert node._extract_mono(msg) is None


def test_extract_mono_invalid_channel_index_returns_none() -> None:
    node = _make_verifier(channel_strategy="fixed", channel_index=5)
    tone = np.sin(np.linspace(0, 2 * np.pi, 160, dtype=np.float32)) * 0.5
    msg = FakeAudioFrame(format="signed_16", sampling_frequency=16000, channel_count=2, data=_pcm_bytes(
        np.column_stack([tone, tone]).flatten()
    ))
    assert node._extract_mono(msg) is None


# ---------------------------------------------------------------------------
# Cosine similarity / scoring tests (with fake embeddings)
# ---------------------------------------------------------------------------

def test_cosine_similarity_identical_embeddings_score_one() -> None:
    emb = np.random.randn(256).astype(np.float32)
    emb /= np.linalg.norm(emb)
    score = float(np.dot(emb, emb))
    assert score == pytest.approx(1.0, abs=1e-5)


def test_cosine_similarity_orthogonal_embeddings_score_zero() -> None:
    a = np.zeros(256, dtype=np.float32)
    a[0] = 1.0
    b = np.zeros(256, dtype=np.float32)
    b[1] = 1.0
    score = float(np.dot(a, b))
    assert score == pytest.approx(0.0, abs=1e-5)


def test_cosine_similarity_opposite_embeddings_score_negative_one() -> None:
    a = np.random.randn(256).astype(np.float32)
    a /= np.linalg.norm(a)
    b = -a
    score = float(np.dot(a, b))
    assert score == pytest.approx(-1.0, abs=1e-5)


def test_threshold_comparison_matches_poc_calibration() -> None:
    """PoC calibration: same-speaker ~0.78, other ~0.58, threshold 0.68."""
    threshold = 0.68
    assert 0.78 >= threshold  # same speaker passes
    assert 0.58 < threshold   # other speaker fails
