# Phase 1: Secure Onboarding Foundation - Research

**Researched:** 2026-03-21  
**Domain:** Secure multi-tenant onboarding (FastAPI + React)  
**Confidence:** MEDIUM-HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
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

### Claude's Discretion
- Exact limiter implementation choice and storage backend.
- API-key vs session token mechanics for owner/admin auth, as long as SEC-01 is satisfied.
- Final snippet parameter naming and formatting conventions.

### Deferred Ideas (OUT OF SCOPE)
- Reservation notification workflow details (Phase 3).
- Knowledge retrieval quality improvements (Phase 4).
- Advanced analytics and operations UX expansion (Phase 5).
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| ONB-01 | Business owner can create a tenant profile with name, domain, services, and description. | Strict schema + server validation + deterministic field-level error contract. |
| ONB-02 | Business owner can upload supported documents (PDF, DOCX, TXT) during onboarding. | Keep UploadFile + multipart flow, add ownership checks and upload guardrails. |
| ONB-03 | System validates file type and file size and returns clear errors for invalid uploads. | Normalize validation path with explicit 400/413 responses and shared error shape. |
| ONB-04 | Business owner receives an embeddable widget snippet with tenant-specific configuration. | Generate parameterized snippet template with safe defaults and tenant binding. |
| SEC-01 | Tenant-scoped endpoints enforce authorization checks beyond tenant ID possession. | Add auth dependency + tenant ownership resolution on every tenant-scoped endpoint. |
| SEC-02 | API CORS policy is restricted to explicit allowed origins for production contexts. | Replace wildcard CORS with explicit origin allowlist from settings. |
| SEC-03 | Chat and upload endpoints enforce abuse protections (rate limits and/or request guards). | Add route-level rate limiter + deterministic 429 callback + request-size constraints. |
</phase_requirements>

## Summary

Phase 1 should be implemented as security-hardening of existing flows, not a new architecture. The current backend already has onboarding, upload, and chat paths, but tenant identity is effectively trusted from user-provided IDs, CORS is globally open (`allow_origins=["*"]` with credentials enabled), and there is no abuse control on high-cost endpoints. The highest-risk gap is Broken Object Level Authorization: tenant ID presence is checked, but tenant ownership is not.

The standard path is to enforce authentication and authorization via FastAPI security dependencies, then bind tenant access to the authenticated principal on every tenant-scoped endpoint. For abuse controls, use a maintained FastAPI rate-limiter library (not a custom in-memory implementation) and return explicit 429 responses with retry guidance. Keep onboarding and upload UX simple, but make validation and error contracts deterministic.

**Primary recommendation:** Implement a single auth+tenant-ownership dependency layer first, then enforce explicit CORS allowlists and endpoint-level throttling before refining onboarding/widget UX details.

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| fastapi | 0.116.1 (repo pinned), latest 0.135.1 (released 2026-03-01) | API framework and dependency/security model | Existing project foundation and all current route wiring depend on FastAPI patterns. |
| pydantic | 2.11.7 (repo pinned), latest 2.12.5 (released 2025-11-26) | Request/response validation and typed contracts | Existing schemas already use Pydantic v2 models and constraints. |
| sqlalchemy | 2.0.42 (repo pinned) | Tenant/user persistence and ownership checks | Existing async ORM/session layer is already integrated and avoids architectural churn. |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| python-multipart | 0.0.22 latest (released 2026-01-25), repo pinned 0.0.6 | Multipart form/file parsing for UploadFile endpoints | Required for onboarding document uploads and OAuth2 form flows. |
| fastapi-limiter | 0.2.0 (released 2026-02-06) | Route and middleware rate limiting with configurable identifier/callback | Use for SEC-03 on chat/upload endpoints with deterministic 429 behavior. |
| starlette CORSMiddleware | bundled with FastAPI/Starlette | Browser CORS controls | Use explicit origin allowlists, not wildcard + credentials. |
| fastapi.security | bundled with FastAPI | Authentication dependency primitives (OAuth2 bearer/API key) | Use to gate owner/admin endpoints and integrate with OpenAPI docs. |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| fastapi-limiter | slowapi | slowapi is mature and production-used, but has explicit endpoint-signature constraints and less recent release cadence. |
| OAuth2 bearer first | API key header first | API key is faster to ship for Phase 1, but JWT/OAuth2 scales better for future multi-role/session flows. |
| Route-level limiter dependencies | Global middleware limiter | Global limiter is simpler to apply but can over-throttle low-risk routes unless skip rules are curated carefully. |

**Installation:**
```bash
pip install fastapi-limiter
pip install -U python-multipart
```

**Version verification:**
```bash
# Checked via PyPI project pages
# fastapi: 0.135.1 (2026-03-01)
# pydantic: 2.12.5 (2025-11-26)
# python-multipart: 0.0.22 (2026-01-25)
# fastapi-limiter: 0.2.0 (2026-02-06)
```

## Architecture Patterns

### Recommended Project Structure
```text
apps/backend/app/
├── api/
│   ├── tenants.py          # onboarding, upload endpoints
│   ├── chat.py             # chat endpoint
│   └── analytics.py        # tenant-scoped read endpoints
├── auth/
│   ├── dependencies.py     # get_current_owner/get_authorized_tenant
│   └── models.py           # auth context models
├── core/
│   └── config.py           # CORS origins, limiter settings, auth toggles
└── services/
    └── assistant_service.py
```

### Pattern 1: Tenant Ownership as a Dependency
**What:** Resolve authenticated principal once, then validate tenant ownership before route logic executes.  
**When to use:** Every endpoint that accepts tenant ID in path/body/query.

**Example:**
```python
# Source: https://fastapi.tiangolo.com/tutorial/security/first-steps/
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_subject(token: Annotated[str, Depends(oauth2_scheme)]):
    # Phase 1: token parse/lookup stub; replace with full verification later.
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing auth token")
    return {"subject": token}

async def require_tenant_access(tenant_id: str, subject=Depends(get_current_subject)):
    # Enforce subject->tenant binding via DB lookup.
    if not is_subject_allowed_for_tenant(subject["subject"], tenant_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tenant access denied")
```

### Pattern 2: Explicit CORS Allowlist from Settings
**What:** Configure `allow_origins` to concrete origins; avoid wildcard when credentials/authorization headers are used.  
**When to use:** All production API deployments.

**Example:**
```python
# Source: https://fastapi.tiangolo.com/tutorial/cors/
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)
```

### Pattern 3: Route-Level Rate Limiting with Deterministic 429
**What:** Apply rate limit dependencies on high-risk routes and return a consistent error payload.  
**When to use:** Chat, upload, and any cost-amplifying endpoint.

**Example:**
```python
# Source: https://pypi.org/project/fastapi-limiter/
from fastapi import Depends
from pyrate_limiter import Duration, Limiter, Rate
from fastapi_limiter.depends import RateLimiter

chat_limit = RateLimiter(limiter=Limiter(Rate(10, Duration.MINUTE)))

@router.post("", dependencies=[Depends(chat_limit)])
async def chat(...):
    ...
```

### Anti-Patterns to Avoid
- **Tenant ID as authorization:** Checking tenant existence is not authorization; enforce owner/admin-to-tenant binding.
- **Wildcard CORS with credentials:** `*` + credentials/authorization exposure is unsafe and violates explicit-origin requirement.
- **Custom ad-hoc limiter logic:** Hand-rolled counters miss burst windows, keying edge cases, and consistent 429 behavior.
- **Generic upload errors:** Returning only "Failed to upload" breaks ONB-03 feedback quality and slows UAT.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Auth extraction and auth docs wiring | Manual header parsing in every endpoint | `fastapi.security` dependencies | Centralized behavior and built-in OpenAPI security integration. |
| Browser CORS protocol behavior | Custom CORS headers middleware | Starlette/FastAPI `CORSMiddleware` | Correct preflight/simple request handling and credential rules. |
| Rate limiting algorithm/storage | In-memory dict counters per process | `fastapi-limiter` with `pyrate-limiter` backend | Correct window semantics, callback hooks, and route/middleware coverage. |
| Multipart parsing | Manual boundary parsing | `UploadFile` + `python-multipart` | Streaming-friendly parsing and stable form-data integration. |

**Key insight:** Phase 1 risk is security correctness, not feature novelty. Reusing standard middleware/dependency primitives lowers exploit and regression risk significantly.

## Common Pitfalls

### Pitfall 1: "Authenticated" but not tenant-authorized
**What goes wrong:** Caller authenticates once and can query any tenant by changing path ID.  
**Why it happens:** Authorization decision ignores object ownership boundary.  
**How to avoid:** Use an ownership dependency that validates `subject -> tenant_id` before service calls.  
**Warning signs:** 200 responses for cross-tenant IDs during API tests.

### Pitfall 2: CORS appears to work locally but leaks in production
**What goes wrong:** `allow_origins=["*"]` plus credentialed auth headers leaves permissive cross-origin surface.  
**Why it happens:** Dev defaults shipped as prod configuration.  
**How to avoid:** Explicit origin allowlist from env for each deploy environment.  
**Warning signs:** Any origin can call authenticated endpoints from browser context.

### Pitfall 3: Upload validation drifts across frontend/backend
**What goes wrong:** Frontend accepts file set/rules that backend rejects (or vice versa), producing poor UX.  
**Why it happens:** Validation rules duplicated in multiple places without shared contract.  
**How to avoid:** Define allowed extensions/max size in one backend source and expose constraints to UI.  
**Warning signs:** Frequent 400/413 support issues with "but UI allowed it" reports.

### Pitfall 4: Rate limits trigger unpredictably
**What goes wrong:** Different endpoints return inconsistent 429 messages or one endpoint is unprotected.  
**Why it happens:** Mixed ad-hoc guards instead of consistent limiter dependency/callback setup.  
**How to avoid:** Central limiter config + shared callback payload + endpoint inventory tests.  
**Warning signs:** Load test passes on one path, fails open on another.

## Code Examples

Verified patterns from official sources:

### OAuth2 bearer dependency skeleton
```python
# Source: https://fastapi.tiangolo.com/tutorial/security/first-steps/
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/secured")
async def secured(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
```

### CORS with explicit origins
```python
# Source: https://fastapi.tiangolo.com/tutorial/cors/
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://owner.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)
```

### Upload endpoint with UploadFile
```python
# Source: https://fastapi.tiangolo.com/tutorial/request-files/
from fastapi import UploadFile

async def upload(file: UploadFile):
    content = await file.read()
    return {"filename": file.filename, "size": len(content)}
```

### FastAPI limiter dependency
```python
# Source: https://pypi.org/project/fastapi-limiter/
from fastapi import Depends
from pyrate_limiter import Duration, Limiter, Rate
from fastapi_limiter.depends import RateLimiter

limit_dep = Depends(RateLimiter(limiter=Limiter(Rate(2, Duration.SECOND * 5))))
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Tenant existence check only | Object-level tenant authorization tied to authenticated principal | OWASP API Top 10 2023 emphasis | Prevents cross-tenant read/write abuse (SEC-01). |
| Wildcard CORS defaults | Explicit allowlisted origins with credential-safe config | Current FastAPI/Starlette guidance | Reduces browser-origin attack surface (SEC-02). |
| Ad-hoc throttling | Framework-supported limiter dependency/middleware | Mature FastAPI ecosystem (2025-2026 updates) | Deterministic 429 behavior and lower DoS/cost risk (SEC-03). |

**Deprecated/outdated:**
- Open CORS (`*`) for authenticated APIs: outdated for production tenant platforms.
- Treating tenant ID as secret authorization key: incompatible with OWASP BOLA guidance.

## Open Questions

1. **Auth mechanism in Phase 1: API key or OAuth2 bearer-first?**
   - What we know: Either is allowed by phase constraints if SEC-01 is met.
   - What's unclear: Existing user/owner identity store is not yet formalized in current models.
   - Recommendation: Use an owner API key model for Phase 1 speed, but keep dependency interface token-agnostic for JWT migration.

2. **Rate-limit storage backend choice**
   - What we know: fastapi-limiter can run with in-process or backend-backed limiters; callback supports deterministic 429.
   - What's unclear: Production deployment topology and shared-state requirement across instances.
   - Recommendation: Start with in-process for local/dev; plan Redis/shared backend before horizontal scaling.

3. **Widget snippet parameter contract**
   - What we know: Must be tenant-specific and parameterized with safe defaults (D-03/D-04).
   - What's unclear: Final parameter list (`theme`, `position`, `apiBase`, etc.) and allowed values.
   - Recommendation: Freeze a minimal v1 schema and validate server-side before returning snippet.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.4.2 + FastAPI TestClient |
| Config file | none - see Wave 0 |
| Quick run command | `python -m pytest apps/backend/tests/test_health.py -q` |
| Full suite command | `python -m pytest apps/backend/tests -q` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| ONB-01 | Tenant create enforces required business fields and clear validation errors | integration | `python -m pytest apps/backend/tests/test_onboarding_api.py::test_create_tenant_required_fields -q` | ❌ Wave 0 |
| ONB-02 | Supported onboarding documents upload successfully | integration | `python -m pytest apps/backend/tests/test_upload_api.py::test_upload_supported_files -q` | ❌ Wave 0 |
| ONB-03 | Invalid upload type/size returns actionable errors | integration | `python -m pytest apps/backend/tests/test_upload_api.py::test_upload_rejects_invalid_type_and_size -q` | ❌ Wave 0 |
| ONB-04 | Widget snippet includes tenant-specific configuration and safe defaults | unit/integration | `python -m pytest apps/backend/tests/test_widget_snippet.py::test_widget_snippet_is_parameterized -q` | ❌ Wave 0 |
| SEC-01 | Cross-tenant access is rejected despite valid authentication | integration/security | `python -m pytest apps/backend/tests/test_tenant_authz.py::test_cross_tenant_forbidden -q` | ❌ Wave 0 |
| SEC-02 | CORS only allows configured origins in production mode | integration | `python -m pytest apps/backend/tests/test_cors_policy.py::test_disallowed_origin_blocked -q` | ❌ Wave 0 |
| SEC-03 | Chat/upload endpoints enforce deterministic 429 throttling | integration/load-smoke | `python -m pytest apps/backend/tests/test_rate_limits.py::test_chat_and_upload_rate_limited -q` | ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** `python -m pytest apps/backend/tests/test_health.py -q`
- **Per wave merge:** `python -m pytest apps/backend/tests -q`
- **Phase gate:** Full suite green before /gsd:verify-work

### Wave 0 Gaps
- [ ] `apps/backend/tests/test_onboarding_api.py` - covers REQ ONB-01
- [ ] `apps/backend/tests/test_upload_api.py` - covers REQ ONB-02 and ONB-03
- [ ] `apps/backend/tests/test_widget_snippet.py` - covers REQ ONB-04
- [ ] `apps/backend/tests/test_tenant_authz.py` - covers REQ SEC-01
- [ ] `apps/backend/tests/test_cors_policy.py` - covers REQ SEC-02
- [ ] `apps/backend/tests/test_rate_limits.py` - covers REQ SEC-03
- [ ] Shared auth/tenant fixtures in `apps/backend/tests/conftest.py`

## Sources

### Primary (HIGH confidence)
- https://fastapi.tiangolo.com/tutorial/security/first-steps/ - FastAPI security dependencies and bearer token flow
- https://fastapi.tiangolo.com/tutorial/cors/ - CORS behavior and explicit-origin guidance
- https://fastapi.tiangolo.com/tutorial/request-files/ - UploadFile/form-data behavior and constraints
- https://starlette.dev/middleware/ - middleware behavior, CORS constraints, and host/security middleware options
- https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/ - object-level authorization requirements
- https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/ - rate limiting and resource guardrails

### Secondary (MEDIUM confidence)
- https://pypi.org/project/fastapi-limiter/ - package metadata, usage examples, release date/version
- https://github.com/long2ice/fastapi-limiter - implementation/readme details and recent activity
- https://pypi.org/project/fastapi/ - latest release verification
- https://pypi.org/project/pydantic/ - latest release verification
- https://pypi.org/project/python-multipart/ - latest release verification

### Tertiary (LOW confidence)
- https://github.com/laurentS/slowapi - alternative limiter capability and limitations summary (not selected as primary stack)

## Metadata

**Confidence breakdown:**
- Standard stack: MEDIUM - core framework is certain; limiter choice has ecosystem alternatives.
- Architecture: HIGH - directly supported by FastAPI/Starlette/OWASP guidance and current code shape.
- Pitfalls: HIGH - validated against current repo concerns and widely documented API security risks.

**Research date:** 2026-03-21  
**Valid until:** 2026-04-20
