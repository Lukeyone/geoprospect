"""Validation tests for the Step 0.7 authoritative-source registry."""

from __future__ import annotations

import copy
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from geoprospect.stage0.contracts import (
    DiscoveryStatus,
    EndpointValidationStatus,
    LicenceReviewStatus,
    SourceClass,
    SourceRegistry,
    SourceRegistryEntry,
)

SOURCE_DIR = Path(__file__).parents[2] / "configs" / "sources"
SOURCE_FILES = (
    "mineral_occurrences.yaml",
    "geology.yaml",
    "structures.yaml",
    "magnetics.yaml",
    "gravity.yaml",
)
MANDATORY_CLASSES = {
    SourceClass.MINERAL_OCCURRENCES,
    SourceClass.GEOLOGY,
    SourceClass.STRUCTURES,
    SourceClass.MAGNETICS,
    SourceClass.GRAVITY,
}


def load_payload(name: str) -> dict[str, Any]:
    """Load a JSON-syntax YAML 1.2 source entry."""
    value: object = json.loads((SOURCE_DIR / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def load_entries() -> list[SourceRegistryEntry]:
    """Validate every configured source entry."""
    return [SourceRegistryEntry.model_validate(load_payload(name)) for name in SOURCE_FILES]


def test_every_mandatory_source_class_has_one_plausible_entry() -> None:
    """Step 0.7 cannot pass with a missing or duplicated mandatory pathway."""
    registry = SourceRegistry(
        discovered_at=datetime(2026, 8, 3, 5, 25, tzinfo=UTC),
        entries=load_entries(),
    )

    assert {entry.source_class for entry in registry.entries} == MANDATORY_CLASSES
    assert all(entry.status is DiscoveryStatus.PLAUSIBLE for entry in registry.entries)


def test_registry_entries_are_traceable_and_defer_licensing() -> None:
    """Discovery must expose access evidence without pre-empting Step 0.8."""
    for entry in load_entries():
        assert entry.access_urls
        assert entry.formats
        assert entry.spatial_extent
        assert entry.update_metadata
        assert entry.relevant_fields_or_bands
        assert entry.limitations
        assert entry.endpoint_validation.observed_evidence
        assert entry.endpoint_validation.status in {
            EndpointValidationStatus.LIVE_METADATA_VALIDATED,
            EndpointValidationStatus.OFFICIAL_METADATA_VALIDATED,
        }
        assert entry.licence_review_status is LicenceReviewStatus.PENDING_STEP_0_8


def test_registry_rejects_missing_mandatory_class() -> None:
    """An apparently complete registry cannot silently omit gravity."""
    entries = [
        entry for entry in load_entries() if entry.source_class is not SourceClass.GRAVITY
    ]

    with pytest.raises(ValidationError, match="gravity"):
        SourceRegistry(
            discovered_at=datetime(2026, 8, 3, 5, 25, tzinfo=UTC),
            entries=entries,
        )


def test_registry_rejects_duplicate_plausible_class() -> None:
    """Competing plausible sources require an explicit later comparison."""
    entries = load_entries()
    entries.append(entries[0].model_copy(update={"source_id": "duplicate-minocc"}))

    with pytest.raises(ValidationError, match="unique"):
        SourceRegistry(
            discovered_at=datetime(2026, 8, 3, 5, 25, tzinfo=UTC),
            entries=entries,
        )


def test_plausible_source_rejects_failed_endpoint_validation() -> None:
    """A failed underlying endpoint cannot be hidden behind a catalogue page."""
    payload = load_payload("mineral_occurrences.yaml")
    endpoint = payload["endpoint_validation"]
    assert isinstance(endpoint, dict)
    endpoint["status"] = EndpointValidationStatus.FAILED.value

    with pytest.raises(ValidationError, match="failed endpoint"):
        SourceRegistryEntry.model_validate(payload)


def test_registry_rejects_unqualified_source_without_limitations() -> None:
    """Known source limitations are mandatory evidence, not optional commentary."""
    payload = copy.deepcopy(load_payload("magnetics.yaml"))
    payload["limitations"] = []

    with pytest.raises(ValidationError, match="limitations"):
        SourceRegistryEntry.model_validate(payload)
