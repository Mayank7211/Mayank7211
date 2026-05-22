**Retrieval Evaluation**

This document describes how to run the local retrieval evaluation harness and
use the TF-IDF reranker prototype.

1) Quick local smoke run

 - Prepare the in-memory adapter with some sample documents (the harness can
   also read fixtures). Example:

```bash
python -m pip install -r apps/backend/requirements.txt
python tools/retrieval_eval.py --fixtures apps/backend/tests/fixtures/sample_qa.json --k 3
```

2) What it does

 - Runs retrieval via the `default_vector_adapter` (in-memory) and optionally
   via `PgVectorAdapter` when a DB is configured.
 - Computes precision@k and recall@k before and after reranking using the
   TF-IDF reranker prototype in `apps/backend/app/services/reranker.py`.

3) Extending

 - Replace the reranker with a learned reranker (e.g., cross-encoder) by
   implementing the same `rerank(query,candidates)` signature.
 - Provide real ground-truth fixtures under `apps/backend/tests/fixtures/`.
# Retrieval Evaluation

This document describes the lightweight retrieval evaluation harness included
in the repository.

Run a smoke evaluation (uses the in-memory adapter, no external services):

```bash
python tools/retrieval_eval.py --smoke
```

Optional: apply the simple TF-IDF-like reranker during evaluation:

```bash
python tools/retrieval_eval.py --smoke --rerank
```

Output: `retrieval_eval_results.csv` with precision@k and recall@k metrics.

Notes:
- The harness is intentionally small and uses the `default_vector_adapter`.
- If you have a Postgres DB configured and populated, the harness can be extended
  to evaluate `PgVectorAdapter` outputs — this is left as a follow-up task.
