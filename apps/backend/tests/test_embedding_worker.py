import asyncio

from apps.backend.scripts import run_embedding_worker as runner


def test_run_loop_calls_worker(monkeypatch):
    calls = []

    async def fake_worker():
        calls.append("called")
        # yield back to the loop briefly
        await asyncio.sleep(0)

    monkeypatch.setattr(runner, "worker_main", fake_worker)

    loop = asyncio.get_event_loop()
    task = loop.create_task(runner.run_loop())

    # allow the loop to run the worker once
    loop.run_until_complete(asyncio.sleep(0.05))

    # cancel the long-running loop and finish
    task.cancel()
    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        pass

    assert len(calls) >= 1


def test_run_loop_handles_exceptions(monkeypatch):
    calls = []
    state = {"count": 0}

    async def flaky_worker():
        state["count"] += 1
        if state["count"] == 1:
            raise RuntimeError("boom")
        calls.append("ok")
        await asyncio.sleep(0)

    monkeypatch.setattr(runner, "worker_main", flaky_worker)

    loop = asyncio.get_event_loop()
    task = loop.create_task(runner.run_loop())
    loop.run_until_complete(asyncio.sleep(0.05))
    task.cancel()
    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        pass

    # ensure we attempted at least one run and later succeeded
    assert state["count"] >= 1
    assert len(calls) >= 1
