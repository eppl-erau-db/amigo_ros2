import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator
import yaml
from ament_index_python.packages import get_package_share_directory
import os
import sys
import time
from robot_localization.srv import FromLL
from rclpy.node import Node
from go2_control.utils.gps_utils import latLonYaw2Geopose
from nav2_msgs.action import FollowWaypoints
from geometry_msgs.msg import PoseStamped


class YamlWaypointParser:
    """
    Parse a set of gps waypoints from a yaml file
    """

    def __init__(self, wps_file_path: str) -> None:
        with open(wps_file_path, 'r') as wps_file:
            self.wps_dict = yaml.safe_load(wps_file)

    def get_wps(self):
        """
        Get an array of geographic_msgs/msg/GeoPose objects from the yaml file
        """
        gepose_wps = []
        for wp in self.wps_dict["waypoints"]:
            latitude, longitude, yaw = wp["latitude"], wp["longitude"], wp["yaw"]
            gepose_wps.append(latLonYaw2Geopose(latitude, longitude, yaw))
        return gepose_wps


class GpsWpCommander(Node):
    """
    Class to use nav2 gps waypoint follower to follow a set of waypoints logged in a yaml file
    """

    def __init__(self, wps_file_path):
        super().__init__('minimal_client_async')
        self.navigator = BasicNavigator("bt_navigator")
        self.wp_parser = YamlWaypointParser(wps_file_path)
        self.localizer = self.create_client(FromLL,  '/fromLL')
        while not self.localizer.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')

    def start_wpf(self):
        """
        Function to start the waypoint following
        """
        self.navigator.waitUntilNav2Active(localizer='robot_localization')
        wps = self.wp_parser.get_wps()

        wpl = []
        for wp in wps:
            self.req = FromLL.Request()
            self.req.ll_point.longitude = wp.position.longitude
            self.req.ll_point.latitude = wp.position.latitude
            self.req.ll_point.altitude = wp.position.altitude

            log = 'long{:f}, lat={:f}, alt={:f}'.format(self.req.ll_point.longitude, self.req.ll_point.latitude, self.req.ll_point.altitude)
            self.get_logger().info(log)

            self.future = self.localizer.call_async(self.req)
            rclpy.spin_until_future_complete(self, self.future)

            self.resp = PoseStamped()
            self.resp.header.frame_id = 'map'
            self.resp.header.stamp = self.get_clock().now().to_msg()
            self.resp.pose.position = self.future.result().map_point

            log = 'x={:f}, y={:f}, z={:f}'.format(self.future.result().map_point.x, self.future.result().map_point.y, self.future.result().map_point.z)
            self.get_logger().info(log)
            
            self.resp.pose.orientation = wp.orientation
            wpl += [self.resp]

        self.navigator.followWaypoints(wpl)
        print("wps completed successfully")

def main():
    rclpy.init()

    # allow to pass the waypoints file as an argument
    default_yaml_file_path = os.path.join(get_package_share_directory(
        "go2_control"), "config", "demo_waypoints.yaml")
    if len(sys.argv) > 1:
        yaml_file_path = sys.argv[1]
    else:
        yaml_file_path = default_yaml_file_path

    gps_wpf = GpsWpCommander(yaml_file_path)
    gps_wpf.start_wpf()


if __name__ == "__main__":
    main()