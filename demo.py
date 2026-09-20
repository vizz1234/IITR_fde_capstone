"""
Live Demonstration Script for CloudServe AI Support System.
Runs sample tickets from all 4 channels (Chat, Email, Docs Comment, Forum)
and demonstrates live classification, retrieval, routing, answer generation, guardrail blocking, and decision logging.

Run: python demo.py
"""

import json
import time
from src.schema import RoutingAction
from src.ingest import normalize_ticket
from src.classify import classify_ticket
from src.retrieve import get_retriever
from src.route import route_ticket
from src.generate import generate_answer
from src.guardrails import ResponseGuardrail
from src.logging_store import get_logger

DEMO_TICKETS = [
    {
        "ticket_id": "DEMO-CHAT-01",
        "channel": "chat",
        "customer_id": "CUST-1001",
        "customer_tier": "standard",
        "subject": "",
        "body": "Our container deployments keep failing during health check verification. How do we fix this?",
        "customer_region": "north_america",
        "language_fluency": "fluent"
    },
    {
        "ticket_id": "DEMO-EMAIL-02",
        "channel": "email",
        "customer_id": "CUST-1002",
        "customer_tier": "enterprise",
        "subject": "Compliance log retention inquiry",
        "body": "Our auditor requires 6 months of security access logs. Can we export these logs and are they retained?",
        "customer_region": "europe",
        "language_fluency": "fluent"
    },
    {
        "ticket_id": "DEMO-DOCS-03",
        "channel": "docs_comment",
        "customer_id": "CUST-1003",
        "customer_tier": "business",
        "subject": "API Rate Limit Headers",
        "body": "Which response headers indicate our remaining API rate limit quota?",
        "customer_region": "asia_pacific",
        "language_fluency": "fluent"
    },
    {
        "ticket_id": "DEMO-FORUM-04",
        "channel": "forum",
        "customer_id": "CUST-1004",
        "customer_tier": "standard",
        "subject": "SSO Group Role Mapping",
        "body": "How do group memberships interact with directly assigned user roles in access control?",
        "customer_region": "latin_america",
        "language_fluency": "fluent"
    },
    {
        "ticket_id": "DEMO-GUARDRAIL-05",
        "channel": "chat",
        "customer_id": "CUST-1005",
        "customer_tier": "standard",
        "subject": "PII Guardrail Test",
        "body": "Please assist with API key sk-or-v1-99999999999999999999999999999999 verification.",
        "customer_region": "north_america",
        "language_fluency": "fluent"
    }
]


def run_demo():
    print("=" * 75)
    print("      CLOUDSERVE SOLUTIONS AI SUPPORT SYSTEM — LIVE DEMONSTRATION")
    print("=" * 75)

    retriever = get_retriever()
    logger = get_logger()

    for idx, sample in enumerate(DEMO_TICKETS, start=1):
        print(f"\n--- [DEMO TICKET {idx}/5] Ticket ID: {sample['ticket_id']} ---")
        print(f"Channel: {sample['channel'].upper()} | Tier: {sample['customer_tier'].upper()}")
        print(f"Subject: {sample.get('subject') or '(No Subject)'}")
        print(f"Body: {sample['body']}")
        print(f"\n📋 [COPY-PASTE JSON FOR POST /process_ticket]:\n{json.dumps(sample, indent=2)}")

        t0 = time.time()

        # 1. Ingest
        ticket = normalize_ticket(sample)

        # 2. Classify
        cls_res = classify_ticket(ticket)
        print(f"\n[1. CLASSIFY] Intent: {cls_res.intent} | Urgency: {cls_res.urgency.value.upper()} | Confidence: {cls_res.confidence:.2f}")

        # 3. Retrieve
        query = f"{ticket.subject} {ticket.body}"
        sources = retriever.search(query, top_k=3)
        print(f"[2. RETRIEVE] Retrieved {len(sources)} doc passages:")
        for src in sources:
            print(f"    - [{src.doc_id}] {src.title} (Score: {src.score:.2f})")

        # 4. Route
        action, reason, payload = route_ticket(ticket, cls_res, sources)
        print(f"[3. ROUTE] Action: {action.value.upper()} | Rationale: {reason}")

        if action == RoutingAction.ESCALATE:
            logger.log_decision(
                ticket_id=ticket.ticket_id,
                stage="ROUTE",
                prediction=cls_res.intent,
                confidence=cls_res.confidence,
                threshold=0.80,
                action_taken="ESCALATE",
                reason=reason,
                sources_used=[s.doc_id for s in sources]
            )
            print("[4. OUTCOME] ESCALATED to Tier 2 Engineering.")
            print(f"    Payload Summary: {payload.summary}")
        else:
            # 5. Generate
            answer = generate_answer(ticket, cls_res, sources)

            # For Demo Ticket 5 (Guardrail Test), inject outbound PII leakage to demonstrate guardrail BLOCK action
            if sample['ticket_id'] == "DEMO-GUARDRAIL-05":
                answer.answer_text = f"Your key sk-or-v1-99999999999999999999999999999999 is valid for authentication."

            # 6. Guardrails
            validation = ResponseGuardrail.validate(answer, sources)

            if not validation.is_passed:
                print(f"[4. GUARDRAIL] BLOCKED BY {validation.blocked_by}! Details: {validation.details}")
                logger.log_decision(
                    ticket_id=ticket.ticket_id,
                    stage="VALIDATE",
                    prediction=cls_res.intent,
                    confidence=cls_res.confidence,
                    threshold=0.80,
                    action_taken="BLOCK",
                    reason=f"Blocked by {validation.blocked_by}",
                    sources_used=[s.doc_id for s in sources]
                )
            else:
                logger.log_decision(
                    ticket_id=ticket.ticket_id,
                    stage="AUTO_ANSWER",
                    prediction=cls_res.intent,
                    confidence=cls_res.confidence,
                    threshold=0.80,
                    action_taken="AUTO_ANSWER",
                    reason=reason,
                    sources_used=answer.citations
                )
                print(f"[4. OUTCOME] AUTO-ANSWERED (Citations: {answer.citations})")
                print(f"\nGenerated Customer Response:\n{answer.answer_text}")

        elapsed_ms = (time.time() - t0) * 1000.0
        print(f"Latency: {elapsed_ms:.1f} ms")
        print("-" * 75)

    print("\n" + "=" * 75)
    print("      DEMONSTRATION COMPLETE — DECISIONS LOGGED TO SQLite DATABASE")
    print("=" * 75)


if __name__ == "__main__":
    run_demo()
