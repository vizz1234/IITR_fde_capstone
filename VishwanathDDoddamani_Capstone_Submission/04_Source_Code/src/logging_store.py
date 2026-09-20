"""
Logging Store Module: SQLite database manager recording all automated system decisions
for auditability, compliance, and metrics reconciliation.
"""

import os
import json
import sqlite3
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from src.schema import DecisionRecord


class DecisionLogger:
    def __init__(self, db_path: str = "./storage/decisions.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Initializes decision log database schema."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS decisions (
                    decision_id     TEXT PRIMARY KEY,
                    created_at      TEXT NOT NULL,
                    ticket_id       TEXT NOT NULL,
                    stage           TEXT NOT NULL,
                    prediction      TEXT,
                    confidence      REAL,
                    threshold       REAL,
                    action_taken    TEXT NOT NULL,
                    reason          TEXT NOT NULL,
                    sources_used    TEXT,
                    guardrails      TEXT,
                    prompt_version  TEXT,
                    requirement_ids TEXT
                )
            """)
            conn.commit()

    def log_decision(
        self,
        ticket_id: str,
        stage: str,
        action_taken: str,
        reason: str,
        prediction: Optional[str] = None,
        confidence: Optional[float] = None,
        threshold: Optional[float] = None,
        sources_used: Optional[List[str]] = None,
        guardrails: Optional[Dict[str, Any]] = None,
        prompt_version: str = "v1.0",
        requirement_ids: Optional[str] = "F1,F3,F5,F7"
    ) -> DecisionRecord:
        """Logs a single automated decision record to the SQLite database."""
        decision_id = f"DEC-{uuid.uuid4().hex[:10]}"
        created_at = datetime.utcnow().isoformat()

        sources_json = json.dumps(sources_used) if sources_used else None
        guardrails_json = json.dumps(guardrails) if guardrails else None

        record = DecisionRecord(
            decision_id=decision_id,
            created_at=created_at,
            ticket_id=ticket_id,
            stage=stage,
            prediction=prediction,
            confidence=confidence,
            threshold=threshold,
            action_taken=action_taken,
            reason=reason,
            sources_used=sources_json,
            guardrails=guardrails_json,
            prompt_version=prompt_version,
            requirement_ids=requirement_ids
        )

        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO decisions (
                    decision_id, created_at, ticket_id, stage, prediction,
                    confidence, threshold, action_taken, reason, sources_used,
                    guardrails, prompt_version, requirement_ids
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record.decision_id, record.created_at, record.ticket_id, record.stage,
                record.prediction, record.confidence, record.threshold, record.action_taken,
                record.reason, record.sources_used, record.guardrails, record.prompt_version,
                record.requirement_ids
            ))
            conn.commit()

        return record

    def get_records_by_ticket(self, ticket_id: str) -> List[Dict[str, Any]]:
        """Retrieves decision records for a given ticket ID."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM decisions WHERE ticket_id = ? ORDER BY created_at ASC", (ticket_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_all_records(self) -> List[Dict[str, Any]]:
        """Retrieves all logged decision records."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM decisions ORDER BY created_at ASC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]


# Lazy singleton instance
_logger_instance: Optional[DecisionLogger] = None


def get_logger() -> DecisionLogger:
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = DecisionLogger()
    return _logger_instance
