#!/usr/bin/env python3
"""
map_marker_recorder_node — records ArUco marker positions during an "explore the
area" session and persists the SLAM map + marker table when asked.

While the mission supervisor reports ``task_mode == EXPLORE`` this node folds each
``/aruco/markers_map`` (map-frame MarkerArray) detection into a running per-marker
estimate. Entering EXPLORE starts a fresh session.

On ``SaveExploreMap`` (called by the supervisor when you say "we are done
exploring") it:
  * writes ``<maps_dir>/<name>.aruco.yaml``  (the marker table), and
  * triggers slam_toolbox ``save_map`` (occupancy grid .yaml/.pgm) and
    ``serialize_map`` (.posegraph/.data) under the same base path.

so the saved set can later be reloaded for "deliver swag".
"""
from __future__ import annotations

import os

import rclpy
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile
from std_msgs.msg import ColorRGBA, String
from visualization_msgs.msg import Marker, MarkerArray

from go2_interfaces.msg import RobotModeState
from go2_interfaces.srv import SaveExploreMap

from go2_control.aruco_map_store import MarkerAccumulator, save_markers

try:  # slam_toolbox Python service bindings (exec_depend); guard for degraded run
    from slam_toolbox.srv import SaveMap, SerializePoseGraph
    SLAM_SRV_AVAILABLE = True
except Exception as exc:  # pragma: no cover
    SaveMap = SerializePoseGraph = None
    SLAM_SRV_AVAILABLE = False
    _SLAM_IMPORT_ERROR = exc


class MapMarkerRecorderNode(Node):
    def __init__(self) -> None:
        super().__init__("map_marker_recorder_node")

        self.robot_mode_state_topic = str(self.declare_parameter(
            "robot_mode_state_topic", "/robot_mode_state").value)
        self.markers_topic = str(self.declare_parameter(
            "markers_topic", "/aruco/markers_map").value)
        self.maps_dir = os.path.expanduser(str(self.declare_parameter(
            "maps_dir", os.path.expanduser("~/amigo_maps")).value))
        self.default_map_name = str(self.declare_parameter("default_map_name", "venue").value)
        self.map_frame = str(self.declare_parameter("map_frame", "map").value)
        self.save_service_name = str(self.declare_parameter(
            "save_service_name", "/explore/save_map").value)
        self.slam_save_map_service = str(self.declare_parameter(
            "slam_save_map_service", "/slam_toolbox/save_map").value)
        self.slam_serialize_service = str(self.declare_parameter(
            "slam_serialize_service", "/slam_toolbox/serialize_map").value)
        self.record_when_idle = bool(self.declare_parameter("record_when_idle", False).value)
        self.recorded_markers_topic = str(self.declare_parameter(
            "recorded_markers_topic", "/aruco/recorded_markers").value)
        self.marker_viz_size_m = float(self.declare_parameter("marker_viz_size_m", 0.2).value)
        self.debug = bool(self.declare_parameter("debug", False).value)

        self._acc = MarkerAccumulator()
        self._recording = False
        self._prev_task_mode = ""

        # Persistent (latched) MarkerArray of every marker recorded so far, so RViz can show
        # where each ArUco was mapped even after it leaves the camera view. The detector's
        # /aruco/markers_map markers expire after ~1s; these stay until the session is reset.
        latched = QoSProfile(depth=1)
        latched.durability = DurabilityPolicy.TRANSIENT_LOCAL
        self._recorded_pub = self.create_publisher(
            MarkerArray, self.recorded_markers_topic, latched)

        self.create_subscription(
            RobotModeState, self.robot_mode_state_topic, self._mode_cb, 10)
        self.create_subscription(MarkerArray, self.markers_topic, self._markers_cb, 10)
        self._save_srv = self.create_service(
            SaveExploreMap, self.save_service_name, self._save_cb)

        self._save_map_client = None
        self._serialize_client = None
        if SLAM_SRV_AVAILABLE:
            self._save_map_client = self.create_client(SaveMap, self.slam_save_map_service)
            self._serialize_client = self.create_client(
                SerializePoseGraph, self.slam_serialize_service)
        else:  # pragma: no cover
            self.get_logger().warn(
                f"slam_toolbox srv bindings unavailable ({_SLAM_IMPORT_ERROR}); "
                "SaveExploreMap will write the marker sidecar only.")

        self.get_logger().info(
            f"map_marker_recorder_node ready. markers={self.markers_topic} "
            f"maps_dir={self.maps_dir} save_service={self.save_service_name} debug={self.debug}")

    # ------------------------------------------------------------------ inputs
    def _mode_cb(self, msg: RobotModeState) -> None:
        task = str(msg.task_mode)
        recording = task == "EXPLORE" or (self.record_when_idle and task == "IDLE")
        if task == "EXPLORE" and self._prev_task_mode != "EXPLORE":
            # New explore session — start a fresh marker table.
            self._acc = MarkerAccumulator()
            self.get_logger().info("Explore session started; recording ArUco markers.")
            self._publish_recorded()  # wipe any markers shown from a previous session
        if recording != self._recording:
            self._recording = recording
            self.get_logger().info(f"Marker recording {'ON' if recording else 'OFF'}.")
        self._prev_task_mode = task

    def _markers_cb(self, msg: MarkerArray) -> None:
        if not self._recording:
            return
        for m in msg.markers:
            p = m.pose.position
            o = m.pose.orientation
            est = self._acc.update(m.id, p.x, p.y, p.z, o.x, o.y, o.z, o.w)
            if self.debug:
                self.get_logger().info(
                    f"[recorder] marker {m.id}: ({est.x:.2f},{est.y:.2f}) n={est.samples} "
                    f"total_markers={self._acc.count()}",
                    throttle_duration_sec=1.0)
        if msg.markers:
            self._publish_recorded()

    def _publish_recorded(self) -> None:
        """Publish the running marker table as a persistent MarkerArray (CUBE + id label)
        so RViz shows where every ArUco has been mapped so far."""
        arr = MarkerArray()
        # Wipe the previous set first so a session reset / re-estimate doesn't leave ghosts.
        clear = Marker()
        clear.action = Marker.DELETEALL
        arr.markers.append(clear)
        now = self.get_clock().now().to_msg()
        for mid, est in sorted(self._acc.markers.items()):
            cube = Marker()
            cube.header.frame_id = self.map_frame
            cube.header.stamp = now
            cube.ns = "recorded_aruco"
            cube.id = int(mid)
            cube.type = Marker.CUBE
            cube.action = Marker.ADD
            cube.pose.position.x = float(est.x)
            cube.pose.position.y = float(est.y)
            cube.pose.position.z = float(est.z)
            cube.pose.orientation.x = float(est.qx)
            cube.pose.orientation.y = float(est.qy)
            cube.pose.orientation.z = float(est.qz)
            cube.pose.orientation.w = float(est.qw)
            cube.scale.x = cube.scale.y = self.marker_viz_size_m
            cube.scale.z = 0.02
            cube.color = ColorRGBA(r=0.1, g=0.8, b=1.0, a=0.9)
            arr.markers.append(cube)
            label = Marker()
            label.header.frame_id = self.map_frame
            label.header.stamp = now
            label.ns = "recorded_aruco_label"
            label.id = int(mid)
            label.type = Marker.TEXT_VIEW_FACING
            label.action = Marker.ADD
            label.pose.position.x = float(est.x)
            label.pose.position.y = float(est.y)
            label.pose.position.z = float(est.z) + 0.25
            label.pose.orientation.w = 1.0
            label.scale.z = 0.2
            label.color = ColorRGBA(r=1.0, g=1.0, b=1.0, a=1.0)
            label.text = f"id {int(mid)} (n={est.samples})"
            arr.markers.append(label)
        self._recorded_pub.publish(arr)

    # ------------------------------------------------------------------ save
    def _save_cb(self, request: SaveExploreMap.Request, response: SaveExploreMap.Response):
        name = str(request.map_name).strip() or self.default_map_name
        try:
            os.makedirs(self.maps_dir, exist_ok=True)
        except OSError as exc:
            response.success = False
            response.message = f"cannot create maps_dir {self.maps_dir}: {exc}"
            response.map_path = ""
            self.get_logger().error(response.message)
            return response

        base = os.path.join(self.maps_dir, name)
        sidecar = base + ".aruco.yaml"
        try:
            save_markers(sidecar, self._acc, self.map_frame)
        except Exception as exc:
            response.success = False
            response.message = f"failed to write marker sidecar {sidecar}: {exc}"
            response.map_path = ""
            self.get_logger().error(response.message)
            return response

        notes: list[str] = []
        # Trigger slam_toolbox saves fire-and-forget (avoid blocking this callback
        # waiting on another node's service); log the real results when they land.
        if self._save_map_client is not None and self._save_map_client.wait_for_service(timeout_sec=0.5):
            req = SaveMap.Request()
            req.name = String(data=base)
            self._save_map_client.call_async(req).add_done_callback(
                lambda fut: self._log_slam_result("save_map", fut))
        else:
            notes.append("slam save_map unavailable")

        if self._serialize_client is not None and self._serialize_client.wait_for_service(timeout_sec=0.5):
            req = SerializePoseGraph.Request()
            req.filename = base
            self._serialize_client.call_async(req).add_done_callback(
                lambda fut: self._log_slam_result("serialize_map", fut))
        else:
            notes.append("slam serialize_map unavailable")

        response.success = True
        response.map_path = base + ".yaml"
        response.message = (
            f"wrote {self._acc.count()} markers to {sidecar}"
            + (f"; map save triggered ({base}.yaml/.posegraph)" if not notes else "")
            + (("; " + ", ".join(notes)) if notes else "")
        )
        self.get_logger().info(response.message)
        return response

    def _log_slam_result(self, label: str, future) -> None:
        try:
            res = future.result()
            self.get_logger().info(f"slam {label} result={getattr(res, 'result', res)}")
        except Exception as exc:  # pragma: no cover
            self.get_logger().error(f"slam {label} failed: {exc}")


def main() -> None:
    rclpy.init()
    node = MapMarkerRecorderNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
