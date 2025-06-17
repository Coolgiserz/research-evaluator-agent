# @Author: weirdgiser
# @Time: 2025/6/15
# @Function:
import os
from pathlib import Path

from src.research_evaluator_agent.cli.main import app

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
PYTHON_EXE = os.path.join(BASE_DIR, ".venv", "bin", "python")
print(PYTHON_EXE)
if __name__ == "__main__":
    os.system(f"{PYTHON_EXE} main.py")