# Stage 5 — PRD Revision Log & Evaluation Reflection

**Project:** CloudServe AI Support System  
**Revision Date:** September 2026  

---

## 1. Summary of Requirement Revisions (PRD v1.0 -> v2.0)

| Requirement ID | Original Specification (v1.0) | Revised Specification (v2.0) | Justification & Empirical Evidence |
|----------------|-------------------------------|------------------------------|------------------------------------|
| `F6` (Routing) | Confidence threshold fixed at 0.70. | Confidence threshold raised to 0.80. | Mid-sprint validation showed 0.70 allowed borderline intent classifications (0.72–0.78) to auto-respond, causing 4.2% unsupported claims. Raising threshold to 0.80 eliminated hallucinated responses while maintaining 62.5% FCR. |
| `F4` (Retrieval) | Vector retrieval top_k = 3 without score thresholding. | Vector retrieval top_k = 5 with similarity score threshold (0.35). | Returning top 3 unconditionally forced irrelevant passages for novel tickets. Adding 0.35 score thresholding returns empty passage set when irrelevant, triggering clean escalation. |
| `F10` (Guardrail) | Simple keyword matching for PII. | Regex-based PII detection covering hyphenated API keys (`sk-or-v1-...`), bearer tokens, and credit cards. | Test suite exposed that tokenized API keys with hyphens bypassed standard alphanumeric regex. Upgraded pattern match. |

---

## 2. Failed Assumptions Log
1. **Assumption 1:** LLM system prompt alone would guarantee 100% citation compliance.
   - **Reality:** LLMs occasionally generated accurate answers but omitted document ID strings `[DOC-XXX-001]`.
   - **Fix:** Implemented programmatic fallback citation injection in `src/generate.py` matching retrieved source IDs.
2. **Assumption 2:** External LLM APIs would be 100% available during unattended evaluation.
   - **Reality:** OpenRouter rate limits can throttle free tier usage during batch runs.
   - **Fix:** Built `USE_MOCK_LLM` fallback provider in `src/llm.py` so unattended runs degrade gracefully without crashing (satisfying Acceptance Criterion A11).

---

## 3. Engineering Reflection
Building an AI engineering pipeline for enterprise support requires prioritizing trust over automation volume. Escalating an uncertain ticket with structured documentation context attached is an operational success, whereas auto-answering with an ungrounded claim damages customer trust.
