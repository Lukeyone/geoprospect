"""Common types and geometry validation for Stage 0 evidence contracts."""

from __future__ import annotations

import math
from itertools import pairwise
from typing import Annotated, Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, StringConstraints, model_validator

type NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
type Identifier = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=128,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]*$",
    ),
]
type Sha256 = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{64}$")]
type Percentage = Annotated[float, Field(ge=0.0, le=100.0)]
type Longitude = Annotated[float, Field(ge=-180.0, le=180.0)]
type Latitude = Annotated[float, Field(ge=-90.0, le=90.0)]
type Coordinate2D = tuple[float, float]


class Stage0Contract(BaseModel):
    """Strict base model for versioned Stage 0 evidence."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )


class BoundingBox(Stage0Contract):
    """Axis-aligned bounding box in the separately declared CRS."""

    min_x: float
    min_y: float
    max_x: float
    max_y: float

    @model_validator(mode="after")
    def validate_bounds(self) -> BoundingBox:
        """Require finite, ordered bounds with positive width and height."""
        values = (self.min_x, self.min_y, self.max_x, self.max_y)
        if not all(math.isfinite(value) for value in values):
            raise ValueError("bounding-box coordinates must be finite")
        if self.min_x >= self.max_x or self.min_y >= self.max_y:
            raise ValueError("bounding box must have positive width and height")
        return self


class PointGeometry(Stage0Contract):
    """GeoJSON-like point geometry."""

    type: Literal["Point"] = "Point"
    coordinates: Coordinate2D

    @model_validator(mode="after")
    def validate_coordinates(self) -> PointGeometry:
        """Require finite point coordinates."""
        if not all(math.isfinite(value) for value in self.coordinates):
            raise ValueError("point coordinates must be finite")
        return self


class PolygonGeometry(Stage0Contract):
    """GeoJSON-like polygon with validated closed, simple rings."""

    type: Literal["Polygon"] = "Polygon"
    coordinates: list[list[Coordinate2D]]

    @model_validator(mode="after")
    def validate_rings(self) -> PolygonGeometry:
        """Reject empty, open, degenerate or self-intersecting rings."""
        if not self.coordinates:
            raise ValueError("polygon must contain at least one ring")
        for ring in self.coordinates:
            _validate_ring(ring)
        return self


class MultiPolygonGeometry(Stage0Contract):
    """GeoJSON-like multipolygon with validated component rings."""

    type: Literal["MultiPolygon"] = "MultiPolygon"
    coordinates: list[list[list[Coordinate2D]]]

    @model_validator(mode="after")
    def validate_polygons(self) -> MultiPolygonGeometry:
        """Reject empty or invalid component polygons."""
        if not self.coordinates:
            raise ValueError("multipolygon must contain at least one polygon")
        for polygon in self.coordinates:
            if not polygon:
                raise ValueError("multipolygon components must contain a ring")
            for ring in polygon:
                _validate_ring(ring)
        return self


type PolygonalGeometry = Annotated[
    PolygonGeometry | MultiPolygonGeometry,
    Field(discriminator="type"),
]


def ensure_not_future(value: AwareDatetime, *, reference: AwareDatetime, label: str) -> None:
    """Reject source timestamps occurring after their retrieval timestamp."""
    if value > reference:
        raise ValueError(f"{label} cannot be later than retrieval time")


def _validate_ring(ring: list[Coordinate2D]) -> None:
    if len(ring) < 4:
        raise ValueError("polygon rings must contain at least four positions")
    if ring[0] != ring[-1]:
        raise ValueError("polygon rings must be closed")
    if not all(math.isfinite(value) for point in ring for value in point):
        raise ValueError("polygon coordinates must be finite")
    if _has_self_intersection(ring):
        raise ValueError("polygon rings must not self-intersect")
    if abs(_signed_area(ring)) <= 1e-12:
        raise ValueError("polygon rings must enclose non-zero area")


def _signed_area(ring: list[Coordinate2D]) -> float:
    return 0.5 * sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in pairwise(ring))


def _has_self_intersection(ring: list[Coordinate2D]) -> bool:
    segments = list(pairwise(ring))
    last_index = len(segments) - 1
    for first_index, first_segment in enumerate(segments):
        for second_index in range(first_index + 1, len(segments)):
            if second_index in {first_index - 1, first_index, first_index + 1}:
                continue
            if first_index == 0 and second_index == last_index:
                continue
            if _segments_intersect(first_segment, segments[second_index]):
                return True
    return False


def _segments_intersect(
    first: tuple[Coordinate2D, Coordinate2D],
    second: tuple[Coordinate2D, Coordinate2D],
) -> bool:
    a, b = first
    c, d = second
    orientations = (
        _orientation(a, b, c),
        _orientation(a, b, d),
        _orientation(c, d, a),
        _orientation(c, d, b),
    )
    if orientations[0] != orientations[1] and orientations[2] != orientations[3]:
        return True
    return (
        (orientations[0] == 0 and _on_segment(a, c, b))
        or (orientations[1] == 0 and _on_segment(a, d, b))
        or (orientations[2] == 0 and _on_segment(c, a, d))
        or (orientations[3] == 0 and _on_segment(c, b, d))
    )


def _orientation(a: Coordinate2D, b: Coordinate2D, c: Coordinate2D) -> int:
    value = (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])
    if math.isclose(value, 0.0, abs_tol=1e-12):
        return 0
    return 1 if value > 0 else 2


def _on_segment(a: Coordinate2D, b: Coordinate2D, c: Coordinate2D) -> bool:
    return min(a[0], c[0]) <= b[0] <= max(a[0], c[0]) and min(a[1], c[1]) <= b[1] <= max(a[1], c[1])


def validate_identifier_collection(values: list[str], *, label: str) -> None:
    """Require identifier collections to contain no duplicates."""
    if len(values) != len(set(values)):
        raise ValueError(f"{label} must not contain duplicate identifiers")
