import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped
from go2_interfaces.action import LogPose
import json

class LogPoseActionServer(Node):

    def __init__(self):
        super().__init__('log_pose_action_server')
        self._action_server = ActionServer(
            self,
            LogPose,
            'log_pose',
            self.execute_callback)
        self.pose_log = []
        self.task_types = []
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
        self.get_logger().info(f'Starting to log pose with task type: {goal_handle.request.task_type}')
        
        # Check if the current_pose has been updated at least once
        if not self.pose_log and self.current_pose == Pose():
            self.get_logger().warn('Current pose is not available yet.')
            goal_handle.abort()
            return LogPose.Result(success=False)

        # Log the current pose
        self.pose_log.append(self.current_pose)
        self.task_types.append(goal_handle.request.task_type)

        # Save the current pose log to a file
        self.save_pose_log()

        # Print the current pose log
        # self.get_logger().info('Current Pose Log:')
        # for i, pose in enumerate(self.pose_log):
        #     self.get_logger().info(f'Pose {i+1}: Position(x={pose.position.x}, y={pose.position.y}, z={pose.position.z}), '
        #                            f'Orientation(x={pose.orientation.x}, y={pose.orientation.y}, z={pose.orientation.z}, w={pose.orientation.w})')

        goal_handle.succeed()
        return LogPose.Result(success=True)

    def save_pose_log(self):
        data = []
        for i, pose in enumerate(self.pose_log):
            data.append({
                'position': {
                    'x': pose.position.x,
                    'y': pose.position.y,
                    'z': pose.position.z
                },
                'orientation': {
                    'x': pose.orientation.x,
                    'y': pose.orientation.y,
                    'z': pose.orientation.z,
                    'w': pose.orientation.w
                },
                'task_type': self.task_types[i]
            })
        with open('pose_log.json', 'w') as f:
            json.dump(data, f, indent=4)
        self.get_logger().info('Pose log saved to pose_log.json')

def main(args=None):
    rclpy.init(args=args)
    node = LogPoseActionServer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
