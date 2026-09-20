"""
Tests for classify module: Acceptance Criterion A3.
Verifies tickets are classified for intent and urgency with a numeric confidence score [0.0, 1.0].
"""

from src.classify import classify_ticket
from src.schema import Ticket, ChannelEnum, UrgencyEnum


def test_classify_deployment_failure(sample_chat_ticket):
    res = classify_ticket(sample_chat_ticket)
    assert res.intent in ["deployment_failure", "configuration_help", "unclear_request"]
    assert isinstance(res.confidence, float)
    assert 0.0 <= res.confidence <= 1.0
    assert isinstance(res.urgency, UrgencyEnum)


def test_classify_billing_query(sample_email_ticket):
    res = classify_ticket(sample_email_ticket)
    assert isinstance(res.confidence, float)
    assert 0.0 <= res.confidence <= 1.0


def test_classify_fallback_handling():
    malformed_ticket = Ticket(
        ticket_id="TEST-MALFORMED",
        channel=ChannelEnum.EMAIL,
        body="x"
    )
    res = classify_ticket(malformed_ticket)
    assert 0.0 <= res.confidence <= 1.0
    assert res.intent is not None
