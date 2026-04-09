#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseWithCovarianceStamped, Pose, PoseStamped
from nav_msgs.msg import OccupancyGrid, MapMetaData
from std_msgs.msg import Header

from go2_interfaces.srv import RegionMap

import yaml
import os
import numpy as np
import cv2  # For reading images and connected components

import tf2_ros
from tf2_ros import TransformException
from tf2_geometry_msgs import do_transform_pose
from rclpy.duration import Duration

class RegionMapServiceNode(Node):
    def __init__(self):
        super().__init__('region_map_service_node')

        # PARAMETERS
        self.declare_parameter('map_yaml_file', 'isaac_ros-dev/src/go2_description/maps/test_room.yaml')
        self.declare_parameter('publish_on_service_call', False)
        self.declare_parameter('continuous_publish', False)
        self.declare_parameter('publish_rate', 1.0)
        # New parameter: Only mark cells if the cost is at or above this threshold.
        self.declare_parameter('local_costmap_obstacle_threshold', 100)

        # Read threshold parameter into a member variable
        self.obstacle_threshold = self.get_parameter('local_costmap_obstacle_threshold').get_parameter_value().integer_value

        # Publisher for "current region only" masked map
        self.current_region_pub = self.create_publisher(
            OccupancyGrid, 
            'current_region_map',
            10
        )

        # Service to return region info or full map
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

        # Subscribe to the local costmap occupancy grid.
        self.local_costmap_sub = self.create_subscription(
            OccupancyGrid,
            '/local_costmap/costmap',
            self.local_costmap_callback,
            10
        )

        # Initialize tf2 buffer and listener for transforming frames.
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # Internals
        self.occupancy_grid_full = None
        self.region_id_map = None
        self.current_robot_region_id = -1

        self.resolution = None
        self.origin = None
        self.width = None
        self.height = None

        # Variable to store the most recent local costmap (after transformation to map frame)
        self.local_costmap = None

        # Load global map from YAML image.
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
        Loads the YAML that describes a 3-color grayscale image,
        unifies black+gray => obstacle, and uses connectedComponents to label free areas.
        """
        map_yaml_file = self.get_parameter('map_yaml_file').get_parameter_value().string_value
        if not os.path.exists(map_yaml_file):
            self.get_logger().error(f"Map yaml file does not exist: {map_yaml_file}")
            return

        with open(map_yaml_file, 'r') as f:
            map_params = yaml.safe_load(f)

        image_path = map_params['image']
        resolution = float(map_params['resolution'])
        origin = map_params['origin']  # Expected to be a list: [x, y, theta]

        if not os.path.isabs(image_path):
            map_dir = os.path.dirname(map_yaml_file)
            image_path = os.path.join(map_dir, image_path)

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

        # Build the global OccupancyGrid
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

    def local_costmap_callback(self, msg: OccupancyGrid):
        """
        Callback to update the most recent local costmap.
        Since the local costmap is published in the 'odom' frame,
        we transform its origin into the 'map' frame.
        """
        if msg.header.frame_id != "map":
            try:
                # Lookup the transform from the costmap's frame (e.g. "odom") to "map"
                transform = self.tf_buffer.lookup_transform(
                    "map",
                    msg.header.frame_id,
                    self.get_clock().now().to_msg(),
                    timeout=Duration(seconds=1.0)
                )
            except TransformException as ex:
                self.get_logger().warn(f"Transform failure: {ex}")
                return

            # Create a new Pose from the costmap's origin
            origin_pose = Pose()
            origin_pose.position.x = msg.info.origin.position.x
            origin_pose.position.y = msg.info.origin.position.y
            origin_pose.position.z = msg.info.origin.position.z
            origin_pose.orientation.x = msg.info.origin.orientation.x
            origin_pose.orientation.y = msg.info.origin.orientation.y
            origin_pose.orientation.z = msg.info.origin.orientation.z
            origin_pose.orientation.w = msg.info.origin.orientation.w

            # Create a PoseStamped using the new Pose
            pose_stamped = PoseStamped()
            pose_stamped.header.stamp = self.get_clock().now().to_msg()
            pose_stamped.header.frame_id = msg.header.frame_id
            pose_stamped.pose = origin_pose

            # WORKAROUND: Pass the contained pose to do_transform_pose
            transformed_pose = do_transform_pose(pose_stamped.pose, transform)
            msg.info.origin = transformed_pose
            msg.header.frame_id = "map"
            self.get_logger().debug("Transformed local costmap to map frame.")

        self.local_costmap = msg

    def amcl_pose_callback(self, msg: PoseWithCovarianceStamped):
        if self.occupancy_grid_full is None or self.region_id_map is None:
            return

        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        ox = self.origin[0]
        oy = self.origin[1]
        res = self.resolution

        col = int((x - ox) / res)
        row = int((y - oy) / res)
        # Adjust for the image coordinate system (row 0 is the bottom)
        row_in_image = (self.height - 1) - row

        if (row_in_image < 0 or row_in_image >= self.height or
            col < 0 or col >= self.width):
            self.get_logger().warn("Robot is out of map bounds!")
            return

        region_id = int(self.region_id_map[row_in_image, col])
        if region_id == 0:
            region_id = -1

        if region_id != self.current_robot_region_id:
            self.current_robot_region_id = region_id
            self.get_logger().info(f"Robot is now in region {region_id}")

            masked_map = self.create_masked_map(region_id)
            self.current_region_pub.publish(masked_map)

    def create_masked_map(self, region_id: int) -> OccupancyGrid:
        """
        Create an OccupancyGrid that blacks out everything except the given region.
        If region_id < 1, the entire map is blacked out.
        Overlays dynamic obstacles from the (transformed) local costmap.
        """
        if self.occupancy_grid_full is None:
            return OccupancyGrid()

        masked = OccupancyGrid()
        masked.header = Header()
        masked.header.frame_id = 'map'
        masked.header.stamp = self.get_clock().now().to_msg()
        masked.info = self.occupancy_grid_full.info

        if region_id < 1:
            masked.data = [-1] * (self.width * self.height)
            return masked

        data = []
        for row in range(self.height):
            for col in range(self.width):
                # Invert the row index to account for image coordinates
                label_val = int(self.region_id_map[(self.height - 1) - row, col])
                if label_val == region_id:
                    data.append(0)   # free
                else:
                    data.append(-1)  # masked out (unknown)
        masked.data = data

        # Overlay dynamic obstacles from the local costmap (if available)
        if self.local_costmap is not None:
            local_info = self.local_costmap.info
            local_data = self.local_costmap.data
            local_width = local_info.width
            local_height = local_info.height
            local_res = local_info.resolution
            local_origin_x = local_info.origin.position.x
            local_origin_y = local_info.origin.position.y

            # Iterate over each cell in the local costmap
            for i in range(local_height):
                for j in range(local_width):
                    local_index = i * local_width + j
                    cell_value = local_data[local_index]
                    # Only consider cells with cost at or above the obstacle threshold.
                    if cell_value >= self.obstacle_threshold:
                        # Compute the cell center coordinates in the world
                        world_x = local_origin_x + (j + 0.5) * local_res
                        world_y = local_origin_y + (i + 0.5) * local_res

                        # Map these coordinates to the global grid indices
                        global_col = int((world_x - self.origin[0]) / self.resolution)
                        global_row = int((world_y - self.origin[1]) / self.resolution)

                        if 0 <= global_col < self.width and 0 <= global_row < self.height:
                            global_index = global_row * self.width + global_col
                            # Only update if the cell is part of the current region (currently free)
                            if masked.data[global_index] == 0:
                                masked.data[global_index] = 100  # mark as occupied
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
        if self.current_robot_region_id > 0:
            masked_map = self.create_masked_map(self.current_robot_region_id)
            self.current_region_pub.publish(masked_map)

def main(args=None):
    rclpy.init(args=args)
    node = RegionMapServiceNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
