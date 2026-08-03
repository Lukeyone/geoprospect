"""Contracts for candidate study areas and provisional spatial layouts."""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import AwareDatetime, Field, model_validator

from geoprospect.stage0.contracts.base import (
    Coordinate2D,
    Identifier,
    NonEmptyStr,
    PolygonGeometry,
    PolygonalGeometry,
    Sha256,
    Stage0Contract,
    validate_identifier_collection,
)


class StudyAreaStatus(StrEnum):
    """Current candidate-boundary disposition."""

    CANDIDATE = "candidate"
    SELECTED = "selected"
    REJECTED = "rejected"


class CandidateStudyArea(Stage0Contract):
    """Versioned candidate boundary with explicit provenance and rationale."""

    schema_version: Literal["1.0"] = "1.0"
    study_area_id: Identifier
    version: Identifier
    name: NonEmptyStr
    commodity_definition_ids: list[Identifier]
    crs: NonEmptyStr
    geometry: PolygonalGeometry
    geometry_sha256: Sha256
    context_buffer_metres: float = Field(ge=0.0)
    boundary_source: NonEmptyStr
    rationale: NonEmptyStr
    positive_site_count: int = Field(ge=0)
    geological_coherence_notes: list[NonEmptyStr] = Field(default_factory=list)
    status: StudyAreaStatus = StudyAreaStatus.CANDIDATE
    created_at: AwareDatetime

    @model_validator(mode="after")
    def validate_definitions(self) -> CandidateStudyArea:
        """Require at least one unique commodity definition."""
        if not self.commodity_definition_ids:
            raise ValueError("candidate study areas require a commodity definition")
        validate_identifier_collection(
            list(self.commodity_definition_ids),
            label="commodity_definition_ids",
        )
        return self


class ProvisionalCell(Stage0Contract):
    """One deterministic provisional audit cell assigned to exactly one block."""

    schema_version: Literal["1.0"] = "1.0"
    cell_id: Identifier
    grid_version: Identifier
    study_area_id: Identifier
    crs: NonEmptyStr
    geometry: PolygonGeometry
    centroid: Coordinate2D
    nominal_size_metres: float = Field(gt=0.0)
    area_square_metres: float = Field(gt=0.0)
    clipped_to_boundary: bool
    block_id: Identifier
    positive_site_ids: list[Identifier] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_positive_assignments(self) -> ProvisionalCell:
        """Reject duplicate site assignments within a cell."""
        validate_identifier_collection(
            list(self.positive_site_ids),
            label="positive_site_ids",
        )
        return self


class SpatialBlock(Stage0Contract):
    """Provisional block used only for Stage 0 spread and fold feasibility."""

    schema_version: Literal["1.0"] = "1.0"
    block_id: Identifier
    block_scheme_version: Identifier
    study_area_id: Identifier
    crs: NonEmptyStr
    geometry: PolygonGeometry
    nominal_size_metres: float = Field(gt=0.0)
    area_square_metres: float = Field(gt=0.0)
    cell_ids: list[Identifier]
    positive_site_ids: list[Identifier] = Field(default_factory=list)
    fold_id: Identifier | None = None

    @model_validator(mode="after")
    def validate_members(self) -> SpatialBlock:
        """Require unique cells and positive sites."""
        if not self.cell_ids:
            raise ValueError("spatial blocks must contain at least one cell")
        validate_identifier_collection(list(self.cell_ids), label="cell_ids")
        validate_identifier_collection(
            list(self.positive_site_ids),
            label="positive_site_ids",
        )
        return self


class SpatialLayout(Stage0Contract):
    """Cross-object validation for cells, blocks and deterministic assignments."""

    schema_version: Literal["1.0"] = "1.0"
    layout_id: Identifier
    study_area_id: Identifier
    grid_version: Identifier
    block_scheme_version: Identifier
    cells: list[ProvisionalCell]
    blocks: list[SpatialBlock]

    @model_validator(mode="after")
    def reconcile_layout(self) -> SpatialLayout:
        """Require unique IDs and exactly one declared block for every cell."""
        if not self.cells or not self.blocks:
            raise ValueError("spatial layouts require cells and blocks")
        cell_ids = [cell.cell_id for cell in self.cells]
        block_ids = [block.block_id for block in self.blocks]
        validate_identifier_collection(cell_ids, label="cell IDs")
        validate_identifier_collection(block_ids, label="block IDs")
        cell_id_set = set(cell_ids)
        block_id_set = set(block_ids)
        for cell in self.cells:
            if cell.study_area_id != self.study_area_id:
                raise ValueError("all cells must belong to the layout study area")
            if cell.grid_version != self.grid_version:
                raise ValueError("all cells must use the layout grid version")
            if cell.block_id not in block_id_set:
                raise ValueError("every cell must reference a declared block")
        declared_memberships: list[str] = []
        for block in self.blocks:
            if block.study_area_id != self.study_area_id:
                raise ValueError("all blocks must belong to the layout study area")
            if block.block_scheme_version != self.block_scheme_version:
                raise ValueError("all blocks must use the layout block scheme version")
            if not set(block.cell_ids) <= cell_id_set:
                raise ValueError("blocks cannot reference undeclared cells")
            declared_memberships.extend(block.cell_ids)
        if sorted(declared_memberships) != sorted(cell_ids):
            raise ValueError("each cell must occur in exactly one block membership list")
        for cell in self.cells:
            containing_block = next(
                block for block in self.blocks if cell.cell_id in block.cell_ids
            )
            if containing_block.block_id != cell.block_id:
                raise ValueError("cell block_id must match block membership")
        return self
