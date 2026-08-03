"""Contracts for versioned commodity-token mapping results."""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import Field, model_validator

from geoprospect.stage0.contracts.base import (
    Identifier,
    NonEmptyStr,
    Stage0Contract,
    validate_identifier_collection,
)


class CommodityMappingStatus(StrEnum):
    """Disposition of an observed commodity token."""

    MAPPED = "mapped"
    EXCLUDED = "excluded"
    UNRESOLVED = "unresolved"


class CommodityTokenMapping(Stage0Contract):
    """Mapping decision for one observed source-record token."""

    mapping_id: Identifier
    source_record_id: Identifier
    raw_token: NonEmptyStr
    normalised_token: NonEmptyStr
    status: CommodityMappingStatus
    canonical_commodity: str | None = None
    candidate_definition_ids: list[Identifier] = Field(default_factory=list)
    mapping_rule_id: Identifier | None = None
    rationale: NonEmptyStr
    review_required: bool = False

    @model_validator(mode="after")
    def validate_disposition(self) -> CommodityTokenMapping:
        """Require mapped, excluded and unresolved tokens to be explicit."""
        if self.status is CommodityMappingStatus.MAPPED:
            if not self.canonical_commodity or not self.mapping_rule_id:
                raise ValueError("mapped tokens require a canonical commodity and mapping rule")
        else:
            if self.canonical_commodity is not None:
                raise ValueError("excluded or unresolved tokens cannot name a canonical commodity")
            if self.candidate_definition_ids:
                raise ValueError("excluded or unresolved tokens cannot enter candidate definitions")
        if self.status is CommodityMappingStatus.UNRESOLVED and not self.review_required:
            raise ValueError("unresolved tokens must require review")
        validate_identifier_collection(
            list(self.candidate_definition_ids),
            label="candidate_definition_ids",
        )
        return self


class CommodityMappingResult(Stage0Contract):
    """Versioned batch result with reconciled mapping and unknown-token counts."""

    schema_version: Literal["1.0"] = "1.0"
    result_id: Identifier
    snapshot_id: Identifier
    mapping_version: Identifier
    mappings: list[CommodityTokenMapping]
    observed_mapping_count: int = Field(ge=0)
    mapped_count: int = Field(ge=0)
    excluded_count: int = Field(ge=0)
    unresolved_count: int = Field(ge=0)
    unknown_tokens: list[NonEmptyStr] = Field(default_factory=list)

    @model_validator(mode="after")
    def reconcile_counts(self) -> CommodityMappingResult:
        """Ensure reported counts and unknown tokens match the mapping rows."""
        mapping_ids = [mapping.mapping_id for mapping in self.mappings]
        validate_identifier_collection(mapping_ids, label="mapping IDs")
        counts = {
            status: sum(mapping.status is status for mapping in self.mappings)
            for status in CommodityMappingStatus
        }
        if self.observed_mapping_count != len(self.mappings):
            raise ValueError("observed_mapping_count must equal the number of mappings")
        if self.mapped_count != counts[CommodityMappingStatus.MAPPED]:
            raise ValueError("mapped_count does not reconcile")
        if self.excluded_count != counts[CommodityMappingStatus.EXCLUDED]:
            raise ValueError("excluded_count does not reconcile")
        if self.unresolved_count != counts[CommodityMappingStatus.UNRESOLVED]:
            raise ValueError("unresolved_count does not reconcile")
        expected_unknowns = sorted(
            mapping.raw_token
            for mapping in self.mappings
            if mapping.status is CommodityMappingStatus.UNRESOLVED
        )
        if sorted(self.unknown_tokens) != expected_unknowns:
            raise ValueError("unknown_tokens must match unresolved mapping rows")
        return self
