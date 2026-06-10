#!/usr/bin/env python3
"""Pure (ROS-free) geometry helpers for sampling-based baseline pose selection.

These implement the "geometry-aware selection of the next measurement pose" math
from the Steam-Leak-Localization document (eqs. 9-13): a candidate move from the
dog's current pose toward a sampled free-space point only helps the two-bearing
triangulation through the component of its displacement that is *perpendicular* to
the current leak bearing. The selector therefore scores candidates by that
perpendicular baseline and prefers the largest one reaching the target (>= ~0.5 m),
falling back to the best weak-geometry candidate when none do.

Kept ROS-free (mirrors mission_supervisor_core / person_follow_controller_core) so
the numeric edge cases can be unit-tested without rclpy/Nav2.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

EPS = 1.0e-6


def perpendicular_fraction(dx: float, dy: float, bearing_rad: float) -> float:
    """Fraction (0..1) of a displacement that is perpendicular to ``bearing_rad``.

    This is ``|sin(theta)|`` where ``theta`` is the angle between the displacement
    vector ``(dx, dy)`` and the leak bearing, computed from the 2-D cross product of
    the unit displacement with the unit bearing direction. (The *dot* product would
    instead give the parallel ``|cos|`` component.) A perfectly perpendicular move
    returns 1.0; a move straight along the bearing returns 0.0.
    """
    norm = math.hypot(dx, dy)
    if norm < EPS:
        return 0.0
    cross = (dx * math.sin(bearing_rad)) - (dy * math.cos(bearing_rad))
    return min(1.0, abs(cross) / norm)


def perpendicular_baseline_component(dx: float, dy: float, bearing_rad: float) -> float:
    """Length of the perpendicular component of a displacement (eq. 9: ``L*|sin|``)."""
    return abs((dx * math.sin(bearing_rad)) - (dy * math.cos(bearing_rad)))


@dataclass(frozen=True)
class ScoredCandidate:
    """Minimal candidate for ranking; mirrors the node's CandidateGoal fields."""

    achieved_perpendicular_baseline_m: float
    path_length_m: float
    # Signed component of the move along the leak bearing: > 0 = toward the leak
    # (forward-ish), < 0 = away from the leak (the dog would reverse/back up).
    parallel_component_m: float = 0.0


def rank_baseline_candidates(candidates, target_m: float, weak_min_m: float):
    """Order baseline candidates for the next measurement pose (doc eqs. 12-13).

    Each candidate must expose ``achieved_perpendicular_baseline_m`` and
    ``path_length_m`` (and optionally ``parallel_component_m``). The key behaviour:

    * Candidates that reach the perpendicular-baseline ``target_m`` are strongly
      preferred. Among them we DO NOT maximise the baseline (that sends the dog on
      a needlessly long, often rearward trek); instead, per eq. 13, we take the
      *shortest move that still achieves the target*, and we prefer moves with a
      non-negative parallel component so the dog steps toward/around the leak
      rather than reversing.
    * Only if nothing reaches ``target_m`` do we fall back to the weak-geometry
      pool (>= ``weak_min_m``) and there take the largest baseline available.
    """
    meeting = [
        c for c in candidates if c.achieved_perpendicular_baseline_m >= target_m
    ]
    if meeting:
        return sorted(
            meeting,
            key=lambda c: (
                getattr(c, "parallel_component_m", 0.0) < 0.0,  # toward-leak first
                c.path_length_m,                                 # shortest move (eq. 13)
                -c.achieved_perpendicular_baseline_m,
            ),
        )
    weak = [
        c for c in candidates if c.achieved_perpendicular_baseline_m >= weak_min_m
    ]
    return sorted(
        weak,
        key=lambda c: (-c.achieved_perpendicular_baseline_m, c.path_length_m),
    )
