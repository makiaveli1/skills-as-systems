#!/usr/bin/env python3
"""Run deterministic FOUNDRY routing, context, adversarial, and artifact-gate checks."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from validate_artifact import validate_value

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_BUDGET = 22_000


def load_json(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8-sig"))


def main() -> int:
    errors: list[str] = []
    routing = load_json("tests/routing-cases.json")
    negative = load_json("tests/negative-routing-cases.json")
    adversarial = load_json("tests/evaluation-cases.json")["cases"]
    available = {path.stem for path in (ROOT / "references").glob("*.md")}
    packet_sizes: list[tuple[int, str]] = []

    for case in routing:
        required = case.get("required_references", [])
        unknown = set(required).difference(available)
        if unknown:
            errors.append(f"{case['id']}: unknown references {sorted(unknown)}")
            continue
        size = sum(
            len((ROOT / "references" / f"{reference}.md").read_text(encoding="utf-8-sig"))
            for reference in required
        )
        packet_sizes.append((size, case["id"]))
        if len(required) > case.get("max_references", 0):
            errors.append(f"{case['id']}: route exceeds its reference count")
        if size > REFERENCE_BUDGET:
            errors.append(f"{case['id']}: route is {size} characters")
        if not case.get("must_not"):
            errors.append(f"{case['id']}: no failure boundaries")

    for case in negative:
        if case.get("expected") != "exclude_foundry":
            errors.append(f"{case.get('id')}: negative case does not exclude FOUNDRY")

    for case in adversarial:
        for key in ("expected_behaviour", "required_evidence", "failure_vetoes"):
            if not case.get(key):
                errors.append(f"{case.get('id')}: missing {key}")

    mutations = []
    system_map = load_json("examples/system-map-example.json")
    system_map["captured_state"]["freshness"] = "stale"
    mutations.append(("stale-understanding", system_map, "sufficient_for_action"))
    contract = load_json("examples/change-contract-example.json")
    contract["authority"]["permissions_carried_by_contract"] = True
    mutations.append(("contract-authority", contract, "permissions"))
    receipt = load_json("examples/verification-receipt-example.json")
    receipt["claims"][0]["evidence_ids"] = []
    mutations.append(("unsupported-tested-claim", receipt, "evidence"))
    continuation = load_json("examples/continuation-record-example.json")
    continuation["safety"]["permissions_carried_over"] = True
    mutations.append(("continuation-authority", continuation, "prohibited"))
    for name, value, expected_fragment in mutations:
        mutation_errors = validate_value(value)
        if not any(expected_fragment in error for error in mutation_errors):
            errors.append(f"{name}: corruption was not rejected as expected")

    if errors:
        print("FOUNDRY scenario evaluation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    largest_size, largest_case = max(packet_sizes)
    print("PASS: FOUNDRY deterministic scenario evaluation")
    print(f"Positive routed scenarios: {len(routing)}")
    print(f"Negative routing scenarios: {len(negative)}")
    print(f"Adversarial engineering scenarios: {len(adversarial)}")
    print(f"Artifact corruption gates: {len(mutations)}")
    print(f"Largest specialist packet: {largest_size} characters ({largest_case})")
    print(f"Specialist packet budget: {REFERENCE_BUDGET} characters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
