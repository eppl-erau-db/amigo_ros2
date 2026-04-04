#!/usr/bin/env python3
"""
Voice attention acknowledgment node.

Sequence on each request:
1. Rough turn toward the freshest DOA sample, if available.
2. Short visual yaw-centering refinement, if available.
3. Engage the pitch acknowledgment.
4. Publish attention-ready so the gate can open the command window.
5. Hold the pitch until the gate closes the command window, then return to neutral.
"""

from __future__ import annotations

import json
import math
import threading
import time

import rclpy
from geometry_msgs.msg import PointStamped, Twist
from rclpy.node import Node
from rclpy.time import Time
from std_msgs.msg import Bool, Int32, String
import tf2_ros
from unitree_api.msg import Request as UnitreeRequest

try:
    from odas_ros_msgs.msg import OdasSstArrayStamped
except Exception:  # pragma: no cover - environment-dependent optional import
    OdasSstArrayStamped = None

try:
    from zed_msgs.msg import ObjectsStamped
except Exception:  # pragma: no cover - environment-dependent optional import
    ObjectsStamped = None


ROBOT_SPORT_API_ID_STOPMOVE = 1003
ROBOT_SPORT_API_ID_EULER = 1007
ROBOT_SPORT_API_ID_MOVE = 1008

TRACKING_STATE_OK = 1
TRACKING_STATE_SEARCHING = 2

ATTENTION_STATE_IDLE = "IDLE_WAIT_WAKE"
ATTENTION_STATE_WAITING = "WAITING_FOR_ATTENTION_ACK"
ATTENTION_STATE_WINDOW_OPEN = "COMMAND_WINDOW_OPEN"
ATTENTION_STATE_COMMAND_HELD = "COMMAND_HELD"


class VoiceAttentionAckNode(Node):
    def __init__(self) -> None:
        super().__init__("voice_attention_ack_node")

        self.request_topic = str(
            self.declare_parameter("request_topic", "/voice/attention_request").value
        )
        self.ready_topic = str(
            self.declare_parameter("ready_topic", "/voice/attention_ready").value
        )
        self.attention_state_topic = str(
            self.declare_parameter("attention_state_topic", "/voice/attention/state").value
        )
        self.turn_cmd_topic = str(
            self.declare_parameter("turn_cmd_topic", "/voice/attention/cmd_vel").value
        )
        self.gait_reassert_topic = str(
            self.declare_parameter(
                "gait_reassert_topic", "/voice/attention/reassert_gait"
            ).value
        )
        self.sport_request_topic = str(
            self.declare_parameter("sport_request_topic", "/api/sport/request").value
        )
        self.doa_topic = str(self.declare_parameter("doa_topic", "/doa_angle").value)
        self.sst_topic = str(self.declare_parameter("sst_topic", "/sst").value)
        self.doa_ttl_s = max(0.1, float(self.declare_parameter("doa_ttl_s", 2.5).value))
        self.sst_ttl_s = max(0.1, float(self.declare_parameter("sst_ttl_s", 1.5).value))
        self.sst_min_activity = max(
            0.0, float(self.declare_parameter("sst_min_activity", 0.35).value)
        )
        self.doa_zero_offset_deg = float(
            self.declare_parameter("doa_zero_offset_deg", 0.0).value
        )
        self.turn_tolerance_deg = max(
            0.0, float(self.declare_parameter("turn_tolerance_deg", 15.0).value)
        )
        self.turn_timeout_s = max(
            0.1, float(self.declare_parameter("turn_timeout_s", 1.5).value)
        )
        self.turn_kp = max(0.05, float(self.declare_parameter("turn_kp", 0.8).value))
        self.max_turn_rate_radps = max(
            0.05,
            float(self.declare_parameter("max_turn_rate_radps", 0.5).value),
        )

        self.person_follow_enable = bool(
            self.declare_parameter("person_follow_enable", True).value
        )
        self.visual_refine_enable = bool(
            self.declare_parameter("visual_refine_enable", True).value
        )
        self.visual_target_point_topic = str(
            self.declare_parameter(
                "visual_target_point_topic", "/person_follow_vision_node/target_point"
            ).value
        )
        self.visual_target_visible_topic = str(
            self.declare_parameter(
                "visual_target_visible_topic", "/person_follow_vision_node/target_visible"
            ).value
        )
        self.visual_target_status_topic = str(
            self.declare_parameter(
                "visual_target_status_topic", "/person_follow_vision_node/status"
            ).value
        )
        self.visual_objects_topic = str(
            self.declare_parameter(
                "visual_objects_topic", "/zed/zed_node/obj_det/objects"
            ).value
        )
        self.visual_refine_timeout_s = max(
            0.1, float(self.declare_parameter("visual_refine_timeout_s", 2.0).value)
        )
        self.visual_target_ttl_s = max(
            0.1, float(self.declare_parameter("visual_target_ttl_s", 1.0).value)
        )
        self.visual_center_tolerance_rad = max(
            0.01,
            float(self.declare_parameter("visual_center_tolerance_rad", 0.15).value),
        )
        self.visual_turn_kp = max(
            0.05, float(self.declare_parameter("visual_turn_kp", 0.8).value)
        )
        self.visual_max_turn_rate_radps = max(
            0.05,
            float(self.declare_parameter("visual_max_turn_rate_radps", 0.35).value),
        )
        self.visual_target_label = self._normalize_label(
            str(self.declare_parameter("visual_target_label", "person").value)
        )
        self.visual_min_target_confidence = float(
            self.declare_parameter("visual_min_target_confidence", 40.0).value
        )

        self.base_frame = str(self.declare_parameter("base_frame", "base_footprint").value)
        self.pitch_rad = float(self.declare_parameter("pitch_rad", -0.15).value)
        self.pitch_hold_s = max(
            0.0, float(self.declare_parameter("pitch_hold_s", 0.6).value)
        )
        self.return_to_neutral = bool(
            self.declare_parameter("return_to_neutral", True).value
        )
        self.reassert_gait_after_pitch = bool(
            self.declare_parameter("reassert_gait_after_pitch", True).value
        )
        self.gait_reassert_settle_s = max(
            0.0, float(self.declare_parameter("gait_reassert_settle_s", 0.2).value)
        )
        self.attention_release_timeout_s = max(
            1.0,
            float(self.declare_parameter("attention_release_timeout_s", 8.0).value),
        )
        self.debug = bool(self.declare_parameter("debug", False).value)

        self._latest_doa_deg: int | None = None
        self._latest_doa_time = 0.0
        self._latest_sst_doa_deg: float | None = None
        self._latest_sst_activity = 0.0
        self._latest_sst_time = 0.0

        self._latest_target_point: PointStamped | None = None
        self._latest_target_point_time = 0.0
        self._latest_target_visible = False
        self._latest_target_visible_time = 0.0
        self._latest_target_status = ""
        self._latest_target_status_time = 0.0

        self._latest_objects = None
        self._latest_objects_time = 0.0
        self._latest_attention_state = ATTENTION_STATE_IDLE
        self._latest_attention_state_time = 0.0
        self._last_warning_times: dict[str, float] = {}

        self._worker_lock = threading.Lock()
        self._worker_thread: threading.Thread | None = None
        self._cancel_event = threading.Event()

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        self.ready_pub = self.create_publisher(String, self.ready_topic, 10)
        self.turn_cmd_pub = self.create_publisher(Twist, self.turn_cmd_topic, 10)
        self.gait_reassert_pub = self.create_publisher(Bool, self.gait_reassert_topic, 10)
        self.sport_request_pub = self.create_publisher(UnitreeRequest, self.sport_request_topic, 10)

        self.create_subscription(String, self.request_topic, self._request_cb, 10)
        self.create_subscription(String, self.attention_state_topic, self._attention_state_cb, 10)
        self.create_subscription(Int32, self.doa_topic, self._doa_cb, 10)
        if OdasSstArrayStamped is not None:
            self.create_subscription(OdasSstArrayStamped, self.sst_topic, self._sst_cb, 10)
        else:
            self.get_logger().warn(
                "odas_ros_msgs import failed; SST-based attention fallback is unavailable."
            )
        self.create_subscription(
            PointStamped, self.visual_target_point_topic, self._target_point_cb, 10
        )
        self.create_subscription(
            Bool, self.visual_target_visible_topic, self._target_visible_cb, 10
        )
        self.create_subscription(
            String, self.visual_target_status_topic, self._target_status_cb, 10
        )

        if ObjectsStamped is not None:
            self.create_subscription(ObjectsStamped, self.visual_objects_topic, self._objects_cb, 10)
        else:
            self.get_logger().warn(
                "zed_msgs import failed; raw object fallback is unavailable. "
                "Attention refinement will rely on existing person-follow target topics only."
            )

        self.get_logger().info(
            "Voice attention acknowledgment node ready. "
            f'request_topic="{self.request_topic}", '
            f'ready_topic="{self.ready_topic}", '
            f'attention_state_topic="{self.attention_state_topic}", '
            f'turn_cmd_topic="{self.turn_cmd_topic}", '
            f'gait_reassert_topic="{self.gait_reassert_topic}", '
            f'doa_topic="{self.doa_topic}", '
            f'sst_topic="{self.sst_topic}", '
            f"visual_refine_enable={self.visual_refine_enable}, "
            f"person_follow_enable={self.person_follow_enable}."
        )

    def _request_cb(self, msg: String) -> None:
        request_text = str(msg.data).strip() or "wake"
        previous_thread: threading.Thread | None = None

        with self._worker_lock:
            if self._worker_thread is not None and self._worker_thread.is_alive():
                self._cancel_event.set()
                previous_thread = self._worker_thread

        if previous_thread is not None:
            previous_thread.join(timeout=1.0)

        cancel_event = threading.Event()
        worker = threading.Thread(
            target=self._run_attention_sequence,
            args=(request_text, cancel_event),
            daemon=True,
        )
        with self._worker_lock:
            self._cancel_event = cancel_event
            self._worker_thread = worker
        worker.start()

    def _run_attention_sequence(self, request_text: str, cancel_event: threading.Event) -> None:
        if self.debug:
            self.get_logger().info(f'Starting attention acknowledgment for "{request_text}".')

        release_reason = "not_started"
        try:
            self._perform_rough_turn(cancel_event)
            self._send_turn_command(0.0, 0.0, 0.0)
            self._perform_visual_refine(cancel_event)
            self._send_turn_command(0.0, 0.0, 0.0)
            release_reason = self._perform_pitch_ack(cancel_event)
        except Exception as exc:
            self.get_logger().warn(
                f"Attention acknowledgment hit an unexpected error; continuing fail-soft: {exc}"
            )
        finally:
            self._send_turn_command(0.0, 0.0, 0.0)
            if release_reason != "command_released" and self.reassert_gait_after_pitch and not cancel_event.is_set():
                self._request_gait_reassert()
                self._sleep_with_cancel(self.gait_reassert_settle_s, cancel_event)

        if cancel_event.is_set() and self.debug:
            self.get_logger().info("Attention acknowledgment was canceled by a newer request.")

    def _doa_cb(self, msg: Int32) -> None:
        self._latest_doa_deg = int(msg.data)
        self._latest_doa_time = time.monotonic()

    def _sst_cb(self, msg) -> None:
        best_doa_deg: float | None = None
        best_activity = float("-inf")

        for source in msg.sources:
            try:
                activity = float(source.activity)
                x = float(source.x)
                y = float(source.y)
            except Exception:
                continue

            if not (math.isfinite(activity) and math.isfinite(x) and math.isfinite(y)):
                continue
            if activity < self.sst_min_activity:
                continue
            if abs(x) < 1.0e-6 and abs(y) < 1.0e-6:
                continue

            raw_az_deg = math.degrees(math.atan2(y, x))
            calibrated_doa_deg = (raw_az_deg - self.doa_zero_offset_deg) % 360.0
            if activity > best_activity:
                best_activity = activity
                best_doa_deg = calibrated_doa_deg

        if best_doa_deg is None:
            return

        self._latest_sst_doa_deg = best_doa_deg
        self._latest_sst_activity = best_activity
        self._latest_sst_time = time.monotonic()

    def _attention_state_cb(self, msg: String) -> None:
        self._latest_attention_state = str(msg.data).strip() or ATTENTION_STATE_IDLE
        self._latest_attention_state_time = time.monotonic()

    def _target_point_cb(self, msg: PointStamped) -> None:
        self._latest_target_point = msg
        self._latest_target_point_time = time.monotonic()

    def _target_visible_cb(self, msg: Bool) -> None:
        self._latest_target_visible = bool(msg.data)
        self._latest_target_visible_time = time.monotonic()

    def _target_status_cb(self, msg: String) -> None:
        self._latest_target_status = str(msg.data)
        self._latest_target_status_time = time.monotonic()

    def _objects_cb(self, msg) -> None:
        self._latest_objects = msg
        self._latest_objects_time = time.monotonic()

    def _perform_rough_turn(self, cancel_event: threading.Event) -> None:
        initial_sample = self._fresh_turn_error_rad()
        if initial_sample is None:
            self.get_logger().info(
                "Skipping rough DOA turn because neither /doa_angle nor live /sst "
                "provided a fresh direction sample."
            )
            return
        if self.debug:
            self.get_logger().info(
                f'Starting rough attention turn using source="{initial_sample[1]}".'
            )

        deadline = time.monotonic() + self.turn_timeout_s
        tolerance_rad = math.radians(self.turn_tolerance_deg)

        while time.monotonic() < deadline and not cancel_event.is_set():
            sample = self._fresh_turn_error_rad()
            if sample is None:
                self.get_logger().info(
                    "Stopping rough DOA turn because the direction sample became stale."
                )
                break
            error_rad, source = sample

            if abs(error_rad) <= tolerance_rad:
                if self.debug:
                    self.get_logger().info(
                        f'Completed rough attention turn within {self.turn_tolerance_deg:.1f} deg '
                        f'using source="{source}".'
                    )
                break

            yaw_rate = self._clamp(
                self.turn_kp * error_rad,
                -self.max_turn_rate_radps,
                self.max_turn_rate_radps,
            )
            self._send_turn_command(0.0, 0.0, yaw_rate)
            self._sleep_with_cancel(0.1, cancel_event)

    def _perform_visual_refine(self, cancel_event: threading.Event) -> None:
        if not self.visual_refine_enable:
            if self.debug:
                self.get_logger().info("Visual refinement disabled by parameter.")
            return

        if not self.person_follow_enable:
            self.get_logger().info(
                "Skipping visual refinement because person_follow_enable=false; "
                "falling back to DOA-only acknowledgment."
            )
            return

        deadline = time.monotonic() + self.visual_refine_timeout_s
        used_source = ""

        while time.monotonic() < deadline and not cancel_event.is_set():
            target_point, source = self._select_visual_target_point()
            if target_point is None:
                self._sleep_with_cancel(0.1, cancel_event)
                continue

            transformed = self._transform_point_to_base(target_point)
            if transformed is None:
                self._sleep_with_cancel(0.1, cancel_event)
                continue

            target_x, target_y, _ = transformed
            if not math.isfinite(target_x) or not math.isfinite(target_y):
                self._sleep_with_cancel(0.1, cancel_event)
                continue

            yaw_error = math.atan2(target_y, target_x)
            used_source = source
            if abs(yaw_error) <= self.visual_center_tolerance_rad:
                self.get_logger().info(
                    f'Visual refinement centered using source="{source}" '
                    f"(yaw_error_rad={yaw_error:.3f})."
                )
                return

            yaw_rate = self._clamp(
                self.visual_turn_kp * yaw_error,
                -self.visual_max_turn_rate_radps,
                self.visual_max_turn_rate_radps,
            )
            self._send_turn_command(0.0, 0.0, yaw_rate)
            self._sleep_with_cancel(0.1, cancel_event)

        if used_source:
            self.get_logger().info(
                f'Visual refinement timed out after {self.visual_refine_timeout_s:.1f}s '
                f'using source="{used_source}". Continuing to pitch acknowledgment.'
            )
            return

        status_suffix = f' latest_status="{self._latest_target_status}"' if self._latest_target_status else ""
        self.get_logger().info(
            "Visual refinement unavailable within timeout; "
            f"continuing with DOA-only attention acknowledgment.{status_suffix}"
        )

    def _perform_pitch_ack(self, cancel_event: threading.Event) -> str:
        if abs(self.pitch_rad) <= 1.0e-4:
            self.get_logger().info("Skipping pitch acknowledgment because pitch_rad is zero.")
            self.ready_pub.publish(String(data="attention_ready"))
            self.get_logger().info("Attention acknowledgment complete without pitch; published attention_ready.")
            return "no_pitch"

        self._send_euler_command(0.0, self.pitch_rad, 0.0)
        self.ready_pub.publish(String(data="attention_ready"))
        if self.debug:
            self.get_logger().info("Published attention_ready while holding the attention pitch.")

        release_reason = self._wait_for_attention_release(cancel_event)
        if release_reason == "fallback":
            self._sleep_with_cancel(self.pitch_hold_s, cancel_event)

        if self.return_to_neutral:
            self._send_euler_command(0.0, 0.0, 0.0)
            self._sleep_with_cancel(0.2, cancel_event)

        if cancel_event.is_set():
            return "canceled"

        self.get_logger().info(
            f"Attention acknowledgment complete after release_reason={release_reason}."
        )
        return release_reason

    def _wait_for_attention_release(self, cancel_event: threading.Event) -> str:
        deadline = time.monotonic() + self.attention_release_timeout_s
        observed_active_state = False
        observed_command_hold = False

        while time.monotonic() < deadline and not cancel_event.is_set():
            attention_state = self._latest_attention_state
            if attention_state in (
                ATTENTION_STATE_WAITING,
                ATTENTION_STATE_WINDOW_OPEN,
                ATTENTION_STATE_COMMAND_HELD,
            ):
                observed_active_state = True
                if attention_state == ATTENTION_STATE_COMMAND_HELD:
                    observed_command_hold = True
            elif observed_active_state and attention_state == ATTENTION_STATE_IDLE:
                return "command_released" if observed_command_hold else "attention_released"

            self._sleep_with_cancel(0.05, cancel_event)

        if cancel_event.is_set():
            return "canceled"

        if observed_active_state:
            self.get_logger().warn(
                "Attention state did not return to idle before timeout; using fallback pitch hold."
            )
        else:
            self.get_logger().info(
                "Attention state activity was not observed; using fallback pitch hold."
            )
        return "fallback"

    def _fresh_turn_error_rad(self) -> tuple[float, str] | None:
        doa_error = self._fresh_doa_error_rad()
        if doa_error is not None:
            return doa_error, "doa_topic"

        sst_error = self._fresh_sst_error_rad()
        if sst_error is not None:
            return sst_error, "sst"

        return None

    def _fresh_doa_error_rad(self) -> float | None:
        if self._latest_doa_deg is None:
            return None
        if (time.monotonic() - self._latest_doa_time) > self.doa_ttl_s:
            return None

        normalized_deg = ((int(self._latest_doa_deg) + 180) % 360) - 180
        return math.radians(float(normalized_deg))

    def _fresh_sst_error_rad(self) -> float | None:
        if self._latest_sst_doa_deg is None:
            return None
        if (time.monotonic() - self._latest_sst_time) > self.sst_ttl_s:
            return None

        normalized_deg = ((float(self._latest_sst_doa_deg) + 180.0) % 360.0) - 180.0
        return math.radians(normalized_deg)

    def _select_visual_target_point(self) -> tuple[PointStamped | None, str]:
        now = time.monotonic()

        if (
            self._latest_target_visible and
            self._latest_target_point is not None and
            (now - self._latest_target_point_time) <= self.visual_target_ttl_s and
            (now - self._latest_target_visible_time) <= self.visual_target_ttl_s
        ):
            return self._latest_target_point, "person_follow_target"

        raw_point = self._select_raw_person_point()
        if raw_point is not None:
            return raw_point, "zed_objects"

        return None, ""

    def _select_raw_person_point(self) -> PointStamped | None:
        if ObjectsStamped is None or self._latest_objects is None:
            return None
        if (time.monotonic() - self._latest_objects_time) > self.visual_target_ttl_s:
            return None

        best_point: PointStamped | None = None
        best_distance = float("inf")

        for obj in self._latest_objects.objects:
            if self._normalize_label(getattr(obj, "label", "")) != self.visual_target_label:
                continue
            if float(getattr(obj, "confidence", 0.0)) < self.visual_min_target_confidence:
                continue

            tracking_available = bool(getattr(obj, "tracking_available", False))
            tracking_state = int(getattr(obj, "tracking_state", 0))
            if tracking_available and tracking_state not in (
                TRACKING_STATE_OK,
                TRACKING_STATE_SEARCHING,
            ):
                continue

            position = getattr(obj, "position", None)
            if position is None or len(position) < 3:
                continue

            point_x = float(position[0])
            point_y = float(position[1])
            point_z = float(position[2])
            if not (
                math.isfinite(point_x) and
                math.isfinite(point_y) and
                math.isfinite(point_z)
            ):
                continue

            distance = math.sqrt((point_x * point_x) + (point_y * point_y) + (point_z * point_z))
            if distance >= best_distance:
                continue

            point = PointStamped()
            point.header = self._latest_objects.header
            point.point.x = point_x
            point.point.y = point_y
            point.point.z = point_z
            best_point = point
            best_distance = distance

        return best_point

    def _transform_point_to_base(self, point_msg: PointStamped) -> tuple[float, float, float] | None:
        source_frame = str(point_msg.header.frame_id)
        if not source_frame:
            self._warn_throttled("missing_target_frame", "Visual target frame_id is empty.")
            return None

        try:
            transform = self.tf_buffer.lookup_transform(
                self.base_frame,
                source_frame,
                Time(),
            )
        except Exception as exc:
            self._warn_throttled(
                "visual_target_transform",
                f"Failed to transform visual target into {self.base_frame}: {exc}",
            )
            return None

        return self._apply_transform_to_point(
            float(transform.transform.translation.x),
            float(transform.transform.translation.y),
            float(transform.transform.translation.z),
            float(transform.transform.rotation.x),
            float(transform.transform.rotation.y),
            float(transform.transform.rotation.z),
            float(transform.transform.rotation.w),
            float(point_msg.point.x),
            float(point_msg.point.y),
            float(point_msg.point.z),
        )

    def _send_turn_command(self, vx: float, vy: float, vyaw: float) -> None:
        msg = Twist()
        msg.linear.x = float(vx)
        msg.linear.y = float(vy)
        msg.angular.z = float(vyaw)
        self.turn_cmd_pub.publish(msg)

    def _send_euler_command(self, roll: float, pitch: float, yaw: float) -> None:
        request = UnitreeRequest()
        request.header.identity.api_id = int(ROBOT_SPORT_API_ID_EULER)
        request.parameter = json.dumps(
            {
                "x": float(roll),
                "y": float(pitch),
                "z": float(yaw),
            },
            separators=(",", ":"),
        )
        self.sport_request_pub.publish(request)

    def _request_gait_reassert(self) -> None:
        self.gait_reassert_pub.publish(Bool(data=True))

    @staticmethod
    def _normalize_label(label: str) -> str:
        lowered = str(label).strip().lower()
        return "".join(ch if ch.isalnum() else "_" for ch in lowered).strip("_")

    def _sleep_with_cancel(self, duration_s: float, cancel_event: threading.Event) -> None:
        deadline = time.monotonic() + max(0.0, duration_s)
        while time.monotonic() < deadline:
            if cancel_event.is_set():
                return
            time.sleep(0.05)

    def _warn_throttled(self, key: str, message: str, period_s: float = 2.0) -> None:
        now_s = time.monotonic()
        last_s = self._last_warning_times.get(key)
        if last_s is not None and (now_s - last_s) < period_s:
            return
        self._last_warning_times[key] = now_s
        self.get_logger().warn(message)

    @staticmethod
    def _clamp(value: float, lower: float, upper: float) -> float:
        return max(lower, min(upper, value))

    @staticmethod
    def _apply_transform_to_point(
        tx: float,
        ty: float,
        tz: float,
        qx: float,
        qy: float,
        qz: float,
        qw: float,
        px: float,
        py: float,
        pz: float,
    ) -> tuple[float, float, float]:
        rx, ry, rz = VoiceAttentionAckNode._rotate_vector_by_quaternion(
            qx, qy, qz, qw, px, py, pz
        )
        return tx + rx, ty + ry, tz + rz

    @staticmethod
    def _rotate_vector_by_quaternion(
        qx: float,
        qy: float,
        qz: float,
        qw: float,
        vx: float,
        vy: float,
        vz: float,
    ) -> tuple[float, float, float]:
        tx = 2.0 * ((qy * vz) - (qz * vy))
        ty = 2.0 * ((qz * vx) - (qx * vz))
        tz = 2.0 * ((qx * vy) - (qy * vx))
        rx = vx + (qw * tx) + ((qy * tz) - (qz * ty))
        ry = vy + (qw * ty) + ((qz * tx) - (qx * tz))
        rz = vz + (qw * tz) + ((qx * ty) - (qy * tx))
        return rx, ry, rz


def main() -> None:
    rclpy.init()
    node = VoiceAttentionAckNode()
    try:
        rclpy.spin(node)
    finally:
        with node._worker_lock:
            node._cancel_event.set()
            worker = node._worker_thread
        if worker is not None and worker.is_alive():
            worker.join(timeout=1.0)
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
