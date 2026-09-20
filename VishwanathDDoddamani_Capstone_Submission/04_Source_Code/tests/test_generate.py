"""
Tests for generate module: Acceptance Criterion A6.
Verifies generated answers carry citations that resolve to real retrieved documentation passages.
"""

from src.generate import generate_answer
from src.schema import ClassificationResult, UrgencyEnum, PassageSource


def test_generation_carries_citations(sample_chat_ticket):
    cls_res = ClassificationResult(
        intent="deployment_failure",
        urgency=UrgencyEnum.HIGH,
        confidence=0.90,
        reasoning="Good match"
    )
    sources = [
        PassageSource(
            doc_id="DOC-DEPLOY-001",
            title="Resolving Container Health Check Failures",
            content="Ensure your health check endpoint returns HTTP 200 within 30 seconds.",
            score=0.89
        )
    ]

    answer = generate_answer(sample_chat_ticket, cls_res, sources)
    assert answer.answer_text != ""
    assert "DOC-DEPLOY-001" in answer.citations or "DOC-DEPLOY-001" in answer.answer_text
    assert answer.is_grounded is True


def test_generation_no_sources_fallback(sample_email_ticket):
    cls_res = ClassificationResult(
        intent="feature_request",
        urgency=UrgencyEnum.LOW,
        confidence=0.90,
        reasoning="Feature request"
    )
    answer = generate_answer(sample_email_ticket, cls_res, sources=[])
    assert "unable to find" in answer.answer_text.lower() or "escalated" in answer.answer_text.lower()
