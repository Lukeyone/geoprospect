"""Tests for repository security-control helpers."""

from __future__ import annotations

import json
from pathlib import Path

from geoprospect.secret_scan import main


def _write_report(path: Path, results: object) -> None:
    path.write_text(json.dumps({"results": results}), encoding="utf-8")


def test_secret_scan_verifier_accepts_empty_results(tmp_path: Path) -> None:
    report = tmp_path / "report.json"
    _write_report(report, {})

    assert main([str(report)]) == 0


def test_secret_scan_verifier_rejects_findings(tmp_path: Path) -> None:
    report = tmp_path / "report.json"
    _write_report(report, {"example.txt": [{"type": "Secret Keyword", "line_number": 4}]})

    assert main([str(report)]) == 1


def test_secret_scan_verifier_rejects_invalid_report(tmp_path: Path) -> None:
    report = tmp_path / "report.json"
    report.write_text("[]", encoding="utf-8")

    assert main([str(report)]) == 2
