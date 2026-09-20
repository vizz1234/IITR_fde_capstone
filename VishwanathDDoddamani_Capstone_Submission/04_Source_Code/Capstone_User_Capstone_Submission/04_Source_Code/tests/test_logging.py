"""
Tests for logging module: Acceptance Criterion A8.
Verifies every automated decision is written to persistent SQLite log with required fields.
"""

import os
import sqlite3
from src.logging_store import DecisionLogger


def test_decision_logger_persistence(tmp_path):
    db_file = os.path.join(tmp_path, "test_decisions.db")
    logger = DecisionLogger(db_path=db_file)

    rec = logger.log_decision(
        ticket_id="TICK-LOG-TEST-01",
        stage="ROUTE",
        prediction="deployment_failure",
        confidence=0.88,
        threshold=0.80,
        action_taken="AUTO_ANSWER",
        reason="Confidence score above threshold",
        sources_used=["DOC-DEPLOY-001"],
        guardrails={"status": "passed"}
    )

    assert rec.decision_id.startswith("DEC-")

    # Re-open database file independently to verify SQLite persistence
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM decisions WHERE ticket_id = ?", ("TICK-LOG-TEST-01",))
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert row["ticket_id"] == "TICK-LOG-TEST-01"
    assert row["action_taken"] == "AUTO_ANSWER"
    assert row["prediction"] == "deployment_failure"
    assert float(row["confidence"]) == 0.88
