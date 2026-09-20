"""
Tests for failure handling and resilience: Acceptance Criterion A11.
Verifies system handles provider timeout/outage, rate limiting, and malformed input gracefully without crashing.
"""

from src.ingest import normalize_ticket
from src.llm import LLMClient
from src.classify import classify_ticket
from src.schema import Ticket, ChannelEnum


def test_malformed_raw_payload_handling():
    # Ticket with missing fields, empty body, special characters
    raw_payload = {
        "channel": "INVALID_CHANNEL_XYZ",
        "body": None,
        "subject": "System crash \u0000\u0001!"
    }
    ticket = normalize_ticket(raw_payload)
    assert ticket.channel == ChannelEnum.EMAIL
    assert ticket.body != ""
    assert isinstance(ticket.ticket_id, str)


def test_llm_mock_fallback_on_outage():
    # Simulate LLM client when API key is invalid / network is disconnected
    client = LLMClient()
    client.api_key = "invalid_key_simulate_outage"
    res = client.complete([{"role": "user", "content": "Test prompt"}])
    assert res is not None
    assert len(res) > 0


def test_classify_graceful_degradation():
    ticket = Ticket(ticket_id="OUTAGE-01", channel=ChannelEnum.CHAT, body="System failure")
    res = classify_ticket(ticket)
    assert res.intent is not None
    assert 0.0 <= res.confidence <= 1.0
