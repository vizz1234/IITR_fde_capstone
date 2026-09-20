"""
Routing Module: Implements deterministic routing decisions (Auto-Answer vs Escalate),
threshold evaluation, and escalation payload creation.
"""

import os
from typing import List, Tuple
from src.schema import Ticket, ClassificationResult, PassageSource, RoutingAction, EscalationPayload


def route_ticket(
    ticket: Ticket,
    classification: ClassificationResult,
    sources: List[PassageSource],
    custom_threshold: float = None
) -> Tuple[RoutingAction, str, EscalationPayload]:
    """
    Decides whether to answer automatically or escalate to Tier 2 support.
    Deterministic: identical inputs guarantee identical routing outcomes.
    
    Rules for escalation:
    1. Mandatory escalation intents: security_incident, compliance_request, feature_request, data_residency.
    2. Must-not-auto-respond flag in ticket labels.
    3. Classification confidence below threshold (default 0.80).
    4. No relevant documentation retrieved (sources list empty).
    """
    threshold = custom_threshold if custom_threshold is not None else float(os.getenv("CONFIDENCE_THRESHOLD", "0.80"))

    intent = classification.intent.lower()
    confidence = classification.confidence

    # Mandatory escalation categories
    mandatory_escalate_intents = [
        "security_incident",
        "compliance_request",
        "feature_request",
        "data_residency",
        "rollback_request"
    ]

    # Check ticket labels
    must_not_auto = ticket.labels.get("must_not_auto_respond", False)

    # Escalation reason evaluation
    reasons = []

    if must_not_auto:
        reasons.append("Ticket is marked as must_not_auto_respond in system flags.")
    if intent in mandatory_escalate_intents:
        reasons.append(f"Intent '{intent}' requires mandatory human tier-two engineering review.")
    if confidence < threshold:
        reasons.append(f"Classification confidence ({confidence:.2f}) is below confidence threshold ({threshold:.2f}).")
    if not sources:
        reasons.append("No relevant knowledge base documentation passages were retrieved.")

    if reasons:
        action = RoutingAction.ESCALATE
        reason_str = " | ".join(reasons)
        payload = EscalationPayload(
            summary=f"Escalated ticket from customer {ticket.customer_id} ({ticket.customer_tier} tier). Subject: {ticket.subject or 'No Subject'}",
            predicted_intent=intent,
            predicted_urgency=classification.urgency.value,
            confidence=confidence,
            retrieved_sources=sources,
            uncertainty_reason=reason_str
        )
    else:
        action = RoutingAction.AUTO_ANSWER
        reason_str = f"Confidence {confidence:.2f} >= threshold {threshold:.2f} and {len(sources)} relevant documentation passages retrieved."
        payload = EscalationPayload(
            summary=f"Auto-answering ticket {ticket.ticket_id}",
            predicted_intent=intent,
            predicted_urgency=classification.urgency.value,
            confidence=confidence,
            retrieved_sources=sources,
            uncertainty_reason="None"
        )

    return action, reason_str, payload
