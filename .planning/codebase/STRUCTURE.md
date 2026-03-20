# Codebase Structure

**Analysis Date:** 2026-03-21

## Directory Layout

```text
project-root/
├── apps/                    # Deployable application code
│   ├── backend/             # FastAPI service and tests
│   │   ├── app/             # Backend source package
│   │   │   ├── api/         # Active FastAPI routers
│   │   │   ├── services/    # Business/service orchestration
│   │   │   ├── models/      # ORM entities + schema variants
│   │   │   ├── db/          # Async SQLAlchemy session/bootstrap
│   │   │   ├── core/        # App settings + (legacy) sync DB helpers
│   │   │   └── routes/      # Legacy/inferred-unused router set
│   │   └── tests/           # Backend tests
│   ├── frontend/            # React + Vite single-page app
│   │   └── src/             # UI components and API client code
│   └── widget/              # Widget static assets (duplicate path exists at root)
├── infra/
│   └── sql/                 # SQL init scripts for Postgres bootstrap
├── widget/                  # Root-level widget assets (inferred duplicate copy)
├── .github/                 # GSD workflows, skills, and agent definitions
└── .planning/               # Planning artifacts and codebase mapping docs
```

## Directory Purposes

**apps/backend/app/api:**
- Purpose: Define active REST endpoints.
- Contains: `health.py`, `tenants.py`, `chat.py`, `analytics.py`.
- Key files: `apps/backend/app/api/tenants.py`, `apps/backend/app/api/chat.py`.

**apps/backend/app/services:**
- Purpose: Hold orchestration logic and domain services.
- Contains: Assistant workflow, model gateway, context ranking, parsing, analytics.
- Key files: `apps/backend/app/services/assistant_service.py`, `apps/backend/app/services/model_gateway.py`.

**apps/backend/app/models:**
- Purpose: Persisted entity schemas and request/response models.
- Contains: Active SQLAlchemy entities (`entities.py`), Pydantic models (`schemas.py`), plus legacy model (`tenant.py`).
- Key files: `apps/backend/app/models/entities.py`, `apps/backend/app/models/schemas.py`.

**apps/frontend/src/components:**
- Purpose: User-facing screens for onboarding and chat testing.
- Contains: Form UX, chat sandbox, admin dashboard component.
- Key files: `apps/frontend/src/components/OnboardingForm.tsx`, `apps/frontend/src/components/ChatSandbox.tsx`.

**infra/sql:**
- Purpose: Initialize database schema in Docker Postgres flow.
- Contains: SQL DDL script(s).
- Key files: `infra/sql/001_init.sql`.

## Key File Locations

**Entry Points:**
- `apps/backend/app/main.py`: FastAPI app creation, lifespan hooks, router registration.
- `apps/frontend/src/main.tsx`: React bootstrap and root render.
- `docker-compose.yml`: Multi-container local runtime wiring.

**Configuration:**
- `apps/backend/app/core/config.py`: Environment-driven backend settings.
- `apps/frontend/vite.config.ts`: Vite dev server and plugin config.
- `apps/frontend/package.json`: Frontend scripts/dependencies.
- `apps/backend/requirements.txt`: Backend package dependencies.

**Core Logic:**
- `apps/backend/app/services/assistant_service.py`: Tenant + chat orchestration and persistence.
- `apps/backend/app/services/analytics.py`: Tenant analytics aggregations.
- `apps/frontend/src/lib/api.ts`: Browser-side API contract layer.

**Testing:**
- `apps/backend/tests/test_health.py`: API health check.
- `apps/backend/test_api.py`: additional backend test module at package root.

## Naming Conventions

**Files:**
- Backend Python uses snake_case module names: `assistant_service.py`, `model_gateway.py`.
- Frontend React components use PascalCase filenames: `OnboardingForm.tsx`, `AdminDashboard.tsx`.

**Directories:**
- Functional grouping by concern: `api`, `services`, `models`, `db`, `core`.

## Where to Add New Code

**New Backend Feature:**
- Primary code: `apps/backend/app/api` for endpoint, `apps/backend/app/services` for workflow, `apps/backend/app/models` for schemas/entities.
- Tests: `apps/backend/tests`.

**New Frontend Module:**
- Implementation: `apps/frontend/src/components`.
- API integration helpers: `apps/frontend/src/lib`.

**Utilities:**
- Backend shared helpers: `apps/backend/app/services` or `apps/backend/app/core` (for non-domain cross-cutting helpers).

## Special Directories

**apps/backend/venv:**
- Purpose: Local Python virtual environment.
- Generated: Yes.
- Committed: Yes (currently present in workspace).

**.planning/codebase:**
- Purpose: Generated architectural/convention reference docs for GSD workflow.
- Generated: Yes.
- Committed: Yes (expected in this workflow).

**apps/backend/app/routes:**
- Purpose: Inferred legacy FastAPI router set.
- Generated: No.
- Committed: Yes.

---

*Structure analysis: 2026-03-21*
