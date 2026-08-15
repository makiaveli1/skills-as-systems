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
    sitecraft = load(
        "benchmarks/deep-baseline-study/sitecraft/results/results.json", errors
    )
    if isinstance(sitecraft, dict):
        candidates = sitecraft.get("candidates", {})
        expected_candidates = {
            "baseline-1": ("baseline", "pass", "pass", 15, 4),
            "baseline-2": ("baseline", "pass", "pass", 22, 2),
            "skilled-1": ("named_skill", "pass", "pass", 24, 1),
            "skilled-2": ("named_skill", "pass", "pass", 20, 3),
        }
        for name, values in expected_candidates.items():
            candidate = candidates.get(name, {})
            actual = (
                candidate.get("condition"),
                candidate.get("static_acceptance"),
                candidate.get("browser_acceptance"),
                candidate.get("blind_visual_score"),
                candidate.get("blind_rank"),
            )
            if actual != values:
                errors.append(f"SITECRAFT deep-study receipt drift for {name}: {actual!r}")
        summary = sitecraft.get("condition_summary", {})
        summary_actual = (
            summary.get("baseline", {}).get("functional_passes"),
            summary.get("baseline", {}).get("mean_blind_visual_score"),
            summary.get("named_skill", {}).get("functional_passes"),
            summary.get("named_skill", {}).get("mean_blind_visual_score"),
            summary.get("visual_score_difference"),
            summary.get("paired_visual_differences"),
            summary.get("repeatable_visual_advantage"),
            sitecraft.get("decision"),
        )
        summary_expected = (
            2,
            18.5,
            2,
            22.0,
            3.5,
            {"replicate_1": 9, "replicate_2": -2},
            False,
            "inconclusive_for_repeatable_output_superiority",
        )
        if summary_actual != summary_expected:
            errors.append(f"SITECRAFT deep-study summary drift: {summary_actual!r}")
        for name in ("skilled-1", "skilled-2"):
            if candidates.get(name, {}).get("skill_reopened_in_turns") != [1, 2, 3]:
                errors.append(f"SITECRAFT lifecycle evidence drift for {name}")

    blind = load(
        "benchmarks/deep-baseline-study/sitecraft/results/blind-visual-review.json",
        errors,
    )
    if isinstance(blind, dict) and (
        blind.get("winner") != "C" or blind.get("ranking") != ["C", "D", "A", "B"]
    ):
        errors.append("SITECRAFT blind review result drift")
    condition_map = load(
        "benchmarks/deep-baseline-study/sitecraft/results/condition-map.json", errors
    )
    expected_map = {
        "A": "skilled-2",
        "B": "baseline-1",
        "C": "skilled-1",
        "D": "baseline-2",
    }
    if condition_map != expected_map:
        errors.append(f"SITECRAFT blind condition map drift: {condition_map!r}")

    execution = load(
        "benchmarks/deep-baseline-study/sitecraft/results/execution-summary.json",
        errors,
    )
    if isinstance(execution, dict):
        execution_candidates = execution.get("candidates", {})
        for name in ("baseline-1", "baseline-2", "skilled-1", "skilled-2"):
            turns = execution_candidates.get(name)
            if not isinstance(turns, list) or [item.get("turn") for item in turns] != [1, 2, 3]:
                errors.append(f"SITECRAFT execution turn coverage drift: {name}")
                continue
            read_counts = [item.get("skill_read_commands") for item in turns]
            if name.startswith("baseline") and read_counts != [0, 0, 0]:
                errors.append(f"SITECRAFT baseline unexpectedly records skill reads: {name}")
            if name.startswith("skilled") and not all(
                isinstance(count, int) and count > 0 for count in read_counts
            ):
                errors.append(f"SITECRAFT skilled run lacks lifecycle reads: {name}")
            if not all(
                isinstance(item.get("completed_commands"), int)
                and item["completed_commands"] > 0
                and isinstance(item.get("usage"), dict)
                and isinstance(item["usage"].get("input_tokens"), int)
                and item["usage"]["input_tokens"] > 0
                for item in turns
            ):
                errors.append(f"SITECRAFT execution metadata is incomplete: {name}")
        if execution.get("private_reasoning_published") is not False:
            errors.append("SITECRAFT execution summary must exclude private reasoning")

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

    for name in ("baseline-1", "baseline-2", "skilled-1", "skilled-2"):
        base = "benchmarks/deep-baseline-study/sitecraft/results/evidence"
        static = load(f"{base}/{name}/static-results.json", errors)
        browser = load(f"{base}/{name}/browser-results.json", errors)
        if isinstance(static, dict) and static.get("passed") is not True:
            errors.append(f"SITECRAFT static receipt is not passing: {name}")
        if isinstance(browser, dict) and browser.get("passed") is not True:
            errors.append(f"SITECRAFT browser receipt is not passing: {name}")


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
    for condition in ("baseline-1", "baseline-2", "skilled-1", "skilled-2"):
        run(
            [
                python,
                "benchmarks/deep-baseline-study/sitecraft/evaluation/evaluate_static.py",
                f"benchmarks/deep-baseline-study/sitecraft/results/candidates/{condition}",
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
