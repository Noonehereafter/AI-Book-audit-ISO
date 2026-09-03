from __future__ import annotations

from dataclasses import dataclass, field
from rapidfuzz import fuzz
from epub_translate_audit.ingest.epub_parser import EPUBBook, EPUBChapter, EPUBBlock


@dataclass
class AlignedPair:
    pair_id: str
    source_chapter_id: str
    target_chapter_id: str
    source_block_ids: list[str]
    target_block_ids: list[str]
    source_text: str
    target_text: str
    confidence: float
    alignment_type: str  # "1:1", "1:2", "2:1", "1:0", "0:1"


@dataclass
class AlignmentResult:
    aligned_pairs: list[AlignedPair] = field(default_factory=list)
    unaligned_source_blocks: list[str] = field(default_factory=list)
    unaligned_target_blocks: list[str] = field(default_factory=list)
    overall_confidence: float = 1.0


class EPUBAligner:
    """Aligns source and target EPUB books at chapter and block levels using structure & rapidfuzz text matching."""

    def __init__(self, source_book: EPUBBook, target_book: EPUBBook) -> None:
        self.source_book = source_book
        self.target_book = target_book

    def align(self) -> AlignmentResult:
        result = AlignmentResult()
        chapter_pairs: list[tuple[EPUBChapter, EPUBChapter]] = []

        src_chapters = self.source_book.chapters
        tgt_chapters = self.target_book.chapters

        min_len = min(len(src_chapters), len(tgt_chapters))
        for i in range(min_len):
            chapter_pairs.append((src_chapters[i], tgt_chapters[i]))

        pair_counter = 0

        for src_ch, tgt_ch in chapter_pairs:
            src_blocks = src_ch.blocks
            tgt_blocks = tgt_ch.blocks

            s_idx = 0
            t_idx = 0

            while s_idx < len(src_blocks) and t_idx < len(tgt_blocks):
                sb = src_blocks[s_idx]
                tb = tgt_blocks[t_idx]

                pair_id = f"pair_{pair_counter:04d}"
                pair_counter += 1

                # Calculate similarity with rapidfuzz token ratio
                sim = fuzz.token_sort_ratio(sb.text_normalized, tb.text_normalized) / 100.0
                confidence = round(0.5 + 0.5 * sim, 2)

                aligned = AlignedPair(
                    pair_id=pair_id,
                    source_chapter_id=src_ch.chapter_id,
                    target_chapter_id=tgt_ch.chapter_id,
                    source_block_ids=[sb.block_id],
                    target_block_ids=[tb.block_id],
                    source_text=sb.text_normalized,
                    target_text=tb.text_normalized,
                    confidence=confidence,
                    alignment_type="1:1",
                )
                result.aligned_pairs.append(aligned)

                s_idx += 1
                t_idx += 1

            while s_idx < len(src_blocks):
                result.unaligned_source_blocks.append(src_blocks[s_idx].block_id)
                s_idx += 1

            while t_idx < len(tgt_blocks):
                result.unaligned_target_blocks.append(tgt_blocks[t_idx].block_id)
                t_idx += 1

        return result
