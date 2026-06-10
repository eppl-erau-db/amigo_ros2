#!/usr/bin/env python3
"""
aruco_detector_node — detect ArUco markers in the ZED rectified RGB image and
publish each detected marker's pose.

Why a new node (instead of the ZED ``zed_aruco_localization`` example): that
example only *resets the ZED's own pose* from hard-coded marker world-poses via
the ``set_pose`` service. It never publishes *where a detected marker is*, so it
can neither record markers during a mapping drive nor align the robot to one.

This node detects DICT_6X6_100 markers with OpenCV, recovers each marker's pose
via solvePnP using the camera intrinsics (from camera_info) and the configured
marker size, and publishes the marker poses transformed into two frames:

* ``markers_map_topic``  (default /aruco/markers_map)  — MarkerArray in the map
  frame, used by the explore recorder (to log marker positions) and by deliver
  staging (to navigate near a marker).
* ``markers_base_topic`` (default /aruco/markers_base) — MarkerArray in the robot
  base frame, derived straight from the camera→base extrinsic (no localization),
  used by the deliver fine-alignment visual servo.

Each ``visualization_msgs/Marker`` carries the ArUco id in ``marker.id`` and the
pose in ``marker.pose``. Optionally also broadcasts ``<tf_frame_prefix><id>`` TF
in the map frame for RViz / convenience.
"""
from __future__ import annotations

import math

import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from geometry_msgs.msg import TransformStamped
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rclpy.time import Time
from sensor_msgs.msg import CameraInfo, Image
from std_msgs.msg import ColorRGBA
import tf2_ros
from visualization_msgs.msg import Marker, MarkerArray


# OpenCV ArUco API differs across versions; build a small compatibility shim.
def _make_aruco(dict_name: str):
    aruco = cv2.aruco
    dict_id = getattr(aruco, dict_name, aruco.DICT_6X6_100)
    dictionary = aruco.getPredefinedDictionary(dict_id)
    # DetectorParameters: 4.7+ uses DetectorParameters(); 4.6 uses *_create().
    if hasattr(aruco, "DetectorParameters_create"):
        params = aruco.DetectorParameters_create()
    else:
        params = aruco.DetectorParameters()

    if hasattr(aruco, "ArucoDetector"):
        detector = aruco.ArucoDetector(dictionary, params)

        def detect(gray):
            corners, ids, _ = detector.detectMarkers(gray)
            return corners, ids
    else:
        def detect(gray):
            corners, ids, _ = aruco.detectMarkers(gray, dictionary, parameters=params)
            return corners, ids

    return detect


def _quat_to_rot(qx, qy, qz, qw):
    """Quaternion -> 3x3 rotation matrix."""
    n = math.sqrt(qx * qx + qy * qy + qz * qz + qw * qw) or 1.0
    qx, qy, qz, qw = qx / n, qy / n, qz / n, qw / n
    return np.array([
        [1 - 2 * (qy * qy + qz * qz), 2 * (qx * qy - qz * qw), 2 * (qx * qz + qy * qw)],
        [2 * (qx * qy + qz * qw), 1 - 2 * (qx * qx + qz * qz), 2 * (qy * qz - qx * qw)],
        [2 * (qx * qz - qy * qw), 2 * (qy * qz + qx * qw), 1 - 2 * (qx * qx + qy * qy)],
    ])


def _rot_to_quat(R):
    """3x3 rotation matrix -> (x, y, z, w) quaternion."""
    t = np.trace(R)
    if t > 0:
        s = math.sqrt(t + 1.0) * 2
        w = 0.25 * s
        x = (R[2, 1] - R[1, 2]) / s
        y = (R[0, 2] - R[2, 0]) / s
        z = (R[1, 0] - R[0, 1]) / s
    elif R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
        s = math.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2]) * 2
        w = (R[2, 1] - R[1, 2]) / s
        x = 0.25 * s
        y = (R[0, 1] + R[1, 0]) / s
        z = (R[0, 2] + R[2, 0]) / s
    elif R[1, 1] > R[2, 2]:
        s = math.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2]) * 2
        w = (R[0, 2] - R[2, 0]) / s
        x = (R[0, 1] + R[1, 0]) / s
        y = 0.25 * s
        z = (R[1, 2] + R[2, 1]) / s
    else:
        s = math.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1]) * 2
        w = (R[1, 0] - R[0, 1]) / s
        x = (R[0, 2] + R[2, 0]) / s
        y = (R[1, 2] + R[2, 1]) / s
        z = 0.25 * s
    return x, y, z, w


def _tf_to_matrix(tf: TransformStamped) -> np.ndarray:
    M = np.eye(4)
    M[:3, :3] = _quat_to_rot(
        tf.transform.rotation.x, tf.transform.rotation.y,
        tf.transform.rotation.z, tf.transform.rotation.w,
    )
    M[0, 3] = tf.transform.translation.x
    M[1, 3] = tf.transform.translation.y
    M[2, 3] = tf.transform.translation.z
    return M


class ArucoDetectorNode(Node):
    def __init__(self) -> None:
        super().__init__("aruco_detector_node")

        # NITROS zed-ros2-wrapper publishes the rectified color stream under
        # rgb/color/rect/* (the older rgb/image_rect_color / rgb/camera_info names
        # are gone; a mismatch leaves this node stuck at "waiting for camera_info").
        self.image_topic = str(self.declare_parameter(
            "image_topic", "/zed/zed_node/rgb/color/rect/image").value)
        self.camera_info_topic = str(self.declare_parameter(
            "camera_info_topic", "/zed/zed_node/rgb/color/rect/camera_info").value)
        self.markers_map_topic = str(self.declare_parameter(
            "markers_map_topic", "/aruco/markers_map").value)
        self.markers_base_topic = str(self.declare_parameter(
            "markers_base_topic", "/aruco/markers_base").value)
        self.dictionary_name = str(self.declare_parameter("dictionary", "DICT_6X6_1000").value)
        self.marker_size_m = float(self.declare_parameter("marker_size_m", 0.20).value)
        self.map_frame = str(self.declare_parameter("map_frame", "map").value)
        self.base_frame = str(self.declare_parameter("base_frame", "base_link").value)
        self.detect_rate_hz = max(0.5, float(self.declare_parameter("detect_rate_hz", 5.0).value))
        self.publish_tf = bool(self.declare_parameter("publish_tf", True).value)
        self.tf_frame_prefix = str(self.declare_parameter("tf_frame_prefix", "aruco_").value)
        self.marker_lifetime_s = float(self.declare_parameter("marker_lifetime_s", 1.0).value)
        self.debug = bool(self.declare_parameter("debug", False).value)

        self._bridge = CvBridge()
        self._detect = _make_aruco(self.dictionary_name)
        self._K: np.ndarray | None = None
        self._D: np.ndarray | None = None
        self._latest_image: Image | None = None
        self._dbg_last: dict[str, float] = {}  # per-message last-log time for manual throttling

        s = self.marker_size_m / 2.0
        # Object points in the marker frame matching ArUco corner order
        # (top-left, top-right, bottom-right, bottom-left); x right, y up, z out.
        self._obj_points = np.array(
            [[-s, s, 0.0], [s, s, 0.0], [s, -s, 0.0], [-s, -s, 0.0]],
            dtype=np.float32,
        )
        self._pnp_flag = getattr(cv2, "SOLVEPNP_IPPE_SQUARE", cv2.SOLVEPNP_ITERATIVE)

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self) if self.publish_tf else None

        self.markers_map_pub = self.create_publisher(MarkerArray, self.markers_map_topic, 10)
        self.markers_base_pub = self.create_publisher(MarkerArray, self.markers_base_topic, 10)

        # The ZED wrapper publishes images + camera_info with sensor-data QoS (BEST_EFFORT).
        # A default RELIABLE subscription is QoS-incompatible and receives NOTHING (the node
        # would sit forever at "waiting for camera_info"), so subscribe BEST_EFFORT here.
        self.create_subscription(
            CameraInfo, self.camera_info_topic, self._camera_info_cb, qos_profile_sensor_data)
        self.create_subscription(
            Image, self.image_topic, self._image_cb, qos_profile_sensor_data)
        self.create_timer(1.0 / self.detect_rate_hz, self._process_latest)

        self.get_logger().info(
            f"aruco_detector_node ready. dict={self.dictionary_name} "
            f"marker_size={self.marker_size_m}m image={self.image_topic} "
            f"rate={self.detect_rate_hz}Hz frames=[{self.map_frame},{self.base_frame}] "
            f"debug={self.debug}"
        )

    def _dbg(self, msg: str, throttle_s: float = 0.0, key: str = "") -> None:
        if not self.debug:
            return
        # Throttle manually by message identity rather than via rclpy's
        # throttle_duration_sec kwarg. All _dbg calls share THIS single
        # get_logger().info() call-site, and rclpy keys its throttle filter on the
        # call-site (function+file+line) — passing two different throttle values
        # through here raises "Logging filter parameters cannot be changed between
        # calls" and kills the node. `key` buckets messages with jittering content
        # (e.g. formatted poses) so the bucket dict stays bounded.
        if throttle_s > 0.0:
            bucket = key or msg
            now = self.get_clock().now().nanoseconds * 1e-9
            if now - self._dbg_last.get(bucket, -1e18) < throttle_s:
                return
            self._dbg_last[bucket] = now
        self.get_logger().info(f"[aruco] {msg}")

    def _camera_info_cb(self, msg: CameraInfo) -> None:
        first = self._K is None
        self._K = np.array(msg.k, dtype=np.float64).reshape(3, 3)
        d = np.array(msg.d, dtype=np.float64)
        self._D = d if d.size else np.zeros((5,), dtype=np.float64)
        if first:
            self._dbg(f"camera_info received from {self.camera_info_topic}; fx={self._K[0, 0]:.1f}")

    def _image_cb(self, msg: Image) -> None:
        self._latest_image = msg

    def _process_latest(self) -> None:
        msg = self._latest_image
        if msg is None or self._K is None:
            if self._K is None:
                self._dbg("waiting for camera_info...", throttle_s=5.0)
            elif msg is None:
                self._dbg("waiting for image...", throttle_s=5.0)
            return
        self._latest_image = None  # process each frame at most once

        try:
            gray = self._bridge.imgmsg_to_cv2(msg, desired_encoding="mono8")
        except Exception as exc:
            self.get_logger().warn(f"cv_bridge conversion failed: {exc}", throttle_duration_sec=5.0)
            return

        corners, ids = self._detect(gray)
        if ids is None or len(ids) == 0:
            self._dbg("no markers in view", throttle_s=3.0)
            return
        self._dbg(f"detected {len(ids)} marker(s): ids={sorted(int(i) for i in ids.flatten())}",
                  throttle_s=1.0, key="detected")

        optical_frame = msg.header.frame_id or "zed_left_camera_optical_frame"
        stamp = msg.header.stamp

        map_tf = self._lookup(self.map_frame, optical_frame, stamp)
        base_tf = self._lookup(self.base_frame, optical_frame, stamp)
        map_M = _tf_to_matrix(map_tf) if map_tf is not None else None
        base_M = _tf_to_matrix(base_tf) if base_tf is not None else None

        map_markers = MarkerArray()
        base_markers = MarkerArray()
        tf_msgs: list[TransformStamped] = []

        for corner, marker_id in zip(corners, ids.flatten()):
            ok, rvec, tvec = cv2.solvePnP(
                self._obj_points, corner.reshape(4, 2).astype(np.float32),
                self._K, self._D, flags=self._pnp_flag,
            )
            if not ok:
                continue
            R, _ = cv2.Rodrigues(rvec)
            optical_M = np.eye(4)
            optical_M[:3, :3] = R
            optical_M[:3, 3] = tvec.flatten()

            if map_M is not None:
                m = self._make_marker(int(marker_id), self.map_frame, stamp, map_M @ optical_M)
                map_markers.markers.append(m)
                if self.tf_broadcaster is not None:
                    tf_msgs.append(self._make_tf(int(marker_id), self.map_frame, stamp, map_M @ optical_M))
            if base_M is not None:
                base_markers.markers.append(
                    self._make_marker(int(marker_id), self.base_frame, stamp, base_M @ optical_M))

        if map_markers.markers:
            self.markers_map_pub.publish(map_markers)
            if self.debug:
                poses = ", ".join(
                    f"{m.id}:({m.pose.position.x:.2f},{m.pose.position.y:.2f})"
                    for m in map_markers.markers)
                self._dbg(f"{self.map_frame}: {poses}", throttle_s=1.0, key="map_poses")
        elif map_M is None:
            self._dbg(f"TF {self.map_frame}<-{optical_frame} unavailable; no map poses",
                      throttle_s=5.0, key="tf_map_missing")
        if base_markers.markers:
            self.markers_base_pub.publish(base_markers)
        if tf_msgs and self.tf_broadcaster is not None:
            self.tf_broadcaster.sendTransform(tf_msgs)

    def _lookup(self, target: str, source: str, stamp):
        try:
            return self.tf_buffer.lookup_transform(target, source, Time())
        except Exception as exc:
            self.get_logger().warn(
                f"TF {target}<-{source} unavailable: {exc}", throttle_duration_sec=5.0)
            return None

    def _make_marker(self, marker_id: int, frame: str, stamp, M: np.ndarray) -> Marker:
        m = Marker()
        m.header.frame_id = frame
        m.header.stamp = stamp
        m.ns = "aruco"
        m.id = marker_id
        m.type = Marker.CUBE
        m.action = Marker.ADD
        m.pose.position.x = float(M[0, 3])
        m.pose.position.y = float(M[1, 3])
        m.pose.position.z = float(M[2, 3])
        qx, qy, qz, qw = _rot_to_quat(M[:3, :3])
        m.pose.orientation.x, m.pose.orientation.y = qx, qy
        m.pose.orientation.z, m.pose.orientation.w = qz, qw
        m.scale.x = m.scale.y = self.marker_size_m
        m.scale.z = 0.01
        m.color = ColorRGBA(r=0.0, g=1.0, b=0.2, a=0.8)
        m.lifetime = Duration(seconds=self.marker_lifetime_s).to_msg()
        return m

    def _make_tf(self, marker_id: int, frame: str, stamp, M: np.ndarray) -> TransformStamped:
        t = TransformStamped()
        t.header.frame_id = frame
        t.header.stamp = stamp
        t.child_frame_id = f"{self.tf_frame_prefix}{marker_id}"
        t.transform.translation.x = float(M[0, 3])
        t.transform.translation.y = float(M[1, 3])
        t.transform.translation.z = float(M[2, 3])
        qx, qy, qz, qw = _rot_to_quat(M[:3, :3])
        t.transform.rotation.x, t.transform.rotation.y = qx, qy
        t.transform.rotation.z, t.transform.rotation.w = qz, qw
        return t


def main() -> None:
    rclpy.init()
    node = ArucoDetectorNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
