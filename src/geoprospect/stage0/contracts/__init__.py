"""Validated data contracts for all required Stage 0 evidence types."""

from geoprospect.stage0.contracts.commodities import (
    CommodityMappingResult,
    CommodityMappingStatus,
    CommodityTokenMapping,
)
from geoprospect.stage0.contracts.coverage import CoverageSummary, CoverageUnit
from geoprospect.stage0.contracts.gates import (
    ComparisonOperator,
    GateName,
    GateResult,
    GateResultSet,
    GateStatus,
    Stage0Decision,
)
from geoprospect.stage0.contracts.occurrences import (
    CountReconciliationStatus,
    OccurrenceQualityFlag,
    OccurrenceSnapshot,
    OccurrenceSourceRecord,
    SnapshotFormat,
)
from geoprospect.stage0.contracts.regions import (
    CandidateStudyArea,
    ProvisionalCell,
    SpatialBlock,
    SpatialLayout,
    StudyAreaStatus,
)
from geoprospect.stage0.contracts.sites import (
    CanonicalSite,
    CanonicalSiteMember,
    DeduplicationMethod,
    MatchConfidence,
)
from geoprospect.stage0.contracts.sources import (
    AccessMethod,
    DiscoveryStatus,
    EndpointValidation,
    EndpointValidationStatus,
    LicenceMetadata,
    LicenceReviewStatus,
    PublicationPermission,
    SourceClass,
    SourceManifest,
    SourceRegistry,
    SourceRegistryEntry,
)

__all__ = [
    "AccessMethod",
    "CandidateStudyArea",
    "CanonicalSite",
    "CanonicalSiteMember",
    "CommodityMappingResult",
    "CommodityMappingStatus",
    "CommodityTokenMapping",
    "ComparisonOperator",
    "CountReconciliationStatus",
    "CoverageSummary",
    "CoverageUnit",
    "DeduplicationMethod",
    "DiscoveryStatus",
    "EndpointValidation",
    "EndpointValidationStatus",
    "GateName",
    "GateResult",
    "GateResultSet",
    "GateStatus",
    "LicenceMetadata",
    "LicenceReviewStatus",
    "MatchConfidence",
    "OccurrenceQualityFlag",
    "OccurrenceSnapshot",
    "OccurrenceSourceRecord",
    "ProvisionalCell",
    "PublicationPermission",
    "SnapshotFormat",
    "SourceClass",
    "SourceManifest",
    "SourceRegistry",
    "SourceRegistryEntry",
    "SpatialBlock",
    "SpatialLayout",
    "Stage0Decision",
    "StudyAreaStatus",
]
