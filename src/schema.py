"""
Data models and schema definitions for CloudServe AI Support System.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ChannelEnum(str, Enum):
    EMAIL = "email"
    CHAT = "chat"
    DOCS_COMMENT = "docs_comment"
    FORUM = "forum"


class UrgencyEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CustomerTierEnum(str, Enum):
    STANDARD = "standard"
    BUSINESS = "business"
    ENTERPRISE = "enterprise"


class Ticket(BaseModel):
    """Normalized internal representation of a support ticket."""
    ticket_id: str
    channel: ChannelEnum
    customer_id: str = "unknown"
    customer_tier: CustomerTierEnum = CustomerTierEnum.STANDARD
    region: str = "US"
    language_fluency: str = "fluent"
    subject: str = ""
    body: str
    raw_payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    labels: Dict[str, Any] = Field(default_factory=dict)


class ClassificationResult(BaseModel):
    """Result of intent and urgency classification."""
    intent: str
    urgency: UrgencyEnum
    confidence: float
    reasoning: str
    alternatives_considered: List[Dict[str, Any]] = Field(default_factory=list)


class PassageSource(BaseModel):
    """Passage returned by vector store RAG search."""
    doc_id: str
    title: str
    content: str
    score: float
    chunk_id: Optional[str] = None


class RoutingAction(str, Enum):
    AUTO_ANSWER = "auto_answer"
    ESCALATE = "escalate"
    BLOCK = "block"


class EscalationPayload(BaseModel):
    """Structured context attached to escalated tickets for Tier 2 engineers."""
    summary: str
    predicted_intent: str
    predicted_urgency: str
    confidence: float
    retrieved_sources: List[PassageSource] = Field(default_factory=list)
    uncertainty_reason: str


class GroundedAnswer(BaseModel):
    """Generated response grounded in retrieved documentation."""
    answer_text: str
    citations: List[str] = Field(default_factory=list)
    is_grounded: bool = True
    claims_supported: bool = True


class ValidationResult(BaseModel):
    """Result of guardrail validation checks."""
    is_passed: bool
    blocked_by: Optional[str] = None
    pii_detected: bool = False
    unsupported_claims: bool = False
    toxic_tone: bool = False
    details: List[str] = Field(default_factory=list)


class DecisionRecord(BaseModel):
    """Record written to the SQLite decision database for audit and compliance."""
    decision_id: str
    created_at: str
    ticket_id: str
    stage: str
    prediction: Optional[str] = None
    confidence: Optional[float] = None
    threshold: Optional[float] = None
    action_taken: str
    reason: str
    sources_used: Optional[str] = None
    guardrails: Optional[str] = None
    prompt_version: str = "v1.0"
    requirement_ids: Optional[str] = None
