import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from generator import generate_scenario


def test_generator_counts_and_ranges():
    scenario = generate_scenario(5, 20, seed=1, map_size=50)
    assert len(scenario["agents"]) == 5
    assert len(scenario["tasks"]) == 20
    for agent in scenario["agents"]:
        x, y = agent["location"]
        assert 0 <= x <= 50
        assert 0 <= y <= 50
