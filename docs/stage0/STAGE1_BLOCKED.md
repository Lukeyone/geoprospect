# BLOCKED — Stage 1 Not Authorised

**Project:** GeoProspect MVP  
**Current stage:** Stage 0 — Project Bootstrap and Feasibility Gate  
**Status:** Stage 1 blocked  
**Decision:** No GO decision has been issued

GeoProspect Stage 1, “Immutable Acquisition and Data Manifests,” is not authorised.

The initial north-west Queensland copper-cobalt concept remains a candidate only. It has not yet passed the mandatory occurrence-count, spatial-spread, geology, magnetics, gravity, label-quality, licensing, evaluation-feasibility and exploration-bias gates.

Do not begin or represent as approved:

- Production-grade immutable acquisition for a final scope.
- Final positive labels or background sampling.
- Production feature engineering or feature-store work.
- Model training or prospectivity scoring.
- API, PostGIS, frontend or agent development.
- Publication of model artefacts.

## Unblock conditions

Stage 1 may be unblocked only when:

1. `docs/decisions/ADR-001-commodity-region-selection.md` records a GO decision.
2. One exact commodity/deposit-system definition and one versioned study boundary are named.
3. Every mandatory Stage 0 gate passes with measured evidence.
4. `reports/stage0/feasibility_report.md` and `reports/stage0/gate_results.yaml` agree.
5. Licensing and attribution pathways are compliant.
6. `reports/stage0/stage1_handover.md` explicitly authorises Stage 1 for the selected scope.

Until then, later-stage issues and pull requests must carry the status:

> **BLOCKED — STAGE 0 GATE**
