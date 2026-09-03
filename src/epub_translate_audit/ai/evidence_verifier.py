from __future__ import annotations

from epub_translate_audit.ai.schemas import AIFinding, AuditCategory


class EvidenceVerifier:
    """Verifies that quotes in findings actually exist in the source and target texts."""

    @staticmethod
    def verify_finding(finding: AIFinding, source_text: str, target_text: str) -> list[str]:
        errors: list[str] = []

        # Verify target quote
        if finding.evidence.target_quote and finding.evidence.target_quote not in target_text:
            errors.append(
                f"Target quote '{finding.evidence.target_quote}' not found in target text."
            )

        # Verify source quote (unless category is TECHNICAL or target-only)
        if finding.category != AuditCategory.TECHNICAL:
            if not finding.evidence.source_quote:
                errors.append("Source quote is required for non-technical issues.")
            elif finding.evidence.source_quote and finding.evidence.source_quote not in source_text:
                errors.append(
                    f"Source quote '{finding.evidence.source_quote}' not found in source text."
                )

        return errors

    @classmethod
    def filter_valid_findings(
        cls, findings: list[AIFinding], source_text: str, target_text: str
    ) -> tuple[list[AIFinding], list[tuple[AIFinding, list[str]]]]:
        valid: list[AIFinding] = []
        rejected: list[tuple[AIFinding, list[str]]] = []

        for f in findings:
            errs = cls.verify_finding(f, source_text, target_text)
            if errs:
                rejected.append((f, errs))
            else:
                valid.append(f)

        return valid, rejected
