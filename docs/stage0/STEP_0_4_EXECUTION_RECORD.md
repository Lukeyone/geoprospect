# Phase B, Step 0.4 — Execution Record

**Execution date:** 30 July 2026  
**Requested action:** Bootstrap the Python project  
**Result:** COMPLETE  
**Tracking issue:** [#6 — Bootstrap the Python project](https://github.com/Lukeyone/geoprospect/issues/6)

## Implemented

- Added a Python package under `src/geoprospect/`.
- Declared Python support as `>=3.12,<3.14` and pinned the preferred interpreter to Python 3.12.
- Added `pyproject.toml` using the `uv_build` backend.
- Generated and committed `uv.lock`.
- Added the `geoprospect` console command and `python -m geoprospect` entry point.
- Added a minimal `status` command that reports the active Stage 0 control state.
- Added standard-library import and CLI tests.
- Added environment setup and validation instructions.
- Added ignore rules for virtual environments, build outputs, secrets and common geospatial working-data formats.

## Validation performed

Validation used `uv 0.10.0` with CPython 3.13.5 because Python 3.12 was not installed in the isolated validation environment. The project metadata and lockfile require Python 3.12 or 3.13, and `.python-version` pins clean project setups to 3.12.

Commands passed:

```text
UV_PYTHON=3.13 uv lock --offline
UV_PYTHON=3.13 uv sync --offline
UV_PYTHON=3.13 uv lock --check --offline
UV_PYTHON=3.13 uv sync --locked --offline
UV_PYTHON=3.13 uv run --offline python -c "import geoprospect; print(geoprospect.__version__)"
UV_PYTHON=3.13 uv run --offline geoprospect status
UV_PYTHON=3.13 uv run --offline python -m geoprospect status
UV_PYTHON=3.13 uv run --offline python -m unittest discover -s tests -v
```

Observed results:

- Package version: `0.1.0`
- CLI output: `Stage 0 active; Stage 1 blocked.`
- Tests: 2 passed
- Lockfile check: passed
- Locked sync: passed

## Acceptance result

- Python project metadata exists: **PASS**
- Python 3.12 project preference is explicit: **PASS**
- `uv.lock` exists and is current: **PASS**
- Package imports after sync: **PASS**
- Console command executes: **PASS**
- Module command executes: **PASS**
- Bootstrap tests pass: **PASS**
- Clean setup instructions exist: **PASS**
- Stage 1 remains blocked: **PASS**

## Current status

Step 0.4 is complete. The next authorised execution unit is **Phase B, Step 0.5 — Add CI, Security and Contribution Controls** ([issue #7](https://github.com/Lukeyone/geoprospect/issues/7)).
