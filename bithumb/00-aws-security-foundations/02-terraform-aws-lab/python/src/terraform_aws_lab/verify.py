from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


AWS_ENV = {
    "AWS_ACCESS_KEY_ID": "study2",
    "AWS_SECRET_ACCESS_KEY": "study2",
    "AWS_REGION": "ap-northeast-2",
}


def terraform_available() -> bool:
    return shutil.which("terraform") is not None


def run_lab(lab_dir: Path) -> dict[str, Any]:
    if not terraform_available():
        raise RuntimeError("terraform is not installed")

    env = os.environ.copy()
    env.update(AWS_ENV)

    subprocess.run(
        ["terraform", f"-chdir={lab_dir}", "init", "-backend=false"],
        check=True,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    subprocess.run(
        ["terraform", f"-chdir={lab_dir}", "validate"],
        check=True,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    plan_path = lab_dir / "tfplan"
    json_path = lab_dir / "tfplan.json"
    subprocess.run(
        ["terraform", f"-chdir={lab_dir}", "plan", "-refresh=false", f"-out={plan_path.name}"],
        check=True,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    rendered = subprocess.run(
        ["terraform", f"-chdir={lab_dir}", "show", "-json", plan_path.name],
        check=True,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    json_path.write_text(rendered.stdout)
    return json.loads(rendered.stdout)


def default_labs_root() -> Path:
    return Path(__file__).resolve().parents[3] / "terraform"


if __name__ == "__main__":
    root = default_labs_root()
    for lab_name in ("insecure", "secure"):
        plan = run_lab(root / lab_name)
        resource_count = len(plan["planned_values"]["root_module"]["resources"])
        print(f"{lab_name}: {resource_count} resources")
