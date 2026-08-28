# CardinalOps

**A multi-agent assistant for University of Louisville students — built in public, in active development.** 🚧

CardinalOps answers real campus questions — degree requirements, IT helpdesk triage, campus events — by orchestrating specialized AI sub-agents over real tools. Every answer ships with its execution trace: which agents ran, which tools they called, which model handled each step, and what it cost.

The project is a working demonstration of four production patterns for modern agentic systems:

1. **Orchestrator / sub-agent architecture** — a planner routes queries to specialists with dedicated context
2. **Tool use via MCP** — capabilities exposed through a Model Context Protocol server, not hardcoded functions
3. **Hybrid model routing** — routine steps go to a cheap open-weight model; hard reasoning escalates to a frontier API, with per-step cost logging
4. **Observability-first UI** — a Next.js dashboard surfaces traces and cost breakdowns as first-class features

Full architecture, component design, and scope: **[docs/spec.md](docs/spec.md)**

## Roadmap

- [x] **M1 — Scaffold:** Next.js 15 app (`web/`) + FastAPI skeleton (`api/`), repo hygiene, CI
- [ ] **M2 — Chat slice:** end-to-end chat through the orchestrator to a frontier model, trace events streamed to the UI
- [ ] **M3 — KnowledgeAgent:** RAG over public UofL pages, sources cited in answers
- [ ] **M4 — Model router:** open-weight + frontier routing with per-step cost logging
- [ ] **M5 — MCP server:** tools moved behind MCP; HelpdeskAgent added
- [ ] **M6 — Dashboard polish + deploy:** trace viewer, cost charts, hosted demo

## Stack

**Frontend:** Next.js 15 (App Router) · TypeScript (strict) · Tailwind CSS
**Backend:** FastAPI · Python 3.12 (uv-managed) · LangChain/LangGraph *(from M2)* · MCP Python SDK *(from M5)*
**Storage:** SQLite for traces (v1)

## Development

```bash
# Frontend — http://localhost:3000
cd web
npm install
npm run dev

# Backend — http://localhost:8000/health
cd api
uv sync
uv run uvicorn main:app --reload

# Tests & checks
cd web && npm run lint && npm run build
cd api && uv run pytest
```

Every API response uses a shared envelope — `{ data, error, trace_id }` (`api/schemas.py`) — so observability is wired in from the first endpoint.

## Workflow

Developed with a feature-branch/PR workflow (no direct commits to `main`), CI on every PR, and AI-assisted development via Claude Code with project conventions defined in [CLAUDE.md](CLAUDE.md).

---
*Ali Zain Kaimkhani · MS Computer Science, University of Louisville*