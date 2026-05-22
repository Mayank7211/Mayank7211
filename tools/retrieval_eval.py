"""Simple retrieval evaluation harness.

Usage:
  python tools/retrieval_eval.py --fixtures apps/backend/tests/fixtures/sample_qa.json --k 3

This script runs retrieval using the in-memory adapter (default) and optionally
the PgVectorAdapter if `AI_AGENT_DATABASE_URL` is set. It computes precision@k
and recall@k before and after reranking.
"""
import argparse
import json
import os
from typing import List

from app.services.knowledge import default_vector_adapter, PgVectorAdapter

try:
    from app.services.reranker import rerank
except Exception:
    # local import path
    from apps.backend.app.services.reranker import rerank  # type: ignore


def precision_at_k(relevant: List[str], retrieved: List[str], k: int) -> float:
    topk = retrieved[:k]
    if not topk:
        return 0.0
    return sum(1 for d in topk if d in relevant) / len(topk)


def recall_at_k(relevant: List[str], retrieved: List[str], k: int) -> float:
    topk = set(retrieved[:k])
    if not relevant:
        return 0.0
    return sum(1 for d in relevant if d in topk) / len(relevant)


def run_evaluation(fixtures_path: str, k: int = 3):
    with open(fixtures_path, 'r', encoding='utf-8') as f:
        items = json.load(f)

    # items: list of {query, relevant: [doc strings]}

    # Evaluate using default adapter (in-memory)
    pre_scores = []
    post_scores = []

    # If DB URL set, create PgVectorAdapter
    db_url = os.getenv('AI_AGENT_DATABASE_URL')
    pg_adapter = None
    if db_url:
        # user should ensure db session factory is available; skip if not
        try:
            from app.services.knowledge import PgVectorAdapter
            pg_adapter = PgVectorAdapter(None)
        except Exception:
            pg_adapter = None

    for it in items:
        q = it['query']
        relevant = it.get('relevant', [])

        retrieved = default_vector_adapter.query('test-tenant', q, k*5)
        if hasattr(retrieved, '__await__'):
            import asyncio

            retrieved = asyncio.get_event_loop().run_until_complete(retrieved)

        pre_p = precision_at_k(relevant, retrieved, k)
        pre_r = recall_at_k(relevant, retrieved, k)

        # rerank
        reranked = [d for d, _ in rerank(q, retrieved)]
        post_p = precision_at_k(relevant, reranked, k)
        post_r = recall_at_k(relevant, reranked, k)

        pre_scores.append((pre_p, pre_r))
        post_scores.append((post_p, post_r))

        print(f"Query: {q}")
        print(f"  Pre  precision@{k}: {pre_p:.3f}, recall@{k}: {pre_r:.3f}")
        print(f"  Post precision@{k}: {post_p:.3f}, recall@{k}: {post_r:.3f}")
        print()

    # Aggregate
    def agg(scores):
        if not scores:
            return 0.0, 0.0
        p = sum(s[0] for s in scores) / len(scores)
        r = sum(s[1] for s in scores) / len(scores)
        return p, r

    pre_p, pre_r = agg(pre_scores)
    post_p, post_r = agg(post_scores)

    print("Summary:")
    print(f"  Avg pre precision@{k}: {pre_p:.3f}, recall@{k}: {pre_r:.3f}")
    print(f"  Avg post precision@{k}: {post_p:.3f}, recall@{k}: {post_r:.3f}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--fixtures', required=True)
    p.add_argument('--k', type=int, default=3)
    args = p.parse_args()

    run_evaluation(args.fixtures, args.k)


if __name__ == '__main__':
    main()
"""Retrieval evaluation harness.

Usage (smoke):
  python tools/retrieval_eval.py --smoke

This script runs simple precision@k / recall@k evaluations against the
in-memory `default_vector_adapter`. If a Postgres DB is configured via
`AI_AGENT_DATABASE_URL` it will also attempt to run the `PgVectorAdapter`.
"""
import os
import csv
import argparse
from typing import List, Dict

from apps.backend.app.services import knowledge as knowledge_mod
from apps.backend.app.services.reranker import rerank_tfidf


def synthetic_dataset():
    # tenant -> list of docs
    tenant = "t-smoke"
    docs = [
        "How to make masala chai at home",
        "Best recipes for masala chai and snacks",
        "Opening hours and contact info",
        "Menu and pricing for small cafe",
        "How to reserve a table",
    ]

    queries = {
        "how to make tea": [0, 1],
        "reserve table": [4],
        "opening hours": [2],
    }

    return tenant, docs, queries


def precision_recall_at_k(retrieved: List[str], relevant_idxs: List[int], all_docs: List[str], ks=(1, 3, 5)):
    results = {}
    relevant_set = set(relevant_idxs)
    for k in ks:
        top = retrieved[:k]
        top_idxs = [all_docs.index(d) for d in top if d in all_docs]
        tp = sum(1 for i in top_idxs if i in relevant_set)
        prec = tp / k
        rec = tp / max(1, len(relevant_set))
        results[f"p@{k}"] = prec
        results[f"r@{k}"] = rec
    return results


def run_eval(smoke: bool = False, rerank: bool = False):
    tenant, docs, queries = synthetic_dataset()

    # index into in-memory adapter
    knowledge_mod.default_vector_adapter.index_documents(tenant, docs)

    rows = []
    for q, rel_idxs in queries.items():
        retrieved = knowledge_mod.default_vector_adapter.query(tenant, q, top_k=5)

        if rerank:
            scored = rerank_tfidf(q, retrieved)
            retrieved = [p for (_s, p) in scored]

        metrics = precision_recall_at_k(retrieved, rel_idxs, docs, ks=(1, 3, 5))
        row = {"query": q, **metrics}
        rows.append(row)

    out = "retrieval_eval_results.csv"
    with open(out, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["query", "p@1", "r@1", "p@3", "r@3", "p@5", "r@5"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print("Wrote:", out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--rerank", action="store_true")
    args = parser.parse_args()

    run_eval(smoke=args.smoke, rerank=args.rerank)
