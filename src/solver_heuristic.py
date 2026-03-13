from __future__ import annotations

from typing import Dict, Sequence, Set, Tuple

from models import Agent, AgentPlan, Solution, Task, Visit
from utils import euclidean


def _utility(priority: int, travel: float, projected_finish: float, deadline: float | None) -> float:
    lateness_risk = 0.0
    if deadline is not None:
        lateness_risk = max(0.0, projected_finish - deadline)
    deadline_pressure = 0.0 if deadline is None else max(0.0, deadline - projected_finish)
    return priority * 28.0 - travel * 7.5 - lateness_risk * 30.0 - deadline_pressure * 0.2


def solve_heuristic(agents: Sequence[Agent], tasks: Sequence[Task]) -> Solution:
    remaining: Set[int] = {t.id for t in tasks}
    tasks_by_id: Dict[int, Task] = {t.id: t for t in tasks}

    state: Dict[int, Tuple[Tuple[float, float], float, float]] = {
        a.id: (a.location, 0.0, a.max_workload) for a in agents
    }
    plans = {a.id: AgentPlan(agent_id=a.id) for a in agents}

    while remaining:
        progress = False
        for agent in agents:
            loc, current_time, capacity_left = state[agent.id]

            best_choice = None
            best_utility = float("-inf")
            for task_id in remaining:
                task = tasks_by_id[task_id]
                travel = euclidean(loc, task.location)
                projected_finish = current_time + travel + task.duration
                required = travel + task.duration
                if required > capacity_left:
                    continue
                value = _utility(task.priority, travel, projected_finish, task.deadline)
                if value > best_utility:
                    best_utility = value
                    best_choice = (task, travel, projected_finish)

            if best_choice is None:
                continue

            chosen, travel, finish = best_choice
            start = current_time + travel
            late = max(0.0, finish - chosen.deadline) if chosen.deadline is not None else 0.0
            plans[agent.id].visits.append(
                Visit(
                    task_id=chosen.id,
                    start_time=start,
                    finish_time=finish,
                    travel_distance=travel,
                    late_by=late,
                )
            )
            state[agent.id] = (chosen.location, finish, capacity_left - (travel + chosen.duration))
            remaining.remove(chosen.id)
            progress = True

        if not progress:
            break

    return Solution(plans=list(plans.values()), unassigned_task_ids=sorted(remaining))
