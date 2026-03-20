import hashlib
import hmac
from typing import Any

import pytest


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
