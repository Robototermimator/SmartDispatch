README.md# SmartDispatch-A-Resource-Allocation-and-Task-Scheduling-Optimiser
# SmartDispatch: A Resource Allocation and Task Scheduling Optimiser

SmartDispatch is a Python project for assigning limited agents (drivers/workers) to many tasks while maximising a score.

## 1) What this project does
Given:
- a set of tasks with `(x, y)` location, priority, duration, and optional deadline
- a set of agents with start location and workload limit

SmartDispatch computes:
- which agent takes which tasks
- in what order each agent executes them
- a final score and breakdown metrics

---

## 2) Scoring formula
The current scorer uses:

```text
Score =
(CompletedTasks × 100)
+ (PriorityPointsCompleted × 20)
- (TotalDistance × 2)
- (LatePenalty × 15)
- (IdlePenalty × 5)
```

Where:
- `CompletedTasks`: number of assigned and executed tasks
- `PriorityPointsCompleted`: sum of task priorities completed
- `TotalDistance`: total travel distance across all agents
- `LatePenalty`: summed lateness (time units after deadlines)
- `IdlePenalty`: number of agents with no assigned tasks

---

## 3) Solvers included
- **Greedy (`solver_greedy.py`)**
  - Chooses nearest feasible task first.
  - Fast baseline.

- **Heuristic (`solver_heuristic.py`)**
  - Uses weighted utility of priority, travel, and lateness risk.
  - Designed for easy weight tuning.

- **Local Search (`solver_local_search.py`)**
  - Starts from heuristic result.
  - Reorders per-agent task sequences and keeps improvements.

---

## 4) Project structure
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

---

## 5) Installation

### Option A: install all dependencies (recommended)
```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Option B: install only Streamlit
```bash
python -m pip install --upgrade pip
pip install streamlit
```

Verify Streamlit:
```bash
streamlit --version
```

If your shell cannot find `streamlit`, run:
```bash
python -m streamlit --version
```

---

## 6) Run from CLI
Generate a scenario and solve it:

```bash
python src/main.py --agents 10 --tasks 50 --solver heuristic --seed 42
```

Run with a different solver:

```bash
python src/main.py --agents 10 --tasks 50 --solver greedy --seed 42
python src/main.py --agents 10 --tasks 50 --solver local_search --seed 42
```

Save a generated scenario:

```bash
python src/main.py --agents 10 --tasks 50 --solver heuristic --save-scenario data/generated_cases/case_01.json
```

Load a scenario:

```bash
python src/main.py --scenario-path data/generated_cases/case_01.json --solver heuristic
```

---

## 7) Benchmarking
Run the benchmark script to compare solver score distributions over multiple seeds:

```bash
python experiments/benchmark.py
```

Current benchmark output may show that heuristic/local search need additional tuning to consistently beat greedy; this is expected at MVP stage.

---

## 8) Dashboard (optional)
If Streamlit is installed:

```bash
streamlit run dashboard/app.py
```

If command resolution fails:

```bash
python -m streamlit run dashboard/app.py
```

---

## 9) Testing
Run tests:

```bash
pytest -q
```

---

## 10) Improvement roadmap
- Tune heuristic utility weights in `experiments/tuning.py`
- Improve local search neighbourhood moves (swap between agents, insert/move task)
- Add simulated annealing or GA for broader search
- Replace Euclidean distance with map/road-time travel model
- Add richer visualisation of routes and lateness
