import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from go2_interfaces.action import LogPose
import sys

class LogPoseActionClient(Node):

    def __init__(self):
        super().__init__('log_pose_action_client')
        self._action_client = ActionClient(self, LogPose, 'log_pose')

    def send_goal(self, task_type):
        goal_msg = LogPose.Goal()
        goal_msg.task_type = task_type

        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        if result.success:
            self.get_logger().info('Goal succeeded')
        else:
            self.get_logger().info('Goal failed')

def main(args=None):
    rclpy.init(args=args)
    node = LogPoseActionClient()
    try:
        while rclpy.ok():
            task_type = input('Enter task type ("task" or "normal") or "exit" to quit: ')
            if task_type.lower() == 'exit':
                break
            if task_type not in ['task', 'normal']:
                print('Invalid input. Please enter "task" or "normal".')
                continue
            node.send_goal(task_type)
            rclpy.spin_once(node)
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()
