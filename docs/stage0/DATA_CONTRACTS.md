# GeoProspect Stage 0 Data Contracts

**Status:** Active Stage 0 foundation  
**Tracking issue:** [#8 — Define Stage 0 data contracts](https://github.com/Lukeyone/geoprospect/issues/8)  
**Stage 1:** BLOCKED

## Purpose

These Pydantic contracts define the minimum validated structures that later Stage 0 evidence must follow. They protect the feasibility audit from silent schema drift, irreproducible identifiers, contradictory counts, invalid provisional geometry, unmasked coverage claims and gate decisions that conflict with measured thresholds.

They are audit contracts, not final production schemas. Provisional cells, blocks, sites and candidate areas remain Stage 0 evidence only.

## Contract catalogue

| Required evidence type | Primary model | Module | Representative fixture or evidence |
|---|---|---|---|
| Source discovery entry | `SourceRegistryEntry` | `sources.py` | `configs/sources/*.yaml` |
| Complete mandatory source registry | `SourceRegistry` | `sources.py` | `tests/stage0/test_source_registry.py` |
| Retrieved source manifest | `SourceManifest` | `sources.py` | `source_manifest.json` |
| Occurrence source record | `OccurrenceSourceRecord` | `occurrences.py` | `occurrence_record.json` |
| Occurrence snapshot | `OccurrenceSnapshot` | `occurrences.py` | `occurrence_snapshot.json` |
| Commodity mapping result | `CommodityMappingResult` | `commodities.py` | `commodity_mapping.json` |
| Canonical site | `CanonicalSite` | `sites.py` | `canonical_site.json` |
| Candidate study area | `CandidateStudyArea` | `regions.py` | `candidate_study_area.json` |
| Provisional cell | `ProvisionalCell` | `regions.py` | `provisional_cell.json` |
| Spatial block | `SpatialBlock` | `regions.py` | `spatial_block.json` |
| Coverage summary | `CoverageSummary` | `coverage.py` | `coverage_summary.json` |
| Gate results | `GateResultSet` | `gates.py` | `gate_results.json` |

`SpatialLayout` provides an additional aggregate contract that reconciles cell, block and positive-site assignments. `SourceRegistry` requires one unique plausible pathway for each mandatory source class.

## Binding validation rules

All contracts:

- use schema version `1.0`;
- reject undeclared fields rather than silently ignoring them;
- strip surrounding string whitespace and validate assignments;
- require non-empty identifiers and evidence fields;
- expose generated JSON Schema through Pydantic;
- remain serialisable for manifest, JSON, YAML or tabular adapter layers.

Evidence-specific rules include:

- source-discovery entries require publisher, official page, underlying endpoint, product or layer identifier, format, CRS, extent, update metadata, relevant fields or bands, endpoint evidence and visible limitations;
- plausible discovery entries cannot contain failed endpoint validation and must leave final licence classification pending Step 0.8;
- the aggregate source registry requires exactly one plausible pathway for mineral occurrences, geology, structures, magnetics and gravity;
- retrieved source manifests require publisher, access pathway, CRS, licence metadata, retrieval time and SHA-256 identity;
- occurrence records preserve original values and cannot carry contradictory point coordinates;
- snapshots reconcile acquired and source-reported counts where source counts exist;
- commodity summaries reconcile mapped, excluded and unresolved token rows;
- canonical sites retain unique source-record memberships and a traceable representative record;
- polygon rings must be closed, non-degenerate and non-self-intersecting;
- provisional layouts enforce deterministic cell, block and positive-site membership;
- coverage counts must reconcile, percentages remain between 0 and 100, and masking is mandatory;
- numeric gate status must agree with the threshold comparison;
- resolved qualitative gates require measured evidence;
- a formal `GO` is rejected unless every mandatory gate is present and passes.

## Fixtures and tests

The files under `tests/stage0/fixtures/` are small synthetic examples. They are not authoritative sources, measured project results, selected study areas or evidence of a GO decision.

The source-registry files under `configs/sources/` are evidence records rather than data snapshots. They use JSON syntax, which is valid YAML 1.2, and are validated without an additional parser dependency.

The test suite validates representative fixtures, source entries, JSON round trips and generated schemas. Negative tests cover schema drift, invalid checksums, future source timestamps, lost original values, inconsistent coordinates, count mismatches, unresolved mapping reconciliation, duplicate memberships, self-intersecting polygons, duplicate block assignments, unreconciled positive-site assignments, unmasked or inconsistent coverage, missing mandatory sources, failed source endpoints, omitted source limitations and threshold or decision contradictions.

Run the complete repository suite with:

```bash
uv sync --locked
uvx --from pre-commit==4.6.0 pre-commit run --all-files
```

## Change control

A backward-incompatible contract change requires:

1. a schema-version change;
2. updated representative fixtures or registry evidence;
3. migration or compatibility notes for existing Stage 0 evidence;
4. updated tests and evidence-register paths;
5. review of any effect on scientific validity, reproducibility, licensing and the GO/SWITCH/STOP gate.

Contract validation does not itself establish source authority, data quality, coverage, label independence, licence compliance or feasibility. Those questions remain assigned to their named Stage 0 steps. Stage 1 remains blocked until the complete formal gate produces a documented GO for one exact scope.
