#!/usr/bin/env python3
"""
Voice command bridge for Go2 voice-triggered actions.

- Subscribes to a transcript topic (`std_msgs/String`)
- Uses a wake phrase to arm commands for a short window
- Can trigger one or more command groups from the same launch
"""

import json
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
        self.follow_phrase = str(self.declare_parameter(
            'follow_phrase', 'follow me').value)
        raw_follow_phrases = self.declare_parameter('follow_phrases', ['']).value
        if isinstance(raw_follow_phrases, str):
            self.follow_phrases_extra = [raw_follow_phrases]
        elif isinstance(raw_follow_phrases, (list, tuple)):
            self.follow_phrases_extra = [str(value) for value in raw_follow_phrases]
        else:
            self.follow_phrases_extra = []
        self.stop_follow_phrase = str(self.declare_parameter(
            'stop_follow_phrase', 'stop following').value)
        raw_stop_follow_phrases = self.declare_parameter('stop_follow_phrases', ['']).value
        if isinstance(raw_stop_follow_phrases, str):
            self.stop_follow_phrases_extra = [raw_stop_follow_phrases]
        elif isinstance(raw_stop_follow_phrases, (list, tuple)):
            self.stop_follow_phrases_extra = [str(value) for value in raw_stop_follow_phrases]
        else:
            self.stop_follow_phrases_extra = []
        self.search_action_name = str(self.declare_parameter(
            'search_action_name', 'search').value)
        self.sport_request_topic = str(self.declare_parameter(
            'sport_request_topic', '/api/sport/request').value)
        self.command_topic = str(self.declare_parameter(
            'command_topic', '/voice/command').value)
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
        self.debug_topic = str(self.declare_parameter(
            'debug_topic', '/voice/debug').value)
        self.publish_debug_topic = bool(self.declare_parameter(
            'publish_debug_topic', True).value)

        self._wake_phrases_norm = self._build_phrase_list(
            self.wake_phrase, self.wake_phrases_extra, fallback='hey amigo')
        self._search_phrases_norm = self._build_phrase_list(
            self.search_phrase, self.search_phrases_extra, fallback='look for a leak')
        self._stand_up_phrases_norm = self._build_phrase_list(
            self.stand_up_phrase, self.stand_up_phrases_extra, fallback='stand up')
        self._lay_down_phrases_norm = self._build_phrase_list(
            self.lay_down_phrase, self.lay_down_phrases_extra, fallback='lay down')
        self._follow_phrases_norm = self._build_phrase_list(
            self.follow_phrase, self.follow_phrases_extra, fallback='follow me')
        self._stop_follow_phrases_norm = self._build_phrase_list(
            self.stop_follow_phrase, self.stop_follow_phrases_extra, fallback='stop following')

        self._awake_until = 0.0
        self._last_command_time = 0.0
        self._last_transcript_norm = ''
        self._last_transcript_time = 0.0
        self._goal_in_flight = False
        self._active_search_goal_handle = None
        self._pending_follow_dispatch = None

        self.search_client = ActionClient(self, Search, self.search_action_name)
        self.sport_req_pub = self.create_publisher(UnitreeRequest, self.sport_request_topic, 10)
        self.command_pub = self.create_publisher(String, self.command_topic, 10)
        self.debug_pub = self.create_publisher(String, self.debug_topic, 10)
        self.tfbuf = tf2_ros.Buffer(cache_time=Duration(seconds=10.0))
        self.tflistener = tf2_ros.TransformListener(self.tfbuf, self)

        self.create_subscription(String, self.transcript_topic, self._transcript_cb, 10)

        self._enabled_command_groups, unknown_command_groups = self._parse_command_mode(
            self.command_mode
        )
        if unknown_command_groups:
            self.get_logger().warn(
                f'Unknown command_mode token(s)={unknown_command_groups}. '
                'Supported values include "search", "sport_test", "follow", and "all".'
            )
        if not self._enabled_command_groups:
            self.get_logger().warn(
                f'command_mode="{self.command_mode}" enabled no valid command groups. '
                'Falling back to "search".'
            )
            self._enabled_command_groups = {'search'}

        self.get_logger().info(
            f'Voice command node ready. mode="{self.command_mode}", '
            f'enabled_groups={sorted(self._enabled_command_groups)}, '
            f'topic="{self.transcript_topic}", '
            f'wake_phrases={self._wake_phrases_norm}, search_phrases={self._search_phrases_norm}, '
            f'stand_up_phrases={self._stand_up_phrases_norm}, '
            f'lay_down_phrases={self._lay_down_phrases_norm}, '
            f'follow_phrases={self._follow_phrases_norm}, '
            f'stop_follow_phrases={self._stop_follow_phrases_norm}, '
            f'require_wake={self.require_wake_phrase}, action="{self.search_action_name}", '
            f'command_topic="{self.command_topic}", debug_topic="{self.debug_topic}".'
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

    @staticmethod
    def _parse_command_mode(raw_mode: str) -> tuple[set[str], list[str]]:
        enabled_groups: set[str] = set()
        unknown_groups: list[str] = []

        for token in re.split(r'[\s,]+', str(raw_mode).strip().lower()):
            if not token:
                continue
            if token in ('all', 'multi', 'hybrid'):
                enabled_groups.update(('search', 'sport_test', 'follow'))
            elif token == 'search':
                enabled_groups.add('search')
            elif token in ('sport', 'sport_test'):
                enabled_groups.add('sport_test')
            elif token in ('follow', 'follow_me', 'person_follow'):
                enabled_groups.add('follow')
            else:
                unknown_groups.append(token)

        return enabled_groups, unknown_groups


    def _emit_debug_event(self, event: str, **payload) -> None:
        if not self.publish_debug_topic:
            return
        message = String()
        event_payload = {
            'source': 'voice_command_node',
            'event': str(event),
            'timestamp_ns': self.get_clock().now().nanoseconds,
        }
        event_payload.update(payload)
        message.data = json.dumps(event_payload, separators=(',', ':'), sort_keys=True)
        self.debug_pub.publish(message)

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
        self._emit_debug_event(
            'transcript_received',
            raw=raw,
            transcript=transcript,
            awake=self._is_awake(now),
        )

        # Drop rapid duplicate transcripts from streaming STT backends.
        if (transcript == self._last_transcript_norm and
                (now - self._last_transcript_time) <= self.dedupe_window_s):
            if self.debug_decisions:
                self.get_logger().info(
                    f'Debug: dropped duplicate transcript "{transcript}" '
                    f'within {self.dedupe_window_s:.1f}s dedupe window.'
                )
            self._emit_debug_event(
                'transcript_dropped',
                reason='duplicate',
                transcript=transcript,
                dedupe_window_s=self.dedupe_window_s,
            )
            return
        self._last_transcript_norm = transcript
        self._last_transcript_time = now

        if self._has_wake_phrase(transcript, self._wake_phrases_norm):
            self._awake_until = now + self.wake_window_s
            self.get_logger().info(
                f'Wake phrase heard. Command window open for {self.wake_window_s:.1f}s.'
            )
            self._emit_debug_event(
                'wake_detected',
                transcript=transcript,
                wake_window_s=self.wake_window_s,
            )

        if not self._is_awake(now):
            if self.debug_decisions:
                self.get_logger().info(
                    f'Debug: ignored transcript while asleep: "{transcript}"'
                )
            self._emit_debug_event(
                'transcript_ignored',
                reason='asleep',
                transcript=transcript,
            )
            return

        if 'sport_test' in self._enabled_command_groups:
            matched_phrase = self._match_intent_phrase(transcript, self._stand_up_phrases_norm)
            if matched_phrase is not None:
                self._trigger_sport_if_allowed(
                    now_mono=now,
                    command_label='stand_up',
                    api_id=ROBOT_SPORT_API_ID_STANDUP,
                    transcript=transcript,
                    matched_phrase=matched_phrase,
                )
                return

            matched_phrase = self._match_intent_phrase(transcript, self._lay_down_phrases_norm)
            if matched_phrase is not None:
                self._trigger_sport_if_allowed(
                    now_mono=now,
                    command_label='lay_down',
                    api_id=ROBOT_SPORT_API_ID_STANDDOWN,
                    transcript=transcript,
                    matched_phrase=matched_phrase,
                )
                return

        if 'follow' in self._enabled_command_groups:
            matched_phrase = self._match_intent_phrase(transcript, self._stop_follow_phrases_norm)
            if matched_phrase is not None:
                self._trigger_follow_command_if_allowed(
                    now_mono=now,
                    command_label='stop_follow',
                    transcript=transcript,
                    matched_phrase=matched_phrase,
                )
                return

            matched_phrase = self._match_intent_phrase(transcript, self._follow_phrases_norm)
            if matched_phrase is not None:
                self._trigger_follow_command_if_allowed(
                    now_mono=now,
                    command_label='follow_me',
                    transcript=transcript,
                    matched_phrase=matched_phrase,
                )
                return

        if 'search' in self._enabled_command_groups:
            matched_phrase = self._match_intent_phrase(transcript, self._search_phrases_norm)
            if matched_phrase is not None:
                self._trigger_search_if_allowed(now, transcript, matched_phrase)
                return

        if self.debug_decisions:
            enabled_groups = sorted(self._enabled_command_groups)
            self.get_logger().info(
                f'Debug: no command intent match for "{transcript}". '
                f'enabled_groups={enabled_groups}, '
                f'search={self._search_phrases_norm}, '
                f'stand_up={self._stand_up_phrases_norm}, '
                f'lay_down={self._lay_down_phrases_norm}, '
                f'follow={self._follow_phrases_norm}, '
                f'stop_follow={self._stop_follow_phrases_norm}.'
            )
        self._emit_debug_event(
            'transcript_ignored',
            reason='no_intent_match',
            transcript=transcript,
            enabled_groups=sorted(self._enabled_command_groups),
        )

    @staticmethod
    def _match_intent_phrase(transcript: str, phrase_list: Iterable[str]) -> str | None:
        for phrase in phrase_list:
            if phrase in transcript:
                return phrase
        return None

    def _publish_command(self, command_label: str) -> None:
        msg = String()
        msg.data = command_label
        self.command_pub.publish(msg)

    def _trigger_search_if_allowed(self, now_mono: float, transcript: str, matched_phrase: str) -> None:
        if self._goal_in_flight:
            self.get_logger().info('Search goal already in progress; ignoring voice command.')
            self._emit_debug_event(
                'search_rejected',
                reason='goal_in_flight',
                transcript=transcript,
                matched_phrase=matched_phrase,
            )
            return

        elapsed = now_mono - self._last_command_time
        if elapsed < self.command_cooldown_s:
            remaining_s = self.command_cooldown_s - elapsed
            self.get_logger().info(
                f'Search command on cooldown ({remaining_s:.1f}s remaining).'
            )
            self._emit_debug_event(
                'search_rejected',
                reason='cooldown',
                transcript=transcript,
                matched_phrase=matched_phrase,
                remaining_s=remaining_s,
            )
            return

        if not self.search_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().warn(
                f'Search action server "{self.search_action_name}" not available.'
            )
            self._emit_debug_event(
                'search_rejected',
                reason='server_unavailable',
                transcript=transcript,
                matched_phrase=matched_phrase,
                action=self.search_action_name,
            )
            return

        goal = Search.Goal()
        goal.initial_pose = self._build_initial_pose()
        goal.behavior_tree = ''

        self._goal_in_flight = True
        self._last_command_time = now_mono
        if self.require_wake_phrase:
            self._awake_until = 0.0

        self._publish_command('search')
        self.get_logger().info('Voice command matched. Sending Search action goal.')
        self._emit_debug_event(
            'search_dispatched',
            transcript=transcript,
            matched_phrase=matched_phrase,
            action=self.search_action_name,
        )
        send_future = self.search_client.send_goal_async(goal)
        send_future.add_done_callback(self._on_goal_response)

    def _trigger_sport_if_allowed(
        self,
        now_mono: float,
        command_label: str,
        api_id: int,
        transcript: str,
        matched_phrase: str,
    ) -> None:
        elapsed = now_mono - self._last_command_time
        if elapsed < self.command_cooldown_s:
            remaining_s = self.command_cooldown_s - elapsed
            self.get_logger().info(
                f'Command on cooldown ({remaining_s:.1f}s remaining).'
            )
            self._emit_debug_event(
                'sport_rejected',
                reason='cooldown',
                transcript=transcript,
                matched_phrase=matched_phrase,
                command=command_label,
                remaining_s=remaining_s,
            )
            return

        request = UnitreeRequest()
        request.header.identity.api_id = int(api_id)
        self.sport_req_pub.publish(request)

        self._last_command_time = now_mono
        if self.require_wake_phrase:
            self._awake_until = 0.0

        self._publish_command(command_label)
        self.get_logger().info(
            f'Published sport command "{command_label}" (api_id={api_id}) '
            f'to "{self.sport_request_topic}".'
        )
        self._emit_debug_event(
            'sport_dispatched',
            transcript=transcript,
            matched_phrase=matched_phrase,
            command=command_label,
            api_id=api_id,
        )

    def _trigger_follow_command_if_allowed(
        self,
        now_mono: float,
        command_label: str,
        transcript: str,
        matched_phrase: str,
    ) -> None:
        elapsed = now_mono - self._last_command_time
        bypass_cooldown = (
            command_label == 'stop_follow' or
            (command_label == 'follow_me' and self._goal_in_flight)
        )
        if not bypass_cooldown and elapsed < self.command_cooldown_s:
            remaining_s = self.command_cooldown_s - elapsed
            self.get_logger().info(
                f'Command on cooldown ({remaining_s:.1f}s remaining).'
            )
            self._emit_debug_event(
                'follow_rejected',
                reason='cooldown',
                transcript=transcript,
                matched_phrase=matched_phrase,
                command=command_label,
                remaining_s=remaining_s,
            )
            return

        if command_label == 'stop_follow':
            self._pending_follow_dispatch = None
            self._dispatch_follow_command(command_label, transcript, matched_phrase)
            return

        if command_label == 'follow_me' and self._goal_in_flight:
            self._pending_follow_dispatch = {
                'command_label': command_label,
                'matched_phrase': matched_phrase,
                'transcript': transcript,
            }
            self.get_logger().info(
                'Follow command matched while Search is active. '
                'Canceling Search before enabling follow mode.'
            )
            self._emit_debug_event(
                'follow_preempt_requested',
                transcript=transcript,
                matched_phrase=matched_phrase,
                command=command_label,
                action=self.search_action_name,
            )
            self._cancel_active_search_for_follow()
            return

        self._dispatch_follow_command(command_label, transcript, matched_phrase)

    def _dispatch_follow_command(
        self,
        command_label: str,
        transcript: str,
        matched_phrase: str,
    ) -> None:
        self._last_command_time = time.monotonic()
        if self.require_wake_phrase:
            self._awake_until = 0.0

        self._publish_command(command_label)
        self.get_logger().info(
            f'Published follow command "{command_label}" to "{self.command_topic}".'
        )
        self._emit_debug_event(
            'follow_dispatched',
            transcript=transcript,
            matched_phrase=matched_phrase,
            command=command_label,
            topic=self.command_topic,
        )

    def _cancel_active_search_for_follow(self) -> None:
        if self._pending_follow_dispatch is None or not self._goal_in_flight:
            return

        if self._active_search_goal_handle is None:
            self.get_logger().info(
                'Search goal is still being accepted; follow dispatch will wait for '
                'the goal handle and then request cancellation.'
            )
            self._emit_debug_event(
                'follow_preempt_waiting_for_goal_handle',
                action=self.search_action_name,
            )
            return

        try:
            cancel_future = self._active_search_goal_handle.cancel_goal_async()
            cancel_future.add_done_callback(self._on_search_cancel_response)
        except Exception as exc:
            self.get_logger().error(
                f'Failed to cancel active Search goal before follow dispatch: {exc}'
            )
            self._emit_debug_event(
                'follow_preempt_cancel_error',
                action=self.search_action_name,
                error=str(exc),
            )

    def _on_search_cancel_response(self, future) -> None:
        try:
            cancel_response = future.result()
        except Exception as exc:
            self.get_logger().error(f'Failed to cancel Search goal: {exc}')
            self._emit_debug_event(
                'follow_preempt_cancel_error',
                action=self.search_action_name,
                error=str(exc),
            )
            return

        goals_canceling = getattr(cancel_response, 'goals_canceling', [])
        if goals_canceling:
            self.get_logger().info(
                'Search cancel accepted. Waiting for the Search result callback '
                'before enabling follow mode.'
            )
            self._emit_debug_event(
                'follow_preempt_cancel_accepted',
                action=self.search_action_name,
                goals_canceling=len(goals_canceling),
            )
            return

        self.get_logger().warn(
            'Search cancel was not accepted immediately. '
            'Follow dispatch will wait for Search to finish.'
        )
        self._emit_debug_event(
            'follow_preempt_cancel_rejected',
            action=self.search_action_name,
        )

    def _complete_pending_follow_dispatch(self) -> None:
        if self._pending_follow_dispatch is None:
            return
        payload = self._pending_follow_dispatch
        self._pending_follow_dispatch = None
        self._dispatch_follow_command(
            str(payload['command_label']),
            str(payload['transcript']),
            str(payload['matched_phrase']),
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
            self._active_search_goal_handle = None
            self.get_logger().error(f'Failed to send Search goal: {exc}')
            self._emit_debug_event('search_send_error', error=str(exc))
            self._complete_pending_follow_dispatch()
            return

        if goal_handle is None or not goal_handle.accepted:
            self._goal_in_flight = False
            self._active_search_goal_handle = None
            self.get_logger().warn('Search goal was rejected by server.')
            self._emit_debug_event('search_goal_rejected', action=self.search_action_name)
            self._complete_pending_follow_dispatch()
            return

        self._active_search_goal_handle = goal_handle
        self.get_logger().info('Search goal accepted.')
        self._emit_debug_event('search_goal_accepted', action=self.search_action_name)
        if self._pending_follow_dispatch is not None:
            self._cancel_active_search_for_follow()
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._on_search_result)

    def _on_search_result(self, future) -> None:
        self._goal_in_flight = False
        self._active_search_goal_handle = None
        try:
            wrapped_result = future.result()
        except Exception as exc:
            self.get_logger().error(f'Failed while waiting for Search result: {exc}')
            self._emit_debug_event('search_result_error', error=str(exc))
            self._complete_pending_follow_dispatch()
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
        self._emit_debug_event(
            'search_result',
            status=int(status),
            error_code=int(result.error_code),
            error_msg=str(result.error_msg),
            final_message=str(result.final_message),
        )
        self._complete_pending_follow_dispatch()


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
