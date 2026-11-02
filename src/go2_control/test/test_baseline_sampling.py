from __future__ import annotations

import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from go2_control.localize_baseline_core import (  # noqa: E402
    ScoredCandidate,
    perpendicular_baseline_component,
    perpendicular_fraction,
    rank_baseline_candidates,
)


def test_perpendicular_fraction_parallel_is_zero() -> None:
    # Moving straight along the bearing has no perpendicular component.
    assert perpendicular_fraction(1.0, 0.0, 0.0) == 0.0
    assert perpendicular_fraction(-2.0, 0.0, 0.0) == 0.0


def test_perpendicular_fraction_orthogonal_is_one() -> None:
    # Moving 90 deg off the bearing is fully perpendicular.
    assert math.isclose(perpendicular_fraction(0.0, 1.0, 0.0), 1.0, abs_tol=1e-9)


def test_perpendicular_fraction_thirty_degrees() -> None:
    # A heading 30 deg off the bearing keeps |sin 30| = 0.5 of its length.
    dx = math.cos(math.radians(30.0))
    dy = math.sin(math.radians(30.0))
    assert math.isclose(perpendicular_fraction(dx, dy, 0.0), 0.5, abs_tol=1e-9)


def test_baseline_component_scales_with_distance() -> None:
    # 1.4 m travel at 30 deg off bearing -> 0.70 m perpendicular (>= 0.5 target).
    dx = 1.4 * math.cos(math.radians(30.0))
    dy = 1.4 * math.sin(math.radians(30.0))
    assert math.isclose(
        perpendicular_baseline_component(dx, dy, 0.0), 0.70, abs_tol=1e-9
    )
    # 0.6 m travel at 30 deg -> 0.30 m perpendicular (< 0.5 target).
    sx = 0.6 * math.cos(math.radians(30.0))
    sy = 0.6 * math.sin(math.radians(30.0))
    assert math.isclose(
        perpendicular_baseline_component(sx, sy, 0.0), 0.30, abs_tol=1e-9
    )


def test_rank_prefers_shortest_target_meeting_move() -> None:
    # Per eq. 13: among candidates that reach the target, take the SHORTEST move
    # (do NOT maximise the baseline, which sends the dog on a needless long trek).
    candidates = [
        ScoredCandidate(achieved_perpendicular_baseline_m=0.30, path_length_m=0.4),
        ScoredCandidate(achieved_perpendicular_baseline_m=1.90, path_length_m=2.1),
        ScoredCandidate(achieved_perpendicular_baseline_m=0.55, path_length_m=0.9),
    ]
    ranked = rank_baseline_candidates(candidates, target_m=0.5, weak_min_m=0.25)
    # 0.30 dropped (< target); the short 0.55 m move beats the long 1.90 m one.
    assert [round(c.achieved_perpendicular_baseline_m, 2) for c in ranked] == [0.55, 1.90]


def test_rank_prefers_forward_over_reverse_when_target_met() -> None:
    forward = ScoredCandidate(0.6, path_length_m=1.2, parallel_component_m=0.4)
    reverse_short = ScoredCandidate(0.6, path_length_m=0.7, parallel_component_m=-0.4)
    ranked = rank_baseline_candidates([reverse_short, forward], target_m=0.5, weak_min_m=0.25)
    # Even though the reverse move is shorter, a toward-leak move is preferred.
    assert ranked[0] is forward


def test_rank_target_tie_breaks_on_shorter_path() -> None:
    candidates = [
        ScoredCandidate(0.60, path_length_m=2.0, parallel_component_m=0.5),
        ScoredCandidate(0.60, path_length_m=0.8, parallel_component_m=0.5),
    ]
    ranked = rank_baseline_candidates(candidates, target_m=0.5, weak_min_m=0.25)
    assert ranked[0].path_length_m == 0.8


def test_rank_weak_geometry_fallback_when_none_meet_target() -> None:
    candidates = [
        ScoredCandidate(achieved_perpendicular_baseline_m=0.10, path_length_m=0.4),
        ScoredCandidate(achieved_perpendicular_baseline_m=0.35, path_length_m=0.9),
    ]
    ranked = rank_baseline_candidates(candidates, target_m=0.5, weak_min_m=0.25)
    # No candidate reaches 0.5 m, so the best >= weak_min (0.25) is returned.
    assert len(ranked) == 1
    assert math.isclose(ranked[0].achieved_perpendicular_baseline_m, 0.35)


def test_rank_returns_empty_when_all_below_weak_min() -> None:
    candidates = [
        ScoredCandidate(achieved_perpendicular_baseline_m=0.10, path_length_m=0.4),
        ScoredCandidate(achieved_perpendicular_baseline_m=0.20, path_length_m=0.9),
    ]
    ranked = rank_baseline_candidates(candidates, target_m=0.5, weak_min_m=0.25)
    assert ranked == []
