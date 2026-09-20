# Effort Log & Time Tracking

**Project:** CloudServe Solutions AI Support System  
**Engineer:** Forward Deployed AI Engineer  

---

## Stage-by-Stage Effort Tracking

| Stage | Activity / Task | Estimated Hours | Actual Hours | Variance (Hours) | Key Notes |
|-------|-----------------|-----------------|--------------|------------------|-----------|
| **Stage 1** | Stakeholder Interview Analysis & Ticket Dataset Exploration | 12h | 11h | -1h | Discovery interviews revealed 71.4% doc-answerability; keyword search bottleneck. |
| **Stage 2** | Product Requirements Document (PRD v1.0 & v2.0) | 10h | 9h | -1h | Traceability matrix mapped all 12 functional requirements back to evidence. |
| **Stage 3** | Prompt Library Specification & System Prompts | 8h | 8h | 0h | Built versioned system prompts, classification, grounded generation, and guardrails. |
| **Stage 4** | Sprint Planning & Scope Definition | 6h | 5h | -1h | Backlog prioritized around 12 acceptance criteria (A1–A12). |
| **Stage 5** | Core Build: Ingest, Classify, Retrieve, Route, Generate, Guardrails | 35h | 34h | -1h | Built normalized ingest, Chroma vector store RAG, calibrated classifier, deterministic router, grounded generator, PII guardrails, and SQLite decision logger. |
| **Stage 5** | Test Suite & Evaluation Harness | 15h | 14h | -1h | Built Pytest suite (22 tests) and unattended evaluation harness (`evaluation/harness.py`). |
| **Stage 6** | Governance Framework, Risk Register, & Packaging | 10h | 10h | 0h | Written decision log schema, fairness audit, incident runbook, and root `README.md`. |
| **Total** | **Full Capstone Project End-to-End** | **96h** | **91h** | **-5h** | **Completed within allocation.** |

---

## Variance Analysis & Lessons Learned
- **High Efficiency Area:** RAG retrieval and vector database indexing with Chroma was fast to set up thanks to pre-cleaned `documentation.json`.
- **Iteration Area:** PII guardrail regex required updating to support hyphenated API tokens (`sk-or-v1-...`).
