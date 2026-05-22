"""Compute embeddings for existing `knowledge_sources.raw_text` rows and store
them in the `embedding` pgvector column.

Usage:
  # ensure your AI_AGENT_DATABASE_URL and AI_AGENT_OPENAI_API_KEY are set
  python apps/backend/scripts/compute_embeddings.py

Notes:
  - This script uses OpenAI embeddings API if `AI_AGENT_OPENAI_API_KEY` is set.
  - It requires `requests` and `sqlalchemy[asyncio]` in the environment.
"""
import os
import json
import logging
from typing import List

import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

logger = logging.getLogger("compute_embeddings")
logging.basicConfig(level=logging.INFO)


OPENAI_API_KEY = os.getenv("AI_AGENT_OPENAI_API_KEY")
DB_URL = os.getenv("AI_AGENT_DATABASE_URL") or os.getenv("AI_AGENT_DATABASE")
EMBEDDING_MODEL = os.getenv("AI_AGENT_EMBEDDING_MODEL", "text-embedding-3-small")


def get_embedding_for_text(text: str) -> List[float]:
    if not OPENAI_API_KEY:
        raise RuntimeError("No OpenAI API key found in AI_AGENT_OPENAI_API_KEY")

    # Uses requests to call OpenAI embeddings endpoint; use your preferred client in production
    try:
        import requests
    except Exception as e:
        raise RuntimeError("The `requests` package is required. Install with `pip install requests`") from e

    url = "https://api.openai.com/v1/embeddings"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {"input": text, "model": EMBEDDING_MODEL}
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    # OpenAI returns 'data' as a list of embeddings; pick the first
    emb = data["data"][0]["embedding"]
    return emb


async def main():
    if not DB_URL:
        logger.error("No database URL found (AI_AGENT_DATABASE_URL). Aborting.")
        return

    engine = create_async_engine(DB_URL, echo=False)

    async with engine.begin() as conn:
        # Fetch rows missing embedding
        rows = await conn.execute(text("SELECT id, raw_text FROM knowledge_sources WHERE embedding IS NULL OR array_length(embedding,1) = 0 ORDER BY created_at DESC LIMIT 200"))
        rows = rows.fetchall()

        if not rows:
            logger.info("No rows found requiring embeddings.")
            return

        for r in rows:
            id_, raw_text = r[0], r[1]
            if not raw_text or not raw_text.strip():
                continue
            try:
                emb = get_embedding_for_text(raw_text)
            except Exception as e:
                logger.exception("Failed to compute embedding for id %s: %s", id_, e)
                continue

            # Use the Postgres pgvector input syntax: passing a Python list with asyncpg works with SQLAlchemy/asyncpg
            await conn.execute(
                text("UPDATE knowledge_sources SET embedding = :vec WHERE id = :id"),
                {"vec": emb, "id": id_},
            )
            logger.info("Updated embedding for id %s", id_)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
