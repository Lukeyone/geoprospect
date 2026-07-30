# Stage 0 Master Feasibility Audit and GO/SWITCH/STOP Gate

This file preserves the canonical issue body used for the live Stage 0 master tracking issue.

## Purpose

Control the complete GeoProspect Stage 0 feasibility audit and prevent Stage 1 or later work from beginning before a documented GO decision.

The initial candidate is **north-west Queensland copper-cobalt prospectivity**, but it is not a commitment. It must pass the mandatory count, spatial, coverage, label-quality, licensing, evaluation and bias gates. Thresholds must not be weakened to preserve the initial idea.

Authoritative scope: `docs/stage0/STAGE0_SCOPE.md`  
Stage 1 block: `docs/stage0/STAGE1_BLOCKED.md`

## Primary decision question

Do the selected public datasets provide enough reliable, deduplicated, spatially distributed and licensable evidence — with adequate geology, magnetics and gravity coverage — to justify Stage 1 for one precise commodity-region scope?

## Stage status

- [x] Stage 0 active
- [x] Stage 1 blocked
- [ ] Formal decision issued: GO / SWITCH / STOP
- [ ] ADR-001 complete
- [ ] Feasibility report complete
- [ ] Gate-results file complete
- [ ] Stage 1 handover or withholding statement complete

## Phase checklist

### Phase A — Stage control

- [x] Step 0.1 — Confirm Stage 0 scope
- [ ] Step 0.2 — Create the evidence register
- [ ] Step 0.3 — Confirm repository architecture

### Phase B — Repository and reproducibility foundation

- [ ] Step 0.4 — Bootstrap the Python project
- [ ] Step 0.5 — Add CI, security and contribution controls
- [ ] Step 0.6 — Define Stage 0 data contracts

### Phase C — Source and licence validation

- [ ] Step 0.7 — Discover current authoritative sources
- [ ] Step 0.8 — Validate licensing and attribution

### Phase D — Occurrence evidence

- [ ] Step 0.9 — Design occurrence acquisition
- [ ] Step 0.10 — Acquire and identify the occurrence snapshot
- [ ] Step 0.11 — Profile occurrence quality

### Phase E — Commodity and site independence

- [ ] Step 0.12 — Build the commodity alias registry
- [ ] Step 0.13 — Compare candidate commodity definitions
- [ ] Step 0.14 — Design provisional deduplication rules
- [ ] Step 0.15 — Run provisional deduplication

### Phase F — Region and spatial evaluation design

- [ ] Step 0.16 — Define candidate study areas
- [ ] Step 0.17 — Create provisional cells and spatial blocks

### Phase G — Coverage audit

- [ ] Step 0.18 — Audit geology and structures coverage
- [ ] Step 0.19 — Audit magnetics and gravity coverage

### Phase H — Spatial feasibility and bias

- [ ] Step 0.20 — Evaluate spatial spread and fold feasibility
- [ ] Step 0.21 — Assess exploration-bias risk

### Phase I — Candidate comparison and decision

- [ ] Step 0.22 — Build the candidate comparison matrix
- [ ] Step 0.23 — Evaluate the formal gate
- [ ] Step 0.24 — Write the feasibility report
- [ ] Step 0.25 — Record ADR-001 and final decision
- [ ] Step 0.26 — Produce the Stage 1 handover or withhold authorisation

## Mandatory gate checklist

- [ ] At least 80 deduplicated high-confidence positive sites; 120+ preferred
- [ ] Positives occupy at least eight useful spatial blocks
- [ ] No unacceptable single-mine-cluster dominance
- [ ] At least 95% valid geology coverage
- [ ] At least 90% valid magnetic coverage after masking
- [ ] At least 90% valid gravity coverage after masking
- [ ] Commodity aliases, statuses and coordinates can be standardised
- [ ] Duplicate risk can be resolved sufficiently for an honest independence estimate
- [ ] Public inputs have a compliant licence and attribution pathway
- [ ] Every proposed held-out fold supports meaningful top-k and precision-recall evaluation
- [ ] Exploration bias is manageable or severe-but-testable with binding mitigation requirements

## Prohibited before GO

- Model training or prospectivity scoring
- Final feature-store construction
- Final labels or background sampling
- Production PostGIS or API work
- Frontend or agent development
- Model publication
- Claims that GeoProspect can discover deposits or recommend drilling
- Threshold reductions intended to avoid SWITCH or STOP

## Evidence links

These paths will be populated and tracked through Step 0.2:

- `docs/stage0/evidence_register.csv`
- `configs/sources/`
- `configs/commodities/`
- `configs/study_areas/`
- `reports/stage0/gate_results.yaml`
- `reports/stage0/feasibility_report.md`
- `docs/decisions/ADR-001-commodity-region-selection.md`
- `reports/stage0/stage1_handover.md`

## Exit condition

Close the live master issue only when every mandatory gate is resolved and the feasibility report, gate-results file, ADR-001 and handover are mutually consistent.

The final issue comment must contain exactly one outcome:

- **GO** — Stage 1 authorised for one exact passing scope.
- **SWITCH** — Stage 1 remains blocked; named Stage 0 steps repeat for a new candidate.
- **STOP** — Supervised GeoProspect Stage 1 is not authorised.
