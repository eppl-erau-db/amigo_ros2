#!/usr/bin/env python3
"""
deliver_swag_action_server — orchestrates the swag-delivery mission.

Sequence (each step is cancel-aware):
  1. load the ArUco marker table (sidecar saved by "explore", else live map markers)
  2. Nav2 to a staging pose in front of the PICKUP marker
  3. ArUco visual-servo to the precise pickup pose (live base-frame detection)
  4. lock stance (BalanceStand) and play the "pickup" arm script
  5. (stub) verify the basket was picked up
  6. Nav2 + servo to the DELIVERY marker; play the "deliver" arm script
  7. wait for the hand-off ("amigo all done" -> /deliver/handoff_done) or timeout
  8. return to the PICKUP marker; play the "dropoff" arm script
  9. succeed

Motion: during DELIVER the mission supervisor routes /motion/candidate/nav ->
cmd_vel. The Nav2 legs publish there via the cmd_vel remap; the servo legs cancel
Nav2 and publish their own Twist to the SAME topic, so the supervisor + collision
monitor stay in the loop throughout. Runs on a dedicated SingleThreadedExecutor
because nav2_simple_commander's BasicNavigator nests rclpy spins.
"""
from __future__ import annotations

import math
import os

import rclpy
import tf2_ros
from geometry_msgs.msg import PoseStamped, Twist
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from nav_msgs.msg import OccupancyGrid
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile
from rclpy.task import Future
from rclpy.time import Time
from std_srvs.srv import Trigger
from unitree_api.msg import Request as UnitreeRequest
from visualization_msgs.msg import MarkerArray

from go2_interfaces.action import DeliverSwag
from go2_interfaces.srv import PlayArmScript

from go2_control.aruco_map_store import load_markers
from go2_control.delivery_geometry import (
    quat_from_yaw,
    servo_command,
    staging_pose,
)

ROBOT_SPORT_API_ID_BALANCESTAND = 1002


class DeliverSwagServer(Node):
    def __init__(self) -> None:
        super().__init__("deliver_swag_action_server")

        self.action_name = str(self.declare_parameter("action_name", "deliver_swag").value)
        self.map_frame = str(self.declare_parameter("map_frame", "map").value)
        self.base_frame = str(self.declare_parameter("base_frame", "base_link").value)
        self.maps_dir = os.path.expanduser(str(self.declare_parameter(
            "maps_dir", os.path.expanduser("~/amigo_maps")).value))
        self.default_map_name = str(self.declare_parameter("default_map_name", "venue").value)
        self.markers_base_topic = str(self.declare_parameter(
            "markers_base_topic", "/aruco/markers_base").value)
        self.markers_map_topic = str(self.declare_parameter(
            "markers_map_topic", "/aruco/markers_map").value)
        self.nav_candidate_topic = str(self.declare_parameter(
            "nav_candidate_topic", "/motion/candidate/nav").value)
        self.sport_request_topic = str(self.declare_parameter(
            "sport_request_topic", "/api/sport/request").value)
        self.arm_service_name = str(self.declare_parameter("arm_service_name", "/arm/play_script").value)
        self.handoff_service_name = str(self.declare_parameter(
            "handoff_service_name", "/deliver/handoff_done").value)

        self.pickup_marker_id = int(self.declare_parameter("pickup_marker_id", 0).value)
        self.delivery_marker_id = int(self.declare_parameter("delivery_marker_id", 1).value)
        self.pickup_script = str(self.declare_parameter("pickup_script", "pickup").value)
        self.deliver_script = str(self.declare_parameter("deliver_script", "deliver").value)
        self.dropoff_script = str(self.declare_parameter("dropoff_script", "dropoff").value)

        self.approach_standoff_m = float(self.declare_parameter("approach_standoff_m", 0.7).value)
        self.align_standoff_m = float(self.declare_parameter("align_standoff_m", 0.55).value)
        # Costmap-aware staging: a fixed-standoff staging pose can land too close to an obstacle
        # for the robot footprint, so SmacPlanner2D rejects it ("no valid path found") and the
        # mission dies in Nav2 recovery spins. Probe the SLAM /map and shrink/grow the standoff
        # until the staging point clears, then let the servo do the final align to align_standoff_m.
        self.map_topic = str(self.declare_parameter("map_topic", "/map").value)
        self.staging_min_clearance_m = float(
            self.declare_parameter("staging_min_clearance_m", 0.40).value)
        self.staging_standoff_min_m = float(self.declare_parameter("staging_standoff_min_m", 0.8).value)
        self.staging_standoff_max_m = float(self.declare_parameter("staging_standoff_max_m", 3.0).value)
        self.staging_standoff_step_m = max(
            0.05, float(self.declare_parameter("staging_standoff_step_m", 0.25).value))
        self.staging_occupied_cost = int(self.declare_parameter("staging_occupied_cost", 50).value)
        # Reacquire search: the head-mounted camera only moves when the body turns, so when the
        # marker isn't in view, rotate the body toward the marker's known map location (via TF)
        # until the camera reacquires it, then the closed-loop servo takes over.
        self.search_wz_max = float(self.declare_parameter("search_wz_max", 0.5).value)
        self.search_wz_min = float(self.declare_parameter("search_wz_min", 0.2).value)
        self.search_kw = float(self.declare_parameter("search_kw", 1.0).value)
        self.servo_kv = float(self.declare_parameter("servo_kv", 0.6).value)
        self.servo_kw = float(self.declare_parameter("servo_kw", 1.2).value)
        self.servo_vx_max = float(self.declare_parameter("servo_vx_max", 0.22).value)
        self.servo_wz_max = float(self.declare_parameter("servo_wz_max", 0.7).value)
        self.servo_pos_tol_m = float(self.declare_parameter("servo_pos_tol_m", 0.05).value)
        self.servo_yaw_tol_rad = float(self.declare_parameter("servo_yaw_tol_rad", 0.06).value)
        self.servo_dt_s = max(0.02, float(self.declare_parameter("servo_dt_s", 0.1).value))
        self.align_timeout_s = float(self.declare_parameter("align_timeout_s", 25.0).value)
        self.marker_timeout_s = float(self.declare_parameter("marker_timeout_s", 1.0).value)

        self.handoff_timeout_s = float(self.declare_parameter("handoff_timeout_s", 120.0).value)
        self.feedback_period_s = max(0.1, float(self.declare_parameter("feedback_period_s", 0.5).value))
        self.nav_server_timeout_s = float(self.declare_parameter("nav_server_timeout_s", 5.0).value)
        self.arm_server_wait_s = float(self.declare_parameter("arm_server_wait_s", 5.0).value)
        self.balance_settle_s = float(self.declare_parameter("balance_settle_s", 1.0).value)
        self.lock_stance = bool(self.declare_parameter("lock_stance", True).value)
        self.use_nav_legs = bool(self.declare_parameter("use_nav_legs", True).value)
        self.verify_pickup = bool(self.declare_parameter("verify_pickup", True).value)
        self.return_to_pickup = bool(self.declare_parameter("return_to_pickup", True).value)
        # use_arm=false: skip the arm service entirely and just wait arm_stub_wait_s at each
        # pickup/deliver/dropoff step, so the rest of the mission (nav + align + flow) can be
        # tested before the arm is mounted. Set use_arm:=true once the arm is on the dog.
        self.use_arm = bool(self.declare_parameter("use_arm", True).value)
        self.arm_stub_wait_s = max(0.0, float(self.declare_parameter("arm_stub_wait_s", 3.0).value))
        self.debug = bool(self.declare_parameter("debug", False).value)
        # Log every Nth servo iteration when debug is on (servo runs at ~1/servo_dt_s Hz).
        self.servo_debug_every = max(1, int(self.declare_parameter("servo_debug_every", 5).value))

        self.navigator = BasicNavigator()
        self.nav_pub = self.create_publisher(Twist, self.nav_candidate_topic, 10)
        self.sport_pub = self.create_publisher(UnitreeRequest, self.sport_request_topic, 10)
        self.arm_client = self.create_client(PlayArmScript, self.arm_service_name)

        self._live_base: dict[int, tuple[float, float, float]] = {}  # id -> (x, y, stamp_s)
        self._live_map: dict[int, tuple[float, float, float, float, float, float, float]] = {}
        self._map_grid: OccupancyGrid | None = None
        self._handoff_done = False

        self.create_subscription(MarkerArray, self.markers_base_topic, self._base_markers_cb, 10)
        self.create_subscription(MarkerArray, self.markers_map_topic, self._map_markers_cb, 10)
        map_qos = QoSProfile(depth=1)
        map_qos.durability = DurabilityPolicy.TRANSIENT_LOCAL  # SLAM /map is latched
        self.create_subscription(OccupancyGrid, self.map_topic, self._map_cb, map_qos)
        self.create_service(Trigger, self.handoff_service_name, self._handoff_cb)
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        self._goal_active = False
        self._action_server = ActionServer(
            self, DeliverSwag, self.action_name,
            execute_callback=self._execute_cb,
            goal_callback=self._goal_cb,
            cancel_callback=self._cancel_cb,
        )
        self.get_logger().info(
            f"deliver_swag_action_server ready. action={self.action_name} "
            f"pickup_id={self.pickup_marker_id} delivery_id={self.delivery_marker_id} "
            f"maps_dir={self.maps_dir} arm={self.arm_service_name} use_arm={self.use_arm} "
            f"debug={self.debug}")

    def _dbg(self, msg: str) -> None:
        if self.debug:
            self.get_logger().info(f"[deliver] {msg}")

    # --------------------------------------------------------------- callbacks
    def _goal_cb(self, goal_req):
        del goal_req
        if self._goal_active:
            self.get_logger().warn("Rejecting DeliverSwag goal; a mission is already active.")
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def _cancel_cb(self, goal_handle):
        del goal_handle
        self.get_logger().info("DeliverSwag cancel requested.")
        return CancelResponse.ACCEPT

    def _handoff_cb(self, request, response):
        del request
        self._handoff_done = True
        response.success = True
        response.message = "hand-off acknowledged"
        self.get_logger().info("Hand-off signal received.")
        return response

    def _base_markers_cb(self, msg: MarkerArray) -> None:
        now = self._now_s()
        for m in msg.markers:
            self._live_base[int(m.id)] = (float(m.pose.position.x), float(m.pose.position.y), now)

    def _map_markers_cb(self, msg: MarkerArray) -> None:
        for m in msg.markers:
            p, o = m.pose.position, m.pose.orientation
            self._live_map[int(m.id)] = (p.x, p.y, p.z, o.x, o.y, o.z, o.w)

    def _map_cb(self, msg: OccupancyGrid) -> None:
        self._map_grid = msg

    # ----------------------------------------------------------------- helpers
    def _now_s(self) -> float:
        return self.get_clock().now().nanoseconds * 1e-9

    async def _sleep_async(self, duration_s: float) -> None:
        if duration_s <= 0.0:
            return
        future: Future = Future()
        box: dict[str, object] = {"timer": None, "done": False}

        def _complete():
            if box["done"]:
                return
            box["done"] = True
            if not future.done():
                future.set_result(True)

        box["timer"] = self.create_timer(duration_s, _complete)
        try:
            await future
        finally:
            timer = box.get("timer")
            if timer is not None:
                timer.cancel()
                self.destroy_timer(timer)

    def _load_marker_table(self, map_name: str) -> dict:
        """Return {id: (x, y, qx, qy, qz, qw)} in the map frame from the sidecar,
        falling back to live /aruco/markers_map detections."""
        name = (map_name or self.default_map_name).strip() or self.default_map_name
        sidecar = os.path.join(self.maps_dir, name + ".aruco.yaml")
        table: dict[int, tuple] = {}
        if os.path.isfile(sidecar):
            try:
                _frame, markers = load_markers(sidecar)
                for mid, est in markers.items():
                    table[int(mid)] = (est.x, est.y, est.qx, est.qy, est.qz, est.qw)
                self.get_logger().info(f"Loaded {len(table)} markers from {sidecar}.")
                return table
            except Exception as exc:
                self.get_logger().warn(f"Failed to read {sidecar}: {exc}; trying live markers.")
        for mid, (x, y, _z, qx, qy, qz, qw) in self._live_map.items():
            table[int(mid)] = (x, y, qx, qy, qz, qw)
        if table:
            self.get_logger().info(f"Using {len(table)} live map markers (no sidecar).")
        return table

    def _staging_clear(self, x: float, y: float) -> bool:
        """True if no occupied map cell lies within staging_min_clearance_m of (x, y). Mirrors why
        SmacPlanner2D rejects a goal — the robot footprint can't overlap an obstacle."""
        grid = self._map_grid
        if grid is None or grid.info.resolution <= 0.0:
            return True  # no map yet — don't block; let Nav2 decide
        info = grid.info
        res = info.resolution
        rad = int(math.ceil(self.staging_min_clearance_m / res))
        cx = int((x - info.origin.position.x) / res)
        cy = int((y - info.origin.position.y) / res)
        w, h, data = info.width, info.height, grid.data
        r2 = rad * rad
        for i in range(-rad, rad + 1):
            for j in range(-rad, rad + 1):
                if i * i + j * j > r2:
                    continue
                gx, gy = cx + j, cy + i
                if gx < 0 or gy < 0 or gx >= w or gy >= h:
                    continue  # off-map cells count as unknown/traversable
                if data[gy * w + gx] >= self.staging_occupied_cost:
                    return False
        return True

    def _staging_standoff_candidates(self) -> list:
        """Standoff distances to try, nearest the configured approach_standoff_m first (and the
        nominal value tested exactly, not just the nearest grid step)."""
        cands = [round(self.approach_standoff_m, 3)]
        s = self.staging_standoff_min_m
        while s <= self.staging_standoff_max_m + 1e-6:
            v = round(s, 3)
            if v not in cands:
                cands.append(v)
            s += self.staging_standoff_step_m
        cands.sort(key=lambda v: abs(v - self.approach_standoff_m))
        return cands

    def _select_staging(self, marker_map: tuple) -> tuple:
        """Pick a staging (x, y, yaw) on the marker's outward normal whose footprint is clear,
        preferring approach_standoff_m and falling back to nearer/farther standoffs."""
        mx, my, qx, qy, qz, qw = marker_map
        for standoff in self._staging_standoff_candidates():
            sx, sy, yaw = staging_pose(mx, my, qx, qy, qz, qw, standoff)
            if self._staging_clear(sx, sy):
                if abs(standoff - self.approach_standoff_m) > 1e-3:
                    self.get_logger().warn(
                        f"staging: nominal {self.approach_standoff_m:.2f} m standoff is too close "
                        f"to an obstacle; using {standoff:.2f} m (clear). Servo still targets "
                        f"align_standoff_m={self.align_standoff_m:.2f} m.")
                else:
                    self._dbg(f"staging: standoff {standoff:.2f} m is clear.")
                return sx, sy, yaw
        self.get_logger().warn(
            f"staging: no clear standoff found on the marker normal; using nominal "
            f"{self.approach_standoff_m:.2f} m and letting Nav2 try anyway.")
        return staging_pose(mx, my, qx, qy, qz, qw, self.approach_standoff_m)

    def _staging_pose_stamped(self, marker_map: tuple) -> PoseStamped:
        sx, sy, yaw = self._select_staging(marker_map)
        ps = PoseStamped()
        ps.header.frame_id = self.map_frame
        ps.header.stamp = self.get_clock().now().to_msg()
        ps.pose.position.x = sx
        ps.pose.position.y = sy
        oqx, oqy, oqz, oqw = quat_from_yaw(yaw)
        ps.pose.orientation.x, ps.pose.orientation.y = oqx, oqy
        ps.pose.orientation.z, ps.pose.orientation.w = oqz, oqw
        return ps

    def _send_balance_stand(self) -> None:
        req = UnitreeRequest()
        req.header.identity.api_id = ROBOT_SPORT_API_ID_BALANCESTAND
        self.sport_pub.publish(req)

    def _publish_zero(self) -> None:
        self.nav_pub.publish(Twist())

    def _reacquire_wz(self, marker_map: tuple):
        """Angular velocity (rad/s, +CCW) to rotate the body toward the marker's known map
        position so the head camera can reacquire it. None if the robot-pose TF isn't available."""
        try:
            tf = self.tf_buffer.lookup_transform(self.base_frame, self.map_frame, Time())
        except Exception as exc:
            self._dbg(f"reacquire: TF {self.base_frame}<-{self.map_frame} unavailable: {exc}")
            return None
        mx, my = float(marker_map[0]), float(marker_map[1])
        q = tf.transform.rotation
        t = tf.transform.translation
        yaw = math.atan2(2.0 * (q.w * q.z + q.x * q.y),
                         1.0 - 2.0 * (q.y * q.y + q.z * q.z))
        cos_y, sin_y = math.cos(yaw), math.sin(yaw)
        # marker position expressed in the base frame (x forward, y left)
        bx = cos_y * mx - sin_y * my + t.x
        by = sin_y * mx + cos_y * my + t.y
        bearing = math.atan2(by, bx)
        wz = max(-self.search_wz_max, min(self.search_wz_max, self.search_kw * bearing))
        if abs(wz) < self.search_wz_min:
            wz = math.copysign(self.search_wz_min, bearing if bearing != 0.0 else 1.0)
        return wz

    # --------------------------------------------------------------- mission steps
    async def _nav_to(self, goal_handle, goal_pose: PoseStamped, stage: str) -> str:
        if not self.use_nav_legs:
            self._dbg(f"{stage}: use_nav_legs=false, skipping Nav2 leg")
            return "ok"
        self._dbg(
            f"{stage}: goToPose staging=({goal_pose.pose.position.x:.2f}, "
            f"{goal_pose.pose.position.y:.2f}) frame={goal_pose.header.frame_id}")
        try:
            self.navigator.goToPose(goal_pose)
        except Exception as exc:
            self.get_logger().error(f"goToPose failed in {stage}: {exc}")
            return "nav_error"
        while not self.navigator.isTaskComplete():
            if goal_handle.is_cancel_requested:
                self._cancel_nav()
                return "canceled"
            goal_handle.publish_feedback(self._feedback(stage))
            await self._sleep_async(self.feedback_period_s)
        result = self.navigator.getResult()
        self._dbg(f"{stage}: Nav2 result={result}")
        if result == TaskResult.SUCCEEDED:
            return "ok"
        if result == TaskResult.CANCELED:
            return "canceled"
        return "nav_failed"

    def _cancel_nav(self) -> None:
        try:
            self.navigator.cancelTask()
        except Exception:
            pass

    async def _servo_align(self, goal_handle, marker_id: int, marker_map: tuple, stage: str) -> str:
        # Stop Nav2 so the servo owns /motion/candidate/nav.
        self._cancel_nav()
        await self._sleep_async(0.2)
        self._dbg(f"{stage}: servo to marker {marker_id}, standoff={self.align_standoff_m:.2f}m")
        deadline = self._now_s() + self.align_timeout_s
        seen_any = False
        i = 0
        while self._now_s() < deadline:
            if goal_handle.is_cancel_requested:
                self._publish_zero()
                return "canceled"
            obs = self._live_base.get(marker_id)
            fresh = obs is not None and (self._now_s() - obs[2]) <= self.marker_timeout_s
            if not fresh:
                # Marker not in view: the camera is fixed to the body, so rotate toward the
                # marker's known map location to bring it into frame. Once a fresh detection
                # lands the closed-loop servo below takes over.
                wz = self._reacquire_wz(marker_map)
                if wz is None:
                    self._publish_zero()  # no robot-pose TF yet — hold
                else:
                    tw = Twist()
                    tw.angular.z = wz
                    self.nav_pub.publish(tw)
                if self.debug and i % self.servo_debug_every == 0:
                    how = (f"rotating to reacquire (wz={wz:.2f})" if wz is not None
                           else "holding (no TF)")
                    self._dbg(f"{stage}: marker {marker_id} not visible, {how}")
                goal_handle.publish_feedback(self._feedback(f"{stage}_searching"))
                await self._sleep_async(self.servo_dt_s)
                i += 1
                continue
            seen_any = True
            vx, wz, aligned = servo_command(
                obs[0], obs[1], self.align_standoff_m,
                kv=self.servo_kv, kw=self.servo_kw,
                vx_max=self.servo_vx_max, wz_max=self.servo_wz_max,
                pos_tol_m=self.servo_pos_tol_m, yaw_tol_rad=self.servo_yaw_tol_rad,
            )
            if self.debug and i % self.servo_debug_every == 0:
                rng = math.hypot(obs[0], obs[1])
                self._dbg(
                    f"{stage}: marker_base=({obs[0]:.3f},{obs[1]:.3f}) range={rng:.3f} "
                    f"-> vx={vx:.3f} wz={wz:.3f}")
            if aligned:
                self._publish_zero()
                self.get_logger().info(f"{stage}: aligned to marker {marker_id}.")
                return "ok"
            tw = Twist()
            tw.linear.x = vx
            tw.angular.z = wz
            self.nav_pub.publish(tw)
            goal_handle.publish_feedback(self._feedback(stage))
            await self._sleep_async(self.servo_dt_s)
            i += 1
        self._publish_zero()
        self._dbg(f"{stage}: align ended seen_any={seen_any}")
        return "align_timeout" if seen_any else "marker_not_seen"

    async def _run_arm(self, goal_handle, script: str, stage: str) -> str:
        if not self.use_arm:
            # Arm not mounted yet: pretend the motion ran by waiting, so the rest of
            # the mission (nav + align + flow + hand-off) can be validated.
            self.get_logger().info(
                f"{stage}: arm disabled (use_arm=false) — waiting {self.arm_stub_wait_s:.1f}s "
                f"instead of running '{script}'.")
            deadline = self._now_s() + self.arm_stub_wait_s
            while self._now_s() < deadline:
                if goal_handle.is_cancel_requested:
                    return "canceled"
                goal_handle.publish_feedback(self._feedback(f"{stage}_stub"))
                await self._sleep_async(self.feedback_period_s)
            return "ok"
        if not self.arm_client.wait_for_service(timeout_sec=self.arm_server_wait_s):
            self.get_logger().error(f"Arm service {self.arm_service_name} unavailable.")
            return "arm_unavailable"
        req = PlayArmScript.Request()
        req.script = script
        req.speed = 0.0  # node default
        self._dbg(f"{stage}: calling arm script '{script}'")
        future = self.arm_client.call_async(req)
        while not future.done():
            if goal_handle.is_cancel_requested:
                return "canceled"
            goal_handle.publish_feedback(self._feedback(stage))
            await self._sleep_async(self.feedback_period_s)
        try:
            resp = future.result()
        except Exception as exc:
            self.get_logger().error(f"Arm call failed in {stage}: {exc}")
            return "arm_error"
        if not resp.success:
            self.get_logger().error(f"Arm script '{script}' failed: {resp.message}")
            return "arm_failed"
        self._dbg(f"{stage}: arm script '{script}' done ({resp.duration_s:.1f}s)")
        return "ok"

    async def _await_handoff(self, goal_handle) -> str:
        self._handoff_done = False
        self._dbg(f"await_handoff: waiting up to {self.handoff_timeout_s:.0f}s for 'all done'")
        deadline = self._now_s() + self.handoff_timeout_s
        while self._now_s() < deadline:
            if goal_handle.is_cancel_requested:
                return "canceled"
            if self._handoff_done:
                return "ok"
            goal_handle.publish_feedback(self._feedback("await_handoff"))
            await self._sleep_async(self.feedback_period_s)
        self.get_logger().warn("Hand-off wait timed out; proceeding to drop-off.")
        return "timeout"

    async def _approach_and_arm(self, goal_handle, marker_id, marker_map, script, label) -> str:
        self._dbg(f"=== {label}: marker {marker_id} map=({marker_map[0]:.2f},{marker_map[1]:.2f}) ===")
        rc = await self._nav_to(goal_handle, self._staging_pose_stamped(marker_map), f"nav_to_{label}")
        if rc != "ok":
            return rc
        rc = await self._servo_align(goal_handle, marker_id, marker_map, f"aligning_{label}")
        if rc != "ok":
            return rc
        if self.lock_stance:
            self._dbg(f"{label}: BalanceStand lock + settle {self.balance_settle_s:.1f}s")
            self._send_balance_stand()
            await self._sleep_async(self.balance_settle_s)
        return await self._run_arm(goal_handle, script, f"arm_{label}")

    def _feedback(self, stage: str) -> DeliverSwag.Feedback:
        fb = DeliverSwag.Feedback()
        fb.stage = str(stage)
        return fb

    @staticmethod
    def _result(success: bool, reason: str) -> DeliverSwag.Result:
        res = DeliverSwag.Result()
        res.success = bool(success)
        res.reason = str(reason)
        return res

    # ----------------------------------------------------------------- execute
    async def _execute_cb(self, goal_handle):
        self._goal_active = True
        self.get_logger().info("DeliverSwag mission started.")
        try:
            table = self._load_marker_table(goal_handle.request.map_name)
            self._dbg(f"marker table ids={sorted(table)}")
            pickup = table.get(self.pickup_marker_id)
            delivery = table.get(self.delivery_marker_id)
            if pickup is None or delivery is None:
                goal_handle.abort()
                missing = []
                if pickup is None:
                    missing.append(f"pickup({self.pickup_marker_id})")
                if delivery is None:
                    missing.append(f"delivery({self.delivery_marker_id})")
                return self._result(False, f"marker(s) not found: {', '.join(missing)}")

            def _bail(rc, where):
                self.get_logger().warn(f"DeliverSwag bailing: '{rc}' during {where}.")
                if rc == "canceled":
                    goal_handle.canceled()
                    return self._result(False, f"canceled during {where}")
                goal_handle.abort()
                return self._result(False, f"{rc} during {where}")

            # --- PICKUP ---
            rc = await self._approach_and_arm(
                goal_handle, self.pickup_marker_id, pickup, self.pickup_script, "pickup")
            if rc != "ok":
                return _bail(rc, "pickup")

            if self.verify_pickup and not self._verify_pickup_stub():
                goal_handle.abort()
                return self._result(False, "pickup verification failed")

            # --- DELIVERY ---
            rc = await self._approach_and_arm(
                goal_handle, self.delivery_marker_id, delivery, self.deliver_script, "delivery")
            if rc != "ok":
                return _bail(rc, "delivery")

            # --- HAND-OFF ---
            rc = await self._await_handoff(goal_handle)
            if rc == "canceled":
                return _bail(rc, "handoff")

            # --- RETURN + DROP-OFF ---
            if self.return_to_pickup:
                rc = await self._approach_and_arm(
                    goal_handle, self.pickup_marker_id, pickup, self.dropoff_script, "dropoff")
                if rc != "ok":
                    return _bail(rc, "dropoff")

            goal_handle.succeed()
            self.get_logger().info("DeliverSwag mission complete.")
            return self._result(True, "delivery complete")
        finally:
            self._publish_zero()
            self._goal_active = False

    def _verify_pickup_stub(self) -> bool:
        # TODO(user): replace with a real pickup check (motor torque, weight, vision).
        return True


def main() -> None:
    rclpy.init()
    node = DeliverSwagServer()
    # Dedicated executor: BasicNavigator nests rclpy spins on the global executor.
    executor = SingleThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    finally:
        executor.shutdown()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
