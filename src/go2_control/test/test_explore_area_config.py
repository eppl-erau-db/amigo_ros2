from __future__ import annotations

import math
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

if not hasattr(np, "float"):
    np.float = float  # type: ignore[attr-defined]

from go2_control.explore_area_action_server import (  # noqa: E402
    adjust_pose_correction_target,
    ArucoDetectorCompat,
    normalize_quaternion_xyzw,
    parse_fixed_marker_pose_config,
    quaternion_from_euler,
    quaternion_matrix,
    rpy_from_quaternion_xyzw,
    yaw_from_quaternion_xyzw,
)


def test_aruco_detector_compat_uses_modern_api_when_available() -> None:
    class FakeModernArucoModule:
        DICT_6X6_1000 = 99

        @staticmethod
        def getPredefinedDictionary(dictionary_id):
            return f"dict:{dictionary_id}"

        class DetectorParameters:
            pass

        class ArucoDetector:
            def __init__(self, dictionary, detector_parameters) -> None:
                self.dictionary = dictionary
                self.detector_parameters = detector_parameters

            def detectMarkers(self, image):
                return (image, self.dictionary, self.detector_parameters, "modern")

    detector = ArucoDetectorCompat.from_module(FakeModernArucoModule, 17)

    result = detector.detectMarkers("frame")

    assert result[0] == "frame"
    assert result[1] == "dict:17"
    assert result[3] == "modern"


def test_aruco_detector_compat_falls_back_to_legacy_api() -> None:
    class FakeLegacyArucoModule:
        DICT_6X6_1000 = 99

        @staticmethod
        def getPredefinedDictionary(dictionary_id):
            return f"dict:{dictionary_id}"

        @staticmethod
        def DetectorParameters_create():
            return "legacy-params"

        @staticmethod
        def detectMarkers(image, dictionary, parameters=None):
            return (image, dictionary, parameters, "legacy")

    detector = ArucoDetectorCompat.from_module(FakeLegacyArucoModule, 23)

    result = detector.detectMarkers("frame")

    assert result == ("frame", "dict:23", "legacy-params", "legacy")


def test_yaw_from_quaternion_xyzw_accepts_tuple_input() -> None:
    yaw = yaw_from_quaternion_xyzw((0.0, 0.0, math.sin(math.pi / 4.0), math.cos(math.pi / 4.0)))

    assert math.isclose(yaw, math.pi / 2.0, rel_tol=1e-6)


def test_rpy_from_quaternion_xyzw_accepts_tuple_input() -> None:
    roll, pitch, yaw = rpy_from_quaternion_xyzw(
        (0.0, 0.0, math.sin(math.pi / 4.0), math.cos(math.pi / 4.0))
    )

    assert math.isclose(roll, 0.0, abs_tol=1e-6)
    assert math.isclose(pitch, 0.0, abs_tol=1e-6)
    assert math.isclose(yaw, math.pi / 2.0, rel_tol=1e-6)


def test_adjust_pose_correction_target_preserves_z_roll_and_pitch() -> None:
    current_quat = quaternion_from_euler(0.2, -0.1, 0.3)
    current_matrix = quaternion_matrix(current_quat)
    current_matrix[0, 3] = 1.0
    current_matrix[1, 3] = 2.0
    current_matrix[2, 3] = 0.6

    corrected_quat = quaternion_from_euler(-0.4, 0.35, 1.1)
    corrected_matrix = quaternion_matrix(corrected_quat)
    corrected_matrix[0, 3] = 4.0
    corrected_matrix[1, 3] = 5.0
    corrected_matrix[2, 3] = 1.8

    adjusted_matrix, adjusted_rpy, adjusted_quat = adjust_pose_correction_target(
        corrected_matrix,
        current_matrix,
        preserve_z=True,
        preserve_roll_pitch=True,
    )

    assert math.isclose(adjusted_matrix[0, 3], 4.0, abs_tol=1e-6)
    assert math.isclose(adjusted_matrix[1, 3], 5.0, abs_tol=1e-6)
    assert math.isclose(adjusted_matrix[2, 3], 0.6, abs_tol=1e-6)
    assert math.isclose(adjusted_rpy[0], 0.2, abs_tol=1e-6)
    assert math.isclose(adjusted_rpy[1], -0.1, abs_tol=1e-6)
    assert math.isclose(adjusted_rpy[2], 1.1, abs_tol=1e-6)
    adjusted_roll, adjusted_pitch, adjusted_yaw = rpy_from_quaternion_xyzw(adjusted_quat)
    assert math.isclose(adjusted_roll, 0.2, abs_tol=1e-6)
    assert math.isclose(adjusted_pitch, -0.1, abs_tol=1e-6)
    assert math.isclose(adjusted_yaw, 1.1, abs_tol=1e-6)


def test_parse_fixed_marker_pose_config_with_rpy_orientation() -> None:
    position, quaternion = parse_fixed_marker_pose_config(
        {
            "position": [1.0, 2.0, 0.5],
            "orientation": [0.0, 0.0, math.pi / 2.0],
        }
    )

    assert position == (1.0, 2.0, 0.5)
    assert math.isclose(quaternion[2], math.sin(math.pi / 4.0), rel_tol=1e-6)
    assert math.isclose(quaternion[3], math.cos(math.pi / 4.0), rel_tol=1e-6)


def test_parse_fixed_marker_pose_config_with_quaternion() -> None:
    position, quaternion = parse_fixed_marker_pose_config(
        {
            "position": [0.0, 0.0, 1.0],
            "quaternion": [0.0, 0.0, 0.0, 2.0],
        }
    )

    assert position == (0.0, 0.0, 1.0)
    assert quaternion == (0.0, 0.0, 0.0, 1.0)


def test_parse_fixed_marker_pose_config_rejects_conflicting_orientation_formats() -> None:
    try:
        parse_fixed_marker_pose_config(
            {
                "position": [0.0, 0.0, 0.0],
                "orientation": [0.0, 0.0, 0.0],
                "quaternion": [0.0, 0.0, 0.0, 1.0],
            }
        )
    except ValueError as exc:
        assert "Specify only one" in str(exc)
    else:
        raise AssertionError("Expected conflicting fixed_map_pose formats to fail")


def test_normalize_quaternion_xyzw_rejects_zero_norm() -> None:
    try:
        normalize_quaternion_xyzw([0.0, 0.0, 0.0, 0.0])
    except ValueError as exc:
        assert "non-zero magnitude" in str(exc)
    else:
        raise AssertionError("Expected zero quaternion normalization to fail")
