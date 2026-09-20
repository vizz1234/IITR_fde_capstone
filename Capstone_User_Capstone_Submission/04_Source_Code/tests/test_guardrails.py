"""
Tests for guardrails module: Acceptance Criterion A7.
Verifies at least one guardrail can block a response and does so when triggered by an engineered payload.
"""

from src.guardrails import ResponseGuardrail
from src.schema import GroundedAnswer, PassageSource


def test_guardrail_blocks_pii_leakage():
    # Engineered answer containing a leaked API key
    malicious_answer = GroundedAnswer(
        answer_text="Here is your API key sk-or-v1-abcdef1234567890abcdef1234567890 for authentication.",
        citations=["DOC-AUTH-001"]
    )
    sources = [PassageSource(doc_id="DOC-AUTH-001", title="Auth", content="Content", score=0.90)]

    val = ResponseGuardrail.validate(malicious_answer, sources)
    assert val.is_passed is False
    assert val.pii_detected is True
    assert val.blocked_by == "PII_GUARDRAIL"


def test_guardrail_blocks_hallucinated_citation():
    # Engineered answer citing a document that was NOT retrieved
    hallucinated_answer = GroundedAnswer(
        answer_text="Based on our policy [DOC-HALLUCINATED-999], all fees are non-refundable.",
        citations=["DOC-HALLUCINATED-999"]
    )
    sources = [PassageSource(doc_id="DOC-BILLING-001", title="Billing", content="Content", score=0.90)]

    val = ResponseGuardrail.validate(hallucinated_answer, sources)
    assert val.is_passed is False
    assert val.unsupported_claims is True
    assert val.blocked_by == "CITATION_HALLUCINATION_GUARDRAIL"


def test_guardrail_passes_clean_response():
    clean_answer = GroundedAnswer(
        answer_text="You can configure SSO via Saml 2.0 as documented in [DOC-SEC-001].",
        citations=["DOC-SEC-001"]
    )
    sources = [PassageSource(doc_id="DOC-SEC-001", title="SSO", content="Content", score=0.90)]

    val = ResponseGuardrail.validate(clean_answer, sources)
    assert val.is_passed is True
    assert val.blocked_by is None
