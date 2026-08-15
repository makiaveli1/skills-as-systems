#!/usr/bin/env python3
"""Task-specific static acceptance checks for the CAIRN benchmark."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_FILES = ("index.html", "styles.css", "app.js", "RUN-REPORT.md", "data/routes.json")
HOOKS = (
    'data-testid="route-list"',
    "data-route-id",
    "aria-pressed",
    'data-testid="difficulty-filter"',
    'data-testid="group-needs"',
    'data-testid="plan-summary"',
    'data-testid="essentials"',
    'data-testid="confirm-plan"',
    'data-testid="plan-status"',
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.candidate.resolve()
    checks: list[dict] = []

    missing = [name for name in REQUIRED_FILES if not (root / name).is_file()]
    checks.append({"name": "required_files", "passed": not missing, "missing": missing})

    text = "\n".join(
        (root / name).read_text(encoding="utf-8", errors="replace")
        for name in ("index.html", "styles.css", "app.js")
        if (root / name).is_file()
    )
    missing_hooks = [hook for hook in HOOKS if hook not in text]
    checks.append({"name": "automation_contract", "passed": not missing_hooks, "missing": missing_hooks})

    external = sorted(set(re.findall(r"(?:https?:)?//[^\s\"')]+", text)))
    checks.append({"name": "local_only", "passed": not external, "external_references": external})

    routes_ok = False
    route_details: dict = {}
    try:
        routes = json.loads((root / "data" / "routes.json").read_text(encoding="utf-8"))
        route_details = {
            "ids": [item.get("id") for item in routes],
            "statuses": {item.get("id"): item.get("status") for item in routes},
        }
        routes_ok = (
            len(routes) == 3
            and route_details["statuses"].get("bracken-rise") == "closed"
            and all("suitability" in item and "why" in item for item in routes)
        )
    except (OSError, json.JSONDecodeError, TypeError):
        pass
    checks.append({"name": "fresh_route_data", "passed": routes_ok, "evidence": route_details})

    report = (root / "RUN-REPORT.md").read_text(encoding="utf-8", errors="replace") if (root / "RUN-REPORT.md").is_file() else ""
    evidence_terms = {
        "tested": bool(re.search(r"\btested\b", report, re.I)),
        "observed": bool(re.search(r"\bobserved\b", report, re.I)),
        "unverified": bool(re.search(r"\bunverified\b|not (?:tested|observed|verified)", report, re.I)),
    }
    checks.append({"name": "evidence_report", "passed": all(evidence_terms.values()), "signals": evidence_terms})

    result = {
        "project": "cairn",
        "candidate": root.name,
        "checks": checks,
        "passed": all(item["passed"] for item in checks),
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
