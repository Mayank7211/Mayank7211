import asyncio

from app.services import assistant_service as assistant_mod


class FakeResult:
    def __init__(self, items):
        self._items = items

    def scalars(self):
        return self

    def all(self):
        return self._items


class DummyDB:
    async def execute(self, query):
        # Return knowledge blocks; one includes the token 'booking' to match query
        return FakeResult([
            "We offer haircuts and grooming.",
            "Booking available on Monday and Tuesday.",
            "Contact us for more info.",
        ])


def test__load_context_returns_relevant_chunks():
    db = DummyDB()
    result = asyncio.run(assistant_mod.assistant_service._load_context("tenant-x", "booking", db))
    assert isinstance(result, list)
    assert len(result) > 0
    assert any("booking" in item.lower() for item in result)
