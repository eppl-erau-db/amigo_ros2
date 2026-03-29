import subprocess
import sys
import threading

import rclpy
import rclpy.time
import tf2_ros
from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import OccupancyGrid, Odometry
from rclpy.action import ActionClient
from rclpy.duration import Duration
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix, LaserScan, Imu, PointCloud2, JointState

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
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


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

    health_model    = TopicHealthModel(node)
    anomaly_bridge  = AnomalyBridge()
    command_bridge  = CommandBridge(node)

    engine.rootContext().setContextProperty("healthModel",    health_model)
    engine.rootContext().setContextProperty("anomalyBridge",  anomaly_bridge)
    engine.rootContext().setContextProperty("commandBridge",  command_bridge)

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
