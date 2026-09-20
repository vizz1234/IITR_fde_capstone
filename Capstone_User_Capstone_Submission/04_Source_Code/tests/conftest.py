"""
Pytest configuration and shared test fixtures.
"""

import os
import pytest
from src.schema import Ticket, ChannelEnum, CustomerTierEnum


@pytest.fixture
def sample_chat_ticket():
    return Ticket(
        ticket_id="TEST-CHAT-01",
        channel=ChannelEnum.CHAT,
        customer_id="CUST-101",
        customer_tier=CustomerTierEnum.STANDARD,
        subject="",
        body="Our deployments keep failing during container health check verification.",
        labels={"intent": "deployment_failure", "urgency": "high"}
    )


@pytest.fixture
def sample_email_ticket():
    return Ticket(
        ticket_id="TEST-EMAIL-01",
        channel=ChannelEnum.EMAIL,
        customer_id="CUST-202",
        customer_tier=CustomerTierEnum.ENTERPRISE,
        subject="Monthly Invoice Question",
        body="Why is our monthly invoice higher than expected for enterprise tier?",
        labels={"intent": "billing_query", "urgency": "medium"}
    )


@pytest.fixture
def sample_docs_ticket():
    return Ticket(
        ticket_id="TEST-DOCS-01",
        channel=ChannelEnum.DOCS_COMMENT,
        customer_id="CUST-303",
        customer_tier=CustomerTierEnum.BUSINESS,
        subject="API Pagination Clarification",
        body="Does the list endpoints API support cursor-based pagination?",
        labels={"intent": "api_usage_question", "urgency": "low"}
    )


@pytest.fixture
def sample_forum_ticket():
    return Ticket(
        ticket_id="TEST-FORUM-01",
        channel=ChannelEnum.FORUM,
        customer_id="CUST-404",
        customer_tier=CustomerTierEnum.STANDARD,
        subject="Group Permissions Issue",
        body="A user cannot access a project even after being added to the team.",
        labels={"intent": "account_access", "urgency": "medium"}
    )
