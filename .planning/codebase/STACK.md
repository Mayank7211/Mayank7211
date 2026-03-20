# Technology Stack

**Analysis Date:** 2026-03-21

## Languages

**Primary:**
- Python 3.x (version not pinned; inferred) - backend API/services in `apps/backend/app/**/*.py`
- TypeScript 5.x - frontend app in `apps/frontend/src/**/*.ts` and `apps/frontend/src/**/*.tsx`
- JavaScript (ES6+) - embeddable widget scripts in `apps/widget/agent.js` and `widget/agent.js`
- SQL (PostgreSQL dialect) - schema/init scripts in `infra/sql/001_init.sql`

**Secondary:**
- Markdown - project and process docs (`README.md`, `SUMMARY.md`, `.planning/**`)

## Runtime

**Environment:**
- Python runtime for FastAPI backend (inferred from `apps/backend/requirements.txt`)
- Node.js runtime for frontend tooling and dev server (inferred from `apps/frontend/package.json`)
- Browser runtime for React UI and standalone widget scripts (`apps/frontend/src/main.tsx`, `apps/widget/agent.js`)

**Package Manager:**
- Frontend: npm (inferred from script usage in `README.md` and `apps/frontend/package.json`)
- Backend: pip with requirements file (`apps/backend/requirements.txt`)
- Lockfiles: missing for both ecosystems (`package-lock.json`, `poetry.lock`, `Pipfile.lock` not detected)

## Frameworks

**Core:**
- FastAPI 0.116.1 - backend HTTP API and routing (`apps/backend/requirements.txt`, `apps/backend/app/main.py`)
- React 18.3.1 + React DOM 18.3.1 - frontend UI (`apps/frontend/package.json`)
- SQLAlchemy 2.0.42 - ORM/data layer (`apps/backend/requirements.txt`, `apps/backend/app/db/session.py`)

**Testing:**
- pytest 8.4.2 - backend tests (`apps/backend/requirements.txt`, `apps/backend/tests/test_health.py`)
- FastAPI TestClient - API test client (`apps/backend/tests/test_health.py`)

**Build/Dev:**
- Vite 5.4.10 - frontend dev/build (`apps/frontend/package.json`, `apps/frontend/vite.config.ts`)
- TypeScript compiler 5.6.3 - type checking/build step (`apps/frontend/package.json`, `apps/frontend/tsconfig.json`)
- Uvicorn 0.35.0 - ASGI server for backend (`apps/backend/requirements.txt`, `README.md`)

## Key Dependencies

**Critical:**
- `groq==0.14.0` - primary LLM provider client (`apps/backend/app/services/model_gateway.py`)
- `pydantic==2.11.7` + `pydantic-settings==2.10.1` - schema and env config (`apps/backend/app/models/schemas.py`, `apps/backend/app/core/config.py`)
- `python-multipart==0.0.6` - file upload handling in tenant upload endpoint (`apps/backend/app/api/tenants.py`)

**Infrastructure:**
- `asyncpg==0.30.0` - async PostgreSQL driver (`apps/backend/requirements.txt`)
- `aiosqlite==0.21.0` - local SQLite async fallback/dev DB (`apps/backend/app/core/config.py`)
- `PyPDF2==4.0.1` and `python-docx==0.8.11` - document ingestion/parsing (`apps/backend/app/services/document_parser.py`)
- `@vitejs/plugin-react==4.3.4` - React transform/plugin (`apps/frontend/package.json`, `apps/frontend/vite.config.ts`)

## Configuration

**Environment:**
- Backend settings loaded from `.env` with prefix `AI_AGENT_` (`apps/backend/app/core/config.py`)
- Example backend vars in `apps/backend/.env.example`:
  - `AI_AGENT_DATABASE_URL`
  - `AI_AGENT_GROQ_API_KEY`
  - `AI_AGENT_DEFAULT_SMALL_MODEL`
  - `AI_AGENT_DEFAULT_LARGE_MODEL`
  - `AI_AGENT_AUTO_CREATE_TABLES`
- Frontend base API URL via `VITE_API_BASE_URL` (`apps/frontend/.env.example`, `apps/frontend/src/env.d.ts`)

**Build/Run Commands:**
- Frontend (`apps/frontend/package.json`):
  - `npm run dev`
  - `npm run build`
  - `npm run preview`
- Backend (`README.md` + inferred):
  - `pip install -r requirements.txt`
  - `uvicorn app.main:app --reload --port 8000`
  - `pytest` (inferred from dependency + `apps/backend/tests/test_health.py`)

## Platform Requirements

**Development:**
- Local backend on `http://localhost:8000` (documented in `README.md` and used by frontend/widget defaults)
- Local frontend on Vite default `http://localhost:5173` (`README.md`, `apps/frontend/vite.config.ts`)
- Database options:
  - PostgreSQL in containerized workflow (`README.md`, `apps/backend/.env.example`, `infra/sql/001_init.sql`)
  - SQLite local fallback (`apps/backend/app/core/config.py`)

**Production:**
- Deployment target not strictly codified; inferred split architecture:
  - ASGI-hosted FastAPI service
  - Static frontend bundle
  - Hosted database
- Widget CDN path in response is placeholder/inferred (`apps/backend/app/services/assistant_service.py` uses `https://cdn.your-app.com/widget.js`)

---

*Stack analysis: 2026-03-21*
