from pathlib import Path
from epub_translate_audit.reports.report_generator import ReportGenerator
from epub_translate_audit.ai.schemas import ReleaseDecisionResponse, AIFinding, AuditCategory, Severity, Evidence


def test_report_generator(tmp_path: Path):
    audit_res = {
        "run_id": "test_run_01",
        "translated_path": "/tmp/vi.epub",
        "source_path": "/tmp/src.epub",
        "total_target_words": 500,
        "all_findings": [
            AIFinding(
                category=AuditCategory.ACCURACY,
                subcategory="omission",
                severity=Severity.MINOR,
                confidence=0.85,
                evidence=Evidence(source_quote="word", target_quote="từ"),
                explanation_vi="Giải thích lỗi.",
                impact_vi="Ảnh hưởng nhẹ.",
            )
        ],
        "release_decision": ReleaseDecisionResponse(
            status="PASS",
            hard_blockers=[],
            quality_summary_vi="Bản dịch đạt chuẩn."
        )
    }

    out_files = ReportGenerator.generate_all(tmp_path, audit_res)
    assert out_files["html"].exists()
    assert out_files["csv_issues"].exists()
    assert out_files["xlsx_ledger"].exists()
    assert out_files["json_manifest"].exists()
    assert out_files["json_decision"].exists()
