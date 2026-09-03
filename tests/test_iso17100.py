from epub_translate_audit.ai.schemas import AIFinding, AuditCategory, Severity, Evidence
from epub_translate_audit.compliance.iso17100 import ISO17100ComplianceEngine, ISO17100Status


def test_iso17100_compliance_engine():
    # Case 1: Clean findings -> Compliant
    report_clean = ISO17100ComplianceEngine.evaluate_compliance([], total_words=1000)
    assert report_clean.overall_status == ISO17100Status.COMPLIANT
    assert len(report_clean.phase_results) == 4

    # Case 2: Critical inaccuracy finding -> Non-compliant in Revision phase
    crit_finding = AIFinding(
        category=AuditCategory.ACCURACY,
        subcategory="omission",
        severity=Severity.CRITICAL,
        confidence=0.95,
        evidence=Evidence(source_quote="missing text", target_quote="đoạn bị thiếu"),
        explanation_vi="Mất thông tin quan trọng.",
        impact_vi="Ảnh hưởng cốt truyện.",
    )

    report_crit = ISO17100ComplianceEngine.evaluate_compliance([crit_finding], total_words=1000)
    assert report_crit.overall_status == ISO17100Status.NON_COMPLIANT
    assert len(report_crit.recommendations_vi) > 0
