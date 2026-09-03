from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class LinguaGachaLine:
    line_number: int
    speaker_tag: str | None
    source_text: str
    translated_text: str | None
    placeholders: list[str] = field(default_factory=list)


@dataclass
class LinguaGachaFile:
    file_path: Path
    lines: list[LinguaGachaLine] = field(default_factory=list)


class LinguaGachaAdapter:
    """Parser & Adapter for LinguaGacha translation tool outputs (novel/game text files, placeholdered lines, speaker tags)."""

    # Matches LinguaGacha speaker tag syntax like [Speaker] or <speaker:Name> or Name: "Dialog"
    SPEAKER_PATTERN = re.compile(r"^(?:\[(.*?)\]|<speaker:(.*?)>|([A-Za-zÂĂĐÊÔƠƯâăđêôơưA-Z0-9\s]+):)\s*(.*)$")
    PLACEHOLDER_PATTERN = re.compile(r"(\{\d+\}|<ph_.*?/?>|\[ph_.*?\])")

    @classmethod
    def parse_file(cls, file_path: str | Path) -> LinguaGachaFile:
        path = Path(file_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"LinguaGacha output file not found: {path}")

        lines: list[LinguaGachaLine] = []
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for idx, raw_line in enumerate(f, 1):
                raw = raw_line.strip()
                if not raw:
                    continue

                speaker = None
                content = raw

                m = cls.SPEAKER_PATTERN.match(raw)
                if m:
                    speaker = m.group(1) or m.group(2) or m.group(3)
                    content = m.group(4) or raw

                placeholders = cls.PLACEHOLDER_PATTERN.findall(content)

                lines.append(
                    LinguaGachaLine(
                        line_number=idx,
                        speaker_tag=speaker,
                        source_text=content,
                        translated_text=content,  # In standalone output mode, content contains translated string
                        placeholders=placeholders,
                    )
                )

        return LinguaGachaFile(file_path=path, lines=lines)
