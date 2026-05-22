import hashlib
import hmac
import sys
import os
from typing import Any, AsyncIterator

import pytest
from fastapi.testclient import TestClient

# Ensure tests can import the application package when PYTHONPATH isn't set by the environment
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.db.session import get_db_session
from app.main import app
from app.models.entities import TenantEntity


class DummySession:
    def __init__(self) -> None:
        self.tenants: dict[str, TenantEntity] = {}
        self._added: list[object] = []

    async def get(self, model: type[TenantEntity], tenant_id: str) -> TenantEntity | None:
        if model is not TenantEntity:
            return None
        return self.tenants.get(tenant_id)

    def add(self, obj: object) -> None:
        self._added.append(obj)

    async def commit(self) -> None:
        return None


@pytest.fixture
def dummy_session() -> DummySession:
    return DummySession()


@pytest.fixture
def client(dummy_session: DummySession) -> AsyncIterator[TestClient]:
    async def override_get_db_session() -> AsyncIterator[DummySession]:
        yield dummy_session

    app.dependency_overrides[get_db_session] = override_get_db_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def owner_access_secret() -> str:
    return "test-owner-secret"


@pytest.fixture
def tenant_id() -> str:
    return "tenant-test-001"


@pytest.fixture
def owner_token(owner_access_secret: str, tenant_id: str) -> str:
    return hmac.new(
        owner_access_secret.encode("utf-8"),
        tenant_id.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


@pytest.fixture
def upload_limits() -> dict[str, Any]:
    return {
        "allowed_extensions": [".pdf", ".docx", ".txt"],
        "max_size_bytes": 10 * 1024 * 1024,
    }


@pytest.fixture(autouse=True)
def reset_rate_limiter_state() -> None:
    from app.core.rate_limits import rate_limiter

    rate_limiter._buckets.clear()
