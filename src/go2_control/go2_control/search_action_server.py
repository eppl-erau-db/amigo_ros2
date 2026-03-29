#!/usr/bin/env python3
from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Optional

import rclpy
from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseStamped
from rclpy.action import ActionClient, ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from rclpy.task import Future
from std_msgs.msg import Bool, String

from go2_interfaces.action import ExploreUntilDetected, LocalizeDetectedLeak, Search


ERROR_NONE = 0
ERROR_TIMEOUT = 1
ERROR_CANCELED = 2
ERROR_NO_LEAK_FOUND = 3
ERROR_PHASE_UNAVAILABLE = 4
ERROR_PHASE_FAILED = 5


@dataclass
class PhaseExecutionResult:
    state: str
    phase_name: str
    result: object | None = None
    status: int | None = None
    last_stage: str = ''
    last_estimate: PoseStamped | None = None
    detail: str = ''


class LeakSearchMissionCoordinator(Node):
    def __init__(self) -> None:
        super().__init__('leak_search_server')

        self.search_action_name = str(
            self.declare_parameter('search_action_name', 'search').value
        )
        self.explore_action_name = str(
            self.declare_parameter('explore_action_name', 'explore_until_detected').value
        )
        self.localize_action_name = str(
            self.declare_parameter('localize_action_name', 'localize_detected_leak').value
        )
        self.feedback_period_s = max(
            0.1, float(self.declare_parameter('feedback_period_s', 0.5).value)
        )
        self.search_timeout_s = max(
            1.0, float(self.declare_parameter('search_timeout_s', 300.0).value)
        )
        self.phase_server_wait_s = max(
            0.1, float(self.declare_parameter('phase_server_wait_s', 2.0).value)
        )
        self.phase_retry_delay_s = max(
            0.0, float(self.declare_parameter('phase_retry_delay_s', 0.5).value)
        )
        self.estimate_topic = str(
            self.declare_parameter(
                'estimate_topic', '/sound_localizer/current_estimate'
            ).value
        )
        self.leak_topic = str(
            self.declare_parameter('leak_topic', '/leak_detected').value
        )
        self.debug_topic = str(
            self.declare_parameter('debug_topic', '/voice/debug').value
        )
        self.publish_debug_events = bool(
            self.declare_parameter('publish_debug_events', True).value
        )

        self._goal_active = False
        self._latest_estimate: PoseStamped | None = None
        self._leak_detected = False
        self._active_phase = 'idle'

        self._voice_debug_pub = self.create_publisher(String, self.debug_topic, 10)
        self.create_subscription(PoseStamped, self.estimate_topic, self._estimate_cb, 10)
        self.create_subscription(Bool, self.leak_topic, self._leak_cb, 10)

        self.explore_client = ActionClient(
            self, ExploreUntilDetected, self.explore_action_name
        )
        self.localize_client = ActionClient(
            self, LocalizeDetectedLeak, self.localize_action_name
        )

        self._action_server = ActionServer(
            self,
            Search,
            self.search_action_name,
            execute_callback=self.execute_cb,
            goal_callback=self.goal_cb,
            cancel_callback=self.cancel_cb,
        )

        self.get_logger().info(
            'Leak search mission coordinator ready: '
            f'action="{self.search_action_name}", '
            f'explore_action="{self.explore_action_name}", '
            f'localize_action="{self.localize_action_name}", '
            f'debug_topic="{self.debug_topic}"'
        )

    def _estimate_cb(self, msg: PoseStamped) -> None:
        self._latest_estimate = msg

    def _leak_cb(self, msg: Bool) -> None:
        self._leak_detected = bool(msg.data)

    def goal_cb(self, goal_req: Search.Goal):
        del goal_req
        if self._goal_active:
            self.get_logger().warn(
                'Rejecting Search goal because another search mission is already active.'
            )
            return GoalResponse.REJECT
        self.get_logger().info('Search goal received.')
        return GoalResponse.ACCEPT

    def cancel_cb(self, goal_handle):
        del goal_handle
        self.get_logger().info('Search cancel requested.')
        return CancelResponse.ACCEPT

    @staticmethod
    def _copy_pose_stamped(pose: PoseStamped) -> PoseStamped:
        copied = PoseStamped()
        copied.header = pose.header
        copied.pose = pose.pose
        return copied

    def _fallback_pose(self, request_pose: PoseStamped) -> PoseStamped:
        fallback = PoseStamped()
        fallback.header = request_pose.header
        fallback.pose = request_pose.pose
        if not fallback.header.frame_id:
            fallback.header.frame_id = 'map'
        if fallback.pose.orientation.w == 0.0:
            fallback.pose.orientation.w = 1.0
        return fallback

    @staticmethod
    def _make_result(error_code: int, error_msg: str, final_message: str) -> Search.Result:
        result = Search.Result()
        result.error_code = int(error_code)
        result.error_msg = str(error_msg)
        result.final_message = str(final_message)
        return result

    def _feedback_pose(
        self,
        fallback_pose: PoseStamped,
        phase_estimate: PoseStamped | None = None,
    ) -> PoseStamped:
        if phase_estimate is not None:
            return self._copy_pose_stamped(phase_estimate)
        if self._latest_estimate is not None:
            return self._copy_pose_stamped(self._latest_estimate)
        return self._copy_pose_stamped(fallback_pose)

    def _make_feedback(
        self,
        status: str,
        search_complete: bool,
        fallback_pose: PoseStamped,
        phase_estimate: PoseStamped | None = None,
    ) -> Search.Feedback:
        feedback = Search.Feedback()
        feedback.object_class = str(status)
        feedback.object_location = self._feedback_pose(fallback_pose, phase_estimate)
        feedback.search_complete = bool(search_complete)
        return feedback

    def _emit_debug_event(self, event: str, **payload) -> None:
        if not self.publish_debug_events:
            return
        message = String()
        event_payload = {
            'source': 'mission_coordinator',
            'event': str(event),
            'active_phase': self._active_phase,
            'timestamp_ns': self.get_clock().now().nanoseconds,
        }
        event_payload.update(payload)
        message.data = json.dumps(event_payload, separators=(',', ':'), sort_keys=True)
        self._voice_debug_pub.publish(message)

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

    async def _cancel_phase_goal(self, phase_goal_handle) -> None:
        if phase_goal_handle is None:
            return
        try:
            cancel_future = phase_goal_handle.cancel_goal_async()
        except Exception:
            return
        while cancel_future is not None and not cancel_future.done():
            await self._sleep_async(0.1)

    async def _run_phase(
        self,
        public_goal_handle,
        client,
        goal_msg,
        phase_name: str,
        fallback_pose: PoseStamped,
        deadline_mono: float,
    ) -> PhaseExecutionResult:
        if not client.wait_for_server(timeout_sec=self.phase_server_wait_s):
            detail = f'Action server for phase "{phase_name}" is not available.'
            return PhaseExecutionResult(
                state='unavailable',
                phase_name=phase_name,
                last_stage='server_unavailable',
                detail=detail,
            )

        phase_feedback = {
            'stage': phase_name,
            'estimate': None,
        }

        def _feedback_cb(feedback_msg) -> None:
            feedback = feedback_msg.feedback
            stage = getattr(feedback, 'stage', phase_name)
            phase_feedback['stage'] = str(stage)
            current_estimate = getattr(feedback, 'current_estimate', None)
            if current_estimate is not None:
                phase_feedback['estimate'] = self._copy_pose_stamped(current_estimate)

        self._emit_debug_event('phase_goal_dispatch', phase=phase_name)
        send_future = client.send_goal_async(goal_msg, feedback_callback=_feedback_cb)
        while not send_future.done():
            if public_goal_handle.is_cancel_requested:
                return PhaseExecutionResult(
                    state='canceled',
                    phase_name=phase_name,
                    last_stage=str(phase_feedback['stage']),
                    last_estimate=phase_feedback['estimate'],
                    detail='Search mission canceled while dispatching phase goal.',
                )
            if time.monotonic() >= deadline_mono:
                return PhaseExecutionResult(
                    state='timeout',
                    phase_name=phase_name,
                    last_stage=str(phase_feedback['stage']),
                    last_estimate=phase_feedback['estimate'],
                    detail='Search mission timed out while dispatching phase goal.',
                )
            public_goal_handle.publish_feedback(
                self._make_feedback(
                    str(phase_feedback['stage']),
                    False,
                    fallback_pose,
                    phase_feedback['estimate'],
                )
            )
            await self._sleep_async(self.feedback_period_s)

        try:
            phase_goal_handle = send_future.result()
        except Exception as exc:
            return PhaseExecutionResult(
                state='error',
                phase_name=phase_name,
                last_stage=str(phase_feedback['stage']),
                last_estimate=phase_feedback['estimate'],
                detail=f'Failed to send phase goal: {exc}',
            )

        if phase_goal_handle is None or not phase_goal_handle.accepted:
            return PhaseExecutionResult(
                state='rejected',
                phase_name=phase_name,
                last_stage=str(phase_feedback['stage']),
                last_estimate=phase_feedback['estimate'],
                detail=f'Phase goal for "{phase_name}" was rejected.',
            )

        result_future = phase_goal_handle.get_result_async()
        while not result_future.done():
            if public_goal_handle.is_cancel_requested:
                await self._cancel_phase_goal(phase_goal_handle)
                return PhaseExecutionResult(
                    state='canceled',
                    phase_name=phase_name,
                    last_stage=str(phase_feedback['stage']),
                    last_estimate=phase_feedback['estimate'],
                    detail='Search mission canceled while waiting for phase result.',
                )
            if time.monotonic() >= deadline_mono:
                await self._cancel_phase_goal(phase_goal_handle)
                return PhaseExecutionResult(
                    state='timeout',
                    phase_name=phase_name,
                    last_stage=str(phase_feedback['stage']),
                    last_estimate=phase_feedback['estimate'],
                    detail='Search mission timed out while waiting for phase result.',
                )
            public_goal_handle.publish_feedback(
                self._make_feedback(
                    str(phase_feedback['stage']),
                    False,
                    fallback_pose,
                    phase_feedback['estimate'],
                )
            )
            await self._sleep_async(self.feedback_period_s)

        try:
            wrapped_result = result_future.result()
        except Exception as exc:
            return PhaseExecutionResult(
                state='error',
                phase_name=phase_name,
                last_stage=str(phase_feedback['stage']),
                last_estimate=phase_feedback['estimate'],
                detail=f'Failed while waiting for phase result: {exc}',
            )

        return PhaseExecutionResult(
            state='completed',
            phase_name=phase_name,
            result=wrapped_result.result,
            status=wrapped_result.status,
            last_stage=str(phase_feedback['stage']),
            last_estimate=phase_feedback['estimate'],
        )

    async def execute_cb(self, goal_handle):
        self._goal_active = True
        start_mono = time.monotonic()
        deadline_mono = start_mono + self.search_timeout_s
        fallback_pose = self._fallback_pose(goal_handle.request.initial_pose)
        next_phase = 'localizing' if self._leak_detected else 'exploring'

        self._emit_debug_event(
            'mission_started',
            leak_detected=self._leak_detected,
            timeout_s=self.search_timeout_s,
        )

        try:
            while rclpy.ok():
                if goal_handle.is_cancel_requested:
                    goal_handle.canceled()
                    self._emit_debug_event('mission_finished', outcome='canceled')
                    return self._make_result(
                        ERROR_CANCELED,
                        'Search canceled.',
                        'Search canceled before a stable leak estimate was available.',
                    )

                if time.monotonic() >= deadline_mono:
                    goal_handle.abort()
                    self._emit_debug_event('mission_finished', outcome='timeout')
                    return self._make_result(
                        ERROR_TIMEOUT,
                        'Search mission timed out.',
                        'Search mission timed out before a stable leak estimate was available.',
                    )

                self._active_phase = next_phase
                self._emit_debug_event('mission_stage', stage=next_phase)

                if next_phase == 'exploring':
                    phase_result = await self._run_phase(
                        goal_handle,
                        self.explore_client,
                        ExploreUntilDetected.Goal(),
                        'exploring',
                        fallback_pose,
                        deadline_mono,
                    )
                    if phase_result.state == 'canceled':
                        goal_handle.canceled()
                        self._emit_debug_event('mission_finished', outcome='canceled')
                        return self._make_result(
                            ERROR_CANCELED,
                            'Search canceled.',
                            'Search canceled while exploring for a leak.',
                        )
                    if phase_result.state == 'timeout':
                        goal_handle.abort()
                        self._emit_debug_event(
                            'mission_finished', outcome='timeout', phase='exploring'
                        )
                        return self._make_result(
                            ERROR_TIMEOUT,
                            phase_result.detail,
                            'Search mission timed out while exploring for a leak.',
                        )
                    if phase_result.state != 'completed':
                        goal_handle.abort()
                        self._emit_debug_event(
                            'mission_finished',
                            outcome='phase_error',
                            phase='exploring',
                            detail=phase_result.detail,
                        )
                        return self._make_result(
                            ERROR_PHASE_UNAVAILABLE,
                            phase_result.detail,
                            'Search could not start the exploration phase.',
                        )
                    if phase_result.status != GoalStatus.STATUS_SUCCEEDED or phase_result.result is None:
                        goal_handle.abort()
                        self._emit_debug_event(
                            'mission_finished',
                            outcome='phase_error',
                            phase='exploring',
                            status=phase_result.status,
                        )
                        return self._make_result(
                            ERROR_PHASE_FAILED,
                            'Exploration phase did not complete successfully.',
                            'Search could not complete the exploration phase.',
                        )

                    phase_reason = str(getattr(phase_result.result, 'reason', ''))
                    self._emit_debug_event(
                        'phase_completed',
                        phase='exploring',
                        reason=phase_reason,
                        success=bool(getattr(phase_result.result, 'success', False)),
                    )
                    if bool(getattr(phase_result.result, 'success', False)):
                        next_phase = 'localizing'
                        continue

                    goal_handle.abort()
                    self._emit_debug_event(
                        'mission_finished',
                        outcome='no_leak_detected',
                        phase='exploring',
                        reason=phase_reason,
                    )
                    return self._make_result(
                        ERROR_NO_LEAK_FOUND,
                        'No leak was detected before exploration exhausted all frontiers.',
                        'Search explored all frontiers without detecting a leak.',
                    )

                phase_result = await self._run_phase(
                    goal_handle,
                    self.localize_client,
                    LocalizeDetectedLeak.Goal(),
                    'localizing',
                    fallback_pose,
                    deadline_mono,
                )
                if phase_result.state == 'canceled':
                    goal_handle.canceled()
                    self._emit_debug_event('mission_finished', outcome='canceled')
                    return self._make_result(
                        ERROR_CANCELED,
                        'Search canceled.',
                        'Search canceled while localizing the leak.',
                    )
                if phase_result.state == 'timeout':
                    goal_handle.abort()
                    self._emit_debug_event(
                        'mission_finished', outcome='timeout', phase='localizing'
                    )
                    return self._make_result(
                        ERROR_TIMEOUT,
                        phase_result.detail,
                        'Search mission timed out while localizing the leak.',
                    )
                if phase_result.state != 'completed':
                    goal_handle.abort()
                    self._emit_debug_event(
                        'mission_finished',
                        outcome='phase_error',
                        phase='localizing',
                        detail=phase_result.detail,
                    )
                    return self._make_result(
                        ERROR_PHASE_UNAVAILABLE,
                        phase_result.detail,
                        'Search could not start the leak-localization phase.',
                    )
                if phase_result.status != GoalStatus.STATUS_SUCCEEDED or phase_result.result is None:
                    goal_handle.abort()
                    self._emit_debug_event(
                        'mission_finished',
                        outcome='phase_error',
                        phase='localizing',
                        status=phase_result.status,
                    )
                    return self._make_result(
                        ERROR_PHASE_FAILED,
                        'Leak-localization phase did not complete successfully.',
                        'Search could not complete the leak-localization phase.',
                    )

                phase_reason = str(getattr(phase_result.result, 'reason', ''))
                phase_success = bool(getattr(phase_result.result, 'success', False))
                self._emit_debug_event(
                    'phase_completed',
                    phase='localizing',
                    reason=phase_reason,
                    success=phase_success,
                )
                if phase_success:
                    goal_handle.publish_feedback(
                        self._make_feedback(
                            'stable_estimate_found',
                            True,
                            fallback_pose,
                            getattr(phase_result.result, 'estimate_pose', None),
                        )
                    )
                    goal_handle.succeed()
                    self._emit_debug_event(
                        'mission_finished',
                        outcome='stable_estimate_found',
                        reason=phase_reason,
                    )
                    return self._make_result(
                        ERROR_NONE,
                        '',
                        'Stable leak estimate available from sound localization.',
                    )

                next_phase = 'exploring'
                goal_handle.publish_feedback(
                    self._make_feedback(
                        'resuming_exploration',
                        False,
                        fallback_pose,
                        getattr(phase_result.result, 'estimate_pose', None),
                    )
                )
                self._emit_debug_event(
                    'mission_stage',
                    stage='resuming_exploration',
                    reason=phase_reason,
                )
                await self._sleep_async(self.phase_retry_delay_s)

            goal_handle.abort()
            self._emit_debug_event('mission_finished', outcome='ros_shutdown')
            return self._make_result(
                ERROR_PHASE_FAILED,
                'ROS shutdown during search mission.',
                'Search stopped because ROS shut down.',
            )
        finally:
            self._active_phase = 'idle'
            self._goal_active = False


def main() -> None:
    rclpy.init()
    node = LeakSearchMissionCoordinator()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
