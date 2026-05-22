import asyncio

from app.models.entities import TenantEntity
from app.models.schemas import TenantCreateRequest, KnowledgeIngestRequest
from app.services import assistant_service as assistant_mod


def test_create_tenant_schedules_index(monkeypatch):
    scheduled = []

    def fake_index_documents(tenant_id, blocks):
        async def _coro():
            # would compute embeddings in real adapter
            await asyncio.sleep(0)

        return _coro()

    monkeypatch.setattr(assistant_mod.default_vector_adapter, "index_documents", fake_index_documents)

    created_tasks = []

    def fake_create_task(coro):
        created_tasks.append(coro)

        class DummyTask:
            pass

        return DummyTask()

    monkeypatch.setattr(asyncio, "create_task", fake_create_task)


    class FakeSession:
        async def execute(self, *args, **kwargs):
            class Res:
                def scalar_one_or_none(self):
                    return None

            return Res()

        async def flush(self):
            return None

        def add(self, obj):
            return None

        async def commit(self):
            return None


    payload = TenantCreateRequest(
        business_name="My Biz",
        domain="example.com",
        category="food",
        services=["s1"],
        description="descr",
        faqs=[],
    )

    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(assistant_mod.assistant_service.create_tenant(payload, FakeSession()))

    assert created_tasks, "index_documents coroutine should be scheduled via create_task"
    assert hasattr(res, "widget_embed_script")


def test_ingest_knowledge_schedules_index(monkeypatch):
    created_tasks = []

    def fake_index_documents(tenant_id, blocks):
        async def _coro():
            await asyncio.sleep(0)

        return _coro()

    monkeypatch.setattr(assistant_mod.default_vector_adapter, "index_documents", fake_index_documents)

    def fake_create_task(coro):
        created_tasks.append(coro)

        class DummyTask:
            pass

        return DummyTask()

    monkeypatch.setattr(asyncio, "create_task", fake_create_task)

    class FakeSession:
        def __init__(self):
            self._tenant = TenantEntity(id="t-1", business_name="B", domain="d", category="c", description="x")

        async def get(self, model, tenant_id):
            return self._tenant

        def add(self, obj):
            return None

        async def commit(self):
            return None

    payload = KnowledgeIngestRequest(text_blocks=["block one", "block two"], source_url=None)

    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(assistant_mod.assistant_service.ingest_knowledge("t-1", payload, FakeSession()))

    assert created_tasks, "index_documents coroutine should be scheduled via create_task"
    assert res["indexed_blocks"] == 2
