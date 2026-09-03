from epub_typesetter.diff_checker import TypesettingDiffChecker


def test_diff_checker():
    orig_html = "<h1>Chương 1</h1><p>Nội dung câu chuyện bắt đầu ở đây.</p>"
    typeset_html = "<h1 class='chapter-title'>Chương 1</h1><p class='no-indent'><span class='drop-cap'>N</span>ội dung câu chuyện bắt đầu ở đây.</p>"

    ok, msg = TypesettingDiffChecker.verify_no_text_loss(orig_html, typeset_html)
    assert ok is True
    assert "identical" in msg or "verified" in msg
