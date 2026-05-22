import asyncio

from types import SimpleNamespace

from app.services.knowledge import PgVectorAdapter


class DummyAsyncSession:
    def __init__(self, rows):
        self._rows = rows

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def execute(self, query, params=None):
        class R:
            def __init__(self, rows):
                self._rows = rows

            def fetchall(self):
                return self._rows

        return R(self._rows)


def test_pgvector_adapter_fetches_and_ranks(monkeypatch):
    rows = [("Booking on Tuesday",), ("We do haircuts",), ("Open daily",)]

    async def factory():
        return DummyAsyncSession(rows)

    adapter = PgVectorAdapter(db_session_factory=factory)
    res_coro = adapter.query("t1", "booking", 2)
    res = asyncio.get_event_loop().run_until_complete(res_coro)
    assert isinstance(res, list)
    assert any("booking" in r.lower() for r in res)
