from pathlib import Path
from epub_translate_audit.ai.schemas import AIFinding, AuditCategory, Severity, Evidence
from epub_translate_audit.orchestrator.self_evolution import SelfEvolutionEngine


def test_self_evolution_engine(tmp_path: Path):
    rules_file = tmp_path / "learned_rules.yaml"
    engine = SelfEvolutionEngine(rules_file)

    findings = [
        AIFinding(
            category=AuditCategory.ACCURACY,
            subcategory="mistranslation",
            severity=Severity.MAJOR,
            confidence=0.9,
            evidence=Evidence(source_quote="fox", target_quote="cáo"),
            explanation_vi="Sai nghĩa tên riêng/thuật ngữ.",
            impact_vi="Ảnh hưởng nội dung.",
            suggested_correction_vi="Đề nghị sửa thành 'hồ ly'.",
        ),
        AIFinding(
            category=AuditCategory.ACCURACY,
            subcategory="mistranslation",
            severity=Severity.MINOR,
            confidence=0.8,
            evidence=Evidence(source_quote="quick", target_quote="nhanh"),
            explanation_vi="Sai nghĩa từ đệm.",
            impact_vi="Ảnh hưởng văn phong.",
            suggested_correction_vi="Đề nghị sửa thành 'nhanh nhẹn'.",
        )
    ]

    rules = engine.consolidate_session_learnings(findings)
    assert len(rules) == 1
    assert rules[0].rule_id == "LEARNED_ACCURACY_MISTRANSLATION"
    assert rules[0].occurrences_count == 2
    assert rules_file.exists()

    # Second run to test accumulation
    rules2 = engine.consolidate_session_learnings(findings)
    assert rules2[0].occurrences_count == 4
