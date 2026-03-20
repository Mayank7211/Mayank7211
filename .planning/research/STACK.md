# Technology Stack

**Project:** AI Assistant Builder for Local Businesses (brownfield)
**Researched:** 2026-03-21
**Question:** Standard 2025 stack for this domain, and what this project should keep/adopt next

## Recommended Direction (Current vs Next)

| Layer | Current in Project | Recommended Next | Rationale | Confidence |
|---|---|---|---|---|
| API/backend | FastAPI + SQLAlchemy + Pydantic | Keep FastAPI; standardize async DB/session patterns and typed contracts | This is still a mainstream high-velocity Python API stack, already aligned with your codebase and tenant API model. No rewrite needed. | HIGH |
| Frontend/admin | React + Vite + TypeScript | Keep React + Vite; tighten component/API typing and error boundaries | This remains standard for SaaS dashboards and keeps onboarding speed high for brownfield evolution. | HIGH |
| Widget runtime | Plain JS widget + backend embed config | Keep widget architecture; add versioned widget delivery + backward-compatible config schema | Embedded chat for SMB websites is a domain fit; stability/versioning matters more than framework churn. | HIGH |
| Primary DB | PostgreSQL + SQL schema | Keep PostgreSQL as system of record | Best fit for multi-tenant transactional + analytics + reservation workflows already in place. | HIGH |
| Vector retrieval | Doc parsing + DB storage (no first-class vector strategy documented) | Adopt pgvector in Postgres for embeddings + hybrid retrieval (vector + full-text) | Domain standard in 2025 is "keep vectors near operational data" for small/medium SaaS. pgvector gives ANN indexes (HNSW/IVFFlat) without extra datastore ops burden. | HIGH |
| LLM provider integration | Groq-specific gateway | Move to a provider gateway (LiteLLM) with OpenAI-compatible response shape; keep Groq as one routed provider | Standard practice is multi-provider routing/fallback/cost controls to avoid outages and lock-in. LiteLLM provides unified API, routing, spend tracking hooks, and gateway model. | MEDIUM-HIGH |
| LLM API shape | Chat-style gateway patterns | Adopt Responses-style orchestration abstraction for new flows (tool-capable, state-ready), keep legacy chat paths during migration | OpenAI explicitly positions Responses as future direction and Assistants API is deprecated (sunset 2026-08-26). Build internal adapter around tool-calling items, not provider-specific chat DTOs. | HIGH |
| Tool use + agent loop | Tenant-aware prompting + custom flow | Introduce explicit tool-runtime contract (JSON schema strictness) and provider-agnostic tool interface | Both OpenAI and Anthropic center tool use/MCP patterns in production agent workflows. Standard stack now assumes tool contracts as first-class. | HIGH |
| Orchestration runtime | Custom service logic | Adopt lightweight workflow engine boundary; use LangGraph only for long-running/stateful/human-in-loop paths | LangGraph is strong for durable stateful agents, but not required for every request. Use it selectively where durability/interruptibility adds real product value. | MEDIUM |
| Async jobs | Sync/API-path heavy operations; email flow still incomplete | Add Redis-backed job queue for reservation emails, document processing, retries, dead-letter handling. Start with RQ (or Dramatiq) for simplicity. | Reservation notification reliability is core product value. RQ has low barrier; Dramatiq is simple/reliable. Celery is powerful but heavier operationally for this product stage. | MEDIUM-HIGH |
| Observability | Basic analytics endpoints | Add OpenTelemetry traces/metrics/log correlation + AI-specific tracing (LangSmith or equivalent) + error monitoring (Sentry) | OTel remains the vendor-neutral baseline; AI traces/evals are now table stakes for debugging tool-calling and retrieval quality. | HIGH |

## Prescriptive Stack (What To Keep vs Adopt)

### Keep (do not rewrite)

1. FastAPI + SQLAlchemy + Pydantic backend foundation.
2. React + Vite admin UI.
3. PostgreSQL as primary transactional store.
4. Existing embeddable widget model and onboarding flow.

### Adopt Next (this milestone and next)

1. Add pgvector to Postgres and move knowledge retrieval to hybrid search.
2. Introduce model gateway layer (LiteLLM or equivalent) with:
   - provider routing (Groq + at least one backup provider),
   - budget/rate controls per tenant,
   - standardized request/response envelope.
3. Introduce Responses-style/tool-first internal API contract for new assistant flows.
4. Implement Redis-backed background jobs for reservation notifications and ingestion pipelines.
5. Instrument end-to-end traces (chat request -> retrieval -> model/tool calls -> reservation side effects).

## What NOT To Use (for this project stage)

1. Do not build a custom vector search engine.
Reason: pgvector already provides exact + ANN search (HNSW/IVFFlat), filtering strategies, and Postgres-native operations.

2. Do not remain single-provider (Groq-only) at the gateway layer.
Reason: Reliability, regional outages, model drift, and pricing changes are business risks for SMB-facing assistants.

3. Do not start net-new features on deprecated Assistants API patterns.
Reason: OpenAI states Responses API is the future direction and Assistants API has a published deprecation/sunset timeline.

4. Do not introduce Celery first unless workflow complexity truly requires it.
Reason: Great tool, but operationally heavier than needed for your near-term queue use cases; start with simpler Redis queue stack.

5. Do not keep SQLite fallback paths in production-grade multi-tenant environments.
Reason: It weakens operational consistency, migration discipline, and incident handling for tenant-critical reservation data.

## Recommended Versions / Targets

- Python: 3.11+
- FastAPI: stay on current minor train, upgrade regularly
- SQLAlchemy: 2.0.x stable line
- PostgreSQL: current supported major (17/18)
- pgvector: current 0.8.x line
- Node.js: align frontend tooling to current Vite-supported LTS baseline
- Redis: current stable 7+

## Confidence By Major Recommendation

| Recommendation | Confidence | Why |
|---|---|---|
| Keep FastAPI/React/Postgres brownfield core | HIGH | Strong fit for existing architecture and still mainstream for this SaaS domain. |
| Adopt pgvector in Postgres for retrieval | HIGH | Official pgvector capabilities + broad deployment pattern for app+vector colocation. |
| Move to provider gateway + multi-provider routing | MEDIUM-HIGH | Strong docs support and clear operational benefits; exact vendor choice can vary. |
| Shift new flows to Responses/tool-first abstraction | HIGH | Official OpenAI direction and deprecation timeline are explicit. |
| Add Redis-backed async job system now | MEDIUM-HIGH | Clear need from reservation reliability; queue implementation choice (RQ vs Dramatiq) is context-dependent. |
| Use LangGraph for selective long-running workflows | MEDIUM | Technically strong and documented, but adoption depth depends on product complexity trajectory. |
| Standardize on OTel + AI tracing | HIGH | Vendor-neutral observability standard with strong ecosystem support. |

## Sources

- Project context: `.planning/PROJECT.md`
- Existing stack map: `.planning/codebase/STACK.md`
- OpenAI Responses migration + deprecation notes: https://developers.openai.com/api/docs/guides/migrate-to-responses
- OpenAI tools guide: https://developers.openai.com/api/docs/guides/tools
- OpenAI embeddings guide: https://developers.openai.com/api/docs/guides/embeddings
- LangGraph overview: https://docs.langchain.com/oss/python/langgraph/overview
- LangSmith docs: https://docs.langchain.com/langsmith/home
- LiteLLM docs: https://docs.litellm.ai/docs/
- pgvector docs/repo: https://github.com/pgvector/pgvector
- OpenTelemetry docs: https://opentelemetry.io/docs/
- Sentry Insights docs: https://docs.sentry.io/product/insights/
- RQ docs: https://python-rq.org/
- Dramatiq docs: https://dramatiq.io/
- Celery docs (tradeoff reference): https://docs.celeryq.dev/en/stable/getting-started/introduction.html
- FastAPI docs: https://fastapi.tiangolo.com/
- Vite docs: https://vite.dev/guide/
- PostgreSQL docs: https://www.postgresql.org/docs/current/index.html
- SQLAlchemy release/docs page: https://www.sqlalchemy.org/
- Anthropic tool use docs: https://platform.claude.com/docs/en/docs/build-with-claude/tool-use
