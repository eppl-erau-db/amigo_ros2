"""
Pure helpers for accumulating and persisting the ArUco-marker table recorded
during an "explore the area" session.

No ROS dependency — only PyYAML + math — so this is directly unit-testable and
shared by the recorder node (write) and the deliver action server (read).

Sidecar file format (``<map>.aruco.yaml``):

    map_frame: map
    markers:
      40:
        position: [x, y, z]
        orientation: [qx, qy, qz, qw]
        samples: 12
"""
from __future__ import annotations

from dataclasses import dataclass, field

import yaml


@dataclass
class MarkerEstimate:
    marker_id: int
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    qx: float = 0.0
    qy: float = 0.0
    qz: float = 0.0
    qw: float = 1.0
    samples: int = 0

    def as_yaml(self) -> dict:
        return {
            "position": [float(self.x), float(self.y), float(self.z)],
            "orientation": [float(self.qx), float(self.qy), float(self.qz), float(self.qw)],
            "samples": int(self.samples),
        }


@dataclass
class MarkerAccumulator:
    """Running estimate of each marker's map-frame pose.

    Position is a running mean over samples (markers are static, so this rejects
    per-frame jitter); orientation keeps the most recent observation (quaternion
    averaging is not worth the complexity for a static fiducial).
    """

    markers: dict[int, MarkerEstimate] = field(default_factory=dict)

    def update(self, marker_id: int, x, y, z, qx, qy, qz, qw) -> MarkerEstimate:
        marker_id = int(marker_id)
        est = self.markers.get(marker_id)
        if est is None:
            est = MarkerEstimate(marker_id=marker_id, x=x, y=y, z=z,
                                 qx=qx, qy=qy, qz=qz, qw=qw, samples=1)
            self.markers[marker_id] = est
            return est
        n = est.samples
        est.x = (est.x * n + x) / (n + 1)
        est.y = (est.y * n + y) / (n + 1)
        est.z = (est.z * n + z) / (n + 1)
        est.qx, est.qy, est.qz, est.qw = qx, qy, qz, qw
        est.samples = n + 1
        return est

    def count(self) -> int:
        return len(self.markers)


def save_markers(path: str, accumulator: MarkerAccumulator, map_frame: str = "map") -> None:
    data = {
        "map_frame": str(map_frame),
        "markers": {
            int(mid): est.as_yaml() for mid, est in sorted(accumulator.markers.items())
        },
    }
    with open(path, "w") as handle:
        yaml.safe_dump(data, handle, default_flow_style=False, sort_keys=True)


def load_markers(path: str) -> tuple[str, dict[int, MarkerEstimate]]:
    """Return ``(map_frame, {id: MarkerEstimate})`` from a sidecar file."""
    with open(path) as handle:
        data = yaml.safe_load(handle) or {}
    map_frame = str(data.get("map_frame", "map"))
    out: dict[int, MarkerEstimate] = {}
    for mid, entry in (data.get("markers") or {}).items():
        pos = list(entry.get("position", [0.0, 0.0, 0.0]))
        ori = list(entry.get("orientation", [0.0, 0.0, 0.0, 1.0]))
        pos += [0.0] * (3 - len(pos))
        ori += [0.0, 0.0, 0.0, 1.0][len(ori):]
        out[int(mid)] = MarkerEstimate(
            marker_id=int(mid),
            x=float(pos[0]), y=float(pos[1]), z=float(pos[2]),
            qx=float(ori[0]), qy=float(ori[1]), qz=float(ori[2]), qw=float(ori[3]),
            samples=int(entry.get("samples", 0)),
        )
    return map_frame, out
