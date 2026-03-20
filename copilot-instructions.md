<!-- GSD:project-start source:PROJECT.md -->
## Project

**AI Assistant Builder for Local Businesses**

A multi-tenant AI assistant platform for local businesses that provides website chat, business-specific responses, and admin visibility into conversations and reservations. Business owners onboard their assistant, embed a widget, upload knowledge, and monitor outcomes through a dashboard. Website visitors get fast answers and can submit reservation-style requests.

**Core Value:** A local business can go from setup to a working website assistant quickly, and reliably capture customer reservation intent.

### Constraints

- **Tech stack**: Keep compatibility with existing FastAPI + React + widget architecture — avoid disruptive rewrites.
- **Usability**: Setup flow must stay simple for small business operators — minimize operational overhead.
- **Reliability**: Reservation capture and owner notification must be dependable — this is core business value.
- **Security**: Tenant-scoped data paths need safer defaults — current concerns must be reduced as implementation proceeds.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->
## Technology Stack

## Languages
- Python 3.x (version not pinned; inferred) - backend API/services in `apps/backend/app/**/*.py`
- TypeScript 5.x - frontend app in `apps/frontend/src/**/*.ts` and `apps/frontend/src/**/*.tsx`
- JavaScript (ES6+) - embeddable widget scripts in `apps/widget/agent.js` and `widget/agent.js`
- SQL (PostgreSQL dialect) - schema/init scripts in `infra/sql/001_init.sql`
- Markdown - project and process docs (`README.md`, `SUMMARY.md`, `.planning/**`)
## Runtime
- Python runtime for FastAPI backend (inferred from `apps/backend/requirements.txt`)
- Node.js runtime for frontend tooling and dev server (inferred from `apps/frontend/package.json`)
- Browser runtime for React UI and standalone widget scripts (`apps/frontend/src/main.tsx`, `apps/widget/agent.js`)
- Frontend: npm (inferred from script usage in `README.md` and `apps/frontend/package.json`)
- Backend: pip with requirements file (`apps/backend/requirements.txt`)
- Lockfiles: missing for both ecosystems (`package-lock.json`, `poetry.lock`, `Pipfile.lock` not detected)
## Frameworks
- FastAPI 0.116.1 - backend HTTP API and routing (`apps/backend/requirements.txt`, `apps/backend/app/main.py`)
- React 18.3.1 + React DOM 18.3.1 - frontend UI (`apps/frontend/package.json`)
- SQLAlchemy 2.0.42 - ORM/data layer (`apps/backend/requirements.txt`, `apps/backend/app/db/session.py`)
- pytest 8.4.2 - backend tests (`apps/backend/requirements.txt`, `apps/backend/tests/test_health.py`)
- FastAPI TestClient - API test client (`apps/backend/tests/test_health.py`)
- Vite 5.4.10 - frontend dev/build (`apps/frontend/package.json`, `apps/frontend/vite.config.ts`)
- TypeScript compiler 5.6.3 - type checking/build step (`apps/frontend/package.json`, `apps/frontend/tsconfig.json`)
- Uvicorn 0.35.0 - ASGI server for backend (`apps/backend/requirements.txt`, `README.md`)
## Key Dependencies
- `groq==0.14.0` - primary LLM provider client (`apps/backend/app/services/model_gateway.py`)
- `pydantic==2.11.7` + `pydantic-settings==2.10.1` - schema and env config (`apps/backend/app/models/schemas.py`, `apps/backend/app/core/config.py`)
- `python-multipart==0.0.6` - file upload handling in tenant upload endpoint (`apps/backend/app/api/tenants.py`)
- `asyncpg==0.30.0` - async PostgreSQL driver (`apps/backend/requirements.txt`)
- `aiosqlite==0.21.0` - local SQLite async fallback/dev DB (`apps/backend/app/core/config.py`)
- `PyPDF2==4.0.1` and `python-docx==0.8.11` - document ingestion/parsing (`apps/backend/app/services/document_parser.py`)
- `@vitejs/plugin-react==4.3.4` - React transform/plugin (`apps/frontend/package.json`, `apps/frontend/vite.config.ts`)
## Configuration
- Backend settings loaded from `.env` with prefix `AI_AGENT_` (`apps/backend/app/core/config.py`)
- Example backend vars in `apps/backend/.env.example`:
- Frontend base API URL via `VITE_API_BASE_URL` (`apps/frontend/.env.example`, `apps/frontend/src/env.d.ts`)
- Frontend (`apps/frontend/package.json`):
- Backend (`README.md` + inferred):
## Platform Requirements
- Local backend on `http://localhost:8000` (documented in `README.md` and used by frontend/widget defaults)
- Local frontend on Vite default `http://localhost:5173` (`README.md`, `apps/frontend/vite.config.ts`)
- Database options:
- Deployment target not strictly codified; inferred split architecture:
- Widget CDN path in response is placeholder/inferred (`apps/backend/app/services/assistant_service.py` uses `https://cdn.your-app.com/widget.js`)
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

## Naming Patterns
- Frontend React components use `PascalCase.tsx` (for example `apps/frontend/src/components/OnboardingForm.tsx`).
- Frontend utilities/types use lowercase module names (for example `apps/frontend/src/lib/api.ts`).
- Backend modules use `snake_case.py` (for example `apps/backend/app/services/assistant_service.py`).
- Tests follow `test_*.py` naming (for example `apps/backend/tests/test_health.py`).
- Frontend functions and hooks use `camelCase` (`handleSubmit`, `uploadDocuments` in `apps/frontend/src/components/OnboardingForm.tsx`).
- Backend functions use `snake_case` (`create_tenant`, `get_db_session` in `apps/backend/app/api/tenants.py` and `apps/backend/app/db/session.py`).
- Frontend state and locals use `camelCase` (`isSubmitting`, `tenantId` in `apps/frontend/src/components/ChatSandbox.tsx`).
- Backend variables and fields use `snake_case` (`tenant_id`, `source_url` in `apps/backend/app/models/schemas.py`).
- TypeScript interfaces use `PascalCase` with suffixes like `Payload`/`Response` (`TenantCreatePayload`, `ChatResponse` in `apps/frontend/src/lib/api.ts`).
- Python Pydantic schemas use `PascalCase` class names with request/response suffixes (`TenantCreateRequest`, `TenantCreateResponse` in `apps/backend/app/models/schemas.py`).
- SQLAlchemy entities use `PascalCase` with `Entity` suffix (`TenantEntity` in `apps/backend/app/models/entities.py`).
## Code Style
- No repository-level formatter config detected (`.prettierrc`, `pyproject.toml`, `black` config not found).
- Style appears tool-default and editor-driven (inferred).
- No repository-level lint config detected (`eslint`, `ruff`, `flake8`, `biome` config files not found).
- TypeScript strictness is enforced in `apps/frontend/tsconfig.json` (`"strict": true`).
## Import Organization
- Not detected; relative imports are used in frontend and absolute `app.*` package imports are used in backend.
## API Conventions
- FastAPI routers define resource prefixes and tags (`APIRouter(prefix="/tenants", tags=["tenants"])` in `apps/backend/app/api/tenants.py`).
- Request/response models are explicitly typed with `response_model` on endpoints (`apps/backend/app/api/chat.py`).
- API payload fields use `snake_case` consistently (`tenant_id`, `text_blocks` in `apps/backend/app/models/schemas.py`).
- Frontend API client maps directly to backend routes (`createTenant`, `chatWithAssistant` in `apps/frontend/src/lib/api.ts`).
## Data Model Conventions
- Validation rules are defined at schema boundaries using Pydantic `Field` constraints (`apps/backend/app/models/schemas.py`).
- Persistence layer uses SQLAlchemy 2 typed mappings (`Mapped[...]`, `mapped_column` in `apps/backend/app/models/entities.py`).
- Entity names end with `Entity`; API schemas end with `Request`/`Response`; this split is consistent across backend models.
- UUID strings are primary IDs for tenant-facing entities (`apps/backend/app/models/entities.py`).
## Error Handling
- Backend raises `HTTPException` with explicit status codes for expected API errors (`apps/backend/app/api/tenants.py`, `apps/backend/app/services/assistant_service.py`).
- Frontend API client throws `Error` on non-OK responses and surfaces user-friendly fallback messages in components (`apps/frontend/src/lib/api.ts`, `apps/frontend/src/components/ChatSandbox.tsx`).
## Logging
- Frontend uses `console.error(...)` in async failure paths (`apps/frontend/src/components/OnboardingForm.tsx`).
- Backend generally returns structured HTTP errors instead of explicit logging in route/service code (inferred).
## Comments
- Comments are sparse and mostly used for non-obvious behavior (for example table-discovery note in `apps/backend/app/db/session.py`, validation notes in `apps/backend/app/api/tenants.py`).
- Not detected in sampled frontend/backend source.
## Function Design
- Endpoint handlers are thin and delegate business logic to services (`apps/backend/app/api/chat.py`).
- Service methods can be medium-sized and orchestrate persistence plus model calls (`apps/backend/app/services/assistant_service.py`).
- Backend endpoints favor dependency injection (`Depends(get_db_session)`) and typed payload models.
- Frontend handlers receive explicit event types (`FormEvent`, `ChangeEvent`) in TSX components.
- Backend returns typed schema objects (`ChatResponse`) or plain dictionaries for operational responses (`ingest_knowledge`).
- Frontend async API wrappers return typed promises (`Promise<TenantCreateResponse>`).
## Module Design
- Frontend uses default export for components and named exports for API helpers/types.
- Backend exposes module-level singletons for shared services (`assistant_service` in `apps/backend/app/services/assistant_service.py`).
- Minimal barrel usage; backend package init files exist but most imports target explicit modules.
## Testing Practices
- Test footprint is backend-only and minimal: one pytest-compatible health check in `apps/backend/tests/test_health.py`.
- A script-style API exerciser exists (`apps/backend/test_api.py`) but is not structured as a deterministic automated suite (inferred).
- No frontend test framework/config detected.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

## Pattern Overview
- FastAPI app composes feature routers and service classes (`apps/backend/app/main.py`, `apps/backend/app/api/*.py`, `apps/backend/app/services/*.py`).
- Frontend is a single React app that calls backend HTTP endpoints directly (`apps/frontend/src/App.tsx`, `apps/frontend/src/lib/api.ts`).
- Persistence uses SQLAlchemy async ORM entities mapped to tenant-scoped tables (`apps/backend/app/models/entities.py`, `apps/backend/app/db/session.py`).
## Layers
- Purpose: Collect tenant onboarding data, upload knowledge files, and run chat sandbox interactions.
- Location: `apps/frontend/src`
- Contains: React pages/components and API client helpers.
- Depends on: Browser `fetch`, Vite env vars, backend HTTP API.
- Used by: End users through Vite dev server or Nginx static build (`apps/frontend/Dockerfile`).
- Purpose: Expose HTTP endpoints for health, tenant lifecycle, chat, and analytics.
- Location: `apps/backend/app/api`
- Contains: FastAPI routers (`health.py`, `tenants.py`, `chat.py`, `analytics.py`).
- Depends on: Pydantic request/response models and DB session dependency.
- Used by: Frontend clients and tests (`apps/backend/tests/test_health.py`).
- Purpose: Implement business workflows for tenant creation, knowledge ingestion, model orchestration, and reporting.
- Location: `apps/backend/app/services`
- Contains: `assistant_service.py`, `analytics.py`, `model_gateway.py`, `knowledge.py`, `document_parser.py`.
- Depends on: ORM entities, SQLAlchemy async session, provider SDKs (`groq`).
- Used by: API routers.
- Purpose: Define schema and manage DB lifecycle.
- Location: `apps/backend/app/models`, `apps/backend/app/db`, `infra/sql`
- Contains: ORM entities, async engine/session, SQL bootstrap migration.
- Depends on: SQLAlchemy and configured database URL.
- Used by: Service layer and app startup lifespan hooks.
## Data Flow
- Frontend: component-local React state with prop drilling from `App` to child components.
- Backend: request-scoped async DB sessions and persisted SQL state; no separate cache/state store.
## Key Abstractions
- Purpose: Bind every workflow to tenant identity and tenant-owned knowledge.
- Examples: `apps/backend/app/models/entities.py`, `apps/backend/app/services/assistant_service.py`.
- Pattern: Tenant ID is mandatory across creation, ingestion, chat, and analytics paths.
- Purpose: Separate model routing/fallback from endpoint handlers.
- Examples: `apps/backend/app/services/model_gateway.py`.
- Pattern: Protocol-based provider abstraction with primary+fallback execution.
- Purpose: Compute operational metrics from conversations/knowledge/reservations.
- Examples: `apps/backend/app/services/analytics.py`, `apps/backend/app/api/analytics.py`.
- Pattern: Thin API router + service queries using SQL aggregates.
## Entry Points
- Location: `apps/backend/app/main.py`
- Triggers: Uvicorn startup (`apps/backend/Dockerfile`) or local `uvicorn app.main:app`.
- Responsibilities: Initialize DB on lifespan start, configure CORS, and mount API routers.
- Location: `apps/frontend/src/main.tsx`
- Triggers: Vite dev/build runtime.
- Responsibilities: Render root React app and global styles.
- Location: `docker-compose.yml`
- Triggers: `docker compose up --build`.
- Responsibilities: Start Postgres, backend API container, and frontend Nginx container.
## Error Handling
- Validation and business conflicts use `HTTPException` with status codes 400/404/409/413/500 (`apps/backend/app/api/tenants.py`, `apps/backend/app/services/assistant_service.py`).
- LLM provider failures are intercepted in gateway and redirected to backup response generator (`apps/backend/app/services/model_gateway.py`).
## Cross-Cutting Concerns
- A second synchronous route/model stack exists under `apps/backend/app/routes` and `apps/backend/app/models/tenant.py` using `app/core/database.py`.
- This stack is inferred as legacy/unwired because `apps/backend/app/main.py` only mounts routers from `app/api`.
<!-- GSD:architecture-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
