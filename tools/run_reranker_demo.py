"""Demo runner for the cross-encoder reranker.

Reads `data/retrieval_dataset/labels.csv` and for each row uses the query and
the small pool of documents in the CSV to demonstrate rescoring. This is a
lightweight smoke harness useful in CI.
"""
import csv
from collections import defaultdict
import sys
import os

# Ensure repository root is on sys.path so `apps.backend...` imports work when
# running scripts from the repo root.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from apps.backend.app.services.cross_encoder_reranker import default_reranker
import argparse


def load_dataset(path: str):
    q_to_docs = defaultdict(list)
    queries = []
    with open(path, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            q = row.get("query", "").strip()
            if not q:
                # skip blank queries (exported DB rows)
                continue
            queries.append((q, row.get("tenant_id")))
            # For demo, collect all docs for tenant
            q_to_docs[q].append(row.get("doc_text", ""))
    return queries, q_to_docs


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="infile", required=True)
    args = p.parse_args()

    queries, q_to_docs = load_dataset(args.infile)
    reranker = default_reranker()
    print("Cross-encoder available:", reranker.available())

    for q, _ in queries:
        docs = q_to_docs.get(q, [])
        if not docs:
            continue
        ranked = reranker.rerank(q, docs)
        top = ranked[0]
        print(f"Query: {q}")
        print(f"Top: score={top[1]:.4f} doc={top[0][:120]}")
        print("---")


if __name__ == "__main__":
    main()
