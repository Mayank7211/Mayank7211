import hashlib
import hmac
from typing import Any, AsyncIterator

import pytest
from fastapi.testclient import TestClient

from app.db.session import get_db_session
from app.main import app
from app.models.entities import TenantEntity


class DummySession:
    def __init__(self) -> None:
        self.tenants: dict[str, TenantEntity] = {}

    async def get(self, model: type[TenantEntity], tenant_id: str) -> TenantEntity | None:
        if model is not TenantEntity:
            return None
        return self.tenants.get(tenant_id)


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
