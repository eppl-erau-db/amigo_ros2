#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import OccupancyGrid, MapMetaData
from std_msgs.msg import Header

from go2_interfaces.srv import RegionMap

import yaml
import os
import numpy as np
import cv2  # For reading images and connected components

class RegionMapServiceNode(Node):
    def __init__(self):
        super().__init__('region_map_service_node')

        # PARAMETERS
        # 1) Map YAML file path
        self.declare_parameter('map_yaml_file', 'isaac_ros-dev/src/go2_description/maps/lab_partitioned.yaml')
        # 2) If True, also publish the masked map each time GET_CURRENT_REGION_MAP is called
        self.declare_parameter('publish_on_service_call', False)
        # 3) If True, continuously publish the masked map on a timer
        self.declare_parameter('continuous_publish', False)
        # 4) Publish rate in Hz if continuous_publish is True
        self.declare_parameter('publish_rate', 1.0)

        # Publisher for "current region only" masked map
        self.current_region_pub = self.create_publisher(
            OccupancyGrid, 
            'current_region_map',
            10
        )

        # Our custom service to return region info or full map
        self.service_ = self.create_service(
            RegionMap,
            'region_map_service',
            self.service_callback
        )

        # Subscribe to /amcl_pose to track robot's region
        self.amcl_pose_sub = self.create_subscription(
            PoseWithCovarianceStamped,
            '/amcl_pose',
            self.amcl_pose_callback,
            10
        )

        # Internals
        self.occupancy_grid_full = None
        self.region_id_map = None
        self.current_robot_region_id = -1

        self.resolution = None
        self.origin = None
        self.width = None
        self.height = None

        # Load map on startup
        self.load_region_map()

        # Start a timer if continuous publishing is requested
        continuous = self.get_parameter('continuous_publish').get_parameter_value().bool_value
        if continuous:
            publish_rate = self.get_parameter('publish_rate').get_parameter_value().double_value
            period = 1.0 / publish_rate if publish_rate > 0.0 else 1.0
            self.timer = self.create_timer(period, self.continuous_publish_cb)
            self.get_logger().info(f"Continuous publish enabled at {publish_rate} Hz")

    def load_region_map(self):
        """
        Loads the .yaml describing a 3-color (white/black/gray) grayscale .png,
        unifies black+gray => obstacle, runs connectedComponents to label free areas.
        """
        map_yaml_file = self.get_parameter('map_yaml_file').get_parameter_value().string_value
        if not os.path.exists(map_yaml_file):
            self.get_logger().error(f"Map yaml file does not exist: {map_yaml_file}")
            return

        # Parse YAML
        with open(map_yaml_file, 'r') as f:
            map_params = yaml.safe_load(f)

        image_path = map_params['image']
        resolution = float(map_params['resolution'])
        origin = map_params['origin']  # [x, y, theta]

        # If the image path is relative
        if not os.path.isabs(image_path):
            map_dir = os.path.dirname(map_yaml_file)
            image_path = os.path.join(map_dir, image_path)

        # Load grayscale image
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            self.get_logger().error(f"Failed to load image: {image_path}")
            return

        self.height, self.width = img.shape[:2]
        self.resolution = resolution
        self.origin = origin

        threshold_value = 200
        _, bin_img = cv2.threshold(img, threshold_value, 255, cv2.THRESH_BINARY)

        num_labels, label_image = cv2.connectedComponents(bin_img, connectivity=8)
        self.get_logger().info(f"Found {num_labels - 1} connected free-space regions")

        self.region_id_map = label_image

        # Build an OccupancyGrid
        occupancy_grid = OccupancyGrid()
        occupancy_grid.header.frame_id = 'map'
        metadata = MapMetaData()
        metadata.resolution = resolution
        metadata.width = self.width
        metadata.height = self.height
        metadata.origin.position.x = float(origin[0])
        metadata.origin.position.y = float(origin[1])
        occupancy_grid.info = metadata

        data = []
        for r in range(self.height):
            for c in range(self.width):
                px_val = bin_img[r, c]  # 0 or 255
                if px_val == 255:
                    data.append(0)   # free
                else:
                    data.append(100) # occupied
        occupancy_grid.data = data

        self.occupancy_grid_full = occupancy_grid

        self.get_logger().info(
            f"Loaded map from {image_path}, size: {self.width}x{self.height}, threshold={threshold_value}"
        )

    def amcl_pose_callback(self, msg: PoseWithCovarianceStamped):
        # If map not loaded yet, skip
        if self.occupancy_grid_full is None or self.region_id_map is None:
            return

        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        ox = self.origin[0]
        oy = self.origin[1]
        res = self.resolution

        col = int((x - ox) / res)
        row = int((y - oy) / res)
        row_in_image = (self.height - 1) - row

        if (row_in_image < 0 or row_in_image >= self.height or
            col < 0 or col >= self.width):
            self.get_logger().warn("Robot is out of map bounds!")
            return

        region_id = int(self.region_id_map[row_in_image, col])  # cast to int
        if region_id == 0:
            region_id = -1

        # If region changed, publish an updated masked map
        if region_id != self.current_robot_region_id:
            self.current_robot_region_id = region_id
            self.get_logger().info(f"Robot is now in region {region_id}")

            masked_map = self.create_masked_map(region_id)
            self.current_region_pub.publish(masked_map)

    def create_masked_map(self, region_id: int) -> OccupancyGrid:
        """
        Create an OccupancyGrid that blacks out everything except 'region_id'.
        region_id < 1 => fully blacked out
        """
        if self.occupancy_grid_full is None:
            return OccupancyGrid()

        masked = OccupancyGrid()
        masked.header = Header()
        masked.header.frame_id = 'map'
        masked.header.stamp = self.get_clock().now().to_msg()
        masked.info = self.occupancy_grid_full.info

        if region_id < 1:
            # black out entire map
            masked.data = [-1] * (self.width * self.height)
            return masked

        data = []
        for row in range(self.height):
            for col in range(self.width):
                label_val = int(self.region_id_map[(self.height - 1) - row, col])
                if label_val == region_id:
                    data.append(0)   # free
                else:
                    data.append(-1)  # unknown
        masked.data = data
        return masked

    def service_callback(self, request: RegionMap.Request, response: RegionMap.Response):
        cmd = request.command.upper()
        self.get_logger().info(f"Received RegionMap service request: {cmd}")

        current_id_int = int(self.current_robot_region_id)
        response.current_region_id = current_id_int
        response.success = True
        response.message = f"Current region is {current_id_int}"

        if cmd == "GET_CURRENT_REGION_MAP":
            if current_id_int < 1:
                response.success = False
                response.message = "Robot not in a valid free-space region"
            else:
                masked_map = self.create_masked_map(current_id_int)
                response.region_map = masked_map

                # Optionally publish on service call, if parameter is True
                publish_on_call = self.get_parameter('publish_on_service_call').get_parameter_value().bool_value
                if publish_on_call:
                    self.current_region_pub.publish(masked_map)

        elif cmd == "GET_FULL_MAP":
            if self.occupancy_grid_full is None:
                response.success = False
                response.message = "No map loaded"
            else:
                response.region_map = self.occupancy_grid_full

        else:
            response.success = False
            response.message = "Unknown command. Try GET_CURRENT_REGION_MAP or GET_FULL_MAP."

        return response

    def continuous_publish_cb(self):
        """
        Timer callback to continuously publish the current region map, if valid.
        """
        # If we're in a valid region (>0), publish it periodically
        if self.current_robot_region_id > 0:
            masked_map = self.create_masked_map(self.current_robot_region_id)
            self.current_region_pub.publish(masked_map)
        else:
            # If invalid region, optionally publish a fully blacked out map
            # or do nothing. For demonstration, let's do nothing:
            pass


def main(args=None):
    rclpy.init(args=args)
    node = RegionMapServiceNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
