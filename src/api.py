"""
FastAPI Application Interface: Exposes endpoints for ticket ingestion, classification,
retrieval, routing, generation, end-to-end processing, and Prometheus monitoring metrics.
"""

from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST, REGISTRY
from pydantic import BaseModel
from src.schema import Ticket, RoutingAction, GroundedAnswer, ValidationResult
from src.ingest import normalize_ticket
from src.classify import classify_ticket
from src.retrieve import get_retriever
from src.route import route_ticket
from src.generate import generate_answer
from src.guardrails import ResponseGuardrail
from src.logging_store import get_logger

app = FastAPI(
    title="CloudServe Solutions AI Support API",
    description="Intelligent Customer Support Triage, RAG Retrieval, Routing, Guardrails, and Decision Logging API",
    version="1.0.0"
)

def _get_metric(metric_type, name, doc, labels=()):
    if name in REGISTRY._names_to_collectors:
        return REGISTRY._names_to_collectors[name]
    return metric_type(name, doc, labels)

# Prometheus Metrics
TICKETS_TOTAL = _get_metric(Counter, "tickets_processed_total", "Total tickets processed", ["channel", "outcome"])
LATENCY = _get_metric(Histogram, "ticket_processing_latency_seconds", "End-to-end processing latency")
GUARDRAIL_BLOCKS = _get_metric(Counter, "guardrail_blocks_total", "Responses blocked by guardrails", ["guardrail_type"])


class TicketProcessRequest(BaseModel):
    ticket_id: str = ""
    channel: str = "email"
    subject: str = ""
    body: str
    customer_id: str = "CUST-001"
    customer_tier: str = "standard"
    customer_region: str = "US"
    language_fluency: str = "fluent"
    labels: Dict[str, Any] = {}


class ProcessResult(BaseModel):
    ticket_id: str
    channel: str
    action: str
    predicted_intent: str
    predicted_urgency: str
    confidence: float
    reason: str
    response_text: str
    citations: List[str]
    guardrail_passed: bool
    blocked_by: str = ""


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "CloudServe AI Support API", "version": "1.0.0"}


@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/process_ticket", response_model=ProcessResult)
def process_ticket_endpoint(req: TicketProcessRequest):
    """Executes end-to-end pipeline for a single support ticket."""
    raw_data = req.model_dump()

    with LATENCY.time():
        # 1. Ingest
        ticket = normalize_ticket(raw_data)

        # 2. Classify
        classification = classify_ticket(ticket)

        # 3. Retrieve
        retriever = get_retriever()
        query = f"{ticket.subject} {ticket.body}"
        sources = retriever.search(query, top_k=5)

        # 4. Route
        action, route_reason, payload = route_ticket(ticket, classification, sources)

        logger = get_logger()

        if action == RoutingAction.ESCALATE:
            logger.log_decision(
                ticket_id=ticket.ticket_id,
                stage="ROUTE",
                prediction=classification.intent,
                confidence=classification.confidence,
                threshold=0.80,
                action_taken="ESCALATE",
                reason=route_reason,
                sources_used=[s.doc_id for s in sources],
                requirement_ids="F1,F4,F5,F8"
            )

            TICKETS_TOTAL.labels(channel=ticket.channel.value, outcome="ESCALATE").inc()

            return ProcessResult(
                ticket_id=ticket.ticket_id,
                channel=ticket.channel.value,
                action="ESCALATE",
                predicted_intent=classification.intent,
                predicted_urgency=classification.urgency.value,
                confidence=classification.confidence,
                reason=route_reason,
                response_text="Ticket has been escalated to Tier-2 Engineering with detailed context.",
                citations=[s.doc_id for s in sources],
                guardrail_passed=True
            )

        # 5. Generate
        answer = generate_answer(ticket, classification, sources)

        # 6. Guardrails
        validation = ResponseGuardrail.validate(answer, sources)

        if not validation.is_passed:
            blocked_by = validation.blocked_by or "UNKNOWN_GUARDRAIL"
            GUARDRAIL_BLOCKS.labels(guardrail_type=blocked_by).inc()

            logger.log_decision(
                ticket_id=ticket.ticket_id,
                stage="VALIDATE",
                prediction=classification.intent,
                confidence=classification.confidence,
                threshold=0.80,
                action_taken="BLOCK",
                reason=f"Response blocked by guardrail: {validation.details}",
                sources_used=[s.doc_id for s in sources],
                guardrails={"blocked_by": blocked_by, "details": validation.details},
                requirement_ids="F1,F6,F7"
            )

            TICKETS_TOTAL.labels(channel=ticket.channel.value, outcome="BLOCK").inc()

            return ProcessResult(
                ticket_id=ticket.ticket_id,
                channel=ticket.channel.value,
                action="BLOCK",
                predicted_intent=classification.intent,
                predicted_urgency=classification.urgency.value,
                confidence=classification.confidence,
                reason=f"Blocked by safety guardrail ({blocked_by}). Escalated to human team.",
                response_text="Response was blocked by safety policy. Escalating to human agent.",
                citations=[],
                guardrail_passed=False,
                blocked_by=blocked_by
            )

        # Successfully auto-answered
        logger.log_decision(
            ticket_id=ticket.ticket_id,
            stage="AUTO_ANSWER",
            prediction=classification.intent,
            confidence=classification.confidence,
            threshold=0.80,
            action_taken="AUTO_ANSWER",
            reason=route_reason,
            sources_used=answer.citations,
            guardrails={"status": "passed"},
            requirement_ids="F1,F2,F3,F5,F6,F7"
        )

        TICKETS_TOTAL.labels(channel=ticket.channel.value, outcome="AUTO_ANSWER").inc()

        return ProcessResult(
            ticket_id=ticket.ticket_id,
            channel=ticket.channel.value,
            action="AUTO_ANSWER",
            predicted_intent=classification.intent,
            predicted_urgency=classification.urgency.value,
            confidence=classification.confidence,
            reason=route_reason,
            response_text=answer.answer_text,
            citations=answer.citations,
            guardrail_passed=True
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)
