# Phase B, Step 0.6 — Execution Record

**Execution date:** 3 August 2026  
**Requested action:** Define Stage 0 data contracts  
**Result:** COMPLETE  
**Tracking issue:** [#8 — Define Stage 0 data contracts](https://github.com/Lukeyone/geoprospect/issues/8)  
**Passing implementation workflow:** [CI run 30786155018](https://github.com/Lukeyone/geoprospect/actions/runs/30786155018)

## Implemented

- Added strict Pydantic contracts under `src/geoprospect/stage0/contracts/`.
- Covered source manifests, occurrence source records, occurrence snapshots, commodity mapping results, canonical sites, candidate study areas, provisional cells, spatial blocks, coverage summaries and gate results.
- Added `SpatialLayout` to reconcile cross-object cell and block assignments.
- Added ten small synthetic JSON fixtures under `tests/stage0/fixtures/`.
- Added contract, round-trip, generated-schema and negative boundary tests under `tests/stage0/test_contracts.py`.
- Added explicit SHA-256, retrieval-time, raw-value preservation, count-reconciliation, mapping-reconciliation, geometry, coverage and gate-decision controls.
- Added a hard rule that rejects `GO` unless every mandatory gate is present and passes.
- Added `docs/stage0/DATA_CONTRACTS.md` with the contract catalogue and change-control rules.
- Added exact-pinned Pydantic to the reproducible project lockfile.
- Corrected CI and pre-commit mypy execution so strict typing runs inside the locked project environment and can inspect project dependencies and test modules.
- Added no source acquisition, final study boundary, production identifier, model, API, PostGIS, frontend or agent work.

## Validation result

The implementation workflow completed successfully on Python 3.12 and 3.13:

- Locked dependency synchronisation: **PASS**
- All ten required representative evidence fixtures validate: **PASS**
- JSON round-trip validation and generated JSON Schema checks: **PASS**
- Invalid checksum and future-source-timestamp rejection: **PASS**
- Original-value preservation and coordinate-consistency rejection: **PASS**
- Snapshot count-reconciliation rejection: **PASS**
- Commodity count and unknown-token reconciliation: **PASS**
- Duplicate canonical-site membership rejection: **PASS**
- Self-intersecting polygon rejection: **PASS**
- Exactly-one-block-per-cell reconciliation: **PASS**
- Coverage masking, count and percentage boundary validation: **PASS**
- Numeric gate threshold-boundary validation: **PASS**
- `GO` rejection when any mandatory gate is non-passing: **PASS**
- pytest: **17 tests passed** on Python 3.12 and 3.13
- Strict mypy: **no issues in 17 source files**
- Ruff formatting and linting: **PASS**
- Pre-commit full-repository suite: **PASS**
- Secret, private-key and added-file checks: **PASS**
- Stage 1 remains blocked: **PASS**

## Current status

Step 0.6 is complete. The next authorised execution unit is **Phase C, Step 0.7 — Discover Current Authoritative Sources** ([issue #9](https://github.com/Lukeyone/geoprospect/issues/9)).
