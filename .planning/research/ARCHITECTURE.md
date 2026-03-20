# Architecture Patterns

**Domain:** AI assistant platform for local businesses (brownfield FastAPI + React + widget)
**Researched:** 2026-03-21

## Recommended Architecture

Use a **modular monolith with asynchronous workflow lanes** as the next evolution step.

Why this is the right fit now:
- You already have one deployable FastAPI backend and one React admin app; keeping one backend deployable minimizes migration risk.
- The current reliability gap is in reservation notification and operational consistency, which is best solved by introducing durable async processing (job queue + outbox-like event recording), not by immediate microservice decomposition.
- The codebase has duplicate backend stacks today; splitting into services now would amplify drift. First consolidate boundaries in-process, then split only if scale requires it.

Target shape:
- One canonical FastAPI app with clear bounded modules.
- One React admin frontend that talks only to versioned backend contracts.
- One embeddable widget runtime that talks only to a public widget API surface.
- One relational database (Postgres preferred) with tenant scoping, migration discipline, and an outbox/events table for reliable side effects.
- One async worker lane for non-blocking work (emails, heavy parsing, retries).

## Component Boundaries

| Component | Responsibility | Communicates With |
|-----------|---------------|-------------------|
| API Gateway Layer (FastAPI routers) | Versioned HTTP contracts, authn/authz, request validation, rate limits, idempotency keys | Application modules, auth module, observability |
| Tenant & Identity Module | Tenant lifecycle, ownership checks, API keys/session/JWT mapping to tenant scope | API Gateway, DB |
| Conversation Module | Chat request orchestration, conversation persistence, context assembly coordination | Knowledge module, Model gateway, DB |
| Knowledge Module | Ingestion pipeline orchestration, document metadata, chunk lifecycle, retrieval API | Conversation module, Async worker, DB |
| Model Gateway Module | Provider abstraction, fallback policy, timeout/circuit rules, cost/latency telemetry | Conversation module, external LLM provider |
| Reservation Module | Reservation capture, status lifecycle, notification intent creation | Conversation module, Notification module, DB |
| Notification Module (async-first) | Reliable owner notifications (email), retry policy, dead-letter handling | Worker lane, provider adapter, DB/outbox |
| Analytics/Reporting Module | Tenant-scoped metrics, dashboard query models, PII-safe views | DB, API Gateway |
| Widget Delivery + Runtime Contract | Script bootstrap, host-site integration contract, theme/config model | Public widget API, postMessage channel |
| Async Worker Lane | Executes queued jobs (email send, heavy parse, reprocessing) | DB queue/outbox, provider adapters |
| Shared Platform Layer | Logging, tracing, metrics, config, feature flags, migration tooling | All modules |

Boundary rules:
- API routers never call provider SDKs directly.
- Modules communicate via interfaces/events, not cross-imported internals.
- Widget-facing endpoints are isolated from admin endpoints (separate auth and CORS policy).
- Reservation creation and notification dispatch are separate responsibilities connected by durable state transition.

## Data Flow

### 1) Onboarding to Live Assistant
1. Admin UI calls tenant onboarding endpoint.
2. Tenant module creates tenant + default assistant configuration in one transaction.
3. API returns widget bootstrap config and embed snippet metadata.
4. Widget script uses bootstrap endpoint to fetch runtime config (theme, endpoint, tenant-safe public key).

### 2) Knowledge Ingestion
1. Admin uploads file/text.
2. API validates request and writes ingestion job record.
3. Worker parses/chunks document and writes normalized knowledge rows.
4. Knowledge module marks ingestion state and emits completion event for analytics.

### 3) Chat Runtime
1. Widget/admin sends chat message with tenant context.
2. Conversation module validates tenant auth scope and rate limits.
3. Knowledge retrieval provides relevant chunks.
4. Model gateway calls primary provider, then fallback policy if needed.
5. Conversation + usage metadata are persisted.
6. Response is returned to client.
7. If intent indicates reservation, reservation module creates reservation intent atomically and emits notification task.

### 4) Reservation Notification Reliability Path
1. Reservation row and notification_outbox row are written in the same DB transaction.
2. Worker consumes pending outbox rows, attempts email send, records provider response.
3. Retries follow bounded backoff; terminal failures move to dead-letter state.
4. Dashboard surfaces notification status so business owners can trust capture outcomes.

## Build-Order Implications

Build in this order to reduce regression risk and maximize early business value:

1. **Canonical backend consolidation first**
- Remove legacy route/model track from active imports.
- Freeze one API contract surface.
- Rationale: every next step depends on stable module boundaries.

2. **Tenant authz + CORS hardening second**
- Enforce tenant ownership checks.
- Separate admin vs widget origin policies.
- Rationale: prevents architecture debt from being encoded into new endpoints.

3. **Reservation reliability lane third**
- Add notification outbox table + worker processing + retry/dead-letter semantics.
- Rationale: core active requirement is dependable owner email flow.

4. **Knowledge async ingestion fourth**
- Move heavy parse/chunk work out of request path.
- Rationale: protects chat latency and lowers timeout risk as tenants grow.

5. **Analytics query-model optimization fifth**
- Replace N+1 metrics loops with grouped aggregates/materialized strategy where needed.
- Rationale: dashboard confidence without degrading primary chat path.

6. **Widget contract stabilization sixth**
- Versioned widget API, strict postMessage origin checks, backward-compatible bootstrap schema.
- Rationale: protects existing embeds while enabling future widget features.

7. **Only then consider service extraction**
- Extract notification or ingestion module if independent scaling pressure is proven.
- Rationale: avoid premature distributed-system complexity.

## Brownfield Migration / Evolution Guidance

Use a **strangler-style incremental modernization** inside the existing repo and deployment model.

### Migration Principles
- Preserve external contracts first; refactor internals behind stable API routes.
- Introduce seams before rewrites (module interfaces, adapter layers, event records).
- Prefer additive migrations (new table/column + dual-read/write window) over destructive changes.
- Keep rollback paths for every step (feature flags, reversible DB migrations, compatibility endpoints).

### Practical Evolution Steps
1. **Define canonical architecture map in code**
- Mark deprecated modules (legacy routes/models) and block new imports in CI.

2. **Introduce an internal event/outbox table**
- Start with reservation notification events only.
- Add idempotency key and processing status fields.

3. **Add worker process without forcing full queue migration**
- For small jobs, FastAPI BackgroundTasks can bridge initially.
- For durable/retry-heavy tasks, move to Celery/RQ style worker with Redis/RabbitMQ.

4. **Create widget boundary package**
- Centralize widget bootstrap payload, host handshake, and message schema validation.
- Enforce explicit targetOrigin and origin checks for postMessage.

5. **Adopt contract tests before major refactors**
- Snapshot key API responses used by admin and widget.
- Fail CI if contract drift is unintended.

6. **De-risk data model changes**
- Add migrations and stop runtime auto-DDL in production paths.
- Use expand/contract database migration pattern for zero-downtime transitions.

### Exit Criteria for Future Service Split
Only split a module into its own service when at least two are true:
- Independent scaling profile is measurable (for example, ingestion CPU saturation independent of chat).
- Deployment cadence conflicts with other modules.
- Team ownership is clearly separate.
- Operational SLOs cannot be met in modular monolith form.

## Patterns to Follow

### Pattern 1: API Router -> Module Service -> Repository
**What:** Keep HTTP concerns in routers, business logic in modules, data access behind repositories.
**When:** All tenant-facing features.
**Why:** Enables safe refactoring and eventual extraction without contract churn.

### Pattern 2: Transaction + Outbox for Side Effects
**What:** Persist business state and side-effect intent atomically; execute side effects asynchronously.
**When:** Reservation emails, webhook-like notifications, billing events.
**Why:** Prevents "reservation saved but email not sent" inconsistencies.

### Pattern 3: Versioned Public Contracts
**What:** Version widget/admin API contracts and maintain backward compatibility windows.
**When:** Any endpoint consumed by external embeds or released frontend bundles.
**Why:** Brownfield deployments always have mixed client versions in the wild.

## Anti-Patterns to Avoid

### Anti-Pattern 1: Big-bang rewrite to microservices
**Why bad:** High delivery risk, long freeze on business features, duplicated bugs.
**Instead:** Modular monolith + strangler extraction over time.

### Anti-Pattern 2: Synchronous notification on request path
**Why bad:** User-facing latency and failure coupling to email provider availability.
**Instead:** Async worker lane with retries and status tracking.

### Anti-Pattern 3: Shared wildcard cross-origin trust for widget/admin
**Why bad:** Tenant data exposure risk and weak browser security boundaries.
**Instead:** Explicit origin allowlists per channel + strict postMessage verification.

## Scalability Considerations

| Concern | At 100 users | At 10K users | At 1M users |
|---------|--------------|--------------|-------------|
| Chat throughput | Single API instance + DB pooling | Horizontal API replicas + cache hot paths | Multi-region routing, provider failover strategy |
| Knowledge retrieval | SQL + bounded chunk scan | Add indexed retrieval (FTS/vector) | Dedicated retrieval infrastructure + async indexing |
| Notification delivery | In-process background tasks | Dedicated worker + broker + retries | Partitioned queues, throughput controls, dead-letter automation |
| Analytics | Direct aggregate queries | Pre-aggregations/materialized views | Streaming/event-driven analytics pipeline |
| Tenant isolation | App-level tenant checks | Add row-level safeguards and stricter auth scopes | Strong policy enforcement, compliance controls, audit trails |

## Confidence Notes

- **HIGH confidence:** FastAPI modularization (APIRouter, lifespan), CORS and postMessage security boundaries, Celery worker model, and strangler-style modernization are well-supported by authoritative docs.
- **MEDIUM confidence:** Specific outbox implementation details for your exact deployment topology (polling vs CDC) need phase-level validation against infra constraints.
- **LOW confidence:** None for core recommendations; unresolved area is exact broker/runtime choice because current ops constraints are not yet fully documented.

## Sources

- FastAPI docs: Bigger applications (APIRouter + modular structure) - https://fastapi.tiangolo.com/tutorial/bigger-applications/ (HIGH)
- FastAPI docs: Lifespan events and startup/shutdown guidance - https://fastapi.tiangolo.com/advanced/events/ (HIGH)
- FastAPI docs: BackgroundTasks caveat and when to use task queues - https://fastapi.tiangolo.com/tutorial/background-tasks/ (HIGH)
- React docs: Scaling with reducer + context patterns - https://react.dev/learn/scaling-up-with-reducer-and-context (HIGH)
- MDN: postMessage security guidance (targetOrigin/origin validation) - https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage (HIGH; last modified 2025-11-30)
- MDN: CORS headers and credentialed-request constraints - https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS (HIGH; last modified 2025-11-30)
- Celery docs: broker/worker architecture basics - https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html (HIGH)
- Martin Fowler: Strangler Fig modernization framing - https://martinfowler.com/bliki/StranglerFigApplication.html (MEDIUM-HIGH; dated 2024-08-22)
- Debezium docs: Outbox event router and outbox table semantics - https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html (MEDIUM-HIGH)
- Internal codebase architecture and concern audits - .planning/codebase/ARCHITECTURE.md, .planning/codebase/CONCERNS.md, .planning/codebase/INTEGRATIONS.md (HIGH for current-state fit)
