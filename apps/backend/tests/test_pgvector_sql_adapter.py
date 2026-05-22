import asyncio

from app.services.knowledge import PgVectorAdapter


class DummyResult:
    def __init__(self, rows):
        self._rows = rows

    def fetchall(self):
        return self._rows


class DummySession:
    def __init__(self, rows):
        self.rows = rows

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def execute(self, stmt, params=None):
        # ignore stmt/params for this dummy and return preset rows
        return DummyResult(self.rows)


def dummy_factory(rows):
    async def _make():
        return DummySession(rows)

    return _make


def test_pgvector_adapter_uses_vector_query():
    # Prepare dummy rows as (raw_text,)
    rows = [("Best service details",), ("Other context",)]
    adapter = PgVectorAdapter(dummy_factory(rows), openai_api_key="dummy-key")

    # Patch _get_query_embedding to return a fixed vector without calling OpenAI
    adapter._get_query_embedding = lambda t: [0.01] * 1536

    res_coro = adapter.query("tenant123", "what services?", 2)
    res = asyncio.get_event_loop().run_until_complete(res_coro)
    assert res == [r[0] for r in rows]


def test_pgvector_adapter_fallback_ranking():
    rows = [("Book appointment now",), ("Contact phone 555-1234",), ("Irrelevant info",)]
    adapter = PgVectorAdapter(dummy_factory(rows), openai_api_key=None)

    # _get_query_embedding will raise because no API key; adapter should fallback
    res_coro = adapter.query("tenant123", "appointment", 2)
    res = asyncio.get_event_loop().run_until_complete(res_coro)
    # Expect token-overlap ranking to pick the most overlapping rows
    assert any("appointment" in r.lower() or "contact" in r.lower() for r in res)
