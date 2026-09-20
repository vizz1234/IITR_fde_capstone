# Stage 3 — Prompt Library & Specification

**System:** CloudServe AI Support System  
**Prompt Register & Versioning**  

---

## 1. Overview & Architectural Principles
Prompts are treated as version-controlled software artifacts. Every prompt is designed with:
- **Role Scoping:** Clear system identity (CloudServe Support AI).
- **Strict Output Formatting:** JSON output or enforced inline citations.
- **Strict Grounding:** Instruction blocking the model from inventing ungrounded claims.

---

## 2. Prompt Library Catalog

### `PRMPT-CLS-001`: Intent & Urgency Classifier (v1.0)
- **Target Component:** `src/classify.py`
- **Output Schema:** Enforced JSON containing `intent`, `urgency`, `confidence`, `reasoning`, and `alternatives_considered`.
- **System Prompt Snippet:**
  ```text
  You are an expert AI ticket classifier for CloudServe Solutions.
  Analyze the support ticket subject and body, then classify it into:
  1. Intent (must be one of 22 valid intent categories)
  2. Urgency (low, medium, high)
  3. Confidence (float 0.00 to 1.00)
  Return ONLY valid JSON.
  ```

### `PRMPT-GEN-001`: Grounded RAG Generator (v1.0)
- **Target Component:** `src/generate.py`
- **Output Constraint:** Must cite exact document IDs `[DOC-XXX-001]`. Must state "unable to find information" if context does not support claim.
- **System Prompt Snippet:**
  ```text
  You are a helpful support engineer at CloudServe Solutions.
  Strict Grounding Rule: You MUST answer the question using ONLY the retrieved documentation context.
  Citations: Include inline citations [DOC-XXX-001] for every claim made.
  ```

### `PRMPT-GRD-001`: Guardrail Validator (v1.0)
- **Target Component:** `src/guardrails.py`
- **Execution Rule:** Deterministic regex + heuristic validator checking PII, citation validity, and tone.

---

## 3. Prompt Quality & Safety Checklist
- [x] Versioned in version control (`prompts/README.md`).
- [x] Zero credential exposure in prompt strings.
- [x] Anti-hallucination grounding instructions included.
- [x] Automated fallback parsing logic implemented.
