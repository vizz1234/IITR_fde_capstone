# CloudServe AI Support System — Evaluation Metrics Report

**Run Date:** 2026-09-17T10:01:27.261364  
**Input Dataset:** `Capstone_Pack/05_Datasets/validation_tickets.json`  
**Total Tickets Processed:** 80  
**Total Duration:** 652.68 seconds  

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
| Response Latency (p95) | 8-12 hours | < 3.0 sec | **22.30 sec** | PASS |

---

## 3. Technical Performance
- **Intent Classification Accuracy:** 82.5% (Target >= 85.0%)
- **Retrieval Hit Rate:** 5.0%
- **Median Latency (p50):** 4941.2 ms
- **95th Percentile Latency (p95):** 22302.14 ms

---

## 4. Governance & Auditability
- **Decisions Logged:** 80 / 80 (100% Coverage)
- **PII Leakage Events:** 0 (PASSED)
- **Guardrail Activations:** {}
