#!/usr/bin/env python3

## code not properly working ##
## coede used to visualize the the current section of the occupancy grid map as a .png file for debugging ##
import rclpy
from rclpy.node import Node
import numpy as np
import cv2

from nav_msgs.msg import OccupancyGrid

class OccupancyGridToImageNode(Node):
    def __init__(self):
        super().__init__('occupancy_grid_to_image')

        # Subscribe to the OccupancyGrid topic you want to visualize
        self.subscription = self.create_subscription(
            OccupancyGrid,
            '/current_region_map',  # or your masked map topic
            self.occ_callback,
            10
        )

    def occ_callback(self, msg: OccupancyGrid):
        width = msg.info.width
        height = msg.info.height
        data = np.array(msg.data, dtype=np.int8).reshape((height, width))

        # Convert to a grayscale image
        # -1 => unknown => 127
        #  0 => free => 255
        # 100 => occupied => 0

        img = np.zeros((height, width), dtype=np.uint8)
        for r in range(height):
            for c in range(width):
                val = data[r, c]
                if val < 0:
                    img[r, c] = 127     # unknown
                elif val == 0:
                    img[r, c] = 255     # free
                else:
                    img[r, c] = 0       # occupied

        # The occupancy grid is typically stored from the top row to bottom row,
        # or vice versa depending on your usage. If you see it flipped,
        # you can flip vertically:
        img = np.flipud(img)

        # (Optional) Save to disk for debugging
        cv2.imwrite('masked_map_debug.png', img)
        self.get_logger().info('Saved masked_map_debug.png')

        # Or display it in a window (if you have a GUI):
        cv2.imshow('Masked Occupancy', img)
        cv2.waitKey(1)

        # After one save, you can unsubscribe if you only need one image
        self.destroy_subscription(self.subscription)


def main(args=None):
    rclpy.init(args=args)
    node = OccupancyGridToImageNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
