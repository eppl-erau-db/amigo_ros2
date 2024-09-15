import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from go2_interfaces.action import LogPose
import sys

class LogPoseActionClient(Node):

    def __init__(self):
        super().__init__('log_pose_action_client')
        self._action_client = ActionClient(self, LogPose, 'log_pose')

    def send_goal(self, current_map, task_type, switch_to_map=None, map_file_path=None):
        goal_msg = LogPose.Goal()
        goal_msg.current_map = current_map
        goal_msg.task_type = task_type
        if switch_to_map:
            goal_msg.switch_to_map = switch_to_map  # Include map_name if provided
        if map_file_path:
            goal_msg.map_file_path = map_file_path

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
            current_map = input('Enter current map name: ')
            task_type = input('Enter task type ("task", "normal" or "map_change") or "exit" to quit: ')
            if task_type.lower() == 'exit':
                break
            if task_type not in ['task', 'normal', 'map_change']:
                print('Invalid input. Please enter "task" or "normal" or "map_change".')
                continue

            switch_to_map = None
            map_file_path = None
            if task_type == 'map_change':
                switch_to_map = input('Enter map name: ')
                if not switch_to_map:
                    print('Map name cannot be empty for "map_change" task type.')
                    continue

            map_file_path = input('Enter map file path: ')
            if not map_file_path:
                print('Map file path cannot be empty for "map_change" task type.')
                continue

            node.send_goal(current_map, task_type, switch_to_map, map_file_path)

            rclpy.spin_once(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
