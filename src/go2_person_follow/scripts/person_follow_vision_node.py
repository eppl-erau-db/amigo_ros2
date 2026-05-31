#!/usr/bin/env python3
from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Sequence

import cv_bridge
import message_filters
import numpy as np
import rclpy
from geometry_msgs.msg import PointStamped
from rcl_interfaces.msg import ParameterDescriptor
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import CameraInfo, Image
from std_msgs.msg import Bool, Int32, String
from vision_msgs.msg import Detection2DArray


@dataclass(frozen=True)
class CameraIntrinsics:
    fx: float
    fy: float
    cx: float
    cy: float
    width: int
    height: int
    frame_id: str


@dataclass(frozen=True)
class DetectionCandidate:
    detection_index: int
    target_id: int
    class_id: str
    score: float
    center_x: float
    center_y: float
    size_x: float
    size_y: float


def _class_matches(class_id: str, target_class_id: str, target_label: str) -> bool:
    normalized = str(class_id).strip().lower()
    return normalized in {
        str(target_class_id).strip().lower(),
        str(target_label).strip().lower(),
        "person",
    }


def _select_best_candidate(
    detections: Sequence,
    target_class_id: str,
    target_label: str,
) -> DetectionCandidate | None:
    best: DetectionCandidate | None = None
    best_key: tuple[float, float, int] | None = None

    for detection_index, detection in enumerate(detections):
        bbox = getattr(detection, "bbox", None)
        if bbox is None:
            continue

        center = getattr(bbox, "center", None)
        position = getattr(center, "position", None)
        if position is None:
            continue

        center_x = float(getattr(position, "x", math.nan))
        center_y = float(getattr(position, "y", math.nan))
        size_x = float(getattr(bbox, "size_x", math.nan))
        size_y = float(getattr(bbox, "size_y", math.nan))
        if not all(math.isfinite(value) for value in (center_x, center_y, size_x, size_y)):
            continue
        if size_x <= 0.0 or size_y <= 0.0:
            continue

        matched_class_id = ""
        matched_score = -math.inf
        for result in getattr(detection, "results", []):
            hypothesis = getattr(result, "hypothesis", result)
            class_id = str(getattr(hypothesis, "class_id", "")).strip()
            if not _class_matches(class_id, target_class_id, target_label):
                continue
            score = float(getattr(hypothesis, "score", 0.0))
            if score > matched_score:
                matched_score = score
                matched_class_id = class_id

        if matched_score == -math.inf:
            continue

        raw_id = str(getattr(detection, "id", "")).strip()
        try:
            target_id = int(raw_id)
        except ValueError:
            target_id = detection_index

        candidate = DetectionCandidate(
            detection_index=detection_index,
            target_id=target_id,
            class_id=matched_class_id,
            score=matched_score,
            center_x=center_x,
            center_y=center_y,
            size_x=size_x,
            size_y=size_y,
        )
        key = (candidate.score, candidate.size_x * candidate.size_y, -candidate.detection_index)
        if best_key is None or key > best_key:
            best = candidate
            best_key = key

    return best


def _network_to_source_pixel(
    x: float,
    y: float,
    network_width: float,
    network_height: float,
    source_width: float,
    source_height: float,
    keep_aspect_ratio: bool,
    enable_padding: bool,
) -> tuple[float, float]:
    if network_width <= 0.0 or network_height <= 0.0:
        return x, y
    if source_width <= 0.0 or source_height <= 0.0:
        return x, y

    if not keep_aspect_ratio:
        return x * (source_width / network_width), y * (source_height / network_height)

    width_scale = network_width / source_width
    height_scale = network_height / source_height
    scale = min(width_scale, height_scale) if enable_padding else max(width_scale, height_scale)
    scaled_width = source_width * scale
    scaled_height = source_height * scale
    offset_x = (network_width - scaled_width) * 0.5
    offset_y = (network_height - scaled_height) * 0.5
    return (x - offset_x) / scale, (y - offset_y) / scale


def _depth_scale_for_encoding(encoding: str, dtype: np.dtype) -> float:
    normalized = str(encoding).strip().lower()
    if normalized in {"16uc1", "mono16"} or np.issubdtype(dtype, np.uint16):
        return 0.001
    return 1.0


def _sample_depth_m(
    depth_image: np.ndarray,
    x: float,
    y: float,
    encoding: str,
    window_radius_px: int,
    min_depth_m: float,
    max_depth_m: float,
) -> float | None:
    if depth_image.ndim == 3:
        depth_image = depth_image[:, :, 0]

    height, width = depth_image.shape[:2]
    column = int(round(x))
    row = int(round(y))
    if column < 0 or row < 0 or column >= width or row >= height:
        return None

    radius = max(0, int(window_radius_px))
    x0 = max(0, column - radius)
    x1 = min(width, column + radius + 1)
    y0 = max(0, row - radius)
    y1 = min(height, row + radius + 1)

    window = depth_image[y0:y1, x0:x1].astype(np.float64, copy=False)
    values = window.reshape(-1) * _depth_scale_for_encoding(encoding, depth_image.dtype)
    valid = values[
        np.isfinite(values) &
        (values >= float(min_depth_m)) &
        (values <= float(max_depth_m))
    ]
    if valid.size == 0:
        return None
    return float(np.median(valid))


def _project_pixel_to_3d(
    x: float,
    y: float,
    depth_m: float,
    intrinsics: CameraIntrinsics,
) -> tuple[float, float, float] | None:
    if intrinsics.fx <= 0.0 or intrinsics.fy <= 0.0:
        return None
    if not all(math.isfinite(value) for value in (x, y, depth_m)):
        return None
    return (
        ((x - intrinsics.cx) * depth_m) / intrinsics.fx,
        ((y - intrinsics.cy) * depth_m) / intrinsics.fy,
        depth_m,
    )


def _camera_intrinsics_from_msg(msg: CameraInfo) -> CameraIntrinsics | None:
    if len(msg.k) < 9:
        return None
    fx = float(msg.k[0])
    fy = float(msg.k[4])
    cx = float(msg.k[2])
    cy = float(msg.k[5])
    if fx <= 0.0 or fy <= 0.0:
        return None
    return CameraIntrinsics(
        fx=fx,
        fy=fy,
        cx=cx,
        cy=cy,
        width=int(msg.width),
        height=int(msg.height),
        frame_id=str(msg.header.frame_id),
    )


class PersonFollowVisionNode(Node):
    def __init__(self) -> None:
        super().__init__("person_follow_vision_node")
        self.declare_parameter("robot_mode_state_topic", "/robot_mode_state")
        self.detections_topic = str(
            self.declare_parameter("detections_topic", "/detections_output").value
        )
        self.declare_parameter("color_image_topic", "/camera/color/image_raw")
        self.depth_image_topic = str(
            self.declare_parameter(
                "depth_image_topic", "/camera/aligned_depth_to_color/image_raw"
            ).value
        )
        self.camera_info_topic = str(
            self.declare_parameter("camera_info_topic", "/camera/color/camera_info").value
        )
        dynamic_parameter_descriptor = ParameterDescriptor(dynamic_typing=True)
        self.target_class_id = str(
            self.declare_parameter(
                "target_class_id",
                "0",
                dynamic_parameter_descriptor,
            ).value
        )
        self.target_label = str(self.declare_parameter("target_label", "person").value)
        self.network_image_width = float(
            self.declare_parameter("network_image_width", 640.0).value
        )
        self.network_image_height = float(
            self.declare_parameter("network_image_height", 640.0).value
        )
        self.source_image_width = float(
            self.declare_parameter("source_image_width", 640.0).value
        )
        self.source_image_height = float(
            self.declare_parameter("source_image_height", 360.0).value
        )
        self.encoder_keep_aspect_ratio = bool(
            self.declare_parameter("encoder_keep_aspect_ratio", True).value
        )
        self.encoder_enable_padding = bool(
            self.declare_parameter("encoder_enable_padding", True).value
        )
        self.depth_window_radius_px = int(
            self.declare_parameter("depth_window_radius_px", 4).value
        )
        self.min_depth_m = float(self.declare_parameter("min_depth_m", 0.20).value)
        self.max_depth_m = float(self.declare_parameter("max_depth_m", 8.0).value)
        sync_queue_size = int(self.declare_parameter("sync_queue_size", 10).value)
        sync_slop_s = float(self.declare_parameter("sync_slop_s", 0.20).value)
        self.target_stale_timeout_s = float(
            self.declare_parameter("target_stale_timeout_s", 0.80).value
        )

        self.bridge = cv_bridge.CvBridge()
        self.latest_intrinsics: CameraIntrinsics | None = None
        self.latest_target_mono_s: float | None = None
        self.currently_visible = False

        self.target_point_pub = self.create_publisher(PointStamped, "~/target_point", 10)
        self.target_visible_pub = self.create_publisher(Bool, "~/target_visible", 10)
        self.target_id_pub = self.create_publisher(Int32, "~/target_id", 10)
        self.status_pub = self.create_publisher(String, "~/status", 10)

        sensor_qos = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=max(1, sync_queue_size),
            reliability=ReliabilityPolicy.BEST_EFFORT,
        )
        self.create_subscription(CameraInfo, self.camera_info_topic, self._camera_info_cb, sensor_qos)
        self.detections_sub = message_filters.Subscriber(
            self,
            Detection2DArray,
            self.detections_topic,
            qos_profile=sensor_qos,
        )
        self.depth_sub = message_filters.Subscriber(
            self,
            Image,
            self.depth_image_topic,
            qos_profile=sensor_qos,
        )
        self.sync = message_filters.ApproximateTimeSynchronizer(
            [self.detections_sub, self.depth_sub],
            queue_size=max(1, sync_queue_size),
            slop=max(0.0, sync_slop_s),
        )
        self.sync.registerCallback(self._synced_detection_depth_cb)
        self.create_timer(0.25, self._stale_timer_cb)

        self._publish_invisible("waiting_for_detector")
        self.get_logger().info(
            "Person-follow perception adapter ready. "
            f"detections_topic={self.detections_topic} "
            f"depth_image_topic={self.depth_image_topic} "
            f"camera_info_topic={self.camera_info_topic} "
            f"target_class_id={self.target_class_id}"
        )

    def _camera_info_cb(self, msg: CameraInfo) -> None:
        intrinsics = _camera_intrinsics_from_msg(msg)
        if intrinsics is None:
            self._publish_invisible("invalid_camera_info")
            return
        self.latest_intrinsics = intrinsics

    def _synced_detection_depth_cb(
        self,
        detections_msg: Detection2DArray,
        depth_msg: Image,
    ) -> None:
        candidate = _select_best_candidate(
            detections_msg.detections,
            self.target_class_id,
            self.target_label,
        )
        if candidate is None:
            status = "no_detections" if not detections_msg.detections else "no_person_detection"
            self._publish_invisible(status)
            return

        intrinsics = self.latest_intrinsics
        if intrinsics is None:
            self._publish_invisible("missing_camera_info")
            return

        source_width = float(intrinsics.width or depth_msg.width or self.source_image_width)
        source_height = float(intrinsics.height or depth_msg.height or self.source_image_height)
        source_x, source_y = _network_to_source_pixel(
            candidate.center_x,
            candidate.center_y,
            self.network_image_width,
            self.network_image_height,
            source_width,
            source_height,
            self.encoder_keep_aspect_ratio,
            self.encoder_enable_padding,
        )

        try:
            depth_image = self.bridge.imgmsg_to_cv2(depth_msg, desired_encoding="passthrough")
        except Exception as exc:
            self.get_logger().warn(f"Failed to convert depth image: {exc}")
            self._publish_invisible("depth_conversion_failed")
            return

        depth_m = _sample_depth_m(
            depth_image,
            source_x,
            source_y,
            depth_msg.encoding,
            self.depth_window_radius_px,
            self.min_depth_m,
            self.max_depth_m,
        )
        if depth_m is None:
            self._publish_invisible("invalid_depth")
            return

        point_xyz = _project_pixel_to_3d(source_x, source_y, depth_m, intrinsics)
        if point_xyz is None:
            self._publish_invisible("invalid_intrinsics")
            return

        point_msg = PointStamped()
        point_msg.header.stamp = depth_msg.header.stamp
        point_msg.header.frame_id = intrinsics.frame_id or str(depth_msg.header.frame_id)
        point_msg.point.x = float(point_xyz[0])
        point_msg.point.y = float(point_xyz[1])
        point_msg.point.z = float(point_xyz[2])

        self.target_point_pub.publish(point_msg)
        self.target_visible_pub.publish(Bool(data=True))
        self.target_id_pub.publish(Int32(data=int(candidate.target_id)))
        self.status_pub.publish(
            String(
                data=(
                    f"tracking class_id={candidate.class_id} score={candidate.score:.3f} "
                    f"pixel=({source_x:.1f},{source_y:.1f}) depth_m={depth_m:.3f}"
                )
            )
        )
        self.currently_visible = True
        self.latest_target_mono_s = time.monotonic()

    def _stale_timer_cb(self) -> None:
        if not self.currently_visible or self.latest_target_mono_s is None:
            return
        if (time.monotonic() - self.latest_target_mono_s) > self.target_stale_timeout_s:
            self._publish_invisible("target_stale")

    def _publish_invisible(self, status: str) -> None:
        self.target_visible_pub.publish(Bool(data=False))
        self.target_id_pub.publish(Int32(data=-1))
        self.status_pub.publish(String(data=str(status)))
        self.currently_visible = False


def main() -> None:
    rclpy.init()
    node = PersonFollowVisionNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
