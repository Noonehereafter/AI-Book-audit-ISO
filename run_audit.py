#!/usr/bin/env python3
"""Main Entrypoint for Automated EPUB Translation Audit.

User simply runs:
    python run_audit.py <path_to_translated_epub>
"""

from __future__ import annotations

import sys
from pathlib import Path
from epub_translate_audit.config import Settings
from epub_translate_audit.orchestrator.orchestrator import AuditOrchestrator
from epub_translate_audit.reports.report_generator import ReportGenerator


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python run_audit.py <path_to_translated_epub> [path_to_source_epub]")
        sys.exit(1)

    translated_epub_path = Path(sys.argv[1])
    source_epub_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    print(f"🚀 Initializing Audit for: {translated_epub_path.name}")

    # Load Settings
    settings = Settings.load()

    # Initialize Orchestrator & Run Audit
    orchestrator = AuditOrchestrator(settings)
    audit_result = orchestrator.run_audit(translated_epub_path, source_epub_path)

    # Generate Reports
    out_dir = Path(settings.audit.output_dir)
    generated_files = ReportGenerator.generate_all(out_dir, audit_result)

    print("\n✅ Audit Completed Successfully!")
    print(f"📊 Status: {audit_result['release_decision'].status}")
    print(f"📁 Reports saved in: {out_dir.resolve()}")
    for k, v in generated_files.items():
        print(f"  - {k}: {v.name}")


if __name__ == "__main__":
    main()
