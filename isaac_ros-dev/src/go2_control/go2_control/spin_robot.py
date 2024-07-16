# my_robot_package/spin_robot.py

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from nav2_msgs.action import Spin
from rclpy.action import ActionClient
from geometry_msgs.msg import Quaternion
import math

class SpinRobot(Node):

    def __init__(self):
        super().__init__('spin_robot')
        self.subscription = self.create_subscription(
            Odometry,
            '/visual_slam/vis/slam_odometry',
            self.odom_callback,
            10)
        self.action_client = ActionClient(self, Spin, 'spin')
        self.goal_in_progress = False
        self.goal_sent = False  # Flag to track if the goal has been sent
        self.target_yaw_tolerance = 0.3  # Increased tolerance in radians for considering the goal achieved
        self.current_yaw = 0.0
        self.target_yaw = 0.0
        self.spin_completed = False  # Flag to track if the spin is completed
        self.get_logger().info('Node has been started.')

    def odom_callback(self, msg):
        orientation = msg.pose.pose.orientation
        self.current_yaw = self.quaternion_to_yaw(orientation)
        self.get_logger().info(f'Current Yaw: {self.current_yaw}')

        if self.goal_sent and not self.spin_completed:
            if abs(self.target_yaw - self.current_yaw) <= self.target_yaw_tolerance:
                self.get_logger().info('Target yaw achieved.')
                self.goal_in_progress = False
                self.goal_sent = False
                self.spin_completed = True  # Set the flag to indicate spin completion

    def quaternion_to_yaw(self, q: Quaternion):
        # Convert a quaternion to a yaw angle
        t3 = +2.0 * (q.w * q.z + q.x * q.y)
        t4 = +1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        yaw_z = math.atan2(t3, t4)
        return yaw_z

    def calculate_target_yaw(self, current_yaw):
        # Calculate target yaw 180 degrees from current yaw
        target_yaw = current_yaw + math.pi
        target_yaw = (target_yaw + math.pi) % (2 * math.pi) - math.pi
        return target_yaw

    def send_spin_goal(self, target_yaw):
        if not self.goal_in_progress:
            # Create a goal message for the Spin action
            goal_msg = Spin.Goal()
            goal_msg.target_yaw = target_yaw
            goal_msg.time_allowance.sec = 30  
            goal_msg.time_allowance.nanosec = 0

            self.action_client.wait_for_server()
            self.get_logger().info('Sending spin goal...')
            self.goal_in_progress = True
            self.goal_sent = True
            self.spin_completed = False  # Reset spin completed flag
            self._send_goal_future = self.action_client.send_goal_async(goal_msg)
            self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            self.goal_in_progress = False
            self.goal_sent = False
            return

        self.get_logger().info('Goal accepted')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Total elapsed time: {result.total_elapsed_time.sec} sec')
        self.goal_in_progress = False

def spin_180_degrees(spin_robot):
    target_yaw = spin_robot.calculate_target_yaw(spin_robot.current_yaw)
    spin_robot.send_spin_goal(target_yaw)
    while not spin_robot.spin_completed:
        rclpy.spin_once(spin_robot)
