from pathlib import Path
from epub_translate_audit.ai.schemas import AIFinding, AuditCategory, Severity, Evidence
from epub_translate_audit.compliance.iso5060 import ISO5060ComplianceEngine, ISO5060QualityGrade
from epub_translate_audit.ingest.linguagacha_adapter import LinguaGachaAdapter


def test_linguagacha_adapter(tmp_path: Path):
    lg_file = tmp_path / "translation_output.txt"
    lg_file.write_text(
        "[John]: Hello {0}, welcome to the town!\n"
        "<speaker:Mary>: Thank you very much.\n"
        "Ordinary line without speaker tag.\n",
        encoding="utf-8"
    )

    parsed = LinguaGachaAdapter.parse_file(lg_file)
    assert len(parsed.lines) == 3
    assert parsed.lines[0].speaker_tag == "John"
    assert "{0}" in parsed.lines[0].placeholders
    assert parsed.lines[1].speaker_tag == "Mary"
    assert parsed.lines[2].speaker_tag is None


def test_iso5060_mqm_engine():
    findings = [
        AIFinding(
            category=AuditCategory.ACCURACY,
            subcategory="mistranslation",
            severity=Severity.MINOR,
            confidence=0.9,
            evidence=Evidence(source_quote="town", target_quote="thị trấn"),
            explanation_vi="Lỗi dịch nhẹ.",
            impact_vi="Thấp.",
        )
    ]

    report = ISO5060ComplianceEngine.evaluate_compliance(findings, total_target_words=1000)
    assert report.pass_threshold_met is True
    assert report.quality_grade in [ISO5060QualityGrade.GRADE_A_EXCELLENT, ISO5060QualityGrade.GRADE_B_ACCEPTABLE]
    assert report.weighted_error_rate_per_1000_words == 1.0
