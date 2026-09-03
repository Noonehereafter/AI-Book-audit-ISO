from __future__ import annotations

from typing import Any
from epub_translate_audit.ai.schemas import AIFinding, ReleaseDecisionResponse, Severity


class ReleaseGateEngine:
    """Evaluates Hard Blocks and Quality Thresholds to render release decisions."""

    @staticmethod
    def evaluate(
        all_findings: list[AIFinding],
        total_target_words: int,
        unaligned_source_count: int = 0,
        unaligned_target_count: int = 0,
    ) -> ReleaseDecisionResponse:
        hard_blockers: list[str] = []

        if unaligned_source_count > 0:
            hard_blockers.append(f"There are {unaligned_source_count} unaligned source blocks.")
        if unaligned_target_count > 0:
            hard_blockers.append(f"There are {unaligned_target_count} unaligned target blocks.")

        # Count severities
        critical_count = sum(1 for f in all_findings if f.severity == Severity.CRITICAL)
        major_count = sum(1 for f in all_findings if f.severity == Severity.MAJOR)

        if critical_count > 0:
            hard_blockers.append(f"Found {critical_count} CRITICAL errors.")

        # Major threshold: e.g. > 0.5 per 1000 words
        words_k = max(total_target_words, 1) / 1000.0
        major_rate = major_count / words_k

        if hard_blockers:
            status = "FAIL"
            summary = f"Audit failed due to {len(hard_blockers)} hard blockers."
        elif major_rate > 0.5:
            status = "FAIL"
            summary = f"Major error rate ({major_rate:.2f}/1000 words) exceeds threshold (0.50)."
        elif major_count > 0:
            status = "CONDITIONAL_PASS"
            summary = f"Passed with {major_count} major issues requiring review."
        else:
            status = "PASS"
            summary = "All release criteria met cleanly."

        return ReleaseDecisionResponse(
            status=status,
            hard_blockers=hard_blockers,
            quality_summary_vi=summary,
        )
