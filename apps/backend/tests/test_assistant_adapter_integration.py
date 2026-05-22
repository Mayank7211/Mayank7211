from app.services import assistant_service as assistant_mod


def test_assistant_uses_adapter(monkeypatch):
    # stub adapter to return known results
    def _fake_query(tenant_id, query, top_k):
        return ["adapter result 1", "adapter result 2"]

    monkeypatch.setattr(assistant_mod.default_vector_adapter, "query", _fake_query)

    # call _load_context directly
    res = assistant_mod.assistant_service._load_context("t-1", "any", None)
    # _load_context may be synchronous or async; normalize
    if hasattr(res, "__await__"):
        import asyncio

        res = asyncio.get_event_loop().run_until_complete(res)

    assert isinstance(res, list)
    assert "adapter result 1" in res
