# AUTH:DEVNEUROSIM:7A3F9E2B | conftest.py
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

ENGINE_SRC = ROOT / "NeuroSim.Engine" / "src"
PROBLEMS_SRC = ROOT / "NeuroSim.Problems" / "src"

sys.path.insert(0, str(ENGINE_SRC))
sys.path.insert(0, str(PROBLEMS_SRC))
