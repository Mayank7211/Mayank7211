# Architecture

**Analysis Date:** 2026-03-21

## Pattern Overview

**Overall:** Layered monolith with API-first backend and separate SPA frontend.

**Key Characteristics:**
- FastAPI app composes feature routers and service classes (`apps/backend/app/main.py`, `apps/backend/app/api/*.py`, `apps/backend/app/services/*.py`).
- Frontend is a single React app that calls backend HTTP endpoints directly (`apps/frontend/src/App.tsx`, `apps/frontend/src/lib/api.ts`).
- Persistence uses SQLAlchemy async ORM entities mapped to tenant-scoped tables (`apps/backend/app/models/entities.py`, `apps/backend/app/db/session.py`).

## Layers

**Frontend UI Layer:**
- Purpose: Collect tenant onboarding data, upload knowledge files, and run chat sandbox interactions.
- Location: `apps/frontend/src`
- Contains: React pages/components and API client helpers.
- Depends on: Browser `fetch`, Vite env vars, backend HTTP API.
- Used by: End users through Vite dev server or Nginx static build (`apps/frontend/Dockerfile`).

**API Layer:**
- Purpose: Expose HTTP endpoints for health, tenant lifecycle, chat, and analytics.
- Location: `apps/backend/app/api`
- Contains: FastAPI routers (`health.py`, `tenants.py`, `chat.py`, `analytics.py`).
- Depends on: Pydantic request/response models and DB session dependency.
- Used by: Frontend clients and tests (`apps/backend/tests/test_health.py`).

**Application Service Layer:**
- Purpose: Implement business workflows for tenant creation, knowledge ingestion, model orchestration, and reporting.
- Location: `apps/backend/app/services`
- Contains: `assistant_service.py`, `analytics.py`, `model_gateway.py`, `knowledge.py`, `document_parser.py`.
- Depends on: ORM entities, SQLAlchemy async session, provider SDKs (`groq`).
- Used by: API routers.

**Data Access Layer:**
- Purpose: Define schema and manage DB lifecycle.
- Location: `apps/backend/app/models`, `apps/backend/app/db`, `infra/sql`
- Contains: ORM entities, async engine/session, SQL bootstrap migration.
- Depends on: SQLAlchemy and configured database URL.
- Used by: Service layer and app startup lifespan hooks.

## Data Flow

**Tenant Onboarding + Knowledge Ingestion:**

1. `OnboardingForm` submits tenant payload to `POST /api/tenants` (`apps/frontend/src/components/OnboardingForm.tsx`, `apps/frontend/src/lib/api.ts`).
2. API router delegates to `assistant_service.create_tenant`, which writes `TenantEntity` and seed `KnowledgeSourceEntity` rows (`apps/backend/app/api/tenants.py`, `apps/backend/app/services/assistant_service.py`).
3. Optional manual text and file upload call `POST /api/tenants/{tenant_id}/knowledge` and `POST /api/tenants/{tenant_id}/upload`; parser chunks content before persistence (`apps/backend/app/services/document_parser.py`).

**Chat Runtime:**

1. Frontend sends `POST /api/chat` with `tenant_id` + message (`apps/frontend/src/components/ChatSandbox.tsx`, `apps/frontend/src/lib/api.ts`).
2. API validates payload via `ChatRequest` and forwards to `assistant_service.chat` (`apps/backend/app/api/chat.py`, `apps/backend/app/models/schemas.py`).
3. Service loads tenant + recent knowledge + conversation history, ranks context, builds `ModelRequest`, and calls `ModelGateway.complete` (`apps/backend/app/services/assistant_service.py`, `apps/backend/app/services/knowledge.py`).
4. Gateway routes to primary Groq provider and falls back to backup provider on failure (`apps/backend/app/services/model_gateway.py`).
5. Conversation is persisted and response metadata is returned to client (`apps/backend/app/models/entities.py`).

**State Management:**
- Frontend: component-local React state with prop drilling from `App` to child components.
- Backend: request-scoped async DB sessions and persisted SQL state; no separate cache/state store.

## Key Abstractions

**Tenant-Scoped Assistant Context:**
- Purpose: Bind every workflow to tenant identity and tenant-owned knowledge.
- Examples: `apps/backend/app/models/entities.py`, `apps/backend/app/services/assistant_service.py`.
- Pattern: Tenant ID is mandatory across creation, ingestion, chat, and analytics paths.

**Model Gateway + Provider Strategy:**
- Purpose: Separate model routing/fallback from endpoint handlers.
- Examples: `apps/backend/app/services/model_gateway.py`.
- Pattern: Protocol-based provider abstraction with primary+fallback execution.

**Analytics Aggregator Service:**
- Purpose: Compute operational metrics from conversations/knowledge/reservations.
- Examples: `apps/backend/app/services/analytics.py`, `apps/backend/app/api/analytics.py`.
- Pattern: Thin API router + service queries using SQL aggregates.

## Entry Points

**Backend API Entry Point:**
- Location: `apps/backend/app/main.py`
- Triggers: Uvicorn startup (`apps/backend/Dockerfile`) or local `uvicorn app.main:app`.
- Responsibilities: Initialize DB on lifespan start, configure CORS, and mount API routers.

**Frontend Entry Point:**
- Location: `apps/frontend/src/main.tsx`
- Triggers: Vite dev/build runtime.
- Responsibilities: Render root React app and global styles.

**Container Orchestration Entry Point:**
- Location: `docker-compose.yml`
- Triggers: `docker compose up --build`.
- Responsibilities: Start Postgres, backend API container, and frontend Nginx container.

## Error Handling

**Strategy:** API-first exception handling with explicit HTTP errors plus model-provider fallback.

**Patterns:**
- Validation and business conflicts use `HTTPException` with status codes 400/404/409/413/500 (`apps/backend/app/api/tenants.py`, `apps/backend/app/services/assistant_service.py`).
- LLM provider failures are intercepted in gateway and redirected to backup response generator (`apps/backend/app/services/model_gateway.py`).

## Cross-Cutting Concerns

**Logging:** Minimal explicit logging; mostly `console.error` in frontend and exception propagation in backend (inferred from `apps/frontend/src/components/*.tsx` and service code).
**Validation:** Pydantic schema validation for API payloads (`apps/backend/app/models/schemas.py`).
**Authentication:** Not detected in active API routers; endpoints are currently open (inferred from `apps/backend/app/main.py` and `apps/backend/app/api/*.py`).

**Inferred Legacy Track:**
- A second synchronous route/model stack exists under `apps/backend/app/routes` and `apps/backend/app/models/tenant.py` using `app/core/database.py`.
- This stack is inferred as legacy/unwired because `apps/backend/app/main.py` only mounts routers from `app/api`.

---

*Architecture analysis: 2026-03-21*
