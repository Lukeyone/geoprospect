# Contributing to GeoProspect

## Current contribution boundary

GeoProspect is in Stage 0: feasibility audit and project bootstrap. Contributions must support the documented Stage 0 evidence plan. They must not introduce model training, prospectivity scoring, final labels, feature stores, production data acquisition, API, PostGIS, frontend or agent work before a documented GO decision.

Read these controls before changing the repository:

- `docs/stage0/STAGE0_SCOPE.md`
- `docs/stage0/STAGE1_BLOCKED.md`
- `docs/stage0/evidence_register.csv`
- `docs/stage0/REVIEW_AND_MERGE_POLICY.md`
- `docs/decisions/ADR-002-repository-and-publication-architecture.md`

## Development setup

```bash
uv sync --locked
uv run geoprospect status
```

Install the Git hook runner:

```bash
uvx --from pre-commit==4.6.0 pre-commit install
```

Run the full local control suite:

```bash
uvx --from pre-commit==4.6.0 pre-commit run --all-files
```

The CI workflow also runs Ruff formatting and linting, strict mypy checks, pytest, pre-commit and a full tracked-file secret scan.

## Change requirements

Every pull request must:

1. Link the relevant Stage 0 issue and evidence-register item.
2. State what changed and what was deliberately not changed.
3. Record the commands and results used for validation.
4. Identify any data source, licence, attribution or redistribution impact.
5. Preserve the Stage 1 block unless the final Stage 0 decision package explicitly authorises an exact passing scope.
6. Avoid credentials, restricted data and large working datasets.
7. Keep generated artefacts traceable to code, configuration and source manifests.

## Data and artefact controls

Do not commit:

- Credentials, tokens, private keys or `.env` files.
- Restricted or unapproved raw source data.
- Large working snapshots or generated geospatial products.
- Model files, prospectivity scores, ranked targets or predictive-performance claims during Stage 0.

The pre-commit large-file limit is 512 KiB. A larger file requires an explicit repository-architecture and publication decision; bypassing the hook is not approval.

## Review and merge

Routine pull requests do not wait for manual owner review. Under the repository's review policy, an AI-assisted reviewer may inspect the complete diff, verify applicable checks, correct issues and merge routine work. The owner is involved only for material scope, scientific, licensing, publication, security, cost, destructive-action or GO/SWITCH/STOP decisions.

## Licensing

No project-wide software licence has been selected yet. Do not add or change licensing terms without an explicit owner decision. Source-specific data licences and attribution requirements must be recorded independently.
