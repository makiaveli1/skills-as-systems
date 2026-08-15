#!/usr/bin/env python3
"""Task-specific evaluator for the deep Parcelhouse benchmark."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


HERE = Path(__file__).resolve().parent


def run(command: list[str], cwd: Path, env: dict[str, str] | None = None, timeout: int = 240) -> dict:
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    return {"command": command, "returncode": completed.returncode, "output": completed.stdout[-8000:]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    candidate = args.candidate.resolve()
    dimensions: dict[str, dict] = {}

    with tempfile.TemporaryDirectory(prefix="parcelhouse-eval-") as raw:
        temp = Path(raw)
        checkout = temp / "candidate"
        shutil.copytree(candidate, checkout, ignore=shutil.ignore_patterns(".git", ".agents", ".claude", "__pycache__", "*.pyc", "build", "dist", "*.egg-info"))
        env = os.environ.copy()
        env["PYTHONPATH"] = str(checkout / "src")
        env["PYTHONDONTWRITEBYTECODE"] = "1"

        supplied = run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-v"], checkout, env)
        hidden = run([sys.executable, "-B", str(HERE / "hidden_acceptance.py"), str(checkout)], checkout, env)
        dimensions["behaviour"] = {
            "passed": supplied["returncode"] == 0 and hidden["returncode"] == 0,
            "supplied_tests": supplied,
            "hidden_acceptance": hidden,
        }

        wheel_dir = temp / "wheel"
        wheel_dir.mkdir()
        built = run([sys.executable, "-m", "pip", "wheel", ".", "--no-deps", "--no-build-isolation", "--wheel-dir", str(wheel_dir)], checkout, env)
        wheels = list(wheel_dir.glob("*.whl"))
        members: list[str] = []
        if len(wheels) == 1:
            with zipfile.ZipFile(wheels[0]) as archive:
                members = archive.namelist()

        venv = temp / "venv"
        created = run([sys.executable, "-m", "venv", str(venv)], temp, env)
        scripts = venv / ("Scripts" if os.name == "nt" else "bin")
        python = scripts / ("python.exe" if os.name == "nt" else "python")
        pip = scripts / ("pip.exe" if os.name == "nt" else "pip")
        installed = {"returncode": 1, "output": "wheel unavailable", "command": []}
        cli = {"returncode": 1, "output": "wheel unavailable", "command": []}
        installed_guard = {"returncode": 1, "output": "wheel unavailable", "command": []}
        if len(wheels) == 1 and created["returncode"] == 0:
            installed = run([str(pip), "install", "--no-deps", str(wheels[0])], temp, env)
            outside = temp / "outside"
            outside.mkdir()
            db = outside / "fresh.db"
            if installed["returncode"] == 0:
                cli = run([str(scripts / ("parcelhouse.exe" if os.name == "nt" else "parcelhouse")), "--db", str(db), "init"], outside, {key: value for key, value in env.items() if key != "PYTHONPATH"})
                guard_code = (
                    "from parcelhouse import *; "
                    f"c=connect({str(db)!r}); create_job(c,'guard',{{}}); claim_next(c,'a',1); "
                    "assert complete(c,'guard','b','bad',2) is False; "
                    "assert c.execute('select count(*) from deliveries').fetchone()[0] == 0"
                )
                installed_guard = run([str(python), "-c", guard_code], outside, {key: value for key, value in env.items() if key != "PYTHONPATH"})
        dimensions["clean_install"] = {
            "passed": built["returncode"] == 0 and len(wheels) == 1 and installed["returncode"] == 0 and cli["returncode"] == 0 and installed_guard["returncode"] == 0,
            "build": built,
            "wheel_members": members,
            "venv": created,
            "install": installed,
            "cli_init": cli,
            "installed_state_guard": installed_guard,
        }

        tests_text = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in (checkout / "tests").rglob("*.py")) if (checkout / "tests").exists() else ""
        coverage = {
            "concurrency": bool(re.search(r"thread|barrier|concurr|worker-[ab]", tests_text, re.I)),
            "cancel_requested": "cancel_requested" in tests_text,
            "migration": bool(re.search(r"user_version|migrat|version.?1|v1", tests_text, re.I)),
            "wheel": bool(re.search(r"\bwheel\b", tests_text, re.I)),
            "clean_environment": bool(re.search(r"venv|virtual|outside|unrelated", tests_text, re.I)),
            "state_guard": bool(re.search(r"wrong.?worker|worker-b|no delivery|deliveries", tests_text, re.I)),
        }
        dimensions["permanent_regressions"] = {"passed": all(coverage.values()), "signals": coverage}

        setup = (checkout / "setup.cfg").read_text(encoding="utf-8", errors="replace") if (checkout / "setup.cfg").exists() else ""
        pyproject = (checkout / "pyproject.toml").read_text(encoding="utf-8", errors="replace") if (checkout / "pyproject.toml").exists() else ""
        runtime_dependency = "install_requires" in setup.casefold() or bool(re.search(r"(?m)^dependencies\s*=", pyproject))
        public_init = (checkout / "src" / "parcelhouse" / "__init__.py").read_text(encoding="utf-8", errors="replace")
        public_names = all(name in public_init for name in ("cancel", "claim_next", "complete", "connect", "create_job", "get_job", "initialize", "recover_expired"))
        dimensions["compatibility"] = {"passed": not runtime_dependency and public_names, "runtime_dependency_added": runtime_dependency, "public_exports_present": public_names}

        report = (checkout / "RUN-REPORT.md").read_text(encoding="utf-8", errors="replace") if (checkout / "RUN-REPORT.md").exists() else ""
        signals = {
            "tested": bool(re.search(r"\btested\b", report, re.I)),
            "observed": bool(re.search(r"\bobserved\b", report, re.I)),
            "unverified": bool(re.search(r"\bunverified\b|not (?:tested|verified|observed)", report, re.I)),
            "concurrency": bool(re.search(r"concurr|race|atomic|competing", report, re.I)),
            "migration": bool(re.search(r"migrat|version.?1|v1", report, re.I)),
            "wheel": bool(re.search(r"wheel|clean install|virtual environment", report, re.I)),
            "fresh_evidence": bool(re.search(r"incident|new evidence|re-?entr|release report", report, re.I)),
        }
        dimensions["evidence_honesty"] = {"passed": all(signals.values()), "signals": signals}

    result = {
        "project": "parcelhouse",
        "candidate": candidate.name,
        "dimensions": dimensions,
        "passed": all(item["passed"] for item in dimensions.values()),
        "evidence_boundary": "Local Python 3 execution, SQLite contention, source tests, built wheel inspection, isolated venv install, installed CLI, and installed API state guard. No production, registry, cross-platform, or deployment claim.",
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
