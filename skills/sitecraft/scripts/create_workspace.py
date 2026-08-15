#!/usr/bin/env python3
"""Create a portable SITECRAFT project workspace without overwriting files."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "sitecraft-project"


def build_contract(project: str) -> dict:
    template = json.loads(
        (ROOT / "assets" / "experience-contract-template.json").read_text(
            encoding="utf-8-sig"
        )
    )
    template["contract_id"] = f"{slugify(project)}-experience-v1"
    template["project"] = project
    template["owner"] = ""
    template["updated_at"] = date.today().isoformat()
    return template


def build_review(project: str) -> dict:
    template = json.loads(
        (ROOT / "assets" / "sitecraft-review-template.json").read_text(
            encoding="utf-8-sig"
        )
    )
    template["review_id"] = f"{slugify(project)}-review-v1"
    template["project"] = project
    template["exact_state"]["observed_at"] = date.today().isoformat()
    return template


def build_handoff(project: str) -> dict:
    template = json.loads(
        (ROOT / "assets" / "handoff-packet-template.json").read_text(
            encoding="utf-8-sig"
        )
    )
    template["handoff_id"] = f"{slugify(project)}-handoff-v1"
    template["generated_at"] = date.today().isoformat()
    template["project"]["name"] = project
    template["project"]["workspace_reference"] = "."
    template["contract"]["reference"] = "contracts/experience-contract.json"
    return template


def create_workspace(destination: Path, project: str) -> list[Path]:
    if destination.exists():
        raise FileExistsError(f"Destination already exists: {destination}")

    directories = [
        destination / "contracts",
        destination / "reviews",
        destination / "evidence" / "screenshots",
        destination / "evidence" / "recordings",
        destination / "evidence" / "reports",
        destination / "prompts",
        destination / "research",
        destination / "assets" / "source",
        destination / "assets" / "derived",
        destination / "decisions",
        destination / "handoffs",
    ]

    created: list[Path] = []
    try:
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=False)
            created.append(directory)

        contract_path = destination / "contracts" / "experience-contract.json"
        contract_path.write_text(
            json.dumps(build_contract(project), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        created.append(contract_path)

        review_path = destination / "reviews" / "review-template.json"
        review_path.write_text(
            json.dumps(build_review(project), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        created.append(review_path)

        handoff_path = destination / "handoffs" / "sitecraft-handoff.json"
        handoff_path.write_text(
            json.dumps(build_handoff(project), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        created.append(handoff_path)

        copies = {
            ROOT / "assets" / "ai-builder-work-packet.md": destination
            / "prompts"
            / "ai-builder-work-packet.md",
            ROOT / "assets" / "image-generation-pack.md": destination
            / "prompts"
            / "image-generation-pack.md",
            ROOT / "assets" / "video-generation-pack.md": destination
            / "prompts"
            / "video-generation-pack.md",
            ROOT / "assets" / "video-generation-workflow-template.json": destination
            / "contracts"
            / "video-generation-workflow-template.json",
            ROOT / "assets" / "asset-ledger.csv": destination
            / "assets"
            / "asset-ledger.csv",
            ROOT / "assets" / "reference-role-map.csv": destination
            / "research"
            / "reference-role-map.csv",
            ROOT / "assets" / "evidence-matrix.csv": destination
            / "evidence"
            / "evidence-matrix.csv",
            ROOT / "assets" / "platform-evidence-matrix.csv": destination
            / "evidence"
            / "platform-evidence-matrix.csv",
            ROOT / "assets" / "decision-log.csv": destination
            / "decisions"
            / "decision-log.csv",
        }
        for source, target in copies.items():
            shutil.copyfile(source, target)
            created.append(target)
    except Exception:
        shutil.rmtree(destination, ignore_errors=True)
        raise

    return created


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="New workspace directory")
    parser.add_argument("--project", required=True, help="Human-readable project name")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        created = create_workspace(args.destination.expanduser().resolve(), args.project)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"SITECRAFT workspace creation failed: {exc}", file=sys.stderr)
        return 1

    print(f"Created SITECRAFT workspace: {args.destination}")
    for path in created:
        print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
