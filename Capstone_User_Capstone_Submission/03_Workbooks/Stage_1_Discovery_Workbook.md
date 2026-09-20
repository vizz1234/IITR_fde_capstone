# Stage 1 — Discovery Workbook

**Client:** CloudServe Solutions  
**Project:** Intelligent Customer Support Triage & Automation System  
**Author:** Forward Deployed AI Engineer  
**Date:** September 2026  

---

## 1. Stakeholder Interviews Summary

Five discovery interviews were conducted across key organizational roles to uncover operational bottlenecks, systemic risks, and unstated requirements.

| Stakeholder | Role & Tenure | Key Discovery Insight | Stated Risk / Constraint |
|-------------|---------------|----------------------|---------------------------|
| **Marcus Adeyemi** | Head of Support (4 yrs) | Support queue volume (>500/week) is overwhelming 6 agents; response SLA (2h) breached at 8–12h. FCR is 42% (industry benchmark 65%). Bounced tickets cost ~4x resolved ones. | Prefers silence over confident incorrect answers; enterprise SLA compliance; autumn compliance audit. |
| **Sofia Restrepo** | Tier 1 Support Agent (14 mos) | ~70% of tickets are repeat issues (passwords, rate limits, invoices, rollbacks). Knowledge base search is ineffective, so agents use fragmented personal snippet files. Non-fluent English tickets take double time and suffer lowest CSAT. | Fears picking up angry customer follow-ups from incorrect automated responses. Desires drafted context + attached doc pages. |
| **Daniel Okonkwo** | Tier 2 Support Engineer (3 yrs) | ~50% of escalations reaching Tier 2 are findability/confidence issues solvable by Tier 1. Escalated tickets lack context (no summary or tried steps). | Personal snippet files across agents contain outdated answers (scale up mistakes). Security, billing disputes, and data residency must never be automated. |
| **Ines Varga** | Technical Writer (2 yrs) | 29 knowledge base articles cover key topics, but internal search fails due to keyword mismatch (e.g., "deployment keeps dying" vs "resolving container health check failures"). | Needs clear document citation mapping to distinguish doc defects from system reading errors. |
| **Ravi Menon** | Customer (Platform Lead) | Waiting for responses is acceptable for low-urgency queries (pagination), but catastrophic for active deployment failures. | Wants honest machine transparency ("machine-drafted") and zero hallucinated confidence. |

---

## 2. Ticket Dataset Quantitative Analysis

Analysis of 500 labeled tickets in `development_tickets.json`:

- **Total Ticket Volume:** 500 tickets
- **Channel Distribution:**
  - Email: 212 tickets (42.4%) — longest, most complex
  - Live Chat: 155 tickets (31.0%) — strictest latency demand (<3 sec)
  - Documentation Comments: 78 tickets (15.6%) — narrow, highly technical
  - Community Forum: 55 tickets (11.0%) — asynchronous, multi-party
- **Document Answerability:** 357 / 500 tickets (**71.4%**) are fully answerable from the 29 documentation articles in `documentation.json`.
- **Primary Bottlenecks Identified:**
  1. Search Keyword Mismatch: Keyword-only search fails on natural customer phrasing.
  2. Fragmented Personal Answer Snippets: Outdated local agent snippets cause inconsistent answers.
  3. Context-Free Escalation: Tier 2 engineers spend ~50% of time re-investigating escalations.

---

## 3. Core Problem Statement

> CloudServe Solutions' support operation is failing to meet its 2-hour response SLA (averaging 8–12 hours) and achieving only 42% First Contact Resolution (FCR) not because of a shortage of technical answers, but because 71.4% of incoming tickets query information already documented in their 29 knowledge base articles, which agents and customers cannot find due to keyword search mismatch and fragmented personal snippet files. This results in unnecessary, context-free escalations to Tier 2 engineers and falling customer satisfaction (3.2/5).

---

## 4. Evidence Traceability Table

| Finding ID | Evidence Source | Problem Observed | Solution Implication |
|------------|-----------------|------------------|----------------------|
| `EVD-01` | Marcus Interview & Ticket Data | FCR at 42%, SLA breach (8–12h), 71.4% doc-answerable tickets | Implement RAG auto-answering with high confidence threshold |
| `EVD-02` | Sofia & Ines Interviews | Keyword search fails on customer phrasing | Dense vector embeddings (`all-MiniLM-L6-v2`) for semantic search |
| `EVD-03` | Daniel Interview | Context-free escalations cost Tier 2 time | Structured escalation payload with summary & retrieved docs |
| `EVD-04` | Daniel & Marcus Interviews | Security/billing/data residency risks | Mandatory escalation routing rules & zero PII guardrails |
| `EVD-05` | Ravi & Sofia Interviews | Low-fluency English tickets have poor CSAT | Normalization layer with language fluency preservation |
