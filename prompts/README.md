# CloudServe AI Support System — Versioned Prompt Library

This prompt library registers, documents, and versions all system prompts, classification prompts, answer generation prompts, guardrail prompts, and evaluation prompts. Prompts are treated as production software design artifacts.

---

## Prompt Register

| Prompt ID | Name | Version | Scope / Purpose | Target Requirement |
|-----------|------|---------|-----------------|--------------------|
| `PRMPT-SYS-001` | System Instructions | v1.0 | Core persona and behavior guidelines | F1 |
| `PRMPT-CLS-001` | Intent & Urgency Classifier | v1.0 | Predicts intent (22 categories) & urgency with confidence score | F2, F3 |
| `PRMPT-GEN-001` | Grounded RAG Generator | v1.0 | Generates answers strictly grounded in retrieved doc context with citations | F5, F6 |
| `PRMPT-GRD-001` | Response Guardrail Validator | v1.0 | Checks response for PII, unsupported claims, and tone compliance | F7 |
| `PRMPT-EVL-001` | Evaluation Framework Judge | v1.0 | Evaluates ground truth answer alignment and correctness | F11 |

---

## Traceability & Checklist

Every prompt in this library satisfies the quality checklist:
1. **Explicit Role & Persona**: Defined role as CloudServe Support AI.
2. **Strict Output Formatting**: Enforces JSON schema / structured markup.
3. **Grounding & Anti-Hallucination**: Restricts answer content strictly to supplied retrieved passages.
4. **Safety & Compliance**: Enforces zero PII disclosure.
