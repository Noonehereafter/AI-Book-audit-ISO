from __future__ import annotations

import json
from pathlib import Path
from typing import Any
import pandas as pd
from jinja2 import Template

from epub_translate_audit.ai.schemas import AIFinding, ReleaseDecisionResponse
from epub_translate_audit.compliance.iso17100 import ISO17100ComplianceReport
from epub_translate_audit.compliance.iso5060 import ISO5060ComplianceReport

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Báo Cáo Audit Bản Dịch (ISO 17100 & ISO 5060) - {{ run_id }}</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 30px; background-color: #f9f9f9; color: #333; }
        .card { background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .status-PASS, .status-COMPLIANT, .status-GRADE_A_EXCELLENT, .status-GRADE_B_ACCEPTABLE { color: #2e7d32; font-weight: bold; }
        .status-CONDITIONAL_PASS, .status-CONDITIONALLY_COMPLIANT, .status-GRADE_C_MARGINAL { color: #ed6c02; font-weight: bold; }
        .status-FAIL, .status-NON_COMPLIANT, .status-GRADE_F_UNACCEPTABLE { color: #d32f2f; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #f0f0f0; }
        .sev-critical { background-color: #ffebee; color: #c62828; font-weight: bold; }
        .sev-major { background-color: #fff3e0; color: #e65100; }
        .sev-minor { background-color: #f1f8e9; color: #33691e; }
        .iso-badge { display: inline-block; padding: 6px 12px; background: #e3f2fd; color: #1565c0; border-radius: 4px; font-weight: bold; margin-bottom: 10px; margin-right: 10px; }
    </style>
</head>
<body>
    <h1>Báo Cáo Kiểm Toán Bản Dịch (ISO 17100 & ISO 5060)</h1>
    <div class="card">
        <h2>Tổng Quan Quyết Định Phát Hành</h2>
        <p><strong>Mã Lần Chạy:</strong> {{ run_id }}</p>
        <p><strong>Trạng Thái Phát Hành:</strong> <span class="status-{{ release_decision.status }}">{{ release_decision.status }}</span></p>
        <p><strong>Tóm Tắt Chất Lượng:</strong> {{ release_decision.quality_summary_vi }}</p>
        {% if release_decision.hard_blockers %}
        <h3>Hard Blockers:</h3>
        <ul>
            {% for blocker in release_decision.hard_blockers %}
            <li>{{ blocker }}</li>
            {% endfor %}
        </ul>
        {% endif %}
    </div>

    {% if iso5060_compliance %}
    <div class="card">
        <h2>Đánh Giá Chất Lượng ISO 5060 / MQM Error Typology</h2>
        <div class="iso-badge">Xếp Hạng Chất Lượng: <span class="status-{{ iso5060_compliance.quality_grade }}">{{ iso5060_compliance.quality_grade }}</span></div>
        <p><strong>Weighted Error Rate (WER):</strong> {{ iso5060_compliance.weighted_error_rate_per_1000_words }} điểm phạt / 1000 từ (Tổng điểm phạt: {{ iso5060_compliance.total_penalty_points }})</p>
        <p><strong>Đánh Giá Tóm Tắt:</strong> {{ iso5060_compliance.summary_vi }}</p>
        {% if iso5060_compliance.category_breakdowns %}
        <table>
            <thead>
                <tr>
                    <th>Hạng Mục Lỗi MQM</th>
                    <th>Critical (25đ)</th>
                    <th>Major (5đ)</th>
                    <th>Minor (1đ)</th>
                    <th>Cosmetic (0.25đ)</th>
                    <th>Tổng Điểm Phạt</th>
                </tr>
            </thead>
            <tbody>
                {% for b in iso5060_compliance.category_breakdowns %}
                <tr>
                    <td><strong>{{ b.category }}</strong></td>
                    <td>{{ b.critical_count }}</td>
                    <td>{{ b.major_count }}</td>
                    <td>{{ b.minor_count }}</td>
                    <td>{{ b.cosmetic_count }}</td>
                    <td>{{ "%.2f"|format(b.weighted_penalty_points) }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% endif %}
    </div>
    {% endif %}

    {% if iso_compliance %}
    <div class="card">
        <h2>Chứng Nhận Quy Trình Tuân Thủ ISO 17100</h2>
        <div class="iso-badge">ISO 17100 Status: <span class="status-{{ iso_compliance.overall_status }}">{{ iso_compliance.overall_status }}</span></div>
        <p><strong>Đánh Giá Tổng Thể:</strong> {{ iso_compliance.certificate_summary_vi }}</p>
        <table>
            <thead>
                <tr>
                    <th>Giai Đoạn Quy Trình ISO 17100</th>
                    <th>Trạng Thái</th>
                    <th>Điểm Chất Lượng</th>
                    <th>Số Lỗi Ghi Nhận</th>
                    <th>Ghi Chú Đánh Giá</th>
                </tr>
            </thead>
            <tbody>
                {% for phase in iso_compliance.phase_results %}
                <tr>
                    <td><strong>{{ phase.phase.upper() }}</strong></td>
                    <td><span class="status-{{ phase.status }}">{{ phase.status }}</span></td>
                    <td>{{ "%.1f"|format(phase.score_percentage) }}%</td>
                    <td>{{ phase.findings_count }}</td>
                    <td>{{ phase.notes_vi }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% endif %}

    <div class="card">
        <h2>Danh Sách Lỗi Phát Hiện ({{ findings|length }})</h2>
        <table>
            <thead>
                <tr>
                    <th>STT</th>
                    <th>Hạng Mục</th>
                    <th>Mức Độ</th>
                    <th>Trích Dẫn Nguồn</th>
                    <th>Trích Dẫn Đích (Việt)</th>
                    <th>Giải Thích & Tác Động</th>
                </tr>
            </thead>
            <tbody>
                {% for f in findings %}
                <tr>
                    <td>{{ loop.index }}</td>
                    <td>{{ f.category }} ({{ f.subcategory }})</td>
                    <td class="sev-{{ f.severity }}">{{ f.severity.upper() }}</td>
                    <td><code>{{ f.evidence.source_quote or "N/A" }}</code></td>
                    <td><code>{{ f.evidence.target_quote }}</code></td>
                    <td>{{ f.explanation_vi }}<br><em>Tác động: {{ f.impact_vi }}</em></td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
"""


class ReportGenerator:
    """Generates all output artifacts including ISO 17100 & ISO 5060 compliance reports."""

    @staticmethod
    def generate_all(
        output_dir: Path | str,
        audit_result: dict[str, Any],
    ) -> dict[str, Path]:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        run_id = audit_result["run_id"]
        findings: list[AIFinding] = audit_result["all_findings"]
        release_decision: ReleaseDecisionResponse = audit_result["release_decision"]
        iso17100_compliance: ISO17100ComplianceReport | None = audit_result.get("iso_compliance")
        iso5060_compliance: ISO5060ComplianceReport | None = audit_result.get("iso5060_compliance")

        # 1. HTML Report
        template = Template(HTML_TEMPLATE)
        html_content = template.render(
            run_id=run_id,
            release_decision=release_decision,
            iso_compliance=iso17100_compliance,
            iso5060_compliance=iso5060_compliance,
            findings=findings,
        )
        html_file = out_path / "audit_report.html"
        html_file.write_text(html_content, encoding="utf-8")

        # 2. JSON Manifest & Release Decision
        manifest_file = out_path / "run_manifest.json"
        manifest_file.write_text(
            json.dumps(
                {
                    "run_id": run_id,
                    "translated_path": audit_result["translated_path"],
                    "source_path": audit_result["source_path"],
                    "total_target_words": audit_result["total_target_words"],
                    "total_issues_found": len(findings),
                    "iso17100_status": iso17100_compliance.overall_status if iso17100_compliance else "UNKNOWN",
                    "iso5060_grade": iso5060_compliance.quality_grade if iso5060_compliance else "UNKNOWN",
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        decision_file = out_path / "release_decision.json"
        decision_payload = release_decision.model_dump()
        if iso17100_compliance:
            decision_payload["iso17100_compliance"] = iso17100_compliance.model_dump()
        if iso5060_compliance:
            decision_payload["iso5060_compliance"] = iso5060_compliance.model_dump()

        decision_file.write_text(
            json.dumps(decision_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        # 3. CSV Issues
        rows = []
        for idx, f in enumerate(findings, 1):
            rows.append(
                {
                    "issue_id": f"ISSUE_{idx:03d}",
                    "category": f.category,
                    "subcategory": f.subcategory,
                    "severity": f.severity,
                    "confidence": f.confidence,
                    "source_quote": f.evidence.source_quote,
                    "target_quote": f.evidence.target_quote,
                    "explanation_vi": f.explanation_vi,
                    "impact_vi": f.impact_vi,
                    "suggested_correction_vi": f.suggested_correction_vi,
                }
            )

        df_issues = pd.DataFrame(rows)
        csv_file = out_path / "issues.csv"
        df_issues.to_csv(csv_file, index=False, encoding="utf-8-sig")

        # 4. XLSX Issue Ledger
        xlsx_file = out_path / "issue_ledger.xlsx"
        with pd.ExcelWriter(xlsx_file, engine="openpyxl") as writer:
            df_issues.to_excel(writer, sheet_name="Issues", index=False)

        return {
            "html": html_file,
            "json_manifest": manifest_file,
            "json_decision": decision_file,
            "csv_issues": csv_file,
            "xlsx_ledger": xlsx_file,
        }
