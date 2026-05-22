from app.models.entities import ReservationEntity, TenantEntity
from app.services import assistant_service as assistant_mod


def test_reservation_persisted_on_detection(client, dummy_session, tenant_id, monkeypatch):
    # register tenant
    tenant = TenantEntity(id=tenant_id, business_name="T", domain="example.com", category="spa", description="d")
    dummy_session.tenants[tenant_id] = tenant

    # stub model to return confirmation text
    async def _complete(req):
        return type("R", (), {"answer": "Sure, I can help you book an appointment.", "provider": "groq", "model": "m", "confidence": 0.9})

    monkeypatch.setattr(assistant_mod.assistant_service.gateway, "complete", _complete)

    async def _async_load_context(*a, **k):
        return []

    async def _async_load_history(*a, **k):
        return []

    monkeypatch.setattr(assistant_mod.assistant_service, "_load_context", _async_load_context)
    monkeypatch.setattr(assistant_mod.assistant_service, "_load_conversation_history", _async_load_history)

    # send a booking-like user message (contains 'book' and 'appointment')
    r = client.post("/api/chat", json={"tenant_id": tenant_id, "message": "I want to book an appointment", "session_id": "s-r"})
    assert r.status_code == 200

    # check that a ReservationEntity was added to the dummy session
    added = [obj for obj in dummy_session._added if isinstance(obj, ReservationEntity)]
    assert len(added) == 1
    res = added[0]
    assert res.tenant_id == tenant_id
    assert res.session_id == "s-r"
    assert res.status == "pending"
