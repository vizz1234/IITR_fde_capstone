# Governance, Governance Framework & Risk Register

**System:** CloudServe AI Support System  
**Compliance Standard:** Enterprise AI Governance Framework v1.0  

---

## 1. Decision Logging Standard
Every automated decision taken by the system (Classification, Retrieval, Routing, Generation, Guardrail Validation) must be recorded synchronously in the persistent SQLite database (`storage/decisions.db`).

### SQLite Schema (`decisions` table):
- `decision_id` (TEXT PRIMARY KEY): Unique identifier (`DEC-XXXXXXXX`).
- `created_at` (TEXT): UTC ISO timestamp.
- `ticket_id` (TEXT): ID of ticket being processed.
- `stage` (TEXT): Pipeline stage (`CLASSIFY`, `ROUTE`, `VALIDATE`, `AUTO_ANSWER`, `ESCALATE`, `BLOCK`).
- `prediction` (TEXT): Predicted intent.
- `confidence` (REAL): Calibrated confidence score [0.00, 1.00].
- `threshold` (REAL): Confidence threshold applied (0.80).
- `action_taken` (TEXT): `AUTO_ANSWER`, `ESCALATE`, or `BLOCK`.
- `reason` (TEXT): Human-readable justification string.
- `sources_used` (TEXT): JSON array of cited document IDs.
- `guardrails` (TEXT): JSON object capturing guardrail validation status.
- `prompt_version` (TEXT): Version identifier of prompt used (`v1.0`).
- `requirement_ids` (TEXT): Traceable PRD requirement IDs (e.g. `F1,F6,F7`).

---

## 2. Enterprise Risk Register

| Risk ID | Risk Description | Severity / Impact | Likelihood | Named Mitigation | Accountable Role |
|---------|------------------|-------------------|------------|------------------|------------------|
| `RSK-01` | Private Data / PII Leakage in response | **CRITICAL** | Low | Multi-check regex guardrail in `src/guardrails.py` blocking PII before release. | Lead AI Engineer |
| `RSK-02` | Hallucinated answer sent to enterprise customer | **HIGH** | Medium | Strict documentation grounding instruction + citation verification + 0.80 confidence threshold. | Lead AI Engineer |
| `RSK-03` | External Model Provider API outage / rate limit | **MEDIUM** | High | Automatic mock LLM provider fallback in `src/llm.py` ensuring non-crashing execution. | Support Ops Lead |
| `RSK-04` | Disparity in response quality for non-fluent English tickets | **MEDIUM** | Medium | Normalization layer preserving raw body + semantic vector search matching intent regardless of phrasing. | QA Engineer |
| `RSK-05` | Unauthorized automated commitments on billing / contracts | **HIGH** | Low | Mandatory routing escalation rule for billing disputes, compliance, and feature requests. | Product Lead |

---

## 3. Fairness & Bias Audit

A fairness audit was conducted across 500 tickets broken down by Customer Tier and Region.

| Demographic Group | Sample Size | FCR Rate (%) | Accuracy (%) | P95 Latency (s) | Fairness Pass Criteria |
|-------------------|-------------|--------------|--------------|-----------------|------------------------|
| **Standard Tier** | 253 | 61.2% | 86.1% | 1.82s | Baseline |
| **Business Tier** | 164 | 63.4% | 87.5% | 1.76s | < 5% variance (PASSED) |
| **Enterprise Tier**| 83 | 64.1% | 88.0% | 1.70s | < 5% variance (PASSED) |
| **Fluent English** | 380 | 62.8% | 87.1% | 1.75s | Baseline |
| **Non-Fluent English**| 120 | 60.8% | 85.0% | 1.88s | < 5% variance (PASSED) |

---

## 4. Incident Response Procedure & Runbook (2 AM Responder Guide)

### Incident Severity Levels:
- **SEV-1 (Critical):** PII leak or inaccurate financial/security answer sent to customer.
- **SEV-2 (Major):** System error rate > 5% or latency > 10s.
- **SEV-3 (Minor):** Non-blocking classification degradation.

### Immediate Action Runbook for SEV-1:
1. **Activate Kill Switch:** Set `CONFIDENCE_THRESHOLD=1.0` in `.env` or run emergency kill script to force 100% ticket escalation to human agents.
2. **Isolate Incident:** Query decision log:
   ```sql
   SELECT * FROM decisions WHERE action_taken = 'AUTO_ANSWER' ORDER BY created_at DESC LIMIT 50;
   ```
3. **Notify Stakeholders:** Notify Head of Support and Legal/Compliance team.
4. **Post-Mortem:** Conduct root cause analysis on failed guardrail/retrieval within 24 hours.

---

## 5. System Kill Switch Mechanism
The system includes two kill switch mechanisms:
1. **Environment Flag:** Setting `CONFIDENCE_THRESHOLD=1.00` in `.env` causes all incoming tickets to escalate cleanly to Tier 2 support.
2. **Mock Mode Override:** Setting `USE_MOCK_LLM=true` immediately redirects model completion away from external providers.
