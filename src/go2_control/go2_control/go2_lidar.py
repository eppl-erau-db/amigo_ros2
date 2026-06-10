#!/usr/bin/env python3
"""Self/ground-filtered republisher for the Go2 Unitree L1 lidar.

The raw L1 cloud sees the robot's own legs/body and the floor right next to the
feet. Fed straight into the Nav2 SpatioTemporalVoxelLayer those returns get
marked as lethal obstacles in a ring around the robot, so the local costmap shows
no clear space ahead and the controller refuses to move forward (or backs up).

This node subscribes to ``/utlidar/cloud_base`` -- the L1 cloud the Unitree
firmware has already transformed into ``base_link`` (it moves with the robot, so
no TF hop is needed and the geometry is correct) -- removes the points that fall
inside the robot's own body/leg envelope and the floor/overhead bands, and
republishes the survivors on ``/pointcloud`` for the costmap.

IMPORTANT: the self/ground filter assumes the input cloud is expressed in
``base_link`` (or a body-fixed frame with the same axes). ``/utlidar/cloud_base``
satisfies this; ``/utlidar/cloud`` (frame ``utlidar_lidar``) and
``/utlidar/cloud_deskewed`` (frame ``odom``) do NOT -- don't point ``input_topic``
at them without reworking the filter frame.
"""

import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2


class Go2LidarNode(Node):
    def __init__(self):
        super().__init__("go2_lidar")

        self.input_topic = str(
            self.declare_parameter("input_topic", "/utlidar/cloud_deskewed").value
        )
        self.output_topic = str(self.declare_parameter("output_topic", "pointcloud").value)
        self.output_frame = str(self.declare_parameter("output_frame", "base_link").value)

        # Self envelope in base_link (half-extents): drop points inside the robot's
        # trunk + leg footprint. Hips sit at x=+/-0.193, y=+/-0.047; standing feet
        # splay to ~y=+/-0.13, so +/-0.30 x +/-0.18 m covers the whole body/leg
        # envelope. (Footprint half-length is 0.36 m, so real obstacles within the
        # self box are inside the footprint anyway and are covered by the 2D /scan.)
        self.self_box_x = float(self.declare_parameter("self_box_x", 0.30).value)
        self.self_box_y = float(self.declare_parameter("self_box_y", 0.18).value)

        # Height band in base_link Z: drop the floor (and feet) below ground_clip_z
        # and overhead clutter above max_height_z. base_link sits ~0.30 m above the
        # floor, so -0.20 keeps obstacles taller than ~0.10 m and discards the floor.
        # Tune ground_clip_z up if the floor still marks, down to catch lower obstacles.
        self.ground_clip_z = float(self.declare_parameter("ground_clip_z", -0.20).value)
        self.max_height_z = float(self.declare_parameter("max_height_z", 0.60).value)

        self.go2_lidar_publisher = self.create_publisher(
            PointCloud2, self.output_topic, 10
        )
        self.go2_lidar_subscriber = self.create_subscription(
            PointCloud2, self.input_topic, self.go2_lidar_callback, 10
        )
        self.get_logger().info(
            "go2 lidar self/ground filter started: "
            f"in={self.input_topic} -> out={self.output_topic} (frame={self.output_frame}); "
            f"self_box=+/-{self.self_box_x}x+/-{self.self_box_y} m, "
            f"z=[{self.ground_clip_z}, {self.max_height_z}] m"
        )

    def go2_lidar_callback(self, msg):
        pts = point_cloud2.read_points(
            msg, field_names=("x", "y", "z"), skip_nans=True
        )
        if len(pts) == 0:
            return

        x = pts["x"]
        y = pts["y"]
        z = pts["z"]
        inside_self = (np.abs(x) < self.self_box_x) & (np.abs(y) < self.self_box_y)
        in_band = (z >= self.ground_clip_z) & (z <= self.max_height_z)
        keep = (~inside_self) & in_band

        xyz = np.column_stack((x[keep], y[keep], z[keep])).astype(np.float32)

        header = msg.header
        header.frame_id = self.output_frame
        new_msg = point_cloud2.create_cloud_xyz32(header, xyz)
        self.go2_lidar_publisher.publish(new_msg)


def main(args=None):
    rclpy.init(args=args)
    node = Go2LidarNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
