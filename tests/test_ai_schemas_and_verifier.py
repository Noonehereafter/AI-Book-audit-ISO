from epub_translate_audit.ai.schemas import AIFinding, AuditCategory, Severity, Evidence
from epub_translate_audit.ai.evidence_verifier import EvidenceVerifier


def test_evidence_verification():
    source = "The quick brown fox jumps over the lazy dog."
    target = "Con cáo nâu nhanh nhạy nhảy qua con chó lười biếng."

    # Valid finding
    valid_f = AIFinding(
        category=AuditCategory.ACCURACY,
        subcategory="mistranslation",
        severity=Severity.MINOR,
        confidence=0.9,
        evidence=Evidence(
            source_quote="quick brown fox",
            target_quote="Con cáo nâu nhanh nhạy"
        ),
        explanation_vi="Dịch đúng cụm từ.",
        impact_vi="Không đáng kể.",
    )

    errs = EvidenceVerifier.verify_finding(valid_f, source, target)
    assert len(errs) == 0

    # Invalid finding (quote not in target)
    invalid_f = AIFinding(
        category=AuditCategory.ACCURACY,
        subcategory="mistranslation",
        severity=Severity.MAJOR,
        confidence=0.9,
        evidence=Evidence(
            source_quote="quick brown fox",
            target_quote="Con mèo đen"
        ),
        explanation_vi="Trích dẫn không có thực.",
        impact_vi="Sai lệch.",
    )

    errs_inv = EvidenceVerifier.verify_finding(invalid_f, source, target)
    assert len(errs_inv) == 1
    assert "not found in target text" in errs_inv[0]
