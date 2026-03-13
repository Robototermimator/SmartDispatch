from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

Location = Tuple[float, float]


@dataclass(frozen=True)
class Task:
    id: int
    location: Location
    priority: int
    duration: float
    deadline: Optional[float] = None


@dataclass
class Agent:
    id: int
    location: Location
    max_workload: float


@dataclass
class Visit:
    task_id: int
    start_time: float
    finish_time: float
    travel_distance: float
    late_by: float


@dataclass
class AgentPlan:
    agent_id: int
    visits: List[Visit] = field(default_factory=list)

    @property
    def total_distance(self) -> float:
        return sum(v.travel_distance for v in self.visits)


@dataclass
class Solution:
    plans: List[AgentPlan]
    unassigned_task_ids: List[int]
