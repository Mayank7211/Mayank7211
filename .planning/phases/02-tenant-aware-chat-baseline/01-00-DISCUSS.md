---
phase: 02-tenant-aware-chat-baseline
plan: 00
type: discuss
autonomous: false
created: 2026-05-22
---

# Phase 2 Discussion: Tenant-Aware Chat Baseline

Purpose: capture stakeholder preferences and unresolved design decisions before planning and implementation.

Please answer the questions below or provide priorities where noted.

1) Success criteria and priority
   - What are the top 3 success metrics for Phase 2 (e.g., median response latency, tenant-context accuracy, conversation continuity rate)?
   - Which is highest priority: low latency, contextual accuracy, reservation detection quality, or cost minimization?

2) Model provider and cost constraints
   - Which model providers are acceptable (Groq, OpenAI, local LLMs, others)?
   - Are there strict cost limits per tenant or per month we must respect?

3) Tenant context retrieval strategy
   - Prefer a simple recent-chunks approach (last N seed/knowledge blocks) or semantic retrieval (pgvector-style embeddings + similarity search)?
   - If semantic retrieval, do we have embeddings storage (pgvector) or must we rely on approximate in-memory ranking for v1?

4) Session & conversation continuity
   - How long must short-term session context persist (in-memory during widget session vs DB retention across visits)?
   - Is cross-device continuity required for v1 or can it be deferred to Phase 3?

5) Reservation intent detection
   - Should reservation detection run on the server after model response, in middleware, or on the client with heuristic prechecks?
   - How aggressive should detection be (precision vs recall)? Which is more important?

6) Rate limits and abuse handling
   - Are the Phase 1 rate limits sufficient (20 req/min chat, 5 req/min upload) or should chat be stricter per tenant for public widgets?
   - Do we want per-IP+tenant and per-API-key quotas for owners?

7) Fallbacks, errors, and observability
   - If the primary provider fails, do we return a graceful fallback message, or a retry-and-inform flow? What telemetry matters (latency, errors, tokens)?

8) Security and privacy constraints
   - Any PI/PHI concerns for tenant knowledge? Must we redact or never store user messages?
   - Is it acceptable to log assistant responses for analytics, or must logging be opt-in per tenant?

9) UI/UX constraints for the widget
   - Preferred behavior for long responses (collapse, show 'more')?
   - Should the widget show a confidence/hand-off suggestion in v1?

10) Acceptance tests and sample scenarios
    - Provide 3 sample conversation scenarios we should include in Wave 0 tests (e.g., appointment booking, pricing inquiry, hours/location question).

11) Timeline and rollout
    - Do you want a staged rollout (owner preview then public) or immediate public availability?

Optional: paste example tenant data (small) for testing: business_name, domain, 3 services, and a short description.

Next steps after answers:
- Produce Phase 2 `01-01-PLAN.md` with prioritized tasks (Wave 1 implementation scaffolding and tests).
- Create Wave 0 PyTest scaffolds in `apps/backend/tests/test_chat_api.py`.
