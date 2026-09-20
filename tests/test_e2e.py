"""
End-to-End Pipeline & Evaluation Harness Test: Acceptance Criteria A9 & A12.
Verifies full pipeline processes tickets unattended and pytest test suite executes cleanly.
"""

import os
import json
from evaluation.harness import run_evaluation


def test_unattended_evaluation_run_sample(tmp_path):
    # Create sample validation ticket file
    sample_tickets = [
        {
            "ticket_id": "VAL-TEST-001",
            "channel": "chat",
            "subject": "Deployment rollback question",
            "body": "How do I trigger an automatic rollback when health checks fail?",
            "customer_tier": "standard",
            "labels": {"intent": "rollback_request", "urgency": "medium"}
        },
        {
            "ticket_id": "VAL-TEST-002",
            "channel": "email",
            "subject": "Security audit logs request",
            "body": "Our compliance team needs security logs for Q2.",
            "customer_tier": "enterprise",
            "labels": {"intent": "compliance_request", "urgency": "high"}
        }
    ]

    input_file = os.path.join(tmp_path, "sample_val_tickets.json")
    output_dir = os.path.join(tmp_path, "results")

    with open(input_file, "w", encoding="utf-8") as f:
        json.dump(sample_tickets, f)

    run_evaluation(input_file, output_dir)

    metrics_file = os.path.join(output_dir, "metrics_report.json")
    assert os.path.exists(metrics_file)

    with open(metrics_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["volume"]["total_tickets_processed"] == 2
    assert "business_outcomes" in data
    assert "technical_performance" in data
    assert "governance" in data
