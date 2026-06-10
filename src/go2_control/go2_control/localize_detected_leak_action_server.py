#!/usr/bin/env python3
from __future__ import annotations

import math
import os
import random
import subprocess
import time
from dataclasses import dataclass
from typing import Optional

import rclpy
from ament_index_python.packages import PackageNotFoundError, get_package_prefix
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from nav_msgs.msg import OccupancyGrid, Path as NavPath
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.duration import Duration
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from rclpy.task import Future
from rclpy.time import Time
from std_msgs.msg import Bool, Int32
from tf2_ros import Buffer, TransformException, TransformListener
from unitree_api.msg import Request as UnitreeRequest

from go2_control.localize_baseline_core import (
    perpendicular_baseline_component,
    perpendicular_fraction,
    rank_baseline_candidates,
)
from go2_control.person_follow_controller_core import (
    FootprintParams,
    GridMap2D,
    Pose2D,
    SafetyOracleParams,
    footprint_in_collision,
)
from go2_interfaces.action import LocalizeDetectedLeak


EPS = 1.0e-6
ROBOT_SPORT_API_ID_BALANCESTAND = 1002
ROBOT_SPORT_API_ID_STOPMOVE = 1003
ROBOT_SPORT_API_ID_STANDUP = 1004
ROBOT_SPORT_API_ID_SIT = 1009
ROBOT_SPORT_API_ID_RISESIT = 1010


@dataclass(frozen=True)
class RobotPose2D:
    x: float
    y: float
    yaw: float


@dataclass(frozen=True)
class CandidateGoal:
    heading_map_rad: float
    travel_distance_m: float
    achieved_perpendicular_baseline_m: float
    path_length_m: float
    goal_x: float
    goal_y: float
    endpoint_x: float
    endpoint_y: float
    # Signed move component along the leak bearing: > 0 toward the leak (forward),
    # < 0 away (the dog would reverse). Used to avoid rearward baseline treks.
    parallel_component_m: float = 0.0


@dataclass(frozen=True)
class ApproachGoalCandidate:
    goal_x: float
    goal_y: float
    goal_yaw: float
    radius_m: float
    offset_deg: float
    path_length_m: float


def wrap_pi(angle_rad: float) -> float:
    return math.atan2(math.sin(angle_rad), math.cos(angle_rad))


def yaw_from_quaternion(q) -> float:
    siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny_cosp, cosy_cosp)


class LocalizeDetectedLeakServer(Node):
    def __init__(self) -> None:
        super().__init__('localize_detected_leak_server')

        self.action_name = str(
            self.declare_parameter('action_name', 'localize_detected_leak').value
        )
        self.map_frame = str(self.declare_parameter('map_frame', 'map').value)
        self.base_frame = str(self.declare_parameter('base_frame', 'base_link').value)
        self.map_topic = str(self.declare_parameter('map_topic', '/map').value)
        self.leak_topic = str(self.declare_parameter('leak_topic', '/leak_detected').value)
        self.doa_topic = str(self.declare_parameter('doa_topic', '/doa_angle').value)
        self.estimate_valid_topic = str(
            self.declare_parameter(
                'estimate_valid_topic', '/sound_localizer/estimate_valid'
            ).value
        )
        self.estimate_stable_topic = str(
            self.declare_parameter(
                'estimate_stable_topic', '/sound_localizer/estimate_stable'
            ).value
        )
        self.estimate_topic = str(
            self.declare_parameter(
                'estimate_topic', '/sound_localizer/current_estimate'
            ).value
        )
        self.sport_request_topic = str(
            self.declare_parameter('sport_request_topic', '/api/sport/request').value
        )

        self.feedback_period_s = max(
            0.1, float(self.declare_parameter('feedback_period_s', 0.5).value)
        )
        self.localization_timeout_s = max(
            1.0, float(self.declare_parameter('localization_timeout_s', 90.0).value)
        )
        self.initial_bearing_timeout_s = max(
            1.0,
            float(self.declare_parameter('initial_bearing_timeout_s', 20.0).value),
        )
        self.post_navigation_wait_s = max(
            0.0, float(self.declare_parameter('post_navigation_wait_s', 2.0).value)
        )
        self.approach_goal_tolerance_m = max(
            0.05, float(self.declare_parameter('approach_goal_tolerance_m', 0.30).value)
        )
        raw_approach_radii = self.declare_parameter(
            'approach_radius_candidates_m', [0.0, 0.12, 0.20, 0.28]
        ).value
        self.approach_radius_candidates_m = sorted(
            {
                min(
                    self.approach_goal_tolerance_m,
                    max(0.0, float(radius)),
                )
                for radius in (raw_approach_radii or [0.0, 0.12, 0.20, 0.28])
            }
        )
        self.found_pose_hold_duration_s = max(
            0.0, float(self.declare_parameter('found_pose_hold_duration_s', 3.0).value)
        )
        self.release_to_stand_on_exit = bool(
            self.declare_parameter('release_to_stand_on_exit', True).value
        )
        self.sit_on_stable_estimate_without_final_approach = bool(
            self.declare_parameter(
                'sit_on_stable_estimate_without_final_approach', True
            ).value
        )
        self.max_motion_legs = max(
            1, int(self.declare_parameter('max_motion_legs', 3).value)
        )
        self.max_nav_goal_attempts_per_leg = max(
            1,
            int(self.declare_parameter('max_nav_goal_attempts_per_leg', 6).value),
        )
        self.target_perpendicular_baseline_m = max(
            0.1,
            float(
                self.declare_parameter(
                    'target_perpendicular_baseline_m', 1.0
                ).value
            ),
        )
        raw_distance_ladder = self.declare_parameter(
            'candidate_distance_ladder_m', [0.5, 0.75, 1.0, 1.25]
        ).value
        self.candidate_distance_ladder_m = sorted(
            {
                max(0.1, float(distance))
                for distance in (raw_distance_ladder or [0.5, 0.75, 1.0, 1.25])
            }
        )
        self.heading_step_deg = min(
            90.0,
            max(5.0, float(self.declare_parameter('heading_step_deg', 15.0).value)),
        )
        self.max_heading_offset_deg = min(
            90.0,
            max(
                self.heading_step_deg,
                float(self.declare_parameter('max_heading_offset_deg', 60.0).value),
            ),
        )
        self.occupied_threshold = int(
            self.declare_parameter('occupied_threshold', 50).value
        )
        self.allow_unknown = bool(self.declare_parameter('allow_unknown', True).value)
        self.clearance_radius_m = max(
            0.0, float(self.declare_parameter('clearance_radius_m', 0.55).value)
        )
        self.local_inflation_radius_m = max(
            0.0, float(self.declare_parameter('local_inflation_radius_m', 0.0).value)
        )
        self.global_inflation_radius_m = max(
            0.0, float(self.declare_parameter('global_inflation_radius_m', 0.0).value)
        )
        self.debug_search = bool(
            self.declare_parameter('debug_search', False).value
        )

        # --- Sampling-based baseline pose selection (doc eqs. 9-13) ---
        self.local_costmap_topic = str(
            self.declare_parameter(
                'local_costmap_topic', '/local_costmap/costmap'
            ).value
        )
        self.local_costmap_occupied_threshold = int(
            self.declare_parameter('local_costmap_occupied_threshold', 50).value
        )
        self.perp_baseline_target_m = max(
            0.1, float(self.declare_parameter('perp_baseline_target_m', 0.5).value)
        )
        self.weak_geometry_min_m = max(
            0.05,
            min(
                self.perp_baseline_target_m,
                float(self.declare_parameter('weak_geometry_min_m', 0.25).value),
            ),
        )
        self.sample_num = max(
            1, int(self.declare_parameter('sample_num', 80).value)
        )
        self.max_path_checks_per_leg = max(
            1, int(self.declare_parameter('max_path_checks_per_leg', 20).value)
        )
        self.sample_radius_m = max(
            0.5, float(self.declare_parameter('sample_radius_m', 1.5).value)
        )
        self.sample_min_radius_m = max(
            0.1,
            min(
                self.sample_radius_m,
                float(self.declare_parameter('sample_min_radius_m', 0.4).value),
            ),
        )
        self.costmap_clear_enabled = bool(
            self.declare_parameter('costmap_clear_enabled', True).value
        )
        self.costmap_repopulate_wait_s = max(
            0.0, float(self.declare_parameter('costmap_repopulate_wait_s', 1.0).value)
        )
        self.sample_seed = int(self.declare_parameter('sample_seed', 1).value)

        # --- Oriented-footprint feasibility check for the final-approach goal ---
        # _select_approach_goal's clearance check only scans a CIRCLE against the
        # static /map, which misses low obstacles (e.g. the leak source) that the
        # L1 lidar paints into the LOCAL costmap and that MPPI's ObstaclesCritic
        # (consider_footprint:true) refuses to drive onto. Without this, an approach
        # goal can be planner-valid yet footprint-infeasible -> the dog boxes itself
        # against it ("Failed to make progress" forever). Defaults MIRROR the Nav2
        # local_costmap footprint in nav2_mppi_controller.yaml ([[0.36,0.20],...]).
        self.approach_footprint_forward_m = max(
            0.05, float(self.declare_parameter('approach_footprint_forward_m', 0.36).value)
        )
        self.approach_footprint_rear_m = max(
            0.05, float(self.declare_parameter('approach_footprint_rear_m', 0.36).value)
        )
        self.approach_footprint_half_width_m = max(
            0.05, float(self.declare_parameter('approach_footprint_half_width_m', 0.20).value)
        )
        self.approach_footprint_padding_m = max(
            0.0, float(self.declare_parameter('approach_footprint_padding_m', 0.05).value)
        )
        self._approach_safety_params = SafetyOracleParams(
            occupied_threshold=self.local_costmap_occupied_threshold,
            footprint=FootprintParams(
                forward_extent_m=self.approach_footprint_forward_m,
                rear_extent_m=self.approach_footprint_rear_m,
                half_width_m=self.approach_footprint_half_width_m,
                padding_m=self.approach_footprint_padding_m,
            ),
        )

        # --- Recovery from the leak-found Sit (doc/SDK: RiseSit -> BalanceStand -> gait) ---
        self.rise_sit_settle_s = max(
            0.0, float(self.declare_parameter('rise_sit_settle_s', 1.5).value)
        )
        self.balance_settle_s = max(
            0.0, float(self.declare_parameter('balance_settle_s', 1.0).value)
        )
        self.gait_restore_enabled = bool(
            self.declare_parameter('gait_restore_enabled', True).value
        )
        self.gait_restore_network_interface = str(
            self.declare_parameter('gait_restore_network_interface', '').value
        )
        self.gait_restore_motion_mode = str(
            self.declare_parameter('gait_restore_motion_mode', 'normal').value
        )
        self.gait_restore_gait = str(
            self.declare_parameter('gait_restore_gait', 'static_walk').value
        )
        self.gait_restore_wait_s = max(
            0.0, float(self.declare_parameter('gait_restore_wait_s', 0.0).value)
        )
        self.gait_restore_retries = max(
            1, int(self.declare_parameter('gait_restore_retries', 4).value)
        )
        self.gait_restore_retry_interval_s = max(
            0.0,
            float(self.declare_parameter('gait_restore_retry_interval_s', 0.75).value),
        )

        self._rng = random.Random(self.sample_seed)
        self._motion_mode_switcher_executable = (
            self._resolve_motion_mode_switcher_executable()
        )

        self._goal_active = False
        self._map_msg: OccupancyGrid | None = None
        self._local_costmap_msg: OccupancyGrid | None = None
        self._leak_detected = False
        self._last_doa_rad: float | None = None
        self._last_doa_time_mono = 0.0
        self._estimate_valid = False
        self._estimate_stable = False
        self._latest_estimate: PoseStamped | None = None
        self._warn_times_mono: dict[str, float] = {}

        self.navigator = BasicNavigator()
        self.tf_buffer = Buffer(cache_time=Duration(seconds=10.0))
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.sport_req_pub = self.create_publisher(
            UnitreeRequest, self.sport_request_topic, 10
        )

        self.create_subscription(OccupancyGrid, self.map_topic, self._map_cb, 10)
        self.create_subscription(
            OccupancyGrid, self.local_costmap_topic, self._local_costmap_cb, 10
        )
        self.create_subscription(Bool, self.leak_topic, self._leak_cb, 10)
        self.create_subscription(Int32, self.doa_topic, self._doa_cb, 10)
        self.create_subscription(Bool, self.estimate_valid_topic, self._estimate_valid_cb, 10)
        self.create_subscription(Bool, self.estimate_stable_topic, self._estimate_stable_cb, 10)
        self.create_subscription(PoseStamped, self.estimate_topic, self._estimate_cb, 10)

        self._action_server = ActionServer(
            self,
            LocalizeDetectedLeak,
            self.action_name,
            execute_callback=self.execute_cb,
            goal_callback=self.goal_cb,
            cancel_callback=self.cancel_cb,
        )

        self.get_logger().info(
            'Localize-detected-leak action server ready: '
            f'action="{self.action_name}", map_topic="{self.map_topic}", '
            f'target_perpendicular_baseline_m={self.target_perpendicular_baseline_m:.2f}, '
            f'approach_goal_tolerance_m={self.approach_goal_tolerance_m:.2f}, '
            f'distance_ladder={self.candidate_distance_ladder_m}, '
            f'allow_unknown={self.allow_unknown}, '
            f'clearance_radius_m={self.clearance_radius_m:.2f}, '
            f'sport_request_topic="{self.sport_request_topic}"'
        )

    def _warn_throttled(self, key: str, message: str, period_s: float = 3.0) -> None:
        now_mono = time.monotonic()
        last_mono = self._warn_times_mono.get(key, 0.0)
        if (now_mono - last_mono) >= period_s:
            self._warn_times_mono[key] = now_mono
            self.get_logger().warn(message)

    def _map_cb(self, msg: OccupancyGrid) -> None:
        self._map_msg = msg

    def _local_costmap_cb(self, msg: OccupancyGrid) -> None:
        self._local_costmap_msg = msg

    def _resolve_motion_mode_switcher_executable(self) -> str | None:
        if not self.gait_restore_enabled:
            return None
        try:
            prefix = get_package_prefix('go2_driver')
        except PackageNotFoundError:
            self.get_logger().warn(
                'gait_restore_enabled=true, but package "go2_driver" was not found; '
                'gait will not be restored after the leak-found sit.'
            )
            return None
        executable = os.path.join(prefix, 'lib', 'go2_driver', 'go2_motion_mode_switcher')
        if not os.path.exists(executable):
            self.get_logger().warn(
                f'gait_restore_enabled=true, but "{executable}" is unavailable; '
                'gait will not be restored after the leak-found sit.'
            )
            return None
        return executable

    def _leak_cb(self, msg: Bool) -> None:
        self._leak_detected = bool(msg.data)

    def _doa_cb(self, msg: Int32) -> None:
        doa_deg = float(msg.data) % 360.0
        self._last_doa_rad = math.radians(doa_deg)
        self._last_doa_time_mono = time.monotonic()

    def _estimate_valid_cb(self, msg: Bool) -> None:
        self._estimate_valid = bool(msg.data)

    def _estimate_stable_cb(self, msg: Bool) -> None:
        self._estimate_stable = bool(msg.data)

    def _estimate_cb(self, msg: PoseStamped) -> None:
        self._latest_estimate = msg

    def goal_cb(self, goal_request: LocalizeDetectedLeak.Goal):
        del goal_request
        if self._goal_active:
            self.get_logger().warn(
                'Rejecting LocalizeDetectedLeak goal because another goal is already active.'
            )
            return GoalResponse.REJECT
        self.get_logger().info('LocalizeDetectedLeak goal received.')
        return GoalResponse.ACCEPT

    def cancel_cb(self, goal_handle):
        del goal_handle
        self.get_logger().info('LocalizeDetectedLeak cancel requested.')
        return CancelResponse.ACCEPT

    @staticmethod
    def _copy_pose_stamped(pose: PoseStamped) -> PoseStamped:
        copied = PoseStamped()
        copied.header = pose.header
        copied.pose = pose.pose
        return copied

    def _default_pose(self) -> PoseStamped:
        pose = PoseStamped()
        pose.header.frame_id = self.map_frame
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.orientation.w = 1.0
        return pose

    def _current_estimate_pose(self, fallback_pose: PoseStamped) -> PoseStamped:
        if self._latest_estimate is not None:
            return self._copy_pose_stamped(self._latest_estimate)
        return self._copy_pose_stamped(fallback_pose)

    def _make_result(self, success: bool, reason: str, fallback_pose: PoseStamped) -> LocalizeDetectedLeak.Result:
        result = LocalizeDetectedLeak.Result()
        result.success = bool(success)
        result.reason = str(reason)
        result.estimate_pose = self._current_estimate_pose(fallback_pose)
        return result

    def _make_feedback(self, stage: str, fallback_pose: PoseStamped) -> LocalizeDetectedLeak.Feedback:
        feedback = LocalizeDetectedLeak.Feedback()
        feedback.stage = str(stage)
        feedback.current_estimate = self._current_estimate_pose(fallback_pose)
        feedback.estimate_stable = bool(self._estimate_stable)
        return feedback

    def _log_debug(self, message: str) -> None:
        if self.debug_search:
            self.get_logger().info(f'[debug] {message}')

    async def _sleep_async(self, duration_s: float) -> None:
        if duration_s <= 0.0:
            return

        future: Future = Future()
        timer_box: dict[str, object] = {'timer': None, 'done': False}

        def _complete_sleep() -> None:
            if timer_box['done']:
                return
            timer_box['done'] = True
            if not future.done():
                future.set_result(True)

        timer_box['timer'] = self.create_timer(duration_s, _complete_sleep)
        try:
            await future
        finally:
            timer = timer_box.get('timer')
            if timer is not None:
                timer.cancel()
                self.destroy_timer(timer)

    def _lookup_robot_pose(self) -> RobotPose2D | None:
        try:
            tf_msg = self.tf_buffer.lookup_transform(
                self.map_frame,
                self.base_frame,
                Time(),
            )
        except TransformException as exc:
            self._warn_throttled(
                'tf_lookup',
                f'TF lookup {self.map_frame}->{self.base_frame} failed: {exc}',
            )
            return None

        translation = tf_msg.transform.translation
        yaw = yaw_from_quaternion(tf_msg.transform.rotation)
        return RobotPose2D(float(translation.x), float(translation.y), float(yaw))

    def _pose_stamped_from_xy_yaw(self, x: float, y: float, yaw: float) -> PoseStamped:
        pose = PoseStamped()
        pose.header.frame_id = self.map_frame
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = float(x)
        pose.pose.position.y = float(y)
        pose.pose.position.z = 0.0
        pose.pose.orientation.z = math.sin(yaw / 2.0)
        pose.pose.orientation.w = math.cos(yaw / 2.0)
        return pose

    def _publish_sport_request(self, api_id: int) -> None:
        request = UnitreeRequest()
        request.header.identity.api_id = int(api_id)
        self.sport_req_pub.publish(request)

    def _clear_all_costmaps(self, reason: str) -> None:
        try:
            self.navigator.clearAllCostmaps()
            self._log_debug(f'Cleared Nav2 costmaps before {reason}.')
        except Exception as exc:
            self._warn_throttled(
                'nav2_clear_costmaps',
                f'Failed to clear Nav2 costmaps before {reason}: {exc}',
                period_s=5.0,
            )

    @staticmethod
    def _distance_between_xy(x0: float, y0: float, x1: float, y1: float) -> float:
        return math.hypot(x1 - x0, y1 - y0)

    def _distance_to_estimate(
        self,
        robot_pose: RobotPose2D,
        estimate_pose: PoseStamped,
    ) -> float:
        return self._distance_between_xy(
            robot_pose.x,
            robot_pose.y,
            float(estimate_pose.pose.position.x),
            float(estimate_pose.pose.position.y),
        )

    def _select_approach_goal(
        self,
        robot_pose: RobotPose2D,
        estimate_pose: PoseStamped,
    ) -> PoseStamped | None:
        if self._map_msg is None:
            return None

        estimate_x = float(estimate_pose.pose.position.x)
        estimate_y = float(estimate_pose.pose.position.y)
        start_pose = self._pose_stamped_from_xy_yaw(
            robot_pose.x, robot_pose.y, robot_pose.yaw
        )
        base_angle = math.atan2(robot_pose.y - estimate_y, robot_pose.x - estimate_x)
        offset_candidates_deg = [0.0, -30.0, 30.0, -60.0, 60.0, -90.0, 90.0, 180.0]
        candidates: list[ApproachGoalCandidate] = []
        seen_keys: set[tuple[int, int]] = set()

        for radius_m in self.approach_radius_candidates_m:
            angles = [0.0] if radius_m <= EPS else offset_candidates_deg
            for offset_deg in angles:
                heading_rad = base_angle + math.radians(offset_deg)
                goal_x = estimate_x + (radius_m * math.cos(heading_rad))
                goal_y = estimate_y + (radius_m * math.sin(heading_rad))
                dedupe_key = (
                    int(round(goal_x * 100.0)),
                    int(round(goal_y * 100.0)),
                )
                if dedupe_key in seen_keys:
                    continue
                seen_keys.add(dedupe_key)

                clearance_ok, clearance_reason = self._point_has_clearance_status(
                    self._map_msg, goal_x, goal_y
                )
                if not clearance_ok:
                    self._log_debug(
                        'Rejected approach candidate for endpoint clearance: '
                        f'goal=({goal_x:.2f}, {goal_y:.2f}) '
                        f'radius={radius_m:.2f} m reason={clearance_reason}'
                    )
                    continue

                if radius_m <= EPS:
                    goal_yaw = math.atan2(
                        estimate_y - robot_pose.y,
                        estimate_x - robot_pose.x,
                    )
                else:
                    goal_yaw = math.atan2(estimate_y - goal_y, estimate_x - goal_x)
                goal_pose = self._pose_stamped_from_xy_yaw(goal_x, goal_y, goal_yaw)
                path = self._path_for_goal(start_pose, goal_pose)
                if path is None or not getattr(path, 'poses', []):
                    self._log_debug(
                        'Rejected approach candidate because Nav2 returned no path: '
                        f'goal=({goal_x:.2f}, {goal_y:.2f}) radius={radius_m:.2f} m'
                    )
                    continue

                if not self._goal_footprint_is_free(goal_x, goal_y, goal_yaw):
                    self._log_debug(
                        'Rejected approach candidate because the robot footprint '
                        'overlaps a LOCAL-costmap obstacle MPPI would refuse: '
                        f'goal=({goal_x:.2f}, {goal_y:.2f}) radius={radius_m:.2f} m'
                    )
                    continue

                candidates.append(
                    ApproachGoalCandidate(
                        goal_x=goal_x,
                        goal_y=goal_y,
                        goal_yaw=goal_yaw,
                        radius_m=radius_m,
                        offset_deg=offset_deg,
                        path_length_m=self._path_length(path),
                    )
                )

        if not candidates:
            return None

        candidates.sort(
            key=lambda candidate: (
                candidate.path_length_m,
                candidate.radius_m,
                abs(candidate.offset_deg),
            )
        )
        best = candidates[0]
        self._log_debug(
            'Selected approach goal: '
            f'goal=({best.goal_x:.2f}, {best.goal_y:.2f}) '
            f'radius={best.radius_m:.2f} m offset={best.offset_deg:.1f} deg '
            f'path={best.path_length_m:.2f} m'
        )
        return self._pose_stamped_from_xy_yaw(best.goal_x, best.goal_y, best.goal_yaw)

    async def _monitor_approach_navigation(
        self,
        goal_handle,
        approach_goal_pose: PoseStamped,
        estimate_pose: PoseStamped,
    ) -> str:
        while not self.navigator.isTaskComplete():
            if goal_handle.is_cancel_requested:
                await self._cancel_navigation()
                return 'canceled'

            robot_pose = self._lookup_robot_pose()
            if (
                robot_pose is not None
                and self._distance_to_estimate(robot_pose, estimate_pose)
                <= self.approach_goal_tolerance_m
            ):
                await self._cancel_navigation()
                return 'reached_estimate'

            goal_handle.publish_feedback(
                self._make_feedback('approaching_stable_estimate', approach_goal_pose)
            )
            await self._sleep_async(self.feedback_period_s)

        result = self.navigator.getResult()
        self._log_debug(f'Approach Nav2 task completed with result={result}.')
        if result == TaskResult.SUCCEEDED:
            robot_pose = self._lookup_robot_pose()
            if (
                robot_pose is not None
                and self._distance_to_estimate(robot_pose, estimate_pose)
                <= self.approach_goal_tolerance_m
            ):
                return 'reached_estimate'
            return 'goal_reached'
        if result == TaskResult.CANCELED:
            return 'canceled'
        return 'failed'

    async def _hold_after_sit(
        self,
        goal_handle,
        fallback_pose: PoseStamped,
    ) -> str:
        if self.found_pose_hold_duration_s <= 0.0:
            return 'completed'

        start_mono = time.monotonic()
        last_logged_remaining_s: int | None = None
        self.get_logger().info(
            'Leak found. Holding Sit for '
            f'{self.found_pose_hold_duration_s:.1f}s before RiseSit.'
        )

        while rclpy.ok():
            if goal_handle.is_cancel_requested:
                return 'canceled'

            elapsed_s = time.monotonic() - start_mono
            remaining_s = max(0.0, self.found_pose_hold_duration_s - elapsed_s)
            remaining_ceil_s = int(math.ceil(remaining_s))
            if remaining_ceil_s != last_logged_remaining_s:
                last_logged_remaining_s = remaining_ceil_s
                self.get_logger().info(
                    f'Leak-found hold countdown: {remaining_ceil_s}s remaining.'
                )

            if remaining_s <= 0.0:
                return 'completed'

            goal_handle.publish_feedback(
                self._make_feedback(
                    f'waiting_after_sit_{remaining_ceil_s}s',
                    fallback_pose,
                )
            )
            await self._sleep_async(min(self.feedback_period_s, max(0.05, remaining_s)))

        return 'canceled'

    async def _release_found_pose(self) -> None:
        """Recover from the leak-found Sit and restore a walk-ready stance.

        The Go2 SDK pairs Sit (1009) with RiseSit (1010) as its inverse; StandUp
        (1004) is NOT the correct recovery from a seated pose. After rising we
        settle into BalanceStand (1002) and then restore the walking gait via the
        go2_motion_mode_switcher (the same mechanism the mission supervisor uses
        for its stand-up recovery).
        """
        if not self.release_to_stand_on_exit:
            return
        self._publish_sport_request(ROBOT_SPORT_API_ID_RISESIT)
        self.get_logger().info('Sent RiseSit to recover from the leak-found sit.')
        await self._sleep_async(self.rise_sit_settle_s)
        self._publish_sport_request(ROBOT_SPORT_API_ID_BALANCESTAND)
        self.get_logger().info('Sent BalanceStand to settle after RiseSit.')
        await self._sleep_async(self.balance_settle_s)
        self._restore_gait()

    def _restore_gait(self) -> None:
        if not self.gait_restore_enabled or not self._motion_mode_switcher_executable:
            return
        command = [self._motion_mode_switcher_executable]
        if self.gait_restore_network_interface:
            command += ['--network-interface', self.gait_restore_network_interface]
        command += [
            '--motion-mode', self.gait_restore_motion_mode,
            '--gait', self.gait_restore_gait,
            '--wait', str(self.gait_restore_wait_s),
            '--retries', str(self.gait_restore_retries),
            '--retry-interval', str(self.gait_restore_retry_interval_s),
        ]
        self.get_logger().info(
            'Restoring gait after leak-found recovery: '
            f'motion_mode="{self.gait_restore_motion_mode}" '
            f'gait="{self.gait_restore_gait}".'
        )
        try:
            completed = subprocess.run(command, capture_output=True, text=True, timeout=30.0)
        except Exception as exc:
            self._warn_throttled(
                'gait_restore_failed',
                f'Gait restore subprocess failed to run: {exc}',
                period_s=5.0,
            )
            return
        if completed.returncode != 0:
            self._warn_throttled(
                'gait_restore_failed',
                f'Gait restore returned code {completed.returncode}: '
                f'{completed.stderr.strip()}',
                period_s=5.0,
            )

    async def _complete_found_leak_sequence(
        self,
        goal_handle,
        robot_pose: RobotPose2D,
        fallback_pose: PoseStamped,
    ) -> tuple[bool, str]:
        estimate_pose = self._current_estimate_pose(fallback_pose)
        distance_to_estimate_m = self._distance_to_estimate(robot_pose, estimate_pose)
        used_final_approach_fallback = False
        self.get_logger().info(
            'Stable leak estimate locked at '
            f'({estimate_pose.pose.position.x:.2f}, {estimate_pose.pose.position.y:.2f}). '
            f'Current robot distance is {distance_to_estimate_m:.2f} m.'
        )

        if distance_to_estimate_m > self.approach_goal_tolerance_m:
            goal_handle.publish_feedback(
                self._make_feedback('planning_approach_to_estimate', estimate_pose)
            )
            self._clear_all_costmaps('final approach planning')
            if self.costmap_clear_enabled:
                # Give the LOCAL costmap a beat to repopulate from the L1 lidar
                # after the clear, so _select_approach_goal's footprint check sees
                # the real obstacles instead of a momentarily-empty grid.
                await self._sleep_async(self.costmap_repopulate_wait_s)
            approach_goal_pose = self._select_approach_goal(robot_pose, estimate_pose)
            if approach_goal_pose is None:
                if not self.sit_on_stable_estimate_without_final_approach:
                    self.get_logger().warn(
                        'Stable leak estimate found, but no reachable approach goal '
                        f'within {self.approach_goal_tolerance_m:.2f} m was available.'
                    )
                    return False, 'stable_estimate_approach_unreachable'
                used_final_approach_fallback = True
                self.get_logger().warn(
                    'Stable leak estimate found, but no reachable approach goal '
                    f'within {self.approach_goal_tolerance_m:.2f} m was available. '
                    'Using Sit in place as the leak-found fallback signal.'
                )

            if approach_goal_pose is not None:
                try:
                    self.navigator.goToPose(approach_goal_pose)
                except Exception as exc:
                    self._warn_throttled(
                        'nav2_go_to_approach_pose',
                        f'Nav2 rejected the approach goal for the stable leak estimate: {exc}',
                        period_s=2.0,
                    )
                    if not self.sit_on_stable_estimate_without_final_approach:
                        return False, 'approach_goal_rejected'
                    used_final_approach_fallback = True
                    self.get_logger().warn(
                        'Approach goal was rejected by Nav2. '
                        'Using Sit in place as the leak-found fallback signal.'
                    )
                else:
                    approach_outcome = await self._monitor_approach_navigation(
                        goal_handle,
                        approach_goal_pose,
                        estimate_pose,
                    )
                    if approach_outcome == 'canceled':
                        return False, 'canceled'
                    if approach_outcome not in {'reached_estimate', 'goal_reached'}:
                        if not self.sit_on_stable_estimate_without_final_approach:
                            return False, 'approach_failed'
                        used_final_approach_fallback = True
                        self.get_logger().warn(
                            'Approach navigation failed before reaching the leak estimate. '
                            'Using Sit in place as the leak-found fallback signal.'
                        )

                    refreshed_pose = self._lookup_robot_pose()
                    if refreshed_pose is not None:
                        robot_pose = refreshed_pose
                    distance_to_estimate_m = self._distance_to_estimate(
                        robot_pose,
                        estimate_pose,
                    )
                    if distance_to_estimate_m > self.approach_goal_tolerance_m:
                        if not self.sit_on_stable_estimate_without_final_approach:
                            self.get_logger().warn(
                                'Approach navigation finished, but the robot is still '
                                f'{distance_to_estimate_m:.2f} m from the leak estimate '
                                f'(tolerance {self.approach_goal_tolerance_m:.2f} m).'
                            )
                            return False, 'approach_distance_not_met'
                        used_final_approach_fallback = True
                        self.get_logger().warn(
                            'Approach navigation finished, but the robot is still '
                            f'{distance_to_estimate_m:.2f} m from the leak estimate '
                            f'(tolerance {self.approach_goal_tolerance_m:.2f} m). '
                            'Using Sit in place as the leak-found fallback signal.'
                        )

        if used_final_approach_fallback and distance_to_estimate_m > self.approach_goal_tolerance_m:
            self.get_logger().info(
                'Issuing Sit as the leak-found fallback signal from '
                f'{distance_to_estimate_m:.2f} m away because the final approach '
                'could not be completed.'
            )
        else:
            self.get_logger().info(
                f'Robot is within {distance_to_estimate_m:.2f} m of the leak estimate. '
                'Issuing Sit as the leak-found signal.'
            )

        self._publish_sport_request(ROBOT_SPORT_API_ID_STOPMOVE)
        self._publish_sport_request(ROBOT_SPORT_API_ID_SIT)
        hold_outcome = await self._hold_after_sit(goal_handle, estimate_pose)
        await self._release_found_pose()

        if hold_outcome == 'canceled':
            return False, 'canceled'
        if used_final_approach_fallback:
            return True, 'leak_found_signal_complete_without_final_approach'
        return True, 'leak_found_signal_complete'

    async def _finish_found_leak_goal(
        self,
        goal_handle,
        robot_pose: RobotPose2D,
        fallback_pose: PoseStamped,
    ) -> LocalizeDetectedLeak.Result:
        success, reason = await self._complete_found_leak_sequence(
            goal_handle,
            robot_pose,
            fallback_pose,
        )
        if reason == 'canceled':
            goal_handle.canceled()
        else:
            goal_handle.publish_feedback(self._make_feedback(reason, fallback_pose))
            goal_handle.succeed()
        return self._make_result(success, reason, fallback_pose)

    def _fresh_map_bearing(self, robot_pose: RobotPose2D) -> float | None:
        if self._last_doa_rad is None:
            return None
        if (time.monotonic() - self._last_doa_time_mono) > self.initial_bearing_timeout_s:
            return None
        return wrap_pi(robot_pose.yaw + self._last_doa_rad)

    def _world_to_grid(
        self, map_msg: OccupancyGrid, x_map: float, y_map: float
    ) -> tuple[int, int] | None:
        info = map_msg.info
        res = float(info.resolution)
        origin = info.origin.position
        origin_yaw = yaw_from_quaternion(info.origin.orientation)

        dx = x_map - float(origin.x)
        dy = y_map - float(origin.y)
        cos_yaw = math.cos(-origin_yaw)
        sin_yaw = math.sin(-origin_yaw)
        local_x = (dx * cos_yaw) - (dy * sin_yaw)
        local_y = (dx * sin_yaw) + (dy * cos_yaw)

        ix = int(local_x / res)
        iy = int(local_y / res)
        if ix < 0 or iy < 0 or ix >= int(info.width) or iy >= int(info.height):
            return None
        return ix, iy

    def _cell_is_free(self, cell_value: int) -> bool:
        if cell_value < 0:
            return self.allow_unknown
        return cell_value < self.occupied_threshold

    def _point_has_clearance_status(
        self, map_msg: OccupancyGrid, x_map: float, y_map: float
    ) -> tuple[bool, str]:
        center = self._world_to_grid(map_msg, x_map, y_map)
        if center is None:
            return False, 'out_of_bounds'

        width = int(map_msg.info.width)
        height = int(map_msg.info.height)
        res = float(map_msg.info.resolution)
        radius_cells = int(math.ceil(self.clearance_radius_m / res))
        cx, cy = center

        for dy in range(-radius_cells, radius_cells + 1):
            for dx in range(-radius_cells, radius_cells + 1):
                if radius_cells > 0 and ((dx * dx) + (dy * dy)) > (radius_cells * radius_cells):
                    continue
                ix = cx + dx
                iy = cy + dy
                if ix < 0 or iy < 0 or ix >= width or iy >= height:
                    return False, 'out_of_bounds'
                cell_value = int(map_msg.data[(iy * width) + ix])
                if not self._cell_is_free(cell_value):
                    if cell_value < 0:
                        return False, 'unknown'
                    return False, f'occupied:{cell_value}'
        return True, 'clear'

    def _goal_footprint_is_free(
        self, goal_x: float, goal_y: float, goal_yaw: float
    ) -> bool:
        """True if the robot's ORIENTED footprint at the approach goal is clear of
        obstacles in the L1-fed LOCAL costmap. This complements the static-/map
        circular clearance check: the local costmap carries the low obstacles
        (leak source, supports, low walls) that MPPI's footprint ObstaclesCritic
        will refuse to drive onto. Degrades to True (allow) when the local costmap
        or its TF is unavailable, so selection falls back to the prior behavior."""
        grid_info = self._local_costmap_grid()
        if grid_info is None:
            return True
        grid, costmap_frame = grid_info
        tf = self._lookup_transform_2d(costmap_frame, self.map_frame)
        if tf is None:
            return True
        tx, ty, tyaw = tf
        cos_t, sin_t = math.cos(tyaw), math.sin(tyaw)
        ox = (cos_t * goal_x) - (sin_t * goal_y) + tx
        oy = (sin_t * goal_x) + (cos_t * goal_y) + ty
        pose = Pose2D(ox, oy, wrap_pi(goal_yaw + tyaw))
        return not footprint_in_collision(pose, grid, self._approach_safety_params)

    @staticmethod
    def _path_length(path: NavPath) -> float:
        if path is None or len(path.poses) < 2:
            return 0.0

        total = 0.0
        for previous, current in zip(path.poses[:-1], path.poses[1:]):
            dx = current.pose.position.x - previous.pose.position.x
            dy = current.pose.position.y - previous.pose.position.y
            total += math.hypot(dx, dy)
        return total

    @staticmethod
    def _perpendicular_baseline(
        start_pose: RobotPose2D,
        endpoint_x: float,
        endpoint_y: float,
        first_bearing_map_rad: float,
    ) -> float:
        dx = endpoint_x - start_pose.x
        dy = endpoint_y - start_pose.y
        distance = math.hypot(dx, dy)
        heading = math.atan2(dy, dx)
        return abs(math.sin(wrap_pi(heading - first_bearing_map_rad))) * distance

    def _candidate_heading_offsets_deg(self) -> list[float]:
        offsets_deg = [0.0]
        current = self.heading_step_deg
        while current <= (self.max_heading_offset_deg + EPS):
            offsets_deg.extend([-current, current])
            current += self.heading_step_deg
        return offsets_deg

    def _path_for_goal(self, start_pose: PoseStamped, goal_pose: PoseStamped):
        try:
            return self.navigator.getPath(start_pose, goal_pose)
        except Exception as exc:
            self._warn_throttled(
                'nav2_path_check',
                f'Nav2 path validation failed for candidate goal: {exc}',
                period_s=5.0,
            )
            return None

    def _generate_candidate_goals(
        self, robot_pose: RobotPose2D, first_bearing_map_rad: float
    ) -> list[CandidateGoal]:
        if self._map_msg is None:
            return []

        start_pose = self._pose_stamped_from_xy_yaw(
            robot_pose.x, robot_pose.y, robot_pose.yaw
        )
        seen_keys: set[tuple[int, int, int]] = set()
        candidates: list[CandidateGoal] = []
        preferred_headings = [
            wrap_pi(first_bearing_map_rad + (math.pi / 2.0)),
            wrap_pi(first_bearing_map_rad - (math.pi / 2.0)),
        ]

        for preferred_heading in preferred_headings:
            for offset_deg in self._candidate_heading_offsets_deg():
                heading_map_rad = wrap_pi(preferred_heading + math.radians(offset_deg))
                for travel_distance_m in self.candidate_distance_ladder_m:
                    goal_x = robot_pose.x + (travel_distance_m * math.cos(heading_map_rad))
                    goal_y = robot_pose.y + (travel_distance_m * math.sin(heading_map_rad))
                    dedupe_key = (
                        int(round(math.degrees(heading_map_rad) * 10.0)),
                        int(round(goal_x * 100.0)),
                        int(round(goal_y * 100.0)),
                    )
                    if dedupe_key in seen_keys:
                        continue
                    seen_keys.add(dedupe_key)

                    clearance_ok, clearance_reason = self._point_has_clearance_status(
                        self._map_msg, goal_x, goal_y
                    )
                    if not clearance_ok:
                        self._log_debug(
                            'Rejected candidate for endpoint clearance: '
                            f'heading={math.degrees(heading_map_rad):.1f} deg '
                            f'travel={travel_distance_m:.2f} m '
                            f'reason={clearance_reason}'
                        )
                        continue

                    goal_pose = self._pose_stamped_from_xy_yaw(
                        goal_x, goal_y, heading_map_rad
                    )
                    path = self._path_for_goal(start_pose, goal_pose)
                    if path is None or not getattr(path, 'poses', []):
                        self._log_debug(
                            'Rejected candidate because Nav2 returned no path: '
                            f'heading={math.degrees(heading_map_rad):.1f} deg '
                            f'travel={travel_distance_m:.2f} m'
                        )
                        continue

                    endpoint = path.poses[-1].pose.position
                    path_length_m = self._path_length(path)
                    achieved_baseline_m = self._perpendicular_baseline(
                        robot_pose,
                        float(endpoint.x),
                        float(endpoint.y),
                        first_bearing_map_rad,
                    )
                    candidates.append(
                        CandidateGoal(
                            heading_map_rad=heading_map_rad,
                            travel_distance_m=travel_distance_m,
                            achieved_perpendicular_baseline_m=achieved_baseline_m,
                            path_length_m=path_length_m,
                            goal_x=goal_x,
                            goal_y=goal_y,
                            endpoint_x=float(endpoint.x),
                            endpoint_y=float(endpoint.y),
                        )
                    )

        candidates.sort(
            key=lambda candidate: (
                -candidate.achieved_perpendicular_baseline_m,
                candidate.path_length_m,
                candidate.travel_distance_m,
            )
        )
        return candidates

    def _lookup_transform_2d(
        self, target_frame: str, source_frame: str
    ) -> tuple[float, float, float] | None:
        """Return (tx, ty, yaw) that maps a point in ``source_frame`` to ``target_frame``."""
        try:
            tf_msg = self.tf_buffer.lookup_transform(target_frame, source_frame, Time())
        except TransformException as exc:
            self._warn_throttled(
                f'tf_lookup_{target_frame}_{source_frame}',
                f'TF lookup {target_frame}<-{source_frame} failed: {exc}',
                period_s=3.0,
            )
            return None
        translation = tf_msg.transform.translation
        yaw = yaw_from_quaternion(tf_msg.transform.rotation)
        return float(translation.x), float(translation.y), yaw

    def _local_costmap_grid(self) -> tuple[GridMap2D, str] | None:
        msg = self._local_costmap_msg
        if msg is None:
            return None
        grid = GridMap2D(
            resolution=float(msg.info.resolution),
            width=int(msg.info.width),
            height=int(msg.info.height),
            origin_x=float(msg.info.origin.position.x),
            origin_y=float(msg.info.origin.position.y),
            data=tuple(int(value) for value in msg.data),
        )
        return grid, str(msg.header.frame_id) or self.map_frame

    async def _fetch_fresh_local_costmap(self) -> tuple[GridMap2D, str] | None:
        """Clear the local costmap to drop motion-smear, then return a fresh grid."""
        if self.costmap_clear_enabled:
            try:
                self.navigator.clearLocalCostmap()
            except Exception as exc:
                self._warn_throttled(
                    'nav2_clear_local_costmap',
                    f'Failed to clear the Nav2 local costmap before sampling: {exc}',
                    period_s=5.0,
                )
            await self._sleep_async(self.costmap_repopulate_wait_s)
        return self._local_costmap_grid()

    async def _sample_baseline_candidates(
        self, robot_pose: RobotPose2D, first_bearing_map_rad: float
    ) -> list[CandidateGoal]:
        """Sampling-based, geometry-aware baseline pose selection (doc eqs. 9-13).

        Samples free space from the (de-smeared) Nav2 local costmap, keeps poses
        that Nav2 can actually plan a path to, scores each by the perpendicular
        component of the net displacement relative to the leak bearing, and returns
        candidates ordered so the one with the largest usable perpendicular baseline
        (preferring those >= perp_baseline_target_m) is first. Falls back to the
        legacy deterministic generator if the local costmap / TF is unavailable.
        """
        fresh = await self._fetch_fresh_local_costmap()
        if fresh is None:
            self._warn_throttled(
                'no_local_costmap',
                'Local costmap unavailable; falling back to static-map baseline goals.',
                period_s=5.0,
            )
            return self._generate_candidate_goals(robot_pose, first_bearing_map_rad)

        grid, costmap_frame = fresh
        tf_odom_from_map = self._lookup_transform_2d(costmap_frame, self.map_frame)
        if tf_odom_from_map is None:
            return self._generate_candidate_goals(robot_pose, first_bearing_map_rad)
        tx, ty, tyaw = tf_odom_from_map
        cos_t, sin_t = math.cos(tyaw), math.sin(tyaw)

        # Phase 1: cheap costmap-only sampling of free poses + predicted geometry.
        # (pred_bperp, parallel, travel, gx, gy, heading)
        free_samples: list[tuple[float, float, float, float, float, float]] = []
        seen: set[tuple[int, int]] = set()
        r_min_sq = self.sample_min_radius_m ** 2
        r_max_sq = self.sample_radius_m ** 2
        cos_b, sin_b = math.cos(first_bearing_map_rad), math.sin(first_bearing_map_rad)
        for _ in range(self.sample_num * 6):
            if len(free_samples) >= self.sample_num:
                break
            radius = math.sqrt(self._rng.uniform(r_min_sq, r_max_sq))
            angle = self._rng.uniform(-math.pi, math.pi)
            gx = robot_pose.x + (radius * math.cos(angle))
            gy = robot_pose.y + (radius * math.sin(angle))
            key = (int(round(gx * 20.0)), int(round(gy * 20.0)))  # 0.05 m grid dedupe
            if key in seen:
                continue
            seen.add(key)
            # Map -> costmap (odom) frame for the free-space test.
            ox = (cos_t * gx) - (sin_t * gy) + tx
            oy = (sin_t * gx) + (cos_t * gy) + ty
            if grid.is_occupied(ox, oy, self.local_costmap_occupied_threshold):
                continue
            dx, dy = gx - robot_pose.x, gy - robot_pose.y
            pred_bperp = perpendicular_baseline_component(dx, dy, first_bearing_map_rad)
            parallel = (dx * cos_b) + (dy * sin_b)  # >0 toward leak (forward), <0 reverse
            travel = math.hypot(dx, dy)
            heading = math.atan2(dy, dx)
            free_samples.append((pred_bperp, parallel, travel, gx, gy, heading))

        # Per eq. 13 we want the SHORTEST move that still reaches the target, and we
        # prefer stepping toward the leak over reversing. So path-check the samples
        # that already predict >= target first, toward-leak first, shortest first.
        target = self.perp_baseline_target_m
        free_samples.sort(
            key=lambda s: (s[0] < target, s[1] < 0.0, s[2])  # meets-target, toward-leak, short
        )

        start_pose = self._pose_stamped_from_xy_yaw(
            robot_pose.x, robot_pose.y, robot_pose.yaw
        )
        candidates: list[CandidateGoal] = []
        path_checks = 0
        meeting_target = 0
        for pred_bperp, parallel, travel, gx, gy, heading in free_samples:
            if path_checks >= self.max_path_checks_per_leg:
                break
            if meeting_target >= 3:
                break
            goal_pose = self._pose_stamped_from_xy_yaw(gx, gy, heading)
            path_checks += 1
            path = self._path_for_goal(start_pose, goal_pose)
            if path is None or not getattr(path, 'poses', []):
                continue
            endpoint = path.poses[-1].pose.position
            ex, ey = float(endpoint.x), float(endpoint.y)
            achieved_baseline_m = self._perpendicular_baseline(
                robot_pose, ex, ey, first_bearing_map_rad
            )
            if achieved_baseline_m >= self.perp_baseline_target_m:
                meeting_target += 1
            parallel_component_m = (
                (ex - robot_pose.x) * cos_b + (ey - robot_pose.y) * sin_b
            )
            candidates.append(
                CandidateGoal(
                    heading_map_rad=heading,
                    travel_distance_m=travel,
                    achieved_perpendicular_baseline_m=achieved_baseline_m,
                    path_length_m=self._path_length(path),
                    goal_x=gx,
                    goal_y=gy,
                    endpoint_x=ex,
                    endpoint_y=ey,
                    parallel_component_m=parallel_component_m,
                )
            )

        ranked = rank_baseline_candidates(
            candidates, self.perp_baseline_target_m, self.weak_geometry_min_m
        )
        if ranked:
            best = ranked[0]
            disp = math.hypot(best.endpoint_x - robot_pose.x, best.endpoint_y - robot_pose.y)
            perp_pct = 100.0 * perpendicular_fraction(
                best.endpoint_x - robot_pose.x,
                best.endpoint_y - robot_pose.y,
                first_bearing_map_rad,
            )
            self.get_logger().info(
                'Baseline sampling: %d free / %d reachable samples; chose B_perp=%.2f m '
                '(%.0f%% perpendicular, travel=%.2f m, %s, target=%.2f m).'
                % (
                    len(free_samples),
                    len(candidates),
                    best.achieved_perpendicular_baseline_m,
                    perp_pct,
                    disp,
                    'toward-leak' if best.parallel_component_m >= 0.0 else 'reverse',
                    self.perp_baseline_target_m,
                )
            )
            if best.achieved_perpendicular_baseline_m < self.perp_baseline_target_m:
                self._warn_throttled(
                    'weak_baseline_geometry',
                    'Weak baseline geometry: best achievable B_perp='
                    f'{best.achieved_perpendicular_baseline_m:.2f} m < target '
                    f'{self.perp_baseline_target_m:.2f} m. Taking it and gathering '
                    'another measurement leg.',
                    period_s=3.0,
                )
        else:
            self._warn_throttled(
                'no_baseline_candidate',
                f'No reachable baseline candidate from {len(free_samples)} free samples '
                f'reached the weak-geometry minimum {self.weak_geometry_min_m:.2f} m.',
                period_s=3.0,
            )
        return ranked

    async def _cancel_navigation(self) -> None:
        try:
            self.navigator.cancelTask()
        except Exception:
            return
        await self._sleep_async(0.2)

    async def _monitor_navigation(
        self,
        goal_handle,
        navigation_target_pose: PoseStamped,
    ) -> str:
        while not self.navigator.isTaskComplete():
            if goal_handle.is_cancel_requested:
                await self._cancel_navigation()
                return 'canceled'

            if self._estimate_stable and self._latest_estimate is not None:
                await self._cancel_navigation()
                return 'stable_estimate_ready'

            goal_handle.publish_feedback(
                self._make_feedback('navigating_for_baseline', navigation_target_pose)
            )
            await self._sleep_async(self.feedback_period_s)

        result = self.navigator.getResult()
        self._log_debug(f'Nav2 task completed with result={result}.')
        if result == TaskResult.SUCCEEDED:
            return 'succeeded'
        if result == TaskResult.CANCELED:
            return 'canceled'
        return 'failed'

    async def _wait_for_stable_estimate(
        self,
        goal_handle,
        status_label: str,
        fallback_pose: PoseStamped,
        duration_s: float,
    ) -> str:
        deadline = time.monotonic() + duration_s
        while time.monotonic() < deadline:
            if goal_handle.is_cancel_requested:
                return 'canceled'
            if self._estimate_stable and self._latest_estimate is not None:
                return 'stable_estimate_ready'
            goal_handle.publish_feedback(
                self._make_feedback(status_label, fallback_pose)
            )
            await self._sleep_async(self.feedback_period_s)
        return 'timeout'

    async def execute_cb(self, goal_handle):
        self._goal_active = True
        start_mono = time.monotonic()
        fallback_pose = self._default_pose()
        first_bearing_map_rad: Optional[float] = None
        completed_legs = 0

        try:
            self.get_logger().info(
                'LocalizeDetectedLeak execution started. '
                f'map_available={self._map_msg is not None}, '
                f'leak_detected={self._leak_detected}, '
                f'estimate_valid={self._estimate_valid}, '
                f'estimate_stable={self._estimate_stable}'
            )
            while rclpy.ok():
                elapsed_s = time.monotonic() - start_mono
                if elapsed_s >= self.localization_timeout_s:
                    goal_handle.succeed()
                    return self._make_result(False, 'localization_timeout', fallback_pose)

                if goal_handle.is_cancel_requested:
                    await self._cancel_navigation()
                    goal_handle.canceled()
                    return self._make_result(False, 'canceled', fallback_pose)

                if not self._leak_detected:
                    self._warn_throttled(
                        'waiting_for_leak',
                        'LocalizeDetectedLeak is waiting for /leak_detected=true before planning motion.',
                        period_s=2.0,
                    )
                    goal_handle.publish_feedback(
                        self._make_feedback('waiting_for_leak', fallback_pose)
                    )
                    await self._sleep_async(self.feedback_period_s)
                    continue

                robot_pose = self._lookup_robot_pose()
                if robot_pose is None:
                    self._warn_throttled(
                        'waiting_for_pose',
                        f'LocalizeDetectedLeak is waiting for TF {self.map_frame}->{self.base_frame}.',
                        period_s=2.0,
                    )
                    goal_handle.publish_feedback(
                        self._make_feedback('waiting_for_pose', fallback_pose)
                    )
                    await self._sleep_async(self.feedback_period_s)
                    continue

                fallback_pose = self._pose_stamped_from_xy_yaw(
                    robot_pose.x, robot_pose.y, robot_pose.yaw
                )

                if self._estimate_stable and self._latest_estimate is not None:
                    goal_handle.publish_feedback(
                        self._make_feedback('stable_estimate_found', fallback_pose)
                    )
                    return await self._finish_found_leak_goal(
                        goal_handle,
                        robot_pose,
                        fallback_pose,
                    )

                if self._map_msg is None:
                    self._warn_throttled(
                        'waiting_for_map',
                        'LocalizeDetectedLeak is waiting for /map before generating Nav2 baseline goals.',
                        period_s=2.0,
                    )
                    goal_handle.publish_feedback(
                        self._make_feedback('waiting_for_map', fallback_pose)
                    )
                    await self._sleep_async(self.feedback_period_s)
                    continue

                current_bearing_map_rad = self._fresh_map_bearing(robot_pose)
                if current_bearing_map_rad is None:
                    doa_age_s = time.monotonic() - self._last_doa_time_mono
                    self._warn_throttled(
                        'waiting_for_bearing',
                        'LocalizeDetectedLeak is waiting for a fresh /doa_angle sample. '
                        f'age={doa_age_s:.2f}s timeout={self.initial_bearing_timeout_s:.2f}s',
                        period_s=2.0,
                    )
                    goal_handle.publish_feedback(
                        self._make_feedback('waiting_for_bearing', fallback_pose)
                    )
                    await self._sleep_async(self.feedback_period_s)
                    continue

                if first_bearing_map_rad is None:
                    first_bearing_map_rad = current_bearing_map_rad
                    self.get_logger().info(
                        'Captured first leak bearing for baseline planning: '
                        f'{math.degrees(first_bearing_map_rad):.1f} deg in map frame. '
                        f'robot_pose=({robot_pose.x:.2f}, {robot_pose.y:.2f}, '
                        f'{math.degrees(robot_pose.yaw):.1f} deg)'
                    )

                if completed_legs >= self.max_motion_legs:
                    goal_handle.succeed()
                    return self._make_result(False, 'no_stable_estimate', fallback_pose)

                goal_handle.publish_feedback(
                    self._make_feedback('planning_baseline', fallback_pose)
                )
                candidates = await self._sample_baseline_candidates(
                    robot_pose, first_bearing_map_rad
                )
                if self.debug_search:
                    preview = ', '.join(
                        (
                            f'{math.degrees(candidate.heading_map_rad):.0f}deg/'
                            f'{candidate.travel_distance_m:.2f}m/'
                            f'B={candidate.achieved_perpendicular_baseline_m:.2f}/'
                            f'path={candidate.path_length_m:.2f}'
                        )
                        for candidate in candidates[:5]
                    ) or 'none'
                    self.get_logger().info(
                        '[debug] candidate_ranking ' + preview
                    )
                if not candidates:
                    goal_handle.succeed()
                    return self._make_result(False, 'no_reachable_baseline_goal', fallback_pose)

                leg_succeeded = False
                attempted_candidates = 0
                for candidate in candidates[: self.max_nav_goal_attempts_per_leg]:
                    goal_pose = self._pose_stamped_from_xy_yaw(
                        candidate.goal_x,
                        candidate.goal_y,
                        candidate.heading_map_rad,
                    )
                    attempted_candidates += 1
                    self.get_logger().info(
                        'Baseline move %d/%d: heading=%.1f deg, travel=%.2f m, '
                        'B_perp=%.2f m, path_length=%.2f m'
                        % (
                            completed_legs + 1,
                            self.max_motion_legs,
                            math.degrees(candidate.heading_map_rad),
                            candidate.travel_distance_m,
                            candidate.achieved_perpendicular_baseline_m,
                            candidate.path_length_m,
                        )
                    )
                    self._log_debug(
                        'Sending Nav2 goal: '
                        f'goal=({candidate.goal_x:.2f}, {candidate.goal_y:.2f}, '
                        f'{math.degrees(candidate.heading_map_rad):.1f} deg), '
                        f'endpoint=({candidate.endpoint_x:.2f}, {candidate.endpoint_y:.2f}), '
                        f'baseline={candidate.achieved_perpendicular_baseline_m:.2f} m'
                    )

                    try:
                        self.navigator.goToPose(goal_pose)
                    except Exception as exc:
                        self._warn_throttled(
                            'nav2_go_to_pose',
                            f'Nav2 rejected baseline goal: {exc}',
                            period_s=2.0,
                        )
                        continue

                    nav_outcome = await self._monitor_navigation(goal_handle, goal_pose)
                    if nav_outcome == 'canceled':
                        goal_handle.canceled()
                        return self._make_result(False, 'canceled', fallback_pose)
                    if nav_outcome == 'stable_estimate_ready':
                        refreshed_pose = self._lookup_robot_pose() or robot_pose
                        return await self._finish_found_leak_goal(
                            goal_handle,
                            refreshed_pose,
                            goal_pose,
                        )
                    if nav_outcome != 'succeeded':
                        continue

                    leg_succeeded = True
                    completed_legs += 1
                    self.get_logger().info(
                        f'Baseline move {completed_legs}/{self.max_motion_legs} completed. '
                        f'Waiting {self.post_navigation_wait_s:.1f}s for a stable sound estimate.'
                    )
                    settle_outcome = await self._wait_for_stable_estimate(
                        goal_handle,
                        'waiting_for_stable_estimate',
                        goal_pose,
                        self.post_navigation_wait_s,
                    )
                    if settle_outcome == 'canceled':
                        goal_handle.canceled()
                        return self._make_result(False, 'canceled', goal_pose)
                    if settle_outcome == 'stable_estimate_ready':
                        refreshed_pose = self._lookup_robot_pose() or robot_pose
                        return await self._finish_found_leak_goal(
                            goal_handle,
                            refreshed_pose,
                            goal_pose,
                        )
                    break

                if not leg_succeeded:
                    if attempted_candidates == 0:
                        goal_handle.succeed()
                        return self._make_result(False, 'no_reachable_baseline_goal', fallback_pose)
                    goal_handle.succeed()
                    return self._make_result(False, 'nav_failed', fallback_pose)

            goal_handle.abort()
            return self._make_result(False, 'ros_shutdown', fallback_pose)
        finally:
            self._goal_active = False


def main() -> None:
    rclpy.init()
    node = LocalizeDetectedLeakServer()
    # Spin on a DEDICATED executor, not rclpy's global one. The embedded
    # nav2_simple_commander BasicNavigator calls rclpy.spin_until_future_complete()
    # internally (getPath / goToPose / isTaskComplete), and that uses the GLOBAL
    # executor. On Jazzy, if this node is also driven by the global executor
    # (rclpy.spin), the nested spin raises "Executor is already spinning" and every
    # path/goal request fails (the perpendicular-baseline candidates never validate).
    # Isolating this node onto its own executor leaves the global executor free for
    # the navigator's blocking calls.
    executor = SingleThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    finally:
        executor.shutdown()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
