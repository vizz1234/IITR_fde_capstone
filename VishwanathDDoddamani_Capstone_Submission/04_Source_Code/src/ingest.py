"""
Ingest module: Normalizes support tickets from all four channels (Email, Live Chat, Docs Comment, Forum)
into a unified internal Ticket data structure.
"""

import uuid
from typing import Dict, Any, Union
from src.schema import Ticket, ChannelEnum, CustomerTierEnum


def normalize_ticket(data: Union[Dict[str, Any], str]) -> Ticket:
    """
    Accepts raw ticket dictionary or JSON payload and returns a normalized Ticket model.
    Handles missing fields, missing subjects, unusual characters, and channel mapping.
    """
    if isinstance(data, str):
        import json
        try:
            data = json.loads(data)
        except Exception:
            data = {"body": data}

    ticket_id = str(data.get("ticket_id") or f"TICK-{uuid.uuid4().hex[:8]}")

    # Determine channel
    raw_channel = str(data.get("channel", "email")).lower().strip()
    if raw_channel in ["chat", "live_chat"]:
        channel = ChannelEnum.CHAT
    elif raw_channel in ["docs_comment", "docs", "doc_comment"]:
        channel = ChannelEnum.DOCS_COMMENT
    elif raw_channel in ["forum", "community_forum"]:
        channel = ChannelEnum.FORUM
    else:
        channel = ChannelEnum.EMAIL

    # Normalize customer tier
    raw_tier = str(data.get("customer_tier", "standard")).lower().strip()
    if raw_tier in ["enterprise"]:
        customer_tier = CustomerTierEnum.ENTERPRISE
    elif raw_tier in ["business"]:
        customer_tier = CustomerTierEnum.BUSINESS
    else:
        customer_tier = CustomerTierEnum.STANDARD

    # Extract subject and body
    subject = str(data.get("subject", "") or "").strip()
    body = str(data.get("body", "") or "").strip()

    if not body and subject:
        body = subject
    elif not body:
        body = "[Empty Ticket Body]"

    customer_id = str(data.get("customer_id", "unknown_cust"))
    region = str(data.get("customer_region", "US"))
    language_fluency = str(data.get("language_fluency", "fluent"))
    timestamp = str(data.get("received_at") or data.get("timestamp") or "")

    labels = data.get("labels") or {}

    return Ticket(
        ticket_id=ticket_id,
        channel=channel,
        customer_id=customer_id,
        customer_tier=customer_tier,
        region=region,
        language_fluency=language_fluency,
        subject=subject,
        body=body,
        raw_payload=data,
        timestamp=timestamp,
        labels=labels
    )
