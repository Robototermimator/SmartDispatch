from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Tuple

from generator import generate_scenario, save_scenario
from models import Agent, Task
from scorer import evaluate_solution, summarise
from solver_greedy import solve_greedy
from solver_heuristic import solve_heuristic
from solver_local_search import solve_local_search


def _parse_entities(scenario: dict) -> Tuple[List[Agent], List[Task]]:
    agents = [Agent(**item) for item in scenario["agents"]]
    tasks = [Task(**item) for item in scenario["tasks"]]
    return agents, tasks


def run_solver(solver_name: str, agents: List[Agent], tasks: List[Task]):
    if solver_name == "greedy":
        return solve_greedy(agents, tasks)
    if solver_name == "heuristic":
        return solve_heuristic(agents, tasks)
    if solver_name == "local_search":
        return solve_local_search(agents, tasks)
    raise ValueError(f"Unsupported solver: {solver_name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="SmartDispatch task scheduling optimiser")
    parser.add_argument("--agents", type=int, default=10)
    parser.add_argument("--tasks", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--solver", choices=["greedy", "heuristic", "local_search"], default="heuristic")
    parser.add_argument("--scenario-path", type=Path, default=None)
    parser.add_argument("--save-scenario", type=Path, default=None)
    args = parser.parse_args()

    if args.scenario_path:
        scenario = json.loads(args.scenario_path.read_text())
    else:
        scenario = generate_scenario(args.agents, args.tasks, seed=args.seed)

    if args.save_scenario:
        save_scenario(scenario, args.save_scenario)

    agents, tasks = _parse_entities(scenario)
    solution = run_solver(args.solver, agents, tasks)

    breakdown = evaluate_solution(solution, {t.id: t for t in tasks}, num_agents=len(agents))
    print(f"Scenario generated: {len(agents)} agents, {len(tasks)} tasks")
    print(f"Solver used: {args.solver}")
    print(f"Unassigned tasks: {len(solution.unassigned_task_ids)}")
    print(summarise(breakdown))


if __name__ == "__main__":
    main()
