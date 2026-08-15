#!/usr/bin/env python3
"""Validate and rerun deterministic layers of the public paired showcases."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BENCHMARKS = ROOT / "benchmarks"
MACHINE_PATHS = (
    re.compile(r"(?<![A-Za-z0-9])/Users/[A-Za-z0-9._-]+/"),
    re.compile(r"(?<![A-Za-z0-9])/home/[A-Za-z0-9._-]+/"),
    re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\"),
)
TEXT_SUFFIXES = {".md", ".json", ".py", ".js", ".cjs", ".html", ".css", ".toml", ".cfg", ".txt"}
GENERATED_PARTS = {"__pycache__", ".pytest_cache", "build", "dist"}


def run(command: list[str], errors: list[str]) -> None:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=240,
    )
    if result.returncode != 0:
        errors.append(f"failed command {' '.join(command)}:\n{result.stdout[-4000:]}")


def load(relative: str, errors: list[str]):
    try:
        return json.loads((ROOT / relative).read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"invalid JSON {relative}: {error}")
        return None


def validate_receipts(errors: list[str]) -> None:
    sitecraft = load("benchmarks/sitecraft-tideglass/results.json", errors)
    if isinstance(sitecraft, dict):
        conditions = sitecraft.get("conditions", {})
        expected = {
            "baseline": (55, "pass", 42.5, 97.5),
            "with_sitecraft": (55, "pass", 42, 97),
        }
        for name, values in expected.items():
            condition = conditions.get(name, {})
            actual = (
                condition.get("static_score"),
                condition.get("browser_gate"),
                condition.get("blind_visual_score"),
                condition.get("total"),
            )
            if actual != values:
                errors.append(f"SITECRAFT receipt drift for {name}: {actual!r}")

    for benchmark in ("foundry-ledger-repair", "foundry-relaypack-boundary"):
        result = load(f"benchmarks/{benchmark}/results.json", errors)
        if not isinstance(result, dict):
            continue
        for name in ("baseline", "with_foundry"):
            condition = result.get("conditions", {}).get(name, {})
            if condition.get("score") != 100 or condition.get("blocking_failures") != []:
                errors.append(f"{benchmark} public result is not the recorded passing result: {name}")
            evidence_name = "with-foundry.json" if name == "with_foundry" else "baseline.json"
            evidence = load(f"benchmarks/{benchmark}/evidence/{evidence_name}", errors)
            if isinstance(evidence, dict) and (
                evidence.get("score") != 100 or evidence.get("blocking_failures") != []
            ):
                errors.append(f"{benchmark} evidence receipt drift: {evidence_name}")

    for name in ("baseline", "with-sitecraft"):
        receipt = load(f"benchmarks/sitecraft-tideglass/evidence/{name}/browser-results.json", errors)
        if isinstance(receipt, dict) and receipt.get("passed") is not True:
            errors.append(f"SITECRAFT browser receipt is not passing: {name}")
        if isinstance(receipt, dict) and receipt.get("source") != "local index.html":
            errors.append(f"SITECRAFT browser receipt exposes or drifts source path: {name}")


def validate_hygiene(errors: list[str]) -> None:
    if not BENCHMARKS.is_dir():
        errors.append("benchmarks directory is missing")
        return
    for path in BENCHMARKS.rglob("*"):
        relative = path.relative_to(ROOT).as_posix()
        if ".agents" in path.parts or ".claude" in path.parts:
            errors.append(f"installed skill or host state leaked into showcase: {relative}")
        if any(part in GENERATED_PARTS or part.endswith(".egg-info") for part in path.parts):
            errors.append(f"generated build/test debris leaked into showcase: {relative}")
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            errors.append(f"non-UTF-8 benchmark text: {relative}")
            continue
        if any(pattern.search(text) for pattern in MACHINE_PATHS):
            errors.append(f"machine-specific path in public benchmark: {relative}")
        if "outputs" in path.parts and (
            "chain of thought" in text.casefold()
            or "private reasoning transcript" in text.casefold()
        ):
            errors.append(f"private-reasoning material named inside output: {relative}")


def rerun_deterministic_layers(errors: list[str]) -> None:
    python = sys.executable
    for condition in ("baseline", "with-sitecraft"):
        run(
            [
                python,
                "benchmarks/sitecraft-tideglass/evaluation/evaluate_static.py",
                f"benchmarks/sitecraft-tideglass/outputs/{condition}",
            ],
            errors,
        )
    for condition in ("baseline", "with-foundry"):
        run(
            [
                python,
                "benchmarks/foundry-ledger-repair/evaluation/evaluate.py",
                f"benchmarks/foundry-ledger-repair/outputs/{condition}",
            ],
            errors,
        )
        run(
            [
                python,
                "benchmarks/foundry-relaypack-boundary/evaluation/evaluate.py",
                f"benchmarks/foundry-relaypack-boundary/outputs/{condition}",
            ],
            errors,
        )


def main() -> int:
    errors: list[str] = []
    validate_hygiene(errors)
    validate_receipts(errors)
    rerun_deterministic_layers(errors)
    if errors:
        print("Benchmark validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Benchmark validation passed (paired outputs, receipts, hygiene, deterministic reruns).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
