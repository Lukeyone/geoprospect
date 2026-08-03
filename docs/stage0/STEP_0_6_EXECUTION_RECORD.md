# Phase B, Step 0.6 — Execution Record

**Execution date:** 3 August 2026  
**Requested action:** Define Stage 0 data contracts  
**Result:** PENDING CI  
**Tracking issue:** [#8 — Define Stage 0 data contracts](https://github.com/Lukeyone/geoprospect/issues/8)

## Implemented

- Added strict Pydantic contracts under `src/geoprospect/stage0/contracts/`.
- Covered source manifests, occurrence source records, occurrence snapshots, commodity mapping results, canonical sites, candidate study areas, provisional cells, spatial blocks, coverage summaries and gate results.
- Added `SpatialLayout` to reconcile cross-object cell and block assignments.
- Added ten small synthetic JSON fixtures under `tests/stage0/fixtures/`.
- Added contract, round-trip, schema and negative boundary tests under `tests/stage0/test_contracts.py`.
- Added explicit SHA-256, retrieval-time, raw-value preservation, count-reconciliation, mapping-reconciliation, geometry, coverage and gate-decision controls.
- Added a hard rule that rejects `GO` unless every mandatory gate is present and passes.
- Added `docs/stage0/DATA_CONTRACTS.md` with the contract catalogue and change-control rules.
- Added exact-pinned Pydantic to the reproducible project lockfile.
- Added no source acquisition, final study boundary, production identifier, model, API, PostGIS, frontend or agent work.

## Required validation

Step 0.6 remains incomplete until the pull-request workflow confirms:

- locked dependency synchronisation: pending;
- Ruff formatting and linting: pending;
- strict mypy on Python 3.12 and 3.13: pending;
- pytest on Python 3.12 and 3.13: pending;
- pre-commit full-repository suite: pending;
- secret, private-key and added-file checks: pending;
- every required evidence fixture validates: pending;
- invalid boundary cases are rejected: pending;
- Stage 1 remains blocked: confirmed by scope review.

## Current status

Evidence item E007 remains `planned` until the exact final branch head passes all configured checks and the reviewed pull request is merged.
