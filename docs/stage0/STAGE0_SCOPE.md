# GeoProspect Stage 0 Scope and Control Charter

**Project:** GeoProspect MVP  
**Stage:** Stage 0 — Project Bootstrap and Feasibility Gate  
**Owner:** Lachlan McDonald  
**Prepared:** 30 July 2026  
**Status:** ACTIVE — Stage 1 blocked  
**Initial candidate:** North-west Queensland copper-cobalt prospectivity, subject to the Stage 0 gate  
**Permitted decision outcomes:** GO, SWITCH or STOP

---

## 1. Authority and Purpose

This file is the repository-level source of truth for the permitted scope, decision rules and exit conditions of GeoProspect Stage 0. It operationalises the Stage 0 requirements defined in:

1. `GeoProspect MVP Project Blueprint and AI Handover`.
2. `GeoProspect Stage 0 Feasibility Audit Execution Plan`.
3. `GeoProspect Stage 0 Decomposed Execution Plan`.

Where implementation choices are uncertain, work must remain inside the boundaries in this file. Any departure must be documented through an architecture decision record or an explicit, reviewable issue decision.

Stage 0 exists to prevent GeoProspect from building a technically impressive but scientifically invalid mineral-prospectivity prototype.

### Primary decision question

> Do the selected public datasets provide enough reliable, deduplicated, spatially distributed and licensable evidence — with adequate geology, magnetics and gravity coverage — to justify moving into Stage 1 for one precisely defined commodity-region scope?

Stage 0 does **not** test whether a model can predict mineral prospectivity. It determines whether a later spatially separated, auditable experiment would be scientifically and operationally defensible.

---

## 2. Candidate Scope — Not a Commitment

The initial candidate is:

- **Commodity concept:** copper-cobalt.
- **Study-region concept:** north-west Queensland.

This candidate is provisional. It must not be treated as selected until all mandatory gates pass.

Stage 0 must compare explicit commodity definitions and candidate study boundaries. If the initial candidate fails, the project must broaden the region, change the commodity or deposit-system definition, use an alternative source combination, or issue a STOP decision. Thresholds must not be weakened merely to preserve the original idea.

Potential switch candidates identified by the governing plan include:

- Copper alone.
- Nickel-copper-PGE.
- Rare-earth elements.
- Another scientifically coherent commodity or mineral-system definition supported by public data.

---

## 3. Work Inside Stage 0

The following work is permitted:

1. Establishing Stage 0 governance, issues, evidence paths and decision controls.
2. Creating the central repository foundation, reproducible environment, contracts, tests and CI.
3. Registering current authoritative source pathways and licences.
4. Performing bounded, audit-specific data acquisition.
5. Acquiring and profiling a checksum-identified mineral-occurrence snapshot.
6. Measuring field completeness, coordinate quality, commodity values, statuses and record quality.
7. Creating explicit commodity alias mappings and candidate label definitions.
8. Performing preliminary, reversible site/deposit deduplication while retaining original records.
9. Defining and comparing multiple candidate study areas.
10. Creating provisional cells and spatial blocks solely for feasibility measurement.
11. Measuring geology, structures, magnetic and gravity coverage.
12. Measuring positive counts, spatial spread, cluster concentration and future fold feasibility.
13. Diagnosing exploration-density and survey-intensity bias.
14. Reviewing licensing, attribution and public-release pathways.
15. Producing gate results, a feasibility report, ADR-001 and a Stage 1 handover or withholding notice.
16. Issuing exactly one formal decision: GO, SWITCH or STOP.

---

## 4. Work Outside Stage 0

The following work is prohibited until a valid GO decision authorises Stage 1 or a later stage:

1. Production-grade immutable acquisition for the final selected data scope.
2. Final label production or background/unlabelled sampling.
3. Production feature engineering or feature-store construction.
4. Treating provisional cells or blocks as final stable identifiers.
5. Training logistic regression, tree models, neural networks or any other prospectivity model.
6. Computing, ranking or publishing prospectivity scores.
7. Making predictive-performance claims.
8. Building a production PostGIS database.
9. Building a FastAPI service or other operational scoring API.
10. Building a frontend application.
11. Building a research or autonomous agent.
12. Publishing trained model artefacts to `Lukeyone/geoprospect-models`.
13. Claiming that GeoProspect can discover deposits, recommend drilling or support investment decisions.
14. Lowering Stage 0 thresholds to avoid a SWITCH or STOP result.

Small audit-specific transformations, measurements and fixtures are permitted only when needed to resolve Stage 0 gates. They must not be represented as production-ready Stage 1 artefacts.

---

## 5. Mandatory Feasibility Gates

A GO decision is prohibited unless every mandatory gate passes with measured evidence.

| Gate | Mandatory pass criterion | Required failure action |
|---|---|---|
| Positive count | At least **80 deduplicated high-confidence positive sites**; **120 or more preferred** | Expand the region or switch commodity/definition |
| Spatial spread | Positives occupy at least **eight useful spatial blocks** and are not unacceptably dominated by one mine cluster | Review block design, broaden the region or switch target |
| Geology coverage | At least **95%** of candidate cells intersect a valid geology unit | Repair the layer, reduce the boundary or switch source |
| Magnetic coverage | At least **90% valid coverage** after masking | Acquire an alternate grid or constrain/switch the boundary |
| Gravity coverage | At least **90% valid coverage** after masking | Acquire an alternate grid or constrain/switch the boundary |
| Label quality | Commodity aliases, statuses and coordinates can be standardised; duplicates can be resolved sufficiently for an honest independence estimate | Create a reviewed resolution path or abandon the slice |
| Licensing | Inputs permit a compliant attribution and derived-output pathway | Restrict publication, change source or fail the candidate |
| Evaluation feasibility | Every planned held-out spatial fold contains enough positives for meaningful top-k and precision-recall evaluation | Redesign folds, broaden the scope or switch target |
| Exploration bias | Risk is not disqualifying, and any GO outcome carries explicit mitigation requirements | Switch scope or issue STOP when bias is inseparable from labels |

Passing a high occurrence-count threshold alone is insufficient. Coverage, spatial independence, evaluation feasibility, licensing and bias must also be resolved.

---

## 6. Evidence Rules

Stage 0 decisions must follow these evidence standards:

1. Use current authoritative sources rather than unverified mirrors where an official pathway exists.
2. Record publisher, endpoint, product or layer identifier, retrieval date, CRS, format, extent, licence, attribution and limitations.
3. Preserve original occurrence values and identifiers.
4. Identify acquired snapshots using a manifest and SHA-256 checksum.
5. Reconcile record counts against source counts where supported.
6. Quantify nulls, invalid coordinates, unknown commodity tokens, unresolved mappings and duplicate uncertainty.
7. Use projected distances for spatial deduplication.
8. Retain mappings from every source record to its provisional canonical site.
9. Measure coverage after masking; do not treat output pixel size as proof of effective measurement resolution.
10. Measure results by candidate area and provisional spatial block where required.
11. Treat catalogue modification dates as insufficient evidence of source freshness unless confirmed by service or source content.
12. Keep restricted raw data out of public repositories unless licence review explicitly permits redistribution.
13. Replace no mandatory measurement with an assumption.
14. Make limitations and unresolved uncertainty visible.

---

## 7. Stage Boundary by Repository

The intended repository responsibilities are:

### `Lukeyone/geoprospect`

Central code and governance repository for:

- Stage 0 scope and evidence controls.
- Audit code and configurations.
- Contracts and tests.
- Source registry.
- ADRs.
- Feasibility report and gate logic.
- Small approved figures and handover notes.

### `Lukeyone/geoprospect-data`

Public data-products repository for approved:

- Manifests.
- Data cards.
- Candidate boundaries.
- Deduplicated summary tables.
- Coverage summaries.
- Block summaries.
- Selected figures.

Raw source redistribution is prohibited unless the relevant licence review explicitly permits it.

### `Lukeyone/geoprospect-models`

During Stage 0 this repository may contain only:

- A model-card template.
- A future release policy.
- An empty-registry statement.

No trained model artefact or claimed model result may be published during Stage 0.

---

## 8. Formal Decision Outcomes

### GO

A GO decision means one exact commodity or deposit-system definition and one versioned study boundary pass every mandatory gate with manageable, documented risks.

A GO decision authorises Stage 1 only for that exact scope and the source pathways named in ADR-001 and the Stage 1 handover.

### SWITCH

A SWITCH decision means the initial candidate failed one or more gates, but another tested or clearly specified commodity, region, deposit-system definition or source combination could plausibly pass.

The project remains in Stage 0. Only affected Stage 0 work is repeated. Stage 1 remains blocked.

### STOP

A STOP decision means no tested public-data scope supports a credible supervised mineral-prospectivity experiment, or licensing/evaluation feasibility remains unacceptable.

Stage 1 for supervised GeoProspect is not authorised. A separate non-ML evidence-mapping project may be considered only through a new decision.

---

## 9. Stage 0 Completion Definition

Stage 0 is complete only when all of the following exist and are internally consistent:

- Central repository foundation and governance controls.
- Current official source and licence registry.
- Checksum-identified occurrence snapshot and quality profile.
- Explicit candidate commodity definitions and mappings.
- Reproducible provisional deduplicated-site counts.
- Comparable candidate study areas.
- Deterministic provisional cells and spatial blocks.
- Measured geology, magnetic and gravity coverage.
- Measured spatial spread and proposed fold feasibility.
- Exploration-bias classification and mitigation requirements.
- `reports/stage0/gate_results.yaml` or equivalent.
- `reports/stage0/feasibility_report.md`.
- `docs/decisions/ADR-001-commodity-region-selection.md`.
- `reports/stage0/stage1_handover.md` or explicit withholding statement.
- One explicit GO, SWITCH or STOP outcome.

Completing repository setup alone does not complete Stage 0.

Stage 0 cannot be marked complete when:

- Any mandatory gate is unresolved.
- Assumptions replace required measurements.
- Evidence paths are missing.
- A failing result is hidden by broadening labels without review.
- Thresholds are weakened.
- The final decision does not clearly authorise or withhold Stage 1.

---

## 10. Stage 1 Block

**Stage 1 is blocked by default.**

Stage 1 may begin only when all of the following are true:

1. ADR-001 records a GO decision.
2. The GO decision names one exact commodity/deposit-system definition.
3. The GO decision names one exact study-area ID and version.
4. Every mandatory gate passes using measured evidence.
5. Selected occurrence, geology, magnetic and gravity pathways are recorded.
6. Licensing and attribution support the intended public-code and derived-data strategy.
7. Known data-quality and exploration-bias limitations are carried into Stage 1 requirements.
8. The Stage 1 handover defines the raw snapshot architecture, manifest requirements and deferred questions.
9. The feasibility report and gate-results file contain no unresolved contradiction.

Until these conditions are fulfilled, any Stage 1 or later issue, pull request or implementation activity must remain marked **BLOCKED — STAGE 0 GATE**.

---

## 11. Change Control

Any proposed departure from this scope must:

1. Be recorded in a GitHub issue or ADR.
2. State the current rule being changed.
3. Explain why the change is necessary.
4. Explain its effect on scientific validity, reproducibility, licensing and the GO/SWITCH/STOP decision.
5. Preserve the original mandatory thresholds unless the project is formally re-scoped through a new governing decision.
6. Be approved before implementation.

Silently broadening labels, changing boundaries, changing block sizes or substituting sources to produce a passing result is prohibited.

---

## 12. Step 0.1 Acceptance

Phase A, Step 0.1 is complete when:

- This scope file is present in the central `Lukeyone/geoprospect` repository.
- A Stage 0 master issue links to this file and tracks the overall gate.
- A visible Stage 1-blocked notice exists.
- The initial copper-cobalt/north-west Queensland scope is clearly identified as provisional.
- The mandatory thresholds and prohibited work are explicit.

**Current control status:** Stage 1 blocked. Stage 0 decision not yet issued.
