import math
import subprocess
import sys
import threading

import cv2
import numpy as np

import rclpy
import rclpy.time
import tf2_ros
from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import OccupancyGrid, Odometry
from rclpy.action import ActionClient
from rclpy.duration import Duration
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix, LaserScan, Imu, PointCloud2, JointState, Image, CameraInfo
from std_msgs.msg import String

from go2_interfaces.action import Search

from PySide6.QtCore import (
    QAbstractListModel,
    QModelIndex,
    Qt,
    QTimer,
    Slot,
    QObject,
    Signal,
    Property,
)
from PySide6.QtGui import QGuiApplication, QImage
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickImageProvider


# ── Topic definitions ──────────────────────────────────────────────────────────
MONITORED_TOPICS = [
    {"topic": "/fix",          "alias": "GPS Fix",        "msg_type": NavSatFix},
    {"topic": "/scan",         "alias": "LiDAR Scanner",  "msg_type": LaserScan},
    {"topic": "/imu/data_raw", "alias": "IMU Sensor",     "msg_type": Imu},
    {"topic": "/map",          "alias": "Map",            "msg_type": OccupancyGrid},
    {"topic": "/odom",         "alias": "Odometry",       "msg_type": Odometry},
    {"topic": "/pointcloud",   "alias": "Point Cloud",    "msg_type": PointCloud2},
    {"topic": "/joint_states", "alias": "Joint Motors",   "msg_type": JointState},
]

# A topic is ONLINE if a message arrived in the last N seconds, IDLE within M seconds, else OFFLINE
ONLINE_THRESHOLD_SEC = 2.0
IDLE_THRESHOLD_SEC   = 10.0


# ── Camera image provider ──────────────────────────────────────────────────────
class CameraImageProvider(QQuickImageProvider):
    """Serves the latest annotated ZED camera frame to QML via image://soundvision/frame."""

    def __init__(self):
        super().__init__(QQuickImageProvider.ImageType.Image)
        self._lock = threading.Lock()
        self._image = QImage(640, 360, QImage.Format.Format_RGB888)
        self._image.fill(0)  # black placeholder

    def updateFrame(self, bgr_frame: np.ndarray):
        """Called from the ROS callback thread; converts BGR OpenCV frame to QImage."""
        rgb = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888).copy()
        with self._lock:
            self._image = qimg

    def requestImage(self, id_str, size, requested_size):
        with self._lock:
            return self._image.copy(), self._image.size()


# ── Voice command bridge ───────────────────────────────────────────────────────
class VoiceCommandBridge(QObject):
    """
    Subscribes to /voice/command topic and emits signals when the voice command changes.
    This allows the GUI to display the current voice command and update image subscriptions.
    """

    currentCommandChanged = Signal()

    def __init__(self, node: Node):
        super().__init__()
        self._node = node
        self._current_command = ""
        self._lock = threading.Lock()

        node.create_subscription(String, "/voice/command", self._voice_command_cb, 10)

    @Property(str, notify=currentCommandChanged)
    def currentCommand(self):
        with self._lock:
            return self._current_command

    def _voice_command_cb(self, msg: String):
        with self._lock:
            command = str(msg.data).strip()
            if command != self._current_command:
                self._current_command = command
                self.currentCommandChanged.emit()


# ── Dynamic image source bridge ────────────────────────────────────────────────
class DynamicImageSourceBridge(QObject):
    """
    Subscribes to both the search image and person follow annotated image topics.
    Switches which image to display based on the current voice command.
    - If voice command is "follow_me", display /person_follow_vision_node/annotated_image
    - If voice command is "search", display /zed/zed_node/rgb/image_rect_color with sound annotations
    - For any other voice command, display /zed/zed_node/rgb/image_rect_color without annotations
    """

    frameCountChanged = Signal()
    imageSourceChanged = Signal()

    _SEARCH_IMAGE_TOPIC = "/zed/zed_node/rgb/image_rect_color"
    _FOLLOW_IMAGE_TOPIC = "/person_follow_vision_node/annotated_image"

    def __init__(self, node: Node, image_provider: CameraImageProvider, voice_bridge: VoiceCommandBridge):
        super().__init__()
        self._node = node
        self._provider = image_provider
        self._voice_bridge = voice_bridge
        self._lock = threading.Lock()
        self._frame_count = 0
        self._current_image_topic = self._SEARCH_IMAGE_TOPIC
        self._current_command = ""
        self._use_annotation = False  # Flag to control whether to show annotations

        # Subscribe to both image topics
        self._search_image_sub = node.create_subscription(Image, self._SEARCH_IMAGE_TOPIC, self._search_image_cb, 1)
        self._follow_image_sub = node.create_subscription(Image, self._FOLLOW_IMAGE_TOPIC, self._follow_image_cb, 1)

        # Connect voice command changes
        voice_bridge.currentCommandChanged.connect(self._on_voice_command_changed)

    @Property(int, notify=frameCountChanged)
    def frameCount(self):
        with self._lock:
            return self._frame_count

    @Property(str, notify=imageSourceChanged)
    def currentImageSource(self):
        with self._lock:
            return self._current_image_topic

    @Slot()
    def _on_voice_command_changed(self):
        """Called when voice command changes; update which image stream to use."""
        command = self._voice_bridge.currentCommand
        with self._lock:
            if command != self._current_command:
                self._current_command = command
                # Switch image source and annotation mode based on command
                if command == "follow_me":
                    self._current_image_topic = self._FOLLOW_IMAGE_TOPIC
                    self._use_annotation = True
                elif command == "search":
                    self._current_image_topic = self._SEARCH_IMAGE_TOPIC
                    self._use_annotation = True
                else:
                    # For all other commands, show plain image without annotations
                    self._current_image_topic = self._SEARCH_IMAGE_TOPIC
                    self._use_annotation = False
                self.imageSourceChanged.emit()

    def _search_image_cb(self, msg: Image):
        """Process search image (ZED RGB camera feed, can have annotations depending on mode)."""
        if msg.encoding not in ("bgr8", "rgb8", "bgra8", "rgba8"):
            return

        arr = np.frombuffer(msg.data, dtype=np.uint8).reshape((msg.height, msg.width, -1))
        if msg.encoding == "rgb8":
            frame = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        elif msg.encoding == "bgra8":
            frame = cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)
        elif msg.encoding == "rgba8":
            frame = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
        else:
            frame = arr.copy()

        # Only update if this is the active source
        with self._lock:
            if self._current_image_topic == self._SEARCH_IMAGE_TOPIC:
                self._provider.updateFrame(frame)
                self._frame_count += 1
                self.frameCountChanged.emit()

    def _follow_image_cb(self, msg: Image):
        """Process follow image (annotated from person_follow_vision_node)."""
        if msg.encoding not in ("bgr8", "rgb8", "bgra8", "rgba8"):
            return

        arr = np.frombuffer(msg.data, dtype=np.uint8).reshape((msg.height, msg.width, -1))
        if msg.encoding == "rgb8":
            frame = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        elif msg.encoding == "bgra8":
            frame = cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)
        elif msg.encoding == "rgba8":
            frame = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
        else:
            frame = arr.copy()

        # Only update if this is the active source
        with self._lock:
            if self._current_image_topic == self._FOLLOW_IMAGE_TOPIC:
                self._provider.updateFrame(frame)
                self._frame_count += 1
                self.frameCountChanged.emit()


# ── Sound vision bridge ────────────────────────────────────────────────────────
class SoundVisionBridge(QObject):
    """
    Subscribes to the ZED camera image and /sound_localizer/current_estimate.
    Transforms the map-frame sound position into camera pixel coordinates via TF,
    draws a distance-scaled OpenCV circle marker, and signals QML to refresh.
    Only applies annotations when the voice command is "search".
    """

    frameCountChanged = Signal()

    _IMAGE_TOPIC    = "/zed/zed_node/rgb/image_rect_color"
    _CAMINFO_TOPIC  = "/zed/zed_node/rgb/camera_info"
    _ESTIMATE_TOPIC = "/sound_localizer/current_estimate"
    _ESTIMATE_STALE_S = 5.0

    def __init__(self, node: Node, image_provider: CameraImageProvider, voice_bridge: VoiceCommandBridge):
        super().__init__()
        self._node     = node
        self._provider = image_provider
        self._voice_bridge = voice_bridge
        self._lock     = threading.Lock()
        self._frame_count = 0

        # Camera intrinsics (populated from camera_info)
        self._fx = self._fy = self._cx = self._cy = None
        self._camera_frame: str | None = None

        # Latest sound estimate in map frame
        self._estimate_x: float | None = None
        self._estimate_y: float | None = None
        self._estimate_stamp = None

        self._tf_buf      = tf2_ros.Buffer(cache_time=Duration(seconds=10.0))
        self._tf_listener = tf2_ros.TransformListener(self._tf_buf, node)

        node.create_subscription(CameraInfo, self._CAMINFO_TOPIC, self._caminfo_cb, 1)
        node.create_subscription(Image,      self._IMAGE_TOPIC,   self._image_cb,   1)
        node.create_subscription(PoseStamped, self._ESTIMATE_TOPIC, self._estimate_cb, 10)

    @Property(int, notify=frameCountChanged)
    def frameCount(self):
        return self._frame_count

    def _caminfo_cb(self, msg: CameraInfo):
        with self._lock:
            self._fx = msg.k[0]
            self._fy = msg.k[4]
            self._cx = msg.k[2]
            self._cy = msg.k[5]
            self._camera_frame = msg.header.frame_id

    def _estimate_cb(self, msg: PoseStamped):
        with self._lock:
            self._estimate_x = msg.pose.position.x
            self._estimate_y = msg.pose.position.y
            self._estimate_stamp = self._node.get_clock().now()

    def _image_cb(self, msg: Image):
        if msg.encoding not in ("bgr8", "rgb8", "bgra8", "rgba8"):
            return

        arr = np.frombuffer(msg.data, dtype=np.uint8).reshape((msg.height, msg.width, -1))
        if msg.encoding == "rgb8":
            frame = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        elif msg.encoding == "bgra8":
            frame = cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)
        elif msg.encoding == "rgba8":
            frame = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
        else:
            frame = arr.copy()

        self._annotate_and_publish(frame)

    def _annotate_and_publish(self, frame: np.ndarray):
        # Only apply annotations if the voice command is "search"
        if self._voice_bridge.currentCommand != "search":
            # No annotation mode - just display the plain image
            self._provider.updateFrame(frame)
            self._frame_count += 1
            self.frameCountChanged.emit()
            return

        with self._lock:
            fx, fy, cx, cy   = self._fx, self._fy, self._cx, self._cy
            cam_frame         = self._camera_frame
            est_x, est_y      = self._estimate_x, self._estimate_y
            est_stamp         = self._estimate_stamp

        now = self._node.get_clock().now()
        have_estimate = (
            est_x is not None
            and est_stamp is not None
            and (now - est_stamp).nanoseconds / 1e9 < self._ESTIMATE_STALE_S
        )
        have_intrinsics = fx is not None and cam_frame is not None

        annotated = False
        if have_estimate and have_intrinsics:
            try:
                tf_stamped = self._tf_buf.lookup_transform(
                    cam_frame, "map", rclpy.time.Time())

                t  = tf_stamped.transform
                tx = t.translation.x
                ty = t.translation.y
                tz = t.translation.z
                qx, qy, qz, qw = t.rotation.x, t.rotation.y, t.rotation.z, t.rotation.w

                # Quaternion → rotation matrix
                R = np.array([
                    [1 - 2*(qy*qy + qz*qz), 2*(qx*qy - qz*qw), 2*(qx*qz + qy*qw)],
                    [2*(qx*qy + qz*qw),     1 - 2*(qx*qx + qz*qz), 2*(qy*qz - qx*qw)],
                    [2*(qx*qz - qy*qw),     2*(qy*qz + qx*qw), 1 - 2*(qx*qx + qy*qy)],
                ])

                p_map = np.array([est_x, est_y, 0.0])
                p_cam = R @ p_map + np.array([tx, ty, tz])
                X, Y, Z = p_cam

                if Z > 0.1:
                    u = int(fx * X / Z + cx)
                    v = int(fy * Y / Z + cy)
                    dist_m  = math.sqrt(X*X + Y*Y + Z*Z)
                    yaw_deg = math.degrees(math.atan2(X, Z))
                    radius  = max(15, int(fx * 0.25 / Z))

                    color = (0, 200, 255)
                    cv2.circle(frame, (u, v), radius, color, 3)
                    cv2.circle(frame, (u, v), 4, color, -1)
                    label = f"Sound  {dist_m:.1f}m  {yaw_deg:+.0f}deg"
                    text_y = max(20, v - radius - 8)
                    cv2.putText(
                        frame, label,
                        (max(0, u - radius), text_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                    cv2.putText(
                        frame, "SOUND LOCALIZED",
                        (20, 32),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                    annotated = True
                else:
                    cv2.putText(
                        frame, "SOUND BEHIND CAMERA",
                        (20, 32),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 100, 255), 2)
                    annotated = True

            except Exception:
                pass

        if not annotated:
            cv2.putText(
                frame, "NO SOUND ESTIMATE",
                (20, 32),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (60, 60, 60), 2)

        self._provider.updateFrame(frame)
        self._frame_count += 1
        self.frameCountChanged.emit()


# ── Health model ───────────────────────────────────────────────────────────────
class TopicHealthModel(QAbstractListModel):
    """Tracks live status (online / idle / offline) for each monitored topic."""

    AliasRole  = Qt.UserRole + 1
    TopicRole  = Qt.UserRole + 2
    StatusRole = Qt.UserRole + 3

    countsChanged = Signal()

    def __init__(self, node: Node):
        super().__init__()
        self._node = node
        self._data = [
            {"alias": t["alias"], "topic": t["topic"], "status": "offline"}
            for t in MONITORED_TOPICS
        ]
        self._last_received: dict = {t["topic"]: None for t in MONITORED_TOPICS}
        self._subscriptions = []
        self._online  = 0
        self._idle    = 0
        self._offline = len(MONITORED_TOPICS)
        self._setup_subscriptions()

    def _setup_subscriptions(self):
        for t in MONITORED_TOPICS:
            topic    = t["topic"]
            msg_type = t["msg_type"]

            def make_cb(tp):
                def cb(msg):
                    self._last_received[tp] = self._node.get_clock().now()
                return cb

            try:
                sub = self._node.create_subscription(msg_type, topic, make_cb(topic), 10)
                self._subscriptions.append(sub)
            except Exception as e:
                self._node.get_logger().warn(f"Could not subscribe to {topic}: {e}")

    # ── QAbstractListModel interface ──────────────────────────────────────────
    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._data):
            return None
        item = self._data[index.row()]
        if role == self.AliasRole:  return item["alias"]
        if role == self.TopicRole:  return item["topic"]
        if role == self.StatusRole: return item["status"]
        return None

    def roleNames(self):
        return {
            self.AliasRole:  b"alias",
            self.TopicRole:  b"topic",
            self.StatusRole: b"status",
        }

    # ── Summary count properties ──────────────────────────────────────────────
    @Property(int, notify=countsChanged)
    def onlineCount(self):
        return self._online

    @Property(int, notify=countsChanged)
    def idleCount(self):
        return self._idle

    @Property(int, notify=countsChanged)
    def offlineCount(self):
        return self._offline

    # ── Periodic refresh ──────────────────────────────────────────────────────
    @Slot()
    def refresh(self):
        now         = self._node.get_clock().now()
        data_changed = False
        online = idle = offline = 0

        for i, t in enumerate(MONITORED_TOPICS):
            last = self._last_received[t["topic"]]
            if last is None:
                new_status = "offline"
            else:
                elapsed = (now - last).nanoseconds / 1e9
                if elapsed < ONLINE_THRESHOLD_SEC:
                    new_status = "online"
                elif elapsed < IDLE_THRESHOLD_SEC:
                    new_status = "idle"
                else:
                    new_status = "offline"

            if new_status == "online":  online  += 1
            elif new_status == "idle":  idle    += 1
            else:                       offline += 1

            if self._data[i]["status"] != new_status:
                self._data[i]["status"] = new_status
                data_changed = True

        if data_changed:
            self.dataChanged.emit(self.index(0), self.index(len(self._data) - 1))

        if online != self._online or idle != self._idle or offline != self._offline:
            self._online  = online
            self._idle    = idle
            self._offline = offline
            self.countsChanged.emit()


# ── Anomaly bridge ─────────────────────────────────────────────────────────────
class AnomalyBridge(QObject):
    """
    Exposes anomaly counts to QML.
    The backend decides when to call addDetected(); the user (via the UI) marks
    anomalies as inspected.  A reset() clears both counters.
    """

    detectedChanged  = Signal()
    inspectedChanged = Signal()

    def __init__(self):
        super().__init__()
        self._detected  = 0
        self._inspected = 0

    @Property(int, notify=detectedChanged)
    def detected(self):
        return self._detected

    @Property(int, notify=inspectedChanged)
    def inspected(self):
        return self._inspected

    @Slot()
    def addDetected(self):
        """Increment the detected count (called from backend or test button)."""
        self._detected += 1
        self.detectedChanged.emit()

    @Slot()
    def addInspected(self):
        """Mark one more anomaly as inspected (cannot exceed detected count)."""
        if self._inspected < self._detected:
            self._inspected += 1
            self.inspectedChanged.emit()

    @Slot()
    def reset(self):
        """Reset both counters to zero."""
        self._detected  = 0
        self._inspected = 0
        self.detectedChanged.emit()
        self.inspectedChanged.emit()


# ── Command bridge ─────────────────────────────────────────────────────────────
class CommandBridge(QObject):
    """
    Exposes three mission-control actions to QML:
      • startBringup()         — launches mapping stack
      • startExploreAndInspect() — sends a Search action goal
      • emergencyStop()        — cancels goal + kills navigation processes

    searchStatus reflects live Search.Feedback.object_class (stage strings
    forwarded from ExploreUntilDetected, e.g. "exploring", "leak_detected", …).
    """

    bringupStatusChanged = Signal()
    searchStatusChanged  = Signal()
    searchActiveChanged  = Signal()

    def __init__(self, node: Node):
        super().__init__()
        self._node = node
        self._bringup_status  = "idle"
        self._search_status   = "idle"
        self._search_active   = False
        self._bringup_process = None
        self._search_goal_handle = None

        self._search_client = ActionClient(node, Search, "search")

        # TF buffer — populated via spin_once in the Qt timer loop
        self._tf_buf      = tf2_ros.Buffer(cache_time=Duration(seconds=10.0))
        self._tf_listener = tf2_ros.TransformListener(self._tf_buf, node)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _set_bringup(self, s: str):
        self._bringup_status = s
        self.bringupStatusChanged.emit()

    def _set_search(self, s: str, active: bool | None = None):
        self._search_status = s
        self.searchStatusChanged.emit()
        if active is not None and active != self._search_active:
            self._search_active = active
            self.searchActiveChanged.emit()

    # ── Properties ────────────────────────────────────────────────────────────
    @Property(str, notify=bringupStatusChanged)
    def bringupStatus(self):
        return self._bringup_status

    @Property(str, notify=searchStatusChanged)
    def searchStatus(self):
        return self._search_status

    @Property(bool, notify=searchActiveChanged)
    def searchActive(self):
        return self._search_active

    # ── Slots ─────────────────────────────────────────────────────────────────
    @Slot()
    def startBringup(self):
        """Launch ros2 launch go2_bringup mapping.launch.py in the background."""
        if self._bringup_process and self._bringup_process.poll() is None:
            return  # already running
        self._set_bringup("starting")

        def run():
            try:
                self._bringup_process = subprocess.Popen(
                    ["ros2", "launch", "go2_bringup", "mapping.launch.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                self._set_bringup("running")
                self._bringup_process.wait()
                rc = self._bringup_process.returncode
                # returncode -2 = SIGINT, -15 = SIGTERM (clean stop)
                self._set_bringup("stopped" if rc in (-2, -15) else "done")
            except Exception as exc:
                self._node.get_logger().error(f"Bringup failed: {exc}")
                self._set_bringup("failed")

        threading.Thread(target=run, daemon=True).start()

    @Slot()
    def startExploreAndInspect(self):
        """Send a Search action goal — equivalent to the voice 'look for a leak' command."""
        if self._search_active:
            return
        if not self._search_client.wait_for_server(timeout_sec=1.0):
            self._set_search("server unavailable", active=False)
            return

        goal = Search.Goal()
        goal.initial_pose = self._build_initial_pose()
        goal.behavior_tree = ""

        self._set_search("sending goal", active=True)
        future = self._search_client.send_goal_async(
            goal, feedback_callback=self._on_search_feedback
        )
        future.add_done_callback(self._on_goal_response)

    @Slot()
    def emergencyStop(self):
        """Cancel any active Search goal and kill all navigation processes."""
        # Cancel the Search action goal if one is active
        if self._search_goal_handle is not None:
            try:
                self._search_goal_handle.cancel_goal_async()
            except Exception:
                pass
            self._search_goal_handle = None

        # Terminate the stored bringup process
        if self._bringup_process and self._bringup_process.poll() is None:
            self._bringup_process.terminate()

        # Kill any lingering navigation launch processes
        for pattern in ["mapping.launch.py", "go2_deploy.launch.py", "nav2"]:
            subprocess.Popen(["pkill", "-SIGINT", "-f", pattern])

        self._set_bringup("stopped")
        self._set_search("canceled", active=False)

    # ── Internal callbacks ────────────────────────────────────────────────────
    def _build_initial_pose(self) -> PoseStamped:
        """Build a PoseStamped at the robot's current TF position."""
        pose = PoseStamped()
        pose.header.stamp    = self._node.get_clock().now().to_msg()
        pose.header.frame_id = "map"
        pose.pose.orientation.w = 1.0
        try:
            tf = self._tf_buf.lookup_transform("map", "base_link", rclpy.time.Time())
            pose.pose.position.x    = tf.transform.translation.x
            pose.pose.position.y    = tf.transform.translation.y
            pose.pose.position.z    = tf.transform.translation.z
            pose.pose.orientation.x = tf.transform.rotation.x
            pose.pose.orientation.y = tf.transform.rotation.y
            pose.pose.orientation.z = tf.transform.rotation.z
            pose.pose.orientation.w = tf.transform.rotation.w
        except Exception as exc:
            self._node.get_logger().warn(
                f"TF map->base_link unavailable, using origin: {exc}"
            )
        return pose

    def _on_search_feedback(self, feedback_msg) -> None:
        """Forward the stage string from Search.Feedback.object_class."""
        stage = str(feedback_msg.feedback.object_class)
        if stage:
            self._set_search(stage, active=True)

    def _on_goal_response(self, future) -> None:
        try:
            goal_handle = future.result()
        except Exception as exc:
            self._set_search("send error", active=False)
            self._node.get_logger().error(f"Search goal send error: {exc}")
            return

        if goal_handle is None or not goal_handle.accepted:
            self._set_search("goal rejected", active=False)
            return

        self._search_goal_handle = goal_handle
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._on_search_result)

    def _on_search_result(self, future) -> None:
        self._search_goal_handle = None
        try:
            wrapped = future.result()
        except Exception as exc:
            self._set_search("failed", active=False)
            self._node.get_logger().error(f"Search result error: {exc}")
            return

        if wrapped.status == GoalStatus.STATUS_SUCCEEDED:
            self._set_search("succeeded", active=False)
        elif wrapped.status == GoalStatus.STATUS_CANCELED:
            self._set_search("canceled", active=False)
        else:
            self._set_search("failed", active=False)


# ── ROS 2 node ─────────────────────────────────────────────────────────────────
class AmigoMonitorNode(Node):
    def __init__(self):
        super().__init__("amigo_monitor_node")


# ── Entry point ────────────────────────────────────────────────────────────────
def main():
    rclpy.init()
    node = AmigoMonitorNode()

    app    = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    health_model        = TopicHealthModel(node)
    anomaly_bridge      = AnomalyBridge()
    command_bridge      = CommandBridge(node)
    image_provider      = CameraImageProvider()
    voice_bridge        = VoiceCommandBridge(node)
    dynamic_image_bridge = DynamicImageSourceBridge(node, image_provider, voice_bridge)
    sound_vision_bridge = SoundVisionBridge(node, image_provider, voice_bridge)

    engine.addImageProvider("soundvision", image_provider)
    engine.rootContext().setContextProperty("healthModel",        health_model)
    engine.rootContext().setContextProperty("anomalyBridge",      anomaly_bridge)
    engine.rootContext().setContextProperty("commandBridge",      command_bridge)
    engine.rootContext().setContextProperty("soundVisionBridge",  sound_vision_bridge)
    engine.rootContext().setContextProperty("voiceCommandBridge", voice_bridge)
    engine.rootContext().setContextProperty("dynamicImageBridge", dynamic_image_bridge)

    # Refresh health status every second
    health_timer = QTimer()
    health_timer.timeout.connect(health_model.refresh)
    health_timer.start(1000)
    health_model.refresh()

    # Spin ROS2 callbacks
    ros_timer = QTimer()
    ros_timer.timeout.connect(lambda: rclpy.spin_once(node, timeout_sec=0))
    ros_timer.start(10)

    engine.load("main.qml")
    if not engine.rootObjects():
        sys.exit(-1)

    app.exec()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
