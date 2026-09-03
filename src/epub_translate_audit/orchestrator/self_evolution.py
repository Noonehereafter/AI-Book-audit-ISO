from __future__ import annotations

import logging
from pathlib import Path
from typing import Any
import yaml
from pydantic import BaseModel, Field

from epub_translate_audit.ai.schemas import AIFinding

logger = logging.getLogger(__name__)


class LearnedRule(BaseModel):
    rule_id: str
    category: str
    pattern_description_vi: str
    rule_type: str  # "glossary", "forbidden_variant", "style_rule", "alignment_hint"
    remediation_guideline_vi: str
    occurrences_count: int = 1


class SelfEvolutionEngine:
    """Analyzes audit findings at the end of every session and automatically synthesizes

    new rules/learnings into learned_rules.yaml to ensure self-evolution across runs.
    """

    def __init__(self, rules_file: Path | str | None = None) -> None:
        self.rules_file = Path(rules_file) if rules_file else Path("configs/learned_rules.yaml")
        self.rules_file.parent.mkdir(parents=True, exist_ok=True)

    def load_learned_rules(self) -> list[LearnedRule]:
        if not self.rules_file.exists():
            return []
        try:
            with open(self.rules_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or []
                return [LearnedRule.model_validate(item) for item in data]
        except Exception as e:
            logger.warning("Failed to load learned rules: %s", e)
            return []

    def save_learned_rules(self, rules: list[LearnedRule]) -> None:
        try:
            with open(self.rules_file, "w", encoding="utf-8") as f:
                dumpable = [r.model_dump() for r in rules]
                yaml.dump(dumpable, f, allow_unicode=True, indent=2)
        except Exception as e:
            logger.error("Failed to save learned rules: %s", e)

    def consolidate_session_learnings(self, findings: list[AIFinding]) -> list[LearnedRule]:
        existing_rules = self.load_learned_rules()
        existing_map = {r.rule_id: r for r in existing_rules}

        # Cluster systemic findings by category & subcategory
        category_clusters: dict[tuple[str, str], list[AIFinding]] = {}
        for f in findings:
            key = (f.category.value if hasattr(f.category, "value") else str(f.category), f.subcategory)
            category_clusters.setdefault(key, []).append(f)

        new_or_updated: list[LearnedRule] = []

        for (cat, subcat), cluster in category_clusters.items():
            rule_id = f"LEARNED_{cat.upper()}_{subcat.upper()}"
            sample_explanations = "; ".join([f.explanation_vi for f in cluster[:3]])
            sample_corrections = "; ".join([f.suggested_correction_vi for f in cluster if f.suggested_correction_vi][:2])

            if rule_id in existing_map:
                rule = existing_map[rule_id]
                rule.occurrences_count += len(cluster)
                if sample_corrections and sample_corrections not in rule.remediation_guideline_vi:
                    rule.remediation_guideline_vi += f" | Bổ sung: {sample_corrections}"
            else:
                rule = LearnedRule(
                    rule_id=rule_id,
                    category=cat,
                    pattern_description_vi=f"Mẫu lỗi hệ thống tự đúc kết cho {cat}/{subcat}: {sample_explanations}",
                    rule_type="style_rule" if cat in {"style", "fluency"} else "glossary",
                    remediation_guideline_vi=sample_corrections or "Kiểm tra kỹ đối chiếu song ngữ theo chuẩn đúc kết.",
                    occurrences_count=len(cluster),
                )
                existing_map[rule_id] = rule

            new_or_updated.append(existing_map[rule_id])

        final_rules = list(existing_map.values())
        self.save_learned_rules(final_rules)
        logger.info("Self-evolution complete: %d rules active in system knowledge base.", len(final_rules))
        return final_rules
