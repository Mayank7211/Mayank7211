from app.auth.dependencies import _build_expected_owner_token
from app.models.schemas import ChatResponse
from app.services.assistant_service import assistant_service


def test_chat_and_upload_rate_limited(client, tenant_id, dummy_session, monkeypatch) -> None:
    dummy_session.tenants[tenant_id] = object()

    async def fake_chat(payload, db):  # noqa: ANN001
        return ChatResponse(
            answer="ok",
            provider="test",
            model="fake",
            confidence=0.9,
            handoff_recommended=False,
            reservation_detected=False,
        )

    async def fake_parse_document(filename, file_content):  # noqa: ANN001
        return ["chunk"]

    async def fake_ingest(tenant_id_arg, payload, db):  # noqa: ANN001
        return {
            "tenant_id": tenant_id_arg,
            "indexed_blocks": len(payload.text_blocks),
            "source_url": None,
        }

    monkeypatch.setattr(assistant_service, "chat", fake_chat)
    monkeypatch.setattr("app.api.tenants.parse_document", fake_parse_document)
    monkeypatch.setattr(assistant_service, "ingest_knowledge", fake_ingest)

    for _ in range(20):
        response = client.post(
            "/api/chat",
            json={"tenant_id": tenant_id, "message": "hello"},
        )
        assert response.status_code == 200

    throttled_chat = client.post(
        "/api/chat",
        json={"tenant_id": tenant_id, "message": "hello again"},
    )
    assert throttled_chat.status_code == 429
    chat_payload = throttled_chat.json()
    assert chat_payload["detail"] == "Rate limit exceeded"
    assert isinstance(chat_payload["retry_after_seconds"], int)

    headers = {"X-Owner-Token": _build_expected_owner_token(tenant_id)}
    for _ in range(5):
        response = client.post(
            f"/api/tenants/{tenant_id}/upload",
            files={"file": ("doc.txt", b"sample", "text/plain")},
            headers=headers,
        )
        assert response.status_code == 200

    throttled_upload = client.post(
        f"/api/tenants/{tenant_id}/upload",
        files={"file": ("doc.txt", b"sample", "text/plain")},
        headers=headers,
    )
    assert throttled_upload.status_code == 429
    upload_payload = throttled_upload.json()
    assert upload_payload["detail"] == "Rate limit exceeded"
    assert isinstance(upload_payload["retry_after_seconds"], int)
