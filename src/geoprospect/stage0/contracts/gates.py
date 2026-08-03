"""Contracts and boundary validation for formal Stage 0 gate evidence."""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import AwareDatetime, Field, model_validator

from geoprospect.stage0.contracts.base import Identifier, NonEmptyStr, Stage0Contract


class GateName(StrEnum):
    """Mandatory Stage 0 feasibility gates."""

    POSITIVE_COUNT = "positive_count"
    SPATIAL_SPREAD = "spatial_spread"
    CLUSTER_DOMINANCE = "cluster_dominance"
    GEOLOGY_COVERAGE = "geology_coverage"
    MAGNETIC_COVERAGE = "magnetic_coverage"
    GRAVITY_COVERAGE = "gravity_coverage"
    LABEL_QUALITY = "label_quality"
    LICENSING = "licensing"
    EVALUATION_FEASIBILITY = "evaluation_feasibility"
    EXPLORATION_BIAS = "exploration_bias"


class ComparisonOperator(StrEnum):
    """How a measured value is compared with a threshold."""

    GREATER_THAN_OR_EQUAL = "ge"
    LESS_THAN_OR_EQUAL = "le"
    EQUAL = "eq"
    QUALITATIVE = "qualitative"


class GateStatus(StrEnum):
    """Resolution status of one gate."""

    PASS = "pass"
    FAIL = "fail"
    BLOCKED = "blocked"
    UNRESOLVED = "unresolved"
    NOT_APPLICABLE = "not_applicable"


class Stage0Decision(StrEnum):
    """Formal decision state."""

    PENDING = "pending"
    GO = "go"
    SWITCH = "switch"
    STOP = "stop"


type MeasuredValue = float | int | str | bool


class GateResult(Stage0Contract):
    """One traceable gate measurement, threshold and failure action."""

    schema_version: Literal["1.0"] = "1.0"
    gate_name: GateName
    candidate_id: Identifier
    measured_value: MeasuredValue | None
    unit: NonEmptyStr
    operator: ComparisonOperator
    threshold_value: MeasuredValue | None
    status: GateStatus
    mandatory: bool = True
    evidence_paths: list[NonEmptyStr]
    failure_action: NonEmptyStr
    evaluated_at: AwareDatetime
    notes: list[NonEmptyStr] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_measurement(self) -> GateResult:
        """Require evidence and make numeric pass/fail status deterministic."""
        if not self.evidence_paths:
            raise ValueError("gate results require at least one evidence path")
        if self.operator is ComparisonOperator.QUALITATIVE:
            if self.threshold_value is None:
                raise ValueError("qualitative gates require an explicit acceptance rule")
            return self
        if not isinstance(self.measured_value, (int, float)) or isinstance(
            self.measured_value,
            bool,
        ):
            raise ValueError("numeric gate operators require a numeric measured value")
        if not isinstance(self.threshold_value, (int, float)) or isinstance(
            self.threshold_value,
            bool,
        ):
            raise ValueError("numeric gate operators require a numeric threshold")
        if self.operator is ComparisonOperator.GREATER_THAN_OR_EQUAL:
            passes = self.measured_value >= self.threshold_value
        elif self.operator is ComparisonOperator.LESS_THAN_OR_EQUAL:
            passes = self.measured_value <= self.threshold_value
        else:
            passes = self.measured_value == self.threshold_value
        if self.status in {GateStatus.PASS, GateStatus.FAIL}:
            expected = GateStatus.PASS if passes else GateStatus.FAIL
            if self.status is not expected:
                raise ValueError("gate status contradicts the measured threshold comparison")
        return self


class GateResultSet(Stage0Contract):
    """Complete mandatory gate set enforcing GO/SWITCH/STOP consistency."""

    schema_version: Literal["1.0"] = "1.0"
    decision_id: Identifier
    candidate_id: Identifier
    decision: Stage0Decision
    results: list[GateResult]
    decided_at: AwareDatetime | None = None
    rationale: str | None = None

    @model_validator(mode="after")
    def validate_decision(self) -> GateResultSet:
        """Require every mandatory gate exactly once and forbid GO on any failure."""
        names = [result.gate_name for result in self.results if result.mandatory]
        if len(names) != len(set(names)):
            raise ValueError("mandatory gate names must be unique")
        missing = set(GateName) - set(names)
        if missing:
            missing_names = ", ".join(sorted(gate.value for gate in missing))
            raise ValueError(f"mandatory gate set is incomplete: {missing_names}")
        if any(result.candidate_id != self.candidate_id for result in self.results):
            raise ValueError("all gate results must use the result-set candidate_id")
        mandatory_statuses = {result.status for result in self.results if result.mandatory}
        all_pass = mandatory_statuses == {GateStatus.PASS}
        if self.decision is Stage0Decision.GO and not all_pass:
            raise ValueError("GO is prohibited unless every mandatory gate passes")
        if self.decision is not Stage0Decision.PENDING:
            if self.decided_at is None or not self.rationale:
                raise ValueError("formal decisions require decided_at and rationale")
        elif self.decided_at is not None:
            raise ValueError("pending decisions cannot have decided_at")
        if self.decision in {Stage0Decision.SWITCH, Stage0Decision.STOP} and all_pass:
            raise ValueError("SWITCH or STOP requires at least one non-passing mandatory gate")
        return self
