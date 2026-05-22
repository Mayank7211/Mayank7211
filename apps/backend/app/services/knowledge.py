import os
import re
from typing import Iterable, List, Protocol



def rank_context_blocks(blocks: Iterable[str], query: str, limit: int) -> List[str]:
    knowledge = [item for item in blocks if item and item.strip()]
    if not knowledge or limit <= 0:
        return []

    tokens = set(re.findall(r"[a-zA-Z0-9]+", query.lower()))
    scored = []

    for block in knowledge:
        block_tokens = set(re.findall(r"[a-zA-Z0-9]+", block.lower()))
        overlap = len(tokens.intersection(block_tokens))
        scored.append((overlap, block))

    scored.sort(key=lambda item: item[0], reverse=True)
    top = [item[1] for item in scored[:limit]]
    return top


class VectorStoreAdapter(Protocol):
    """Protocol for vector store adapters.

    Implementations must provide:
      - index_documents(tenant_id, blocks)
      - query(tenant_id, query, top_k) -> List[str]
    """


class InMemoryVectorAdapter:
    """A minimal in-memory adapter that stores raw text blocks per tenant and
    uses token-overlap ranking (via rank_context_blocks) for queries.
    """

    def __init__(self) -> None:
        self.store: dict[str, List[str]] = {}

    def index_documents(self, tenant_id: str, blocks: Iterable[str]) -> None:
        existing = self.store.get(tenant_id, [])
        for b in blocks:
            if b and b.strip():
                existing.append(b.strip())
        self.store[tenant_id] = existing

    def query(self, tenant_id: str, query: str, top_k: int) -> List[str]:
        blocks = self.store.get(tenant_id, [])
        return rank_context_blocks(blocks, query, top_k)


# module-level default adapter (can be swapped in runtime or by config)
default_vector_adapter = InMemoryVectorAdapter()


class PgVectorAdapter:
    """A simple Postgres-backed adapter that fetches raw text for a tenant
    using an async DB session factory and performs client-side ranking.

    This is a pragmatic step toward a true pgvector integration: it allows
    retrieving tenant knowledge from Postgres efficiently and defers
    vector-based similarity to a later, opt-in implementation.
    """

    def __init__(self, db_session_factory, *, openai_api_key: str | None = None, embedding_model: str | None = None) -> None:
        # db_session_factory should be a callable that returns an async session
        self.db_session_factory = db_session_factory
        # embedding settings: if provided, adapter will compute query embeddings
        self.openai_api_key = openai_api_key or os.getenv("AI_AGENT_OPENAI_API_KEY")
        self.embedding_model = embedding_model or os.getenv("AI_AGENT_EMBEDDING_MODEL", "text-embedding-3-small")

    def index_documents(self, tenant_id: str, blocks: Iterable[str]) -> None:
        # Provide an async-compatible index_documents by returning a coroutine when called
        async def _index():
            if not self.db_session_factory:
                return

            sess_candidate = self.db_session_factory()
            if hasattr(sess_candidate, "__await__"):
                sess_candidate = await sess_candidate

            async with sess_candidate as session:
                for block in blocks:
                    if not block or not block.strip():
                        continue
                    try:
                        vec = self._get_query_embedding(block)
                    except Exception:
                        # If embedding computation fails, skip this block
                        continue

                    # Find the most recent row for this tenant/raw_text without embedding
                    sel = __import__("sqlalchemy").sql.text(
                        "SELECT id FROM knowledge_sources WHERE tenant_id = :tid AND raw_text = :raw AND (embedding IS NULL OR array_length(embedding,1) = 0) ORDER BY created_at DESC LIMIT 1"
                    )
                    res = await session.execute(sel, {"tid": tenant_id, "raw": block})
                    row = res.fetchall()
                    if not row:
                        # No matching row to update
                        continue
                    row_id = row[0][0]
                    upd = __import__("sqlalchemy").sql.text(
                        "UPDATE knowledge_sources SET embedding = :vec WHERE id = :id"
                    )
                    await session.execute(upd, {"vec": vec, "id": row_id})
                await session.commit()

        return _index()

    async def query(self, tenant_id: str, query: str, top_k: int) -> List[str]:
        """Fetch raw_text entries for `tenant_id` from the DB and rank them.

        This implementation performs a SELECT of recent `raw_text` values and
        applies the existing `rank_context_blocks` function for now.
        """
        if not self.db_session_factory:
            return []

        # db_session_factory may be async (coroutine) or sync; resolve it
        sess_candidate = self.db_session_factory()
        if hasattr(sess_candidate, "__await__"):
            sess_candidate = await sess_candidate

        # Try to compute an embedding for the query. If we can, run a vector similarity
        # search in Postgres (requires pgvector installed and `embedding` column populated).
        query_vector = None
        try:
            query_vector = self._get_query_embedding(query)
        except Exception:
            query_vector = None

        async with sess_candidate as session:
            if query_vector is not None:
                # Use pgvector similarity operator (<->) to order by distance
                sql = __import__("sqlalchemy").sql.text(
                    "SELECT raw_text FROM knowledge_sources WHERE tenant_id = :tid AND embedding IS NOT NULL ORDER BY embedding <-> :vec LIMIT :k"
                )
                result = await session.execute(sql, {"tid": tenant_id, "vec": query_vector, "k": top_k})
                rows = [r[0] for r in result.fetchall() if r and r[0]]
                return rows

            # Fallback: fetch raw_text and apply client-side ranking
            result = await session.execute(
                __import__("sqlalchemy").sql.text(
                    "SELECT raw_text FROM knowledge_sources WHERE tenant_id = :tid ORDER BY created_at DESC LIMIT 400"
                ),
                {"tid": tenant_id},
            )
            rows = [r[0] for r in result.fetchall() if r and r[0]]

        return rank_context_blocks(rows, query, top_k)

    def _get_query_embedding(self, text: str) -> List[float] | None:
        """Compute an embedding for `text` using OpenAI embeddings when API key is available.

        Returns a list[float] or raises an exception if embedding cannot be computed.
        """
        key = self.openai_api_key
        if not key:
            raise RuntimeError("No OpenAI API key configured for PgVectorAdapter")

        # Lazy-import `requests` to avoid requiring it in test environments.
        try:
            import requests
        except Exception as e:
            raise RuntimeError("The `requests` package is required to compute embeddings") from e

        url = "https://api.openai.com/v1/embeddings"
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        payload = {"input": text, "model": self.embedding_model}
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data["data"][0]["embedding"]
