# 🚀 Copilot Finishing Roadmap

This document serves as an execution plan for GitHub Copilot (or any AI assistant) to finalize the AI Assistant Builder. It is derived directly from the known tech debt, security vulnerabilities, and scalability limits identified in `CONCERNS.md`.

---

## Phase 1: Security & Abuse Prevention (High Priority)
Currently, tenant endpoints are unprotected, CORS is open, and there is no rate limiting.

**Task 1.1: Implement API Key Authentication**
- **Goal:** Secure the `/api/tenants`, `/api/chat`, and `/api/analytics` endpoints so only authorized requests can access them.
- **Copilot Prompt:**
  > "@workspace Look at `apps/backend/app/api/`. Currently, tenant and analytics endpoints do not enforce authentication. Please implement a secure API Key dependency in `apps/backend/app/core/auth/dependencies.py` and apply it to the routers in `tenants.py` and `analytics.py`."

**Task 1.2: Add Rate Limiting**
- **Goal:** Protect the Groq LLM API quota and prevent abuse.
- **Copilot Prompt:**
  > "@workspace We need to add rate limiting to `apps/backend/app/api/chat.py` and `apps/backend/app/api/tenants.py` to prevent abuse. Please implement a Redis-based or memory-based rate limiter middleware (e.g., using `slowapi`) for the FastAPI backend."

**Task 1.3: Lock Down CORS**
- **Goal:** Restrict the `allow_origins` policy in `main.py`.
- **Copilot Prompt:**
  > "@workspace In `apps/backend/app/main.py`, the CORS middleware currently allows all origins (`*`). Update this to read a list of allowed origins from `apps/backend/app/core/config.py`, while keeping it flexible enough for the embeddable widget."

---

## Phase 2: Tech Debt Cleanup (Medium Priority)
Two backend architectures are currently coexisting, and the frontend has monolithic components.

**Task 2.1: Remove Legacy Sync Database Routes**
- **Goal:** Enforce the modern async SQLAlchemy v2 architecture and remove the drift risk.
- **Copilot Prompt:**
  > "@workspace Based on `.planning/codebase/CONCERNS.md`, there is a dual backend implementation. Please carefully delete the legacy synchronous routes in `apps/backend/app/routes/` and the old `apps/backend/app/models/tenant.py`, ensuring all endpoints in `apps/backend/app/api/` are strictly using the async patterns from `apps/backend/app/db/session.py`."

**Task 2.2: Refactor Monolithic React Components**
- **Goal:** Split `AdminDashboard.tsx` and `OnboardingForm.tsx` into smaller, testable sub-components.
- **Copilot Prompt:**
  > "@workspace The file `apps/frontend/src/components/AdminDashboard.tsx` is monolithic. Please refactor it by extracting the 'Overview', 'Conversations', and 'Reservations' tabs into their own separate component files inside an `apps/frontend/src/components/dashboard/` folder."

---

## Phase 3: Database & Scalability (Medium Priority)
Relying on SQLite and `auto_create_tables` limits scalability and makes schema changes dangerous.

**Task 3.1: Implement Alembic Migrations**
- **Goal:** Safely manage PostgreSQL schema evolutions instead of using SQLAlchemy's `create_all()`.
- **Copilot Prompt:**
  > "@workspace Set up Alembic for the FastAPI backend in `apps/backend/`. Create the `alembic.ini` file, configure the `env.py` to use our async SQLAlchemy engine from `apps/backend/app/db/session.py` and our `Base` metadata from `apps/backend/app/models/entities.py`. Generate the first initial migration script."

**Task 3.2: Fix N+1 Analytics Query**
- **Goal:** Optimize the daily metrics loop in the analytics service.
- **Copilot Prompt:**
  > "@workspace In `apps/backend/app/services/analytics.py`, there is an N+1 query issue for daily metrics where it loops over days. Please refactor this to use a single `GROUP BY date` PostgreSQL/SQLAlchemy aggregation query."

---

## Phase 4: Testing & Hardening (Ongoing)
Test coverage is minimal, which allows regressions to slip through.

**Task 4.1: Write Backend Integration Tests**
- **Goal:** Cover the main flows (onboarding, chat, analytics) using `pytest`.
- **Copilot Prompt:**
  > "@workspace The test coverage in `apps/backend/tests/` is currently limited to `test_health.py`. Please write a comprehensive `test_chat_api.py` and `test_analytics_api.py` using `FastAPI TestClient`. Make sure to mock the Groq API call in the model gateway."

**Task 4.2: Implement Robust Model Fallback**
- **Goal:** Ensure the LLM gateway falls back cleanly and logs errors properly.
- **Copilot Prompt:**
  > "@workspace In `apps/backend/app/services/model_gateway.py`, the fallback provider silently degrades quality. Update this to use typed exception handling (e.g., catching `RateLimitError` or `APIConnectionError` specifically), log the failure with standard Python `logging`, and return explicit fallback reason fields in the metadata."