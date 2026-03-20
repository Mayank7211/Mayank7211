# Project Research Summary

**Project:** AI Assistant Builder for Local Businesses
**Domain:** Multi-tenant SMB AI assistant with chat-to-lead and reservation outcomes
**Researched:** 2026-03-21
**Confidence:** MEDIUM-HIGH

## Executive Summary

This product is a local-business conversion assistant: website chat that captures qualified leads/reservations and reliably notifies owners. The research is consistent that successful products in this category optimize for fast onboarding, trustworthy responses, and dependable owner follow-up rather than broad channel breadth or novelty AI features.

The recommended approach is to keep the existing brownfield core (FastAPI + React + Postgres + widget), then harden it with durable async workflows, stricter tenant security, and observable model/runtime behavior. The highest-value v1 path is to reduce setup friction, capture structured reservation intent, and make notification delivery deterministic.

The biggest risks are trust-breakers: tenant data leakage, missed notifications, and hidden quality degradation from silent model fallback. Mitigation is clear: enforce authz and tenant ownership checks everywhere, implement outbox/retry/dead-letter notification flow, and instrument fallback/latency/quality signals per tenant.

## Key Findings

### Recommended Stack

Keep the current foundation and avoid rewrites.

**Core technologies:**
- FastAPI + SQLAlchemy + Pydantic: keep as canonical backend and standardize typed async patterns.
- React + Vite + TypeScript: keep for admin UX velocity; tighten API/component typing and error boundaries.
- PostgreSQL: keep as system of record for tenant, chat, reservation, and analytics data.
- pgvector in Postgres: add hybrid retrieval (vector + text) without introducing another datastore.
- Provider gateway (LiteLLM-style): move from Groq-only to multi-provider routing/fallback with cost controls.
- Redis-backed worker lane: add durable background jobs for notifications and ingestion retries.
- OpenTelemetry + AI tracing + error monitoring: add end-to-end observability for chat quality and failures.

### Expected Features

**Must have (table stakes):**
- Guided onboarding with sane defaults and progressive setup.
- One-line widget embed with basic branding controls.
- Knowledge ingestion with visible processing state.
- Contact capture and structured reservation/lead intent fields.
- Reliable owner email notifications for high-intent leads.
- Basic analytics: volume, response time, leads, reservations.
- Consent/privacy controls in chat flows.

**Should have (competitive):**
- Vertical playbooks by business type.
- Confidence-gated fallback to handoff/form.
- Reservation-readiness scoring and triage cues.
- Multi-channel alert escalation after email baseline is stable.

**Defer (v2+):**
- Full custom CRM.
- Complex automation builder.
- Autonomous external booking writes without confirmation.
- Broad omnichannel expansion before core web chat reliability.

### Architecture Approach

Adopt a modular monolith with async workflow lanes. Keep one canonical FastAPI app with bounded modules (tenant, conversation, knowledge, model gateway, reservation, notification, analytics), one React admin client, and one widget contract boundary. Use transaction + outbox for reservation-to-notification reliability, version public widget contracts, and delay service extraction until scaling pressure is proven.

### Critical Pitfalls

1. **Tenant data leakage**: enforce authn/authz + ownership checks in router and service layers; add cross-tenant regression tests.
2. **Reservation captured but owner not notified**: make notification reliability an SLO with retries, dead-letter handling, and dashboard status.
3. **Open endpoint abuse and cost spikes**: add per-tenant/IP rate limits, quotas, and budget guardrails.
4. **Silent model fallback quality drift**: add explicit fallback reason telemetry and per-tenant quality monitoring.
5. **Brownfield dual-backend drift**: declare canonical backend path and block deprecated imports in CI.

## Implications for Roadmap

Based on combined research, use this v1-first phase structure.

### Phase 1: Foundation Hardening
**Rationale:** Every next step depends on secure tenant boundaries and a single canonical backend path.
**Delivers:** Canonical API surface, tenant authz enforcement, CORS/widget origin hardening, deprecated-path CI guards.
**Addresses:** Security table stakes and brownfield drift risk.
**Avoids:** Cross-tenant leakage, split behavior regressions.

### Phase 2: Reservation Reliability Core (v1 Priority)
**Rationale:** Direct business ROI comes from capturing intent and reliably notifying owners.
**Delivers:** Structured reservation schema, transaction + outbox, worker retries/dead-letter, deterministic email notifications, delivery status visibility.
**Addresses:** Core lead/reservation and owner notification table stakes.
**Avoids:** Missed-booking trust failures.

### Phase 3: Chat Quality and Knowledge Runtime
**Rationale:** After reliability baseline, improve answer quality and conversion outcomes.
**Delivers:** Async ingestion pipeline, pgvector hybrid retrieval, provider gateway with fallback policy, confidence-gated handoff.
**Uses:** Postgres + pgvector, model gateway abstraction.
**Avoids:** Hallucination risk and hidden degraded responses.

### Phase 4: Onboarding and Analytics Optimization
**Rationale:** Once trust path is stable, maximize activation and feedback loops.
**Delivers:** Lower-friction onboarding, embed polish, KPI dashboard (lead/reservation funnel, response metrics), query/perf optimization.
**Addresses:** Adoption and measurable ROI.
**Avoids:** Drop-off from setup friction and slow dashboard experience.

### Phase Ordering Rationale

- Security and canonicalization first prevent compounding architecture debt.
- Reservation reliability before expansion maximizes immediate SMB value.
- Quality/runtime improvements depend on durable async and observability foundations.
- UX and analytics polish are highest leverage after trust/reliability baseline is proven.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 3:** Provider gateway policy design (routing/fallback/cost controls) and retrieval tuning by tenant data shape.
- **Phase 4:** Attribution model design for source-aware conversion analytics.

Phases with standard patterns (can usually skip deep research):
- **Phase 1:** Tenant authz, CORS hardening, modular FastAPI boundaries.
- **Phase 2:** Outbox + worker retry/dead-letter patterns for notification reliability.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Strong alignment with current brownfield architecture and official ecosystem direction. |
| Features | MEDIUM | Table stakes are clear; differentiator impact depends on execution quality and vertical fit. |
| Architecture | HIGH | Modular monolith + async lanes are well-supported and low-risk for current stage. |
| Pitfalls | MEDIUM-HIGH | Risks are validated by current codebase concerns; some mitigations need infra-specific tuning. |

**Overall confidence:** MEDIUM-HIGH

### Gaps to Address

- Exact worker stack choice (RQ vs Dramatiq vs Celery) should be finalized from ops constraints and team familiarity.
- Provider fallback quality thresholds need phase-level validation dataset for critical intents.
- Data retention/masking policy depth should be confirmed against target compliance requirements.

## Sources

### Primary (HIGH confidence)
- Official framework/docs references aggregated in stack and architecture research (FastAPI, Postgres, SQLAlchemy, OpenTelemetry, pgvector, MDN security guidance).
- Internal codebase analysis documents under .planning/codebase (architecture, concerns, integrations, stack).

### Secondary (MEDIUM confidence)
- Vendor/platform docs informing AI gateway, tracing, and orchestration options (LiteLLM, LangGraph/LangSmith, queue frameworks).

### Tertiary (LOW-MEDIUM confidence)
- Competitor feature positioning and marketing pages used for directional feature expectations.

---
*Research completed: 2026-03-21*
*Ready for roadmap: yes*
