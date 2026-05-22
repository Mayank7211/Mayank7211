PGVector (Postgres + pgvector) Setup
===================================

This document describes how to enable Postgres + pgvector support for the project.

1. Provision Postgres with pgvector
   - Install Postgres (13+ recommended).
   - Install `pgvector` extension following project docs: https://github.com/pgvector/pgvector
   - Create database and enable extension:

     ```sql
     CREATE EXTENSION IF NOT EXISTS vector;
     ```

2. Update `AI_AGENT` configuration
   - Set `AI_AGENT_DATABASE_URL` to a Postgres DSN, e.g.: `postgresql+asyncpg://user:pass@host:5432/dbname`
   - Enable the adapter by setting `AI_AGENT_ENABLE_PGVECTOR=true` when you want to use the Postgres-backed adapter.

3. Schema changes
   - Add a `vector` column to `knowledge_sources` to store embeddings (pgvector type). Example SQL migration snippet:

     ```sql
     ALTER TABLE knowledge_sources
     ADD COLUMN embedding vector(1536);
     CREATE INDEX IF NOT EXISTS idx_knowledge_embedding ON knowledge_sources USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);
     ```

   - Populate `embedding` for existing rows by running an embedding step (see next).

4. Embedding pipeline
   - Choose an embedding provider (OpenAI, local model, etc.).
   - Add a small worker or migration script that computes embeddings for `raw_text` and writes them to `embedding`.

5. Querying
   - Replace the interim client-side ranking in `PgVectorAdapter.query` with a SQL similarity search, e.g.:

     ```sql
     SELECT raw_text FROM knowledge_sources
     WHERE tenant_id = :tid AND embedding IS NOT NULL
     ORDER BY embedding <-> :vector
     LIMIT :k
     ```

6. Testing and CI
   - Add an integration test matrix for Postgres+pgvector in CI or run locally using a Docker Compose service.

Notes
-----
- The current `PgVectorAdapter` is a scaffold that fetches raw_text and ranks client-side; full vector similarity will require the embedding pipeline and schema updates.
- Consider using a managed vector DB (Pinecone, Weaviate, or Milvus) if you prefer not to host pgvector.
