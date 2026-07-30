# ADR-002: Repository and Publication Architecture

- **Status:** Accepted
- **Date:** 30 July 2026
- **Decision owner:** GeoProspect Stage 0 governance
- **Tracking issue:** [#5 — Confirm repository architecture](https://github.com/Lukeyone/geoprospect/issues/5)
- **Stage:** Stage 0 — Project Bootstrap and Feasibility Gate

## Context

GeoProspect uses three public repositories. Without explicit boundaries, audit code, restricted raw data, derived public products and future model artefacts could be mixed together, creating reproducibility, licensing and scientific-governance risks.

The Stage 0 execution plan requires:

1. `Lukeyone/geoprospect` for audit code, configurations, contracts, tests, ADRs, source registry, gate logic, feasibility reporting, small approved figures and handover notes.
2. `Lukeyone/geoprospect-data` for approved manifests, data cards, candidate boundaries, deduplicated summary tables, coverage summaries, block summaries and selected figures.
3. `Lukeyone/geoprospect-models` to remain an empty registry containing only a model-card template, future release policy and empty-registry statement during Stage 0.

Raw source redistribution is permitted only after licence review. Stage 0 does not authorise trained model artefacts.

## Decision

### 1. Central repository — `Lukeyone/geoprospect`

This repository is authoritative for implementation and governance.

It owns:

- Stage scope, issue controls and evidence register.
- Source registry and licence metadata.
- Audit code, CLI, configurations, contracts and tests.
- Reproducible data-acquisition and measurement logic.
- ADRs and decision records.
- Gate results, feasibility report and Stage 1 handover.
- Small fixtures and small approved figures required to test or explain the audit.

It does not own:

- Restricted or unnecessarily duplicated raw source files.
- Large working snapshots that can be identified through manifests and checksums elsewhere.
- Public model artefacts.
- Production API, PostGIS, frontend or agent implementations during Stage 0.

### 2. Public data-products repository — `Lukeyone/geoprospect-data`

This repository is a publication surface, not the primary working-data store.

It may contain only artefacts that have passed provenance and licence review, including:

- Source and snapshot manifests.
- Data cards and attribution statements.
- Versioned candidate boundaries.
- Deduplicated summary tables.
- Coverage and spatial-block summaries.
- Selected explanatory figures.

Raw data may be published only when ADR-003 or a later source-specific licence decision explicitly records redistribution permission. Otherwise the repository contains code-independent manifests and derived summaries only.

### 3. Model registry — `Lukeyone/geoprospect-models`

During Stage 0, this repository must remain an empty model registry.

Permitted contents are limited to:

- `README.md`.
- `EMPTY_REGISTRY.md`.
- `MODEL_CARD_TEMPLATE.md`.
- `RELEASE_POLICY.md`.

The following are prohibited during Stage 0:

- Model weights, checkpoints or serialized estimators.
- Prospectivity scores, rasters or ranked targets.
- Model benchmarks or predictive-performance claims.
- Feature stores, embeddings or deployment artefacts.

### 4. Cross-repository publication contract

Every public data or future model artefact must be traceable to:

- A central-repository issue or decision.
- A source or model manifest.
- A versioned generating method or commit.
- Required licence and attribution information.
- Known limitations and restrictions.

A satellite repository must not become the authoritative location for code, gate logic or decisions.

## Responsibility matrix

| Artefact | `geoprospect` | `geoprospect-data` | `geoprospect-models` |
|---|---|---|---|
| Scope, ADRs and evidence register | Authoritative | Prohibited | Prohibited |
| Audit code, configs, tests and contracts | Authoritative | Prohibited | Prohibited |
| Source registry and licence metadata | Authoritative | May mirror approved attribution summaries | Prohibited |
| Raw audit snapshots | External/approved working location referenced by manifest; public copy only if licensed | Only if explicit redistribution approval exists | Prohibited |
| Candidate boundaries and derived summaries | Generates and validates | Approved publication location | Prohibited |
| Coverage tables and selected figures | Generates; small copies may remain for the report | Approved publication location | Prohibited |
| Model-card template and release policy | May reference | Prohibited | Authoritative |
| Trained models and scores during Stage 0 | Prohibited | Prohibited | Prohibited |
| Future authorised model artefacts | Governs and links | May host associated approved data cards | Publication location after later-stage approval |

## Consequences

### Positive

- Licensing and redistribution decisions are separated from implementation.
- Raw-data duplication is reduced.
- Model publication cannot be mistaken for Stage 0 completion.
- Public artefacts remain traceable to code, evidence and decisions.
- Each repository has one unambiguous purpose.

### Costs and constraints

- Publishing an artefact may require coordinated updates across repositories.
- Manifests and provenance links must be maintained.
- Large audit snapshots require an approved external or local working location until a later storage decision is made.
- Satellite repositories remain intentionally sparse during early Stage 0.

## Rejected alternatives

### Single monorepository for all code, data and models

Rejected because public raw-data licensing, large-file handling and future model-release governance require different controls.

### Put working raw data in `geoprospect-data` by default

Rejected because repository naming does not establish redistribution rights, and Git is not the default working store for large source snapshots.

### Publish experimental models during Stage 0 for portfolio visibility

Rejected because Stage 0 determines whether a defensible modelling experiment is possible; publishing models or scores would misrepresent the stage and bypass the GO gate.

## Change control

Changes to repository responsibilities require an ADR amendment or replacement. No change may weaken the Stage 1 block, bypass licence review or permit trained model artefacts during Stage 0.
