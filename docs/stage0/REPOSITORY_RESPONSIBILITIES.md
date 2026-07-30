# GeoProspect Repository Responsibility Statement

**Status:** Active  
**Decision:** [ADR-002](../decisions/ADR-002-repository-and-publication-architecture.md)

## Repository map

| Repository | Primary role | Stage 0 publication boundary |
|---|---|---|
| `Lukeyone/geoprospect` | Code, governance and evidence generation | Audit code, configs, tests, contracts, source registry, ADRs, reports, gate logic and small approved fixtures/figures |
| `Lukeyone/geoprospect-data` | Approved public data products | Manifests, data cards, candidate boundaries, derived summaries, coverage/block tables and selected figures after licence review |
| `Lukeyone/geoprospect-models` | Future model registry | Empty-registry statement, model-card template and release policy only |

## Non-negotiable Stage 0 boundaries

- Restricted raw data is not committed to public repositories.
- Raw redistribution requires explicit licence approval.
- Large working snapshots are referenced through manifests and checksums rather than committed by default.
- Audit code and decision logic remain authoritative in `geoprospect`.
- No trained model, score, ranked target or predictive-performance claim is published during Stage 0.
- Stage 1 remains blocked until an exact passing scope receives a documented GO.
