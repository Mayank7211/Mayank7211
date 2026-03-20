# Codebase Concerns

**Analysis Date:** 2026-03-21

## Tech Debt

**[HIGH] Dual backend implementations with overlapping domains:**
- Issue: Two backend architectures coexist (`app/api` + async SQLAlchemy v2, and `app/routes` + sync SQLAlchemy legacy models), increasing drift and accidental reuse risk.
- Files: `apps/backend/app/main.py`, `apps/backend/app/api/chat.py`, `apps/backend/app/routes/chat.py`, `apps/backend/app/models/entities.py`, `apps/backend/app/models/tenant.py`, `apps/backend/app/core/database.py`, `apps/backend/app/db/session.py`
- Impact: Inconsistent behavior, broken assumptions in tests/clients, and higher bug rate during refactors.
- Fix approach: Pick one backend stack as canonical; deprecate/remove the other; add CI checks that fail on imports from deprecated modules.

**[MEDIUM] Monolithic frontend/widget modules:**
- Issue: UI + networking + state logic are concentrated in large files.
- Files: `widget/agent.js`, `apps/frontend/src/components/AdminDashboard.tsx`, `apps/frontend/src/components/OnboardingForm.tsx`
- Impact: Higher regression risk and slower reviews because unrelated concerns change together.
- Fix approach: Split by concern (API adapter, view components, state hooks, rendering helpers).

## Known Bugs

**[HIGH] Legacy API test script targets endpoints/schemas that do not match active API:**
- Symptoms: Script calls endpoints and payload fields that are absent in active router design.
- Files: `apps/backend/test_api.py`, `apps/backend/app/main.py`, `apps/backend/app/api/tenants.py`, `apps/backend/app/api/chat.py`
- Trigger: Running `apps/backend/test_api.py` against current app.
- Workaround: Use routes in `app/api/*` and payloads from `app/models/schemas.py`; avoid relying on `test_api.py` as validation.

## Security Considerations

**[HIGH] No tenant authentication/authorization on tenant-scoped endpoints:**
- Risk: Any caller with a tenant ID can read analytics/conversations/reservations or write chat/knowledge data.
- Files: `apps/backend/app/api/analytics.py`, `apps/backend/app/api/chat.py`, `apps/backend/app/api/tenants.py`
- Current mitigation: Tenant existence checks only.
- Recommendations: Add authn/authz middleware (JWT/session/API key), enforce tenant ownership checks, and rate-limit per tenant and IP.

**[HIGH] CORS allows all origins with credentials:**
- Risk: Broad cross-origin access increases abuse and data exfiltration surface, especially if credentials are later introduced.
- Files: `apps/backend/app/main.py`
- Current mitigation: None detected.
- Recommendations: Restrict `allow_origins` to trusted domains and disable credentials unless required.

**[MEDIUM] Sensitive PII exposed via analytics responses:**
- Risk: Reservation and conversation endpoints return customer contact details and full message content.
- Files: `apps/backend/app/services/analytics.py`, `apps/backend/app/api/analytics.py`
- Current mitigation: None detected beyond tenant existence check.
- Recommendations: Add role-based scopes, redact/mask fields by default, add audit logging for reads.

## Performance Bottlenecks

**[MEDIUM] N+1 style daily metrics querying:**
- Problem: One SQL query per day in window (`days` up to 90).
- Files: `apps/backend/app/services/analytics.py`
- Cause: Loop over days with per-day count query.
- Improvement path: Replace loop with grouped aggregation query over date buckets.

**[MEDIUM] Per-request context retrieval scans up to 400 knowledge rows:**
- Problem: Chat context loader fetches recent rows then performs token-overlap ranking in Python.
- Files: `apps/backend/app/services/assistant_service.py`, `apps/backend/app/services/knowledge.py`
- Cause: No precomputed index/search backend.
- Improvement path: Add indexed retrieval (FTS/vector), tune limits by tenant size, cache repeated queries.

## Fragile Areas

**[HIGH] Model provider fallback silently degrades output quality:**
- Files: `apps/backend/app/services/model_gateway.py`
- Why fragile: Primary provider exceptions are broadly caught and fallback returns low-confidence generic responses without structured telemetry.
- Safe modification: Introduce typed exception handling, error classification, and explicit fallback reason fields.
- Test coverage: Gap; no tests detected for provider failure behavior.

**[MEDIUM] Frontend upload progress state may race during sequential uploads (inferred):**
- Files: `apps/frontend/src/components/OnboardingForm.tsx`
- Why fragile: State updates use object spreads from captured state in async loop.
- Safe modification: Use functional state updates (`setState(prev => ...)`) in upload loop.
- Test coverage: Gap; no frontend tests detected.

## Scaling Limits

**[MEDIUM] SQLite default and auto table creation suggest single-node/developer posture (inferred):**
- Current capacity: Suitable for local/small workloads.
- Limit: Contention and operational limits under concurrent multi-tenant traffic.
- Scaling path: Move to managed Postgres, disable runtime auto DDL, add migrations and pooling tuning.

## Dependencies at Risk

**[LOW] No immediate vulnerable dependency evidence from inspected manifests:**
- Risk: Not detected from static review alone.
- Impact: Unknown without vulnerability scan.
- Migration plan: Add dependency scanning in CI (pip-audit/Safety, npm audit).

## Missing Critical Features

**[HIGH] No rate limiting/abuse guardrails on chat and upload endpoints:**
- Problem: Endpoints are open to request floods and cost-amplification patterns.
- Blocks: Safe internet exposure and predictable spend.
- Files: `apps/backend/app/api/chat.py`, `apps/backend/app/api/tenants.py`, `apps/backend/app/main.py`

**[MEDIUM] No schema migration workflow detected:**
- Problem: Runtime table creation is enabled by default.
- Blocks: Safe production schema evolution.
- Files: `apps/backend/app/core/config.py`, `apps/backend/app/db/session.py`

## Test Coverage Gaps

**[HIGH] Minimal automated coverage on core business paths:**
- What's not tested: Tenant onboarding, knowledge ingestion/upload, chat flow, analytics endpoints, model fallback, auth boundaries.
- Files: `apps/backend/tests/test_health.py`, `apps/backend/app/services/assistant_service.py`, `apps/backend/app/api/tenants.py`, `apps/backend/app/api/chat.py`, `apps/backend/app/api/analytics.py`
- Risk: Regressions and security gaps can ship unnoticed.
- Priority: High

**[MEDIUM] Widget/frontend behavior largely untested:**
- What's not tested: Session handling, embed configuration, API error handling, rendering edge cases.
- Files: `widget/agent.js`, `apps/widget/agent.js`, `apps/frontend/src/components/AdminDashboard.tsx`, `apps/frontend/src/components/OnboardingForm.tsx`
- Risk: Production UX failures and silent client-side breakage.
- Priority: Medium

---

*Concerns audit: 2026-03-21*
