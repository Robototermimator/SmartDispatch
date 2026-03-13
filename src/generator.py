from __future__ import annotations

import json
import random
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Optional

from models import Agent, Task


def generate_scenario(
    num_agents: int,
    num_tasks: int,
    seed: Optional[int] = None,
    map_size: int = 100,
) -> Dict[str, List[dict]]:
    rng = random.Random(seed)

    agents = [
        Agent(
            id=i,
            location=(rng.uniform(0, map_size), rng.uniform(0, map_size)),
            max_workload=rng.uniform(180, 360),
        )
        for i in range(num_agents)
    ]

    tasks: List[Task] = []
    for i in range(num_tasks):
        has_deadline = rng.random() < 0.7
        duration = rng.uniform(10, 45)
        deadline = rng.uniform(40, 360) if has_deadline else None
        tasks.append(
            Task(
                id=i,
                location=(rng.uniform(0, map_size), rng.uniform(0, map_size)),
                priority=rng.randint(1, 5),
                duration=duration,
                deadline=deadline,
            )
        )

    return {
        "agents": [asdict(a) for a in agents],
        "tasks": [asdict(t) for t in tasks],
    }


def save_scenario(scenario: Dict[str, List[dict]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(scenario, indent=2))
