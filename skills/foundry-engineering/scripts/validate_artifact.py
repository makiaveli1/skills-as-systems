#!/usr/bin/env python3
"""Validate FOUNDRY machine artifacts and their internal references."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {
    "foundry-system-map": ROOT / "schemas" / "system-map.schema.json",
    "foundry-change-contract": ROOT / "schemas" / "change-contract.schema.json",
    "foundry-verification-receipt": ROOT / "schemas" / "verification-receipt.schema.json",
    "foundry-continuation-record": ROOT / "schemas" / "continuation-record.schema.json",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def duplicate_values(values: Iterable[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def schema_errors(value: Any, schema_path: Path) -> list[str]:
    schema = load_json(schema_path)
    try:
        import jsonschema  # type: ignore
    except ImportError:
        required = set(schema.get("required", []))
        missing = sorted(required.difference(value if isinstance(value, dict) else {}))
        return [f"missing required fields: {', '.join(missing)}"] if missing else []

    validator = jsonschema.Draft202012Validator(
        schema,
        format_checker=jsonschema.FormatChecker(),
    )
    errors: list[str] = []
    for error in sorted(validator.iter_errors(value), key=lambda item: list(item.absolute_path)):
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"{location}: {error.message}")
    return errors


def validate_system_map(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    subsystem_ids = [item.get("subsystem_id", "") for item in value.get("subsystems", [])]
    for duplicate in duplicate_values(subsystem_ids):
        errors.append(f"duplicate subsystem_id: {duplicate}")
    known_subsystems = set(subsystem_ids)
    for path in value.get("behavioural_paths", []):
        if path.get("owner") not in known_subsystems:
            errors.append(
                f"behavioural path {path.get('path_id')} has unknown owner {path.get('owner')}"
            )
    claim_ids = [item.get("claim_id", "") for item in value.get("knowledge", [])]
    for duplicate in duplicate_values(claim_ids):
        errors.append(f"duplicate knowledge claim_id: {duplicate}")
    sufficiency = value.get("sufficiency", {})
    if sufficiency.get("sufficient_for_action") and value.get("captured_state", {}).get("freshness") != "current":
        errors.append("sufficient_for_action requires captured_state.freshness=current")
    return errors


def validate_change_contract(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    invariant_ids = [item.get("invariant_id", "") for item in value.get("invariants", [])]
    risk_ids = [item.get("risk_id", "") for item in value.get("risks", [])]
    claim_ids = [item.get("claim_id", "") for item in value.get("verification_plan", [])]
    for label, values in (
        ("invariant_id", invariant_ids),
        ("risk_id", risk_ids),
        ("verification claim_id", claim_ids),
    ):
        for duplicate in duplicate_values(values):
            errors.append(f"duplicate {label}: {duplicate}")

    known_invariants = set(invariant_ids)
    known_risks = set(risk_ids)
    for item in value.get("verification_plan", []):
        for invariant_id in item.get("invariant_ids", []):
            if invariant_id not in known_invariants:
                errors.append(
                    f"verification claim {item.get('claim_id')} references unknown invariant {invariant_id}"
                )
        for risk_id in item.get("risk_ids", []):
            if risk_id not in known_risks:
                errors.append(
                    f"verification claim {item.get('claim_id')} references unknown risk {risk_id}"
                )
    if value.get("authority", {}).get("permissions_carried_by_contract") is not False:
        errors.append("Change Contract cannot carry permissions")
    return errors


def validate_verification_receipt(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    checks = value.get("checks", [])
    claims = value.get("claims", [])
    check_ids = [item.get("check_id", "") for item in checks]
    claim_ids = [item.get("claim_id", "") for item in claims]
    for label, values in (("check_id", check_ids), ("claim_id", claim_ids)):
        for duplicate in duplicate_values(values):
            errors.append(f"duplicate {label}: {duplicate}")

    known_checks = set(check_ids)
    known_claims = set(claim_ids)
    check_outcomes = {item.get("check_id"): item.get("outcome") for item in checks}
    for check in checks:
        for claim_id in check.get("claim_ids", []):
            if claim_id not in known_claims:
                errors.append(f"check {check.get('check_id')} references unknown claim {claim_id}")
    for claim in claims:
        evidence_ids = claim.get("evidence_ids", [])
        for evidence_id in evidence_ids:
            if evidence_id not in known_checks:
                errors.append(f"claim {claim.get('claim_id')} references unknown check {evidence_id}")
        if claim.get("status") in {"TESTED", "OBSERVED"}:
            if not evidence_ids:
                errors.append(f"{claim.get('status')} claim {claim.get('claim_id')} lacks evidence")
            elif not all(check_outcomes.get(evidence_id) == "passed" for evidence_id in evidence_ids):
                errors.append(
                    f"{claim.get('status')} claim {claim.get('claim_id')} uses non-passing evidence"
                )
    if value.get("verdict") == "passed":
        if any(item.get("status") in {"INFERRED", "UNVERIFIED"} for item in claims):
            errors.append("verdict=passed cannot contain INFERRED or UNVERIFIED claims")
        if any(item.get("outcome") != "passed" for item in checks):
            errors.append("verdict=passed requires every recorded check to pass")
        if value.get("state", {}).get("evidence_freshness") != "current":
            errors.append("verdict=passed requires current evidence")
    return errors


def validate_continuation(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    dependency_ids = [item.get("dependency_id", "") for item in value.get("dependencies", [])]
    work_ids = [item.get("work_id", "") for item in value.get("next_eligible_work", [])]
    finding_ids = [item.get("finding_id", "") for item in value.get("established_findings", [])]
    for label, values in (
        ("dependency_id", dependency_ids),
        ("work_id", work_ids),
        ("finding_id", finding_ids),
    ):
        for duplicate in duplicate_values(values):
            errors.append(f"duplicate {label}: {duplicate}")
    known_dependencies = set(dependency_ids)
    for item in value.get("next_eligible_work", []):
        for dependency_id in item.get("dependency_ids", []):
            if dependency_id not in known_dependencies:
                errors.append(
                    f"work {item.get('work_id')} references unknown dependency {dependency_id}"
                )
    safety = value.get("safety", {})
    if any(safety.get(key) is not False for key in (
        "contains_hidden_reasoning",
        "contains_transcript",
        "contains_secrets",
        "permissions_carried_over",
    )):
        errors.append("continuation contains or carries prohibited state")
    if any(safety.get(key) is not True for key in (
        "receiving_worker_must_refresh_state",
        "receiving_worker_must_rediscover_capabilities",
    )):
        errors.append("continuation must require state and capability refresh")
    if value.get("status") == "complete" and value.get("unresolved"):
        errors.append("complete continuation cannot retain unresolved work")
    return errors


CROSS_VALIDATORS = {
    "foundry-system-map": validate_system_map,
    "foundry-change-contract": validate_change_contract,
    "foundry-verification-receipt": validate_verification_receipt,
    "foundry-continuation-record": validate_continuation,
}


def validate_value(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["artifact root must be an object"]
    artifact_type = value.get("artifact_type")
    schema_path = SCHEMAS.get(artifact_type)
    if schema_path is None:
        return [f"unknown artifact_type: {artifact_type!r}"]
    errors = schema_errors(value, schema_path)
    errors.extend(CROSS_VALIDATORS[artifact_type](value))
    return errors


def validate_file(path: Path) -> tuple[list[str], dict[str, Any] | None]:
    try:
        value = load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"unable to read JSON: {exc}"], None
    return validate_value(value), value if isinstance(value, dict) else None


def validate_bundle(values: list[tuple[Path, dict[str, Any]]]) -> list[str]:
    errors: list[str] = []
    by_type = {value.get("artifact_type"): (path, value) for path, value in values}
    system_map = by_type.get("foundry-system-map")
    contract = by_type.get("foundry-change-contract")
    verification = by_type.get("foundry-verification-receipt")
    continuation = by_type.get("foundry-continuation-record")

    if system_map and contract:
        map_project = system_map[1].get("project", {}).get("name")
        if contract[1].get("project_ref") != map_project:
            errors.append("bundle project mismatch between System Map and Change Contract")
    if contract and verification:
        if contract[1].get("project_ref") != verification[1].get("project_ref"):
            errors.append("bundle project mismatch between Change Contract and Verification Receipt")
        planned = {item.get("claim_id") for item in contract[1].get("verification_plan", [])}
        recorded = {item.get("claim_id") for item in verification[1].get("claims", [])}
        missing = sorted(planned.difference(recorded))
        if missing:
            errors.append(f"verification receipt misses planned claims: {', '.join(missing)}")
    if continuation:
        project_refs = {
            value.get("project_ref")
            for _, value in values
            if value.get("artifact_type") != "foundry-system-map"
        }
        if len(project_refs) > 1:
            errors.append("bundle project mismatch involving Continuation Record")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--bundle", action="store_true", help="also check cross-artifact consistency")
    args = parser.parse_args(argv)

    loaded: list[tuple[Path, dict[str, Any]]] = []
    failed = False
    for path in args.paths:
        errors, value = validate_file(path)
        if errors:
            failed = True
            print(f"INVALID: {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"VALID: {path}")
            if value is not None:
                loaded.append((path, value))
    if args.bundle and not failed:
        errors = validate_bundle(loaded)
        if errors:
            failed = True
            print("INVALID BUNDLE")
            for error in errors:
                print(f"  - {error}")
        else:
            print("VALID BUNDLE")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
