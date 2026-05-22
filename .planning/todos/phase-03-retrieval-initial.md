---
id: 003-retrieval-initial
title: Phase 3 - Retrieval & Relevance Tuning (initial)
status: done
created: 2026-05-22
completed: 2026-05-22
notes: |
  Implemented initial tests for embedding worker and non-blocking ingestion. Added retrieval evaluation harness, simple reranker prototype, and CI smoke workflow.
---

Remaining:
- Expand retrieval evaluation to test PgVectorAdapter with a real DB (requires DB creds/migrations).
- Improve reranker to use real vector similarity + ML-based reranker.
- Add end-to-end integration tests with embeddings populated.
