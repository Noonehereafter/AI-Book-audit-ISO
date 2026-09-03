from __future__ import annotations

import re
from rapidfuzz import fuzz
from epub_translate_audit.ai.schemas import AIFinding, AuditCategory


def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text


class EvidenceVerifier:
    """Verifies that quotes in findings exist in the source and target texts using exact and fuzzy matching."""

    @staticmethod
    def verify_finding(finding: AIFinding, source_text: str, target_text: str) -> list[str]:
        errors: list[str] = []

        norm_target = normalize_text(target_text)
        norm_t_quote = normalize_text(finding.evidence.target_quote)

        # Verify target quote
        if norm_t_quote and norm_t_quote not in norm_target:
            sim = fuzz.partial_ratio(norm_t_quote, norm_target)
            if sim < 80.0:
                errors.append(f"Target quote '{finding.evidence.target_quote}' not sufficiently matched in target text (similarity {sim:.1f}%).")

        # Verify source quote (unless category is TECHNICAL)
        if finding.category != AuditCategory.TECHNICAL:
            if not finding.evidence.source_quote:
                errors.append("Source quote is required for non-technical issues.")
            else:
                norm_source = normalize_text(source_text)
                norm_s_quote = normalize_text(finding.evidence.source_quote)
                if norm_s_quote and norm_s_quote not in norm_source:
                    sim_s = fuzz.partial_ratio(norm_s_quote, norm_source)
                    if sim_s < 80.0:
                        errors.append(f"Source quote '{finding.evidence.source_quote}' not sufficiently matched in source text (similarity {sim_s:.1f}%).")

        return errors

    @classmethod
    def filter_valid_findings(
        cls, findings: list[AIFinding], source_text: str, target_text: str
    ) -> tuple[list[AIFinding], list[tuple[AIFinding, list[str]]]]:
        valid: list[AIFinding] = []
        unverified: list[tuple[AIFinding, list[str]]] = []

        for f in findings:
            errs = cls.verify_finding(f, source_text, target_text)
            if errs:
                # Flag for human review instead of silently discarding
                f.requires_human_review = True
                f.explanation_vi += f" [Cảnh báo xác minh trích dẫn: {'; '.join(errs)}]"
                unverified.append((f, errs))
            valid.append(f)

        return valid, unverified
