# Stage 2 — Product Requirements Document (PRD v2.0)

**Project:** CloudServe Solutions Intelligent Customer Support System  
**Document Status:** Approved & Revised (v2.0)  
**Author:** Forward Deployed AI Engineer  

---

## 1. Document Control & Revision Log
- **v1.0 (Week 1):** Initial baseline requirements drafted from Stage 1 Discovery evidence.
- **v2.0 (Week 2/3):** Revised after mid-sprint validation runs. Updated confidence thresholding (0.80), refined vector retrieval score filters (0.35), and strengthened PII guardrails.

---

## 2. Target User Personas
1. **Tier 1 Support Agent (Sofia):** Needs automated high-quality draft responses and doc citations to process tickets faster without fearing customer backlash.
2. **Tier 2 Support Engineer (Daniel):** Needs structured escalation payloads containing ticket summary, predicted intent, retrieved docs, and specific reason for escalation.
3. **Head of Support (Marcus):** Needs SLA response time < 5 min, FCR >= 60%, escalation rate <= 30%, and 100% auditability for compliance.
4. **End Customer (Ravi):** Needs fast, accurate, honest responses with verifiable document links.

---

## 3. Functional Requirements & Evidence Traceability

| Req ID | Title | Functional Requirement Description | Discovery Traceability | Acceptance Criteria |
|--------|-------|------------------------------------|------------------------|---------------------|
| `F1` | Multi-Channel Ingest | Ingest and normalize tickets from Email, Chat, Docs Comments, and Forum into unified `Ticket` schema preserving channel & raw payload. | `EVD-05`, Sofia Interview | A2 |
| `F2` | Intent & Urgency Classifier | Predict intent across 22 categories and urgency (`low`, `medium`, `high`) with calibrated float confidence score [0.0, 1.0]. | `EVD-01`, Marcus Interview | A3 |
| `F3` | Defined Fallback | Provide graceful fallback prediction and non-crashing exception handling on classification failure. | `EVD-01`, Marcus Interview | A3, A11 |
| `F4` | RAG Vector Search | Search 29 knowledge base docs using Chroma vector store and `all-MiniLM-L6-v2` embeddings, returning PassageSource items with doc IDs. | `EVD-02`, Ines Interview | A4 |
| `F5` | Relevance Thresholding | Apply relevance score thresholding to vector search; return empty passage set if no doc exceeds score threshold. | `EVD-02`, Ines Interview | A4 |
| `F6` | Deterministic Routing | Apply calibrated confidence threshold (0.80) to route between `auto_answer` and `escalate`. Identical inputs yield identical decisions. | `EVD-01`, Marcus Interview | A5 |
| `F7` | Mandatory Escalation Rules | Automatically escalate tickets with intents `security_incident`, `compliance_request`, `feature_request`, `data_residency`, or `must_not_auto_respond` flag. | `EVD-04`, Daniel Interview | A5 |
| `F8` | Structured Escalation Payload | Generate rich escalation context (summary, intent, urgency, retrieved docs, reason) for Tier 2 engineers. | `EVD-03`, Daniel Interview | A5 |
| `F9` | Grounded Answer Generation | Draft responses strictly grounded in retrieved passages with exact inline citations `[DOC-XXX-001]`. | `EVD-01`, Ines Interview | A6 |
| `F10` | Response Guardrails | Enforce safety checks blocking responses containing PII, hallucinated citations, or improper tone. | `EVD-04`, Marcus Interview | A7 |
| `F11` | Persistent Decision Logging | Log every decision (input, intent, confidence, threshold, action, reason, sources, guardrails) to SQLite database. | `EVD-01`, Marcus Interview | A8 |
| `F12` | Unattended Evaluation Harness | Provide command line harness (`python -m evaluation.harness --input ... --output ...`) generating full volume, business, technical, and governance metrics. | `EVD-01`, Marcus Interview | A9, A10 |

---

## 4. Non-Functional Requirements (NFRs)
- `NF1` **Response Latency:** 95th percentile (p95) processing latency < 3.0 seconds for live chat compatibility.
- `NF2` **Availability:** System resilience >= 99.5%; handles external API timeouts and rate limits gracefully via mock fallback.
- `NF3` **Zero PII Leakage:** 0 occurrences of private credentials, API keys, or credit cards in outbound text.
- `NF4` **Auditability:** 100% of automated decisions written to SQLite database (`storage/decisions.db`).
- `NF5` **Reproducibility:** System builds cleanly from repository checkout following `README.md`.

---

## 5. Deliberately Out of Scope
- Direct write execution into production databases (system generates recommendations/answers only).
- Automatic refund processing or binding legal commitments.
- Custom LLM fine-tuning (RAG over documentation is enforced).

---

## 6. Assumptions & Risk Controls
- **Assumption:** Documentation in `documentation.json` is accurate and updated.
- **Risk:** LLM provider outage or rate limiting.
- **Mitigation:** Built-in automatic mock LLM fallback client in `src/llm.py` ensures continuous offline operation.
