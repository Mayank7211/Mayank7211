from app.models.schemas import TenantCreateResponse
from app.services.assistant_service import assistant_service


def test_create_tenant_required_fields(client) -> None:
    payload = {
        "business_name": "Maya Skin Clinic",
        "category": "clinic",
        "description": "Skin and wellness consultations",
        "services": ["Consultation"],
    }

    response = client.post("/api/tenants", json=payload)

    assert response.status_code == 422
    detail = response.json()["detail"]
    domain_error = next(item for item in detail if item["loc"][-1] == "domain")
    assert "Field required" in domain_error["msg"]


def test_create_tenant_rejects_empty_services(client, monkeypatch) -> None:
    async def fake_create_tenant(payload, db):  # noqa: ANN001
        return TenantCreateResponse(
            tenant_id="tenant-test-001",
            widget_embed_script=f"<script data-tenant-id='{payload.domain}'></script>",
        )

    monkeypatch.setattr(assistant_service, "create_tenant", fake_create_tenant)

    payload = {
        "business_name": "Maya Skin Clinic",
        "domain": "maya.example",
        "category": "clinic",
        "description": "Skin and wellness consultations",
        "services": ["   "],
    }

    response = client.post("/api/tenants", json=payload)

    assert response.status_code == 422
    detail = response.json()["detail"]
    services_error = next(item for item in detail if item["loc"][-1] == "services")
    assert "services entries must be non-empty strings" in services_error["msg"]
