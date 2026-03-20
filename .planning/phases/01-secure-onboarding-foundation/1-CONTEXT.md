# Phase 1: Secure Onboarding Foundation - Context

**Gathered:** 2026-03-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 1 delivers secure tenant onboarding and deployable widget setup with baseline tenant security and abuse guardrails. This phase clarifies implementation choices for onboarding flow, widget snippet behavior, tenant access enforcement, and abuse control behavior within existing roadmap scope.

</domain>

<decisions>
## Implementation Decisions

### Onboarding validation policy
- **D-01:** Use strict required core fields in v1 onboarding (business name, domain, at least one service) before tenant creation is accepted.
- **D-02:** Validation failures must return actionable errors aligned with field-level feedback in onboarding UI.

### Widget snippet defaults
- **D-03:** Use a fully parameterized widget snippet in v1 so owners can control tenant-specific embed settings without backend changes.
- **D-04:** Preserve safe defaults for optional parameters to keep onboarding-to-live fast for non-technical owners.

### Tenant access boundary
- **D-05:** Enforce SEC-01 in Phase 1 (authenticated owner/admin access plus server-side tenant checks); tenant ID alone is not sufficient authorization.
- **D-06:** Tenant-bound owner operations must reject cross-tenant attempts with explicit authorization errors.

### Abuse protection behavior
- **D-07:** Apply rate limiting to chat and upload endpoints and return clear `429` responses with retry guidance.
- **D-08:** Abuse guard behavior should be visible and deterministic (no silent over-consumption path).

### the agent's Discretion
- Exact limiter implementation choice and storage backend.
- API-key vs session token mechanics for owner/admin auth, as long as SEC-01 is satisfied.
- Final snippet parameter naming and formatting conventions.

</decisions>

<specifics>
## Specific Ideas

- Keep onboarding straightforward for local business owners while retaining strict correctness checks.
- Preserve a copy-paste-friendly widget embed experience.
- Prioritize trust boundaries early to avoid data leakage across tenants.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase and requirement definitions
- `.planning/ROADMAP.md` - Phase 1 scope, requirements, and success criteria.
- `.planning/REQUIREMENTS.md` - ONB-01..ONB-04 and SEC-01..SEC-03 requirement contracts.
- `.planning/PROJECT.md` - Core value, constraints, and project-level decisions.

### Existing codebase guidance
- `.planning/codebase/STRUCTURE.md` - Backend/frontend/widget module layout and integration points.
- `.planning/codebase/CONVENTIONS.md` - Naming/API/model/error conventions to follow.
- `.planning/codebase/CONCERNS.md` - Security and abuse concerns motivating Phase 1 hardening.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `apps/frontend/src/components/OnboardingForm.tsx`: Existing onboarding surface to evolve for strict validation and snippet UX.
- `apps/frontend/src/lib/api.ts`: Existing tenant/onboarding API client layer for request and error handling updates.
- `apps/backend/app/api/tenants.py`: Current tenant creation and onboarding-related endpoints.
- `apps/backend/app/main.py`: CORS middleware and app-level security guardrail integration point.

### Established Patterns
- Backend routes use typed Pydantic request/response models and explicit `HTTPException` responses.
- Frontend uses typed API wrappers and component-level async error handling.
- Current codebase is brownfield; phase should extend existing modules rather than rewrite architecture.

### Integration Points
- Onboarding UI -> tenant API contract -> backend validation and persistence.
- Tenant creation response -> widget snippet generation and owner handoff.
- App middleware and endpoint guards -> CORS restrictions, auth checks, and abuse limiting.

</code_context>

<deferred>
## Deferred Ideas

- Reservation notification workflow details (Phase 3).
- Knowledge retrieval quality improvements (Phase 4).
- Advanced analytics and operations UX expansion (Phase 5).

</deferred>

---

*Phase: 01-secure-onboarding-foundation*
*Context gathered: 2026-03-21*
