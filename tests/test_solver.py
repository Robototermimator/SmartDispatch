import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from generator import generate_scenario
from main import _parse_entities
from solver_greedy import solve_greedy
from solver_heuristic import solve_heuristic


def test_solvers_produce_valid_assignments():
    scenario = generate_scenario(8, 30, seed=7)
    agents, tasks = _parse_entities(scenario)
    task_ids = {t.id for t in tasks}

    greedy = solve_greedy(agents, tasks)
    heuristic = solve_heuristic(agents, tasks)

    for solution in (greedy, heuristic):
        assigned = [v.task_id for p in solution.plans for v in p.visits]
        assert set(assigned).issubset(task_ids)
        assert len(assigned) == len(set(assigned))
        assert set(solution.unassigned_task_ids).isdisjoint(set(assigned))
