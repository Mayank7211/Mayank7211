import os
import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text


async def _check_extension(db_url: str) -> bool:
    engine = create_async_engine(db_url, echo=False)
    try:
        async with engine.begin() as conn:
            res = await conn.execute(text("SELECT extname FROM pg_extension WHERE extname = 'vector'"))
            rows = res.fetchall()
            return len(rows) > 0
    finally:
        await engine.dispose()


def test_pgvector_extension_available():
    db_url = os.getenv("AI_AGENT_DATABASE_URL")
    if not db_url:
        import pytest

        pytest.skip("No AI_AGENT_DATABASE_URL configured for integration test")

    ok = asyncio.get_event_loop().run_until_complete(_check_extension(db_url))
    assert ok, "pgvector extension not available in DB"
