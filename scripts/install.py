#!/usr/bin/env python3
"""Install canonical skills into Codex, Claude Code, or a custom skill root."""

from __future__ import annotations

import argparse
import shutil
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
KNOWN_SKILLS = (
    "sitecraft",
    "foundry-engineering",
)


class InstallError(RuntimeError):
    pass


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install Skills as Systems without editing host settings or permissions."
    )
    parser.add_argument(
        "quick_host",
        nargs="?",
        choices=("codex", "claude"),
        help="Quick install at user scope: install.py codex|claude",
    )
    parser.add_argument("--host", choices=("codex", "claude"))
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument(
        "--project",
        type=Path,
        help="Existing project root. Required when --scope project is used.",
    )
    parser.add_argument(
        "--target",
        type=Path,
        help="Explicit skill root. When supplied, --host and --scope only label the plan.",
    )
    parser.add_argument(
        "--skill",
        action="append",
        choices=KNOWN_SKILLS,
        dest="skills",
        help="Skill to install. Repeat for several; omit to install all.",
    )
    parser.add_argument("--mode", choices=("copy", "symlink"), default="copy")
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Move an existing skill to a timestamped backup before installing.",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    if args.quick_host is not None and args.host is not None and args.quick_host != args.host:
        parser.error("The positional host and --host must match when both are supplied.")
    if args.host is None:
        args.host = args.quick_host
    return args


def resolve_target(args: argparse.Namespace) -> Path:
    if args.target is not None:
        target = args.target.expanduser().resolve(strict=False)
    else:
        if args.host is None:
            raise InstallError("Choose --host codex|claude or supply --target.")
        if args.scope == "user":
            relative = Path(".agents/skills") if args.host == "codex" else Path(".claude/skills")
            target = (Path.home() / relative).resolve(strict=False)
        else:
            if args.project is None:
                raise InstallError("--scope project requires --project /path/to/existing/project.")
            project = args.project.expanduser().resolve(strict=True)
            if not project.is_dir():
                raise InstallError(f"Project is not a directory: {project}")
            relative = Path(".agents/skills") if args.host == "codex" else Path(".claude/skills")
            target = (project / relative).resolve(strict=False)

    if target == Path(target.anchor) or target == Path.home().resolve():
        raise InstallError(f"Refusing unsafe skill root: {target}")

    skills_root = SKILLS_ROOT.resolve()
    try:
        target.relative_to(skills_root)
    except ValueError:
        pass
    else:
        raise InstallError("Target must not be inside the canonical source packages.")
    return target


def read_frontmatter_name(skill_root: Path) -> str:
    path = skill_root / "SKILL.md"
    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise InstallError(f"Cannot read {path}: {exc}") from exc
    if not text.startswith("---\n"):
        raise InstallError(f"Missing YAML frontmatter: {path}")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise InstallError(f"Unclosed YAML frontmatter: {path}")
    for line in text[4:end].splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip('"\'')
    raise InstallError(f"Missing skill name: {path}")


def unique_backup_path(destination: Path, stamp: str) -> Path:
    candidate = destination.with_name(f"{destination.name}.backup.{stamp}")
    counter = 1
    while candidate.exists() or candidate.is_symlink():
        candidate = destination.with_name(f"{destination.name}.backup.{stamp}.{counter}")
        counter += 1
    return candidate


def stage_skill(source: Path, stage: Path, mode: str) -> None:
    if mode == "copy":
        shutil.copytree(source, stage, symlinks=True)
    else:
        stage.symlink_to(source, target_is_directory=True)


def remove_stage(stage: Path) -> None:
    if stage.is_symlink() or stage.is_file():
        stage.unlink(missing_ok=True)
    elif stage.is_dir():
        shutil.rmtree(stage)


def install_one(
    source: Path,
    destination: Path,
    *,
    mode: str,
    replace: bool,
    dry_run: bool,
    stamp: str,
) -> Path | None:
    exists = destination.exists() or destination.is_symlink()
    if exists and not replace:
        raise InstallError(
            f"Target already exists: {destination}. Re-run with --replace to retain a backup."
        )

    backup = unique_backup_path(destination, stamp) if exists else None
    if dry_run:
        action = f"replace (backup: {backup})" if backup else "install"
        print(f"DRY RUN: {action} {source.name} -> {destination} [{mode}]")
        return backup

    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = destination.parent / f".{destination.name}.install-{uuid.uuid4().hex}"
    try:
        stage_skill(source, stage, mode)
        if backup is not None:
            destination.rename(backup)
        try:
            stage.rename(destination)
        except Exception:
            if backup is not None and not destination.exists() and not destination.is_symlink():
                backup.rename(destination)
            raise
    finally:
        if stage.exists() or stage.is_symlink():
            remove_stage(stage)

    if backup is None:
        print(f"Installed {source.name} -> {destination} [{mode}]")
    else:
        print(f"Installed {source.name} -> {destination} [{mode}]; backup: {backup}")
    return backup


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        target_root = resolve_target(args)
        selected = tuple(dict.fromkeys(args.skills or KNOWN_SKILLS))
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        print(f"Skill root: {target_root}")
        for name in selected:
            source = SKILLS_ROOT / name
            if not source.is_dir():
                raise InstallError(f"Missing canonical skill: {source}")
            if read_frontmatter_name(source) != name:
                raise InstallError(f"Directory/frontmatter name mismatch: {source}")
            install_one(
                source,
                target_root / name,
                mode=args.mode,
                replace=args.replace,
                dry_run=args.dry_run,
                stamp=stamp,
            )
    except (InstallError, OSError) as exc:
        print(f"Install failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
