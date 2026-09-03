from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any
import json


class AuditStateStore:
    """SQLite-backed state store for caching audit progress and checkpoints."""

    def __init__(self, db_path: Path | str) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_runs (
                    run_id TEXT PRIMARY KEY,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS pair_results (
                    pair_id TEXT PRIMARY KEY,
                    run_id TEXT,
                    pass_name TEXT,
                    status TEXT,
                    findings_json TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save_run(self, run_id: str, status: str, data: dict[str, Any]) -> None:
        with self._get_conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO audit_runs (run_id, status, data) VALUES (?, ?, ?)",
                (run_id, status, json.dumps(data, ensure_ascii=False)),
            )
            conn.commit()

    def save_pair_findings(self, pair_id: str, run_id: str, pass_name: str, findings: list[dict[str, Any]]) -> None:
        with self._get_conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO pair_results (pair_id, run_id, pass_name, status, findings_json) VALUES (?, ?, ?, ?, ?)",
                (pair_id, run_id, pass_name, "COMPLETED", json.dumps(findings, ensure_ascii=False)),
            )
            conn.commit()

    def get_pair_findings(self, pair_id: str, pass_name: str) -> list[dict[str, Any]] | None:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT findings_json FROM pair_results WHERE pair_id = ? AND pass_name = ?",
                (pair_id, pass_name),
            )
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
            return None
