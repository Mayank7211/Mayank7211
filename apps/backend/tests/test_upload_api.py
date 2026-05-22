from app.auth.dependencies import _build_expected_owner_token
from app.services.assistant_service import assistant_service


def test_upload_supported_files(client, tenant_id, dummy_session, monkeypatch) -> None:
    dummy_session.tenants[tenant_id] = object()

    async def fake_parse_document(filename, file_content):  # noqa: ANN001
        return ["chunk one", "chunk two"]

    async def fake_ingest(tenant_id_arg, payload, db):  # noqa: ANN001
        return {
            "tenant_id": tenant_id_arg,
            "indexed_blocks": len(payload.text_blocks),
            "source_url": None,
        }

    monkeypatch.setattr("app.api.tenants.parse_document", fake_parse_document)
    monkeypatch.setattr(assistant_service, "ingest_knowledge", fake_ingest)

    headers = {"X-Owner-Token": _build_expected_owner_token(tenant_id)}
    response = client.post(
        f"/api/tenants/{tenant_id}/upload",
        files={"file": ("welcome.txt", b"hello world", "text/plain")},
        headers=headers,
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["tenant_id"] == tenant_id
    assert payload["chunks_processed"] == 2


def test_upload_rejects_invalid_type_and_size(client, tenant_id) -> None:
    headers = {"X-Owner-Token": _build_expected_owner_token(tenant_id)}

    invalid_type = client.post(
        f"/api/tenants/{tenant_id}/upload",
        files={"file": ("malware.exe", b"abc", "application/octet-stream")},
        headers=headers,
    )
    assert invalid_type.status_code == 400
    assert ".pdf, .docx, .txt" in invalid_type.json()["detail"]

    oversized = client.post(
        f"/api/tenants/{tenant_id}/upload",
        files={"file": ("big.txt", b"x" * ((10 * 1024 * 1024) + 1), "text/plain")},
        headers=headers,
    )
    assert oversized.status_code == 413
    assert "10MB" in oversized.json()["detail"]
