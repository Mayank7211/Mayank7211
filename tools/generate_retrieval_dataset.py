"""Generate a labeled retrieval dataset.

Usage:
  python tools/generate_retrieval_dataset.py --out data/retrieval_dataset/labels.csv

The script will attempt to connect to a Postgres DB if `AI_AGENT_DATABASE_URL`
is set in the environment and extract `knowledge_sources` rows. If no DB is
available, the script emits a small synthetic sample (written to --out).
"""
from __future__ import annotations

import csv
import os
import argparse
import uuid

DB_URL_ENV = "AI_AGENT_DATABASE_URL"


def generate_sample(out_path: str):
    rows = [
        ("demo-tenant", "what are your opening hours?", "doc-1", "Our location is open Monday to Friday from 9am to 6pm.", 2),
        ("demo-tenant", "do you accept walk-ins?", "doc-2", "We accept walk-ins, but appointments are recommended during peak hours.", 1),
        ("demo-tenant", "what colors do you offer?", "doc-3", "We offer a variety of colors; check catalog for full list.", 0),
    ]
    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["tenant_id", "query", "doc_id", "doc_text", "relevance"])
        for r in rows:
            writer.writerow(r)
    print(f"Wrote sample dataset to {out_path}")


def pull_from_db(out_path: str, db_url: str, max_docs: int = 500):
    # Minimal DB pull using asyncpg if installed; falls back to sample generation.
    try:
        import asyncpg
    except Exception:
        print("asyncpg not installed — falling back to sample generator")
        return generate_sample(out_path)

    async def _run():
        conn = await asyncpg.connect(dsn=db_url)
        try:
            rows = await conn.fetch("SELECT id, tenant_id, raw_text FROM knowledge_sources ORDER BY created_at DESC LIMIT $1", max_docs)
            with open(out_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["tenant_id", "query", "doc_id", "doc_text", "relevance"])
                for r in rows:
                    tid = r.get("tenant_id") or "unknown"
                    doc_id = r.get("id") or str(uuid.uuid4())
                    text = (r.get("raw_text") or "").replace("\n", " ")
                    # For exported dataset, queries are left blank for annotation teams to fill.
                    writer.writerow([tid, "", doc_id, text, 0])
            print(f"Exported {len(rows)} docs to {out_path}")
        finally:
            await conn.close()

    import asyncio

    asyncio.run(_run())


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True, help="Output CSV path")
    p.add_argument("--use-db", action="store_true", help="Force DB extraction if env var set")
    args = p.parse_args()

    out = args.out
    db_url = os.environ.get(DB_URL_ENV)
    if args.use_db and db_url:
        pull_from_db(out, db_url)
    else:
        generate_sample(out)


if __name__ == "__main__":
    main()
