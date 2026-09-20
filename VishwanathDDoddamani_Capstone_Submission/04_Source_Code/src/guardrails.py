"""
Guardrails Module: Enforces safety checks on all outbound responses before release.
Checks for PII / private data leakage, unsupported claims / hallucination, and improper tone.
Can block responses.
"""

import re
from typing import List, Optional
from src.schema import GroundedAnswer, PassageSource, ValidationResult


class ResponseGuardrail:
    """Multi-check guardrail suite for validating generated responses."""

    # PII Regex patterns (API keys, private keys, passwords, credit cards, SSN, internal IPs)
    PII_PATTERNS = [
        (r"sk-[a-zA-Z0-9\-\_]{16,}", "API Key"),
        (r"api[_\-]?key\s*[:=]\s*['\"]?[a-zA-Z0-9\-\_]{12,}", "API Key"),
        (r"bearer\s+[a-zA-Z0-9\-\_\.]{16,}", "Bearer Token"),
        (r"BEGIN\s+PRIVATE\s+KEY", "Private Key"),
        (r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b", "Credit Card"),
        (r"\b\d{3}-\d{2}-\d{4}\b", "SSN"),
        (r"\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", "Internal IP"),
        (r"\b192\.168\.\d{1,3}\.\d{1,3}\b", "Internal IP"),
        (r"password\s*=\s*['\"][^'\"]+['\"]", "Hardcoded Password")
    ]

    TOXIC_TERMS = ["stupid", "idiot", "dumb", "shut up", "useless"]

    @classmethod
    def validate(
        cls,
        answer: GroundedAnswer,
        retrieved_sources: List[PassageSource]
    ) -> ValidationResult:
        """
        Validates generated answer against guardrail rules.
        Returns ValidationResult with is_passed boolean.
        If is_passed is False, the response MUST BE BLOCKED.
        """
        details = []
        pii_detected = False
        unsupported_claims = False
        toxic_tone = False
        blocked_by = None

        text = answer.answer_text

        # 1. PII & Private Data Leakage Check
        for pattern, pii_type in cls.PII_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                pii_detected = True
                details.append(f"PII Leakage detected: {pii_type}")
                blocked_by = "PII_GUARDRAIL"
                break

        # 2. Unsupported Claims / Citation Integrity Check
        valid_doc_ids = {src.doc_id for src in retrieved_sources}
        cited_doc_ids = set(answer.citations)

        # Verify that all citations in response actually belong to retrieved sources
        invalid_citations = cited_doc_ids - valid_doc_ids
        if invalid_citations:
            unsupported_claims = True
            details.append(f"Unsupported citation hallucination detected: {list(invalid_citations)}")
            if not blocked_by:
                blocked_by = "CITATION_HALLUCINATION_GUARDRAIL"

        # Check if citations are missing when text makes specific technical claims without doc sources
        if retrieved_sources and not answer.citations and "unable to find" not in text.lower():
            unsupported_claims = True
            details.append("Response lacks required document citations for technical claims.")
            if not blocked_by:
                blocked_by = "UNSUPPORTED_CLAIMS_GUARDRAIL"

        # 3. Tone & Toxicity Check
        for term in cls.TOXIC_TERMS:
            if term in text.lower():
                toxic_tone = True
                details.append(f"Unprofessional tone keyword detected: '{term}'")
                if not blocked_by:
                    blocked_by = "TONE_GUARDRAIL"
                break

        is_passed = not (pii_detected or unsupported_claims or toxic_tone)

        return ValidationResult(
            is_passed=is_passed,
            blocked_by=blocked_by,
            pii_detected=pii_detected,
            unsupported_claims=unsupported_claims,
            toxic_tone=toxic_tone,
            details=details
        )
