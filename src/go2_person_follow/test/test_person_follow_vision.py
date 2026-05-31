from __future__ import annotations

import importlib.util
import math
import pathlib
import sys
from types import SimpleNamespace

import numpy as np

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "person_follow_vision_node.py"
spec = importlib.util.spec_from_file_location("person_follow_vision_node", MODULE_PATH)
vision = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = vision
spec.loader.exec_module(vision)


def _detection(class_id: str, score: float, *, center=(320.0, 320.0), size=(80.0, 160.0), detection_id=""):
    return SimpleNamespace(
        id=detection_id,
        bbox=SimpleNamespace(
            center=SimpleNamespace(position=SimpleNamespace(x=center[0], y=center[1])),
            size_x=size[0],
            size_y=size[1],
        ),
        results=[
            SimpleNamespace(
                hypothesis=SimpleNamespace(class_id=class_id, score=score),
            )
        ],
    )


def test_select_best_candidate_filters_person_class_id():
    detections = [
        _detection("2", 0.99, detection_id="11"),
        _detection("0", 0.70, detection_id="12"),
        _detection("0", 0.90, detection_id="13"),
    ]

    candidate = vision._select_best_candidate(detections, "0", "person")

    assert candidate is not None
    assert candidate.class_id == "0"
    assert candidate.score == 0.90
    assert candidate.target_id == 13


def test_select_best_candidate_accepts_person_label_fallback():
    detections = [_detection("person", 0.82, detection_id="not-an-int")]

    candidate = vision._select_best_candidate(detections, "0", "person")

    assert candidate is not None
    assert candidate.class_id == "person"
    assert candidate.target_id == 0


def test_network_to_source_pixel_removes_letterbox_padding():
    assert vision._network_to_source_pixel(
        320.0, 320.0, 640.0, 640.0, 640.0, 360.0, True, True
    ) == (320.0, 180.0)
    assert vision._network_to_source_pixel(
        320.0, 140.0, 640.0, 640.0, 640.0, 360.0, True, True
    ) == (320.0, 0.0)


def test_sample_depth_uses_median_valid_depth_in_meters():
    depth = np.zeros((5, 5), dtype=np.uint16)
    depth[2, 1] = 2000
    depth[2, 2] = 0
    depth[2, 3] = 4000

    sampled = vision._sample_depth_m(depth, 2.0, 2.0, "16UC1", 1, 0.2, 8.0)

    assert sampled == 3.0


def test_sample_depth_rejects_invalid_or_out_of_bounds_depth():
    depth = np.array([[math.nan, 0.0], [9.0, -1.0]], dtype=np.float32)

    assert vision._sample_depth_m(depth, 0.0, 0.0, "32FC1", 1, 0.2, 8.0) is None
    assert vision._sample_depth_m(depth, 9.0, 0.0, "32FC1", 1, 0.2, 8.0) is None


def test_project_pixel_to_3d_uses_pinhole_intrinsics():
    intrinsics = vision.CameraIntrinsics(
        fx=100.0,
        fy=100.0,
        cx=50.0,
        cy=60.0,
        width=100,
        height=100,
        frame_id="camera_color_optical_frame",
    )

    point = vision._project_pixel_to_3d(60.0, 40.0, 2.0, intrinsics)

    assert point == (0.2, -0.4, 2.0)
