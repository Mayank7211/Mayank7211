# External Integrations

**Analysis Date:** 2026-03-21

## APIs & External Services

**LLM Provider:**
- Groq API - text generation for assistant responses
  - SDK/Client: `groq` via `AsyncGroq` in `apps/backend/app/services/model_gateway.py`
  - Auth: `AI_AGENT_GROQ_API_KEY` (`apps/backend/.env.example`, `apps/backend/app/core/config.py`)

**Browser/HTTP Integrations:**
- Frontend -> Backend REST API via `fetch` (`apps/frontend/src/lib/api.ts`, `apps/frontend/src/components/AdminDashboard.tsx`)
- Widget -> Backend REST API via `fetch` (`apps/widget/agent.js`, `widget/agent.js`)

## Data Storage

**Databases:**
- PostgreSQL (primary in documented containerized flow; inferred) (`apps/backend/.env.example`, `infra/sql/001_init.sql`)
  - Connection: `AI_AGENT_DATABASE_URL`
  - Client: SQLAlchemy async engine/session (`apps/backend/app/db/session.py`)
- SQLite async (local fallback/default) (`apps/backend/app/core/config.py`)

**File Storage:**
- Local/in-memory processing of uploaded files through FastAPI upload endpoint (`apps/backend/app/api/tenants.py`, `apps/backend/app/services/document_parser.py`)
- Persistent object storage integration not detected

**Caching:**
- None detected (no Redis/Memcached integration found)

## Authentication & Identity

**Auth Provider:**
- External auth provider not detected
  - Implementation: custom tenant-scoped IDs in request payloads (`apps/backend/app/models/schemas.py`, `apps/frontend/src/lib/api.ts`)

## Monitoring & Observability

**Error Tracking:**
- Third-party error tracking (Sentry/Datadog/etc.) not detected

**Logs:**
- Console/error logging only (`console.error` in frontend/widget, default backend exception behavior)

## CI/CD & Deployment

**Hosting:**
- Docker Compose workflow documented (`README.md`; `docker-compose.yml` present)
- Cloud/host provider config not detected

**CI Pipeline:**
- GitHub Actions or other CI config not detected (`.github/workflows/` absent)

## Environment Configuration

**Required env vars:**
- Backend:
  - `AI_AGENT_ENVIRONMENT`
  - `AI_AGENT_DEFAULT_SMALL_MODEL`
  - `AI_AGENT_DEFAULT_LARGE_MODEL`
  - `AI_AGENT_REQUEST_TIMEOUT_SECONDS`
  - `AI_AGENT_MAX_CONTEXT_CHUNKS`
  - `AI_AGENT_DATABASE_URL`
  - `AI_AGENT_AUTO_CREATE_TABLES`
  - `AI_AGENT_GROQ_API_KEY`
- Frontend:
  - `VITE_API_BASE_URL`

**Secrets location:**
- `.env` files expected by app config (`apps/backend/app/core/config.py`)
- `.env.example` templates provided (`apps/backend/.env.example`, `apps/frontend/.env.example`)

## Integration Points (Frontend / Backend / Widget / DB)

**Frontend -> Backend:**
- Tenant provisioning: `POST /api/tenants` (`apps/frontend/src/lib/api.ts` -> `apps/backend/app/api/tenants.py`)
- Knowledge ingestion: `POST /api/tenants/{tenant_id}/knowledge` (`apps/frontend/src/lib/api.ts` -> `apps/backend/app/api/tenants.py`)
- File upload: `POST /api/tenants/{tenant_id}/upload` (`apps/frontend/src/lib/api.ts` -> `apps/backend/app/api/tenants.py`)
- Chat: `POST /api/chat` (`apps/frontend/src/lib/api.ts` -> `apps/backend/app/api/chat.py`)
- Analytics: `GET /api/analytics/tenants/{tenant_id}/*` (`apps/frontend/src/components/AdminDashboard.tsx` -> `apps/backend/app/api/analytics.py`)

**Widget -> Backend:**
- `apps/widget/agent.js` posts to `${backendUrl}/api/chat/${agentId}` (path appears legacy/inferred mismatch with current `/api/chat` endpoint)
- `widget/agent.js` posts to `${API_BASE_URL}/chat` with `tenant_id` model (aligned with current backend contract)

**Backend -> DB:**
- Async SQLAlchemy session used across API services (`apps/backend/app/db/session.py`)
- Core entities persisted for tenants, knowledge, conversations, leads/reservations (`apps/backend/app/models/entities.py`, `infra/sql/001_init.sql`)

**Backend -> LLM provider:**
- `AssistantService` builds model request and calls `ModelGateway.complete()` (`apps/backend/app/services/assistant_service.py`)
- `ModelGateway` calls Groq primary and local fallback provider (`apps/backend/app/services/model_gateway.py`)

## Webhooks & Callbacks

**Incoming:**
- None detected

**Outgoing:**
- None detected (no webhook dispatch/client code found)

---

*Integration audit: 2026-03-21*
