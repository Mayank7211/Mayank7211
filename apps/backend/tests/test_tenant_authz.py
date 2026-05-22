import hashlib
import hmac


def test_owner_token_required(client, tenant_id) -> None:
    response = client.get(f"/api/analytics/tenants/{tenant_id}/stats")

    assert response.status_code == 401
    assert "Missing owner authentication token" in response.json()["detail"]


def test_cross_tenant_forbidden(client, tenant_id, owner_access_secret) -> None:
    wrong_tenant_id = "tenant-wrong-002"
    wrong_token = hmac.new(
        owner_access_secret.encode("utf-8"),
        wrong_tenant_id.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    response = client.get(
        f"/api/analytics/tenants/{tenant_id}/stats",
        headers={"X-Owner-Token": wrong_token},
    )

    assert response.status_code == 403
    assert "Cross-tenant access denied" in response.json()["detail"]
