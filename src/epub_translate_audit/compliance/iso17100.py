from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any
from pydantic import BaseModel, Field

from epub_translate_audit.ai.schemas import AIFinding, Severity


class ISO17100Phase(StrEnum):
    TRANSLATION = "translation"          # Initial MT / Human translation
    REVISION = "revision"                # Bilingual examination against source text
    REVIEW = "review"                    # Monolingual examination of target text for domain suitability
    PROOFREADING = "proofreading"        # Pre-publication formatting, layout & typography check
    FINAL_VERIFICATION = "final_verification"  # Technical & integrity verification against project specs
    SIGN_OFF = "sign_off"                # Formal approval for commercial publication


class ISO17100Status(StrEnum):
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    CONDITIONALLY_COMPLIANT = "CONDITIONALLY_COMPLIANT"


class PhaseCompliance(BaseModel):
    phase: ISO17100Phase
    status: ISO17100Status
    score_percentage: float
    findings_count: int
    notes_vi: str


class ISO17100ComplianceReport(BaseModel):
    overall_status: ISO17100Status
    phase_results: list[PhaseCompliance] = Field(default_factory=list)
    certificate_summary_vi: str
    recommendations_vi: list[str] = Field(default_factory=list)


class ISO17100ComplianceEngine:
    """Evaluates the multi-agent audit results against ISO 17100 Translation Quality Assurance Standards."""

    @staticmethod
    def evaluate_compliance(
        findings: list[AIFinding],
        total_words: int,
        unaligned_source_blocks: int = 0,
        unaligned_target_blocks: int = 0,
    ) -> ISO17100ComplianceReport:
        phase_results: list[PhaseCompliance] = []
        recommendations: list[str] = []

        # 1. Revision Phase (Bilingual Accuracy & Consistency)
        bilingual_issues = [f for f in findings if f.category in {"accuracy", "terminology", "consistency"}]
        crit_bilingual = sum(1 for f in bilingual_issues if f.severity == Severity.CRITICAL)
        maj_bilingual = sum(1 for f in bilingual_issues if f.severity == Severity.MAJOR)

        if crit_bilingual > 0:
            rev_status = ISO17100Status.NON_COMPLIANT
            rev_note = f"Không đạt do có {crit_bilingual} lỗi Critical về chính xác ngữ nghĩa / thuật ngữ."
            recommendations.append("Yêu cầu Biên tập viên Hiệu đính (Reviser) rà soát lại 100% các đoạn lỗi Critical.")
        elif maj_bilingual > 2:
            rev_status = ISO17100Status.CONDITIONALLY_COMPLIANT
            rev_note = f"Đạt có điều kiện: có {maj_bilingual} lỗi Major cần sửa trước khi phát hành."
        else:
            rev_status = ISO17100Status.COMPLIANT
            rev_note = "Đạt chuẩn Hiệu đính song ngữ (Revision) theo ISO 17100."

        phase_results.append(
            PhaseCompliance(
                phase=ISO17100Phase.REVISION,
                status=rev_status,
                score_percentage=max(0.0, 100.0 - (crit_bilingual * 25 + maj_bilingual * 5)),
                findings_count=len(bilingual_issues),
                notes_vi=rev_note,
            )
        )

        # 2. Review Phase (Monolingual Fluency & Literary Style)
        review_issues = [f for f in findings if f.category in {"fluency", "style", "localization"}]
        maj_review = sum(1 for f in review_issues if f.severity in {Severity.CRITICAL, Severity.MAJOR})

        if maj_review > 0:
            review_status = ISO17100Status.CONDITIONALLY_COMPLIANT
            review_note = f"Phát hiện {maj_review} lỗi văn phong / độ tự nhiên cấp độ Major."
            recommendations.append("Chuyển cho Độc giả Đánh giá độc lập (Reviewer) để trau chuốt lại giọng văn tiếng Việt.")
        else:
            review_status = ISO17100Status.COMPLIANT
            review_note = "Đạt chuẩn Đánh giá văn phong đơn ngữ (Review)."

        phase_results.append(
            PhaseCompliance(
                phase=ISO17100Phase.REVIEW,
                status=review_status,
                score_percentage=max(0.0, 100.0 - (maj_review * 10)),
                findings_count=len(review_issues),
                notes_vi=review_note,
            )
        )

        # 3. Proofreading & Formatting Phase
        tech_issues = [f for f in findings if f.category == "technical"]
        proof_status = ISO17100Status.COMPLIANT if len(tech_issues) == 0 else ISO17100Status.CONDITIONALLY_COMPLIANT
        phase_results.append(
            PhaseCompliance(
                phase=ISO17100Phase.PROOFREADING,
                status=proof_status,
                score_percentage=100.0 if proof_status == ISO17100Status.COMPLIANT else 85.0,
                findings_count=len(tech_issues),
                notes_vi="Đạt chuẩn Đọc sửa bản hiển thị & Định dạng EPUB." if proof_status == ISO17100Status.COMPLIANT else "Cần tinh chỉnh lại trình bày/markup.",
            )
        )

        # 4. Final Verification Phase
        if unaligned_source_blocks > 0 or unaligned_target_blocks > 0:
            verif_status = ISO17100Status.NON_COMPLIANT
            verif_note = f"Không đạt: Còn {unaligned_source_blocks} khối nguồn / {unaligned_target_blocks} khối đích chưa ghép cặp."
            recommendations.append("Kiểm tra lại cấu trúc chương EPUB để đảm bảo không bỏ sót văn bản.")
        else:
            verif_status = ISO17100Status.COMPLIANT
            verif_note = "Xác minh toàn vẹn kỹ thuật & cấu trúc hoàn hảo."

        phase_results.append(
            PhaseCompliance(
                phase=ISO17100Phase.FINAL_VERIFICATION,
                status=verif_status,
                score_percentage=100.0 if verif_status == ISO17100Status.COMPLIANT else 50.0,
                findings_count=unaligned_source_blocks + unaligned_target_blocks,
                notes_vi=verif_note,
            )
        )

        # Determine Overall Compliance
        if any(p.status == ISO17100Status.NON_COMPLIANT for p in phase_results):
            overall = ISO17100Status.NON_COMPLIANT
            cert_summary = "Bản dịch CHƯA ĐẠT tiêu chuẩn quản lý chất lượng dịch thuật ISO 17100."
        elif any(p.status == ISO17100Status.CONDITIONALLY_COMPLIANT for p in phase_results):
            overall = ISO17100Status.CONDITIONALLY_COMPLIANT
            cert_summary = "Bản dịch ĐẠT CÓ ĐIỀU KIỆN tiêu chuẩn ISO 17100 (Cần khắc phục các khuyến nghị trước khi xuất bản)."
        else:
            overall = ISO17100Status.COMPLIANT
            cert_summary = "Bản dịch ĐẠT CHUẨN HOÀN HẢO theo tiêu chuẩn chất lượng xuất bản ISO 17100."

        return ISO17100ComplianceReport(
            overall_status=overall,
            phase_results=phase_results,
            certificate_summary_vi=cert_summary,
            recommendations_vi=recommendations,
        )
