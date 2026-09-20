"""
Tests for ingest module: Acceptance Criterion A2.
Verifies tickets from all 4 channels (Email, Live Chat, Docs Comment, Forum) are ingested and normalized.
"""

from src.ingest import normalize_ticket
from src.schema import ChannelEnum, CustomerTierEnum


def test_ingest_email_ticket():
    data = {
        "ticket_id": "TCK-EMAIL-1",
        "channel": "email",
        "subject": "System downtime inquiry",
        "body": "We are experiencing service interruptions on our US instance.",
        "customer_tier": "enterprise"
    }
    ticket = normalize_ticket(data)
    assert ticket.ticket_id == "TCK-EMAIL-1"
    assert ticket.channel == ChannelEnum.EMAIL
    assert ticket.customer_tier == CustomerTierEnum.ENTERPRISE
    assert ticket.subject == "System downtime inquiry"


def test_ingest_chat_ticket():
    data = {
        "ticket_id": "TCK-CHAT-1",
        "channel": "chat",
        "body": "Where do I configure webhooks for deployment events?",
        "customer_tier": "standard"
    }
    ticket = normalize_ticket(data)
    assert ticket.channel == ChannelEnum.CHAT
    assert ticket.subject == ""
    assert "webhooks" in ticket.body


def test_ingest_docs_comment_ticket():
    data = {
        "ticket_id": "TCK-DOCS-1",
        "channel": "docs_comment",
        "subject": "Missing parameter in API docs",
        "body": "The filter parameter is omitted in the API table."
    }
    ticket = normalize_ticket(data)
    assert ticket.channel == ChannelEnum.DOCS_COMMENT


def test_ingest_forum_ticket():
    data = {
        "ticket_id": "TCK-FORUM-1",
        "channel": "forum",
        "subject": "Community help on SSO integration",
        "body": "How do we map Okta groups to CloudServe roles?"
    }
    ticket = normalize_ticket(data)
    assert ticket.channel == ChannelEnum.FORUM
