from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable

from models import Solution, Task


@dataclass
class ScoreBreakdown:
    completed_tasks: int
    priority_points: int
    total_distance: float
    late_penalty: float
    idle_penalty: float
    score: float


def evaluate_solution(
    solution: Solution,
    tasks_by_id: Dict[int, Task],
    num_agents: int,
) -> ScoreBreakdown:
    completed = 0
    priority_points = 0
    total_distance = 0.0
    late_sum = 0.0

    used_agents = 0
    for plan in solution.plans:
        if plan.visits:
            used_agents += 1
        for visit in plan.visits:
            completed += 1
            task = tasks_by_id[visit.task_id]
            priority_points += task.priority
            total_distance += visit.travel_distance
            late_sum += visit.late_by

    idle_penalty = float(max(num_agents - used_agents, 0))
    score = (
        completed * 100
        + priority_points * 20
        - total_distance * 2
        - late_sum * 15
        - idle_penalty * 5
    )

    return ScoreBreakdown(
        completed_tasks=completed,
        priority_points=priority_points,
        total_distance=total_distance,
        late_penalty=late_sum,
        idle_penalty=idle_penalty,
        score=score,
    )


def summarise(b: ScoreBreakdown) -> str:
    return (
        f"Completed tasks: {b.completed_tasks}\n"
        f"Priority points: {b.priority_points}\n"
        f"Total distance: {b.total_distance:.2f}\n"
        f"Late sum: {b.late_penalty:.2f}\n"
        f"Idle agents: {b.idle_penalty:.0f}\n"
        f"Final score: {b.score:.2f}"
    )
