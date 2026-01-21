#!/usr/bin/env python3
"""
pose_click_logger.py — Click on a loaded map in RViz to build pose_log.json
First click = position, second click = heading.
Services:
  /save_pose_log (std_srvs/Trigger) -> writes pose_log.json
  /undo_last     (std_srvs/Trigger)
  /clear_poses   (std_srvs/Trigger)
Params:
  frame_id (default: "map")
  task_type (default: "task")
  outfile (default: "pose_log.json")
"""

import math, json
from typing import List, Optional

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import PointStamped, Pose, PoseStamped, Quaternion
from visualization_msgs.msg import Marker, MarkerArray
from std_srvs.srv import Trigger

def quat_from_yaw(yaw: float) -> Quaternion:
    # ZYX convention with only yaw: q = [0,0,sin(yaw/2), cos(yaw/2)]
    half = 0.5 * yaw
    return Quaternion(x=0.0, y=0.0, z=math.sin(half), w=math.cos(half))

class PoseClickLogger(Node):
    def __init__(self):
        super().__init__('pose_click_logger')

        self.frame_id = self.declare_parameter('frame_id', 'map').get_parameter_value().string_value
        self.task_type = self.declare_parameter('task_type', 'task').get_parameter_value().string_value
        self.outfile   = self.declare_parameter('outfile',  'pose_log.json').get_parameter_value().string_value

        self.poses: List[Pose] = []
        self._pending_pos: Optional[PointStamped] = None

        qos = QoSProfile(depth=10)
        self.click_sub  = self.create_subscription(PointStamped, '/clicked_point', self.on_click, qos)
        self.marker_pub = self.create_publisher(MarkerArray, 'pose_log_markers', 10)

        self.srv_save  = self.create_service(Trigger, 'save_pose_log',  self.on_save)
        self.srv_undo  = self.create_service(Trigger, 'undo_last',      self.on_undo)
        self.srv_clear = self.create_service(Trigger, 'clear_poses',    self.on_clear)

        self.get_logger().info(
            f"Ready. RViz: Publish Point → first click = position, second = heading. Frame='{self.frame_id}', outfile='{self.outfile}'"
        )

    def on_click(self, msg: PointStamped):
        if msg.header.frame_id and msg.header.frame_id != self.frame_id:
            self.get_logger().warn(f'Received point in frame "{msg.header.frame_id}", expected "{self.frame_id}". Using coordinates as-is.')

        if self._pending_pos is None:
            self._pending_pos = msg
            self.get_logger().info(f"Position set at ({msg.point.x:.2f}, {msg.point.y:.2f}). Click a second point to set heading.")
            self.publish_pending_marker(msg)
            return

        dx = msg.point.x - self._pending_pos.point.x
        dy = msg.point.y - self._pending_pos.point.y
        yaw = math.atan2(dy, dx) if (abs(dx) > 1e-6 or abs(dy) > 1e-6) else 0.0

        pose = Pose()
        pose.position.x = self._pending_pos.point.x
        pose.position.y = self._pending_pos.point.y
        pose.position.z = 0.0
        pose.orientation = quat_from_yaw(yaw)

        self.poses.append(pose)
        idx = len(self.poses)
        self.get_logger().info(f"Added pose #{idx}: ({pose.position.x:.2f}, {pose.position.y:.2f}), yaw={yaw:.2f} rad")
        self._pending_pos = None

        self.publish_all_markers()

    def publish_pending_marker(self, pos_msg: PointStamped):
        arr = MarkerArray()
        m = Marker()
        m.header.frame_id = self.frame_id
        m.ns = "pending"
        m.id = 9999
        m.type = Marker.SPHERE
        m.action = Marker.ADD
        m.pose.position.x = pos_msg.point.x
        m.pose.position.y = pos_msg.point.y
        m.pose.position.z = 0.0
        m.scale.x = m.scale.y = m.scale.z = 0.25
        m.color.a = 1.0
        m.color.r = 1.0; m.color.g = 0.8; m.color.b = 0.0
        arr.markers.append(m)
        self.marker_pub.publish(arr)

    def publish_all_markers(self):
        arr = MarkerArray()
        clear = Marker(); clear.action = Marker.DELETEALL; arr.markers.append(clear)

        for i, p in enumerate(self.poses):
            s = Marker()
            s.header.frame_id = self.frame_id
            s.ns = "poses"
            s.id = i
            s.type = Marker.SPHERE
            s.action = Marker.ADD
            s.pose.position.x = p.position.x
            s.pose.position.y = p.position.y
            s.pose.position.z = 0.0
            s.scale.x = s.scale.y = s.scale.z = 0.28
            s.color.a = 1.0
            s.color.r = 0.0; s.color.g = 1.0; s.color.b = 0.0
            arr.markers.append(s)

            a = Marker()
            a.header.frame_id = self.frame_id
            a.ns = "headings"
            a.id = 1000 + i
            a.type = Marker.ARROW
            a.action = Marker.ADD
            a.pose.position.x = p.position.x
            a.pose.position.y = p.position.y
            a.pose.position.z = 0.02
            a.pose.orientation = p.orientation
            a.scale.x = 0.6
            a.scale.y = 0.08
            a.scale.z = 0.12
            a.color.a = 1.0
            a.color.r = 0.2; a.color.g = 0.6; a.color.b = 1.0
            arr.markers.append(a)

            t = Marker()
            t.header.frame_id = self.frame_id
            t.ns = "labels"
            t.id = 2000 + i
            t.type = Marker.TEXT_VIEW_FACING
            t.action = Marker.ADD
            t.pose.position.x = p.position.x
            t.pose.position.y = p.position.y
            t.pose.position.z = 0.5
            t.scale.z = 0.3
            t.color.a = 1.0
            t.color.r = 1.0; t.color.g = 1.0; t.color.b = 1.0
            t.text = str(i + 1)
            arr.markers.append(t)

        self.marker_pub.publish(arr)

    def on_save(self, req, res):
        data = [{
            "position":   {"x": p.position.x, "y": p.position.y, "z": p.position.z},
            "orientation":{"x": p.orientation.x, "y": p.orientation.y, "z": p.orientation.z, "w": p.orientation.w},
            "task_type":  self.task_type
        } for p in self.poses]
        try:
            with open(self.outfile, 'w') as f:
                json.dump(data, f, indent=2)
            res.success = True
            res.message = f"Saved {len(self.poses)} poses to {self.outfile}"
        except Exception as e:
            res.success = False
            res.message = f"Failed to save: {e}"
        return res

    def on_undo(self, req, res):
        if self.poses:
            removed = self.poses.pop()
            self.publish_all_markers()
            res.success = True
            res.message = f'Undid pose at ({removed.position.x:.2f}, {removed.position.y:.2f})'
        else:
            res.success = False
            res.message = 'No poses to undo.'
        return res

    def on_clear(self, req, res):
        self.poses.clear()
        self.publish_all_markers()
        res.success = True
        res.message = 'Cleared all poses.'
        return res

def main():
    rclpy.init()
    rclpy.spin(PoseClickLogger())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
