from __future__ import annotations

import math
from dataclasses import dataclass, field


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def wrap_angle(angle_rad: float) -> float:
    wrapped = math.fmod(angle_rad + math.pi, 2.0 * math.pi)
    if wrapped < 0.0:
        wrapped += 2.0 * math.pi
    return wrapped - math.pi


@dataclass(frozen=True)
class Twist2D:
    vx: float = 0.0
    vy: float = 0.0
    wz: float = 0.0


@dataclass(frozen=True)
class Pose2D:
    x: float = 0.0
    y: float = 0.0
    yaw: float = 0.0


@dataclass(frozen=True)
class FollowControlParams:
    desired_distance_m: float = 0.75
    distance_band_m: float = 0.10
    min_follow_distance_m: float = 0.60
    lateral_deadband_m: float = 0.10
    yaw_deadband_rad: float = 0.10
    forward_gain: float = 0.9
    lateral_gain: float = 1.1
    yaw_gain: float = 1.8
    max_forward_speed_mps: float = 0.60
    max_reverse_speed_mps: float = 0.35
    max_lateral_speed_mps: float = 0.30
    max_yaw_rate_radps: float = 1.20
    yaw_priority_start_rad: float = 0.20
    yaw_freeze_rad: float = 0.45
    max_linear_accel_mps2: float = 1.20
    max_lateral_accel_mps2: float = 0.90
    max_yaw_accel_radps2: float = 3.00
    use_strafe: bool = False


@dataclass(frozen=True)
class FootprintParams:
    forward_extent_m: float = 0.36
    rear_extent_m: float = 0.80
    half_width_m: float = 0.20
    padding_m: float = 0.05


@dataclass(frozen=True)
class SafetyOracleParams:
    horizon_s: float = 0.80
    sim_dt_s: float = 0.10
    occupied_threshold: int = 55
    footprint: FootprintParams = field(default_factory=FootprintParams)


@dataclass(frozen=True)
class GridMap2D:
    resolution: float
    width: int
    height: int
    origin_x: float
    origin_y: float
    data: tuple[int, ...]

    def value_at(self, world_x: float, world_y: float) -> int | None:
        mx = int(math.floor((world_x - self.origin_x) / self.resolution))
        my = int(math.floor((world_y - self.origin_y) / self.resolution))
        if mx < 0 or my < 0 or mx >= self.width or my >= self.height:
            return None
        index = (my * self.width) + mx
        if index < 0 or index >= len(self.data):
            return None
        return int(self.data[index])

    def is_occupied(self, world_x: float, world_y: float, threshold: int) -> bool:
        value = self.value_at(world_x, world_y)
        if value is None:
            return True
        if value < 0:
            return False
        return value >= threshold


class FollowStates:
    IDLE = "IDLE"
    WAITING_FOR_TARGET = "WAITING_FOR_TARGET"
    FOLLOWING = "FOLLOWING"
    REACQUIRE = "REACQUIRE"
    LOST_SIT = "LOST_SIT"


@dataclass
class FollowStateMachine:
    reacquire_timeout_s: float
    sit_on_loss_timeout_s: float
    state: str = FollowStates.IDLE
    state_enter_time_s: float = 0.0
    last_target_seen_time_s: float | None = None

    def handle_follow_command(self, now_s: float) -> str:
        self.state = FollowStates.WAITING_FOR_TARGET
        self.state_enter_time_s = now_s
        self.last_target_seen_time_s = None
        return self.state

    def handle_stop_command(self, now_s: float) -> str:
        self.state = FollowStates.IDLE
        self.state_enter_time_s = now_s
        return self.state

    def note_target_seen(self, now_s: float) -> str:
        self.last_target_seen_time_s = now_s
        if self.state != FollowStates.IDLE:
            self.state = FollowStates.FOLLOWING
            self.state_enter_time_s = now_s
        return self.state

    def update(self, now_s: float, has_fresh_target: bool) -> str:
        if self.state == FollowStates.IDLE:
            return self.state

        if has_fresh_target:
            return self.note_target_seen(now_s)

        if self.state == FollowStates.WAITING_FOR_TARGET:
            return self.state

        if self.state == FollowStates.FOLLOWING:
            self.state = FollowStates.REACQUIRE
            self.state_enter_time_s = now_s
            return self.state

        if self.state == FollowStates.REACQUIRE and self.loss_age_s(now_s) >= self.sit_on_loss_timeout_s:
            self.state = FollowStates.LOST_SIT
            self.state_enter_time_s = now_s

        return self.state

    def loss_age_s(self, now_s: float) -> float:
        if self.last_target_seen_time_s is None:
            return math.inf
        return max(0.0, now_s - self.last_target_seen_time_s)

    def reacquire_motion_enabled(self, now_s: float) -> bool:
        return self.state == FollowStates.REACQUIRE and self.loss_age_s(now_s) <= self.reacquire_timeout_s


def compute_nominal_follow_command(
    target_x_m: float,
    target_y_m: float,
    params: FollowControlParams,
) -> Twist2D:
    range_m = math.hypot(target_x_m, target_y_m)
    forward_error = range_m - params.desired_distance_m
    lateral_error = target_y_m
    bearing_rad = math.atan2(target_y_m, target_x_m)
    too_close = range_m < params.min_follow_distance_m

    vx = 0.0
    if too_close or abs(forward_error) > params.distance_band_m:
        if forward_error >= 0.0:
            vx = clamp(
                params.forward_gain * forward_error,
                0.0,
                params.max_forward_speed_mps,
            )
        else:
            vx = clamp(
                params.forward_gain * forward_error,
                -params.max_reverse_speed_mps,
                0.0,
            )

    vy = 0.0
    if params.use_strafe and abs(lateral_error) > params.lateral_deadband_m:
        vy = clamp(
            params.lateral_gain * lateral_error,
            -params.max_lateral_speed_mps,
            params.max_lateral_speed_mps,
        )

    wz = 0.0
    if abs(bearing_rad) > params.yaw_deadband_rad:
        wz = clamp(
            params.yaw_gain * bearing_rad,
            -params.max_yaw_rate_radps,
            params.max_yaw_rate_radps,
        )

    vx_scale, vy_scale = _translation_scales(abs(bearing_rad), params)
    if too_close and vx < 0.0:
        vx_scale = max(vx_scale, 0.75)
    return Twist2D(vx=vx * vx_scale, vy=vy * vy_scale, wz=wz)


def apply_acceleration_limits(
    previous: Twist2D,
    desired: Twist2D,
    params: FollowControlParams,
    dt_s: float,
) -> Twist2D:
    if dt_s <= 0.0:
        return desired
    return Twist2D(
        vx=_step_toward(previous.vx, desired.vx, params.max_linear_accel_mps2 * dt_s),
        vy=_step_toward(previous.vy, desired.vy, params.max_lateral_accel_mps2 * dt_s),
        wz=_step_toward(previous.wz, desired.wz, params.max_yaw_accel_radps2 * dt_s),
    )


def select_safe_command(
    nominal: Twist2D,
    start_pose: Pose2D,
    grid: GridMap2D,
    safety_params: SafetyOracleParams,
) -> tuple[Twist2D, bool]:
    best_command: Twist2D | None = None
    best_score = math.inf

    for candidate in generate_candidate_commands(nominal):
        if trajectory_is_safe(candidate, start_pose, grid, safety_params):
            score = _command_score(candidate, nominal)
            if score < best_score:
                best_score = score
                best_command = candidate

    if best_command is not None:
        return best_command, True

    yaw_only = Twist2D(vx=0.0, vy=0.0, wz=nominal.wz)
    if abs(yaw_only.wz) > 1.0e-6 and trajectory_is_safe(yaw_only, start_pose, grid, safety_params):
        return yaw_only, False

    return Twist2D(), False


def generate_candidate_commands(nominal: Twist2D) -> list[Twist2D]:
    candidates = [
        nominal,
        Twist2D(vx=nominal.vx * 0.75, vy=nominal.vy * 0.75, wz=nominal.wz),
        Twist2D(vx=nominal.vx * 0.50, vy=nominal.vy * 0.50, wz=nominal.wz),
        Twist2D(vx=0.0, vy=nominal.vy, wz=nominal.wz),
        Twist2D(vx=nominal.vx, vy=0.0, wz=nominal.wz),
        Twist2D(vx=0.0, vy=0.0, wz=nominal.wz),
        Twist2D(),
    ]

    unique_candidates: list[Twist2D] = []
    seen = set()
    for candidate in candidates:
        key = (
            round(candidate.vx, 4),
            round(candidate.vy, 4),
            round(candidate.wz, 4),
        )
        if key not in seen:
            unique_candidates.append(candidate)
            seen.add(key)
    return unique_candidates


def trajectory_is_safe(
    command: Twist2D,
    start_pose: Pose2D,
    grid: GridMap2D,
    safety_params: SafetyOracleParams,
) -> bool:
    steps = max(1, int(math.ceil(safety_params.horizon_s / max(1.0e-3, safety_params.sim_dt_s))))
    pose = Pose2D(x=start_pose.x, y=start_pose.y, yaw=start_pose.yaw)

    for _ in range(steps):
        if footprint_in_collision(pose, grid, safety_params):
            return False
        pose = integrate_pose(pose, command, safety_params.sim_dt_s)

    return not footprint_in_collision(pose, grid, safety_params)


def integrate_pose(pose: Pose2D, command: Twist2D, dt_s: float) -> Pose2D:
    cos_yaw = math.cos(pose.yaw)
    sin_yaw = math.sin(pose.yaw)
    world_vx = (cos_yaw * command.vx) - (sin_yaw * command.vy)
    world_vy = (sin_yaw * command.vx) + (cos_yaw * command.vy)
    return Pose2D(
        x=pose.x + (world_vx * dt_s),
        y=pose.y + (world_vy * dt_s),
        yaw=wrap_angle(pose.yaw + (command.wz * dt_s)),
    )


def footprint_in_collision(
    pose: Pose2D,
    grid: GridMap2D,
    safety_params: SafetyOracleParams,
) -> bool:
    for local_x, local_y in sample_footprint_points(safety_params.footprint, grid.resolution):
        world_x = pose.x + (math.cos(pose.yaw) * local_x) - (math.sin(pose.yaw) * local_y)
        world_y = pose.y + (math.sin(pose.yaw) * local_x) + (math.cos(pose.yaw) * local_y)
        if grid.is_occupied(world_x, world_y, safety_params.occupied_threshold):
            return True
    return False


def sample_footprint_points(
    footprint: FootprintParams,
    map_resolution_m: float,
) -> list[tuple[float, float]]:
    forward = footprint.forward_extent_m + footprint.padding_m
    rear = footprint.rear_extent_m + footprint.padding_m
    half_width = footprint.half_width_m + footprint.padding_m
    step = max(0.05, map_resolution_m * 0.75)

    x_values = _sample_axis(-rear, forward, step)
    y_values = _sample_axis(-half_width, half_width, step)

    points = {(0.0, 0.0)}
    for x_value in x_values:
        points.add((x_value, -half_width))
        points.add((x_value, half_width))
        points.add((x_value, 0.0))
    for y_value in y_values:
        points.add((-rear, y_value))
        points.add((forward, y_value))
        points.add((0.0, y_value))
    return list(points)


def _sample_axis(start: float, end: float, step: float) -> list[float]:
    samples = [start]
    if step <= 0.0 or math.isclose(start, end):
        return [start, end]
    current = start
    while current + step < end:
        current += step
        samples.append(current)
    if not math.isclose(samples[-1], end):
        samples.append(end)
    return samples


def _translation_scales(
    abs_bearing_rad: float,
    params: FollowControlParams,
) -> tuple[float, float]:
    if abs_bearing_rad <= params.yaw_priority_start_rad:
        return 1.0, 1.0
    if abs_bearing_rad >= params.yaw_freeze_rad:
        return 0.0, 0.40

    span = max(1.0e-3, params.yaw_freeze_rad - params.yaw_priority_start_rad)
    progress = (abs_bearing_rad - params.yaw_priority_start_rad) / span
    vx_scale = 1.0 - progress
    vy_scale = 1.0 - (0.60 * progress)
    return clamp(vx_scale, 0.0, 1.0), clamp(vy_scale, 0.40, 1.0)


def _command_score(candidate: Twist2D, nominal: Twist2D) -> float:
    diff_vx = candidate.vx - nominal.vx
    diff_vy = candidate.vy - nominal.vy
    diff_wz = candidate.wz - nominal.wz
    return (diff_vx * diff_vx) + (diff_vy * diff_vy) + (0.6 * diff_wz * diff_wz)


def _step_toward(current: float, desired: float, max_step: float) -> float:
    delta = desired - current
    if abs(delta) <= max_step:
        return desired
    return current + math.copysign(max_step, delta)
