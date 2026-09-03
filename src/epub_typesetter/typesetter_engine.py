from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from bs4 import BeautifulSoup


@dataclass
class SemanticPatchItem:
    xpath: str
    target_tag: str
    class_name: str | None = None
    action: str = "update"  # "update", "wrap_drop_cap", "format_footnote"


@dataclass
class SemanticPatch:
    chapter_id: str
    items: list[SemanticPatchItem] = field(default_factory=list)


class EPUBTypesetterExtractor:
    """Extracts Semantic Intermediate Representation (IR) from XHTML for AI analysis."""

    @staticmethod
    def extract_ir(xhtml_content: str) -> list[dict[str, str]]:
        soup = BeautifulSoup(xhtml_content, "html.parser")
        ir_items = []
        tag_counters: dict[str, int] = {}

        for elem in soup.find_all(["h1", "h2", "h3", "h4", "p", "blockquote", "li", "div"]):
            text = elem.get_text().strip()
            if not text:
                continue

            tag_name = elem.name.lower()
            tag_counters[tag_name] = tag_counters.get(tag_name, 0) + 1
            xpath = f"//{tag_name}[{tag_counters[tag_name]}]"

            ir_items.append({
                "xpath": xpath,
                "current_tag": tag_name,
                "current_class": elem.get("class", []),
                "text": text[:200],  # Preview text for AI semantic classification
            })

        return ir_items


class EPUBTypesetterRenderer:
    """Applies AI JSON Semantic Patches deterministically onto XHTML DOM without modifying text content."""

    @staticmethod
    def apply_patch(xhtml_content: str, patch: SemanticPatch) -> str:
        soup = BeautifulSoup(xhtml_content, "html.parser")

        tag_counters: dict[str, int] = {}
        node_map: dict[str, Any] = {}

        for elem in soup.find_all(["h1", "h2", "h3", "h4", "p", "blockquote", "li", "div"]):
            text = elem.get_text().strip()
            if not text:
                continue
            tag_name = elem.name.lower()
            tag_counters[tag_name] = tag_counters.get(tag_name, 0) + 1
            xpath = f"//{tag_name}[{tag_counters[tag_name]}]"
            node_map[xpath] = elem

        for item in patch.items:
            elem = node_map.get(item.xpath)
            if not elem:
                continue

            if item.target_tag and elem.name != item.target_tag:
                elem.name = item.target_tag

            if item.class_name:
                classes = elem.get("class", [])
                if isinstance(classes, str):
                    classes = [classes]
                if item.class_name not in classes:
                    classes.append(item.class_name)
                elem["class"] = classes

            if item.action == "wrap_drop_cap" and elem.string:
                raw_text = elem.string.strip()
                if raw_text:
                    first_char = raw_text[0]
                    rest = raw_text[1:]
                    elem.clear()
                    span = soup.new_tag("span", attrs={"class": "drop-cap"})
                    span.string = first_char
                    elem.append(span)
                    elem.append(rest)

        return str(soup)
