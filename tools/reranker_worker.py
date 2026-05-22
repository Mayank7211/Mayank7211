"""Simple reranker worker: computes cross-encoder scores for queries vs docs and stores top-K in Redis zsets.

Usage:
  python tools/reranker_worker.py --labels data/retrieval_dataset/labels.csv --topk 5
Requires Redis available via REDIS_URL or AI_AGENT_REDIS_URL env var.
"""
import csv
import os
import sys
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from apps.backend.app.services.cross_encoder_reranker import default_reranker


def load_labels(path):
    qmap = defaultdict(list)
    with open(path, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            q = (row.get("query") or "").strip()
            if not q:
                continue
            qmap[q].append(row)
    return qmap


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--labels", required=True)
    p.add_argument("--topk", type=int, default=5)
    args = p.parse_args()

    qmap = load_labels(args.labels)
    reranker = default_reranker()

    # attempt redis
    try:
        import redis.asyncio as aioredis
        redis_url = os.environ.get("REDIS_URL") or os.environ.get("AI_AGENT_REDIS_URL")
        if not redis_url:
            print("REDIS_URL not set; aborting worker")
            return
        r = aioredis.from_url(redis_url)
    except Exception:
        print("redis.asyncio not available; install redis and set REDIS_URL to enable worker")
        return

    import asyncio

    async def _run():
        for q, docs in qmap.items():
            passages = [d.get("doc_text") or "" for d in docs]
            ids = [d.get("doc_id") or str(i) for i, d in enumerate(docs)]
            scored = reranker.rerank(q, passages)
            # store topk in zset keyed by 'reranker:{q_hash}'
            key = f"reranker:query:{abs(hash(q))}"
            # remove existing
            await r.delete(key)
            for (p, s), doc_id in zip(scored[: args.topk], ids):
                await r.zadd(key, {doc_id: float(s)})
            print(f"Stored top {args.topk} scores for query '{q}' -> {key}")

    asyncio.run(_run())


if __name__ == "__main__":
    main()
