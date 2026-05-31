#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import threading
import time

from ament_index_python.packages import PackageNotFoundError, get_package_prefix
from geometry_msgs.msg import PoseStamped, Twist
import rclpy
from rclpy.action import ActionClient
from rclpy.duration import Duration
from rclpy.node import Node
from std_msgs.msg import String
import tf2_ros
from unitree_api.msg import Request as UnitreeRequest
from unitree_go.msg import SportModeState

from go2_interfaces.action import Search
from go2_interfaces.msg import RobotModeState
from go2_interfaces.srv import SetRobotMode
from go2_control.mission_supervisor_core import (
    PostureModes,
    SupervisorOps,
    SupervisorState,
    TaskModes,
    complete_posture_transition,
    complete_search,
    enter_fault,
    normalize_voice_command,
    request_mode_change,
    request_voice_command,
    select_motion_routing,
    sync_observed_posture,
)


ROBOT_SPORT_API_ID_STANDUP = 1004
ROBOT_SPORT_API_ID_STANDDOWN = 1005
ROBOT_SPORT_API_ID_HELLO = 1016


class MissionSupervisorNode(Node):
    def __init__(self) -> None:
        super().__init__("mission_supervisor_node")

        self.use_sim_time = bool(self._declare_or_get_parameter("use_sim_time", False).value)
        self.voice_command_topic = str(
            self.declare_parameter("voice_command_topic", "/voice/command").value
        )
        self.robot_mode_state_topic = str(
            self.declare_parameter("robot_mode_state_topic", "/robot_mode_state").value
        )
        self.sport_mode_state_topic = str(
            self.declare_parameter("sport_mode_state_topic", "/lf/sportmodestate").value
        )
        self.mode_service_name = str(
            self.declare_parameter("mode_service_name", "~/set_mode").value
        )
        self.event_topic = str(self.declare_parameter("event_topic", "~/event").value)
        self.debug_topic = str(self.declare_parameter("debug_topic", "/voice/debug").value)
        self.base_cmd_vel_topic = str(
            self.declare_parameter("base_cmd_vel_topic", "cmd_vel").value
        )
        self.nav_candidate_topic = str(
            self.declare_parameter("nav_candidate_topic", "/motion/candidate/nav").value
        )
        self.follow_candidate_topic = str(
            self.declare_parameter("follow_candidate_topic", "/motion/candidate/follow").value
        )
        self.follow_command_topic = str(
            self.declare_parameter("follow_command_topic", "/person_follow/cmd_vel").value
        )
        self.follow_event_topic = str(
            self.declare_parameter(
                "follow_event_topic", "/person_follow_controller_node/event"
            ).value
        )
        self.follow_motion_backend = str(
            self.declare_parameter("follow_motion_backend", "sport_free_avoid").value
        ).strip()
        self.search_action_name = str(
            self.declare_parameter("search_action_name", "search").value
        )
        self.search_server_wait_s = max(
            0.1, float(self.declare_parameter("search_server_wait_s", 1.0).value)
        )
        self.command_cooldown_s = max(
            0.0, float(self.declare_parameter("command_cooldown_s", 3.0).value)
        )
        self.map_frame = str(self.declare_parameter("map_frame", "map").value)
        self.base_frame = str(self.declare_parameter("base_frame", "base_link").value)
        self.sport_request_topic = str(
            self.declare_parameter("sport_request_topic", "/api/sport/request").value
        )
        self.lay_down_settle_s = max(
            0.0, float(self.declare_parameter("lay_down_settle_s", 2.5).value)
        )
        self.stand_up_settle_s = max(
            0.0, float(self.declare_parameter("stand_up_settle_s", 2.5).value)
        )
        self.stand_up_recovery_enabled = bool(
            self.declare_parameter("stand_up_recovery_enabled", True).value
        )
        self.stand_up_recovery_delay_s = max(
            0.0, float(self.declare_parameter("stand_up_recovery_delay_s", 1.0).value)
        )
        self.stand_up_recovery_motion_mode = str(
            self.declare_parameter("stand_up_recovery_motion_mode", "none").value
        ).strip()
        self.stand_up_recovery_gait = str(
            self.declare_parameter("stand_up_recovery_gait", "static_walk").value
        ).strip()
        self.stand_up_recovery_wait_s = max(
            0.0, float(self.declare_parameter("stand_up_recovery_wait_s", 0.0).value)
        )
        self.stand_up_recovery_retries = max(
            1, int(self.declare_parameter("stand_up_recovery_retries", 4).value)
        )
        self.stand_up_recovery_retry_interval_s = max(
            0.0,
            float(self.declare_parameter("stand_up_recovery_retry_interval_s", 0.75).value),
        )
        self.stand_up_recovery_network_interface = str(
            self.declare_parameter("stand_up_recovery_network_interface", "").value
        ).strip()

        self._state = SupervisorState()
        self._state_lock = threading.Lock()
        self._last_voice_command_times: dict[str, float] = {}
        self._search_goal_in_flight = False
        self._search_cancel_requested = False
        self._active_search_goal_handle = None
        self._posture_timer = None
        self._stand_up_recovery_thread: threading.Thread | None = None
        self._stand_up_recovery_lock = threading.Lock()
        self._motion_mode_switcher_executable = self._resolve_motion_mode_switcher_executable()

        self.search_client = ActionClient(self, Search, self.search_action_name)
        self.sport_req_pub = self.create_publisher(UnitreeRequest, self.sport_request_topic, 10)
        self.mode_state_pub = self.create_publisher(
            RobotModeState, self.robot_mode_state_topic, 10
        )
        self.event_pub = self.create_publisher(String, self.event_topic, 10)
        self.debug_pub = self.create_publisher(String, self.debug_topic, 10)
        self.base_cmd_pub = self.create_publisher(Twist, self.base_cmd_vel_topic, 10)
        self.follow_cmd_pub = self.create_publisher(Twist, self.follow_command_topic, 10)

        self.tfbuf = tf2_ros.Buffer(cache_time=Duration(seconds=10.0))
        self.tflistener = tf2_ros.TransformListener(self.tfbuf, self)

        self.create_subscription(String, self.voice_command_topic, self._voice_command_cb, 10)
        self.create_subscription(
            SportModeState, self.sport_mode_state_topic, self._sport_mode_state_cb, 10
        )
        self.create_subscription(Twist, self.nav_candidate_topic, self._nav_candidate_cb, 10)
        self.create_subscription(
            Twist, self.follow_candidate_topic, self._follow_candidate_cb, 10
        )
        self.create_subscription(String, self.follow_event_topic, self._follow_event_cb, 10)
        self.create_service(SetRobotMode, self.mode_service_name, self._handle_set_mode)

        self._publish_state()
        self._emit_event("supervisor_ready", detail="Mission supervisor initialized.")
        self.get_logger().info(
            "Mission supervisor ready. "
            f"voice_command_topic={self.voice_command_topic} "
            f"robot_mode_state_topic={self.robot_mode_state_topic} "
            f"sport_mode_state_topic={self.sport_mode_state_topic} "
            f"search_action={self.search_action_name} "
            f"follow_backend={self.follow_motion_backend}"
        )

    def _declare_or_get_parameter(self, name: str, default_value):
        if self.has_parameter(name):
            return self.get_parameter(name)
        return self.declare_parameter(name, default_value)

    def _resolve_motion_mode_switcher_executable(self) -> str | None:
        if not self.stand_up_recovery_enabled:
            return None
        try:
            package_prefix = get_package_prefix("go2_driver")
        except PackageNotFoundError:
            self.get_logger().warn(
                'stand_up_recovery_enabled=true, but package "go2_driver" was not found.'
            )
            return None

        executable = os.path.join(
            package_prefix,
            "lib",
            "go2_driver",
            "go2_motion_mode_switcher",
        )
        if not os.path.isfile(executable) or not os.access(executable, os.X_OK):
            self.get_logger().warn(
                f'stand_up_recovery_enabled=true, but "{executable}" is unavailable.'
            )
            return None
        return executable

    def _current_state(self) -> SupervisorState:
        with self._state_lock:
            return self._state

    def _replace_state(
        self,
        new_state: SupervisorState,
        *,
        event_name: str,
        detail: str,
        zero_motion: bool = True,
    ) -> None:
        with self._state_lock:
            previous_state = self._state
            self._state = new_state

        if zero_motion:
            self._publish_zero_motion()

        self._publish_state()
        self._emit_event(
            event_name,
            previous_task_mode=previous_state.task_mode,
            previous_posture_mode=previous_state.posture_mode,
            new_task_mode=new_state.task_mode,
            new_posture_mode=new_state.posture_mode,
            faulted=new_state.faulted,
            detail=detail or new_state.detail,
        )

    def _publish_state(self) -> None:
        state = self._current_state()
        msg = RobotModeState()
        msg.stamp = self.get_clock().now().to_msg()
        msg.transition_id = int(state.transition_id)
        msg.task_mode = str(state.task_mode)
        msg.posture_mode = str(state.posture_mode)
        msg.motion_enabled = bool(state.motion_enabled and not state.faulted)
        msg.source = str(state.source)
        msg.detail = str(state.detail)
        self.mode_state_pub.publish(msg)

    def _emit_event(self, event: str, **payload) -> None:
        state = self._current_state()
        message = String()
        event_payload = {
            "source": "mission_supervisor",
            "event": str(event),
            "task_mode": str(state.task_mode),
            "posture_mode": str(state.posture_mode),
            "motion_enabled": bool(state.motion_enabled and not state.faulted),
            "faulted": bool(state.faulted),
            "transition_id": int(state.transition_id),
            "timestamp_ns": self.get_clock().now().nanoseconds,
        }
        event_payload.update(payload)
        message.data = json.dumps(event_payload, separators=(",", ":"), sort_keys=True)
        self.event_pub.publish(message)
        self.debug_pub.publish(message)

    def _publish_zero_motion(self) -> None:
        zero = Twist()
        self.base_cmd_pub.publish(zero)
        self.follow_cmd_pub.publish(zero)

    def _publish_base_motion(self, msg: Twist) -> None:
        self.base_cmd_pub.publish(msg)

    def _publish_follow_motion(self, msg: Twist) -> None:
        self.follow_cmd_pub.publish(msg)

    def _cooldown_applies(self, command: str) -> bool:
        normalized = normalize_voice_command(command)
        return normalized not in {"stop_follow", "lay_down", "stand_up"}

    @staticmethod
    def _posture_from_sport_mode(mode: int) -> str | None:
        if mode == 5:
            return PostureModes.LAYING
        if mode in {0, 1, 2, 3, 8}:
            return PostureModes.STANDING
        return None

    def _sport_mode_state_cb(self, msg: SportModeState) -> None:
        observed_posture = self._posture_from_sport_mode(int(msg.mode))
        if observed_posture is None:
            return

        current_state = self._current_state()
        new_state = sync_observed_posture(
            current_state,
            observed_posture,
            source="sport_mode_state",
            detail=f"observed_sport_mode_{int(msg.mode)}",
        )
        if new_state == current_state:
            return

        self._replace_state(
            new_state,
            event_name="observed_posture_sync",
            detail=new_state.detail,
            zero_motion=observed_posture == PostureModes.LAYING,
        )
        self.get_logger().info(
            f"Observed robot posture {observed_posture} from "
            f"{self.sport_mode_state_topic} mode={int(msg.mode)}."
        )

    def _voice_command_cb(self, msg: String) -> None:
        command = str(msg.data).strip()
        if not command:
            return

        now_mono = time.monotonic()
        if self._cooldown_applies(command):
            last_command_time = self._last_voice_command_times.get(command, 0.0)
            elapsed = now_mono - last_command_time
            if elapsed < self.command_cooldown_s:
                remaining_s = self.command_cooldown_s - elapsed
                self._emit_event(
                    "voice_command_rejected",
                    command=command,
                    reason="cooldown",
                    remaining_s=remaining_s,
                )
                self.get_logger().info(
                    f'Voice command "{command}" rejected by cooldown ({remaining_s:.1f}s remaining).'
                )
                return

        if command == "search" and not self._search_request_is_available():
            self._emit_event(
                "voice_command_rejected",
                command=command,
                reason="search_server_unavailable",
            )
            self.get_logger().warn("Voice search command rejected because the Search server is unavailable.")
            return

        decision = request_voice_command(
            self._current_state(),
            command,
            source="voice",
            allow_preempt=True,
        )
        if not decision.accepted:
            self._emit_event(
                "voice_command_rejected",
                command=command,
                reason=decision.message,
            )
            self.get_logger().info(f'Voice command "{command}" rejected: {decision.message}')
            return

        self._last_voice_command_times[command] = now_mono
        self.get_logger().info(
            f'Voice command "{command}" accepted: {decision.message}'
        )
        self._apply_decision(decision, event_name="voice_command_accepted")

    def _handle_set_mode(self, request: SetRobotMode.Request, response: SetRobotMode.Response):
        previous_state = self._current_state()

        if (
            str(request.task_mode).strip().upper() == TaskModes.SEARCH and
            not self._search_request_is_available()
        ):
            response.accepted = False
            response.previous_task_mode = previous_state.task_mode
            response.previous_posture_mode = previous_state.posture_mode
            response.new_task_mode = previous_state.task_mode
            response.new_posture_mode = previous_state.posture_mode
            response.message = "Search server is unavailable."
            return response

        decision = request_mode_change(
            previous_state,
            requested_task_mode=request.task_mode,
            requested_posture_mode=request.posture_mode,
            source=request.source or "service",
            allow_preempt=bool(request.allow_preempt),
        )

        response.accepted = bool(decision.accepted)
        response.previous_task_mode = previous_state.task_mode
        response.previous_posture_mode = previous_state.posture_mode
        response.new_task_mode = decision.state.task_mode
        response.new_posture_mode = decision.state.posture_mode
        response.message = decision.message

        if decision.accepted:
            self._apply_decision(decision, event_name="service_mode_request")
        else:
            self._emit_event(
                "service_mode_rejected",
                source=request.source or "service",
                reason=decision.message,
                requested_task_mode=str(request.task_mode),
                requested_posture_mode=str(request.posture_mode),
            )
        return response

    def _apply_decision(self, decision, *, event_name: str) -> None:
        self._replace_state(
            decision.state,
            event_name=event_name,
            detail=decision.message,
            zero_motion=SupervisorOps.PUBLISH_ZERO_MOTION in decision.operations,
        )

        for operation in decision.operations:
            if operation == SupervisorOps.PUBLISH_ZERO_MOTION:
                continue
            self._execute_operation(operation)

    def _execute_operation(self, operation: str) -> None:
        # Each operation constant is defined in SupervisorOps and declared in
        # behavior_registry.BehaviorDescriptor.operations.  When adding a new
        # behavior, add its operation constant to SupervisorOps, register it in
        # BUILTIN_BEHAVIORS, and add the handler branch here.
        # See ADDING_BEHAVIORS.md for the full checklist.
        if operation == SupervisorOps.START_SEARCH:
            self._start_search()
            return
        if operation == SupervisorOps.CANCEL_SEARCH:
            self._cancel_search("supervisor_preempt")
            return
        if operation == SupervisorOps.SEND_HELLO:
            self._send_hello_gesture()
            return
        if operation == SupervisorOps.SEND_STAND_DOWN:
            self._start_lay_down_transition()
            return
        if operation == SupervisorOps.SEND_STAND_UP:
            self._start_stand_up_transition()
            return

    def _search_request_is_available(self) -> bool:
        state = self._current_state()
        if state.task_mode == TaskModes.SEARCH:
            return True
        return self.search_client.wait_for_server(timeout_sec=self.search_server_wait_s)

    def _start_search(self) -> None:
        if self._search_goal_in_flight or self._active_search_goal_handle is not None:
            self._emit_event("search_dispatch_skipped", reason="already_active")
            return

        if not self.search_client.wait_for_server(timeout_sec=self.search_server_wait_s):
            self.get_logger().warn(f'Search action server "{self.search_action_name}" is unavailable.')
            self._replace_state(
                complete_search(self._current_state(), detail="search_server_unavailable"),
                event_name="search_dispatch_failed",
                detail="Search server unavailable.",
            )
            return

        goal = Search.Goal()
        goal.initial_pose = self._build_initial_pose()
        goal.behavior_tree = ""

        self._search_goal_in_flight = True
        self._search_cancel_requested = False
        self._emit_event("search_dispatch_started", action=self.search_action_name)
        send_future = self.search_client.send_goal_async(goal)
        send_future.add_done_callback(self._on_search_goal_response)

    def _cancel_search(self, reason: str) -> None:
        self._search_cancel_requested = True

        if self._active_search_goal_handle is None:
            self._emit_event(
                "search_cancel_pending",
                reason=reason,
                waiting_for_goal_handle=self._search_goal_in_flight,
            )
            return

        try:
            cancel_future = self._active_search_goal_handle.cancel_goal_async()
            cancel_future.add_done_callback(self._on_search_cancel_response)
            self._emit_event("search_cancel_requested", reason=reason)
        except Exception as exc:
            self.get_logger().error(f"Failed to request Search cancel: {exc}")
            fault_state = enter_fault(self._current_state(), f"search_cancel_failed: {exc}")
            self._replace_state(
                fault_state,
                event_name="search_cancel_failed",
                detail=str(exc),
            )

    def _on_search_cancel_response(self, future) -> None:
        try:
            cancel_response = future.result()
        except Exception as exc:
            self.get_logger().error(f"Search cancel response failed: {exc}")
            fault_state = enter_fault(self._current_state(), f"search_cancel_response_failed: {exc}")
            self._replace_state(
                fault_state,
                event_name="search_cancel_response_failed",
                detail=str(exc),
            )
            return

        self._emit_event(
            "search_cancel_response",
            goals_canceling=len(getattr(cancel_response, "goals_canceling", [])),
        )

    def _on_search_goal_response(self, future) -> None:
        try:
            goal_handle = future.result()
        except Exception as exc:
            self._search_goal_in_flight = False
            self._active_search_goal_handle = None
            self.get_logger().error(f"Failed to send Search goal: {exc}")
            self._replace_state(
                complete_search(self._current_state(), detail=f"search_send_failed: {exc}"),
                event_name="search_send_failed",
                detail=str(exc),
            )
            return

        self._search_goal_in_flight = False
        if goal_handle is None or not goal_handle.accepted:
            self._active_search_goal_handle = None
            self._replace_state(
                complete_search(self._current_state(), detail="search_goal_rejected"),
                event_name="search_goal_rejected",
                detail="Search goal rejected.",
            )
            return

        self._active_search_goal_handle = goal_handle
        self._emit_event("search_goal_accepted", action=self.search_action_name)
        if self._search_cancel_requested:
            self._cancel_search("pending_preempt_after_accept")
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._on_search_result)

    def _on_search_result(self, future) -> None:
        self._active_search_goal_handle = None
        self._search_goal_in_flight = False
        self._search_cancel_requested = False

        try:
            wrapped_result = future.result()
            status = int(wrapped_result.status)
            result = wrapped_result.result
            detail = str(getattr(result, "final_message", "")) or str(
                getattr(result, "error_msg", "")
            )
        except Exception as exc:
            status = -1
            detail = f"search_result_failed: {exc}"

        new_state = complete_search(self._current_state(), detail=detail or f"search_status_{status}")
        self._replace_state(
            new_state,
            event_name="search_finished",
            detail=detail or f"status={status}",
        )

    def _send_sport_request(self, api_id: int) -> None:
        request = UnitreeRequest()
        request.header.identity.api_id = int(api_id)
        self.sport_req_pub.publish(request)

    def _send_hello_gesture(self) -> None:
        self._send_sport_request(ROBOT_SPORT_API_ID_HELLO)
        self._emit_event("shake_hand_requested", api_id=ROBOT_SPORT_API_ID_HELLO)

    def _start_lay_down_transition(self) -> None:
        self._send_sport_request(ROBOT_SPORT_API_ID_STANDDOWN)
        self._emit_event("lay_down_requested", settle_s=self.lay_down_settle_s)

        self._cancel_posture_timer()
        if self.lay_down_settle_s <= 0.0:
            self._complete_lay_down_transition()
            return

        timer_holder = {}

        def _complete() -> None:
            timer = timer_holder.get("timer")
            if timer is not None:
                timer.cancel()
                self.destroy_timer(timer)
            self._posture_timer = None
            self._complete_lay_down_transition()

        timer_holder["timer"] = self.create_timer(self.lay_down_settle_s, _complete)
        self._posture_timer = timer_holder["timer"]

    def _complete_lay_down_transition(self) -> None:
        new_state = complete_posture_transition(
            self._current_state(),
            success=True,
            detail="robot_is_laying",
        )
        self._replace_state(
            new_state,
            event_name="lay_down_complete",
            detail="Robot is now laying.",
        )

    def _start_stand_up_transition(self) -> None:
        self._send_sport_request(ROBOT_SPORT_API_ID_STANDUP)
        self._emit_event(
            "stand_up_requested",
            recovery_enabled=self.stand_up_recovery_enabled,
            settle_s=self.stand_up_settle_s,
        )

        with self._stand_up_recovery_lock:
            if self._stand_up_recovery_thread is not None and self._stand_up_recovery_thread.is_alive():
                self._emit_event("stand_up_recovery_skipped", reason="already_running")
                return

            self._stand_up_recovery_thread = threading.Thread(
                target=self._run_stand_up_sequence,
                daemon=True,
            )
            self._stand_up_recovery_thread.start()

    def _run_stand_up_sequence(self) -> None:
        try:
            if self.stand_up_recovery_delay_s > 0.0:
                time.sleep(self.stand_up_recovery_delay_s)

            if self.stand_up_recovery_enabled and self._motion_mode_switcher_executable:
                command = [self._motion_mode_switcher_executable]
                if self.stand_up_recovery_network_interface:
                    command.extend(
                        [
                            "--network-interface",
                            self.stand_up_recovery_network_interface,
                        ]
                    )
                command.extend(
                    [
                        "--motion-mode",
                        self.stand_up_recovery_motion_mode,
                        "--gait",
                        self.stand_up_recovery_gait,
                        "--wait",
                        str(self.stand_up_recovery_wait_s),
                        "--retries",
                        str(self.stand_up_recovery_retries),
                        "--retry-interval",
                        str(self.stand_up_recovery_retry_interval_s),
                    ]
                )
                self.get_logger().info(
                    "Running stand-up recovery motion switcher with "
                    f'motion_mode="{self.stand_up_recovery_motion_mode}" '
                    f'gait="{self.stand_up_recovery_gait}".'
                )
                completed = subprocess.run(
                    command,
                    check=False,
                    capture_output=True,
                    text=True,
                )
                if completed.returncode != 0:
                    stdout_summary = self._summarize_process_output(completed.stdout)
                    stderr_summary = self._summarize_process_output(completed.stderr)
                    detail = (
                        f"stand_up_recovery_failed(returncode={completed.returncode},"
                        f" stdout={stdout_summary}, stderr={stderr_summary})"
                    )
                    self._replace_state(
                        complete_posture_transition(
                            self._current_state(),
                            success=False,
                            detail=detail,
                        ),
                        event_name="stand_up_failed",
                        detail=detail,
                    )
                    return
                self.get_logger().info(
                    "Stand-up recovery motion switcher completed successfully."
                )

            if self.stand_up_settle_s > 0.0:
                time.sleep(self.stand_up_settle_s)

            self._replace_state(
                complete_posture_transition(
                    self._current_state(),
                    success=True,
                    detail="robot_is_standing",
                ),
                event_name="stand_up_complete",
                detail="Robot is now standing.",
            )
        except Exception as exc:
            self._replace_state(
                complete_posture_transition(
                    self._current_state(),
                    success=False,
                    detail=f"stand_up_transition_failed: {exc}",
                ),
                event_name="stand_up_failed",
                detail=str(exc),
            )

    @staticmethod
    def _summarize_process_output(raw: str, max_lines: int = 6) -> str:
        lines = [line.strip() for line in str(raw).splitlines() if line.strip()]
        if not lines:
            return ""
        return " | ".join(lines[-max_lines:])

    def _cancel_posture_timer(self) -> None:
        if self._posture_timer is None:
            return
        self._posture_timer.cancel()
        self.destroy_timer(self._posture_timer)
        self._posture_timer = None

    def _follow_event_cb(self, msg: String) -> None:
        event = str(msg.data).strip()
        if event != "lost_target_timeout":
            return

        decision = request_mode_change(
            self._current_state(),
            requested_task_mode=TaskModes.IDLE,
            source="person_follow_controller",
            allow_preempt=True,
        )
        if decision.accepted:
            self._apply_decision(decision, event_name="follow_event_preempt")

    def _nav_candidate_cb(self, msg: Twist) -> None:
        routing = select_motion_routing(
            self._current_state(),
            follow_backend=self.follow_motion_backend,
        )
        if routing.base_source == "nav":
            self._publish_base_motion(msg)

    def _follow_candidate_cb(self, msg: Twist) -> None:
        routing = select_motion_routing(
            self._current_state(),
            follow_backend=self.follow_motion_backend,
        )
        if routing.base_source == "follow":
            self._publish_base_motion(msg)
            return
        if routing.follow_bridge_source == "follow":
            self._publish_follow_motion(msg)

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
                f'Failed to get TF {self.map_frame}->{self.base_frame}. Using origin pose: {exc}'
            )

        return pose


def main() -> None:
    rclpy.init()
    node = MissionSupervisorNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
