from __future__ import annotations

import os
import re
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal
from bs4 import BeautifulSoup


@dataclass
class EPUBBlock:
    block_id: str
    chapter_id: str
    spine_index: int
    xhtml_path: str
    xpath: str
    kind: Literal["heading", "paragraph", "blockquote", "verse", "list_item", "table_cell", "note", "other"]
    text_raw: str
    text_normalized: str
    char_count: int
    word_count: int


@dataclass
class EPUBChapter:
    chapter_id: str
    spine_index: int
    title: str
    xhtml_path: str
    blocks: list[EPUBBlock] = field(default_factory=list)


@dataclass
class EPUBBook:
    book_path: Path
    title: str
    language: str
    chapters: list[EPUBChapter] = field(default_factory=list)


def normalize_text(text: str) -> str:
    """Normalize text: Unicode NFC, whitespace collapse."""
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text).strip()
    return text


class EPUBParser:
    """Extract chapters and blocks from an EPUB file preserving reading order according to OPF spine."""

    def __init__(self, epub_path: str | Path) -> None:
        self.epub_path = Path(epub_path).resolve()
        if not self.epub_path.exists():
            raise FileNotFoundError(f"EPUB file not found: {self.epub_path}")

    def parse(self) -> EPUBBook:
        with zipfile.ZipFile(self.epub_path, "r") as z:
            container_bytes = z.read("META-INF/container.xml")
            container_soup = BeautifulSoup(container_bytes, "xml")
            rootfile_tag = container_soup.find("rootfile")
            if not rootfile_tag or not rootfile_tag.get("full-path"):
                raise ValueError("Invalid EPUB: META-INF/container.xml missing rootfile")

            opf_path = str(rootfile_tag["full-path"])
            opf_dir = os.path.dirname(opf_path)

            opf_bytes = z.read(opf_path)
            opf_soup = BeautifulSoup(opf_bytes, "xml")

            title_tag = opf_soup.find("dc:title") or opf_soup.find("title")
            title = title_tag.get_text().strip() if title_tag else self.epub_path.stem

            lang_tag = opf_soup.find("dc:language") or opf_soup.find("language")
            language = lang_tag.get_text().strip() if lang_tag else "unknown"

            manifest: dict[str, str] = {}
            manifest_tag = opf_soup.find("manifest")
            if manifest_tag:
                for item in manifest_tag.find_all("item"):
                    item_id = item.get("id")
                    href = item.get("href")
                    if item_id and href:
                        full_href = os.path.join(opf_dir, href).replace("\\", "/") if opf_dir else href
                        manifest[item_id] = full_href

            spine_ids: list[str] = []
            spine_tag = opf_soup.find("spine")
            if spine_tag:
                for itemref in spine_tag.find_all("itemref"):
                    idref = itemref.get("idref")
                    if idref and idref in manifest:
                        spine_ids.append(manifest[idref])

            chapters: list[EPUBChapter] = []

            for idx, xhtml_rel_path in enumerate(spine_ids):
                try:
                    xhtml_bytes = z.read(xhtml_rel_path)
                except KeyError:
                    continue

                html_soup = BeautifulSoup(xhtml_bytes, "html.parser")
                chapter_id = f"ch_{idx:03d}"

                h_tag = html_soup.find(["h1", "h2", "h3"])
                ch_title = h_tag.get_text().strip() if h_tag else f"Chapter {idx + 1}"

                chapter = EPUBChapter(
                    chapter_id=chapter_id,
                    spine_index=idx,
                    title=ch_title,
                    xhtml_path=xhtml_rel_path,
                )

                tag_counters: dict[str, int] = {}
                block_counter = 0

                for elem in html_soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "blockquote", "li"]):
                    raw_text = elem.get_text()
                    norm_text = normalize_text(raw_text)
                    if not norm_text:
                        continue

                    tag_name = elem.name.lower()
                    tag_counters[tag_name] = tag_counters.get(tag_name, 0) + 1
                    xpath = f"//{tag_name}[{tag_counters[tag_name]}]"

                    if tag_name.startswith("h"):
                        kind = "heading"
                    elif tag_name == "blockquote":
                        kind = "blockquote"
                    elif tag_name == "li":
                        kind = "list_item"
                    else:
                        kind = "paragraph"

                    block_id = f"{chapter_id}.b_{block_counter:03d}"
                    words = len(norm_text.split())

                    block = EPUBBlock(
                        block_id=block_id,
                        chapter_id=chapter_id,
                        spine_index=idx,
                        xhtml_path=xhtml_rel_path,
                        xpath=xpath,
                        kind=kind,
                        text_raw=raw_text,
                        text_normalized=norm_text,
                        char_count=len(norm_text),
                        word_count=words,
                    )
                    chapter.blocks.append(block)
                    block_counter += 1

                if chapter.blocks:
                    chapters.append(chapter)

            return EPUBBook(
                book_path=self.epub_path,
                title=title,
                language=language,
                chapters=chapters,
            )


def discover_source_epub(translated_epub_path: str | Path, allow_grandparent: bool = True) -> Path:
    translated_path = Path(translated_epub_path).resolve()
    parent_dir = translated_path.parent
    candidates: list[Path] = []

    for f in parent_dir.glob("*.epub"):
        if f.resolve() != translated_path:
            candidates.append(f)

    if not candidates and allow_grandparent and parent_dir.parent != parent_dir:
        for f in parent_dir.parent.glob("*.epub"):
            if f.resolve() != translated_path and f.parent != parent_dir:
                candidates.append(f)

    if not candidates:
        raise FileNotFoundError(
            f"Could not automatically discover source EPUB in parent ({parent_dir}) or grandparent directory."
        )

    if len(candidates) > 1:
        non_vi_candidates = [
            c for c in candidates if not any(kw in c.stem.lower() for kw in ["_vi", "_vn", "dich", "translated"])
        ]
        if len(non_vi_candidates) == 1:
            return non_vi_candidates[0]

    return candidates[0]
