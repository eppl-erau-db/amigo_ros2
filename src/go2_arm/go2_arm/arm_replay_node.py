#!/usr/bin/env python3
"""
arm_replay_node — hosts the ``PlayArmScript`` service.

On request it resolves ``<scripts_dir>/<script>.csv`` and replays the recorded
CubeMars-arm trajectory on the gs_usb CAN bus, holds the final pose briefly, and
returns success. With ``dry_run:=true`` (default) it validates and time-simulates
the trajectory WITHOUT touching CAN hardware, so the full delivery pipeline can be
exercised before the arm is wired. Flip ``dry_run:=false`` to drive the real arm.

The replay blocks the service callback for the duration of the motion; this node
does nothing else, so that is intentional and safe.
"""
from __future__ import annotations

import os
import threading
import time

import rclpy
from rclpy.node import Node

from go2_interfaces.srv import PlayArmScript

from go2_arm.arm_trajectory import (
    load_frames,
    replay_frames,
    trajectory_duration,
)


class ArmReplayNode(Node):
    def __init__(self) -> None:
        super().__init__("arm_replay_node")

        default_scripts_dir = os.path.expanduser("~/amigo_arm_scripts")
        self.scripts_dir = str(
            self.declare_parameter("scripts_dir", default_scripts_dir).value
        ) or default_scripts_dir
        self.motor_ids = [int(x) for x in self.declare_parameter("motor_ids", [1, 2, 3]).value]
        self.enc_offsets = [float(x) for x in self.declare_parameter("enc_offsets", [0.0, 0.0, 0.0]).value]
        self.bitrate = int(self.declare_parameter("bitrate", 1_000_000).value)
        self.acc_limit = float(self.declare_parameter("acc_limit", 2.0).value)
        self.min_vel = float(self.declare_parameter("min_vel", 0.05).value)
        self.default_speed = max(0.01, float(self.declare_parameter("default_speed", 1.0).value))
        self.settle_s = max(0.0, float(self.declare_parameter("settle_s", 1.0).value))
        self.hold_after_replay = bool(self.declare_parameter("hold_after_replay", True).value)
        self.dry_run = bool(self.declare_parameter("dry_run", True).value)
        self.can_debug = bool(self.declare_parameter("can_debug", False).value)
        self.debug = bool(self.declare_parameter("debug", False).value)
        self.service_name = str(self.declare_parameter("service_name", "/arm/play_script").value)

        if len(self.enc_offsets) < len(self.motor_ids):
            self.enc_offsets += [0.0] * (len(self.motor_ids) - len(self.enc_offsets))

        self._busy_lock = threading.Lock()
        self._bus = None
        self._motor_map: dict[int, object] = {}

        self._srv = self.create_service(PlayArmScript, self.service_name, self._play_cb)

        self.get_logger().info(
            f"arm_replay_node ready. service={self.service_name} "
            f"scripts_dir={self.scripts_dir} motors={self.motor_ids} "
            f"dry_run={self.dry_run}"
        )
        if self.dry_run:
            self.get_logger().warn(
                "arm_replay_node is in DRY-RUN: trajectories are validated and time-simulated "
                "but the CAN bus is NOT driven. Set dry_run:=false to move the real arm."
            )

    # ------------------------------------------------------------------ hardware
    def _ensure_bus(self) -> str | None:
        """Lazily open the CAN bus + motors. Returns an error string or None."""
        if self._bus is not None:
            return None
        try:
            from go2_arm.ak45_motor import AK45Motor, MotorBus

            motors = [
                AK45Motor(mid, self.enc_offsets[i], None)
                for i, mid in enumerate(self.motor_ids)
            ]
            bus = MotorBus(motors=motors, bitrate=self.bitrate, debug=self.can_debug)
            for m in motors:
                m.bus = bus
            self._bus = bus
            self._motor_map = {m.can_id: m for m in motors}
            self.get_logger().info(f"Opened arm CAN bus; motors={list(self._motor_map)}.")
            return None
        except Exception as exc:  # pragma: no cover - hardware path
            return f"failed to open arm CAN bus: {exc}"

    def _resolve_script_path(self, script: str) -> str:
        name = str(script).strip()
        if not name:
            raise ValueError("empty script name")
        # Allow a bare name ("pickup") or a full/relative .csv path.
        if name.endswith(".csv") and os.path.isabs(name):
            return name
        if name.endswith(".csv"):
            return os.path.join(self.scripts_dir, name)
        return os.path.join(self.scripts_dir, f"{name}.csv")

    # ------------------------------------------------------------------ service
    def _play_cb(self, request: PlayArmScript.Request, response: PlayArmScript.Response):
        speed = request.speed if request.speed and request.speed > 0.0 else self.default_speed

        if not self._busy_lock.acquire(blocking=False):
            response.success = False
            response.message = "arm is busy replaying another script"
            response.duration_s = 0.0
            return response
        try:
            try:
                path = self._resolve_script_path(request.script)
            except ValueError as exc:
                response.success = False
                response.message = str(exc)
                response.duration_s = 0.0
                return response

            if self.debug:
                self.get_logger().info(f"[arm] resolved '{request.script}' -> {path}")
            if not os.path.isfile(path):
                response.success = False
                response.message = f"script not found: {path}"
                response.duration_s = 0.0
                self.get_logger().error(response.message)
                return response

            try:
                frames = load_frames(path)
            except Exception as exc:
                response.success = False
                response.message = f"failed to load '{path}': {exc}"
                response.duration_s = 0.0
                self.get_logger().error(response.message)
                return response

            duration = trajectory_duration(frames)
            self.get_logger().info(
                f'Replaying "{request.script}" ({len(frames)} frames, '
                f"{duration:.1f}s, speed={speed:.2f}, dry_run={self.dry_run})."
            )

            t0 = time.monotonic()
            if self.dry_run:
                # Time-simulate so downstream mission timing is realistic.
                sim = min(duration / speed, 30.0)
                if self.debug:
                    self.get_logger().info(f"[arm] dry-run simulating {sim:.1f}s")
                if sim > 0:
                    time.sleep(sim)
                response.success = True
                response.message = f"dry-run replayed '{request.script}'"
                response.duration_s = float(time.monotonic() - t0)
                return response

            err = self._ensure_bus()
            if err is not None:
                response.success = False
                response.message = err
                response.duration_s = 0.0
                self.get_logger().error(err)
                return response

            def _send(mid, pos, vel_limit, acc_limit):
                motor = self._motor_map.get(mid)
                if motor is not None:
                    motor.set_position(pos, vel_limit=vel_limit, acc_limit=acc_limit)

            last_pos = replay_frames(
                frames,
                _send,
                speed=speed,
                acc_limit=self.acc_limit,
                min_vel=self.min_vel,
            )
            if self.hold_after_replay and last_pos:
                self._hold(last_pos, self.settle_s)

            response.success = True
            response.message = f"replayed '{request.script}'"
            response.duration_s = float(time.monotonic() - t0)
            return response
        finally:
            self._busy_lock.release()

    def _hold(self, last_pos: dict[int, float], duration_s: float) -> None:  # pragma: no cover - hardware path
        if duration_s <= 0.0:
            return
        t_end = time.monotonic() + duration_s
        while time.monotonic() < t_end:
            for mid, pos in last_pos.items():
                motor = self._motor_map.get(mid)
                if motor is not None:
                    motor.set_position(pos, vel_limit=0.1, acc_limit=self.acc_limit)
            time.sleep(0.01)

    def destroy_node(self) -> bool:
        try:
            if self._bus is not None:
                self._bus.close()
        except Exception:  # pragma: no cover
            pass
        return super().destroy_node()


def main() -> None:
    rclpy.init()
    node = ArmReplayNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
