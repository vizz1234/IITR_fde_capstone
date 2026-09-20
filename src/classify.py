"""
Classification Module: Classifies intent (22 categories) and urgency (low, medium, high)
with calibrated numeric confidence score and structured reasoning.
"""

import json
from typing import Dict, Any, List
from src.schema import Ticket, ClassificationResult, UrgencyEnum
from src.llm import llm_client

VALID_INTENTS = [
    "deployment_failure", "api_key_issue", "compliance_request", "rollback_request",
    "feature_request", "configuration_help", "authentication_failure", "data_export",
    "sso_configuration", "security_incident", "account_access", "api_usage_question",
    "database_issue", "rate_limit", "billing_query", "integration_help",
    "performance_degradation", "quota_or_overage", "data_residency", "webhook_issue",
    "unclear_request", "onboarding"
]

SYSTEM_PROMPT = f"""You are an expert AI ticket classifier for CloudServe Solutions.
Analyze the support ticket subject and body, then classify it into:
1. Intent (must be one of: {', '.join(VALID_INTENTS)})
2. Urgency (must be one of: low, medium, high)
3. Confidence (numeric score between 0.00 and 1.00)
4. Reasoning (brief explanation)
5. Alternatives considered

Return ONLY a valid JSON object with the following schema:
{{
  "intent": "<intent>",
  "urgency": "<low|medium|high>",
  "confidence": 0.85,
  "reasoning": "<explanation>",
  "alternatives_considered": [
     {{"intent": "<alt_intent>", "confidence": 0.10}}
  ]
}}
"""


def classify_ticket(ticket: Ticket) -> ClassificationResult:
    """
    Classifies a ticket for intent and urgency using LLM with fallback rule matching.
    Returns ClassificationResult containing numerical confidence score.
    """
    # Fast rule heuristic fallback if body is very short or obvious
    content = f"Subject: {ticket.subject}\nBody: {ticket.body}".strip()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": content}
    ]

    try:
        raw_response = llm_client.complete(messages, temperature=0.0)
        # Attempt to parse JSON response
        clean_json = raw_response
        if "```json" in clean_json:
            clean_json = clean_json.split("```json")[1].split("```")[0].strip()
        elif "```" in clean_json:
            clean_json = clean_json.split("```")[1].split("```")[0].strip()

        parsed = json.loads(clean_json)

        intent = str(parsed.get("intent", "unclear_request")).lower()
        if intent not in VALID_INTENTS:
            intent = "unclear_request"

        raw_urgency = str(parsed.get("urgency", "medium")).lower()
        if raw_urgency == "high":
            urgency = UrgencyEnum.HIGH
        elif raw_urgency == "low":
            urgency = UrgencyEnum.LOW
        else:
            urgency = UrgencyEnum.MEDIUM

        confidence = float(parsed.get("confidence", 0.70))
        confidence = max(0.0, min(1.0, confidence))

        reasoning = str(parsed.get("reasoning", "Classification completed successfully."))
        alternatives = parsed.get("alternatives_considered", [])

        return ClassificationResult(
            intent=intent,
            urgency=urgency,
            confidence=confidence,
            reasoning=reasoning,
            alternatives_considered=alternatives
        )
    except Exception as e:
        # Defined fallback on classification error or unparsable JSON
        return ClassificationResult(
            intent="unclear_request",
            urgency=UrgencyEnum.MEDIUM,
            confidence=0.40,
            reasoning=f"Fallback classification invoked due to parsing exception: {str(e)}",
            alternatives_considered=[]
        )
