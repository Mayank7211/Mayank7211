"""Run quick smoke checks for embedding worker and non-blocking ingest.

This script avoids pytest and heavy DB deps and runs the new unit-style
checks in-process.
"""
import asyncio
import sys
import os

# Ensure the backend package is importable (mirrors tests' conftest behavior)
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apps", "backend"))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def check_embedding_worker():
    # prevent heavy imports from async_compute_embeddings by stubbing the module
    import types
    fake_mod = types.SimpleNamespace()

    async def fake_worker_main():
        await asyncio.sleep(0)

    fake_mod.main = fake_worker_main
    sys.modules["apps.backend.scripts.async_compute_embeddings"] = fake_mod

    from apps.backend.scripts import run_embedding_worker as runner

    calls = []

    async def fake_worker():
        calls.append("called")
        await asyncio.sleep(0)

    runner.worker_main = fake_worker

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    task = loop.create_task(runner.run_loop())
    loop.run_until_complete(asyncio.sleep(0.05))
    task.cancel()
    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        pass

    return len(calls) >= 1


def check_non_blocking_ingest():
    # stub lightweight parts of SQLAlchemy to avoid heavy install for smoke run
    import types
    sqlalchemy_mod = types.ModuleType("sqlalchemy")
    class QueryStub:
        def __init__(self, args=None):
            self.args = args

        def where(self, *a, **k):
            return self

        def order_by(self, *a, **k):
            return self

        def limit(self, *a, **k):
            return self

    def _select(*args, **kwargs):
        return QueryStub(args)

    sqlalchemy_mod.select = _select
    sys.modules["sqlalchemy"] = sqlalchemy_mod

    ext_mod = types.ModuleType("sqlalchemy.ext")
    asyncio_mod = types.ModuleType("sqlalchemy.ext.asyncio")
    asyncio_mod.AsyncSession = object
    sys.modules["sqlalchemy.ext"] = ext_mod
    sys.modules["sqlalchemy.ext.asyncio"] = asyncio_mod

    # stub app.core.config.settings to avoid pydantic dependency
    import types
    core_cfg = types.ModuleType("app.core.config")
    core_cfg.settings = types.SimpleNamespace(
        widget_script_src="/widget.js",
        widget_default_theme="light",
        widget_default_position="bottom-right",
        widget_default_primary_color="#0f766e",
        max_context_chunks=4,
        groq_api_key="",
        retrieval_k=4,
    )
    sys.modules["app.core.config"] = core_cfg

    # stub model gateway to avoid heavy provider logic during import
    mgw = types.ModuleType("app.services.model_gateway")
    class DummyGateway:
        def __init__(self, *args, **kwargs):
            pass

        async def complete(self, request):
            class R:
                answer = "hi"
                provider = "none"
                model = "none"
                confidence = 1.0
                fallback_reason = None

            return R()

    mgw.ModelGateway = DummyGateway
    mgw.GroqProvider = lambda *args, **kwargs: None
    mgw.BackupOpenModelProvider = lambda *args, **kwargs: None
    # Provide lightweight ModelRequest/ModelResult placeholders used by imports
    class ModelRequest:
        def __init__(self, *args, **kwargs):
            pass

    class ModelResult:
        def __init__(self, *args, **kwargs):
            self.answer = ""
            self.provider = ""
            self.model = ""
            self.confidence = 1.0
            self.fallback_reason = None

    mgw.ModelRequest = ModelRequest
    mgw.ModelResult = ModelResult
    sys.modules["app.services.model_gateway"] = mgw

    # stub app.models.entities to avoid SQLAlchemy model imports
    ents = types.ModuleType("app.models.entities")
    class _DummyEntity:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    # TenantEntity is used in select(TenantEntity.id) in assistant_service; provide
    # a lightweight namespace with `id` and `domain` placeholders so the stubbed
    # sqlalchemy.select() call can accept them.
    class TenantStub:
        id = "id"
        domain = "domain"

        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    ents.TenantEntity = TenantStub
    ents.KnowledgeSourceEntity = _DummyEntity
    ents.ConversationEntity = _DummyEntity
    ents.ReservationEntity = _DummyEntity
    sys.modules["app.models.entities"] = ents

    from app.services import assistant_service as assistant_mod
    from app.models.schemas import TenantCreateRequest, KnowledgeIngestRequest
    from app.models.entities import TenantEntity

    # stub adapter to return a coroutine
    def fake_index_documents(tenant_id, blocks):
        async def _coro():
            await asyncio.sleep(0)

        return _coro()

    assistant_mod.default_vector_adapter.index_documents = fake_index_documents

    created_tasks = []

    def fake_create_task(coro):
        created_tasks.append(coro)

        class DummyTask:
            pass

        return DummyTask()

    asyncio.create_task = fake_create_task

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
    ok1 = bool(created_tasks)

    # test ingest_knowledge
    created_tasks.clear()

    class FakeSession2:
        def __init__(self):
            self._tenant = TenantEntity(id="t-1", business_name="B", domain="d", category="c", description="x")

        async def get(self, model, tenant_id):
            return self._tenant

        def add(self, obj):
            return None

        async def commit(self):
            return None

    payload2 = KnowledgeIngestRequest(text_blocks=["a","b"], source_url=None)
    res2 = loop.run_until_complete(assistant_mod.assistant_service.ingest_knowledge("t-1", payload2, FakeSession2()))
    ok2 = bool(created_tasks) and res2.get("indexed_blocks") == 2

    return ok1 and ok2


def main():
    ok_e = check_embedding_worker()
    ok_i = check_non_blocking_ingest()

    all_ok = ok_e and ok_i
    print(f"Embedding worker smoke: {'PASS' if ok_e else 'FAIL'}")
    print(f"Non-blocking ingest smoke: {'PASS' if ok_i else 'FAIL'}")

    if not all_ok:
        sys.exit(2)


if __name__ == '__main__':
    main()
