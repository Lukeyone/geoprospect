"""Contracts for reconciled geology and geophysics coverage summaries."""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import AwareDatetime, Field, model_validator

from geoprospect.stage0.contracts.base import (
    Identifier,
    NonEmptyStr,
    Percentage,
    Stage0Contract,
)
from geoprospect.stage0.contracts.sources import SourceClass


class CoverageUnit(StrEnum):
    """Counting unit used in a coverage calculation."""

    CELL = "cell"
    PIXEL = "pixel"
    FEATURE = "feature"


class CoverageSummary(Stage0Contract):
    """Masked and count-reconciled coverage evidence for an area or block."""

    schema_version: Literal["1.0"] = "1.0"
    coverage_id: Identifier
    source_id: Identifier
    study_area_id: Identifier
    block_id: Identifier | None = None
    layer_class: SourceClass
    calculation_version: Identifier
    unit: CoverageUnit
    total_units: int = Field(gt=0)
    valid_units: int = Field(ge=0)
    nodata_units: int = Field(ge=0)
    excluded_units: int = Field(ge=0)
    valid_percent: Percentage
    nodata_percent: Percentage
    excluded_percent: Percentage
    mask_applied: bool
    source_resolution_metres: float | None = Field(default=None, gt=0.0)
    effective_resolution_notes: list[NonEmptyStr] = Field(default_factory=list)
    reprojection: NonEmptyStr
    resampling: NonEmptyStr
    calculated_at: AwareDatetime

    @model_validator(mode="after")
    def reconcile_coverage(self) -> CoverageSummary:
        """Require explicit masks and consistent counts and percentages."""
        permitted = {
            SourceClass.GEOLOGY,
            SourceClass.STRUCTURES,
            SourceClass.MAGNETICS,
            SourceClass.GRAVITY,
        }
        if self.layer_class not in permitted:
            raise ValueError("coverage summaries require a geology or geophysics layer")
        if not self.mask_applied:
            raise ValueError("coverage summaries must explicitly apply the source mask")
        if self.valid_units + self.nodata_units + self.excluded_units != self.total_units:
            raise ValueError("coverage counts must reconcile to total_units")
        expected = {
            "valid_percent": 100.0 * self.valid_units / self.total_units,
            "nodata_percent": 100.0 * self.nodata_units / self.total_units,
            "excluded_percent": 100.0 * self.excluded_units / self.total_units,
        }
        for field_name, expected_value in expected.items():
            observed = getattr(self, field_name)
            if abs(observed - expected_value) > 0.01:
                raise ValueError(f"{field_name} does not reconcile with coverage counts")
        return self
