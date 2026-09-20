"""
Tests for route module: Acceptance Criterion A5.
Verifies threshold routing and determinism (same input produces same routing decision).
"""

from src.route import route_ticket
from src.schema import ClassificationResult, RoutingAction, UrgencyEnum, PassageSource


def test_routing_determinism(sample_chat_ticket):
    cls_res = ClassificationResult(
        intent="deployment_failure",
        urgency=UrgencyEnum.HIGH,
        confidence=0.92,
        reasoning="High confidence match"
    )
    sources = [PassageSource(doc_id="DOC-DEPLOY-001", title="Deployment Fix", content="Content", score=0.88)]

    # First run
    action1, reason1, payload1 = route_ticket(sample_chat_ticket, cls_res, sources, custom_threshold=0.80)
    # Second run
    action2, reason2, payload2 = route_ticket(sample_chat_ticket, cls_res, sources, custom_threshold=0.80)

    assert action1 == action2 == RoutingAction.AUTO_ANSWER
    assert reason1 == reason2


def test_routing_escalation_below_threshold(sample_chat_ticket):
    cls_res = ClassificationResult(
        intent="deployment_failure",
        urgency=UrgencyEnum.HIGH,
        confidence=0.65,  # Below 0.80 threshold
        reasoning="Low confidence match"
    )
    sources = [PassageSource(doc_id="DOC-DEPLOY-001", title="Deployment Fix", content="Content", score=0.88)]

    action, reason, payload = route_ticket(sample_chat_ticket, cls_res, sources, custom_threshold=0.80)
    assert action == RoutingAction.ESCALATE
    assert "below confidence threshold" in reason.lower()
    assert payload.predicted_intent == "deployment_failure"


def test_routing_mandatory_escalation_intents(sample_email_ticket):
    cls_res = ClassificationResult(
        intent="security_incident",
        urgency=UrgencyEnum.HIGH,
        confidence=0.99,
        reasoning="Security incident match"
    )
    sources = [PassageSource(doc_id="DOC-SEC-001", title="Security", content="Content", score=0.95)]

    action, reason, payload = route_ticket(sample_email_ticket, cls_res, sources)
    assert action == RoutingAction.ESCALATE
    assert "security_incident" in reason
