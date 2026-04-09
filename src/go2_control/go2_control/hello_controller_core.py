from __future__ import annotations

import math
from dataclasses import dataclass


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


@dataclass(frozen=True)
class HelloCandidate:
    base_x_m: float
    base_y_m: float
    base_z_m: float
    memory_x_m: float
    memory_y_m: float
    confidence: float = 0.0
    bbox_area_px: float = 0.0


@dataclass(frozen=True)
class HelloControlParams:
    search_yaw_rate_radps: float = 0.55
    yaw_gain: float = 1.8
    max_yaw_rate_radps: float = 0.90
    target_yaw_deadband_rad: float = 0.18
    greeted_target_memory_s: float = 30.0
    greeted_target_xy_bin_m: float = 0.75
    greeted_target_match_radius_m: float = 1.25


@dataclass(frozen=True)
class GreetedTargetRecord:
    memory_x_m: float
    memory_y_m: float
    greeted_at_s: float


def candidate_range_m(candidate: HelloCandidate) -> float:
    return math.hypot(candidate.base_x_m, candidate.base_y_m)


def candidate_bearing_rad(candidate: HelloCandidate) -> float:
    return math.atan2(candidate.base_y_m, candidate.base_x_m)


def greeting_target_key(
    candidate: HelloCandidate,
    *,
    xy_bin_m: float,
) -> tuple[int, int]:
    bin_size = max(0.05, float(xy_bin_m))
    return (
        int(round(candidate.memory_x_m / bin_size)),
        int(round(candidate.memory_y_m / bin_size)),
    )


def prune_greeted_history(
    history: list[GreetedTargetRecord],
    *,
    now_s: float,
    memory_s: float,
) -> list[GreetedTargetRecord]:
    max_age_s = max(0.0, float(memory_s))
    return [
        record
        for record in history
        if (now_s - record.greeted_at_s) <= max_age_s
    ]


def was_greeted_recently(
    candidate: HelloCandidate,
    history: list[GreetedTargetRecord],
    *,
    now_s: float,
    memory_s: float,
    match_radius_m: float,
) -> bool:
    max_age_s = max(0.0, float(memory_s))
    max_radius_m = max(0.05, float(match_radius_m))
    for record in history:
        if (now_s - record.greeted_at_s) > max_age_s:
            continue
        if math.hypot(candidate.memory_x_m - record.memory_x_m, candidate.memory_y_m - record.memory_y_m) <= max_radius_m:
            return True
    return False


def select_hello_candidate(
    candidates: list[HelloCandidate],
    greeted_history: list[GreetedTargetRecord],
    *,
    now_s: float,
    params: HelloControlParams,
) -> HelloCandidate | None:
    best_candidate: HelloCandidate | None = None
    best_score = -math.inf

    for candidate in candidates:
        if was_greeted_recently(
            candidate,
            greeted_history,
            now_s=now_s,
            memory_s=params.greeted_target_memory_s,
            match_radius_m=params.greeted_target_match_radius_m,
        ):
            continue

        score = _hello_candidate_score(candidate)
        if score > best_score:
            best_score = score
            best_candidate = candidate

    return best_candidate


def record_greeted_target(
    history: list[GreetedTargetRecord],
    candidate: HelloCandidate,
    *,
    now_s: float,
    match_radius_m: float,
) -> list[GreetedTargetRecord]:
    updated_history: list[GreetedTargetRecord] = []
    max_radius_m = max(0.05, float(match_radius_m))
    replaced = False
    for record in history:
        if math.hypot(candidate.memory_x_m - record.memory_x_m, candidate.memory_y_m - record.memory_y_m) <= max_radius_m:
            if not replaced:
                updated_history.append(
                    GreetedTargetRecord(
                        memory_x_m=candidate.memory_x_m,
                        memory_y_m=candidate.memory_y_m,
                        greeted_at_s=now_s,
                    )
                )
                replaced = True
            continue
        updated_history.append(record)

    if not replaced:
        updated_history.append(
            GreetedTargetRecord(
                memory_x_m=candidate.memory_x_m,
                memory_y_m=candidate.memory_y_m,
                greeted_at_s=now_s,
            )
        )
    return updated_history


def hello_session_limit_reached(
    greetings_completed: int,
    max_greetings_per_session: int,
) -> bool:
    limit = max(0, int(max_greetings_per_session))
    if limit <= 0:
        return False
    return int(greetings_completed) >= limit


def compute_centering_yaw_rate(
    candidate: HelloCandidate,
    params: HelloControlParams,
) -> float:
    bearing_rad = candidate_bearing_rad(candidate)
    if abs(bearing_rad) <= params.target_yaw_deadband_rad:
        return 0.0
    return clamp(
        params.yaw_gain * bearing_rad,
        -params.max_yaw_rate_radps,
        params.max_yaw_rate_radps,
    )


def update_wave_dispatch_window(
    current_target_key: tuple[int, int],
    pending_target_key: tuple[int, int] | None,
    pending_ready_at_s: float,
    *,
    now_s: float,
    stop_hold_s: float,
) -> tuple[bool, tuple[int, int], float]:
    settle_s = max(0.0, float(stop_hold_s))
    if settle_s <= 0.0:
        return True, current_target_key, now_s
    if pending_target_key != current_target_key:
        return False, current_target_key, now_s + settle_s
    return now_s >= pending_ready_at_s, current_target_key, pending_ready_at_s


def _hello_candidate_score(candidate: HelloCandidate) -> float:
    confidence_score = max(0.0, float(candidate.confidence)) / 100.0
    range_score = max(0.0, 1.0 - min(candidate_range_m(candidate), 6.0) / 6.0)
    center_score = max(0.0, 1.0 - min(abs(candidate_bearing_rad(candidate)), math.pi) / math.pi)
    area_score = min(max(float(candidate.bbox_area_px), 0.0) / 60000.0, 1.0)
    return confidence_score + (0.75 * center_score) + (0.50 * range_score) + (0.25 * area_score)
