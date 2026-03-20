# Domain Pitfalls

**Domain:** Multi-tenant AI assistant platform for local businesses (brownfield)
**Researched:** 2026-03-21
**Scope:** Subsequent milestone risk prevention for reservation-driven business outcomes
**Overall confidence:** MEDIUM-HIGH (grounded in current codebase concerns and architecture docs)

## Critical Pitfalls

Mistakes that commonly force expensive rewrites, create trust failures for local businesses, or break core ROI (capturing and acting on reservation intent).

### Pitfall 1: Tenant Data Leakage via Weak Isolation
**What goes wrong:** Analytics, conversations, or reservation records become accessible across tenants due to ID-based access patterns without ownership enforcement.
**Why it happens:** Brownfield APIs rely on tenant existence checks but do not enforce authenticated tenant ownership on every read/write path.
**Consequences:** Privacy incidents, legal exposure, immediate loss of business trust, and potential shutdown risk.
**Warning signs:**
- APIs accept only tenant_id with no authenticated principal check.
- Support reports mention "seeing another business's data".
- Sudden spikes in cross-tenant 404/200 patterns from unknown origins.
**Prevention strategy:**
- Add mandatory authn/authz middleware for all tenant-scoped endpoints.
- Enforce ownership checks in service layer and router layer (defense in depth).
- Add audit logs for sensitive read operations and anomaly alerts.
- Add security regression tests for cross-tenant access attempts.
**Suggested phase to address:** Next foundational hardening phase before scaling usage (early milestone phase).

### Pitfall 2: Reservation Capture Without Reliable Owner Notification
**What goes wrong:** Customers submit booking/reservation intent, but owners are not notified reliably or quickly.
**Why it happens:** Notification flow is treated as secondary integration work rather than core product path.
**Consequences:** Businesses perceive "AI chat looks nice but gives no outcomes", causing churn and failed adoption.
**Warning signs:**
- Reservation rows exist but corresponding email delivery records are missing.
- Business owners report missed bookings.
- No measurable reservation-to-notification success metric in dashboard.
**Prevention strategy:**
- Treat reservation notification as a primary success path with explicit SLO.
- Implement durable delivery workflow with retries, dead-letter visibility, and alerting.
- Add end-to-end tests from widget submission to owner inbox confirmation state.
- Expose delivery status in admin dashboard to reduce support guesswork.
**Suggested phase to address:** Immediate business-value phase (first phase in current milestone).

### Pitfall 3: Open Endpoints Leading to Abuse and Cost Runaway
**What goes wrong:** Unauthenticated chat/upload endpoints get spammed, causing model/API cost spikes and degraded service.
**Why it happens:** MVP convenience defaults remain in production exposure without rate limits and abuse controls.
**Consequences:** Budget burn, latency spikes, outages, and emergency throttling that harms real users.
**Warning signs:**
- Burst traffic from few IP ranges.
- Rising token usage without matching increase in valid reservations.
- Increased 5xx and timeout rates during traffic spikes.
**Prevention strategy:**
- Introduce per-tenant and per-IP rate limiting and request quotas.
- Add bot/abuse detection heuristics and payload size controls.
- Require tenant-scoped credentials for ingestion and management APIs.
- Add cost guardrails (daily budget caps, automatic fallback/degradation policies).
**Suggested phase to address:** Platform hardening phase directly after reservation reliability work.

### Pitfall 4: Silent Model Fallback Degrading Response Quality
**What goes wrong:** Primary provider failures silently downgrade output quality, and businesses lose confidence in assistant accuracy.
**Why it happens:** Broad exception handling and weak fallback telemetry hide when degraded paths are serving users.
**Consequences:** Quality drift, hard-to-debug complaints, and lower conversion from chat to reservation.
**Warning signs:**
- Sudden increase in generic or vague assistant replies.
- No clear traceability of provider failures in logs/metrics.
- Support tickets say "assistant became less useful" without obvious outages.
**Prevention strategy:**
- Implement typed provider error taxonomy and explicit fallback reason fields.
- Emit metrics for fallback rate, model latency, and confidence by tenant.
- Add quality smoke tests for critical intents (hours, pricing, booking).
- Surface degraded mode status internally for faster incident response.
**Suggested phase to address:** Reliability and observability phase (early-mid milestone).

### Pitfall 5: Brownfield Dual-Backend Drift and Split Behavior
**What goes wrong:** Teams unknowingly modify legacy and active backend paths differently, creating inconsistent API behavior.
**Why it happens:** Coexisting route/model stacks increase ambiguity over source of truth.
**Consequences:** Regressions, inconsistent tenant behavior, wasted engineering effort, and delayed releases.
**Warning signs:**
- Similar endpoints implemented in two backend locations.
- Tests/scripts target mismatched schemas or routes.
- Frequent "works in one path, fails in another" incidents.
**Prevention strategy:**
- Declare canonical backend path and mark legacy modules deprecated.
- Add CI checks preventing new imports from deprecated stack.
- Consolidate tests and scripts to canonical API contracts only.
- Publish migration map for affected modules/endpoints.
**Suggested phase to address:** Brownfield consolidation phase before major feature expansion.

## Moderate Pitfalls

### Pitfall 1: Onboarding Friction for Non-Technical Owners
**What goes wrong:** Setup requires too many technical choices, causing drop-off before activation.
**Warning signs:**
- High abandonment during embed/setup steps.
- Frequent support questions about basic configuration.
**Prevention strategy:**
- Reduce steps, provide sensible defaults, and add guided validation.
- Track funnel analytics from signup to first successful chat.
**Suggested phase to address:** UX optimization phase after reliability blockers are closed.

### Pitfall 2: PII Overexposure in Analytics Workflows
**What goes wrong:** Admin views expose more conversation/contact detail than necessary.
**Warning signs:**
- Full raw transcripts shown in broad dashboard contexts.
- No role-based masking for sensitive fields.
**Prevention strategy:**
- Default to masked data with role-based reveal permissions.
- Add read-audit logging and retention controls.
**Suggested phase to address:** Security/privacy refinement phase (parallel with auth rollout).

### Pitfall 3: Analytics Query Patterns That Do Not Scale
**What goes wrong:** Dashboard performance degrades as tenant and message volume grows.
**Warning signs:**
- Increasing dashboard load times with longer date windows.
- DB CPU spikes during analytics-heavy periods.
**Prevention strategy:**
- Replace per-day loops with grouped SQL aggregation.
- Add query indexes and pre-aggregation where justified.
**Suggested phase to address:** Performance phase before broader tenant onboarding push.

## Minor Pitfalls

### Pitfall 1: Monolithic UI/Widget Files Slowing Iteration
**What goes wrong:** Simple changes cause broad regressions because state, rendering, and network code are tightly coupled.
**Warning signs:**
- Large unrelated diffs for small UX changes.
- Repeated regressions in upload or chat UI behavior.
**Prevention strategy:**
- Split modules by concern and add focused component tests.
**Suggested phase to address:** Developer experience and maintainability phase.

### Pitfall 2: Missing Migration Discipline
**What goes wrong:** Auto table creation and ad hoc schema changes create environment drift.
**Warning signs:**
- Different schema behavior between local/staging/prod.
- Emergency fixes tied to manual DB edits.
**Prevention strategy:**
- Enforce migration-based schema evolution and disable runtime auto DDL in production.
**Suggested phase to address:** Infrastructure readiness phase.

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Warning Signs | Mitigation |
|-------------|---------------|---------------|------------|
| Reservation outcomes | Notification reliability gap | Stored reservations with no owner delivery evidence | Build durable notification pipeline, retries, and delivery status tracking |
| Tenant security hardening | Cross-tenant data access | Tenant ID only checks, no ownership enforcement | Add authn/authz, ownership guards, and access tests |
| Abuse/cost control | Endpoint flooding and token burn | Cost spikes without business outcome lift | Rate limiting, quotas, and budget guardrails |
| Brownfield consolidation | Dual backend divergence | Conflicting routes/schemas and duplicate logic | Canonicalize stack and block deprecated imports in CI |
| Observability | Hidden degraded model behavior | Generic responses with no failure attribution | Fallback metrics, tracing, and quality monitors |

## Suggested Sequencing for This Milestone

1. Reservation reliability first (direct business ROI).
2. Security and abuse controls second (safe scale and trust).
3. Brownfield consolidation third (reduce regression surface).
4. Observability and quality controls fourth (stabilize assistant behavior).
5. UX and performance polish after core trust/reliability is stable.

## Sources

- Internal project brief: `.planning/PROJECT.md`
- Internal code risk audit: `.planning/codebase/CONCERNS.md`
- Internal architecture map: `.planning/codebase/ARCHITECTURE.md`
- Internal stack map: `.planning/codebase/STACK.md`
