# CloudServe AI Support System — Evaluation Metrics Report

**Run Date:** 2026-09-20T06:14:34.149518  
**Input Dataset:** `Capstone_Pack/05_Datasets/validation_tickets.json`  
**Total Tickets Processed:** 80  
**Total Duration:** 298.46 seconds  

---

## 1. Volume Breakdown
- **Total Processed:** 80
- **Answered Automatically:** 44 (55.0%)
- **Escalated to Tier 2:** 36 (45.0%)
- **Blocked by Guardrails:** 0

---

## 2. Business Outcomes vs Targets
| Metric | Baseline Today | Target | Achieved | Status |
|--------|---------------|--------|----------|--------|
| First Contact Resolution (FCR) | 42.0% | >= 60.0% | **55.0%** | CHECK |
| Escalation Rate | 58.0% | <= 30.0% | **45.0%** | CHECK |
| Response Latency (p95) | 8-12 hours | < 3.0 sec | **8.57 sec** | PASS |

---

## 3. Technical Performance
- **Intent Classification Accuracy:** 78.75% (Target >= 85.0%)
- **Retrieval Hit Rate:** 56.25%
- **Median Latency (p50):** 3043.99 ms
- **95th Percentile Latency (p95):** 8573.56 ms

---

## 4. Governance & Auditability
- **Decisions Logged:** 80 / 80 (100% Coverage)
- **PII Leakage Events:** 0 (PASSED)
- **Guardrail Activations:** {}
