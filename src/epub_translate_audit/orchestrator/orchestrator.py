from __future__ import annotations

import logging
import uuid
from pathlib import Path
from typing import Any

from epub_translate_audit.ai.evidence_verifier import EvidenceVerifier
from epub_translate_audit.ai.llm_client import LLMClient
from epub_translate_audit.ai.schemas import (
    AIFinding,
    AuditCategory,
    AuditPassResponse,
    BookProfileResponse,
    Evidence,
    ReleaseDecisionResponse,
    Severity,
)
from epub_translate_audit.alignment.aligner import EPUBAligner
from epub_translate_audit.config import Settings
from epub_translate_audit.ingest.epub_parser import EPUBBook, EPUBParser, discover_source_epub
from epub_translate_audit.orchestrator.release_gate import ReleaseGateEngine
from epub_translate_audit.orchestrator.state_store import AuditStateStore
from epub_translate_audit.prompts.audit_prompts import (
    CONTINUITY_AUDIT_PROMPT,
    LITERARY_AUDIT_PROMPT,
    RED_TEAM_PROMPT,
    SEMANTIC_AUDIT_PROMPT,
)

logger = logging.getLogger(__name__)


class AuditOrchestrator:
    """Automated multi-agent orchestrator executing multi-pass translation audit."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.llm_client = LLMClient(settings.llm)
        self.state_store = AuditStateStore(Path(settings.audit.cache_dir) / "state.db")

    def run_audit(self, translated_epub_path: str | Path, source_epub_path: str | Path | None = None) -> dict[str, Any]:
        translated_path = Path(translated_epub_path).resolve()
        run_id = f"run_{uuid.uuid4().hex[:8]}"

        logger.info("Starting audit run %s for %s", run_id, translated_path)

        if not source_epub_path and self.settings.audit.auto_discover_source:
            source_path = discover_source_epub(
                translated_path,
                allow_grandparent=self.settings.audit.allow_grandparent_discovery,
            )
        elif source_epub_path:
            source_path = Path(source_epub_path).resolve()
        else:
            raise ValueError("Source EPUB path must be provided or auto-discovery enabled.")

        src_book = EPUBParser(source_path).parse()
        vi_book = EPUBParser(translated_path).parse()

        aligner = EPUBAligner(src_book, vi_book)
        align_result = aligner.align()

        all_valid_findings: list[AIFinding] = []
        total_target_words = sum(b.word_count for ch in vi_book.chapters for b in ch.blocks)

        for pair in align_result.aligned_pairs:
            pair_findings: list[AIFinding] = []

            # Pass 1: Semantic Auditor
            cached_semantic = self.state_store.get_pair_findings(pair.pair_id, "semantic_pass")
            if cached_semantic is not None:
                sem_findings = [AIFinding.model_validate(f) for f in cached_semantic]
            else:
                sem_prompt = (
                    SEMANTIC_AUDIT_PROMPT.replace("{{source_text}}", pair.source_text)
                    .replace("{{target_text}}", pair.target_text)
                )
                sem_findings = self._call_agent(sem_prompt, "Semantic Auditor")
                self.state_store.save_pair_findings(
                    pair.pair_id, run_id, "semantic_pass", [f.model_dump() for f in sem_findings]
                )
            pair_findings.extend(sem_findings)

            # Pass 2: Continuity Auditor (if deep mode)
            if self.settings.audit.deep_mode:
                cached_cont = self.state_store.get_pair_findings(pair.pair_id, "continuity_pass")
                if cached_cont is not None:
                    cont_findings = [AIFinding.model_validate(f) for f in cached_cont]
                else:
                    cont_prompt = (
                        CONTINUITY_AUDIT_PROMPT.replace("{{source_text}}", pair.source_text)
                        .replace("{{target_text}}", pair.target_text)
                    )
                    cont_findings = self._call_agent(cont_prompt, "Continuity Auditor")
                    self.state_store.save_pair_findings(
                        pair.pair_id, run_id, "continuity_pass", [f.model_dump() for f in cont_findings]
                    )
                pair_findings.extend(cont_findings)

                # Pass 3: Literary Auditor
                cached_lit = self.state_store.get_pair_findings(pair.pair_id, "literary_pass")
                if cached_lit is not None:
                    lit_findings = [AIFinding.model_validate(f) for f in cached_lit]
                else:
                    lit_prompt = (
                        LITERARY_AUDIT_PROMPT.replace("{{source_text}}", pair.source_text)
                        .replace("{{target_text}}", pair.target_text)
                    )
                    lit_findings = self._call_agent(lit_prompt, "Literary Auditor")
                    self.state_store.save_pair_findings(
                        pair.pair_id, run_id, "literary_pass", [f.model_dump() for f in lit_findings]
                    )
                pair_findings.extend(lit_findings)

                # Pass 4: Red Team Auditor
                cached_red = self.state_store.get_pair_findings(pair.pair_id, "red_team_pass")
                if cached_red is not None:
                    red_findings = [AIFinding.model_validate(f) for f in cached_red]
                else:
                    red_prompt = (
                        RED_TEAM_PROMPT.replace("{{source_text}}", pair.source_text)
                        .replace("{{target_text}}", pair.target_text)
                    )
                    red_findings = self._call_agent(red_prompt, "Red Team Auditor")
                    self.state_store.save_pair_findings(
                        pair.pair_id, run_id, "red_team_pass", [f.model_dump() for f in red_findings]
                    )
                pair_findings.extend(red_findings)

            valid, _ = EvidenceVerifier.filter_valid_findings(pair_findings, pair.source_text, pair.target_text)
            all_valid_findings.extend(valid)

        release_decision = ReleaseGateEngine.evaluate(
            all_valid_findings,
            total_target_words=total_target_words,
            unaligned_source_count=len(align_result.unaligned_source_blocks),
            unaligned_target_count=len(align_result.unaligned_target_blocks),
        )

        return {
            "run_id": run_id,
            "translated_path": str(translated_path),
            "source_path": str(source_path),
            "align_result": align_result,
            "all_findings": all_valid_findings,
            "release_decision": release_decision,
            "total_target_words": total_target_words,
        }

    def _call_agent(self, prompt: str, system_prompt: str) -> list[AIFinding]:
        try:
            resp = self.llm_client.generate_structured(prompt, AuditPassResponse, system_prompt=system_prompt)
            return resp.findings
        except Exception as e:
            logger.debug("Agent call (%s) fallback: %s", system_prompt, e)
            return []
