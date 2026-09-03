from __future__ import annotations

from enum import StrEnum
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Severity(StrEnum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    COSMETIC = "cosmetic"


class AuditCategory(StrEnum):
    ACCURACY = "accuracy"
    TERMINOLOGY = "terminology"
    ENTITY = "entity"
    CONSISTENCY = "consistency"
    FLUENCY = "fluency"
    STYLE = "style"
    LOCALIZATION = "localization"
    TECHNICAL = "technical"


class Evidence(StrictModel):
    source_quote: str | None = Field(
        default=None,
        description="Exact shortest quote from source. Null only for target-only issues."
    )
    target_quote: str = Field(
        min_length=1,
        description="Exact shortest quote from Vietnamese target."
    )

    @field_validator("source_quote", "target_quote")
    @classmethod
    def no_generic_evidence(cls, value: str | None) -> str | None:
        if value and value.strip().lower() in {"n/a", "none", "không có", "unknown"}:
            raise ValueError("Evidence must be an exact quote, not a placeholder.")
        return value


class AIFinding(StrictModel):
    category: AuditCategory
    subcategory: str = Field(min_length=2, max_length=80)
    severity: Severity
    confidence: Annotated[float, Field(ge=0.0, le=1.0)]
    evidence: Evidence
    explanation_vi: str = Field(min_length=10, max_length=1200)
    impact_vi: str = Field(min_length=5, max_length=700)
    suggested_correction_vi: str | None = Field(default=None, max_length=1200)
    requires_human_review: bool = False


class BookProfileResponse(StrictModel):
    primary_genre: str
    narration_style: str
    tone_register: str
    estimated_risk_level: Literal["low", "medium", "high"]
    key_themes_and_elements: list[str] = Field(default_factory=list)


class AuditPassResponse(StrictModel):
    audit_pass: str
    completed_checks: list[str] = Field(default_factory=list)
    findings: list[AIFinding] = Field(default_factory=list)
    no_material_issue_reason_vi: str | None = None


class AdjudicationResponse(StrictModel):
    accepted_findings: list[AIFinding] = Field(default_factory=list)
    rejected_findings: list[AIFinding] = Field(default_factory=list)
    systemic_issues_summary_vi: list[str] = Field(default_factory=list)


class ReleaseDecisionResponse(StrictModel):
    status: Literal["PASS", "CONDITIONAL_PASS", "REVIEW_REQUIRED", "FAIL"]
    hard_blockers: list[str] = Field(default_factory=list)
    quality_summary_vi: str
