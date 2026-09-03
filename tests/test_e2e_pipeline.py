import zipfile
from pathlib import Path
from epub_translate_audit.config import Settings
from epub_translate_audit.orchestrator.orchestrator import AuditOrchestrator
from epub_translate_audit.reports.report_generator import ReportGenerator


def create_test_epub(file_path: Path, title: str, lang: str, chapter_text: str):
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


def test_full_e2e_pipeline(tmp_path: Path):
    project_dir = tmp_path / "project"
    vi_dir = project_dir / "vi"
    vi_dir.mkdir(parents=True)

    src_epub = project_dir / "source.epub"
    vi_epub = vi_dir / "translated_vi.epub"

    create_test_epub(src_epub, "Original Book", "en", "The quick brown fox jumps over the lazy dog.")
    create_test_epub(vi_epub, "Sách Dịch", "vi", "Con cáo nâu nhanh nhạy nhảy qua con chó lười biếng.")

    # Config
    settings = Settings.load()
    settings.audit.output_dir = str(tmp_path / "audit_output")
    settings.audit.cache_dir = str(tmp_path / ".cache")

    # Run Orchestrator
    orchestrator = AuditOrchestrator(settings)
    audit_res = orchestrator.run_audit(vi_epub)

    assert audit_res["release_decision"].status in ["PASS", "CONDITIONAL_PASS"]
    assert audit_res["total_target_words"] > 0

    # Generate Reports
    out_files = ReportGenerator.generate_all(settings.audit.output_dir, audit_res)
    assert out_files["html"].exists()
    assert out_files["xlsx_ledger"].exists()
