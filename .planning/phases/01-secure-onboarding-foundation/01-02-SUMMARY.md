---
phase: 01-secure-onboarding-foundation
plan: 02
subsystem: api
tags: [fastapi, pydantic, validation, rate-limiting, widget]
requires:
  - phase: 01-00
    provides: Wave 0 backend test targets
  - phase: 01-01
    provides: owner authorization dependency and explicit CORS allowlist
provides:
  - Strict onboarding request validation for required business fields and service lists
  - Parameterized tenant widget snippet output with safe defaults
  - Deterministic upload and chat throttling with explicit 429 responses
affects: [01-03]
tech-stack:
  added: []
  patterns:
    - Pydantic field validators for actionable onboarding feedback
    - Shared in-memory rate limiting with exception-to-JSON conversion
    - Settings-driven widget snippet parameterization
key-files:
  created:
    - .planning/phases/01-secure-onboarding-foundation/01-02-SUMMARY.md
  modified:
    - apps/backend/app/models/schemas.py
    - apps/backend/app/services/assistant_service.py
    - apps/backend/app/api/tenants.py
    - apps/backend/app/api/chat.py
    - apps/backend/tests/test_onboarding_api.py
    - apps/backend/tests/test_widget_snippet.py
    - apps/backend/tests/test_upload_api.py
    - apps/backend/tests/test_rate_limits.py
key-decisions:
  - "Use custom validators for business_name, domain, and category so blank or malformed input returns field-level Pydantic errors instead of generic length failures."
  - "Keep widget embed defaults centralized in settings so the snippet stays copy-paste friendly and easy to rebrand without code changes."
  - "Use a shared RateLimitExceeded exception for chat and upload throttles so 429 responses always include retry guidance."
patterns-established:
  - "Required onboarding fields are normalized and validated before tenant persistence."
  - "Tenant widget snippet generation is parameterized through app settings."
  - "Rate-limited routes surface deterministic JSON payloads with retry_after_seconds."
requirements-completed: [ONB-01, ONB-02, ONB-03, ONB-04, SEC-03]
duration: 25 min
completed: 2026-05-22
---

# Phase 1 Plan 02: Onboarding Contracts and Abuse Guardrails Summary

**Strict onboarding validation, tenant-specific widget defaults, and deterministic 429 guardrails for chat/upload.**

## Performance

- **Duration:** 25 min
- **Started:** 2026-05-22T22:26:00+05:30
- **Completed:** 2026-05-22T22:51:31.0073558+05:30
- **Tasks:** 2
- **Files modified:** 8

## Accomplishments
- Enforced required onboarding fields with actionable field-level errors for blank business name, invalid domain, and category values.
- Parameterized the tenant widget embed script through settings while preserving safe defaults for the copy-paste onboarding handoff.
- Added deterministic in-memory throttling for chat and upload routes with a shared `429` payload shape and retry guidance.
- Locked in backend tests for onboarding validation, widget snippet generation, upload validation, and rate limiting.

## Task Commits
1. **Task 1: Enforce strict onboarding validation and parameterized widget snippet** - `821ba10` (feat)
2. **Task 2: Add deterministic upload and chat abuse protection** - `821ba10` (feat)

## Files Created/Modified
- `.planning/phases/01-secure-onboarding-foundation/01-02-SUMMARY.md` - phase completion record.
- `apps/backend/app/models/schemas.py` - strict onboarding validation and service normalization.
- `apps/backend/app/services/assistant_service.py` - settings-driven widget snippet generation.
- `apps/backend/app/api/tenants.py` - upload validation and upload rate limiting.
- `apps/backend/app/api/chat.py` - chat rate limiting.
- `apps/backend/tests/test_onboarding_api.py` - validation coverage.
- `apps/backend/tests/test_widget_snippet.py` - widget snippet coverage.
- `apps/backend/tests/test_upload_api.py` - upload validation coverage.
- `apps/backend/tests/test_rate_limits.py` - deterministic `429` coverage.

## Decisions Made
- Centralize widget defaults in `app.core.config.settings` to keep onboarding output configurable without backend code changes.
- Use custom validators instead of length-only field constraints so user-facing validation messages stay specific and actionable.
- Reuse one `RateLimitExceeded` exception path for both chat and upload so `429` behavior stays consistent.

## Deviations from Plan
None - plan executed exactly as written.

## Issues Encountered
- `pytest` was not installed in the backend virtual environment, so it was installed before running the verification suite.
- The app required `AI_AGENT_GROQ_API_KEY` at import time, so tests were run with a dummy value to satisfy startup.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Phase 1 backend contracts are hardened and verified.
- `01-03` can now focus on onboarding UI error clarity and the remaining Phase 1 regression coverage.

---
*Phase: 01-secure-onboarding-foundation*
*Completed: 2026-05-22*