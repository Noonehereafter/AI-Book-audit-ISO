from __future__ import annotations

from enum import StrEnum
from pydantic import BaseModel, Field

from epub_translate_audit.ai.schemas import AIFinding, Severity, AuditCategory


class ISO5060QualityGrade(StrEnum):
    GRADE_A_EXCELLENT = "GRADE_A_EXCELLENT"      # WER < 0.5 per 1000 words
    GRADE_B_ACCEPTABLE = "GRADE_B_ACCEPTABLE"    # WER < 2.0 per 1000 words
    GRADE_C_MARGINAL = "GRADE_C_MARGINAL"        # WER < 5.0 per 1000 words
    GRADE_F_UNACCEPTABLE = "GRADE_F_UNACCEPTABLE" # WER >= 5.0 or any Critical error


class MQMCategoryBreakdown(BaseModel):
    category: str
    critical_count: int = 0
    major_count: int = 0
    minor_count: int = 0
    cosmetic_count: int = 0
    weighted_penalty_points: float = 0.0


class ISO5060ComplianceReport(BaseModel):
    quality_grade: ISO5060QualityGrade
    weighted_error_rate_per_1000_words: float
    total_penalty_points: float
    total_target_words: int
    category_breakdowns: list[MQMCategoryBreakdown] = Field(default_factory=list)
    summary_vi: str
    pass_threshold_met: bool


class ISO5060ComplianceEngine:
    """Evaluates LinguaGacha and EPUB translation outputs against ISO 5060 / MQM (Multidimensional Quality Metrics) framework."""

    # ISO 5060 Severity Weights according to MQM standard
    WEIGHT_CRITICAL = 25.0
    WEIGHT_MAJOR = 5.0
    WEIGHT_MINOR = 1.0
    WEIGHT_COSMETIC = 0.25

    @classmethod
    def evaluate_compliance(
        cls,
        findings: list[AIFinding],
        total_target_words: int,
    ) -> ISO5060ComplianceReport:
        words_k = max(total_target_words, 1) / 1000.0

        categories_map: dict[str, MQMCategoryBreakdown] = {}

        total_penalty = 0.0
        has_critical = False

        for f in findings:
            cat_str = f.category.value if hasattr(f.category, "value") else str(f.category)
            if cat_str not in categories_map:
                categories_map[cat_str] = MQMCategoryBreakdown(category=cat_str)

            breakdown = categories_map[cat_str]

            if f.severity == Severity.CRITICAL:
                breakdown.critical_count += 1
                penalty = cls.WEIGHT_CRITICAL
                has_critical = True
            elif f.severity == Severity.MAJOR:
                breakdown.major_count += 1
                penalty = cls.WEIGHT_MAJOR
            elif f.severity == Severity.MINOR:
                breakdown.minor_count += 1
                penalty = cls.WEIGHT_MINOR
            else:
                breakdown.cosmetic_count += 1
                penalty = cls.WEIGHT_COSMETIC

            breakdown.weighted_penalty_points += penalty
            total_penalty += penalty

        wer = round(total_penalty / words_k, 2)

        # Grade determination according to ISO 5060 MQM scoring thresholds
        if has_critical or wer >= 5.0:
            grade = ISO5060QualityGrade.GRADE_F_UNACCEPTABLE
            pass_met = False
            summary = f"Không đạt ISO 5060 (Chỉ số điểm phạt WER = {wer:.2f}/1000 từ). Có lỗi Critical hoặc tổng điểm phạt vượt ngưỡng 5.0."
        elif wer >= 2.0:
            grade = ISO5060QualityGrade.GRADE_C_MARGINAL
            pass_met = True
            summary = f"Đạt ở mức Biên (Marginal Pass) theo ISO 5060 (WER = {wer:.2f}/1000 từ). Cần hiệu đính bổ sung."
        elif wer >= 0.5:
            grade = ISO5060QualityGrade.GRADE_B_ACCEPTABLE
            pass_met = True
            summary = f"Đạt chuẩn Chấp nhận được (Acceptable) theo ISO 5060 (WER = {wer:.2f}/1000 từ)."
        else:
            grade = ISO5060QualityGrade.GRADE_A_EXCELLENT
            pass_met = True
            summary = f"Đạt chuẩn Xuất sắc (Excellent) theo ISO 5060 (WER = {wer:.2f}/1000 từ)."

        return ISO5060ComplianceReport(
            quality_grade=grade,
            weighted_error_rate_per_1000_words=wer,
            total_penalty_points=round(total_penalty, 2),
            total_target_words=total_target_words,
            category_breakdowns=list(categories_map.values()),
            summary_vi=summary,
            pass_threshold_met=pass_met,
        )
