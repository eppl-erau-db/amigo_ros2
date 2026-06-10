from __future__ import annotations

import os
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from go2_control.aruco_map_store import (  # noqa: E402
    MarkerAccumulator,
    load_markers,
    save_markers,
)


def test_accumulator_running_mean_position() -> None:
    acc = MarkerAccumulator()
    acc.update(7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
    acc.update(7, 2.0, 4.0, 0.0, 0.0, 0.0, 0.0, 1.0)
    est = acc.markers[7]
    assert est.samples == 2
    assert est.x == 1.0
    assert est.y == 2.0
    assert acc.count() == 1


def test_accumulator_tracks_multiple_markers() -> None:
    acc = MarkerAccumulator()
    acc.update(1, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
    acc.update(2, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0)
    assert acc.count() == 2
    assert set(acc.markers) == {1, 2}


def test_save_load_roundtrip() -> None:
    acc = MarkerAccumulator()
    acc.update(0, 1.5, -2.0, 0.3, 0.0, 0.0, 0.707, 0.707)
    acc.update(0, 1.5, -2.0, 0.3, 0.0, 0.0, 0.707, 0.707)
    acc.update(5, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)

    fd, path = tempfile.mkstemp(suffix=".aruco.yaml")
    os.close(fd)
    try:
        save_markers(path, acc, map_frame="map")
        frame, markers = load_markers(path)
        assert frame == "map"
        assert set(markers) == {0, 5}
        assert markers[0].x == 1.5
        assert markers[0].y == -2.0
        assert markers[0].samples == 2
        assert markers[0].qz == 0.707
        assert markers[5].x == 3.0
    finally:
        os.remove(path)


def test_load_tolerates_missing_fields() -> None:
    import yaml

    fd, path = tempfile.mkstemp(suffix=".yaml")
    os.close(fd)
    try:
        with open(path, "w") as handle:
            yaml.safe_dump({"map_frame": "map", "markers": {3: {"position": [1.0, 2.0]}}}, handle)
        frame, markers = load_markers(path)
        assert frame == "map"
        assert markers[3].x == 1.0 and markers[3].y == 2.0 and markers[3].z == 0.0
        # Missing orientation defaults to identity.
        assert markers[3].qw == 1.0
    finally:
        os.remove(path)
