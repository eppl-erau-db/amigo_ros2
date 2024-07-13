#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from unitree_go.msg import LowState
from rclpy.qos import QoSProfile


class StatePublisherNode(Node):
    def __init__(self):
        super().__init__("state_publisher")
        qos_profile = QoSProfile(depth=10)
        self.joint_pub = self.create_publisher(JointState, 'joint_states', qos_profile)
        self.subscription = self.create_subscription(LowState, 'lowstate', self.lowstate_callback, qos_profile)
        self.get_logger().info("state publisher has started")

    def lowstate_callback(self, msg):
        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = [
            f'FL_hip_joint', f'FL_thigh_joint', f'FL_calf_joint',
            f'FR_hip_joint', f'FR_thigh_joint', f'FR_calf_joint',
            f'RL_hip_joint', f'RL_thigh_joint', f'RL_calf_joint',
            f'RR_hip_joint', f'RR_thigh_joint', f'RR_calf_joint',
        ]
        joint_state.position = [
            msg.motor_state[3].q, msg.motor_state[4].q, msg.motor_state[5].q,
            msg.motor_state[0].q, msg.motor_state[1].q, msg.motor_state[2].q,
            msg.motor_state[9].q, msg.motor_state[10].q, msg.motor_state[11].q,
            msg.motor_state[6].q, msg.motor_state[7].q, msg.motor_state[8].q,
        ]
        self.joint_pub.publish(joint_state)


def main(args=None):
    rclpy.init(args=args)
    node = StatePublisherNode()
    rclpy.spin(node=node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
