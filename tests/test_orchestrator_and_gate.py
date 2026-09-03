from pathlib import Path
from epub_translate_audit.config import Settings
from epub_translate_audit.ai.schemas import AIFinding, AuditCategory, Severity, Evidence
from epub_translate_audit.orchestrator.release_gate import ReleaseGateEngine
from epub_translate_audit.orchestrator.state_store import AuditStateStore


def test_state_store(tmp_path: Path):
    store = AuditStateStore(tmp_path / "test_state.db")

    findings = [
        {
            "category": "accuracy",
            "subcategory": "mistranslation",
            "severity": "minor",
            "confidence": 0.9,
            "evidence": {"source_quote": "fox", "target_quote": "cáo"},
            "explanation_vi": "Giải thích",
            "impact_vi": "Tác động",
        }
    ]

    store.save_pair_findings("p1", "run1", "semantic", findings)
    cached = store.get_pair_findings("p1", "semantic")
    assert cached == findings


def test_release_gate():
    finding_critical = AIFinding(
        category=AuditCategory.ACCURACY,
        subcategory="omission",
        severity=Severity.CRITICAL,
        confidence=0.95,
        evidence=Evidence(source_quote="missing", target_quote="thiếu"),
        explanation_vi="Bỏ sót một câu quan trọng.",
        impact_vi="Ảnh hưởng cốt truyện.",
    )

    decision = ReleaseGateEngine.evaluate(
        [finding_critical], total_target_words=1000, unaligned_source_count=0
    )
    assert decision.status == "FAIL"
    assert len(decision.hard_blockers) > 0
