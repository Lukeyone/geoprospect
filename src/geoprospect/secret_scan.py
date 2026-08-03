"""Verify detect-secrets JSON reports for CI and local controls."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def _load_report(path: Path) -> dict[str, Any]:
    """Load and minimally validate a detect-secrets JSON report."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Unable to read detect-secrets report: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("detect-secrets report must be a JSON object")
    return data


def _describe_entry(entry: object) -> str:
    """Return non-sensitive finding metadata for diagnostics."""
    if not isinstance(entry, dict):
        return "unknown finding"

    finding_type = entry.get("type", "unknown type")
    line_number = entry.get("line_number", "unknown line")
    return f"{finding_type} at line {line_number}"


def main(argv: list[str] | None = None) -> int:
    """Return non-zero when the report is invalid or contains findings."""
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) != 1:
        print("Usage: python -m geoprospect.secret_scan <report.json>", file=sys.stderr)
        return 2

    try:
        report = _load_report(Path(arguments[0]))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    results = report.get("results")
    if not isinstance(results, dict):
        print("detect-secrets report is missing a valid results object", file=sys.stderr)
        return 2

    findings = {path: entries for path, entries in results.items() if entries}
    if findings:
        print("Potential secrets detected:", file=sys.stderr)
        for path, entries in sorted(findings.items()):
            if isinstance(entries, list):
                descriptions = ", ".join(_describe_entry(entry) for entry in entries)
            else:
                descriptions = _describe_entry(entries)
            print(f"- {path}: {descriptions}", file=sys.stderr)
        return 1

    print("Secret scan passed: no findings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
