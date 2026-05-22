from app.core.config import settings
from app.models.schemas import TenantCreateRequest
from app.services.assistant_service import AssistantService


class _NoopGateway:
    async def complete(self, request):  # noqa: ANN001
        raise RuntimeError("Not used in this test")


class _FakeResult:
    def __init__(self, tenant_id: str) -> None:
        self._tenant_id = tenant_id

    def scalar_one_or_none(self):
        return None


class _FakeSession:
    def __init__(self) -> None:
        self._tenant_id = "tenant-abc-123"

    async def execute(self, query):  # noqa: ANN001
        return _FakeResult(self._tenant_id)

    def add(self, obj):  # noqa: ANN001
        if obj.__class__.__name__ == "TenantEntity":
            obj.id = self._tenant_id

    async def flush(self) -> None:
        return None

    async def commit(self) -> None:
        return None


def test_widget_snippet_is_parameterized() -> None:
    payload = TenantCreateRequest(
        business_name="Maya Skin Clinic",
        domain="maya.example",
        category="clinic",
        services=["Consultation"],
        description="Skin and wellness consultations",
    )
    service = AssistantService(gateway=_NoopGateway(), max_context_chunks=4)
    session = _FakeSession()

    response = __import__("asyncio").run(service.create_tenant(payload, session))

    assert response.tenant_id == "tenant-abc-123"
    assert f"src='{settings.widget_script_src}'" in response.widget_embed_script
    assert "data-tenant-id='tenant-abc-123'" in response.widget_embed_script
    assert f"data-theme='{settings.widget_default_theme}'" in response.widget_embed_script
    assert f"data-position='{settings.widget_default_position}'" in response.widget_embed_script
    assert f"data-primary-color='{settings.widget_default_primary_color}'" in response.widget_embed_script


def test_widget_snippet_respects_configured_defaults(monkeypatch) -> None:
    monkeypatch.setattr(settings, "widget_default_theme", "dark")
    monkeypatch.setattr(settings, "widget_default_position", "bottom-left")
    monkeypatch.setattr(settings, "widget_default_primary_color", "#123456")

    payload = TenantCreateRequest(
        business_name="Maya Skin Clinic",
        domain="maya.example",
        category="clinic",
        services=["Consultation"],
        description="Skin and wellness consultations",
    )
    service = AssistantService(gateway=_NoopGateway(), max_context_chunks=4)
    session = _FakeSession()

    response = __import__("asyncio").run(service.create_tenant(payload, session))

    assert "data-theme='dark'" in response.widget_embed_script
    assert "data-position='bottom-left'" in response.widget_embed_script
    assert "data-primary-color='#123456'" in response.widget_embed_script
