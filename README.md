# GeoProspect

GeoProspect is an independent public-data mineral-prospectivity research project.

## Current status

The project is in **Stage 0 — Project Bootstrap and Feasibility Gate**. Stage 1 and all model training, prospectivity scoring, production data acquisition, feature-store, API, PostGIS, frontend and agent work remain blocked until a documented GO decision is issued.

## Python quickstart

Requirements: Git, `uv` and Python 3.12.

```bash
git clone https://github.com/Lukeyone/geoprospect.git
cd geoprospect
uv sync --locked
uv run geoprospect status
uv run python -m unittest discover -s tests -v
```

Expected status:

```text
Stage 0 active; Stage 1 blocked.
```

See [Stage 0 environment setup](docs/stage0/ENVIRONMENT_SETUP.md) for the full validation commands.

## Quality and security checks

Install and run the pinned pre-commit suite:

```bash
uvx --from pre-commit==4.6.0 pre-commit install
uvx --from pre-commit==4.6.0 pre-commit run --all-files
```

GitHub Actions repeats the controls on Python 3.12 and 3.13. The automated suite includes Ruff formatting and linting, strict mypy checks, pytest, secret detection, private-key detection and a 512 KiB added-file limit.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md) before submitting or publishing changes.

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
- [Stage 0 data contracts](docs/stage0/DATA_CONTRACTS.md)
- [Current authoritative source discovery](docs/stage0/SOURCE_DISCOVERY.md)
- [Source endpoint validation results](reports/stage0/source_endpoint_validation.json)
- [Repository architecture decision](docs/decisions/ADR-002-repository-and-publication-architecture.md)
- [Repository responsibility statement](docs/stage0/REPOSITORY_RESPONSIBILITIES.md)

The initial north-west Queensland copper-cobalt concept is provisional and remains subject to the Stage 0 GO/SWITCH/STOP gate.
