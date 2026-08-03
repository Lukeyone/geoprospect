"""Fail CI when a detect-secrets JSON report contains findings."""

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


def main(argv: list[str] | None = None) -> int:
    """Return non-zero when the report is invalid or contains findings."""
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) != 1:
        print("Usage: verify_secret_scan.py <detect-secrets-report.json>", file=sys.stderr)
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
            count = len(entries) if isinstance(entries, list) else 1
            print(f"- {path}: {count} finding(s)", file=sys.stderr)
        return 1

    print("Secret scan passed: no findings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
