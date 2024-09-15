import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped
from go2_interfaces.action import LogPose
import yaml
import os

class LogPoseActionServer(Node):

    def __init__(self):
        super().__init__('log_pose_action_server')
        self._action_server = ActionServer(
            self,
            LogPose,
            'log_pose',
            self.execute_callback)
        self.current_pose = Pose()  # Initialize with a default Pose object
        self.pose_subscription = self.create_subscription(
            PoseWithCovarianceStamped,
            '/slam_toolbox_pose',
            self.pose_callback,
            10
        )

    def pose_callback(self, msg):
        self.current_pose = msg.pose.pose

    async def execute_callback(self, goal_handle):
        current_map = goal_handle.request.current_map
        task_type = goal_handle.request.task_type
        switch_to_map = goal_handle.request.switch_to_map if goal_handle.request.switch_to_map else None
        map_file_path = goal_handle.request.map_file_path if goal_handle.request.map_file_path else None


        self.get_logger().info(f'Received goal: task_type={task_type}, current_map={current_map}, switch_to_map={switch_to_map}, map_file_path={map_file_path}')        
        # Check if the current_pose has been updated at least once
        if not self.pose_log and self.current_pose == Pose():
            self.get_logger().warn('Current pose is not available yet.')
            goal_handle.abort()
            return LogPose.Result(success=False)
        
        # Create or append to <current_map>_poses.yaml
        pose_log_filename = f'{current_map}_poses.yaml'

        # Create the pose entry
        pose_entry = {
            'position': {
                'x': self.current_pose.position.x,
                'y': self.current_pose.position.y,
                'z': self.current_pose.position.z
            },
            'orientation': {
                'x': self.current_pose.orientation.x,
                'y': self.current_pose.orientation.y,
                'z': self.current_pose.orientation.z,
                'w': self.current_pose.orientation.w
            },
            'task_type': task_type
        }

        # If task_type is 'map_change', add switch_to_map to pose_entry
        if task_type == 'map_change':
            pose_entry['switch_to_map'] = switch_to_map

        # Load existing data if file exists
        if os.path.exists(pose_log_filename):
            with open(pose_log_filename, 'r') as f:
                existing_data = yaml.safe_load(f) or []
        else:
            existing_data = []

        # Append the new pose entry
        existing_data.append(pose_entry)

        # Save back to the file
        with open(pose_log_filename, 'w') as f:
            yaml.dump(existing_data, f)

        self.get_logger().info(f'Pose logged to {pose_log_filename}')

        # If task_type is 'map_change', update map_info.yaml
        if task_type == 'map_change':
            if not switch_to_map or not map_file_path:
                self.get_logger().warn('switch_to_map and map_file_path must be provided for map_change task_type.')
                goal_handle.abort()
                return LogPose.Result(success=False)

            map_info_entry = {
                switch_to_map: {
                    'filepath': map_file_path
                }
            }
            map_info_filename = 'map_info.yaml'
            # Load existing map_info if exists
            if os.path.exists(map_info_filename):
                with open(map_info_filename, 'r') as f:
                    existing_map_info = yaml.safe_load(f) or {}
            else:
                existing_map_info = {}

            # Update the map_info
            existing_map_info.update(map_info_entry)

            # Save back to map_info.yaml
            with open(map_info_filename, 'w') as f:
                yaml.dump(existing_map_info, f)

            self.get_logger().info(f'Map info for {switch_to_map} saved to {map_info_filename}')

        goal_handle.succeed()
        return LogPose.Result(success=True)

def main(args=None):
    rclpy.init(args=args)
    node = LogPoseActionServer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
