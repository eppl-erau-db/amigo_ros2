#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from ament_index_python.packages import PackageNotFoundError, get_package_share_directory
import cv2
from cv_bridge import CvBridge
from explore_lite_msgs.msg import ExploreStatus
from geometry_msgs.msg import PoseStamped
from nav2_msgs.srv import SaveMap
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import numpy as np
import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from rclpy.task import Future
from rclpy.time import Time
from sensor_msgs.msg import CameraInfo, Image
from std_msgs.msg import Bool, String
from std_srvs.srv import Trigger
from tf2_ros import Buffer, TransformException, TransformListener
from tf_transformations import (
    euler_from_quaternion,
    quaternion_from_euler,
    quaternion_from_matrix,
    quaternion_matrix,
)
import yaml
from zed_msgs.srv import SetPose
from visualization_msgs.msg import Marker, MarkerArray

from go2_interfaces.action import ExploreArea


EPS = 1.0e-6


class ArucoDetectorCompat:
    def __init__(
        self,
        *,
        aruco_module: Any,
        dictionary: Any,
        detector_parameters: Any,
        detector: Any = None,
    ) -> None:
        self._aruco_module = aruco_module
        self._dictionary = dictionary
        self._detector_parameters = detector_parameters
        self._detector = detector

    @classmethod
    def from_module(cls, aruco_module: Any, dictionary_id: int) -> ArucoDetectorCompat:
        dictionary = aruco_module.getPredefinedDictionary(dictionary_id)

        detector_parameters_factory = getattr(aruco_module, "DetectorParameters", None)
        if callable(detector_parameters_factory):
            detector_parameters = detector_parameters_factory()
        else:
            detector_parameters = aruco_module.DetectorParameters_create()

        detector_cls = getattr(aruco_module, "ArucoDetector", None)
        detector = None
        if detector_cls is not None:
            detector = detector_cls(dictionary, detector_parameters)

        return cls(
            aruco_module=aruco_module,
            dictionary=dictionary,
            detector_parameters=detector_parameters,
            detector=detector,
        )

    def detectMarkers(self, image):
        if self._detector is not None:
            return self._detector.detectMarkers(image)
        return self._aruco_module.detectMarkers(
            image,
            self._dictionary,
            parameters=self._detector_parameters,
        )


@dataclass(frozen=True)
class LandmarkRoleConfig:
    name: str
    aruco_id: int
    required: bool
    visit_on_first_detection: bool
    standoff_distance_m: float
    dwell_time_s: float
    action_hook: str
    trigger_service_name: str
    enable_pose_correction: bool
    configured_marker_position: tuple[float, float, float] | None = None
    configured_marker_quaternion: tuple[float, float, float, float] | None = None

    def has_configured_marker_pose(self) -> bool:
        return (
            self.configured_marker_position is not None and
            self.configured_marker_quaternion is not None
        )


@dataclass
class LandmarkEstimate:
    aruco_id: int
    role_name: str | None = None
    required: bool = False
    observations: int = 0
    first_seen_ns: int = 0
    last_seen_ns: int = 0
    marker_position_sum: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=float))
    marker_quaternion_sum: np.ndarray = field(default_factory=lambda: np.zeros(4, dtype=float))
    front_vector_sum: np.ndarray = field(default_factory=lambda: np.zeros(2, dtype=float))
    last_distance_m: float = 0.0
    action_performed: bool = False
    visit_attempts: int = 0
    pose_corrections_applied: int = 0
    last_pose_correction_mono_s: float = 0.0

    def update(
        self,
        *,
        marker_position: np.ndarray,
        marker_quaternion: np.ndarray,
        robot_xy: np.ndarray,
        stamp_ns: int,
        distance_m: float,
    ) -> None:
        if self.observations == 0:
            self.first_seen_ns = stamp_ns
        self.last_seen_ns = stamp_ns
        self.last_distance_m = float(distance_m)
        self.observations += 1
        self.marker_position_sum += marker_position

        quaternion = np.array(marker_quaternion, dtype=float)
        if np.linalg.norm(self.marker_quaternion_sum) > EPS:
            if float(np.dot(quaternion, self.marker_quaternion_sum)) < 0.0:
                quaternion *= -1.0
        self.marker_quaternion_sum += quaternion

        front_xy = np.array(robot_xy[:2] - marker_position[:2], dtype=float)
        norm = float(np.linalg.norm(front_xy))
        if norm > EPS:
            self.front_vector_sum += front_xy / norm

    def marker_position(self) -> np.ndarray:
        if self.observations <= 0:
            return np.zeros(3, dtype=float)
        return self.marker_position_sum / float(self.observations)

    def marker_quaternion(self) -> np.ndarray:
        if self.observations <= 0:
            return np.array([0.0, 0.0, 0.0, 1.0], dtype=float)
        quaternion = self.marker_quaternion_sum / float(self.observations)
        norm = float(np.linalg.norm(quaternion))
        if norm <= EPS:
            return np.array([0.0, 0.0, 0.0, 1.0], dtype=float)
        return quaternion / norm

    def marker_pose(self, *, frame_id: str, stamp) -> PoseStamped:
        pose = PoseStamped()
        pose.header.frame_id = frame_id
        pose.header.stamp = stamp
        position = self.marker_position()
        quaternion = self.marker_quaternion()
        pose.pose.position.x = float(position[0])
        pose.pose.position.y = float(position[1])
        pose.pose.position.z = float(position[2])
        pose.pose.orientation.x = float(quaternion[0])
        pose.pose.orientation.y = float(quaternion[1])
        pose.pose.orientation.z = float(quaternion[2])
        pose.pose.orientation.w = float(quaternion[3])
        return pose

    def front_direction_xy(self) -> np.ndarray:
        norm = float(np.linalg.norm(self.front_vector_sum))
        if norm > EPS:
            return self.front_vector_sum / norm

        rotation = quaternion_matrix(self.marker_quaternion())
        candidate = np.array([rotation[0, 2], rotation[1, 2]], dtype=float)
        candidate_norm = float(np.linalg.norm(candidate))
        if candidate_norm > EPS:
            return candidate / candidate_norm
        return np.array([1.0, 0.0], dtype=float)


def rpy_from_quaternion_xyzw(
    quaternion: np.ndarray | tuple[float, ...] | list[float],
) -> tuple[float, float, float]:
    quaternion_xyzw = np.asarray(quaternion, dtype=float).reshape(4)
    roll, pitch, yaw = euler_from_quaternion(quaternion_xyzw.tolist())
    return float(roll), float(pitch), float(yaw)


def yaw_from_quaternion_xyzw(quaternion: np.ndarray | tuple[float, ...] | list[float]) -> float:
    _, _, yaw = rpy_from_quaternion_xyzw(quaternion)
    return float(yaw)


def pose_stamped_from_matrix(matrix: np.ndarray, *, frame_id: str, stamp) -> PoseStamped:
    pose = PoseStamped()
    pose.header.frame_id = frame_id
    pose.header.stamp = stamp
    quaternion = quaternion_from_matrix(matrix)
    pose.pose.position.x = float(matrix[0, 3])
    pose.pose.position.y = float(matrix[1, 3])
    pose.pose.position.z = float(matrix[2, 3])
    pose.pose.orientation.x = float(quaternion[0])
    pose.pose.orientation.y = float(quaternion[1])
    pose.pose.orientation.z = float(quaternion[2])
    pose.pose.orientation.w = float(quaternion[3])
    return pose


def pose_stamped_from_position_quaternion(
    position: np.ndarray | tuple[float, ...],
    quaternion: np.ndarray | tuple[float, ...],
    *,
    frame_id: str,
    stamp,
) -> PoseStamped:
    pose = PoseStamped()
    pose.header.frame_id = frame_id
    pose.header.stamp = stamp
    xyz = np.asarray(position, dtype=float).reshape(3)
    quat = np.asarray(quaternion, dtype=float).reshape(4)
    pose.pose.position.x = float(xyz[0])
    pose.pose.position.y = float(xyz[1])
    pose.pose.position.z = float(xyz[2])
    pose.pose.orientation.x = float(quat[0])
    pose.pose.orientation.y = float(quat[1])
    pose.pose.orientation.z = float(quat[2])
    pose.pose.orientation.w = float(quat[3])
    return pose


def pose_stamped_to_dict(pose: PoseStamped) -> dict[str, Any]:
    return {
        "frame_id": pose.header.frame_id,
        "position": {
            "x": float(pose.pose.position.x),
            "y": float(pose.pose.position.y),
            "z": float(pose.pose.position.z),
        },
        "orientation": {
            "x": float(pose.pose.orientation.x),
            "y": float(pose.pose.orientation.y),
            "z": float(pose.pose.orientation.z),
            "w": float(pose.pose.orientation.w),
        },
    }


def _coerce_float_vector(
    raw_value: Any,
    *,
    expected_len: int,
    field_name: str,
) -> tuple[float, ...]:
    if not isinstance(raw_value, (list, tuple)) or len(raw_value) != expected_len:
        raise ValueError(
            f'"{field_name}" must be a list with {expected_len} numeric value(s).'
        )
    try:
        return tuple(float(value) for value in raw_value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f'"{field_name}" must contain only numeric values.'
        ) from exc


def normalize_quaternion_xyzw(raw_quaternion: Any) -> tuple[float, float, float, float]:
    quaternion = np.asarray(raw_quaternion, dtype=float).reshape(4)
    norm = float(np.linalg.norm(quaternion))
    if norm <= EPS:
        raise ValueError('"quaternion" must have non-zero magnitude.')
    quaternion /= norm
    return tuple(float(value) for value in quaternion.tolist())


def parse_fixed_marker_pose_config(
    raw_pose_config: Any,
) -> tuple[tuple[float, float, float], tuple[float, float, float, float]]:
    if not isinstance(raw_pose_config, dict):
        raise ValueError('"fixed_map_pose" must be a mapping.')

    position = _coerce_float_vector(
        raw_pose_config.get("position"),
        expected_len=3,
        field_name="fixed_map_pose.position",
    )
    has_orientation = "orientation" in raw_pose_config
    has_quaternion = "quaternion" in raw_pose_config
    if has_orientation and has_quaternion:
        raise ValueError(
            'Specify only one of "fixed_map_pose.orientation" or '
            '"fixed_map_pose.quaternion".'
        )

    if has_orientation:
        roll, pitch, yaw = _coerce_float_vector(
            raw_pose_config.get("orientation"),
            expected_len=3,
            field_name="fixed_map_pose.orientation",
        )
        quaternion = normalize_quaternion_xyzw(quaternion_from_euler(roll, pitch, yaw))
    elif has_quaternion:
        quaternion = normalize_quaternion_xyzw(
            _coerce_float_vector(
                raw_pose_config.get("quaternion"),
                expected_len=4,
                field_name="fixed_map_pose.quaternion",
            )
        )
    else:
        quaternion = (0.0, 0.0, 0.0, 1.0)

    return position, quaternion


def matrix_from_pose(pose: PoseStamped) -> np.ndarray:
    quaternion = np.array(
        [
            pose.pose.orientation.x,
            pose.pose.orientation.y,
            pose.pose.orientation.z,
            pose.pose.orientation.w,
        ],
        dtype=float,
    )
    matrix = quaternion_matrix(quaternion)
    matrix[0, 3] = float(pose.pose.position.x)
    matrix[1, 3] = float(pose.pose.position.y)
    matrix[2, 3] = float(pose.pose.position.z)
    return matrix


def matrix_from_transform(transform) -> np.ndarray:
    quaternion = np.array(
        [
            transform.rotation.x,
            transform.rotation.y,
            transform.rotation.z,
            transform.rotation.w,
        ],
        dtype=float,
    )
    matrix = quaternion_matrix(quaternion)
    matrix[0, 3] = float(transform.translation.x)
    matrix[1, 3] = float(transform.translation.y)
    matrix[2, 3] = float(transform.translation.z)
    return matrix


def matrix_from_rvec_tvec(rvec: np.ndarray, tvec: np.ndarray) -> np.ndarray:
    rotation_matrix, _ = cv2.Rodrigues(np.asarray(rvec, dtype=float).reshape(3, 1))
    matrix = np.eye(4, dtype=float)
    matrix[:3, :3] = rotation_matrix
    matrix[:3, 3] = np.asarray(tvec, dtype=float).reshape(3)
    return matrix


def adjust_pose_correction_target(
    corrected_map_to_zed_base: np.ndarray,
    current_map_to_zed_base: np.ndarray,
    *,
    preserve_z: bool,
    preserve_roll_pitch: bool,
) -> tuple[np.ndarray, tuple[float, float, float], tuple[float, float, float, float]]:
    adjusted_position = np.asarray(corrected_map_to_zed_base[:3, 3], dtype=float).copy()
    if preserve_z:
        adjusted_position[2] = float(current_map_to_zed_base[2, 3])

    corrected_roll, corrected_pitch, corrected_yaw = rpy_from_quaternion_xyzw(
        quaternion_from_matrix(corrected_map_to_zed_base)
    )
    if preserve_roll_pitch:
        current_roll, current_pitch, _ = rpy_from_quaternion_xyzw(
            quaternion_from_matrix(current_map_to_zed_base)
        )
        corrected_roll = current_roll
        corrected_pitch = current_pitch

    adjusted_rpy = (
        float(corrected_roll),
        float(corrected_pitch),
        float(corrected_yaw),
    )
    adjusted_quaternion = normalize_quaternion_xyzw(
        quaternion_from_euler(*adjusted_rpy)
    )
    adjusted_matrix = quaternion_matrix(adjusted_quaternion)
    adjusted_matrix[0, 3] = float(adjusted_position[0])
    adjusted_matrix[1, 3] = float(adjusted_position[1])
    adjusted_matrix[2, 3] = float(adjusted_position[2])
    return adjusted_matrix, adjusted_rpy, adjusted_quaternion


class ExploreAreaMissionServer(Node):
    def __init__(self) -> None:
        super().__init__("explore_area_action_server")

        self.action_name = str(
            self.declare_parameter("action_name", "explore_area").value
        )
        self.map_frame = str(self.declare_parameter("map_frame", "map").value)
        self.base_frame = str(self.declare_parameter("base_frame", "base_link").value)
        self.zed_base_frame = str(
            self.declare_parameter("zed_base_frame", "zed_camera_link").value
        )
        self.image_topic = str(
            self.declare_parameter("image_topic", "/zed/zed_node/rgb/image_rect_color").value
        )
        self.camera_info_topic = str(
            self.declare_parameter("camera_info_topic", "/zed/zed_node/rgb/camera_info").value
        )
        self.explore_status_topic = str(
            self.declare_parameter("explore_status_topic", "explore/status").value
        )
        self.explore_resume_topic = str(
            self.declare_parameter("explore_resume_topic", "explore/resume").value
        )
        self.map_topic = str(self.declare_parameter("map_topic", "/map").value)
        self.map_save_service_name = str(
            self.declare_parameter("map_save_service_name", "/map_saver/save_map").value
        )
        self.pose_correction_service_name = str(
            self.declare_parameter("pose_correction_service_name", "/zed/zed_node/set_pose").value
        )
        self.landmark_config_path = str(
            self.declare_parameter("landmark_config_path", "").value
        ).strip()
        self.aruco_dictionary = str(
            self.declare_parameter("aruco_dictionary", "DICT_6X6_1000").value
        ).strip()
        self.marker_size_m = max(
            0.01, float(self.declare_parameter("marker_size_m", 0.16).value)
        )
        self.max_detection_distance_m = max(
            0.1, float(self.declare_parameter("max_detection_distance_m", 3.0).value)
        )
        self.detection_min_period_s = max(
            0.05, float(self.declare_parameter("detection_min_period_s", 0.5).value)
        )
        self.feedback_period_s = max(
            0.1, float(self.declare_parameter("feedback_period_s", 0.5).value)
        )
        self.mission_timeout_s = max(
            30.0, float(self.declare_parameter("mission_timeout_s", 900.0).value)
        )
        self.landmark_visit_settle_s = max(
            0.0, float(self.declare_parameter("landmark_visit_settle_s", 1.0).value)
        )
        self.visit_min_observations = max(
            1, int(self.declare_parameter("visit_min_observations", 2).value)
        )
        self.park_at_home_on_complete = bool(
            self.declare_parameter("park_at_home_on_complete", False).value
        )
        self.artifact_root = Path(
            str(self.declare_parameter("artifact_root", "artifacts/explore_area").value)
        ).expanduser()
        self.map_save_image_format = str(
            self.declare_parameter("map_save_image_format", "pgm").value
        ).strip()
        self.map_save_mode = str(
            self.declare_parameter("map_save_mode", "trinary").value
        ).strip()
        self.map_save_free_thresh = float(
            self.declare_parameter("map_save_free_thresh", 0.25).value
        )
        self.map_save_occupied_thresh = float(
            self.declare_parameter("map_save_occupied_thresh", 0.65).value
        )
        self.pose_correction_enabled = bool(
            self.declare_parameter("pose_correction_enabled", True).value
        )
        self.pose_correction_for_unconfigured_markers = bool(
            self.declare_parameter(
                "pose_correction_for_unconfigured_markers", True
            ).value
        )
        self.pose_correction_cooldown_s = max(
            0.0, float(self.declare_parameter("pose_correction_cooldown_s", 15.0).value)
        )
        self.pose_correction_min_translation_m = max(
            0.0,
            float(self.declare_parameter("pose_correction_min_translation_m", 0.15).value),
        )
        self.pose_correction_min_yaw_rad = math.radians(
            max(0.0, float(self.declare_parameter("pose_correction_min_yaw_deg", 7.5).value))
        )
        self.pose_correction_min_observations = max(
            1, int(self.declare_parameter("pose_correction_min_observations", 2).value)
        )
        self.pose_correction_preserve_z = bool(
            self.declare_parameter("pose_correction_preserve_z", True).value
        )
        self.pose_correction_preserve_roll_pitch = bool(
            self.declare_parameter("pose_correction_preserve_roll_pitch", True).value
        )
        self.clear_costmaps_before_landmark_visit = bool(
            self.declare_parameter("clear_costmaps_before_landmark_visit", True).value
        )
        self.save_partial_on_cancel = bool(
            self.declare_parameter("save_partial_on_cancel", True).value
        )
        self.debug_enable = bool(self.declare_parameter("debug_enable", False).value)
        self.debug_topic = str(
            self.declare_parameter("debug_topic", "/explore_area/debug").value
        )
        self.publish_debug_topic = bool(
            self.declare_parameter("publish_debug_topic", True).value
        )
        self.landmark_marker_topic = str(
            self.declare_parameter(
                "landmark_marker_topic", "/explore_area/landmark_markers"
            ).value
        )
        self.publish_landmark_markers = bool(
            self.declare_parameter("publish_landmark_markers", True).value
        )
        self.tf_warning_throttle_s = max(
            0.5, float(self.declare_parameter("tf_warning_throttle_s", 5.0).value)
        )
        self.camera_warning_throttle_s = max(
            0.5, float(self.declare_parameter("camera_warning_throttle_s", 5.0).value)
        )

        self._bridge = CvBridge()
        self._tf_buffer = Buffer(cache_time=Duration(seconds=10.0))
        self._tf_listener = TransformListener(self._tf_buffer, self)
        self.navigator = BasicNavigator()
        self._resume_pub = self.create_publisher(Bool, self.explore_resume_topic, 10)
        self._debug_pub = self.create_publisher(String, self.debug_topic, 10)
        self._landmark_marker_pub = None
        if self.publish_landmark_markers:
            marker_qos = QoSProfile(depth=1)
            marker_qos.durability = DurabilityPolicy.TRANSIENT_LOCAL
            marker_qos.reliability = ReliabilityPolicy.RELIABLE
            self._landmark_marker_pub = self.create_publisher(
                MarkerArray,
                self.landmark_marker_topic,
                marker_qos,
            )

        self.map_save_client = self.create_client(SaveMap, self.map_save_service_name)
        self.pose_correction_client = self.create_client(
            SetPose, self.pose_correction_service_name
        )
        self._trigger_clients: dict[str, Any] = {}

        self._goal_active = False
        self._latest_camera_info: CameraInfo | None = None
        self._camera_matrix: np.ndarray | None = None
        self._dist_coeffs: np.ndarray | None = None
        self._last_detection_mono_s = 0.0
        self._landmark_estimates: dict[int, LandmarkEstimate] = {}
        self._pending_landmark_roles: list[str] = []
        self._active_landmark_role = ""
        self._latest_explore_status = ExploreStatus.EXPLORATION_PAUSED
        self._pose_correction_in_flight = False
        self._camera_info_logged = False
        self._warning_log_times: dict[str, float] = {}

        self._role_configs, self._save_unconfigured_markers = self._load_landmark_config()
        self._aruco_id_to_role = {
            config.aruco_id: config for config in self._role_configs.values()
        }
        self._publish_landmark_markers()

        self._aruco_detector = self._build_aruco_detector(self.aruco_dictionary)

        self.create_subscription(ExploreStatus, self.explore_status_topic, self._explore_status_cb, 10)
        self.create_subscription(CameraInfo, self.camera_info_topic, self._camera_info_cb, 10)
        self.create_subscription(Image, self.image_topic, self._image_cb, 10)

        self._action_server = ActionServer(
            self,
            ExploreArea,
            self.action_name,
            execute_callback=self.execute_cb,
            goal_callback=self.goal_cb,
            cancel_callback=self.cancel_cb,
        )

        self.get_logger().info(
            "Explore-area action server ready: "
            f'action="{self.action_name}", image_topic="{self.image_topic}", '
            f'camera_info_topic="{self.camera_info_topic}", '
            f'landmarks={sorted(self._role_configs)}, '
            f'debug_topic="{self.debug_topic}", '
            f'landmark_marker_topic="{self.landmark_marker_topic}"'
        )
        if not self._role_configs:
            self.get_logger().warn(
                "No configured landmark roles were loaded. The mission will only persist unconfigured markers."
            )

    @staticmethod
    def _json_debug_default(value: Any):
        if isinstance(value, Path):
            return str(value)
        if isinstance(value, np.ndarray):
            return value.tolist()
        if isinstance(value, (np.integer, np.floating)):
            return value.item()
        return str(value)

    def _emit_debug_event(self, event: str, **payload: Any) -> None:
        if not self.publish_debug_topic:
            return
        message = String()
        event_payload = {
            "source": "explore_area_action_server",
            "event": str(event),
            "goal_active": bool(self._goal_active),
            "active_landmark_role": str(self._active_landmark_role),
            "timestamp_ns": int(self.get_clock().now().nanoseconds),
        }
        event_payload.update(payload)
        message.data = json.dumps(
            event_payload,
            separators=(",", ":"),
            sort_keys=True,
            default=self._json_debug_default,
        )
        self._debug_pub.publish(message)

    @staticmethod
    def _assign_pose_fields(target_pose, source_pose) -> None:
        target_pose.position.x = float(source_pose.position.x)
        target_pose.position.y = float(source_pose.position.y)
        target_pose.position.z = float(source_pose.position.z)
        target_pose.orientation.x = float(source_pose.orientation.x)
        target_pose.orientation.y = float(source_pose.orientation.y)
        target_pose.orientation.z = float(source_pose.orientation.z)
        target_pose.orientation.w = float(source_pose.orientation.w)

    @staticmethod
    def _assign_marker_color(marker: Marker, rgba: tuple[float, float, float, float]) -> None:
        marker.color.r = float(rgba[0])
        marker.color.g = float(rgba[1])
        marker.color.b = float(rgba[2])
        marker.color.a = float(rgba[3])

    def _append_landmark_pose_markers(
        self,
        marker_array: MarkerArray,
        *,
        next_id: int,
        pose: PoseStamped,
        namespace: str,
        label: str,
        body_type: int,
        body_scale_xyz: tuple[float, float, float],
        body_rgba: tuple[float, float, float, float],
    ) -> int:
        body_marker = Marker()
        body_marker.header.frame_id = self.map_frame
        body_marker.header.stamp = pose.header.stamp
        body_marker.ns = f"{namespace}_body"
        body_marker.id = next_id
        body_marker.type = body_type
        body_marker.action = Marker.ADD
        self._assign_pose_fields(body_marker.pose, pose.pose)
        body_marker.scale.x = float(body_scale_xyz[0])
        body_marker.scale.y = float(body_scale_xyz[1])
        body_marker.scale.z = float(body_scale_xyz[2])
        self._assign_marker_color(body_marker, body_rgba)
        marker_array.markers.append(body_marker)
        next_id += 1

        heading_marker = Marker()
        heading_marker.header.frame_id = self.map_frame
        heading_marker.header.stamp = pose.header.stamp
        heading_marker.ns = f"{namespace}_heading"
        heading_marker.id = next_id
        heading_marker.type = Marker.ARROW
        heading_marker.action = Marker.ADD
        self._assign_pose_fields(heading_marker.pose, pose.pose)
        heading_marker.scale.x = 0.35
        heading_marker.scale.y = 0.06
        heading_marker.scale.z = 0.10
        self._assign_marker_color(
            heading_marker,
            (body_rgba[0], body_rgba[1], body_rgba[2], min(1.0, body_rgba[3] + 0.1)),
        )
        marker_array.markers.append(heading_marker)
        next_id += 1

        label_marker = Marker()
        label_marker.header.frame_id = self.map_frame
        label_marker.header.stamp = pose.header.stamp
        label_marker.ns = f"{namespace}_label"
        label_marker.id = next_id
        label_marker.type = Marker.TEXT_VIEW_FACING
        label_marker.action = Marker.ADD
        label_marker.pose.position.x = float(pose.pose.position.x)
        label_marker.pose.position.y = float(pose.pose.position.y)
        label_marker.pose.position.z = float(pose.pose.position.z + 0.30)
        label_marker.pose.orientation.w = 1.0
        label_marker.scale.z = 0.22
        self._assign_marker_color(label_marker, (1.0, 1.0, 1.0, 1.0))
        label_marker.text = str(label)
        marker_array.markers.append(label_marker)
        next_id += 1

        return next_id

    def _publish_landmark_markers(self) -> None:
        if self._landmark_marker_pub is None:
            return

        marker_array = MarkerArray()
        delete_all = Marker()
        delete_all.action = Marker.DELETEALL
        marker_array.markers.append(delete_all)

        stamp = self.get_clock().now().to_msg()
        next_id = 0

        for role_name, role_config in sorted(self._role_configs.items()):
            configured_pose = self._configured_marker_pose(role_config, stamp=stamp)
            if configured_pose is None:
                continue
            next_id = self._append_landmark_pose_markers(
                marker_array,
                next_id=next_id,
                pose=configured_pose,
                namespace="configured_landmarks",
                label=f"{role_name} [{role_config.aruco_id}] configured",
                body_type=Marker.CUBE,
                body_scale_xyz=(0.18, 0.18, 0.18),
                body_rgba=(1.0, 0.65, 0.10, 0.75),
            )

        for marker_id, estimate in sorted(self._landmark_estimates.items()):
            observed_pose = estimate.marker_pose(
                frame_id=self.map_frame,
                stamp=stamp,
            )
            if estimate.action_performed:
                body_rgba = (0.20, 0.85, 0.35, 1.0)
            elif estimate.required:
                body_rgba = (0.15, 0.75, 1.0, 1.0)
            else:
                body_rgba = (0.85, 0.85, 0.20, 1.0)
            label = (
                f'{estimate.role_name or f"aruco_{marker_id}"} [{marker_id}] '
                f"obs={estimate.observations}"
            )
            next_id = self._append_landmark_pose_markers(
                marker_array,
                next_id=next_id,
                pose=observed_pose,
                namespace="observed_landmarks",
                label=label,
                body_type=Marker.SPHERE,
                body_scale_xyz=(0.20, 0.20, 0.20),
                body_rgba=body_rgba,
            )

        self._landmark_marker_pub.publish(marker_array)

    def _debug_log(self, message: str) -> None:
        if self.debug_enable:
            self.get_logger().info(message)

    def _warn_throttled(self, key: str, message: str, *, throttle_s: float) -> bool:
        now_mono_s = time.monotonic()
        last_mono_s = self._warning_log_times.get(key, -float("inf"))
        if (now_mono_s - last_mono_s) < throttle_s:
            return False
        self._warning_log_times[key] = now_mono_s
        self.get_logger().warn(message)
        return True

    def _default_landmark_config_path(self) -> Path:
        candidates: list[Path] = []
        try:
            candidates.append(
                Path(get_package_share_directory("go2_control")) /
                "config" /
                "aruco_explore_landmarks.yaml"
            )
        except PackageNotFoundError:
            pass
        candidates.append(Path(__file__).resolve().parents[1] / "config" / "aruco_explore_landmarks.yaml")
        for candidate in candidates:
            if candidate.is_file():
                return candidate
        return candidates[-1]

    def _load_landmark_config(self) -> tuple[dict[str, LandmarkRoleConfig], bool]:
        raw_path = self.landmark_config_path or str(self._default_landmark_config_path())
        config_path = Path(raw_path).expanduser()
        role_configs: dict[str, LandmarkRoleConfig] = {}
        save_unconfigured_markers = True
        loaded_from_defaults = False
        fixed_pose_roles: list[str] = []

        if not config_path.is_file():
            loaded_from_defaults = True
            self.get_logger().warn(
                f'Landmark config "{config_path}" was not found. Falling back to built-in defaults.'
            )
            default_data = {
                "landmarks": {
                    "swag_station": {
                        "aruco_id": 19,
                        "required": True,
                        "visit_on_first_detection": True,
                        "standoff_distance_m": 1.0,
                        "dwell_time_s": 5.0,
                        "action_hook": "swag_station_dwell",
                    },
                    "home_dock": {
                        "aruco_id": 43,
                        "required": True,
                        "visit_on_first_detection": False,
                        "standoff_distance_m": 1.0,
                        "action_hook": "home_dock_service",
                        "trigger_service_name": "/doghouse/park",
                    },
                },
                "save_unconfigured_markers": True,
            }
            config_data = default_data
        else:
            with config_path.open("r", encoding="utf-8") as stream:
                config_data = yaml.safe_load(stream) or {}

        save_unconfigured_markers = bool(config_data.get("save_unconfigured_markers", True))
        raw_landmarks = config_data.get("landmarks", {})
        if not isinstance(raw_landmarks, dict):
            raw_landmarks = {}

        seen_ids: set[int] = set()
        for role_name, raw_cfg in raw_landmarks.items():
            if not isinstance(raw_cfg, dict):
                continue
            aruco_id = int(raw_cfg.get("aruco_id", -1))
            if aruco_id < 0:
                continue
            if aruco_id in seen_ids:
                self.get_logger().warn(
                    f"Duplicate ArUco id {aruco_id} in landmark config. Keeping the first definition."
                )
                continue
            seen_ids.add(aruco_id)
            configured_marker_position = None
            configured_marker_quaternion = None
            if "fixed_map_pose" in raw_cfg:
                try:
                    configured_marker_position, configured_marker_quaternion = (
                        parse_fixed_marker_pose_config(raw_cfg.get("fixed_map_pose"))
                    )
                except ValueError as exc:
                    self.get_logger().warn(
                        f'Ignoring invalid fixed map pose for role "{role_name}": {exc}'
                    )
            role_configs[str(role_name)] = LandmarkRoleConfig(
                name=str(role_name),
                aruco_id=aruco_id,
                required=bool(raw_cfg.get("required", False)),
                visit_on_first_detection=bool(raw_cfg.get("visit_on_first_detection", False)),
                standoff_distance_m=max(0.1, float(raw_cfg.get("standoff_distance_m", 1.0))),
                dwell_time_s=max(0.0, float(raw_cfg.get("dwell_time_s", 0.0))),
                action_hook=str(raw_cfg.get("action_hook", "none")).strip() or "none",
                trigger_service_name=str(raw_cfg.get("trigger_service_name", "")).strip(),
                enable_pose_correction=bool(raw_cfg.get("enable_pose_correction", True)),
                configured_marker_position=configured_marker_position,
                configured_marker_quaternion=configured_marker_quaternion,
            )
            if configured_marker_position is not None:
                fixed_pose_roles.append(str(role_name))
                self.get_logger().info(
                    f'Role "{role_name}" loaded with a configured fixed map pose for marker {aruco_id}.'
                )

        config_source = "built_in_defaults" if loaded_from_defaults else str(config_path)
        self.get_logger().info(
            "Loaded explore-area landmark config: "
            f'source="{config_source}", roles={sorted(role_configs)}, '
            f"save_unconfigured_markers={save_unconfigured_markers}, "
            f"fixed_pose_roles={sorted(fixed_pose_roles)}"
        )
        self._emit_debug_event(
            "landmark_config_loaded",
            source=config_source,
            roles=sorted(role_configs),
            save_unconfigured_markers=bool(save_unconfigured_markers),
            loaded_from_defaults=bool(loaded_from_defaults),
            fixed_pose_roles=sorted(fixed_pose_roles),
        )
        return role_configs, save_unconfigured_markers

    def _build_aruco_detector(self, dictionary_name: str):
        dictionary_id = getattr(cv2.aruco, dictionary_name, None)
        if dictionary_id is None:
            self.get_logger().warn(
                f'Unknown ArUco dictionary "{dictionary_name}". Falling back to DICT_6X6_1000.'
            )
            dictionary_id = cv2.aruco.DICT_6X6_1000
        return ArucoDetectorCompat.from_module(cv2.aruco, dictionary_id)

    def goal_cb(self, goal_request: ExploreArea.Goal):
        del goal_request
        if self._goal_active:
            self.get_logger().warn(
                "Rejecting ExploreArea goal because another goal is already active."
            )
            self._emit_debug_event("goal_rejected", reason="goal_already_active")
            return GoalResponse.REJECT
        self.get_logger().info("ExploreArea goal received.")
        self._emit_debug_event("goal_received")
        return GoalResponse.ACCEPT

    def cancel_cb(self, goal_handle):
        del goal_handle
        self.get_logger().info("ExploreArea cancel requested.")
        self._emit_debug_event("cancel_requested")
        return CancelResponse.ACCEPT

    def _explore_status_cb(self, msg: ExploreStatus) -> None:
        new_status = str(msg.status or "").strip() or ExploreStatus.EXPLORATION_PAUSED
        if new_status != self._latest_explore_status:
            self._debug_log(
                f'Explore status changed from "{self._latest_explore_status}" to "{new_status}".'
            )
            self._emit_debug_event(
                "explore_status_changed",
                previous_status=str(self._latest_explore_status),
                status=str(new_status),
            )
        self._latest_explore_status = new_status

    def _camera_info_cb(self, msg: CameraInfo) -> None:
        self._latest_camera_info = msg
        self._camera_matrix = np.array(msg.k, dtype=float).reshape(3, 3)
        self._dist_coeffs = np.array(msg.d, dtype=float)
        if not self._camera_info_logged:
            self._camera_info_logged = True
            self.get_logger().info(
                f'Received camera intrinsics from "{self.camera_info_topic}" '
                f'(frame="{msg.header.frame_id}", size={msg.width}x{msg.height}).'
            )
            self._emit_debug_event(
                "camera_info_received",
                topic=self.camera_info_topic,
                frame_id=str(msg.header.frame_id),
                width=int(msg.width),
                height=int(msg.height),
            )

    def _image_cb(self, msg: Image) -> None:
        if not self._goal_active:
            return
        if self._camera_matrix is None or self._dist_coeffs is None:
            if self._warn_throttled(
                "camera_info_missing",
                f'Waiting for camera info on "{self.camera_info_topic}" before running ArUco detection.',
                throttle_s=self.camera_warning_throttle_s,
            ):
                self._emit_debug_event(
                    "camera_info_missing",
                    topic=self.camera_info_topic,
                )
            return

        now_mono_s = time.monotonic()
        if (now_mono_s - self._last_detection_mono_s) < self.detection_min_period_s:
            return
        self._last_detection_mono_s = now_mono_s

        try:
            bgr = self._bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        except Exception as exc:
            self.get_logger().warn(f"Failed to decode camera image for ArUco detection: {exc}")
            self._emit_debug_event("image_decode_failed", error=str(exc))
            return

        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = self._aruco_detector.detectMarkers(gray)
        if ids is None or len(ids) == 0:
            return

        try:
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
                corners,
                self.marker_size_m,
                self._camera_matrix,
                self._dist_coeffs,
            )
        except Exception as exc:
            self.get_logger().warn(f"Failed to estimate ArUco pose(s): {exc}")
            self._emit_debug_event("marker_pose_estimation_failed", error=str(exc))
            return

        image_frame = str(msg.header.frame_id).strip()
        if not image_frame:
            if self._warn_throttled(
                "image_frame_missing",
                "Received an image without a frame_id; skipping ArUco detection.",
                throttle_s=self.camera_warning_throttle_s,
            ):
                self._emit_debug_event("image_frame_missing")
            return

        map_to_camera = self._lookup_transform_matrix(self.map_frame, image_frame)
        base_to_map = self._lookup_transform_matrix(self.map_frame, self.base_frame)
        camera_to_zed_base = self._lookup_transform_matrix(image_frame, self.zed_base_frame)
        if map_to_camera is None or base_to_map is None or camera_to_zed_base is None:
            return

        robot_xy = np.array([base_to_map[0, 3], base_to_map[1, 3]], dtype=float)
        markers_updated = False

        for raw_id, rvec, tvec in zip(ids.flatten().tolist(), rvecs, tvecs):
            marker_id = int(raw_id)
            distance_m = float(np.linalg.norm(np.asarray(tvec, dtype=float).reshape(3)))
            if distance_m > self.max_detection_distance_m:
                continue

            role_config = self._aruco_id_to_role.get(marker_id)
            if role_config is None and not self._save_unconfigured_markers:
                continue

            camera_to_marker = matrix_from_rvec_tvec(rvec, tvec)
            map_to_marker = map_to_camera @ camera_to_marker
            marker_pose = pose_stamped_from_matrix(
                map_to_marker,
                frame_id=self.map_frame,
                stamp=self.get_clock().now().to_msg(),
            )
            marker_quaternion = np.array(
                [
                    marker_pose.pose.orientation.x,
                    marker_pose.pose.orientation.y,
                    marker_pose.pose.orientation.z,
                    marker_pose.pose.orientation.w,
                ],
                dtype=float,
            )
            marker_position = np.array(
                [
                    marker_pose.pose.position.x,
                    marker_pose.pose.position.y,
                    marker_pose.pose.position.z,
                ],
                dtype=float,
            )

            estimate = self._landmark_estimates.get(marker_id)
            is_new_landmark = estimate is None
            if estimate is None:
                estimate = LandmarkEstimate(
                    aruco_id=marker_id,
                    role_name=role_config.name if role_config is not None else None,
                    required=bool(role_config is not None and role_config.required),
                )
                self._landmark_estimates[marker_id] = estimate
                markers_updated = True

            estimate.update(
                marker_position=marker_position,
                marker_quaternion=marker_quaternion,
                robot_xy=robot_xy,
                stamp_ns=self.get_clock().now().nanoseconds,
                distance_m=distance_m,
            )
            markers_updated = True

            if is_new_landmark:
                role_label = estimate.role_name or "relocalization_marker"
                self.get_logger().info(
                    f'Discovered ArUco marker {marker_id} as "{role_label}".'
                )
                self._emit_debug_event(
                    "landmark_discovered",
                    marker_id=int(marker_id),
                    role_name=str(estimate.role_name or ""),
                    distance_m=float(distance_m),
                    required=bool(estimate.required),
                )

            if self.debug_enable and estimate.observations in {
                1,
                self.visit_min_observations,
                self.pose_correction_min_observations,
            }:
                self._debug_log(
                    f'Marker {marker_id} observation {estimate.observations}: '
                    f'distance={distance_m:.2f} m role="{estimate.role_name or "unconfigured"}".'
                )

            if (
                role_config is not None and
                role_config.visit_on_first_detection and
                estimate.visit_attempts == 0 and
                estimate.observations >= self.visit_min_observations and
                role_config.name not in self._pending_landmark_roles
            ):
                self._pending_landmark_roles.append(role_config.name)
                self.get_logger().info(
                    f'Queued landmark role "{role_config.name}" for a visit after detection.'
                )
                self._emit_debug_event(
                    "landmark_visit_queued",
                    marker_id=int(marker_id),
                    role_name=role_config.name,
                    observations=int(estimate.observations),
                )

            self._maybe_correct_pose_from_detection(
                estimate=estimate,
                role_config=role_config,
                image_frame=image_frame,
                camera_to_marker=camera_to_marker,
                camera_to_zed_base=camera_to_zed_base,
            )

        if markers_updated:
            self._publish_landmark_markers()

    def _lookup_transform_matrix(
        self,
        target_frame: str,
        source_frame: str,
    ) -> np.ndarray | None:
        try:
            tf_msg = self._tf_buffer.lookup_transform(
                target_frame,
                source_frame,
                Time(),
            )
        except TransformException as exc:
            if self._warn_throttled(
                f"tf_lookup:{target_frame}:{source_frame}",
                f'Unable to look up TF "{target_frame}" <- "{source_frame}": {exc}',
                throttle_s=self.tf_warning_throttle_s,
            ):
                self._emit_debug_event(
                    "tf_lookup_failed",
                    target_frame=target_frame,
                    source_frame=source_frame,
                    error=str(exc),
                )
            return None
        return matrix_from_transform(tf_msg.transform)

    def _current_pose(self) -> PoseStamped:
        current_matrix = self._lookup_transform_matrix(self.map_frame, self.base_frame)
        if current_matrix is not None:
            return pose_stamped_from_matrix(
                current_matrix,
                frame_id=self.map_frame,
                stamp=self.get_clock().now().to_msg(),
            )
        pose = PoseStamped()
        pose.header.frame_id = self.map_frame
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.orientation.w = 1.0
        return pose

    def _required_roles(self) -> set[str]:
        return {name for name, config in self._role_configs.items() if config.required}

    def _required_landmarks_found(self) -> int:
        found_roles = {
            estimate.role_name
            for estimate in self._landmark_estimates.values()
            if estimate.role_name is not None
        }
        return len(self._required_roles().intersection(found_roles))

    def _role_estimate(self, role_name: str) -> LandmarkEstimate | None:
        for estimate in self._landmark_estimates.values():
            if estimate.role_name == role_name:
                return estimate
        return None

    def _configured_marker_pose(
        self,
        role_config: LandmarkRoleConfig | None,
        *,
        stamp,
    ) -> PoseStamped | None:
        if role_config is None or not role_config.has_configured_marker_pose():
            return None
        return pose_stamped_from_position_quaternion(
            role_config.configured_marker_position,
            role_config.configured_marker_quaternion,
            frame_id=self.map_frame,
            stamp=stamp,
        )

    def _reference_marker_pose(
        self,
        estimate: LandmarkEstimate,
        role_config: LandmarkRoleConfig | None,
        *,
        stamp,
    ) -> tuple[PoseStamped, str]:
        configured_pose = self._configured_marker_pose(role_config, stamp=stamp)
        if configured_pose is not None:
            return configured_pose, "configured"
        return estimate.marker_pose(frame_id=self.map_frame, stamp=stamp), "observed"

    def _standoff_pose(
        self,
        estimate: LandmarkEstimate,
        *,
        distance_m: float,
        role_config: LandmarkRoleConfig | None = None,
    ) -> PoseStamped:
        stamp = self.get_clock().now().to_msg()
        marker_pose, _ = self._reference_marker_pose(
            estimate,
            role_config,
            stamp=stamp,
        )
        front_direction = estimate.front_direction_xy()
        standoff_pose = PoseStamped()
        standoff_pose.header.frame_id = self.map_frame
        standoff_pose.header.stamp = stamp
        standoff_pose.pose.position.x = (
            marker_pose.pose.position.x + (front_direction[0] * distance_m)
        )
        standoff_pose.pose.position.y = (
            marker_pose.pose.position.y + (front_direction[1] * distance_m)
        )
        standoff_pose.pose.position.z = 0.0
        yaw = math.atan2(
            marker_pose.pose.position.y - standoff_pose.pose.position.y,
            marker_pose.pose.position.x - standoff_pose.pose.position.x,
        )
        standoff_pose.pose.orientation.z = math.sin(yaw / 2.0)
        standoff_pose.pose.orientation.w = math.cos(yaw / 2.0)
        return standoff_pose

    def _publish_resume(self, should_resume: bool) -> None:
        self._resume_pub.publish(Bool(data=bool(should_resume)))

    async def _sleep_async(self, duration_s: float) -> None:
        if duration_s <= 0.0:
            return

        future: Future = Future()
        timer_box: dict[str, object] = {"timer": None, "done": False}

        def _complete_sleep() -> None:
            if timer_box["done"]:
                return
            timer_box["done"] = True
            if not future.done():
                future.set_result(True)

        timer_box["timer"] = self.create_timer(duration_s, _complete_sleep)
        try:
            await future
        finally:
            timer = timer_box.get("timer")
            if timer is not None:
                timer.cancel()
                self.destroy_timer(timer)

    async def _wait_for_explore_status(
        self,
        accepted_statuses: set[str],
        timeout_s: float,
    ) -> bool:
        deadline = time.monotonic() + max(0.0, timeout_s)
        while time.monotonic() < deadline:
            if self._latest_explore_status in accepted_statuses:
                return True
            await self._sleep_async(0.1)
        if self._latest_explore_status in accepted_statuses:
            return True
        self.get_logger().warn(
            "Timed out waiting for explore status change: "
            f"accepted={sorted(accepted_statuses)} last={self._latest_explore_status}"
        )
        self._emit_debug_event(
            "explore_status_wait_timeout",
            accepted_statuses=sorted(accepted_statuses),
            last_status=str(self._latest_explore_status),
            timeout_s=float(timeout_s),
        )
        return False

    async def _pause_exploration(self) -> bool:
        self._debug_log('Publishing pause request to "/explore/resume".')
        self._emit_debug_event(
            "exploration_pause_requested",
            last_status=str(self._latest_explore_status),
        )
        self._publish_resume(False)
        paused = await self._wait_for_explore_status(
            {
                ExploreStatus.EXPLORATION_PAUSED,
                ExploreStatus.EXPLORATION_COMPLETE,
                ExploreStatus.RETURNED_TO_ORIGIN,
            },
            timeout_s=3.0,
        )
        if paused:
            self._emit_debug_event(
                "exploration_pause_confirmed",
                status=str(self._latest_explore_status),
            )
        else:
            self.get_logger().warn(
                f'Exploration pause was requested but latest status is "{self._latest_explore_status}".'
            )
        return paused

    async def _resume_exploration(self) -> bool:
        self._debug_log('Publishing resume request to "/explore/resume".')
        self._emit_debug_event(
            "exploration_resume_requested",
            last_status=str(self._latest_explore_status),
        )
        self._publish_resume(True)
        resumed = await self._wait_for_explore_status(
            {
                ExploreStatus.EXPLORATION_STARTED,
                ExploreStatus.EXPLORATION_IN_PROGRESS,
            },
            timeout_s=3.0,
        )
        if resumed:
            self._emit_debug_event(
                "exploration_resume_confirmed",
                status=str(self._latest_explore_status),
            )
        else:
            self.get_logger().warn(
                f'Exploration resume was requested but latest status is "{self._latest_explore_status}".'
            )
        return resumed

    def _make_feedback(self, stage: str) -> ExploreArea.Feedback:
        feedback = ExploreArea.Feedback()
        feedback.stage = str(stage)
        feedback.active_landmark_role = str(self._active_landmark_role)
        feedback.required_landmarks_found = int(self._required_landmarks_found())
        feedback.total_landmarks_found = int(len(self._landmark_estimates))
        feedback.current_pose = self._current_pose()
        return feedback

    def _make_result(
        self,
        *,
        success: bool,
        reason: str,
        map_yaml_path: str = "",
        landmark_registry_path: str = "",
    ) -> ExploreArea.Result:
        result = ExploreArea.Result()
        result.success = bool(success)
        result.reason = str(reason)
        result.map_yaml_path = str(map_yaml_path)
        result.landmark_registry_path = str(landmark_registry_path)
        result.required_landmarks_found = int(self._required_landmarks_found())
        result.total_landmarks_found = int(len(self._landmark_estimates))
        return result

    def _pose_delta(self, lhs: np.ndarray, rhs: np.ndarray) -> tuple[float, float]:
        translation_delta = float(np.linalg.norm(lhs[:3, 3] - rhs[:3, 3]))
        lhs_quat = quaternion_from_matrix(lhs)
        rhs_quat = quaternion_from_matrix(rhs)
        lhs_yaw = yaw_from_quaternion_xyzw(lhs_quat)
        rhs_yaw = yaw_from_quaternion_xyzw(rhs_quat)
        yaw_delta = abs(math.atan2(math.sin(lhs_yaw - rhs_yaw), math.cos(lhs_yaw - rhs_yaw)))
        return translation_delta, yaw_delta

    def _maybe_correct_pose_from_detection(
        self,
        *,
        estimate: LandmarkEstimate,
        role_config: LandmarkRoleConfig | None,
        image_frame: str,
        camera_to_marker: np.ndarray,
        camera_to_zed_base: np.ndarray,
    ) -> None:
        if not self.pose_correction_enabled or self._pose_correction_in_flight:
            return
        if estimate.observations < self.pose_correction_min_observations:
            return
        if role_config is None and not self.pose_correction_for_unconfigured_markers:
            return
        if role_config is not None and not role_config.enable_pose_correction:
            return
        if (
            time.monotonic() - estimate.last_pose_correction_mono_s
        ) < self.pose_correction_cooldown_s:
            return

        known_marker_pose, pose_source = self._reference_marker_pose(
            estimate,
            role_config,
            stamp=self.get_clock().now().to_msg(),
        )
        known_map_to_marker = matrix_from_pose(known_marker_pose)
        try:
            marker_to_camera = np.linalg.inv(camera_to_marker)
        except np.linalg.LinAlgError:
            return
        marker_to_zed_base = marker_to_camera @ camera_to_zed_base
        corrected_map_to_zed_base_raw = known_map_to_marker @ marker_to_zed_base

        current_map_to_zed_base = self._lookup_transform_matrix(
            self.map_frame,
            self.zed_base_frame,
        )
        if current_map_to_zed_base is None:
            return

        corrected_map_to_zed_base, corrected_rpy, _ = adjust_pose_correction_target(
            corrected_map_to_zed_base_raw,
            current_map_to_zed_base,
            preserve_z=self.pose_correction_preserve_z,
            preserve_roll_pitch=self.pose_correction_preserve_roll_pitch,
        )

        translation_delta_m, yaw_delta_rad = self._pose_delta(
            corrected_map_to_zed_base,
            current_map_to_zed_base,
        )
        if (
            translation_delta_m < self.pose_correction_min_translation_m and
            yaw_delta_rad < self.pose_correction_min_yaw_rad
        ):
            return

        if not self.pose_correction_client.wait_for_service(timeout_sec=0.0):
            if self._warn_throttled(
                "pose_correction_service_unavailable",
                f'Pose correction service "{self.pose_correction_service_name}" is unavailable; '
                f"skipping correction from marker {estimate.aruco_id}.",
                throttle_s=5.0,
            ):
                self._emit_debug_event(
                    "pose_correction_service_unavailable",
                    marker_id=int(estimate.aruco_id),
                    role_name=str(estimate.role_name or ""),
                    service_name=self.pose_correction_service_name,
                )
            return

        request = SetPose.Request()
        request.pos[0] = float(corrected_map_to_zed_base[0, 3])
        request.pos[1] = float(corrected_map_to_zed_base[1, 3])
        request.pos[2] = float(corrected_map_to_zed_base[2, 3])
        request.orient[0] = float(corrected_rpy[0])
        request.orient[1] = float(corrected_rpy[1])
        request.orient[2] = float(corrected_rpy[2])
        self._debug_log(
            f"Requesting pose correction from marker {estimate.aruco_id}: "
            f"translation_delta={translation_delta_m:.2f} m "
            f"yaw_delta={math.degrees(yaw_delta_rad):.1f} deg. "
            f"preserve_z={self.pose_correction_preserve_z} "
            f"preserve_roll_pitch={self.pose_correction_preserve_roll_pitch}."
        )
        self._emit_debug_event(
            "pose_correction_requested",
            marker_id=int(estimate.aruco_id),
            role_name=str(estimate.role_name or ""),
            translation_delta_m=float(translation_delta_m),
            yaw_delta_deg=float(math.degrees(yaw_delta_rad)),
            reference_pose_source=pose_source,
            preserve_z=bool(self.pose_correction_preserve_z),
            preserve_roll_pitch=bool(self.pose_correction_preserve_roll_pitch),
        )

        try:
            future = self.pose_correction_client.call_async(request)
        except Exception as exc:
            self.get_logger().warn(
                f"Failed to call pose correction service for marker {estimate.aruco_id}: {exc}"
            )
            self._emit_debug_event(
                "pose_correction_call_failed",
                marker_id=int(estimate.aruco_id),
                role_name=str(estimate.role_name or ""),
                error=str(exc),
            )
            return

        estimate.last_pose_correction_mono_s = time.monotonic()
        self._pose_correction_in_flight = True

        def _pose_correction_done(done_future, marker_id: int = estimate.aruco_id) -> None:
            self._pose_correction_in_flight = False
            landmark_estimate = self._landmark_estimates.get(marker_id)
            if landmark_estimate is None:
                return
            try:
                response = done_future.result()
            except Exception as exc:
                self.get_logger().warn(
                    f"Pose correction service failed for marker {marker_id}: {exc}"
                )
                self._emit_debug_event(
                    "pose_correction_failed",
                    marker_id=int(marker_id),
                    role_name=str(landmark_estimate.role_name or ""),
                    error=str(exc),
                )
                return
            if bool(getattr(response, "success", False)):
                landmark_estimate.pose_corrections_applied += 1
                self.get_logger().info(
                    f"Applied ZED pose correction using ArUco marker {marker_id}."
                )
                self._emit_debug_event(
                    "pose_correction_applied",
                    marker_id=int(marker_id),
                    role_name=str(landmark_estimate.role_name or ""),
                    pose_corrections_applied=int(landmark_estimate.pose_corrections_applied),
                )
                return
            self.get_logger().warn(
                f"Pose correction request was rejected for marker {marker_id}."
            )
            self._emit_debug_event(
                "pose_correction_rejected",
                marker_id=int(marker_id),
                role_name=str(landmark_estimate.role_name or ""),
            )

        future.add_done_callback(_pose_correction_done)

    async def _navigate_to_pose(
        self,
        goal_handle,
        target_pose: PoseStamped,
        *,
        stage: str,
        deadline_mono_s: float,
    ) -> tuple[bool, str]:
        target_quaternion = np.array(
            [
                target_pose.pose.orientation.x,
                target_pose.pose.orientation.y,
                target_pose.pose.orientation.z,
                target_pose.pose.orientation.w,
            ],
            dtype=float,
        )
        target_yaw_deg = float(math.degrees(yaw_from_quaternion_xyzw(target_quaternion)))
        self.get_logger().info(
            f'Navigating for stage "{stage}" to '
            f"({target_pose.pose.position.x:.2f}, {target_pose.pose.position.y:.2f}) "
            f"yaw={target_yaw_deg:.1f} deg."
        )
        self._emit_debug_event(
            "navigate_to_pose_started",
            stage=str(stage),
            target_x=float(target_pose.pose.position.x),
            target_y=float(target_pose.pose.position.y),
            target_yaw_deg=target_yaw_deg,
        )
        if self.clear_costmaps_before_landmark_visit:
            try:
                self.navigator.clearAllCostmaps()
            except Exception as exc:
                self.get_logger().warn(f"Failed to clear costmaps before navigation: {exc}")
                self._emit_debug_event(
                    "clear_costmaps_failed",
                    stage=str(stage),
                    error=str(exc),
                )

        try:
            self.navigator.goToPose(target_pose)
        except Exception as exc:
            self.get_logger().warn(f'Failed to dispatch navigation for stage "{stage}": {exc}')
            self._emit_debug_event(
                "navigate_to_pose_dispatch_failed",
                stage=str(stage),
                error=str(exc),
            )
            return False, f"nav_dispatch_failed:{exc}"
        while not self.navigator.isTaskComplete():
            if goal_handle.is_cancel_requested:
                try:
                    self.navigator.cancelTask()
                except Exception:
                    pass
                self._emit_debug_event("navigate_to_pose_canceled", stage=str(stage))
                return False, "canceled"
            if time.monotonic() >= deadline_mono_s:
                try:
                    self.navigator.cancelTask()
                except Exception:
                    pass
                self.get_logger().warn(f'Navigation timed out for stage "{stage}".')
                self._emit_debug_event("navigate_to_pose_timeout", stage=str(stage))
                return False, "timeout"
            goal_handle.publish_feedback(self._make_feedback(stage))
            await self._sleep_async(self.feedback_period_s)

        result = self.navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            self.get_logger().info(f'Navigation succeeded for stage "{stage}".')
            self._emit_debug_event("navigate_to_pose_succeeded", stage=str(stage))
            return True, "succeeded"
        if result == TaskResult.CANCELED:
            self.get_logger().warn(f'Navigation was canceled for stage "{stage}".')
            self._emit_debug_event("navigate_to_pose_canceled", stage=str(stage))
            return False, "canceled"
        self.get_logger().warn(
            f'Navigation failed for stage "{stage}" with result "{result}".'
        )
        self._emit_debug_event(
            "navigate_to_pose_failed",
            stage=str(stage),
            task_result=str(result),
        )
        return False, "failed"

    async def _call_trigger_service(
        self,
        service_name: str,
        *,
        role_name: str,
        goal_handle,
        deadline_mono_s: float,
    ) -> tuple[bool, str]:
        if not service_name:
            self.get_logger().warn(
                f'Role "{role_name}" is missing a trigger service name for its action hook.'
            )
            self._emit_debug_event(
                "role_service_name_missing",
                role_name=str(role_name),
            )
            return False, f"{role_name}_service_name_missing"

        client = self._trigger_clients.get(service_name)
        if client is None:
            client = self.create_client(Trigger, service_name)
            self._trigger_clients[service_name] = client

        if not client.wait_for_service(timeout_sec=2.0):
            self.get_logger().warn(
                f'Service "{service_name}" for role "{role_name}" is unavailable.'
            )
            self._emit_debug_event(
                "role_service_unavailable",
                role_name=str(role_name),
                service_name=str(service_name),
            )
            return False, f"{role_name}_service_unavailable"

        self.get_logger().info(
            f'Calling service "{service_name}" for role "{role_name}".'
        )
        self._emit_debug_event(
            "role_service_call_started",
            role_name=str(role_name),
            service_name=str(service_name),
        )
        future = client.call_async(Trigger.Request())
        while not future.done():
            if goal_handle.is_cancel_requested:
                self._emit_debug_event(
                    "role_service_call_canceled",
                    role_name=str(role_name),
                    service_name=str(service_name),
                )
                return False, "canceled"
            if time.monotonic() >= deadline_mono_s:
                self.get_logger().warn(
                    f'Service call "{service_name}" timed out for role "{role_name}".'
                )
                self._emit_debug_event(
                    "role_service_call_timeout",
                    role_name=str(role_name),
                    service_name=str(service_name),
                )
                return False, "timeout"
            goal_handle.publish_feedback(self._make_feedback(f"calling_{role_name}_service"))
            await self._sleep_async(0.2)

        try:
            response = future.result()
        except Exception as exc:
            self.get_logger().warn(
                f'Service call "{service_name}" failed for role "{role_name}": {exc}'
            )
            self._emit_debug_event(
                "role_service_call_failed",
                role_name=str(role_name),
                service_name=str(service_name),
                error=str(exc),
            )
            return False, f"{role_name}_service_failed:{exc}"
        success = bool(response.success)
        message = str(response.message or role_name)
        if success:
            self.get_logger().info(
                f'Service "{service_name}" succeeded for role "{role_name}": {message}'
            )
            self._emit_debug_event(
                "role_service_call_succeeded",
                role_name=str(role_name),
                service_name=str(service_name),
                message=message,
            )
        else:
            self.get_logger().warn(
                f'Service "{service_name}" reported failure for role "{role_name}": {message}'
            )
            self._emit_debug_event(
                "role_service_call_rejected",
                role_name=str(role_name),
                service_name=str(service_name),
                message=message,
            )
        return success, message

    async def _execute_role_hook(
        self,
        role_config: LandmarkRoleConfig,
        *,
        goal_handle,
        deadline_mono_s: float,
    ) -> tuple[bool, str]:
        if role_config.action_hook == "swag_station_dwell":
            self.get_logger().info(
                f'Starting swag-station dwell for role "{role_config.name}" '
                f"for up to {role_config.dwell_time_s:.1f} s."
            )
            self._emit_debug_event(
                "role_hook_started",
                role_name=role_config.name,
                action_hook=role_config.action_hook,
                dwell_time_s=float(role_config.dwell_time_s),
            )
            remaining_s = min(role_config.dwell_time_s, max(0.0, deadline_mono_s - time.monotonic()))
            while remaining_s > 0.0:
                if goal_handle.is_cancel_requested:
                    self._emit_debug_event(
                        "role_hook_canceled",
                        role_name=role_config.name,
                        action_hook=role_config.action_hook,
                    )
                    return False, "canceled"
                goal_handle.publish_feedback(self._make_feedback(f"dwell_{role_config.name}"))
                slice_s = min(remaining_s, self.feedback_period_s)
                await self._sleep_async(slice_s)
                remaining_s -= slice_s
            self.get_logger().info(
                f'Completed swag-station dwell for role "{role_config.name}".'
            )
            self._emit_debug_event(
                "role_hook_succeeded",
                role_name=role_config.name,
                action_hook=role_config.action_hook,
                result="swag_station_dwell_complete",
            )
            return True, "swag_station_dwell_complete"

        if role_config.action_hook == "home_dock_service":
            self.get_logger().info(
                f'Executing home-dock service hook for role "{role_config.name}".'
            )
            return await self._call_trigger_service(
                role_config.trigger_service_name,
                role_name=role_config.name,
                goal_handle=goal_handle,
                deadline_mono_s=deadline_mono_s,
            )

        self._debug_log(
            f'No additional hook configured for role "{role_config.name}".'
        )
        return True, "no_additional_action"

    async def _visit_landmark_role(
        self,
        role_name: str,
        *,
        goal_handle,
        deadline_mono_s: float,
    ) -> tuple[bool, str]:
        role_config = self._role_configs.get(role_name)
        if role_config is None:
            self.get_logger().warn(f'Role "{role_name}" is not configured.')
            self._emit_debug_event("role_visit_failed", role_name=str(role_name), reason="role_not_configured")
            return False, "role_not_configured"
        estimate = self._role_estimate(role_name)
        if estimate is None:
            self.get_logger().warn(f'Role "{role_name}" has not been observed yet.')
            self._emit_debug_event("role_visit_failed", role_name=str(role_name), reason="role_not_observed")
            return False, "role_not_observed"
        if estimate.visit_attempts > 0:
            self._debug_log(f'Skipping repeat visit for role "{role_name}".')
            return False, "visit_already_attempted"

        estimate.visit_attempts += 1
        self._active_landmark_role = role_name
        self._publish_landmark_markers()
        self.get_logger().info(
            f'Starting visit for role "{role_name}" using marker {estimate.aruco_id} '
            f"after {estimate.observations} observation(s)."
        )
        self._emit_debug_event(
            "role_visit_started",
            role_name=str(role_name),
            marker_id=int(estimate.aruco_id),
            observations=int(estimate.observations),
        )
        pause_ok = await self._pause_exploration()
        if not pause_ok:
            self.get_logger().warn(
                f'Proceeding with role "{role_name}" visit even though exploration did not confirm a paused state.'
            )
        await self._sleep_async(self.landmark_visit_settle_s)

        standoff_pose = self._standoff_pose(
            estimate,
            distance_m=role_config.standoff_distance_m,
            role_config=role_config,
        )
        self._emit_debug_event(
            "role_visit_standoff_pose",
            role_name=str(role_name),
            target_x=float(standoff_pose.pose.position.x),
            target_y=float(standoff_pose.pose.position.y),
            reference_pose_source=(
                "configured" if role_config.has_configured_marker_pose() else "observed"
            ),
        )
        nav_ok, nav_reason = await self._navigate_to_pose(
            goal_handle,
            standoff_pose,
            stage=f"visiting_{role_name}",
            deadline_mono_s=deadline_mono_s,
        )
        if not nav_ok:
            self._active_landmark_role = ""
            if not goal_handle.is_cancel_requested:
                await self._resume_exploration()
            self.get_logger().warn(
                f'Visit navigation failed for role "{role_name}": {nav_reason}'
            )
            self._emit_debug_event(
                "role_visit_failed",
                role_name=str(role_name),
                reason=str(nav_reason),
            )
            return False, nav_reason

        hook_ok, hook_reason = await self._execute_role_hook(
            role_config,
            goal_handle=goal_handle,
            deadline_mono_s=deadline_mono_s,
        )
        if hook_ok:
            estimate.action_performed = True
            self._publish_landmark_markers()
            self.get_logger().info(
                f'Completed role "{role_name}" visit: {hook_reason}'
            )
            self._emit_debug_event(
                "role_visit_succeeded",
                role_name=str(role_name),
                reason=str(hook_reason),
            )
        else:
            self.get_logger().warn(
                f'Role "{role_name}" hook failed: {hook_reason}'
            )
            self._emit_debug_event(
                "role_visit_failed",
                role_name=str(role_name),
                reason=str(hook_reason),
            )

        self._active_landmark_role = ""
        self._publish_landmark_markers()
        if not goal_handle.is_cancel_requested:
            resume_ok = await self._resume_exploration()
            if not resume_ok:
                self.get_logger().warn(
                    f'Exploration did not confirm a resumed state after visiting role "{role_name}".'
                )
        return hook_ok, hook_reason

    def _landmark_registry_payload(self, map_yaml_path: str) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "schema_version": 1,
            "saved_at_ns": int(self.get_clock().now().nanoseconds),
            "map_yaml_path": str(map_yaml_path),
            "landmarks": {},
        }

        for marker_id, estimate in sorted(self._landmark_estimates.items()):
            stamp = self.get_clock().now().to_msg()
            role_config = self._aruco_id_to_role.get(marker_id)
            observed_marker_pose = estimate.marker_pose(
                frame_id=self.map_frame,
                stamp=stamp,
            )
            reference_marker_pose, reference_pose_source = self._reference_marker_pose(
                estimate,
                role_config,
                stamp=stamp,
            )
            configured_marker_pose = self._configured_marker_pose(role_config, stamp=stamp)
            standoff_distance_m = (
                role_config.standoff_distance_m if role_config is not None else 1.0
            )
            standoff_pose = self._standoff_pose(
                estimate,
                distance_m=standoff_distance_m,
                role_config=role_config,
            )
            front_direction = estimate.front_direction_xy()
            payload["landmarks"][str(marker_id)] = {
                "aruco_id": int(marker_id),
                "role_name": estimate.role_name,
                "required": bool(estimate.required),
                "observations": int(estimate.observations),
                "first_seen_ns": int(estimate.first_seen_ns),
                "last_seen_ns": int(estimate.last_seen_ns),
                "last_distance_m": float(estimate.last_distance_m),
                "action_performed": bool(estimate.action_performed),
                "visit_attempts": int(estimate.visit_attempts),
                "pose_corrections_applied": int(estimate.pose_corrections_applied),
                "marker_pose": pose_stamped_to_dict(observed_marker_pose),
                "reference_pose_source": reference_pose_source,
                "reference_marker_pose": pose_stamped_to_dict(reference_marker_pose),
                "configured_map_pose": (
                    pose_stamped_to_dict(configured_marker_pose)
                    if configured_marker_pose is not None
                    else None
                ),
                "standoff_pose": pose_stamped_to_dict(standoff_pose),
                "front_direction_xy": {
                    "x": float(front_direction[0]),
                    "y": float(front_direction[1]),
                },
            }

        return payload

    async def _save_map(self, map_yaml_path: Path) -> tuple[bool, str]:
        if not self.map_save_client.wait_for_service(timeout_sec=2.0):
            self.get_logger().warn(
                f'Map save service "{self.map_save_service_name}" is unavailable.'
            )
            self._emit_debug_event(
                "map_save_service_unavailable",
                service_name=self.map_save_service_name,
                map_yaml_path=str(map_yaml_path),
            )
            return False, "map_save_service_unavailable"

        request = SaveMap.Request()
        request.map_topic = self.map_topic
        request.map_url = map_yaml_path.resolve().as_uri()
        request.image_format = self.map_save_image_format
        request.map_mode = self.map_save_mode
        request.free_thresh = float(self.map_save_free_thresh)
        request.occupied_thresh = float(self.map_save_occupied_thresh)
        self.get_logger().info(
            f'Saving map to "{map_yaml_path}" from topic "{self.map_topic}".'
        )
        self._emit_debug_event(
            "map_save_requested",
            map_yaml_path=str(map_yaml_path),
            map_topic=self.map_topic,
            service_name=self.map_save_service_name,
        )

        future = self.map_save_client.call_async(request)
        while not future.done():
            await self._sleep_async(0.1)
        try:
            response = future.result()
        except Exception as exc:
            self.get_logger().warn(f"Map save request failed: {exc}")
            self._emit_debug_event("map_save_failed", error=str(exc), map_yaml_path=str(map_yaml_path))
            return False, f"map_save_failed:{exc}"
        saved = bool(response.result)
        if saved:
            self.get_logger().info(f'Saved map successfully to "{map_yaml_path}".')
            self._emit_debug_event("map_save_succeeded", map_yaml_path=str(map_yaml_path))
        else:
            self.get_logger().warn(f'Map save was rejected for "{map_yaml_path}".')
            self._emit_debug_event("map_save_rejected", map_yaml_path=str(map_yaml_path))
        return saved, "saved" if saved else "map_save_rejected"

    async def _save_artifacts(self, *, save_map: bool) -> tuple[bool, str, str, str]:
        artifact_root = self.artifact_root
        if not artifact_root.is_absolute():
            artifact_root = (Path.cwd() / artifact_root).resolve()
        try:
            artifact_root.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            self.get_logger().error(
                f'Failed to prepare explore-area artifact directory "{artifact_root}": {exc}'
            )
            self._emit_debug_event(
                "artifact_root_prepare_failed",
                artifact_root=str(artifact_root),
                error=str(exc),
            )
            return False, "", "", f"artifact_root_prepare_failed:{exc}"

        map_yaml_path = artifact_root / "map.yaml"
        landmark_registry_path = artifact_root / "landmarks.json"
        self.get_logger().info(f'Saving explore-area artifacts under "{artifact_root}".')
        self._emit_debug_event(
            "artifact_save_started",
            artifact_root=str(artifact_root),
            save_map=bool(save_map),
        )

        map_saved = True
        map_reason = "map_save_skipped"
        if save_map:
            map_saved, map_reason = await self._save_map(map_yaml_path)

        registry_payload = self._landmark_registry_payload(str(map_yaml_path))
        try:
            with landmark_registry_path.open("w", encoding="utf-8") as stream:
                json.dump(registry_payload, stream, indent=2, sort_keys=True)
                stream.write("\n")
        except Exception as exc:
            self.get_logger().error(
                f'Failed to write landmark registry "{landmark_registry_path}": {exc}'
            )
            self._emit_debug_event(
                "landmark_registry_write_failed",
                landmark_registry_path=str(landmark_registry_path),
                error=str(exc),
                map_saved=bool(map_saved),
                map_reason=str(map_reason),
            )
            return False, str(map_yaml_path), "", f"landmark_registry_write_failed:{exc}"

        artifacts_saved = bool(map_saved) if save_map else True
        if artifacts_saved:
            self.get_logger().info(
                f'Saved explore-area artifacts: map="{map_yaml_path}", registry="{landmark_registry_path}".'
            )
            self._emit_debug_event(
                "artifact_save_complete",
                map_yaml_path=str(map_yaml_path),
                landmark_registry_path=str(landmark_registry_path),
                map_saved=bool(map_saved),
                map_reason=str(map_reason),
            )
        else:
            self.get_logger().warn(
                f'Landmark registry was saved to "{landmark_registry_path}", but the map save failed: {map_reason}'
            )
            self._emit_debug_event(
                "artifact_save_incomplete",
                map_yaml_path=str(map_yaml_path),
                landmark_registry_path=str(landmark_registry_path),
                map_saved=bool(map_saved),
                map_reason=str(map_reason),
            )
        return artifacts_saved, str(map_yaml_path), str(landmark_registry_path), str(map_reason)

    async def execute_cb(self, goal_handle):
        self._goal_active = True
        self._landmark_estimates = {}
        self._pending_landmark_roles = []
        self._active_landmark_role = ""
        self._pose_correction_in_flight = False
        self._publish_landmark_markers()

        save_map = bool(goal_handle.request.save_map)
        deadline_mono_s = time.monotonic() + self.mission_timeout_s
        self.get_logger().info(
            "Starting ExploreArea mission: "
            f"save_map={save_map}, timeout_s={self.mission_timeout_s:.1f}, "
            f"required_roles={sorted(self._required_roles())}"
        )
        self._emit_debug_event(
            "mission_started",
            save_map=save_map,
            mission_timeout_s=float(self.mission_timeout_s),
            required_roles=sorted(self._required_roles()),
            initial_pose_frame=str(goal_handle.request.initial_pose.header.frame_id),
        )
        self._publish_resume(True)

        try:
            while rclpy.ok():
                if goal_handle.is_cancel_requested:
                    self._publish_resume(False)
                    try:
                        self.navigator.cancelTask()
                    except Exception:
                        pass
                    map_yaml_path = ""
                    landmark_registry_path = ""
                    artifact_reason = ""
                    if self.save_partial_on_cancel:
                        _, map_yaml_path, landmark_registry_path, artifact_reason = await self._save_artifacts(
                            save_map=save_map,
                        )
                    self.get_logger().info("ExploreArea mission canceled.")
                    self._emit_debug_event(
                        "mission_canceled",
                        map_yaml_path=map_yaml_path,
                        landmark_registry_path=landmark_registry_path,
                        artifact_reason=str(artifact_reason),
                    )
                    goal_handle.canceled()
                    return self._make_result(
                        success=False,
                        reason=(
                            f"canceled:{artifact_reason}"
                            if artifact_reason and artifact_reason not in {"saved", "map_save_skipped"}
                            else "canceled"
                        ),
                        map_yaml_path=map_yaml_path,
                        landmark_registry_path=landmark_registry_path,
                    )

                if time.monotonic() >= deadline_mono_s:
                    self._publish_resume(False)
                    self.get_logger().warn("ExploreArea mission timed out.")
                    self._emit_debug_event("mission_timeout")
                    artifacts_saved, map_yaml_path, landmark_registry_path, artifact_reason = await self._save_artifacts(
                        save_map=save_map,
                    )
                    goal_handle.abort()
                    return self._make_result(
                        success=False,
                        reason=(
                            "mission_timeout"
                            if artifacts_saved
                            else f"mission_timeout:{artifact_reason or 'artifact_save_failed'}"
                        ),
                        map_yaml_path=map_yaml_path,
                        landmark_registry_path=landmark_registry_path,
                    )

                if self._pending_landmark_roles:
                    role_name = self._pending_landmark_roles.pop(0)
                    await self._visit_landmark_role(
                        role_name,
                        goal_handle=goal_handle,
                        deadline_mono_s=deadline_mono_s,
                    )
                    continue

                if (
                    self.park_at_home_on_complete and
                    self._latest_explore_status in {
                        ExploreStatus.EXPLORATION_COMPLETE,
                        ExploreStatus.RETURNED_TO_ORIGIN,
                    }
                ):
                    home_estimate = self._role_estimate("home_dock")
                    if home_estimate is not None and home_estimate.visit_attempts == 0:
                        await self._visit_landmark_role(
                            "home_dock",
                            goal_handle=goal_handle,
                            deadline_mono_s=deadline_mono_s,
                        )
                        continue

                if self._latest_explore_status in {
                    ExploreStatus.EXPLORATION_COMPLETE,
                    ExploreStatus.RETURNED_TO_ORIGIN,
                }:
                    self._publish_resume(False)
                    artifacts_saved, map_yaml_path, landmark_registry_path, artifact_reason = await self._save_artifacts(
                        save_map=save_map,
                    )
                    missing_roles = sorted(
                        self._required_roles() - {
                            estimate.role_name
                            for estimate in self._landmark_estimates.values()
                            if estimate.role_name is not None
                        }
                    )
                    success = not missing_roles and artifacts_saved
                    if success:
                        self.get_logger().info(
                            "ExploreArea mission completed successfully."
                        )
                        self._emit_debug_event(
                            "mission_succeeded",
                            map_yaml_path=map_yaml_path,
                            landmark_registry_path=landmark_registry_path,
                        )
                        goal_handle.succeed()
                        return self._make_result(
                            success=True,
                            reason="exploration_complete",
                            map_yaml_path=map_yaml_path,
                            landmark_registry_path=landmark_registry_path,
                        )

                    reason = "missing_required_landmarks"
                    if missing_roles:
                        reason = f'missing_required_landmarks:{",".join(missing_roles)}'
                    if not artifacts_saved:
                        reason = f"{reason}:{artifact_reason or 'artifact_save_failed'}"
                    self.get_logger().warn(
                        f"ExploreArea mission completed unsuccessfully: {reason}"
                    )
                    self._emit_debug_event(
                        "mission_failed",
                        reason=str(reason),
                        missing_roles=missing_roles,
                        map_yaml_path=map_yaml_path,
                        landmark_registry_path=landmark_registry_path,
                    )
                    goal_handle.abort()
                    return self._make_result(
                        success=False,
                        reason=reason,
                        map_yaml_path=map_yaml_path,
                        landmark_registry_path=landmark_registry_path,
                    )

                goal_handle.publish_feedback(
                    self._make_feedback(self._latest_explore_status or "exploration_pending")
                )
                await self._sleep_async(self.feedback_period_s)

            goal_handle.abort()
            self.get_logger().warn("ExploreArea mission aborted because ROS is shutting down.")
            self._emit_debug_event("mission_aborted", reason="ros_shutdown")
            return self._make_result(success=False, reason="ros_shutdown")
        except Exception as exc:
            self.get_logger().error(
                f"ExploreArea mission failed with an unexpected exception: {exc}"
            )
            self._emit_debug_event("mission_exception", error=str(exc))
            goal_handle.abort()
            return self._make_result(success=False, reason=f"exception:{exc}")
        finally:
            self._goal_active = False
            self._active_landmark_role = ""
            self._publish_resume(False)


def main() -> None:
    rclpy.init()
    node = ExploreAreaMissionServer()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
