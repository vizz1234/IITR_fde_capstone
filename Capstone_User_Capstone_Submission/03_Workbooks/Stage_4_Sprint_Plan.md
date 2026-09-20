# Stage 4 — Sprint Plan & Backlog

**Project:** CloudServe AI Support System  
**Sprint Duration:** 2 Weeks (10 Working Days)  
**Team Capacity:** 1 Forward Deployed AI Engineer (100% Allocation)  

---

## 1. Backlog & Estimates

| Item ID | Component | Task Description | Est. Hours | Owner | Definition of Done (DoD) |
|---------|-----------|------------------|------------|-------|--------------------------|
| `TSK-01` | Ingest | Build normalized multi-channel ingestion for Email, Chat, Docs Comment, Forum (`src/ingest.py`). | 6h | FDE | Ingests sample ticket from all 4 channels without errors; passes `test_ingest.py`. |
| `TSK-02` | Retrieve | Build Chroma vector store indexing over `documentation.json` (`src/retrieve.py`). | 8h | FDE | Returns passage sources with doc IDs; applies score thresholding; passes `test_retrieve.py`. |
| `TSK-03` | Classify | Implement intent (22 categories) & urgency classifier with confidence scoring (`src/classify.py`). | 10h | FDE | Returns numerical confidence score [0.0, 1.0] and fallback on error; passes `test_classify.py`. |
| `TSK-04` | Route | Implement deterministic routing logic & structured escalation payload (`src/route.py`). | 8h | FDE | Identical inputs produce identical routing decisions; passes `test_route.py`. |
| `TSK-05` | Generate | Implement grounded answer generator with inline citations `[DOC-XXX-001]` (`src/generate.py`). | 8h | FDE | Generates answers carrying verifiable citations; passes `test_generate.py`. |
| `TSK-06` | Guardrails | Implement PII detection, citation verification, and blocking mechanism (`src/guardrails.py`). | 8h | FDE | Successfully blocks engineered PII and hallucinated payloads; passes `test_guardrails.py`. |
| `TSK-07` | Log Store | Build SQLite decision database logger (`src/logging_store.py`). | 6h | FDE | Every decision written to SQLite `decisions.db`; passes `test_logging.py`. |
| `TSK-08` | Harness | Build unattended evaluation harness (`evaluation/harness.py`). | 10h | FDE | Runs dataset unattended, generates `metrics_report.json` and `metrics_report.md`. |
| `TSK-09` | API & Metrics | Build FastAPI web API and Prometheus monitoring endpoint (`src/api.py`). | 6h | FDE | Endpoint `/process_ticket` and `/metrics` function without errors. |
| `TSK-10` | Docs & Governance | Write PRD, Governance Framework, Risk Register, and Effort Log (`docs/`). | 10h | FDE | All 6 stage workbooks completed and committed. |

---

## 2. Daily Checkpoint Schedule (Week 2 Build)

- **Day 1 (Ingest):** Ingest normalized objects for all 4 channels verified.
- **Day 2 (Retrieval):** Chroma vector database indexed; semantic search returns verifiable doc IDs.
- **Day 3 (Classification & Routing):** Confidence scoring calibrated; routing threshold applied and logged.
- **Day 4 (Generation & Guardrails):** Cited answers generated; PII & hallucination guardrails block invalid payloads.
- **Day 5 (End-to-End Evaluation):** Unattended evaluation harness runs full validation set and outputs metrics report.

---

## 3. Scope Fallback Strategy
If time constraints or provider rate-limits occur:
1. **Primary Drop Candidate:** Complex multi-turn chat memory (preserve single-turn high-accuracy ticket resolution).
2. **Non-Negotiable Core:** Multi-channel ingest, RAG retrieval with citations, deterministic routing threshold, guardrails blocking, and decision logging (A1–A12 compliance).
