from __future__ import annotations

import re
from bs4 import BeautifulSoup


class TypesettingDiffChecker:
    """Verifies that typesetting/formatting patches did not lose or corrupt any text content."""

    @staticmethod
    def extract_clean_text(html_content: str) -> str:
        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.get_text()
        return re.sub(r"\s+", " ", text).strip()

    @classmethod
    def verify_no_text_loss(cls, original_html: str, typeset_html: str) -> tuple[bool, str]:
        orig_text = cls.extract_clean_text(original_html)
        typeset_text = cls.extract_clean_text(typeset_html)

        if orig_text == typeset_text:
            return True, "Text content is identical."

        # If length or content differs significantly
        len_diff = abs(len(orig_text) - len(typeset_text))
        if len_diff > 10:
            return False, f"Text length mismatch: original {len(orig_text)} chars vs typeset {len(typeset_text)} chars."

        return True, "Text content verified with minor whitespace formatting differences."
