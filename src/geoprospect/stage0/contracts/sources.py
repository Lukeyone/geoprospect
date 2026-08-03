"""Contracts for authoritative source and licence manifests."""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import AwareDatetime, Field, HttpUrl, JsonValue, model_validator

from geoprospect.stage0.contracts.base import (
    BoundingBox,
    Identifier,
    NonEmptyStr,
    Sha256,
    Stage0Contract,
    ensure_not_future,
)


class SourceClass(StrEnum):
    """Stage 0 source classes."""

    MINERAL_OCCURRENCES = "mineral_occurrences"
    GEOLOGY = "geology"
    STRUCTURES = "structures"
    MAGNETICS = "magnetics"
    GRAVITY = "gravity"
    AUXILIARY = "auxiliary"


class AccessMethod(StrEnum):
    """Supported authoritative access pathways."""

    ARCGIS_REST = "arcgis_rest"
    OGC_API = "ogc_api"
    WFS = "wfs"
    WCS = "wcs"
    DOWNLOAD = "download"
    OTHER = "other"


class PublicationPermission(StrEnum):
    """Publication permission classification pending licence review."""

    PERMITTED = "permitted"
    PROHIBITED = "prohibited"
    CONDITIONAL = "conditional"
    UNRESOLVED = "unresolved"


class LicenceMetadata(Stage0Contract):
    """Source-specific licence and attribution evidence."""

    name: NonEmptyStr
    url: HttpUrl | None = None
    attribution: NonEmptyStr
    raw_redistribution: PublicationPermission
    derived_outputs: PublicationPermission
    conditions: list[NonEmptyStr] = Field(default_factory=list)


class SourceManifest(Stage0Contract):
    """Checksum-identified manifest for one retrieved authoritative product."""

    schema_version: Literal["1.0"] = "1.0"
    source_id: Identifier
    source_class: SourceClass
    publisher: NonEmptyStr
    title: NonEmptyStr
    official_source_url: HttpUrl
    access_url: HttpUrl
    access_method: AccessMethod
    product_or_layer_id: NonEmptyStr
    format: NonEmptyStr
    crs: NonEmptyStr
    spatial_extent: BoundingBox | None = None
    retrieved_at: AwareDatetime
    source_modified_at: AwareDatetime | None = None
    checksum_sha256: Sha256
    byte_size: int = Field(ge=0)
    record_count: int | None = Field(default=None, ge=0)
    licence: LicenceMetadata
    retrieval_parameters: dict[str, JsonValue] = Field(default_factory=dict)
    limitations: list[NonEmptyStr] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_timestamps(self) -> SourceManifest:
        """Require source modification metadata not to post-date retrieval."""
        if self.source_modified_at is not None:
            ensure_not_future(
                self.source_modified_at,
                reference=self.retrieved_at,
                label="source_modified_at",
            )
        return self
