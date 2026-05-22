"""Async batch embedding worker.

This script computes embeddings for rows in `knowledge_sources` that lack an
`embedding` value and writes them back to Postgres (pgvector column).

It uses `httpx` for async HTTP requests and SQLAlchemy async engine for DB IO.

Usage:
  AI_AGENT_DATABASE_URL="postgresql+asyncpg://user:pass@host:5432/db" \
  AI_AGENT_OPENAI_API_KEY="sk-..." \
  python apps/backend/scripts/async_compute_embeddings.py

Notes:
  - Ensure `pgvector` extension exists and `infra/sql/002_add_embeddings.sql` was applied.
  - Install required packages: `pip install httpx sqlalchemy[asyncio] asyncpg`
"""
import os
import asyncio
import logging
from typing import List

import httpx
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("async_compute_embeddings")

DB_URL = os.getenv("AI_AGENT_DATABASE_URL")
OPENAI_KEY = os.getenv("AI_AGENT_OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("AI_AGENT_EMBEDDING_MODEL", "text-embedding-3-small")


async def fetch_embedding(client: httpx.AsyncClient, text: str) -> List[float]:
    url = "https://api.openai.com/v1/embeddings"
    headers = {"Authorization": f"Bearer {OPENAI_KEY}"}
    payload = {"input": text, "model": EMBEDDING_MODEL}
    resp = await client.post(url, json=payload, timeout=30.0)
    resp.raise_for_status()
    data = resp.json()
    return data["data"][0]["embedding"]


async def main(batch_size: int = 50):
    if not DB_URL:
        logger.error("AI_AGENT_DATABASE_URL not set. Aborting.")
        return
    if not OPENAI_KEY:
        logger.error("AI_AGENT_OPENAI_API_KEY not set. Aborting.")
        return

    engine = create_async_engine(DB_URL, echo=False)

    async with httpx.AsyncClient() as client:
        async with engine.begin() as conn:
            while True:
                res = await conn.execute(
                    text(
                        "SELECT id, raw_text FROM knowledge_sources WHERE embedding IS NULL OR array_length(embedding,1)=0 ORDER BY created_at DESC LIMIT :lim"
                    ),
                    {"lim": batch_size},
                )
                rows = res.fetchall()
                if not rows:
                    logger.info("No more rows to process. Exiting.")
                    break

                tasks = []
                for r in rows:
                    row_id, raw_text = r[0], r[1]
                    if not raw_text or not raw_text.strip():
                        continue
                    tasks.append((row_id, raw_text))

                # Execute embeddings concurrently
                coros = [fetch_embedding(client, rt) for (_id, rt) in tasks]
                results = await asyncio.gather(*coros, return_exceptions=True)

                # Update rows one by one (could batch using COPY in production)
                for (row_id, _), emb in zip(tasks, results):
                    if isinstance(emb, Exception):
                        logger.exception("Embedding failed for id %s: %s", row_id, str(emb))
                        continue
                    await conn.execute(
                        text("UPDATE knowledge_sources SET embedding = :vec WHERE id = :id"),
                        {"vec": emb, "id": row_id},
                    )
                await conn.commit()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
