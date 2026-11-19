"""Record the real candidate failure and the enclosing Actions step outcome."""
import json
import os
from pathlib import Path
import sys

validator = json.loads(Path("shell-probe.json").read_bytes())
observation = {
    "candidate": validator["commit"],
    "validator_result": validator["result"],
    "validator_errors": validator["errors"],
    "step_outcome": os.environ["SHELL_STEP_OUTCOME"],
    "platform": sys.platform,
}
Path("shell-observations.json").write_text(json.dumps(observation, indent=2) + "\n", encoding="utf-8")
print(json.dumps(observation))
assert observation["validator_result"] == "failed", observation
assert observation["step_outcome"] == ("success" if sys.platform == "win32" else "failure"), observation
