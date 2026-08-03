"""Contracts for authoritative source discovery, licensing and manifests."""

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
    WMS = "wms"
    DOWNLOAD = "download"
    OTHER = "other"


class PublicationPermission(StrEnum):
    """Publication permission classification pending licence review."""

    PERMITTED = "permitted"
    PROHIBITED = "prohibited"
    CONDITIONAL = "conditional"
    UNRESOLVED = "unresolved"


class DiscoveryStatus(StrEnum):
    """Step 0.7 disposition of a candidate source pathway."""

    PLAUSIBLE = "plausible"
    REJECTED = "rejected"


class EndpointValidationStatus(StrEnum):
    """Strength of endpoint evidence collected during discovery."""

    LIVE_METADATA_VALIDATED = "live_metadata_validated"
    OFFICIAL_METADATA_VALIDATED = "official_metadata_validated"
    FAILED = "failed"


class LicenceReviewStatus(StrEnum):
    """Boundary between Step 0.7 discovery and Step 0.8 legal review."""

    PENDING_STEP_0_8 = "pending_step_0_8"
    COMPLETE = "complete"


class LicenceMetadata(Stage0Contract):
    """Source-specific licence and attribution evidence."""

    name: NonEmptyStr
    url: HttpUrl | None = None
    attribution: NonEmptyStr
    raw_redistribution: PublicationPermission
    derived_outputs: PublicationPermission
    conditions: list[NonEmptyStr] = Field(default_factory=list)


class EndpointValidation(Stage0Contract):
    """Traceable validation of a source metadata or access endpoint."""

    checked_at: AwareDatetime
    validation_url: HttpUrl
    status: EndpointValidationStatus
    method: NonEmptyStr
    observed_evidence: list[NonEmptyStr]
    limitations: list[NonEmptyStr] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_evidence(self) -> EndpointValidation:
        """A successful validation must contain observed endpoint evidence."""
        if self.status is not EndpointValidationStatus.FAILED and not self.observed_evidence:
            raise ValueError("successful endpoint validation requires observed evidence")
        return self


class SourceRegistryEntry(Stage0Contract):
    """Discovery-time registry entry for one plausible authoritative pathway."""

    schema_version: Literal["1.0"] = "1.0"
    source_id: Identifier
    source_class: SourceClass
    status: DiscoveryStatus
    publisher: NonEmptyStr
    title: NonEmptyStr
    official_source_url: HttpUrl
    metadata_url: HttpUrl
    access_urls: list[HttpUrl]
    access_method: AccessMethod
    product_or_layer_id: NonEmptyStr
    related_layer_ids: list[NonEmptyStr] = Field(default_factory=list)
    formats: list[NonEmptyStr]
    service_crs: NonEmptyStr
    source_crs: NonEmptyStr | None = None
    spatial_extent: BoundingBox
    extent_crs: NonEmptyStr
    nominal_resolution: NonEmptyStr | None = None
    update_metadata: NonEmptyStr
    relevant_fields_or_bands: list[NonEmptyStr]
    endpoint_validation: EndpointValidation
    licence_review_status: LicenceReviewStatus
    licence_evidence_urls: list[HttpUrl] = Field(default_factory=list)
    limitations: list[NonEmptyStr]
    selection_notes: list[NonEmptyStr] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_discovery_entry(self) -> SourceRegistryEntry:
        """Require a usable, non-duplicated and honestly qualified pathway."""
        if not self.access_urls:
            raise ValueError("source registry entries require at least one access URL")
        if len({str(url) for url in self.access_urls}) != len(self.access_urls):
            raise ValueError("access_urls must not contain duplicates")
        if not self.formats:
            raise ValueError("source registry entries require at least one format")
        if len(set(self.formats)) != len(self.formats):
            raise ValueError("formats must not contain duplicates")
        if len(set(self.related_layer_ids)) != len(self.related_layer_ids):
            raise ValueError("related_layer_ids must not contain duplicates")
        if not self.relevant_fields_or_bands:
            raise ValueError("source registry entries require relevant fields or bands")
        if not self.limitations:
            raise ValueError("source registry entries must expose known limitations")
        if self.status is DiscoveryStatus.PLAUSIBLE:
            if self.endpoint_validation.status is EndpointValidationStatus.FAILED:
                raise ValueError("a failed endpoint cannot be registered as plausible")
            if self.licence_review_status is not LicenceReviewStatus.PENDING_STEP_0_8:
                raise ValueError("Step 0.7 entries must defer final licence classification")
            urls = [
                self.official_source_url,
                self.metadata_url,
                self.endpoint_validation.validation_url,
                *self.access_urls,
                *self.licence_evidence_urls,
            ]
            if any(url.scheme != "https" for url in urls):
                raise ValueError("plausible source pathways require HTTPS URLs")
            if self.source_class in {SourceClass.MAGNETICS, SourceClass.GRAVITY}:
                numeric_grid = any((url.path or "").endswith(".nc") for url in self.access_urls)
                if not numeric_grid:
                    raise ValueError("geophysical sources require a numeric NetCDF grid pathway")
        return self


class SourceRegistry(Stage0Contract):
    """Aggregate Step 0.7 registry requiring every mandatory source class."""

    schema_version: Literal["1.0"] = "1.0"
    step_id: Literal["0.7"] = "0.7"
    discovered_at: AwareDatetime
    entries: list[SourceRegistryEntry]

    @model_validator(mode="after")
    def validate_mandatory_coverage(self) -> SourceRegistry:
        """Require one unique plausible pathway for all five mandatory classes."""
        mandatory = {
            SourceClass.MINERAL_OCCURRENCES,
            SourceClass.GEOLOGY,
            SourceClass.STRUCTURES,
            SourceClass.MAGNETICS,
            SourceClass.GRAVITY,
        }
        plausible = [entry for entry in self.entries if entry.status is DiscoveryStatus.PLAUSIBLE]
        classes = [entry.source_class for entry in plausible]
        if len(classes) != len(set(classes)):
            raise ValueError("plausible source classes must be unique")
        missing = mandatory - set(classes)
        if missing:
            missing_names = ", ".join(sorted(item.value for item in missing))
            raise ValueError(f"mandatory source registry is incomplete: {missing_names}")
        for entry in plausible:
            ensure_not_future(
                entry.endpoint_validation.checked_at,
                reference=self.discovered_at,
                label="endpoint validation time",
            )
        return self


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
