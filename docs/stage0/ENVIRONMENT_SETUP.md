# GeoProspect Stage 0 Environment Setup

## Requirements

- Git
- `uv`
- Python 3.12

The repository pins Python in `.python-version` and records the resolved project state in `uv.lock`.

## Clean setup

```bash
git clone https://github.com/Lukeyone/geoprospect.git
cd geoprospect
uv sync --locked
```

## Verify the bootstrap

```bash
uv run python -c "import geoprospect; print(geoprospect.__version__)"
uv run geoprospect status
uv run python -m geoprospect status
uv run python -m unittest discover -s tests -v
```

Expected status output:

```text
Stage 0 active; Stage 1 blocked.
```

## Dependency changes

Use `uv add`, `uv remove` or an intentional `pyproject.toml` edit, then regenerate `uv.lock`. Do not hand-edit the lockfile.

Stage 0 remains limited to feasibility-audit tooling. Environment setup does not authorise data acquisition, modelling, API, PostGIS, frontend or agent work.
