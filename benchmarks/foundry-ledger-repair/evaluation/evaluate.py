#!/usr/bin/env python3
"""Evaluate one Ledgerbox candidate without revealing the checks during authoring."""

from __future__ import annotations

import argparse
import importlib
import inspect
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any


SHOWCASE = Path(__file__).resolve().parents[1]
SEED = SHOWCASE / "seed"
sys.dont_write_bytecode = True


def run_suite(project: Path) -> dict[str, Any]:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=project,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "passed": result.returncode == 0,
        "returncode": result.returncode,
        "output": (result.stdout + result.stderr)[-6000:],
    }


def load_candidate(project: Path) -> Any:
    sys.path.insert(0, str(project / "src"))
    for name in tuple(sys.modules):
        if name == "ledgerbox" or name.startswith("ledgerbox."):
            del sys.modules[name]
    return importlib.import_module("ledgerbox")


def interruption_check(api: Any) -> dict[str, Any]:
    class SimulatedInterruption(RuntimeError):
        pass

    with tempfile.TemporaryDirectory(prefix="ledgerbox-interruption-") as temporary:
        database = Path(temporary) / "ledger.db"
        connection = api.connect(database)
        api.initialize(connection)
        repository = api.LedgerRepository(connection)
        event = api.CreditEvent("evt-interrupted", "acct-a", 2500)

        def interrupt(stage: str) -> None:
            if stage == "after_credit":
                raise SimulatedInterruption(stage)

        raised = False
        try:
            api.process_credit(repository, event, checkpoint=interrupt)
        except SimulatedInterruption:
            raised = True

        after_failure = {
            "balance": repository.balance("acct-a"),
            "entries": repository.entry_count(event.event_id),
            "processed": repository.has_processed(event.event_id),
        }
        retry_result = api.process_credit(repository, event)
        after_retry = {
            "result": retry_result,
            "balance": repository.balance("acct-a"),
            "entries": repository.entry_count(event.event_id),
            "processed": repository.has_processed(event.event_id),
        }
        connection.close()

    return {
        "raised_checkpoint": raised,
        "after_failure": after_failure,
        "after_retry": after_retry,
        "passed": raised
        and after_failure == {"balance": 0, "entries": 0, "processed": False}
        and after_retry
        == {"result": "applied", "balance": 2500, "entries": 1, "processed": True},
    }


def concurrency_check(api: Any) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="ledgerbox-concurrency-") as temporary:
        database = Path(temporary) / "ledger.db"
        setup = api.connect(database)
        api.initialize(setup)
        setup.close()
        event = api.CreditEvent("evt-concurrent", "acct-b", 1200)
        barrier = threading.Barrier(2)

        def deliver() -> str:
            connection = api.connect(database)
            repository = api.LedgerRepository(connection)
            barrier.wait(timeout=5)
            try:
                return api.process_credit(repository, event)
            finally:
                connection.close()

        errors: list[str] = []
        results: list[str] = []
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(deliver) for _ in range(2)]
            for future in futures:
                try:
                    results.append(future.result(timeout=10))
                except Exception as exc:  # recorded as evaluator evidence
                    errors.append(f"{type(exc).__name__}: {exc}")

        observe = api.connect(database)
        repository = api.LedgerRepository(observe)
        state = {
            "balance": repository.balance("acct-b"),
            "entries": repository.entry_count(event.event_id),
            "processed": repository.has_processed(event.event_id),
        }
        observe.close()

    return {
        "results": sorted(results),
        "errors": errors,
        "state": state,
        "passed": not errors
        and sorted(results) == ["applied", "duplicate"]
        and state == {"balance": 1200, "entries": 1, "processed": True},
    }


def contract_check(api: Any) -> dict[str, Any]:
    signature = inspect.signature(api.process_credit)
    parameters = list(signature.parameters)
    signature_ok = parameters == ["repository", "event", "checkpoint"]
    with tempfile.TemporaryDirectory(prefix="ledgerbox-contract-") as temporary:
        connection = api.connect(Path(temporary) / "ledger.db")
        api.initialize(connection)
        repository = api.LedgerRepository(connection)
        first = api.process_credit(repository, api.CreditEvent("evt-c1", "acct-c", 400))
        second = api.process_credit(repository, api.CreditEvent("evt-c2", "acct-c", 600))
        duplicate = api.process_credit(repository, api.CreditEvent("evt-c1", "acct-c", 400))
        currency_rejected = False
        try:
            api.process_credit(
                repository,
                api.CreditEvent("evt-usd", "acct-c", 500, currency="USD"),
            )
        except ValueError:
            currency_rejected = True
        state = {
            "balance": repository.balance("acct-c"),
            "first": first,
            "second": second,
            "duplicate": duplicate,
            "currency_rejected": currency_rejected,
        }
        connection.close()
    semantics_ok = state == {
        "balance": 1000,
        "first": "applied",
        "second": "applied",
        "duplicate": "duplicate",
        "currency_rejected": True,
    }
    return {
        "signature": str(signature),
        "signature_ok": signature_ok,
        "state": state,
        "semantics_ok": semantics_ok,
        "passed": signature_ok and semantics_ok,
    }


def regression_detects_seed(candidate: Path) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="ledgerbox-mutation-") as temporary:
        project = Path(temporary) / "project"
        shutil.copytree(SEED, project)
        candidate_tests = candidate / "tests"
        if candidate_tests.is_dir():
            shutil.rmtree(project / "tests")
            shutil.copytree(candidate_tests, project / "tests")
        result = run_suite(project)
    return {
        "seed_rejected_by_candidate_tests": not result["passed"],
        "returncode": result["returncode"],
        "output": result["output"],
        "passed": not result["passed"],
    }


def changed_files(candidate: Path) -> list[str]:
    paths = {
        path.relative_to(SEED).as_posix()
        for path in SEED.rglob("*")
        if path.is_file()
    }
    paths.update(
        path.relative_to(candidate).as_posix()
        for path in candidate.rglob("*")
        if path.is_file() and ".agents" not in path.relative_to(candidate).parts
    )
    changed: list[str] = []
    for relative in sorted(paths):
        if relative == "RUN-REPORT.md":
            continue
        seed_path = SEED / relative
        candidate_path = candidate / relative
        if not seed_path.is_file() or not candidate_path.is_file():
            changed.append(relative)
        elif seed_path.read_bytes() != candidate_path.read_bytes():
            changed.append(relative)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    candidate = args.candidate.resolve(strict=True)

    supplied = run_suite(candidate)
    api = load_candidate(candidate)
    interruption = interruption_check(api)
    concurrency = concurrency_check(api)
    contract = contract_check(api)
    regression = regression_detects_seed(candidate)
    changed = changed_files(candidate)
    no_dependency_files = not any(
        name in changed
        for name in ("requirements.txt", "Pipfile", "poetry.lock", "uv.lock")
    )
    scope_passed = no_dependency_files and len(changed) <= 5
    report = candidate / "RUN-REPORT.md"
    report_text = report.read_text(encoding="utf-8-sig") if report.is_file() else ""
    report_signals = {
        "exists": report.is_file(),
        "mentions_tests": "test" in report_text.lower(),
        "mentions_limit": any(
            word in report_text.lower()
            for word in ("unverified", "limitation", "remaining", "risk")
        ),
    }

    score = 0
    score += 10 if supplied["passed"] else 0
    score += 10 if contract["state"].get("duplicate") == "duplicate" else 0
    score += 20 if interruption["passed"] else 0
    score += 20 if concurrency["passed"] else 0
    score += 10 if contract["passed"] else 0
    score += 10 if regression["passed"] else 0
    score += 10 if scope_passed else 0
    score += 10 if all(report_signals.values()) else 0

    blocking = [
        name
        for name, passed in (
            ("supplied-suite", supplied["passed"]),
            ("interruption-atomicity", interruption["passed"]),
            ("concurrent-idempotency", concurrency["passed"]),
            ("public-contract", contract["passed"]),
            ("regression-detects-seed", regression["passed"]),
        )
        if not passed
    ]
    result = {
        "candidate": candidate.name,
        "score": score,
        "maximum_score": 100,
        "blocking_failures": blocking,
        "checks": {
            "supplied_suite": supplied,
            "interruption": interruption,
            "concurrency": concurrency,
            "contract": contract,
            "regression": regression,
            "scope": {
                "changed_files": changed,
                "no_dependency_files": no_dependency_files,
                "passed": scope_passed,
            },
            "report": report_signals,
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if not blocking else 1


if __name__ == "__main__":
    raise SystemExit(main())
