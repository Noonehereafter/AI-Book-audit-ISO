import zipfile
from pathlib import Path
from epub_translate_audit.ingest.epub_parser import EPUBParser, discover_source_epub
from epub_translate_audit.alignment.aligner import EPUBAligner


def create_dummy_epub(file_path: Path, title: str, lang: str, chapter_text: str):
    container_xml = """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
   <rootfiles>
      <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
   </rootfiles>
</container>"""

    content_opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="BookId">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>{title}</dc:title>
    <dc:language>{lang}</dc:language>
  </metadata>
  <manifest>
    <item id="ch1" href="ch1.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine>
    <itemref idref="ch1"/>
  </spine>
</package>"""

    ch1_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>{title}</title></head>
<body>
  <h1>{title}</h1>
  <p>{chapter_text}</p>
</body>
</html>"""

    with zipfile.ZipFile(file_path, "w") as z:
        z.writestr("META-INF/container.xml", container_xml)
        z.writestr("OEBPS/content.opf", content_opf)
        z.writestr("OEBPS/ch1.xhtml", ch1_xhtml)


def test_epub_parser_and_discovery(tmp_path: Path):
    parent = tmp_path / "book_project"
    vi_dir = parent / "vi"
    vi_dir.mkdir(parents=True)

    src_epub = parent / "source_book.epub"
    vi_epub = vi_dir / "translated_vi.epub"

    create_dummy_epub(src_epub, "Original Book", "en", "This is chapter one in English.")
    create_dummy_epub(vi_epub, "Sách Dịch", "vi", "Đây là chương một bằng tiếng Việt.")

    # Test auto discovery
    discovered_src = discover_source_epub(vi_epub)
    assert discovered_src == src_epub

    # Test parsing
    src_book = EPUBParser(src_epub).parse()
    vi_book = EPUBParser(vi_epub).parse()

    assert src_book.title == "Original Book"
    assert len(src_book.chapters) == 1
    assert src_book.chapters[0].blocks[0].text_normalized == "Original Book"
    assert src_book.chapters[0].blocks[1].text_normalized == "This is chapter one in English."

    # Test alignment
    aligner = EPUBAligner(src_book, vi_book)
    res = aligner.align()
    assert len(res.aligned_pairs) == 2
    assert res.aligned_pairs[1].source_text == "This is chapter one in English."
    assert res.aligned_pairs[1].target_text == "Đây là chương một bằng tiếng Việt."
