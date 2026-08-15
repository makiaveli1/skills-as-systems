#!/usr/bin/env python3
"""Validate the portable FOUNDRY skill package."""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path
from typing import Any

from validate_artifact import validate_file

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.2.0"
REQUIRED_FILES = {
    "SKILL.md",
    "VERSION",
    "agents/openai.yaml",
    "pyproject.toml",
    "pc-bridge.skill.json",
    "scripts/validate_artifact.py",
    "scripts/evaluate_scenarios.py",
    "scripts/validate_skill.py",
    "schemas/system-map.schema.json",
    "schemas/change-contract.schema.json",
    "schemas/verification-receipt.schema.json",
    "schemas/continuation-record.schema.json",
    "assets/system-map-template.json",
    "assets/change-contract-template.json",
    "assets/verification-receipt-template.json",
    "assets/continuation-record-template.json",
    "examples/system-map-example.json",
    "examples/change-contract-example.json",
    "examples/verification-receipt-example.json",
    "examples/continuation-record-example.json",
    "tests/routing-cases.json",
    "tests/negative-routing-cases.json",
    "tests/evaluation-cases.json",
    "tests/test_package.py",
    "examples/scenario-walkthroughs.md",
    "bridge_v2_tests.py",
}
EXPECTED_WORKFLOWS = {
    "foundry-safe-change": ["understand-contract", "implement-bounded", "verify-challenge", "close-continue"],
    "foundry-debug-repair": ["reproduce-narrow", "repair-cause", "replay-regress-widen"],
}
MACHINE_PATH_PATTERNS = [
    re.compile(r"/Users/[A-Za-z0-9._-]+/"),
    re.compile(r"/home/[A-Za-z0-9._-]+/"),
    re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\"),
]
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".py", ".toml", ".csv"}


def load_json(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8-sig"))


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must begin with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("SKILL.md frontmatter is not closed")
    values: dict[str, str] = {}
    for raw_line in text[4:end].splitlines():
        if not raw_line.strip():
            continue
        if ":" not in raw_line:
            raise ValueError(f"malformed frontmatter line: {raw_line!r}")
        key, value = raw_line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def slugify_heading(text: str) -> str:
    text = re.sub(r"[`*_]", "", text).strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    return re.sub(r"[\s-]+", "-", text).strip("-")


def resolve_selector(selector: str) -> tuple[Path, str | None]:
    file_part, separator, anchor = selector.partition("#")
    return ROOT / file_part, anchor if separator else None


def selector_exists(selector: str) -> bool:
    path, anchor = resolve_selector(selector)
    if not path.is_file():
        return False
    if not anchor or path.suffix.lower() != ".md":
        return True
    headings = {
        slugify_heading(match.group(1))
        for match in re.finditer(r"^#{1,6}\s+(.+?)\s*$", path.read_text(encoding="utf-8-sig"), re.MULTILINE)
    }
    return anchor in headings


def validate_required_files(errors: list[str]) -> None:
    for relative in sorted(REQUIRED_FILES):
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")


def validate_skill_md(errors: list[str]) -> None:
    path = ROOT / "SKILL.md"
    text = path.read_text(encoding="utf-8-sig")
    try:
        frontmatter = parse_frontmatter(text)
    except ValueError as exc:
        errors.append(str(exc))
        return
    if set(frontmatter) != {"name", "description"}:
        errors.append("SKILL.md frontmatter must contain only name and description")
    if frontmatter.get("name") != "foundry-engineering":
        errors.append("SKILL.md name must be foundry-engineering")
    if len(frontmatter.get("description", "")) < 160:
        errors.append("SKILL.md description is too short for reliable engineering routing")
    if len(text) > 10_250:
        errors.append(f"SKILL.md exceeds the 10,250-character Fabric budget: {len(text)}")
    if len(text.splitlines()) > 500:
        errors.append("SKILL.md exceeds the 500-line progressive-disclosure limit")
    for selector in re.findall(r"\]\(([^)]+)\)", text):
        if "://" in selector or selector.startswith("#"):
            continue
        if not selector_exists(selector):
            errors.append(f"broken SKILL.md link: {selector}")
    required_phrases = [
        "Understand first. Change deliberately. Verify reality. Preserve what already works.",
        "KNOWN",
        "TESTED",
        "smallest coherent change",
        "permissions",
    ]
    for phrase in required_phrases:
        if phrase not in text:
            errors.append(f"SKILL.md missing governing phrase: {phrase}")


def validate_openai_yaml(errors: list[str]) -> None:
    text = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8-sig")
    for fragment in (
        'display_name: "FOUNDRY"',
        'default_prompt: "Use $foundry-engineering',
        "allow_implicit_invocation: true",
    ):
        if fragment not in text:
            errors.append(f"agents/openai.yaml missing: {fragment}")
    match = re.search(r'short_description:\s*"([^"]+)"', text)
    if not match or not 25 <= len(match.group(1)) <= 64:
        errors.append("agents/openai.yaml short_description must be quoted and 25-64 characters")


def validate_version_metadata(errors: list[str]) -> None:
    if (ROOT / "VERSION").read_text(encoding="utf-8-sig").strip() != VERSION:
        errors.append(f"VERSION must be {VERSION}")
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8-sig")
    for fragment in (
        'name = "foundry-engineering-skill"',
        f'version = "{VERSION}"',
        'test_entry = "bridge_v2_tests.py"',
    ):
        if fragment not in text:
            errors.append(f"pyproject.toml missing: {fragment}")


def validate_manifest(errors: list[str]) -> None:
    manifest = load_json("pc-bridge.skill.json")
    if manifest.get("schema_version") != "1.1":
        errors.append("pc-bridge.skill.json schema_version must be 1.1")
    if manifest.get("version") != VERSION:
        errors.append(f"pc-bridge.skill.json version must be {VERSION}")
    if "any" not in manifest.get("hosts", []):
        errors.append("pc-bridge.skill.json must support host 'any'")
    if manifest.get("requires") or manifest.get("conflicts"):
        errors.append("portable v1 must not require or conflict with another skill")
    if not 16 <= len(manifest.get("intents", [])) <= 24:
        errors.append("manifest intents must stay between 16 and 24")
    if len(manifest.get("negative_triggers", [])) < 6:
        errors.append("manifest needs at least six negative triggers")
    hints = manifest.get("reference_hints", [])
    if not 16 <= len(hints) <= 24:
        errors.append("manifest reference_hints must stay between 16 and 24")
    for index, hint in enumerate(hints):
        if not hint.get("terms") or not hint.get("paths"):
            errors.append(f"reference hint {index} lacks terms or paths")
        if len(hint.get("paths", [])) > 5:
            errors.append(f"reference hint {index} exceeds five paths")
        for selector in hint.get("paths", []):
            if not selector_exists(selector):
                errors.append(f"manifest selector does not exist: {selector}")

    workflows = manifest.get("workflows", [])
    found_workflows = {workflow.get("id"): workflow for workflow in workflows}
    if set(found_workflows) != set(EXPECTED_WORKFLOWS):
        errors.append(f"unexpected workflow IDs: {sorted(found_workflows)}")
        return
    for workflow_id, expected_stages in EXPECTED_WORKFLOWS.items():
        workflow = found_workflows[workflow_id]
        stages = workflow.get("stages", [])
        if [stage.get("id") for stage in stages] != expected_stages:
            errors.append(f"workflow {workflow_id} stages are missing or out of order")
        for stage in stages:
            if not selector_exists(stage.get("artifact_schema", "")):
                errors.append(f"workflow schema does not exist: {stage.get('artifact_schema')}")
            required_references = stage.get("required_references", [])
            if len(required_references) > stage.get("max_references", 0):
                errors.append(f"workflow stage {stage.get('id')} exceeds max_references")
            for selector in required_references:
                if not selector_exists(selector):
                    errors.append(f"workflow reference does not exist: {selector}")


def validate_artifacts(errors: list[str]) -> None:
    pairs = [
        ("assets/system-map-template.json", "schemas/system-map.schema.json"),
        ("assets/change-contract-template.json", "schemas/change-contract.schema.json"),
        ("assets/verification-receipt-template.json", "schemas/verification-receipt.schema.json"),
        ("assets/continuation-record-template.json", "schemas/continuation-record.schema.json"),
        ("examples/system-map-example.json", "schemas/system-map.schema.json"),
        ("examples/change-contract-example.json", "schemas/change-contract.schema.json"),
        ("examples/verification-receipt-example.json", "schemas/verification-receipt.schema.json"),
        ("examples/continuation-record-example.json", "schemas/continuation-record.schema.json"),
    ]
    for relative, _ in pairs:
        artifact_errors, _value = validate_file(ROOT / relative)
        for error in artifact_errors:
            errors.append(f"{relative}: {error}")

    for schema_relative in sorted({schema for _, schema in pairs}):
        schema = load_json(schema_relative)
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"{schema_relative} must use JSON Schema draft 2020-12")


def validate_test_matrices(errors: list[str]) -> None:
    routing = load_json("tests/routing-cases.json")
    if not isinstance(routing, list) or len(routing) < 20:
        errors.append("routing matrix must contain at least 20 cases")
        return
    ids = [case.get("id", "") for case in routing]
    if len(set(ids)) != len(ids) or not all(ids):
        errors.append("routing cases need unique non-empty IDs")
    available_refs = {path.stem for path in (ROOT / "references").glob("*.md")}
    for case in routing:
        required = case.get("required_references", [])
        missing = sorted(set(required).difference(available_refs))
        if missing:
            errors.append(f"routing case {case.get('id')} has unknown references: {missing}")
        if len(required) > case.get("max_references", 0):
            errors.append(f"routing case {case.get('id')} exceeds max_references")
        if case.get("max_references", 99) > 7:
            errors.append(f"routing case {case.get('id')} exceeds the seven-reference context ceiling")
        if not case.get("must_not") or not case.get("modes"):
            errors.append(f"routing case {case.get('id')} lacks modes or failure boundaries")
        routed_chars = sum(
            len((ROOT / "references" / f"{reference}.md").read_text(encoding="utf-8-sig"))
            for reference in required
            if reference in available_refs
        )
        if routed_chars > 22_000:
            errors.append(
                f"routing case {case.get('id')} exceeds the 22,000-character specialist budget"
            )

    negative = load_json("tests/negative-routing-cases.json")
    if not isinstance(negative, list) or len(negative) < 5:
        errors.append("negative routing matrix must contain at least five cases")
    for case in negative:
        if case.get("expected") != "exclude_foundry" or not case.get("reason_contains"):
            errors.append(f"invalid negative routing case: {case.get('id')}")

    evaluation = load_json("tests/evaluation-cases.json")
    cases = evaluation.get("cases", [])
    minimum = evaluation.get("coverage_requirements", {}).get("minimum_cases", 0)
    if len(cases) < 16 or len(cases) < minimum:
        errors.append("evaluation matrix must contain at least 16 cases")
    eval_ids = [case.get("id", "") for case in cases]
    if len(set(eval_ids)) != len(eval_ids) or not all(eval_ids):
        errors.append("evaluation cases need unique non-empty IDs")
    for case in cases:
        for field in ("expected_behaviour", "required_evidence", "failure_vetoes"):
            if not case.get(field):
                errors.append(f"evaluation case {case.get('id')} lacks {field}")


def validate_context_and_portability(errors: list[str]) -> None:
    compact_paths = sorted((ROOT / "references").glob("*-compact.md"))
    if len(compact_paths) != 3:
        errors.append("v1 must keep exactly three universal compact references")
    for path in compact_paths:
        if len(path.read_text(encoding="utf-8-sig")) > 6_000:
            errors.append(f"compact reference exceeds 6,000 characters: {path.name}")

    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        relative = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8-sig")
        for pattern in MACHINE_PATH_PATTERNS:
            if pattern.search(text):
                errors.append(f"machine-specific user path in distributable file: {relative.as_posix()}")
                break
        if path.suffix.lower() == ".py":
            try:
                tree = ast.parse(text)
            except SyntaxError as exc:
                errors.append(f"Python helper does not parse: {relative.as_posix()}: {exc}")
                continue
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                if (
                    isinstance(node.func, ast.Attribute)
                    and node.func.attr == "system"
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "os"
                ):
                    errors.append(f"portable helper uses os.system: {relative.as_posix()}")
                if any(
                    keyword.arg == "shell"
                    and isinstance(keyword.value, ast.Constant)
                    and keyword.value.value is True
                    for keyword in node.keywords
                ):
                    errors.append(f"portable helper uses shell=True: {relative.as_posix()}")

    forbidden_top_level = ["README.md", "ARCHITECTURE.md", "MIGRATION.md", "CHANGELOG.md"]
    for name in forbidden_top_level:
        if (ROOT / name).exists():
            errors.append(f"extraneous top-level documentation: {name}")
    for part in ("__pycache__", ".DS_Store"):
        if any(path.name == part for path in ROOT.rglob(part)):
            errors.append(f"development leftover in package: {part}")


def validate_governing_content(errors: list[str]) -> None:
    failure_text = (ROOT / "references" / "failure-tests.md").read_text(encoding="utf-8-sig")
    for phrase in (
        "wrong repository",
        "generated",
        "weakens an inconvenient failing test",
        "benchmark",
        "concurrent",
        "prompt-only authorization",
        "unit test treated as product proof",
    ):
        if phrase.casefold() not in failure_text.casefold():
            errors.append(f"failure-tests.md missing adversarial surface: {phrase}")
    bridge_text = (ROOT / "references" / "pc-bridge-integration.md").read_text(encoding="utf-8-sig")
    for phrase in ("FOUNDRY remains complete without PC Bridge", "PC Bridge owns", "permissions"):
        if phrase not in bridge_text:
            errors.append(f"PC Bridge adapter missing boundary: {phrase}")
    research_text = (ROOT / "references" / "research-basis.md").read_text(encoding="utf-8-sig")
    for source in ("SWE-bench", "RepoCoder", "NIST SP 800-218", "Google SRE", "Model Context Protocol"):
        if source not in research_text:
            errors.append(f"research basis missing: {source}")


def validate() -> list[str]:
    errors: list[str] = []
    validate_required_files(errors)
    if errors:
        return errors
    validate_skill_md(errors)
    validate_openai_yaml(errors)
    validate_version_metadata(errors)
    validate_manifest(errors)
    validate_artifacts(errors)
    validate_test_matrices(errors)
    validate_context_and_portability(errors)
    validate_governing_content(errors)
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("FOUNDRY validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALID: foundry-engineering")
    print(f"Version: {VERSION}")
    print(f"Reference modules: {len(list((ROOT / 'references').glob('*.md')))}")
    print(f"Routing cases: {len(load_json('tests/routing-cases.json'))}")
    print(f"Evaluation cases: {len(load_json('tests/evaluation-cases.json')['cases'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
