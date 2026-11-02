from __future__ import annotations

import pathlib
import sys

import rclpy
from std_msgs.msg import String

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from go2_control.voice_command_node import VoiceCommandNode  # noqa: E402


def test_stay_transcript_publishes_stop_follow_without_wake_phrase() -> None:
    started_context = False
    if not rclpy.ok():
        rclpy.init()
        started_context = True

    node = VoiceCommandNode()
    published: list[tuple[str, str, str]] = []
    original_publish_command = node._publish_command

    def capture_publish(command_label: str, transcript: str, matched_phrase: str) -> None:
        published.append((command_label, transcript, matched_phrase))

    try:
        node._publish_command = capture_publish
        node._transcript_cb(String(data="stay"))
    finally:
        node._publish_command = original_publish_command
        node.destroy_node()
        if started_context and rclpy.ok():
            rclpy.shutdown()

    assert published == [("stop_follow", "stay", "stay")]
