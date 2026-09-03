import zipfile
from pathlib import Path
from epub_translate_audit.ingest.epub_parser import EPUBParser
from epub_typesetter.typesetter_engine import EPUBTypesetterRenderer, SemanticPatch, SemanticPatchItem


def test_epub_parser_image_only_block(tmp_path: Path):
    epub_file = tmp_path / "img_test.epub"

    container_xml = """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
   <rootfiles>
      <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
   </rootfiles>
</container>"""

    content_opf = """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="BookId">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>Image Test</dc:title>
    <dc:language>vi</dc:language>
  </metadata>
  <manifest>
    <item id="ch1" href="ch1.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine>
    <itemref idref="ch1"/>
  </spine>
</package>"""

    ch1_xhtml = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>Test</title></head>
<body>
  <h1>Chương 1</h1>
  <p><img src="cover.jpg" alt="Bìa Sách"/></p>
  <p>Văn bản tiếp theo.</p>
</body>
</html>"""

    with zipfile.ZipFile(epub_file, "w") as z:
        z.writestr("META-INF/container.xml", container_xml)
        z.writestr("OEBPS/content.opf", content_opf)
        z.writestr("OEBPS/ch1.xhtml", ch1_xhtml)

    book = EPUBParser(epub_file).parse()
    blocks = book.chapters[0].blocks
    assert any(b.kind == "image_only" for b in blocks)


def test_drop_cap_with_opening_quote():
    xhtml = """<html><body><p>“Ngày xửa ngày xưa...”</p></body></html>"""
    patch = SemanticPatch(
        chapter_id="ch1",
        items=[SemanticPatchItem(xpath="//p[1]", target_tag="p", class_name="no-indent", action="wrap_drop_cap")]
    )
    rendered = EPUBTypesetterRenderer.apply_patch(xhtml, patch)
    assert '<span class="drop-cap">“N</span>gày xửa' in rendered
