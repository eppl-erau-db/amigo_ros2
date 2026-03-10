#!/usr/bin/env python3
"""
Voice command bridge for Go2 search behavior.

- Subscribes to a transcript topic (`std_msgs/String`)
- Uses a wake phrase to arm commands for a short window
- Sends a `go2_interfaces/Search` goal when a search phrase is heard
"""

import re
import time
from typing import Iterable, List

from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseStamped
import rclpy
from rclpy.action import ActionClient
from rclpy.duration import Duration
from rclpy.node import Node
from std_msgs.msg import String
import tf2_ros
from unitree_api.msg import Request as UnitreeRequest

from go2_interfaces.action import Search

ROBOT_SPORT_API_ID_STANDUP = 1004
ROBOT_SPORT_API_ID_STANDDOWN = 1005


class VoiceCommandNode(Node):
    def __init__(self) -> None:
        super().__init__('voice_command_node')

        self.transcript_topic = str(self.declare_parameter(
            'transcript_topic', '/voice/transcript').value)
        self.require_wake_phrase = bool(self.declare_parameter(
            'require_wake_phrase', True).value)
        self.wake_phrase = str(self.declare_parameter(
            'wake_phrase', 'hey amigo').value)
        raw_wake_phrases = self.declare_parameter('wake_phrases', ['amigo']).value
        if isinstance(raw_wake_phrases, str):
            self.wake_phrases_extra = [raw_wake_phrases]
        elif isinstance(raw_wake_phrases, (list, tuple)):
            self.wake_phrases_extra = [str(value) for value in raw_wake_phrases]
        else:
            self.wake_phrases_extra = []
        self.command_mode = str(self.declare_parameter(
            'command_mode', 'search').value).strip().lower()
        self.search_phrase = str(self.declare_parameter(
            'search_phrase', 'look for a leak').value)
        raw_search_phrases = self.declare_parameter('search_phrases', ['']).value
        if isinstance(raw_search_phrases, str):
            self.search_phrases_extra = [raw_search_phrases]
        elif isinstance(raw_search_phrases, (list, tuple)):
            self.search_phrases_extra = [str(value) for value in raw_search_phrases]
        else:
            self.search_phrases_extra = []
        self.stand_up_phrase = str(self.declare_parameter(
            'stand_up_phrase', 'stand up').value)
        raw_stand_up_phrases = self.declare_parameter('stand_up_phrases', ['']).value
        if isinstance(raw_stand_up_phrases, str):
            self.stand_up_phrases_extra = [raw_stand_up_phrases]
        elif isinstance(raw_stand_up_phrases, (list, tuple)):
            self.stand_up_phrases_extra = [str(value) for value in raw_stand_up_phrases]
        else:
            self.stand_up_phrases_extra = []
        self.lay_down_phrase = str(self.declare_parameter(
            'lay_down_phrase', 'lay down').value)
        raw_lay_down_phrases = self.declare_parameter('lay_down_phrases', ['']).value
        if isinstance(raw_lay_down_phrases, str):
            self.lay_down_phrases_extra = [raw_lay_down_phrases]
        elif isinstance(raw_lay_down_phrases, (list, tuple)):
            self.lay_down_phrases_extra = [str(value) for value in raw_lay_down_phrases]
        else:
            self.lay_down_phrases_extra = []
        self.search_action_name = str(self.declare_parameter(
            'search_action_name', 'search').value)
        self.sport_request_topic = str(self.declare_parameter(
            'sport_request_topic', '/api/sport/request').value)
        self.wake_window_s = float(self.declare_parameter(
            'wake_window_s', 8.0).value)
        self.command_cooldown_s = float(self.declare_parameter(
            'command_cooldown_s', 12.0).value)
        self.dedupe_window_s = float(self.declare_parameter(
            'dedupe_window_s', 1.5).value)
        self.map_frame = str(self.declare_parameter(
            'map_frame', 'map').value)
        self.base_frame = str(self.declare_parameter(
            'base_frame', 'base_link').value)
        self.log_transcripts = bool(self.declare_parameter(
            'log_transcripts', False).value)
        self.debug_decisions = bool(self.declare_parameter(
            'debug_decisions', False).value)

        self._wake_phrases_norm = self._build_phrase_list(
            self.wake_phrase, self.wake_phrases_extra, fallback='hey amigo')
        self._search_phrases_norm = self._build_phrase_list(
            self.search_phrase, self.search_phrases_extra, fallback='look for a leak')
        self._stand_up_phrases_norm = self._build_phrase_list(
            self.stand_up_phrase, self.stand_up_phrases_extra, fallback='stand up')
        self._lay_down_phrases_norm = self._build_phrase_list(
            self.lay_down_phrase, self.lay_down_phrases_extra, fallback='lay down')

        self._awake_until = 0.0
        self._last_command_time = 0.0
        self._last_transcript_norm = ''
        self._last_transcript_time = 0.0
        self._goal_in_flight = False

        self.search_client = ActionClient(self, Search, self.search_action_name)
        self.sport_req_pub = self.create_publisher(UnitreeRequest, self.sport_request_topic, 10)
        self.tfbuf = tf2_ros.Buffer(cache_time=Duration(seconds=10.0))
        self.tflistener = tf2_ros.TransformListener(self.tfbuf, self)

        self.create_subscription(String, self.transcript_topic, self._transcript_cb, 10)

        if self.command_mode not in ('search', 'sport_test'):
            self.get_logger().warn(
                f'Unknown command_mode="{self.command_mode}". Falling back to "search".'
            )
            self.command_mode = 'search'

        self.get_logger().info(
            f'Voice command node ready. mode="{self.command_mode}", topic="{self.transcript_topic}", '
            f'wake_phrases={self._wake_phrases_norm}, search_phrases={self._search_phrases_norm}, '
            f'stand_up_phrases={self._stand_up_phrases_norm}, '
            f'lay_down_phrases={self._lay_down_phrases_norm}, '
            f'require_wake={self.require_wake_phrase}, action="{self.search_action_name}".'
        )

    @staticmethod
    def _normalize(text: str) -> str:
        lower = text.lower()
        alnum_spaces_only = re.sub(r'[^a-z0-9 ]+', ' ', lower)
        return re.sub(r'\s+', ' ', alnum_spaces_only).strip()

    def _build_phrase_list(self, primary: str, extra: Iterable[str], fallback: str) -> List[str]:
        phrases: List[str] = []
        for raw in [primary, *extra]:
            norm = self._normalize(str(raw))
            if norm and norm not in phrases:
                phrases.append(norm)
        if not phrases:
            phrases.append(self._normalize(fallback))
        return phrases

    def _is_awake(self, now_mono: float) -> bool:
        if not self.require_wake_phrase:
            return True
        return now_mono <= self._awake_until

    @staticmethod
    def _has_wake_phrase(transcript: str, wake_phrases: Iterable[str]) -> bool:
        for wake in wake_phrases:
            if transcript == wake or transcript.startswith(f'{wake} '):
                return True
        return False

    def _transcript_cb(self, msg: String) -> None:
        raw = str(msg.data).strip()
        if not raw:
            return

        now = time.monotonic()
        transcript = self._normalize(raw)
        if not transcript:
            return

        if self.log_transcripts:
            self.get_logger().info(f'Transcript: "{transcript}"')

        # Drop rapid duplicate transcripts from streaming STT backends.
        if (transcript == self._last_transcript_norm and
                (now - self._last_transcript_time) <= self.dedupe_window_s):
            if self.debug_decisions:
                self.get_logger().info(
                    f'Debug: dropped duplicate transcript "{transcript}" '
                    f'within {self.dedupe_window_s:.1f}s dedupe window.'
                )
            return
        self._last_transcript_norm = transcript
        self._last_transcript_time = now

        if self._has_wake_phrase(transcript, self._wake_phrases_norm):
            self._awake_until = now + self.wake_window_s
            self.get_logger().info(
                f'Wake phrase heard. Command window open for {self.wake_window_s:.1f}s.'
            )

        if not self._is_awake(now):
            if self.debug_decisions:
                self.get_logger().info(
                    f'Debug: ignored transcript while asleep: "{transcript}"'
                )
            return

        if self.command_mode == 'search':
            if self._contains_any_intent(transcript, self._search_phrases_norm):
                self._trigger_search_if_allowed(now)
            elif self.debug_decisions:
                self.get_logger().info(
                    f'Debug: no search intent match for "{transcript}". '
                    f'Expected one of {self._search_phrases_norm}.'
                )
            return

        if self.command_mode == 'sport_test':
            if self._contains_any_intent(transcript, self._stand_up_phrases_norm):
                self._trigger_sport_if_allowed(
                    now_mono=now,
                    command_label='stand_up',
                    api_id=ROBOT_SPORT_API_ID_STANDUP,
                )
                return

            if self._contains_any_intent(transcript, self._lay_down_phrases_norm):
                self._trigger_sport_if_allowed(
                    now_mono=now,
                    command_label='lay_down',
                    api_id=ROBOT_SPORT_API_ID_STANDDOWN,
                )
                return
            if self.debug_decisions:
                self.get_logger().info(
                    f'Debug: no sport intent match for "{transcript}". '
                    f'stand_up={self._stand_up_phrases_norm}, '
                    f'lay_down={self._lay_down_phrases_norm}.'
                )

    @staticmethod
    def _contains_any_intent(transcript: str, phrase_list: Iterable[str]) -> bool:
        return any(phrase in transcript for phrase in phrase_list)

    def _trigger_search_if_allowed(self, now_mono: float) -> None:
        if self._goal_in_flight:
            self.get_logger().info('Search goal already in progress; ignoring voice command.')
            return

        elapsed = now_mono - self._last_command_time
        if elapsed < self.command_cooldown_s:
            self.get_logger().info(
                f'Search command on cooldown ({self.command_cooldown_s - elapsed:.1f}s remaining).'
            )
            return

        if not self.search_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().warn(
                f'Search action server "{self.search_action_name}" not available.'
            )
            return

        goal = Search.Goal()
        goal.initial_pose = self._build_initial_pose()
        goal.behavior_tree = ''

        self._goal_in_flight = True
        self._last_command_time = now_mono
        if self.require_wake_phrase:
            self._awake_until = 0.0

        self.get_logger().info('Voice command matched. Sending Search action goal.')
        send_future = self.search_client.send_goal_async(goal)
        send_future.add_done_callback(self._on_goal_response)

    def _trigger_sport_if_allowed(self, now_mono: float, command_label: str, api_id: int) -> None:
        elapsed = now_mono - self._last_command_time
        if elapsed < self.command_cooldown_s:
            self.get_logger().info(
                f'Command on cooldown ({self.command_cooldown_s - elapsed:.1f}s remaining).'
            )
            return

        request = UnitreeRequest()
        request.header.identity.api_id = int(api_id)
        self.sport_req_pub.publish(request)

        self._last_command_time = now_mono
        if self.require_wake_phrase:
            self._awake_until = 0.0

        self.get_logger().info(
            f'Published sport command "{command_label}" (api_id={api_id}) '
            f'to "{self.sport_request_topic}".'
        )

    def _build_initial_pose(self) -> PoseStamped:
        pose = PoseStamped()
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.header.frame_id = self.map_frame
        pose.pose.orientation.w = 1.0

        try:
            tf = self.tfbuf.lookup_transform(self.map_frame, self.base_frame, rclpy.time.Time())
            pose.pose.position.x = tf.transform.translation.x
            pose.pose.position.y = tf.transform.translation.y
            pose.pose.position.z = tf.transform.translation.z
            pose.pose.orientation.x = tf.transform.rotation.x
            pose.pose.orientation.y = tf.transform.rotation.y
            pose.pose.orientation.z = tf.transform.rotation.z
            pose.pose.orientation.w = tf.transform.rotation.w
        except Exception as exc:
            self.get_logger().warn(
                f'Failed to get TF {self.map_frame}->{self.base_frame}. '
                f'Using default origin pose: {exc}'
            )

        return pose

    def _on_goal_response(self, future) -> None:
        try:
            goal_handle = future.result()
        except Exception as exc:
            self._goal_in_flight = False
            self.get_logger().error(f'Failed to send Search goal: {exc}')
            return

        if goal_handle is None or not goal_handle.accepted:
            self._goal_in_flight = False
            self.get_logger().warn('Search goal was rejected by server.')
            return

        self.get_logger().info('Search goal accepted.')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._on_search_result)

    def _on_search_result(self, future) -> None:
        self._goal_in_flight = False
        try:
            wrapped_result = future.result()
        except Exception as exc:
            self.get_logger().error(f'Failed while waiting for Search result: {exc}')
            return

        status = wrapped_result.status
        result = wrapped_result.result
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info(
                f'Search completed. final_message="{result.final_message}" '
                f'error_code={result.error_code}.'
            )
        else:
            self.get_logger().warn(
                f'Search ended with status={status}, '
                f'error_code={result.error_code}, error_msg="{result.error_msg}".'
            )


def main() -> None:
    rclpy.init()
    node = VoiceCommandNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
