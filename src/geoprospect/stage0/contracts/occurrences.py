"""Contracts for occurrence source records and snapshot evidence."""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import AwareDatetime, Field, JsonValue, model_validator

from geoprospect.stage0.contracts.base import (
    Identifier,
    Latitude,
    Longitude,
    NonEmptyStr,
    PointGeometry,
    Sha256,
    Stage0Contract,
)


class OccurrenceQualityFlag(StrEnum):
    """Non-destructive record-quality flags."""

    MISSING_COORDINATES = "missing_coordinates"
    INVALID_RAW_COORDINATES = "invalid_raw_coordinates"
    MISSING_COMMODITY = "missing_commodity"
    MISSING_STATUS = "missing_status"
    SUSPECT_CLUSTER = "suspect_cluster"
    OTHER = "other"


class SnapshotFormat(StrEnum):
    """Permitted Stage 0 occurrence snapshot formats."""

    JSON = "json"
    GEOJSON = "geojson"
    CSV = "csv"
    PARQUET = "parquet"
    GEOPARQUET = "geoparquet"
    OTHER = "other"


class CountReconciliationStatus(StrEnum):
    """Relationship between acquired and source-reported counts."""

    EXACT = "exact"
    NOT_AVAILABLE = "not_available"
    EXPLAINED_MISMATCH = "explained_mismatch"
    UNRESOLVED_MISMATCH = "unresolved_mismatch"


class OccurrenceSourceRecord(Stage0Contract):
    """Preserved source record with optional validated WGS84 coordinates."""

    schema_version: Literal["1.0"] = "1.0"
    source_id: Identifier
    snapshot_id: Identifier
    source_record_id: Identifier
    name_raw: str | None = None
    status_raw: str | None = None
    occurrence_type_raw: str | None = None
    commodities_raw: list[str] = Field(default_factory=list)
    longitude_raw: str | int | float | None = None
    latitude_raw: str | int | float | None = None
    longitude_wgs84: Longitude | None = None
    latitude_wgs84: Latitude | None = None
    geometry_wgs84: PointGeometry | None = None
    coordinate_crs_raw: str | None = None
    original_values: dict[str, JsonValue]
    retrieved_at: AwareDatetime
    quality_flags: set[OccurrenceQualityFlag] = Field(default_factory=set)

    @model_validator(mode="after")
    def validate_coordinates_and_original_values(self) -> OccurrenceSourceRecord:
        """Preserve raw values and require consistent normalised coordinates."""
        if not self.original_values:
            raise ValueError("original_values must preserve at least one source field")
        has_longitude = self.longitude_wgs84 is not None
        has_latitude = self.latitude_wgs84 is not None
        if has_longitude != has_latitude:
            raise ValueError("normalised longitude and latitude must be provided together")
        if has_longitude:
            if self.geometry_wgs84 is None:
                raise ValueError("geometry_wgs84 is required when normalised coordinates exist")
            expected = (self.longitude_wgs84, self.latitude_wgs84)
            if self.geometry_wgs84.coordinates != expected:
                raise ValueError("geometry_wgs84 must match normalised longitude and latitude")
            if OccurrenceQualityFlag.MISSING_COORDINATES in self.quality_flags:
                raise ValueError("record with normalised coordinates cannot be flagged missing")
        elif self.geometry_wgs84 is not None:
            raise ValueError("geometry_wgs84 requires normalised longitude and latitude")
        elif OccurrenceQualityFlag.MISSING_COORDINATES not in self.quality_flags:
            raise ValueError("records without normalised coordinates must be flagged missing")
        return self


class OccurrenceSnapshot(Stage0Contract):
    """Immutable identity and completeness evidence for one bounded snapshot."""

    schema_version: Literal["1.0"] = "1.0"
    snapshot_id: Identifier
    source_id: Identifier
    retrieved_at: AwareDatetime
    checksum_sha256: Sha256
    storage_uri: NonEmptyStr
    format: SnapshotFormat
    content_type: NonEmptyStr
    byte_size: int = Field(ge=0)
    record_count: int = Field(ge=0)
    source_reported_count: int | None = Field(default=None, ge=0)
    count_reconciliation: CountReconciliationStatus
    count_reconciliation_note: str | None = None
    pagination_complete: bool
    original_values_preserved: bool
    manifest_path: NonEmptyStr
    working_copy_path: str | None = None
    limitations: list[NonEmptyStr] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_reconciliation(self) -> OccurrenceSnapshot:
        """Require internally consistent record-count reconciliation evidence."""
        if self.count_reconciliation is CountReconciliationStatus.NOT_AVAILABLE:
            if self.source_reported_count is not None:
                raise ValueError("not_available reconciliation requires no source-reported count")
        elif self.source_reported_count is None:
            raise ValueError("count reconciliation requires a source-reported count")
        elif self.count_reconciliation is CountReconciliationStatus.EXACT:
            if self.record_count != self.source_reported_count:
                raise ValueError("exact reconciliation requires equal acquired and source counts")
        elif self.record_count == self.source_reported_count:
            raise ValueError("equal counts must use exact reconciliation")
        if (
            self.count_reconciliation
            in {
                CountReconciliationStatus.EXPLAINED_MISMATCH,
                CountReconciliationStatus.UNRESOLVED_MISMATCH,
            }
            and not self.count_reconciliation_note
        ):
            raise ValueError("count mismatches require a reconciliation note")
        return self
