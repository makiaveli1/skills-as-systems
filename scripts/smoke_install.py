#!/usr/bin/env python3
"""Smoke-test clean Codex and Claude Code directory installations."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install.py"
SKILLS = ("sitecraft", "foundry-engineering")


def run(*arguments: str) -> None:
    result = subprocess.run(
        [sys.executable, str(INSTALLER), *arguments],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)


def verify_install(project: Path, relative: Path) -> None:
    for name in SKILLS:
        source = ROOT / "skills" / name
        installed = project / relative / name
        if not installed.is_dir():
            raise AssertionError(f"Missing installed skill: {installed}")
        if (installed / "SKILL.md").read_bytes() != (source / "SKILL.md").read_bytes():
            raise AssertionError(f"SKILL.md differs after install: {name}")
        if (installed / "VERSION").read_bytes() != (source / "VERSION").read_bytes():
            raise AssertionError(f"VERSION differs after install: {name}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="skills-as-systems-") as temporary:
        base = Path(temporary)
        codex_project = base / "codex-project"
        claude_project = base / "claude-project"
        dry_project = base / "dry-project"
        for project in (codex_project, claude_project, dry_project):
            project.mkdir()

        run("codex", "--scope", "project", "--project", str(codex_project))
        verify_install(codex_project, Path(".agents/skills"))

        run("claude", "--scope", "project", "--project", str(claude_project))
        verify_install(claude_project, Path(".claude/skills"))

        run(
            "--host",
            "codex",
            "--scope",
            "project",
            "--project",
            str(dry_project),
            "--dry-run",
        )
        if (dry_project / ".agents").exists():
            raise AssertionError("Dry run modified the target project")

        marker = codex_project / ".agents" / "skills" / "sitecraft" / "LOCAL-MARKER"
        marker.write_text("existing user state\n", encoding="utf-8")
        run(
            "--host",
            "codex",
            "--scope",
            "project",
            "--project",
            str(codex_project),
            "--skill",
            "sitecraft",
            "--replace",
        )
        backups = sorted(marker.parent.parent.glob("sitecraft.backup.*"))
        if len(backups) != 1 or not (backups[0] / "LOCAL-MARKER").is_file():
            raise AssertionError("Replace did not retain one recoverable backup")

    print("Codex and Claude clean-install smoke tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
