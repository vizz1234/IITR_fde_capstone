# CloudServe Solutions — Intelligent Customer Support AI System

An enterprise-grade, RAG-powered customer support triage, classification, routing, grounded answer generation, guardrail validation, and decision logging system for CloudServe Solutions. Built as a Forward Deployed AI Engineering Capstone Project for IIT Roorkee.

---

## 1. Quick Start & Setup Instructions (Acceptance Criterion A1)

### Prerequisites
- Python 3.10 or later (`python3 --version`)
- Git (`git --version`)

### Step 1: Clone & Setup Virtual Environment
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate    # On macOS/Linux
# .venv\Scripts\activate     # On Windows
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
```bash
cp .env.example .env
```
Edit `.env` and add your API Key (e.g., `OPENROUTER_API_KEY=sk-or-v1-...`).  
*Note: If no API key is provided or `USE_MOCK_LLM=true` is set, the system automatically falls back to an offline Mock provider, allowing 100% offline, cost-free execution.*

---

## 2. Running the System & Web API

### Start the FastAPI Web Server & Interactive Docs
```bash
python -m src.api
```
- **API Server Base URL:** `http://localhost:8000`
- **Interactive Swagger Web UI:** `http://localhost:8000/docs`
- **Prometheus Metrics Endpoint:** `http://localhost:8000/metrics`

### Run the Visual Terminal CLI Demonstration
```bash
python3 demo.py
```
*Executes a live 5-ticket pipeline demonstration showing classification, RAG vector retrieval, routing rationale, grounded generation with citations, PII guardrail blocks, and latency timing.*

---

## 3. Running Unattended Evaluation (Acceptance Criteria A9 & A10)

Process any ticket dataset (e.g. `validation_tickets.json` or hidden evaluation sets) unattended in a single command:

```bash
python -m evaluation.harness --input Capstone_Pack/05_Datasets/validation_tickets.json --output evaluation/results/
```

### Output Reports Generated
- `evaluation/results/metrics_report.json`: Detailed Volume, Business, Technical, and Governance metrics.
- `evaluation/results/metrics_report.md`: Markdown summary report.

---

## 4. Running Automated Tests (Acceptance Criteria A12)

Run the complete Pytest suite (22 unit & integration tests) covering all 12 acceptance criteria:

```bash
pytest
```
*All 22 test cases pass in under 20 seconds.*

---

## 5. Acceptance Criteria Checklist Compliance

| Criteria ID | Description | Implementation / Verification Command | Status |
|-------------|-------------|---------------------------------------|--------|
| **A1** | Clean checkout startup following README | `pip install -r requirements.txt` | **PASS** |
| **A2** | Ingest tickets from 4 channels (Email, Chat, Docs, Forum) | `src/ingest.py` & `pytest tests/test_ingest.py` | **PASS** |
| **A3** | Intent & Urgency classification with numeric confidence | `src/classify.py` & `pytest tests/test_classify.py` | **PASS** |
| **A4** | Vector store RAG retrieval over documentation | `src/retrieve.py` & `pytest tests/test_retrieve.py` | **PASS** |
| **A5** | Deterministic threshold routing | `src/route.py` & `pytest tests/test_route.py` | **PASS** |
| **A6** | Grounded answers carrying verifiable doc citations | `src/generate.py` & `pytest tests/test_generate.py` | **PASS** |
| **A7** | Guardrail blocks invalid/PII responses | `src/guardrails.py` & `pytest tests/test_guardrails.py` | **PASS** |
| **A8** | Persistent SQLite decision log database | `src/logging_store.py` & `pytest tests/test_logging.py` | **PASS** |
| **A9** | Full evaluation set processed unattended | `python -m evaluation.harness --input ...` | **PASS** |
| **A10** | Unattended run produces comprehensive metrics report | `evaluation/results/metrics_report.json` | **PASS** |
| **A11** | Failure resilience & model outage degradation | `src/llm.py` & `pytest tests/test_resilience.py` | **PASS** |
| **A12** | Tests run with single documented command and pass | `pytest` | **PASS** |

---

## 6. Project Architecture, Reports & Workbooks

- **CapTone Project Report:**
  - `docs/Capstone_Project_Report.html` (Interactive HTML UI with dark theme, embedded architecture diagrams & performance charts)
  - `docs/Capstone Project Report — CloudServe AI Support System _ IIT Roorkee FDE.pdf` (Official 24-page PDF Report)
- **Effort Log & Time Tracking:**
  - `docs/Effort_Log.html` (Official HTML Effort Log following `Effort_Log.docx` template layout)
  - `docs/Effort Log — Vishwanath D Doddamani _ FDE Capstone.pdf` (Signed 85-hour PDF Effort Log)
  - `docs/Effort_Log.md` (Stage-by-stage effort tracking markdown)
- **Video Presentation Script:**
  - `docs/Video_Presentation_Script.md` (20-minute video presentation speaker script with timestamps & terminal commands)
- **Stage Workbooks:**
  - `docs/Stage_1_Discovery_Workbook.md`: Stakeholder interview analysis & dataset evidence.
  - `docs/Stage_2_PRD.md`: Functional & Non-functional product requirements (F1–F12).
  - `docs/Stage_3_Prompt_Library.md`: Prompt specifications, versioning, and register.
  - `docs/Stage_4_Sprint_Plan.md`: Sprint backlog and DoD.
  - `docs/Stage_5_PRD_Revision_Log.md`: Mid-sprint PRD revisions (v1.0 $\rightarrow$ v2.0).
  - `docs/Governance_Framework.md`: Decision log schema, Risk Register, Fairness Audit, Incident Runbook, Kill Switch.

---

## 7. Submission Package Generation

To package the project into the required 4-folder submission layout (`01_Video`, `02_Report`, `03_Workbooks`, `04_Source_Code`):

```bash
python prepare_submission_package.py --name VishwanathDDoddamani
```

Creates the submission archive: `VishwanathDDoddamani_Capstone_Submission.zip`.
