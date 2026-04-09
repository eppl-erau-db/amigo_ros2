#!/usr/bin/env python3
from __future__ import annotations

import math
from typing import Dict

import rclpy
from rclpy.node import Node
from visualization_msgs.msg import MarkerArray


def yaw_from_quaternion_xyzw(x: float, y: float, z: float, w: float) -> float:
    del x, y
    t3 = 2.0 * (w * z)
    t4 = 1.0 - 2.0 * (z * z)
    return math.atan2(t3, t4)


class ExploreAreaLandmarkWatch(Node):
    def __init__(self) -> None:
        super().__init__("explore_area_landmark_watch")
        self.marker_topic = str(
            self.declare_parameter("marker_topic", "/explore_area/landmark_markers").value
        )
        self._last_snapshot: Dict[str, tuple[float, float, float, float]] = {}
        self.create_subscription(MarkerArray, self.marker_topic, self._markers_cb, 10)
        self.get_logger().info(
            f'Watching explore-area landmarks on "{self.marker_topic}".'
        )

    def _markers_cb(self, msg: MarkerArray) -> None:
        labels_by_group: dict[int, str] = {}
        body_markers: list[tuple[int, any]] = []

        for marker in msg.markers:
            if marker.action != marker.ADD:
                continue
            if marker.ns == "observed_landmarks_label":
                labels_by_group[marker.id // 3] = str(marker.text)
            elif marker.ns == "observed_landmarks_body":
                body_markers.append((marker.id // 3, marker))

        for group_id, marker in body_markers:
            label = labels_by_group.get(group_id, f"group_{group_id}")
            yaw = yaw_from_quaternion_xyzw(
                marker.pose.orientation.x,
                marker.pose.orientation.y,
                marker.pose.orientation.z,
                marker.pose.orientation.w,
            )
            snapshot = (
                float(marker.pose.position.x),
                float(marker.pose.position.y),
                float(marker.pose.position.z),
                float(yaw),
            )
            previous = self._last_snapshot.get(label)
            if previous == snapshot:
                continue
            self._last_snapshot[label] = snapshot
            print(
                f"{label}: "
                f"x={snapshot[0]:.4f} y={snapshot[1]:.4f} z={snapshot[2]:.4f} "
                f"yaw_rad={snapshot[3]:.4f} yaw_deg={math.degrees(snapshot[3]):.1f}",
                flush=True,
            )


def main() -> int:
    rclpy.init()
    node = ExploreAreaLandmarkWatch()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
