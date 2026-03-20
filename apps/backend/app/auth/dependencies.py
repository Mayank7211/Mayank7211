import hashlib
import hmac

from fastapi import Header, HTTPException, status

from app.core.config import settings


def _build_expected_owner_token(tenant_id: str) -> str:
    return hmac.new(
        settings.owner_access_secret.encode("utf-8"),
        tenant_id.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


async def require_owner_tenant_access(
    tenant_id: str,
    x_owner_token: str | None = Header(default=None, alias="X-Owner-Token"),
) -> None:
    if not x_owner_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing owner authentication token. Provide X-Owner-Token header.",
        )

    expected_token = _build_expected_owner_token(tenant_id)
    if not hmac.compare_digest(x_owner_token, expected_token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cross-tenant access denied for requested tenant_id.",
        )
