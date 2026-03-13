# SmartDispatch: A Resource Allocation and Task Scheduling Optimiser

SmartDispatch is a hackathon-friendly optimisation project that assigns limited agents (drivers/workers) to many tasks while maximising a scoring function.

## Problem statement
Each **task** has:
- location `(x, y)`
- priority `1..5`
- estimated duration
- optional deadline

Each **agent** has:
- current location
- workload limit (time budget)

The system should output:
- task-to-agent assignment
- execution order per agent
- final score and diagnostics

## Scoring model
```text
Score =
(CompletedTasks × 100)
+ (PriorityPointsCompleted × 20)
- (TotalDistance × 2)
- (LatePenalty × 15)
- (IdlePenalty × 5)
```

## Algorithms implemented
1. **Greedy** (`solver_greedy.py`): nearest feasible task first, then priority tie-break.
2. **Heuristic** (`solver_heuristic.py`): weighted utility of priority, travel cost, and lateness risk.
3. **Local Search** (`solver_local_search.py`): starts from heuristic and reorders task sequences when score improves.

## Project structure
```text
smartdispatch/
├── data/
│   ├── sample_cases/
│   └── generated_cases/
├── src/
│   ├── generator.py
│   ├── models.py
│   ├── scorer.py
│   ├── solver_greedy.py
│   ├── solver_heuristic.py
│   ├── solver_local_search.py
│   ├── utils.py
│   └── main.py
├── experiments/
│   ├── benchmark.py
│   └── tuning.py
├── dashboard/
│   └── app.py
├── tests/
│   ├── test_generator.py
│   ├── test_scorer.py
│   └── test_solver.py
├── requirements.txt
└── README.md
```

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/main.py --agents 10 --tasks 50 --solver heuristic --seed 42
```

## Example CLI output
```text
Scenario generated: 10 agents, 50 tasks
Solver used: heuristic
Unassigned tasks: 4
Completed tasks: 46
Priority points: 162
Total distance: 212.40
Late sum: 3.00
Idle agents: 0
Final score: 4280.00
```

## Benchmark strategy
- Generate many seeded scenarios (`seed=0..N`) with the same size.
- Run each solver on every scenario.
- Track mean/min/max score to compare solver stability.

Run:
```bash
python experiments/benchmark.py
```

## Optional dashboard
```bash
streamlit run dashboard/app.py
```

## 14-day development plan
- Days 1–2: scenario generator
- Days 3–4: scoring engine
- Days 5–6: baseline greedy solver
- Days 7–8: heuristic solver
- Days 9–10: local search improvements
- Day 11: benchmark runs
- Day 12: CLI/output cleanup
- Day 13: optional dashboard
- Day 14: final tuning and polishing

## Future improvements
- Simulated annealing / genetic algorithm
- Better travel-time model (road graph vs Euclidean)
- Dynamic online task arrival
- Hyperparameter tuning automation
