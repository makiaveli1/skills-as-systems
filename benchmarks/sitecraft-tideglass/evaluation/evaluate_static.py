#!/usr/bin/env python3
"""Run deterministic, non-visual checks against a TIDEGLASS candidate."""

from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


REQUIRED_FILES = ("index.html", "styles.css", "app.js", "README.md", "RUN-REPORT.md")
REQUIRED_COPY = (
    "TIDEGLASS",
    "EAST BREAKWATER",
    "Know the window. Leave with a plan.",
    "CAUTION",
    "SHORT WEATHER WINDOW",
    "06:40",
    "08:10",
    "WSW 17 kn",
    "24 kn",
    "1.4 m",
    "7 s",
    "+1.2 m",
    "6 nm",
    "File a shore contact",
    "Confirm fuel reserve",
    "Check VHF and lifejackets",
    "Reassess at the harbour mouth",
    "Conditions are expected to tighten after 08:10",
    "Get harbour notices",
    "fictional interface built for an Agent Skill benchmark",
)


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str | None]]] = []
        self.text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append((tag, dict(attrs)))

    def handle_data(self, data: str) -> None:
        self.text.append(data)


def contains_all(haystack: str, needles: tuple[str, ...]) -> tuple[bool, list[str]]:
    lowered = haystack.casefold()
    missing = [needle for needle in needles if needle.casefold() not in lowered]
    return not missing, missing


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    candidate = args.candidate.resolve(strict=True)

    files = {name: candidate / name for name in REQUIRED_FILES}
    missing_files = [name for name, path in files.items() if not path.is_file()]
    texts = {
        name: path.read_text(encoding="utf-8-sig") if path.is_file() else ""
        for name, path in files.items()
    }
    combined = "\n".join(texts.values())
    parsed = StructureParser()
    parsed.feed(texts["index.html"])
    visible_html = " ".join(" ".join(parsed.text).split())
    content_ok, missing_copy = contains_all(visible_html, REQUIRED_COPY)
    warning_ok = (
        "demonstration data" in combined.casefold()
        and "not for navigation" in combined.casefold()
    )
    false_transmission_phrases = re.findall(
        r"\b(?:email (?:was |has been )?sent|you(?:'re| are) subscribed|"
        r"address (?:was |has been )?(?:saved|stored)|we (?:saved|stored) your)\b",
        combined,
        re.IGNORECASE,
    )
    local_only_disclosure = bool(
        re.search(
            r"(?:not|nothing|no (?:address|data))[^.]{0,50}(?:sent|transmitted|retained|stored)",
            combined,
            re.IGNORECASE,
        )
    )
    no_false_transmission = not false_transmission_phrases and local_only_disclosure

    html = texts["index.html"]
    css = texts["styles.css"]
    js = texts["app.js"]
    report = texts["RUN-REPORT.md"]
    tags = parsed.tags

    def has_tag(name: str) -> bool:
        return any(tag == name for tag, _ in tags)

    html_attrs = next((attrs for tag, attrs in tags if tag == "html"), {})
    inputs = [attrs for tag, attrs in tags if tag == "input"]
    buttons = [attrs for tag, attrs in tags if tag == "button"]
    external_matches = re.findall(
        r"(?:href|src)\s*=\s*['\"](?:https?:)?//|@import\s+(?:url\()?['\"]?https?://",
        html + "\n" + css,
        re.IGNORECASE,
    )
    network_api = re.findall(r"\b(?:fetch|XMLHttpRequest|sendBeacon)\s*\(", js)

    static_checks: dict[str, Any] = {
        "required_files": {"passed": not missing_files, "missing": missing_files},
        "required_copy": {"passed": content_ok, "missing": missing_copy},
        "trust_warning": {"passed": warning_ok},
        "no_external_dependencies": {
            "passed": not external_matches and not network_api,
            "external_markup": external_matches,
            "network_api": network_api,
        },
        "semantic_structure": {
            "passed": has_tag("main") and has_tag("header") and has_tag("footer"),
            "main": has_tag("main"),
            "header": has_tag("header"),
            "footer": has_tag("footer"),
        },
        "document_language": {"passed": bool(html_attrs.get("lang"))},
        "viewport": {
            "passed": bool(
                re.search(
                    r"<meta[^>]+name=['\"]viewport['\"][^>]+content=['\"][^'\"]*width=device-width",
                    html,
                    re.IGNORECASE,
                )
            )
        },
        "email_input": {
            "passed": any(attrs.get("type", "").lower() == "email" for attrs in inputs)
        },
        "form_label": {
            "passed": has_tag("label")
            or any("aria-label" in attrs or "aria-labelledby" in attrs for attrs in inputs)
        },
        "time_controls": {
            "passed": sum(
                1
                for attrs in buttons
                if "aria-pressed" in attrs or "aria-selected" in attrs or "role" in attrs
            )
            >= 3,
            "button_count": len(buttons),
        },
        "live_status": {
            "passed": bool(
                re.search(r"aria-live\s*=|role\s*=\s*['\"](?:status|alert)['\"]", html, re.I)
            )
        },
        "focus_visible": {"passed": ":focus-visible" in css},
        "reduced_motion": {"passed": "prefers-reduced-motion" in css},
        "narrow_layout_rule": {
            "passed": bool(
                re.search(
                    r"@media[^\{]*(?:max-width|min-width)[^\{]*(?:320|20rem|24rem|480|30rem|32rem|40rem)",
                    css,
                    re.I,
                )
            )
        },
        "time_data": {
            "passed": all(value.casefold() in js.casefold() for value in ("07:00", "09:00", "31 kn", "1.8 m"))
        },
        "form_behavior": {
            "passed": "submit" in js.casefold()
            and any(word in js.casefold() for word in ("validity", "valid", "checkvalidity"))
            and any(word in js.casefold() for word in ("success", "complete", "demo"))
        },
        "no_false_transmission_claim": {"passed": no_false_transmission},
        "code_size": {
            "passed": len(html) + len(css) + len(js) <= 80_000,
            "bytes": len(html) + len(css) + len(js),
        },
        "report": {
            "passed": bool(report)
            and "test" in report.casefold()
            and any(word in report.casefold() for word in ("unverified", "remaining", "limitation"))
        },
    }

    scores = {
        "requirements": 15
        if all(
            static_checks[name]["passed"]
            for name in (
                "required_files",
                "required_copy",
                "trust_warning",
                "no_external_dependencies",
                "no_false_transmission_claim",
            )
        )
        else 0,
        "interaction_static": sum(
            4
            for name in ("time_controls", "time_data", "form_behavior")
            if static_checks[name]["passed"]
        ),
        "accessibility_static": sum(
            2
            for name in (
                "semantic_structure",
                "document_language",
                "viewport",
                "email_input",
                "form_label",
                "live_status",
            )
            if static_checks[name]["passed"]
        ),
        "maintainability": 8
        if static_checks["no_external_dependencies"]["passed"]
        and static_checks["code_size"]["passed"]
        else 0,
        "evidence": 8 if static_checks["report"]["passed"] else 0,
    }
    # Static evidence can award at most 55 points. Browser and independent visual review award the rest.
    score = min(scores["requirements"], 15)
    score += min(scores["interaction_static"], 12)
    score += min(scores["accessibility_static"], 12)
    score += scores["maintainability"]
    score += scores["evidence"]
    blocking_failures = [
        name
        for name in (
            "required_copy",
            "trust_warning",
            "time_controls",
            "no_false_transmission_claim",
        )
        if not static_checks[name]["passed"]
    ]
    result = {
        "candidate": candidate.name,
        "static_score": score,
        "static_maximum": 55,
        "blocking_failures": blocking_failures,
        "scores": scores,
        "checks": static_checks,
        "evidence_boundary": "Static checks do not prove layout, visual quality, keyboard behavior, or runtime interaction.",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if not blocking_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
