#!/usr/bin/env python3
"""Deterministic evaluator for the Relaypack packaging-boundary benchmark."""

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


BENCHMARK = Path(__file__).resolve().parents[1]
SEED = BENCHMARK / "seed"
EXPECTED = "route alpha -> https://api.example.test/v1"


def sanitize(value):
    """Remove machine-specific home and temporary paths from public evidence."""
    text = str(value).replace(str(Path.home()), "<HOME>")
    return re.sub(
        r"/(?:private/)?var/folders/[^/\s]+/[^/\s]+/T/[^/\s'\"]+",
        "<TMP>",
        text,
    )


def run(command, *, cwd, env=None, timeout=120):
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as error:
        return {
            "command": [sanitize(item) for item in command],
            "returncode": 127,
            "output": sanitize(f"{type(error).__name__}: {error}"),
        }
    return {
        "command": [sanitize(item) for item in command],
        "returncode": completed.returncode,
        "output": sanitize(completed.stdout[-6000:]),
    }


def record(checks, name, points, earned, evidence):
    checks.append({
        "name": name,
        "points": points,
        "earned": points if earned else 0,
        "passed": bool(earned),
        "evidence": evidence,
    })


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    candidate = args.candidate.resolve()
    checks = []
    blocking = []

    with tempfile.TemporaryDirectory(prefix="relaypack-supplied-") as raw_supplied:
        supplied_checkout = Path(raw_supplied) / "candidate"
        shutil.copytree(
            candidate,
            supplied_checkout,
            ignore=shutil.ignore_patterns(
                ".git", ".agents", "__pycache__", "*.pyc", "dist", "build", "*.egg-info"
            ),
        )
        supplied = run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
            cwd=supplied_checkout,
        )
    supplied_ok = supplied["returncode"] == 0
    record(checks, "source_baseline", 10, supplied_ok, supplied)
    if not supplied_ok:
        blocking.append("the supplied source tests regress")

    with tempfile.TemporaryDirectory(prefix="relaypack-eval-") as raw_temp:
        temp = Path(raw_temp)
        build_checkout = temp / "build-checkout"
        shutil.copytree(candidate, build_checkout, ignore=shutil.ignore_patterns(".git", ".agents", "__pycache__", "*.pyc", "dist", "build", "*.egg-info"))
        wheels = temp / "wheels"
        wheels.mkdir()
        built = run(
            [sys.executable, "-m", "pip", "wheel", ".", "--no-build-isolation", "--no-deps", "--wheel-dir", str(wheels)],
            cwd=build_checkout,
        )
        wheel_files = list(wheels.glob("*.whl"))
        build_ok = built["returncode"] == 0 and len(wheel_files) == 1

        venv = temp / "venv"
        created = run([sys.executable, "-m", "venv", str(venv)], cwd=temp)
        vpython = venv / "bin" / "python"
        vpip = venv / "bin" / "pip"
        install = {"returncode": 1, "output": "wheel was not built", "command": []}
        if build_ok and created["returncode"] == 0:
            install = run([str(vpip), "install", "--no-deps", str(wheel_files[0])], cwd=temp)
        wheel_ok = build_ok and install["returncode"] == 0
        record(checks, "wheel_build", 10, wheel_ok, {"build": built, "venv": created, "install": install})
        if not wheel_ok:
            blocking.append("the wheel cannot be built or installed")

        members = []
        data_ok = False
        if build_ok:
            with zipfile.ZipFile(wheel_files[0]) as archive:
                members = archive.namelist()
            data_ok = any(name.startswith("relaypack/") and name.endswith(".json") for name in members)
        record(checks, "package_data", 15, data_ok, {"wheel_members": members})
        if not data_ok:
            blocking.append("route data is absent from the wheel")

        shutil.rmtree(build_checkout, ignore_errors=True)
        unrelated = temp / "unrelated-working-directory"
        unrelated.mkdir()
        clean_env = os.environ.copy()
        clean_env.pop("PYTHONPATH", None)

        api = {"returncode": 1, "output": "wheel unavailable", "command": []}
        cli = {"returncode": 1, "output": "wheel unavailable", "command": []}
        unknown_api = {"returncode": 1, "output": "wheel unavailable", "command": []}
        unknown_cli = {"returncode": 0, "output": "wheel unavailable", "command": []}
        if wheel_ok:
            api = run([str(vpython), "-c", "from relaypack import render_route; print(render_route('alpha'))"], cwd=unrelated, env=clean_env)
            cli = run([str(venv / "bin" / "relaypack"), "alpha"], cwd=unrelated, env=clean_env)
            unknown_api = run([str(vpython), "-c", "from relaypack import render_route; render_route('missing')"], cwd=unrelated, env=clean_env)
            unknown_cli = run([str(venv / "bin" / "relaypack"), "missing"], cwd=unrelated, env=clean_env)

        api_ok = api["returncode"] == 0 and api["output"].strip() == EXPECTED
        cli_ok = cli["returncode"] == 0 and cli["output"].strip() == EXPECTED
        unknown_ok = unknown_api["returncode"] != 0 and "KeyError" in unknown_api["output"] and unknown_cli["returncode"] != 0 and "unknown route" in unknown_cli["output"].lower()
        record(checks, "installed_api", 15, api_ok, api)
        record(checks, "installed_cli", 15, cli_ok, cli)
        record(checks, "unknown_route", 5, unknown_ok, {"api": unknown_api, "cli": unknown_cli})
        if not api_ok or not cli_ok:
            blocking.append("the installed API or command fails outside the checkout")
        if not unknown_ok:
            blocking.append("the public API or command contract changes")

    with tempfile.TemporaryDirectory(prefix="relaypack-mutation-") as raw_mutation:
        mutation = Path(raw_mutation) / "seed"
        shutil.copytree(SEED, mutation)
        candidate_tests = candidate / "tests"
        if candidate_tests.exists():
            shutil.rmtree(mutation / "tests")
            shutil.copytree(candidate_tests, mutation / "tests")
        mutated = run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
            cwd=mutation,
            timeout=180,
        )
        regression_ok = mutated["returncode"] != 0
        record(checks, "regression_mutation", 10, regression_ok, mutated)
        if not regression_ok:
            blocking.append("the regression test also passes against the original defect")

    seed_files = {path.relative_to(SEED).as_posix(): path for path in SEED.rglob("*") if path.is_file()}
    candidate_files = {path.relative_to(candidate).as_posix(): path for path in candidate.rglob("*") if path.is_file() and ".agents/" not in path.relative_to(candidate).as_posix() and "__pycache__/" not in path.relative_to(candidate).as_posix() and not path.name.endswith(".pyc")}
    changed = sorted(
        name for name in set(seed_files) | set(candidate_files)
        if name not in seed_files or name not in candidate_files or seed_files[name].read_bytes() != candidate_files[name].read_bytes()
    )
    pyproject = (candidate / "pyproject.toml").read_text(encoding="utf-8")
    setup_cfg = (candidate / "setup.cfg").read_text(encoding="utf-8") if (candidate / "setup.cfg").exists() else ""
    project_section = pyproject.split("[project]", 1)[-1].split("[", 1)[0] if "[project]" in pyproject else ""
    runtime_dependency_added = "dependencies" in project_section or "install_requires" in setup_cfg.lower()
    scope_ok = len(changed) <= 6 and not runtime_dependency_added
    record(checks, "scope", 10, scope_ok, {"changed_files": changed, "runtime_dependency_added": runtime_dependency_added})
    if runtime_dependency_added:
        blocking.append("a runtime dependency is added")

    report_path = candidate / "RUN-REPORT.md"
    report_text = report_path.read_text(encoding="utf-8") if report_path.exists() else ""
    report_lower = report_text.lower()
    evidence_ok = all(token in report_lower for token in ("diagnos", "wheel", "install", "unverified"))
    record(checks, "evidence", 10, evidence_ok, {"path": "RUN-REPORT.md", "required_signals_present": evidence_ok})

    result = {
        "benchmark": "foundry-relaypack-boundary",
        "score": sum(item["earned"] for item in checks),
        "maximum_score": 100,
        "blocking_failures": sorted(set(blocking)),
        "checks": checks,
        "evidence_boundary": "TESTED locally with source tests, a built wheel, an isolated virtual environment, and installed API/CLI subprocesses. No registry publication or cross-platform install was observed.",
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 1 if result["blocking_failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
