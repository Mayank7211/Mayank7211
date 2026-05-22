"""Run retrieval evaluation using labeled CSV and the cross-encoder reranker.

Input CSV format: `tenant_id,query,doc_id,doc_text,relevance` (relevance: 0/1/2)

Outputs: `retrieval_eval_breakdown.csv` and `retrieval_eval_summary.json`
"""
import csv
import json
import sys
import os
import argparse
from collections import defaultdict
from typing import List

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from apps.backend.app.services import knowledge as knowledge_mod
from apps.backend.app.services.cross_encoder_reranker import default_reranker


def load_labels(path: str):
    rows = []
    with open(path, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append(row)
    return rows


def group_by_query(rows):
    qmap = defaultdict(list)
    for r in rows:
        q = (r.get("query") or "").strip()
        if not q:
            continue
        qmap[q].append(r)
    return qmap


def precision_at_k(relevant_ids: List[str], retrieved_ids: List[str], k: int):
    topk = retrieved_ids[:k]
    if not topk:
        return 0.0
    return sum(1 for d in topk if d in relevant_ids) / len(topk)


def run(path: str, k: int = 3):
    rows = load_labels(path)
    qmap = group_by_query(rows)

    reranker = default_reranker()

    breakdown = []
    all_pre = []
    all_post = []

    for q, docs in qmap.items():
        tenant = docs[0].get("tenant_id") or "t-demo"
        # index tenant docs into in-memory adapter for eval
        passages = [d.get("doc_text") or "" for d in docs]
        ids = [d.get("doc_id") or str(i) for i, d in enumerate(docs)]
        knowledge_mod.default_vector_adapter.index_documents(tenant, passages)

        retrieved = knowledge_mod.default_vector_adapter.query(tenant, q, top_k=10)
        if hasattr(retrieved, "__await__"):
            import asyncio

            retrieved = asyncio.get_event_loop().run_until_complete(retrieved)

        # map retrieved passage to doc_id via exact match
        retrieved_ids = []
        for r in retrieved:
            try:
                idx = passages.index(r)
                retrieved_ids.append(ids[idx])
            except ValueError:
                # not found, skip
                pass

        relevant_ids = [d.get("doc_id") for d in docs if int(d.get("relevance") or 0) > 0]

        pre_p = precision_at_k(relevant_ids, retrieved_ids, k)

        # rerank
        ranked = reranker.rerank(q, retrieved)
        reranked_ids = []
        for p, _s in ranked:
            try:
                idx = passages.index(p)
                reranked_ids.append(ids[idx])
            except ValueError:
                pass

        post_p = precision_at_k(relevant_ids, reranked_ids, k)

        breakdown.append({"query": q, "pre_p@k": pre_p, "post_p@k": post_p})
        all_pre.append(pre_p)
        all_post.append(post_p)

        print(f"Query: {q} pre_p@{k}={pre_p:.3f} post_p@{k}={post_p:.3f}")

    summary = {
        "avg_pre_p@k": sum(all_pre) / max(1, len(all_pre)),
        "avg_post_p@k": sum(all_post) / max(1, len(all_post)),
    }

    out_csv = "retrieval_eval_breakdown.csv"
    with open(out_csv, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["query", "pre_p@k", "post_p@k"])
        writer.writeheader()
        for r in breakdown:
            writer.writerow(r)

    out_json = "retrieval_eval_summary.json"
    with open(out_json, "w") as fh:
        json.dump(summary, fh, indent=2)

    print("Wrote:", out_csv, out_json)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--labels", required=True)
    p.add_argument("--k", type=int, default=3)
    args = p.parse_args()
    run(args.labels, args.k)


if __name__ == "__main__":
    main()
