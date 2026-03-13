from __future__ import annotations

from typing import Dict, List, Sequence, Set, Tuple

from models import Agent, AgentPlan, Solution, Task, Visit
from utils import euclidean


def solve_greedy(agents: Sequence[Agent], tasks: Sequence[Task]) -> Solution:
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
            feasible = []
            for task_id in remaining:
                task = tasks_by_id[task_id]
                travel = euclidean(loc, task.location)
                effort = travel + task.duration
                if effort <= capacity_left:
                    feasible.append((travel, task.priority, task))

            if not feasible:
                continue

            feasible.sort(key=lambda x: (x[0], -x[1]))
            travel, _, chosen = feasible[0]
            start = current_time + travel
            finish = start + chosen.duration
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
