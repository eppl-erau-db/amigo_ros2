#!/usr/bin/env python3
from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Optional

import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from nav_msgs.msg import OccupancyGrid, Path as NavPath
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.task import Future
from rclpy.time import Time
from std_msgs.msg import Bool, Int32
from tf2_ros import Buffer, TransformException, TransformListener

from go2_interfaces.action import LocalizeDetectedLeak


EPS = 1.0e-6


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

        self._goal_active = False
        self._map_msg: OccupancyGrid | None = None
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

        self.create_subscription(OccupancyGrid, self.map_topic, self._map_cb, 10)
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
            f'distance_ladder={self.candidate_distance_ladder_m}, '
            f'allow_unknown={self.allow_unknown}, '
            f'clearance_radius_m={self.clearance_radius_m:.2f}'
        )

    def _warn_throttled(self, key: str, message: str, period_s: float = 3.0) -> None:
        now_mono = time.monotonic()
        last_mono = self._warn_times_mono.get(key, 0.0)
        if (now_mono - last_mono) >= period_s:
            self._warn_times_mono[key] = now_mono
            self.get_logger().warn(message)

    def _map_cb(self, msg: OccupancyGrid) -> None:
        self._map_msg = msg

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

                if self._estimate_stable and self._latest_estimate is not None:
                    goal_handle.publish_feedback(
                        self._make_feedback('stable_estimate_found', fallback_pose)
                    )
                    goal_handle.succeed()
                    return self._make_result(True, 'stable_estimate_available', fallback_pose)

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
                candidates = self._generate_candidate_goals(
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
                        goal_handle.publish_feedback(
                            self._make_feedback('stable_estimate_found', goal_pose)
                        )
                        goal_handle.succeed()
                        return self._make_result(True, 'stable_estimate_available', goal_pose)
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
                        goal_handle.publish_feedback(
                            self._make_feedback('stable_estimate_found', goal_pose)
                        )
                        goal_handle.succeed()
                        return self._make_result(True, 'stable_estimate_available', goal_pose)
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
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
