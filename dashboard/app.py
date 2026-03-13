from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from generator import generate_scenario
from main import _parse_entities, run_solver
from scorer import evaluate_solution

st.title("SmartDispatch Quick Dashboard")
agents = st.slider("Agents", 1, 30, 10)
tasks = st.slider("Tasks", 5, 120, 50)
solver = st.selectbox("Solver", ["greedy", "heuristic", "local_search"])
seed = st.number_input("Seed", value=42)

if st.button("Run"):
    scenario = generate_scenario(agents, tasks, int(seed))
    agent_objs, task_objs = _parse_entities(scenario)
    solution = run_solver(solver, agent_objs, task_objs)
    breakdown = evaluate_solution(solution, {t.id: t for t in task_objs}, len(agent_objs))
    st.metric("Score", f"{breakdown.score:.2f}")
    st.write({
        "completed": breakdown.completed_tasks,
        "distance": round(breakdown.total_distance, 2),
        "late_penalty": round(breakdown.late_penalty, 2),
        "unassigned": len(solution.unassigned_task_ids),
    })
