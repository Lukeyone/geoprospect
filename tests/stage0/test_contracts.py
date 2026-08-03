"""Acceptance and boundary tests for all required Stage 0 evidence contracts."""

from __future__ import annotations

import copy
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from geoprospect.stage0.contracts import (
    CandidateStudyArea,
    CanonicalSite,
    CommodityMappingResult,
    ComparisonOperator,
    CoverageSummary,
    GateName,
    GateResult,
    GateResultSet,
    GateStatus,
    OccurrenceSnapshot,
    OccurrenceSourceRecord,
    ProvisionalCell,
    SourceManifest,
    SpatialBlock,
    SpatialLayout,
    Stage0Decision,
)

FIXTURE_DIR = Path(__file__).parent / "fixtures"
FIXTURE_MODELS: dict[str, type[BaseModel]] = {
    "source_manifest.json": SourceManifest,
    "occurrence_record.json": OccurrenceSourceRecord,
    "occurrence_snapshot.json": OccurrenceSnapshot,
    "commodity_mapping.json": CommodityMappingResult,
    "canonical_site.json": CanonicalSite,
    "candidate_study_area.json": CandidateStudyArea,
    "provisional_cell.json": ProvisionalCell,
    "spatial_block.json": SpatialBlock,
    "coverage_summary.json": CoverageSummary,
    "gate_results.json": GateResultSet,
}


def load_fixture(name: str) -> dict[str, Any]:
    """Load one JSON fixture as a mutable mapping."""
    value: object = json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_all_required_contract_fixtures_validate_and_round_trip() -> None:
    """Every required Stage 0 evidence type has a valid representative fixture."""
    for name, model_type in FIXTURE_MODELS.items():
        instance = model_type.model_validate(load_fixture(name))
        round_trip = model_type.model_validate_json(instance.model_dump_json())
        assert round_trip == instance, name
        schema = model_type.model_json_schema()
        assert schema["type"] == "object", name


def test_contracts_forbid_unknown_fields() -> None:
    """Schema drift must be explicit rather than silently ignored."""
    payload = load_fixture("source_manifest.json")
    payload["unexpected_field"] = "not allowed"

    with pytest.raises(ValidationError, match="unexpected_field"):
        SourceManifest.model_validate(payload)


def test_source_manifest_requires_checksum_and_consistent_timestamp() -> None:
    """Manifests require checksum identity and plausible source timestamps."""
    payload = load_fixture("source_manifest.json")
    payload["checksum_sha256"] = "not-a-checksum"
    with pytest.raises(ValidationError, match="checksum_sha256"):
        SourceManifest.model_validate(payload)

    payload = load_fixture("source_manifest.json")
    payload["source_modified_at"] = "2026-08-04T00:00:00Z"
    with pytest.raises(ValidationError, match="source_modified_at"):
        SourceManifest.model_validate(payload)


def test_occurrence_record_preserves_raw_values_and_coordinate_consistency() -> None:
    """Normalised geometry cannot replace or contradict original record values."""
    payload = load_fixture("occurrence_record.json")
    payload["original_values"] = {}
    with pytest.raises(ValidationError, match="original_values"):
        OccurrenceSourceRecord.model_validate(payload)

    payload = load_fixture("occurrence_record.json")
    geometry = payload["geometry_wgs84"]
    assert isinstance(geometry, dict)
    geometry["coordinates"] = [139.0, -20.75]
    with pytest.raises(ValidationError, match="geometry_wgs84"):
        OccurrenceSourceRecord.model_validate(payload)


def test_occurrence_snapshot_reconciles_source_counts() -> None:
    """Exact snapshot reconciliation cannot hide a record-count mismatch."""
    payload = load_fixture("occurrence_snapshot.json")
    payload["record_count"] = 1

    with pytest.raises(ValidationError, match="exact reconciliation"):
        OccurrenceSnapshot.model_validate(payload)


def test_commodity_mapping_counts_and_unknown_tokens_reconcile() -> None:
    """Mapping summaries must match their detailed token decisions."""
    payload = load_fixture("commodity_mapping.json")
    payload["mapped_count"] = 3
    with pytest.raises(ValidationError, match="mapped_count"):
        CommodityMappingResult.model_validate(payload)

    payload = load_fixture("commodity_mapping.json")
    payload["unknown_tokens"] = []
    with pytest.raises(ValidationError, match="unknown_tokens"):
        CommodityMappingResult.model_validate(payload)


def test_canonical_sites_preserve_unique_source_membership() -> None:
    """One source record cannot be represented twice within a canonical site."""
    payload = load_fixture("canonical_site.json")
    members = payload["members"]
    assert isinstance(members, list)
    members.append(copy.deepcopy(members[0]))

    with pytest.raises(ValidationError, match="duplicate"):
        CanonicalSite.model_validate(payload)


def test_unresolved_duplicate_risk_prevents_high_confidence_positive() -> None:
    """Unresolved independence risk cannot enter the high-confidence positive count."""
    payload = load_fixture("canonical_site.json")
    payload["unresolved_duplicate_risk"] = True

    with pytest.raises(ValidationError, match="prevents high-confidence"):
        CanonicalSite.model_validate(payload)


def test_study_area_rejects_self_intersecting_polygon() -> None:
    """Candidate boundaries must be closed, non-degenerate and simple."""
    payload = load_fixture("candidate_study_area.json")
    geometry = payload["geometry"]
    assert isinstance(geometry, dict)
    geometry["coordinates"] = [
        [
            [300000.0, 7600000.0],
            [400000.0, 7700000.0],
            [400000.0, 7600000.0],
            [300000.0, 7700000.0],
            [300000.0, 7600000.0],
        ]
    ]

    with pytest.raises(ValidationError, match="self-intersect"):
        CandidateStudyArea.model_validate(payload)


def test_spatial_layout_enforces_one_block_per_cell() -> None:
    """Cell and block membership must reconcile exactly once."""
    cell = ProvisionalCell.model_validate(load_fixture("provisional_cell.json"))
    block = SpatialBlock.model_validate(load_fixture("spatial_block.json"))
    valid_layout = SpatialLayout(
        layout_id="layout-v1",
        study_area_id="study-area-nwqld-a",
        grid_version="grid-5km-v1",
        block_scheme_version="blocks-50km-v1",
        cells=[cell],
        blocks=[block],
    )
    assert valid_layout.cells[0].block_id == valid_layout.blocks[0].block_id

    duplicate_block_payload = load_fixture("spatial_block.json")
    duplicate_block_payload["block_id"] = "block-0002"
    duplicate_block = SpatialBlock.model_validate(duplicate_block_payload)
    with pytest.raises(ValidationError, match="exactly one block"):
        SpatialLayout(
            layout_id="layout-invalid",
            study_area_id="study-area-nwqld-a",
            grid_version="grid-5km-v1",
            block_scheme_version="blocks-50km-v1",
            cells=[cell],
            blocks=[block, duplicate_block],
        )


def test_spatial_layout_reconciles_positive_sites_with_member_cells() -> None:
    """Block positive lists must be derived from exactly their member cells."""
    cell = ProvisionalCell.model_validate(load_fixture("provisional_cell.json"))
    block_payload = load_fixture("spatial_block.json")
    block_payload["positive_site_ids"] = []
    inconsistent_block = SpatialBlock.model_validate(block_payload)

    with pytest.raises(ValidationError, match="positive-site assignments"):
        SpatialLayout(
            layout_id="layout-inconsistent-sites",
            study_area_id="study-area-nwqld-a",
            grid_version="grid-5km-v1",
            block_scheme_version="blocks-50km-v1",
            cells=[cell],
            blocks=[inconsistent_block],
        )


def test_coverage_requires_mask_and_reconciled_percentages() -> None:
    """Coverage evidence cannot omit masking or report inconsistent percentages."""
    payload = load_fixture("coverage_summary.json")
    payload["mask_applied"] = False
    with pytest.raises(ValidationError, match="source mask"):
        CoverageSummary.model_validate(payload)

    payload = load_fixture("coverage_summary.json")
    payload["valid_percent"] = 91.0
    with pytest.raises(ValidationError, match="valid_percent"):
        CoverageSummary.model_validate(payload)

    payload = load_fixture("coverage_summary.json")
    payload["valid_percent"] = 101.0
    with pytest.raises(ValidationError, match="less than or equal to 100"):
        CoverageSummary.model_validate(payload)


def make_numeric_gate(
    gate_name: GateName,
    measured: float,
    threshold: float,
    status: GateStatus,
) -> GateResult:
    """Create a numeric gate result for threshold-boundary tests."""
    return GateResult(
        gate_name=gate_name,
        candidate_id="candidate-a",
        measured_value=measured,
        unit="percent",
        operator=ComparisonOperator.GREATER_THAN_OR_EQUAL,
        threshold_value=threshold,
        status=status,
        evidence_paths=["reports/stage0/test-evidence.csv"],
        failure_action="Apply the documented corrective or switch action",
        evaluated_at=datetime(2026, 8, 3, 3, 0, tzinfo=UTC),
    )


def test_gate_threshold_boundaries_are_deterministic() -> None:
    """Mandatory numeric thresholds pass at the boundary and fail below it."""
    geology_at_boundary = make_numeric_gate(
        GateName.GEOLOGY_COVERAGE,
        measured=95.0,
        threshold=95.0,
        status=GateStatus.PASS,
    )
    assert geology_at_boundary.status is GateStatus.PASS

    magnetic_below_boundary = make_numeric_gate(
        GateName.MAGNETIC_COVERAGE,
        measured=89.99,
        threshold=90.0,
        status=GateStatus.FAIL,
    )
    assert magnetic_below_boundary.status is GateStatus.FAIL

    with pytest.raises(ValidationError, match="contradicts"):
        make_numeric_gate(
            GateName.POSITIVE_COUNT,
            measured=79.0,
            threshold=80.0,
            status=GateStatus.PASS,
        )


def test_resolved_qualitative_gate_requires_measured_evidence() -> None:
    """A qualitative PASS cannot exist without a recorded observation."""
    payload = load_fixture("gate_results.json")
    results = payload["results"]
    assert isinstance(results, list)
    cluster_gate = next(
        result
        for result in results
        if isinstance(result, dict) and result.get("gate_name") == "cluster_dominance"
    )
    assert isinstance(cluster_gate, dict)
    cluster_gate["measured_value"] = None

    with pytest.raises(ValidationError, match="require a measured value"):
        GateResultSet.model_validate(payload)


def test_go_is_rejected_when_any_mandatory_gate_fails() -> None:
    """A GO decision is impossible when even one mandatory gate is non-passing."""
    payload = load_fixture("gate_results.json")
    results = payload["results"]
    assert isinstance(results, list)
    geology = next(
        result
        for result in results
        if isinstance(result, dict) and result.get("gate_name") == "geology_coverage"
    )
    assert isinstance(geology, dict)
    geology["measured_value"] = 94.99
    geology["status"] = "fail"

    with pytest.raises(ValidationError, match="GO is prohibited"):
        GateResultSet.model_validate(payload)

    payload["decision"] = Stage0Decision.SWITCH.value
    payload["rationale"] = "Geology coverage fails the unchanged mandatory threshold"
    switched = GateResultSet.model_validate(payload)
    assert switched.decision is Stage0Decision.SWITCH
