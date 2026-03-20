# Coding Conventions

**Analysis Date:** 2026-03-21

## Naming Patterns

**Files:**
- Frontend React components use `PascalCase.tsx` (for example `apps/frontend/src/components/OnboardingForm.tsx`).
- Frontend utilities/types use lowercase module names (for example `apps/frontend/src/lib/api.ts`).
- Backend modules use `snake_case.py` (for example `apps/backend/app/services/assistant_service.py`).
- Tests follow `test_*.py` naming (for example `apps/backend/tests/test_health.py`).

**Functions:**
- Frontend functions and hooks use `camelCase` (`handleSubmit`, `uploadDocuments` in `apps/frontend/src/components/OnboardingForm.tsx`).
- Backend functions use `snake_case` (`create_tenant`, `get_db_session` in `apps/backend/app/api/tenants.py` and `apps/backend/app/db/session.py`).

**Variables:**
- Frontend state and locals use `camelCase` (`isSubmitting`, `tenantId` in `apps/frontend/src/components/ChatSandbox.tsx`).
- Backend variables and fields use `snake_case` (`tenant_id`, `source_url` in `apps/backend/app/models/schemas.py`).

**Types:**
- TypeScript interfaces use `PascalCase` with suffixes like `Payload`/`Response` (`TenantCreatePayload`, `ChatResponse` in `apps/frontend/src/lib/api.ts`).
- Python Pydantic schemas use `PascalCase` class names with request/response suffixes (`TenantCreateRequest`, `TenantCreateResponse` in `apps/backend/app/models/schemas.py`).
- SQLAlchemy entities use `PascalCase` with `Entity` suffix (`TenantEntity` in `apps/backend/app/models/entities.py`).

## Code Style

**Formatting:**
- No repository-level formatter config detected (`.prettierrc`, `pyproject.toml`, `black` config not found).
- Style appears tool-default and editor-driven (inferred).

**Linting:**
- No repository-level lint config detected (`eslint`, `ruff`, `flake8`, `biome` config files not found).
- TypeScript strictness is enforced in `apps/frontend/tsconfig.json` (`"strict": true`).

## Import Organization

**Order:**
1. External packages first (`react`, `fastapi`, `sqlalchemy`).
2. Internal app imports second (`app.services...`, `../lib/api`).
3. Side-effect imports last where used (`./styles.css` in `apps/frontend/src/main.tsx`).

**Path Aliases:**
- Not detected; relative imports are used in frontend and absolute `app.*` package imports are used in backend.

## API Conventions

**Patterns:**
- FastAPI routers define resource prefixes and tags (`APIRouter(prefix="/tenants", tags=["tenants"])` in `apps/backend/app/api/tenants.py`).
- Request/response models are explicitly typed with `response_model` on endpoints (`apps/backend/app/api/chat.py`).
- API payload fields use `snake_case` consistently (`tenant_id`, `text_blocks` in `apps/backend/app/models/schemas.py`).
- Frontend API client maps directly to backend routes (`createTenant`, `chatWithAssistant` in `apps/frontend/src/lib/api.ts`).

## Data Model Conventions

**Patterns:**
- Validation rules are defined at schema boundaries using Pydantic `Field` constraints (`apps/backend/app/models/schemas.py`).
- Persistence layer uses SQLAlchemy 2 typed mappings (`Mapped[...]`, `mapped_column` in `apps/backend/app/models/entities.py`).
- Entity names end with `Entity`; API schemas end with `Request`/`Response`; this split is consistent across backend models.
- UUID strings are primary IDs for tenant-facing entities (`apps/backend/app/models/entities.py`).

## Error Handling

**Patterns:**
- Backend raises `HTTPException` with explicit status codes for expected API errors (`apps/backend/app/api/tenants.py`, `apps/backend/app/services/assistant_service.py`).
- Frontend API client throws `Error` on non-OK responses and surfaces user-friendly fallback messages in components (`apps/frontend/src/lib/api.ts`, `apps/frontend/src/components/ChatSandbox.tsx`).

## Logging

**Framework:** console/standard exceptions

**Patterns:**
- Frontend uses `console.error(...)` in async failure paths (`apps/frontend/src/components/OnboardingForm.tsx`).
- Backend generally returns structured HTTP errors instead of explicit logging in route/service code (inferred).

## Comments

**When to Comment:**
- Comments are sparse and mostly used for non-obvious behavior (for example table-discovery note in `apps/backend/app/db/session.py`, validation notes in `apps/backend/app/api/tenants.py`).

**JSDoc/TSDoc:**
- Not detected in sampled frontend/backend source.

## Function Design

**Size:**
- Endpoint handlers are thin and delegate business logic to services (`apps/backend/app/api/chat.py`).
- Service methods can be medium-sized and orchestrate persistence plus model calls (`apps/backend/app/services/assistant_service.py`).

**Parameters:**
- Backend endpoints favor dependency injection (`Depends(get_db_session)`) and typed payload models.
- Frontend handlers receive explicit event types (`FormEvent`, `ChangeEvent`) in TSX components.

**Return Values:**
- Backend returns typed schema objects (`ChatResponse`) or plain dictionaries for operational responses (`ingest_knowledge`).
- Frontend async API wrappers return typed promises (`Promise<TenantCreateResponse>`).

## Module Design

**Exports:**
- Frontend uses default export for components and named exports for API helpers/types.
- Backend exposes module-level singletons for shared services (`assistant_service` in `apps/backend/app/services/assistant_service.py`).

**Barrel Files:**
- Minimal barrel usage; backend package init files exist but most imports target explicit modules.

## Testing Practices

**Current practice:**
- Test footprint is backend-only and minimal: one pytest-compatible health check in `apps/backend/tests/test_health.py`.
- A script-style API exerciser exists (`apps/backend/test_api.py`) but is not structured as a deterministic automated suite (inferred).
- No frontend test framework/config detected.

---

*Convention analysis: 2026-03-21*
