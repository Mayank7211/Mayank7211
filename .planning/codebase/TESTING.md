# Testing Patterns

**Analysis Date:** 2026-03-21

## Test Framework

**Runner:**
- `pytest` 8.4.2 (dependency pinned in `apps/backend/requirements.txt`).
- Config: Not detected (`pytest.ini`/`pyproject.toml`/`tox.ini` not present).

**Assertion Library:**
- Native `assert` statements with pytest discovery (`apps/backend/tests/test_health.py`).

**Run Commands:**
```bash
cd apps/backend && pytest                 # Run discovered tests (inferred command)
cd apps/backend && pytest -q              # Quieter output (inferred)
cd apps/backend && pytest --maxfail=1     # Fast-fail style run (inferred)
```

## Test File Organization

**Location:**
- Primary automated tests are under `apps/backend/tests/`.
- Additional script-like API test at `apps/backend/test_api.py`.

**Naming:**
- Automated test files follow `test_*.py` naming (`test_health.py`).

**Structure:**
```text
apps/backend/tests/test_*.py
apps/backend/test_api.py  (manual/integration-style script)
```

## Test Structure

**Suite Organization:**
```python
from fastapi.testclient import TestClient
from app.main import app


def test_health_check() -> None:
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

**Patterns:**
- Setup pattern: instantiate `TestClient(app)` inside each test function.
- Teardown pattern: implicit cleanup via test function scope; no fixtures detected.
- Assertion pattern: direct status-code and JSON equality assertions.

## Mocking

**Framework:**
- Not detected in current repository tests.

**Patterns:**
```python
# No mocking examples found in current tests.
```

**What to Mock:**
- External model/API calls (`GroqProvider`) should be mocked for deterministic backend tests (inferred from `apps/backend/app/services/model_gateway.py`).

**What NOT to Mock:**
- Pure schema validation and lightweight route wiring can stay unmocked for confidence in request/response contracts (inferred).

## Fixtures and Factories

**Test Data:**
```python
# Current tests inline data directly; no shared factories/fixtures detected.
```

**Location:**
- No fixture module (`conftest.py`) detected.

## Coverage

**Requirements:**
- None enforced; no coverage config or CI gating detected.

**View Coverage:**
```bash
cd apps/backend && pytest --cov=app --cov-report=term-missing  # inferred; requires pytest-cov (not pinned)
```

## Test Types

**Unit Tests:**
- Limited to a basic API health check in `apps/backend/tests/test_health.py`.

**Integration Tests:**
- `apps/backend/test_api.py` performs live HTTP requests against a running server and exercises tenant/agent/chat flows.

**E2E Tests:**
- Not used in current repository.

## Common Patterns

**Async Testing:**
```python
# Async app endpoints are currently exercised through synchronous TestClient.
# No direct async test functions detected.
```

**Error Testing:**
```python
# No explicit negative-path tests (4xx/5xx) detected.
```

## Coverage Signals and Gaps

- Signal: Core app boot + `/health` route is verified by automated test.
- Gap: No automated tests for `/api/tenants`, `/api/chat`, `/api/tenants/{tenant_id}/knowledge`, or `/api/tenants/{tenant_id}/upload`.
- Gap: No tests for service-layer logic in `apps/backend/app/services/assistant_service.py` (conflict handling, reservation detection, conversation history).
- Gap: No tests for parsing logic in `apps/backend/app/services/document_parser.py`.
- Gap: No frontend tests for `apps/frontend/src/components/*` or `apps/frontend/src/lib/api.ts`.
- Gap: No coverage collection in default workflow and no CI test pipeline detected.

---

*Testing analysis: 2026-03-21*
