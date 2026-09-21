# NeuroSim.Problems/tests/conftest.py
import sys
from pathlib import Path

_PROBLEMS_SRC = Path(__file__).parent.parent / "src"
if str(_PROBLEMS_SRC) not in sys.path:
    sys.path.insert(0, str(_PROBLEMS_SRC))