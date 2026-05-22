---
phase: 02-tenant-aware-chat-baseline
plan: 02
status: in-progress
updated_at: "2026-05-22T23:58:00+05:30"
artifacts:
  - apps/backend/app/services/knowledge.py
  - apps/backend/tests/test_knowledge_retrieval.py
  - apps/backend/tests/test_assistant_adapter_integration.py
  - apps/backend/tests/test_pgvector_adapter.py

summary: |
  Plan 02 (Retrieval tuning + pgvector integration) progress:
  - Added a pluggable VectorStoreAdapter and an `InMemoryVectorAdapter`.
  - Implemented a `PgVectorAdapter` scaffold that can fetch tenant knowledge
    via an async DB session and currently applies token-overlap ranking as
    a pragmatic interim step.
  - Wired the `AssistantService` to prefer the pluggable adapter and await
    async adapter queries.
  - Added unit tests validating the in-memory adapter and the PgVector
    adapter scaffold against a dummy async session.

next_steps:
  - Implement full vector storage and similarity search (store vectors, add
    embedding pipeline, and use pgvector similarity queries) OR integrate
    a hosted vector DB.
  - Add migration scripts and README instructions for Postgres+pgvector.
  - Add integration tests (Postgres + pgvector) as part of CI.
