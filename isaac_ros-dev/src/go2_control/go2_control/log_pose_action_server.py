#!/usr/bin/env python3
"""
log_pose_action_server.py – stores way-points coming from RTAB-Map
"""
import json, rclpy
from rclpy.node   import Node
from rclpy.action import ActionServer
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped
from go2_interfaces.action import LogPose

class LogPoseActionServer(Node):

    def __init__(self):
        super().__init__('log_pose_action_server')

        # --- action server ------------------------------------------------
        self._action_server = ActionServer(
            self, LogPose, 'log_pose', self.execute_callback)

        # --- pose subscription -------------------------------------------
        self.current_pose = Pose()                # default until first msg
        self.pose_log     = []
        self.task_types   = []

        self.pose_sub = self.create_subscription(
            PoseWithCovarianceStamped,
            '/rtabmap/localization_pose',         # << was /slam_toolbox_pose
            self.pose_callback,
            10)

        self.get_logger().info('Log-pose action server ready (RTAB-Map pose)')

    # -- callbacks --------------------------------------------------------
    def pose_callback(self, msg: PoseWithCovarianceStamped):
        self.current_pose = msg.pose.pose        # keep only the Pose part

    async def execute_callback(self, goal_handle):
        self.get_logger().info(f'Logging pose – task: {goal_handle.request.task_type}')

        if self.current_pose == Pose():          # still uninitialised?
            self.get_logger().warn('Pose not received yet – aborting')
            goal_handle.abort()
            return LogPose.Result(success=False)

        # log & persist ---------------------------------------------------
        self.pose_log .append(self.current_pose)
        self.task_types.append(goal_handle.request.task_type)
        self.save_pose_log()

        goal_handle.succeed()
        return LogPose.Result(success=True)

    # -- helpers ----------------------------------------------------------
    def save_pose_log(self):
        data = [{
            'position'   : dict(x=p.position.x,  y=p.position.y,  z=p.position.z),
            'orientation': dict(x=p.orientation.x, y=p.orientation.y,
                                z=p.orientation.z, w=p.orientation.w),
            'task_type'  : self.task_types[i]
        } for i, p in enumerate(self.pose_log)]

        with open('pose_log.json', 'w') as f:
            json.dump(data, f, indent=4)

        self.get_logger().info('Pose log saved to pose_log.json')


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(LogPoseActionServer())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
