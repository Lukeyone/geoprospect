# Phase B, Step 0.5 — Execution Record

**Execution date:** 3 August 2026  
**Requested action:** Add CI, security and contribution controls  
**Result:** PENDING CI  
**Tracking issue:** [#7 — Add CI, security and contribution controls](https://github.com/Lukeyone/geoprospect/issues/7)

## Implemented

- Added a GitHub Actions workflow for Python 3.12 and 3.13.
- Added locked-environment synchronisation before quality checks.
- Added pinned Ruff formatting and linting.
- Added strict mypy checking.
- Added pytest execution.
- Added a pinned pre-commit configuration.
- Added full tracked-file secret scanning and a JSON report verifier.
- Added private-key and 512 KiB added-file safeguards.
- Added `SECURITY.md`, `CONTRIBUTING.md`, `CITATION.cff` and a pull-request template.
- Added weekly Dependabot checks for GitHub Actions.
- Preserved the AI-assisted routine review policy; no manual owner approval is required for routine changes.
- Did not select a project-wide software licence.

## Required validation

The step remains incomplete until the pull-request workflow confirms:

- Ruff format: pending
- Ruff lint: pending
- mypy on Python 3.12 and 3.13: pending
- pytest on Python 3.12 and 3.13: pending
- pre-commit: pending
- secret scan: pending
- no unapproved large files: pending
- Stage 1 remains blocked: confirmed by scope review

## Current status

Step 0.5 is in progress. Evidence item E006 remains `in_progress` until all configured checks pass and the reviewed pull request is merged.
