from __future__ import annotations

import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from generator import generate_scenario
from main import _parse_entities, run_solver
from scorer import evaluate_solution


def benchmark(runs: int = 20, agents: int = 10, tasks: int = 50) -> None:
    solvers = ["greedy", "heuristic", "local_search"]
    results = {name: [] for name in solvers}

    for seed in range(runs):
        scenario = generate_scenario(agents, tasks, seed=seed)
        agent_objs, task_objs = _parse_entities(scenario)
        task_map = {t.id: t for t in task_objs}
        for solver in solvers:
            solution = run_solver(solver, agent_objs, task_objs)
            score = evaluate_solution(solution, task_map, len(agent_objs)).score
            results[solver].append(score)

    print("Solver       AvgScore   MaxScore   MinScore")
    for name in solvers:
        vals = results[name]
        print(f"{name:<12} {statistics.mean(vals):>8.2f} {max(vals):>10.2f} {min(vals):>10.2f}")


if __name__ == "__main__":
    benchmark()
