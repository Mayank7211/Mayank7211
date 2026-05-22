import types
import pytest
from types import SimpleNamespace

from app.models.entities import TenantEntity
from app.services import assistant_service as assistant_mod


def _fake_gateway_complete(answer: str = "Hi there", provider: str = "test", model: str = "test-model", confidence: float = 0.95):
    async def _complete(request):
        return SimpleNamespace(answer=answer, provider=provider, model=model, confidence=confidence, fallback_reason=None)

    return _complete


def test_chat_unknown_tenant_returns_404(client):
    r = client.post("/api/chat", json={"tenant_id": "does-not-exist", "message": "hello"})
    assert r.status_code == 404


def test_chat_successful_response_and_rate_limit(client, dummy_session, tenant_id, monkeypatch):
    # register a tenant in dummy session
    tenant = TenantEntity(id=tenant_id, business_name="T", domain="example.com", category="food", description="d")
    dummy_session.tenants[tenant_id] = tenant

    # mock the model gateway to return a deterministic answer
    monkeypatch.setattr(assistant_mod.assistant_service.gateway, "complete", _fake_gateway_complete(answer="Hello from AI", provider="groq", model="gpt-test", confidence=0.8))

    # avoid DB access for context/history by stubbing those helpers
    async def _stub_load_context(tenant_id, query, db):
        return []

    async def _stub_load_history(tenant_id, session_id, db):
        return []

    monkeypatch.setattr(assistant_mod.assistant_service, "_load_context", _stub_load_context)
    monkeypatch.setattr(assistant_mod.assistant_service, "_load_conversation_history", _stub_load_history)

    # first request should succeed
    r = client.post("/api/chat", json={"tenant_id": tenant_id, "message": "Hello", "session_id": "s1"})
    assert r.status_code == 200
    body = r.json()
    assert body["answer"] == "Hello from AI"
    assert body["provider"] == "groq"
    assert body["model"] == "gpt-test"
    assert isinstance(body.get("confidence"), float)

    # ensure rate limiting triggers after threshold (20 requests per minute)
    for i in range(20):
        client.post("/api/chat", json={"tenant_id": tenant_id, "message": f"msg {i}"})

    r2 = client.post("/api/chat", json={"tenant_id": tenant_id, "message": "should be rate limited"})
    assert r2.status_code == 429
    assert "retry_after_seconds" in r2.json()
