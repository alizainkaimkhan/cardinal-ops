# CardinalOps — Project Specification

**Status:** Draft v0.1 · **Author:** Ali Zain Kaimkhani · **Last updated:** 2026-08-27

## 1. Vision

A multi-agent assistant for University of Louisville students that answers real campus questions — degree requirements, registration rules, IT helpdesk triage, campus events — by orchestrating specialized sub-agents over real tools, with transparent traces showing exactly which agents ran, which tools they called, which model handled each step, and what it cost.

The project demonstrates four production patterns for 2026-era agentic systems:
1. **Orchestrator / sub-agent architecture** — a planner routes queries to specialists with dedicated context.
2. **Tool use via MCP** — capabilities exposed as a Model Context Protocol server, not hardcoded functions.
3. **Hybrid model routing** — a cost-aware router sends routine steps to a cheap open-weight model and escalates hard reasoning to a frontier API.
4. **Observability-first UI** — every answer ships with its execution trace and cost breakdown.

## 2. Architecture

```text
┌──────────────────────────────────────────────────────┐
│  Next.js Dashboard (App Router, TS, Tailwind)        │
│  Chat panel · Agent trace viewer · Cost/model stats  │
└───────────────▲──────────────────────────────────────┘
                │ REST/SSE
┌───────────────┴──────────────────────────────────────┐
│  FastAPI Backend                                     │
│  ┌────────────┐   ┌──────────────────────────────┐   │
│  │ Orchestrator│──▶│ Model Router                 │   │
│  │ (planner)   │   │ open-weight ⇄ frontier API   │   │
│  └─────┬──────┘   └──────────────────────────────┘   │
│        ▼                                             │
│  ┌───────────────┬──────────────────┐                │
│  │ KnowledgeAgent│ HelpdeskAgent    │  (sub-agents)  │
│  │ RAG over UofL │ ticket triage +  │                │
│  │ public pages  │ draft generation │                │
│  └───────┬───────┴────────┬─────────┘                │
│          ▼                ▼                          │
│  ┌──────────────────────────────────────┐            │
│  │ MCP Server (tools)                   │            │
│  │ search_docs · get_events · draft_    │            │
│  │ ticket · check_service_status        │            │
│  └──────────────────────────────────────┘            │
└──────────────────────────────────────────────────────┘
```

## 3. Components

### 3.1 Orchestrator
Receives the user query, produces a plan (which sub-agent(s), which order), dispatches, and composes the final answer. Emits a structured trace event for every decision.

### 3.2 Sub-agents (vertical slice: two)
- **KnowledgeAgent:** RAG over a small corpus of scraped public UofL pages (registrar, IT services, academic calendar). Chunking + embedding at ingest; retrieval + synthesis at query time.
- **HelpdeskAgent:** classifies IT issues, checks a mock service-status feed, and drafts a support ticket when the issue can't be self-served.

### 3.3 MCP Server
Tools exposed over MCP so any MCP-capable client (including Claude Code) can use them:
`search_docs(query)`, `get_events(date_range)`, `check_service_status(service)`, `draft_ticket(summary, details)`.

### 3.4 Model Router
Policy-based: classification/retrieval/formatting steps → open-weight model via hosted API; planning and final synthesis → frontier model. Logs model, tokens, latency, and estimated cost per step. Router policy is a config file, not code — swappable and demo-able.

### 3.5 Trace & Cost UI
Per-query execution tree (agent → tool calls → model calls), token/cost roll-up per model, and aggregate dashboard (queries by agent, cost by model over time).

## 4. Non-goals (v1)
- No authentication or per-user state
- No writes to real UofL systems (mock ticket sink only)
- No fine-tuning; prompt + retrieval only
- Corpus limited to a handful of public pages, refreshed manually

## 5. Milestones

- [ ] **M1 — Scaffold:** Next.js app + FastAPI skeleton, repo hygiene, CI (lint + build)
- [ ] **M2 — Chat slice:** end-to-end chat through orchestrator to one frontier model, trace events streamed to UI
- [ ] **M3 — KnowledgeAgent:** ingest script + RAG retrieval, sources cited in answers
- [ ] **M4 — Router:** open-weight + frontier routing with per-step cost logging
- [ ] **M5 — MCP server:** tools moved behind MCP; HelpdeskAgent added
- [ ] **M6 — Dashboard polish + deploy:** trace viewer, cost charts, hosted demo, README with architecture diagram and screenshots

## 6. Stack

Next.js 15 (App Router) · TypeScript · Tailwind CSS · Recharts — FastAPI · Python 3.12 · LangChain/LangGraph · MCP Python SDK — SQLite for traces (v1) — deployed: Vercel (frontend) + Railway/Render (API), TBD at M6
