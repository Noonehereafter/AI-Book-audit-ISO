from pathlib import Path
from epub_typesetter.typesetter_engine import EPUBTypesetterExtractor, EPUBTypesetterRenderer, SemanticPatch, SemanticPatchItem


def test_typesetter_extract_and_render():
    xhtml = """<?xml version="1.0" encoding="utf-8"?>
<html>
<body>
  <p>Chương 1: Khởi Đầu</p>
  <p>Ngày xửa ngày xưa ở một vương quốc xa xôi...</p>
  <p>* * *</p>
</body>
</html>"""

    # 1. Extract IR
    ir = EPUBTypesetterExtractor.extract_ir(xhtml)
    assert len(ir) == 3
    assert ir[0]["xpath"] == "//p[1]"
    assert ir[1]["xpath"] == "//p[2]"

    # 2. Apply Semantic Patch
    patch = SemanticPatch(
        chapter_id="ch1",
        items=[
            SemanticPatchItem(xpath="//p[1]", target_tag="h1", class_name="chapter-title"),
            SemanticPatchItem(xpath="//p[2]", target_tag="p", class_name="no-indent", action="wrap_drop_cap"),
            SemanticPatchItem(xpath="//p[3]", target_tag="div", class_name="scene-break"),
        ]
    )

    rendered = EPUBTypesetterRenderer.apply_patch(xhtml, patch)
    assert '<h1 class="chapter-title">' in rendered
    assert '<span class="drop-cap">N</span>gày xửa' in rendered
    assert '<div class="scene-break">' in rendered
