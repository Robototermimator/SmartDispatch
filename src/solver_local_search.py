from __future__ import annotations

from copy import deepcopy
from typing import Dict, Sequence

from models import Agent, Solution, Task, Visit
from scorer import evaluate_solution
from solver_heuristic import solve_heuristic
from utils import euclidean


def _task_order_score(task: Task) -> float:
    deadline_bias = 0.0 if task.deadline is None else 0.1 * task.deadline
    return task.priority * 10 - task.duration - deadline_bias


def _recompute_visits(solution: Solution, tasks_by_id: Dict[int, Task], agents_by_id: Dict[int, Agent]) -> None:
    for plan in solution.plans:
        agent = agents_by_id[plan.agent_id]
        current_location = agent.location
        current_time = 0.0
        updated: list[Visit] = []
        for visit in plan.visits:
            task = tasks_by_id[visit.task_id]
            travel = euclidean(current_location, task.location)
            start = current_time + travel
            finish = start + task.duration
            late = max(0.0, finish - task.deadline) if task.deadline is not None else 0.0
            updated.append(
                Visit(
                    task_id=task.id,
                    start_time=start,
                    finish_time=finish,
                    travel_distance=travel,
                    late_by=late,
                )
            )
            current_location = task.location
            current_time = finish
        plan.visits = updated


def solve_local_search(agents: Sequence[Agent], tasks: Sequence[Task], iterations: int = 50) -> Solution:
    base = solve_heuristic(agents, tasks)
    tasks_by_id: Dict[int, Task] = {t.id: t for t in tasks}
    agents_by_id: Dict[int, Agent] = {a.id: a for a in agents}

    best = deepcopy(base)
    best_score = evaluate_solution(best, tasks_by_id, len(agents)).score

    for _ in range(iterations):
        candidate = deepcopy(best)
        changed = False

        for plan in candidate.plans:
            if len(plan.visits) < 2:
                continue
            reordered = sorted(plan.visits, key=lambda v: _task_order_score(tasks_by_id[v.task_id]), reverse=True)
            if [v.task_id for v in reordered] != [v.task_id for v in plan.visits]:
                plan.visits = reordered
                changed = True

        if not changed:
            continue

        _recompute_visits(candidate, tasks_by_id, agents_by_id)
        candidate_score = evaluate_solution(candidate, tasks_by_id, len(agents)).score
        if candidate_score > best_score:
            best = candidate
            best_score = candidate_score

    return best
