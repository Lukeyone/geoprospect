# GeoProspect

GeoProspect is an independent public-data mineral-prospectivity research project.

## Current status

The project is in **Stage 0 — Project Bootstrap and Feasibility Gate**. Stage 1 and all model training, prospectivity scoring, production data acquisition, feature-store, API, PostGIS, frontend and agent work remain blocked until a documented GO decision is issued.

## Repository role

This is the **central code and governance repository**. During Stage 0 it contains:

- Stage scope, evidence controls and architecture decisions.
- Audit code, configurations, contracts and tests.
- Source registry and licence metadata.
- Gate logic and small audit-specific fixtures.
- Feasibility reports, small approved figures and handover notes.

It must not contain restricted raw data, large source datasets or trained model artefacts.

## Related repositories

- [`Lukeyone/geoprospect-data`](https://github.com/Lukeyone/geoprospect-data) — approved public data products, manifests, summaries, candidate boundaries, data cards and selected figures after licence review.
- [`Lukeyone/geoprospect-models`](https://github.com/Lukeyone/geoprospect-models) — empty model registry, model-card template and future release policy only during Stage 0.

## Stage 0 controls

- [Authoritative scope](docs/stage0/STAGE0_SCOPE.md)
- [Stage 1 blocked notice](docs/stage0/STAGE1_BLOCKED.md)
- [Evidence register](docs/stage0/evidence_register.csv)
- [Issue index](docs/stage0/STAGE0_ISSUE_INDEX.md)
- [Review and merge policy](docs/stage0/REVIEW_AND_MERGE_POLICY.md)
- [Repository architecture decision](docs/decisions/ADR-002-repository-and-publication-architecture.md)

The initial north-west Queensland copper-cobalt concept is provisional and remains subject to the Stage 0 GO/SWITCH/STOP gate.
