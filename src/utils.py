from __future__ import annotations

import math
from typing import Tuple

Location = Tuple[float, float]


def euclidean(a: Location, b: Location) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])
