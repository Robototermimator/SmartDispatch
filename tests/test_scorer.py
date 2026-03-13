import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from models import AgentPlan, Solution, Task, Visit
from scorer import evaluate_solution


def test_scorer_basic_values():
    tasks = {
        1: Task(id=1, location=(0, 0), priority=3, duration=10, deadline=12),
        2: Task(id=2, location=(1, 1), priority=2, duration=5, deadline=None),
    }
    solution = Solution(
        plans=[
            AgentPlan(
                agent_id=0,
                visits=[
                    Visit(task_id=1, start_time=0, finish_time=13, travel_distance=2, late_by=1),
                    Visit(task_id=2, start_time=15, finish_time=20, travel_distance=1, late_by=0),
                ],
            )
        ],
        unassigned_task_ids=[],
    )
    breakdown = evaluate_solution(solution, tasks, num_agents=2)
    assert breakdown.completed_tasks == 2
    assert breakdown.priority_points == 5
    assert breakdown.idle_penalty == 1
    assert breakdown.score < 400
