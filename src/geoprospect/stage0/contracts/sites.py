"""Contracts for reversible provisional canonical-site grouping."""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import Field, model_validator

from geoprospect.stage0.contracts.base import (
    Identifier,
    NonEmptyStr,
    PointGeometry,
    Stage0Contract,
    validate_identifier_collection,
)


class DeduplicationMethod(StrEnum):
    """Evidence used to group a source record into a provisional site."""

    AUTHORITATIVE_ID = "authoritative_id"
    PARENT_CHILD = "parent_child"
    NORMALISED_NAME = "normalised_name"
    PROJECTED_DISTANCE = "projected_distance"
    MANUAL = "manual"


class MatchConfidence(StrEnum):
    """Confidence in one source-record membership decision."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class CanonicalSiteMember(Stage0Contract):
    """Traceable membership of one preserved occurrence record."""

    source_record_id: Identifier
    snapshot_id: Identifier
    match_methods: set[DeduplicationMethod]
    distance_metres: float | None = Field(default=None, ge=0.0)
    confidence: MatchConfidence
    conflict_flags: list[NonEmptyStr] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_distance_evidence(self) -> CanonicalSiteMember:
        """Require projected-distance evidence only when that method is used."""
        uses_distance = DeduplicationMethod.PROJECTED_DISTANCE in self.match_methods
        if uses_distance and self.distance_metres is None:
            raise ValueError("projected-distance matches require distance_metres")
        if not uses_distance and self.distance_metres is not None:
            raise ValueError("distance_metres is only valid for projected-distance matches")
        if not self.match_methods:
            raise ValueError("each canonical-site member requires at least one match method")
        return self


class CanonicalSite(Stage0Contract):
    """Reversible provisional site retaining every source-record membership."""

    schema_version: Literal["1.0"] = "1.0"
    canonical_site_id: Identifier
    deduplication_version: Identifier
    canonical_name: NonEmptyStr
    geometry_wgs84: PointGeometry
    members: list[CanonicalSiteMember]
    representative_source_record_id: Identifier
    high_confidence_positive: bool
    commodity_definition_ids: list[Identifier] = Field(default_factory=list)
    unresolved_duplicate_risk: bool = False
    notes: list[NonEmptyStr] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_membership(self) -> CanonicalSite:
        """Require unique, traceable source memberships and a valid representative."""
        if not self.members:
            raise ValueError("canonical sites must contain at least one source record")
        member_ids = [member.source_record_id for member in self.members]
        validate_identifier_collection(member_ids, label="source-record memberships")
        if self.representative_source_record_id not in member_ids:
            raise ValueError("representative source record must be a site member")
        validate_identifier_collection(
            list(self.commodity_definition_ids),
            label="commodity_definition_ids",
        )
        return self
