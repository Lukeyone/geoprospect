"""GeoProspect Stage 0 feasibility-audit package."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("geoprospect")
except PackageNotFoundError:  # pragma: no cover - source-tree fallback
    __version__ = "0.0.0+uninstalled"

__all__ = ["__version__"]
