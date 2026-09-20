# 🎙️ Video Presentation Script & Walkthrough Guide
**Project:** CloudServe Solutions Intelligent Customer Support System  
**Presenter:** Vishwanath D Doddamani  
**Target Duration:** 18 – 22 Minutes (Ideal Target: 20:00)  
**File Output Name:** `VishwanathDDoddamani_Capstone_Video.mp4` (Format: MP4, 1080p, Clear Audio)

---

## 📋 Pre-Recording Checklist & Video Guidelines
> [!IMPORTANT]
> - **Camera Requirement:** You must be on camera during the **Introduction (0:00–2:00)** and **Closing (18:00–20:00)**.
> - **Screen Legibility:** Increase your terminal font size (`Cmd +` in VS Code / iTerm) and IDE text size so code and JSON payloads are easily readable on 1080p playback.
> - **Live Demo Requirement:** At least 7 minutes (7:00–14:00) **MUST** show the system actually running on real tickets, including an auto-answer, an escalation, a guardrail block, and the unattended harness run.
> - **Two-Take Strategy:** Record Take 1 to check pacing. If it runs to ~25 minutes, tighten your script and record Take 2.

---

## ⏱️ Minute-by-Minute Master Schedule

| Timecode | Section | Focus & Key Deliverables | Screen Mode |
| :--- | :--- | :--- | :--- |
| **0:00 – 2:00** | **1. The Problem** | Client request vs. real problem, discovery finding, strategic value | **Presenter on Camera** |
| **2:00 – 5:00** | **2. Discovery Findings** | Persona evidence (Marcus, Sofia, Daniel, Ines, Ravi), ticket analysis | **Slides / PDF Report** |
| **5:00 – 7:00** | **3. System Architecture** | 6-stage pipeline walkthrough, SQLite decision audit logging | **Architecture Diagram** |
| **7:00 – 14:00** | **4. Live Demonstration** | Auto-answer, escalation payload, PII guardrail block, unattended run | **IDE / Terminal Live** |
| **14:00 – 17:00** | **5. What the Numbers Say** | Business outcomes (55% FCR), technical metrics (2.23s p95), fairness | **Evaluation Tables / Charts** |
| **17:00 – 18:00** | **6. Governance & Safety** | Risk mitigations (RSK-01–05), kill switch demonstration | **Governance / Code** |
| **18:00 – 20:00** | **7. Lessons & Next Steps** | PRD v1.0 $\rightarrow$ v2.0 revisions, future roadmap, closing summary | **Presenter on Camera** |

---

## 🎬 Detailed Section-by-Section Speaker Script

### 📍 Section 1: The Problem & Client Misalignment (0:00 – 2:00)
**Visual:** Presenter on camera (Full Screen or Picture-in-Picture).  
**Goal:** Hook the viewer, explain what CloudServe asked for vs. what you found, and state why the difference matters.

#### Talking Points:
- **Introduction:** "Hello, I'm Vishwanath D Doddamani, and today I'm presenting the Forward Deployed AI Engineering Capstone for CloudServe Solutions."
- **The Client's Request:** CloudServe initially believed their support team was drowning due to a lack of documentation and insufficient agent bandwidth, asking for a generic LLM chatbot to handle incoming queries.
- **The Core Discovery Finding:** Upon analyzing the dataset of 500 support tickets (`development_tickets.json`), I discovered that **71.4% (357 out of 500)** of all tickets were already fully answerable from the existing 29 knowledge base articles (`documentation.json`).
- **Why it Matters:** The problem was not a content shortage—it was a **search findability and routing bottleneck**. Customers couldn't find answers via keyword search, forcing repetitive routine tickets into human queues.
- **The Solution Overview:** Rather than a simple LLM wrapper, we designed an enterprise-grade RAG pipeline with calibrated confidence thresholds, deterministic safety routing, guardrails, and full audit logging.

---

### 📍 Section 2: What Discovery Told Us (2:00 – 5:00)
**Visual:** Display **Stage 1 Discovery Workbook** or Report Section 2 (Tables & Persona Matrix).  
**Goal:** Show deep domain understanding, cite evidence IDs, and present persona constraints.

#### Talking Points:
- **Multi-Channel Distribution:**
  - Analyzed 500 tickets across four channels: **Email (42.4%)**, **Chat (31.0%)**, **Docs Comments (15.6%)**, and **Forum (11.0%)**.
  - Show how channel format dictates response urgency and tone (e.g., synchronous chat demands sub-3s latency).
- **Stakeholder Personas & Key Evidence (Cite EVD IDs):**
  - **Marcus Vance (VP Ops - EVD-01):** Demanded First Contact Resolution (FCR) increase from 35% to 40%+, and reduction in $18/ticket handling cost.
  - **Sofia Patel (Support Lead - EVD-02):** Reported severe agent burnout from answering basic password and billing API questions repeatedly.
  - **Daniel Kim (Escalation Mgr - EVD-03):** Imposed **hard escalation rules**—any ticket involving data loss, security vulnerabilities, or SLA breach threats must NEVER be auto-answered by AI.
  - **Ines Rivera (Compliance - EVD-04):** Demanded zero PII leaks, 100% audit logging, and strict data privacy compliance.
  - **Ravi Kumar (IT Infrastructure - EVD-05):** Set a operational constraint of max 500 daily ticket processing overhead and sub-3s response time for chat.

---

### 📍 Section 3: System Architecture (5:00 – 7:00)
**Visual:** Display **Architecture Diagram** (Figure from Report Section 4).  
**Goal:** Explain the technical pipeline clearly for a non-technical stakeholder.

#### Talking Points:
- **Walkthrough of the 6-Stage Pipeline:**
  1. **Ingest Layer (`src/ingest.py`):** Normalizes inputs from Email, Chat, Docs, and Forum into a unified `Ticket` schema with language fluency metadata.
  2. **Intent Classifier (`src/classify.py`):** Categorizes tickets into 22 intents, assigns urgency, and calculates a calibrated float confidence score.
  3. **Vector Retriever (`src/retrieve.py`):** Uses Chroma DB with `all-MiniLM-L6-v2` embeddings over 29 documentation articles, enforcing a **0.35 similarity score threshold**.
  4. **Deterministic Router (`src/route.py`):** Applies Daniel's hard escalation rules and compares classification confidence against a strict **0.80 confidence threshold**.
  5. **Grounded Generator (`src/generate.py`):** Synthesizes grounded RAG responses using retrieved passages and strictly enforces inline citations like `[DOC-AUTH-001]`.
  6. **Guardrails Suite (`src/guardrails.py`):** Scans for PII (credit cards, API keys, tokens), hallucinated document IDs, and toxic tone before sending responses.
- **Audit Logging Layer (`src/logging_store.py`):** Persists 100% of pipeline decisions, execution latencies, and requirement IDs into SQLite (`storage/decisions.db`).

---

### 📍 Section 4: Live System Demonstration (7:00 – 14:00) ⚡ *CRITICAL SECTION*
**Visual:** VS Code Terminal / Terminal Window (Large legible font).  
**Goal:** Demonstrate live processing of test cases: Auto-answer, Escalation, Guardrail Block, and Unattended Run.

#### Demo Step 1: Successful Auto-Answer (7:00 – 8:45)
- **Action:** Run a sample query through the pipeline:
  ```bash
  python3 -c "from src.api import process_ticket; print(process_ticket({'ticket_id': 'TCK-DEMO-01', 'channel': 'Email', 'customer_id': 'CUST-101', 'subject': 'Resetting API Key', 'body': 'How do I rotate my production API keys in CloudServe dashboard?', 'timestamp': '2026-09-10T10:00:00Z'}))"
  ```
- **Explain Output:** Point out classification (`AUTH_API_KEY`), confidence score ($\ge 0.80$), retrieved document (`DOC-AUTH-001`), generated response, correct inline citation `[DOC-AUTH-001]`, and status `AUTO_ANSWER`.

#### Demo Step 2: Escalation Trigger (8:45 – 10:30)
- **Action:** Pass a data-loss or low-confidence ticket:
  ```bash
  python3 -c "from src.api import process_ticket; print(process_ticket({'ticket_id': 'TCK-DEMO-02', 'channel': 'Chat', 'customer_id': 'CUST-202', 'subject': 'Database Loss Emergency', 'body': 'Our primary cluster is dropping tables automatically and we have data loss!', 'timestamp': '2026-09-10T10:05:00Z'}))"
  ```
- **Explain Output:** Highlight that Daniel's hard escalation rule immediately intercepted the ticket (`DATA_LOSS` intent), set status to `ESCALATED`, and generated an `EscalationPayload` with full context for the tier-2 human agent.

#### Demo Step 3: PII Guardrail Block (10:30 – 12:00)
- **Action:** Pass a ticket containing a sensitive credential:
  ```bash
  python3 -c "from src.api import process_ticket; print(process_ticket({'ticket_id': 'TCK-DEMO-03', 'channel': 'Email', 'customer_id': 'CUST-303', 'subject': 'My key is sk-or-v1-99af88bcd123', 'body': 'Here is my active bearer token sk-or-v1-99af88bcd123 please fix my account', 'timestamp': '2026-09-10T10:10:00Z'}))"
  ```
- **Explain Output:** Point out how `src/guardrails.py` detected the hyphenated API key (`sk-or-v1-...`), triggered a `BLOCK` status, prevented response generation, and logged the governance alert.

#### Demo Step 4: Unattended Evaluation Run (12:00 – 14:00)
- **Action:** Execute the unattended harness across the validation dataset:
  ```bash
  python3 evaluation/harness.py --input data/validation_tickets.json --output evaluation/results/metrics_report.json
  ```
- **Explain Output:** Show the evaluation progress bar processing all 80 validation tickets in single-run mode. Open `evaluation/results/metrics_report.md` to show 100% completion with 0 manual interventions.

---

### 📍 Section 5: What the Numbers Say — Metrics & Business Impact (14:00 – 17:00)
**Visual:** Display Report Section 5 (Evaluation Metrics Tables & Charts).  
**Goal:** Present business, technical, and governance results clearly.

#### Talking Points:
- **Business Impact:**
  - **First Contact Resolution (FCR):** Achieved **55.0%** auto-answer rate, significantly exceeding the client's 40% target.
  - **Human Workload Reduction:** Reduces agent workload by **~55%**, saving an estimated **3,000+ staff hours annually**.
  - **Cost per Ticket:** Average processing cost lowered to **$0.007 per ticket** (compared to $18.00 human handling cost).
- **Technical Performance:**
  - **Latency:** Synchronous chat p95 latency reached **2.23 seconds** (well within the <3.0s NFR requirement).
  - **Classification Accuracy:** **82.5%** top-1 intent precision across 22 categories.
  - **Test Suite:** **22 out of 22 Pytest unit/integration tests** passing (100% test coverage for acceptance criteria A1–A12).
- **Governance & Fairness Metrics:**
  - **PII Leak Rate:** **0.0%** (0 leaks across all test runs).
  - **Hallucination Rate:** **0.0%** (all responses strictly grounded with valid citation checks).
  - **Demographic Fairness Audit:** Evaluated across 5 user fluency levels; maximum FCR variance across groups was **<2.8 percentage points**, well below the <5.0% bias threshold.

---

### 📍 Section 6: Governance, Risk & Safety Controls (17:00 – 18:00)
**Visual:** Display **Risk Register Table** & Code snippet of `CONFIDENCE_THRESHOLD`.  
**Goal:** Show how enterprise risk is managed and demonstrate the system kill switch.

#### Talking Points:
- **Risk Management (RSK-01 to RSK-05):**
  - **RSK-01 (PII Exposure):** Mitigated by pre-generation and post-generation regex guardrails.
  - **RSK-02 (Outdated KB Info):** Mitigated by passage metadata versioning and similarity score cutoff (0.35).
  - **RSK-03 (Model Hallucination):** Mitigated by strict grounding prompt + fallback citation validator.
- **System Emergency Kill Switch:**
  - Demonstrate how setting environment variable `CONFIDENCE_THRESHOLD=1.00` forces **100% immediate escalation** to human agents in case of LLM provider instability.

---

### 📍 Section 7: Lessons Learned & What We'd Do Next (18:00 – 20:00)
**Visual:** Presenter on camera (Full Screen).  
**Goal:** Summarize key insights, reflect on PRD revisions, discuss future enhancements, and conclude professionally.

#### Talking Points:
- **PRD v1.0 $\rightarrow$ v2.0 Revision Insights:**
  - During mid-sprint testing, we observed that a 0.70 confidence threshold allowed borderline tickets (0.72–0.78) to auto-answer with low-quality grounding.
  - We updated PRD v2.0 to raise the routing threshold to **0.80** and added a **0.35 similarity cutoff** in vector retrieval. This eliminated unsupported claims entirely.
- **Future Roadmap:**
  - Implement **Hybrid Search (BM25 + Dense Vector Embeddings)** to improve exact keyword matching for specific product error codes.
  - Build an **Agent Feedback Loop** allowing tier-2 support agents to vote on escalation quality directly inside SQLite log stores.
- **Closing Statement:**
  - "The CloudServe Intelligent Support System demonstrates how rigorous engineering, evidence-based discovery, and strict safety guardrails can transform customer support operations. Thank you for your time."

---

## 💡 Top Recording Tips for a High-Scoring Video
1. **Pacing:** Keep a steady, confident cadence. Don't rush through the demo section.
2. **Audio Quality:** Use an external microphone or headset if available. Ensure no background noise.
3. **Cursor Highlights:** Highlight lines of code or terminal outputs with your mouse as you explain them.
4. **File Check:** After recording, verify the output file is named `VishwanathDDoddamani_Capstone_Video.mp4`, plays smoothly, and audio is clear throughout.
