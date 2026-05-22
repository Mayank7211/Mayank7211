Labeled retrieval dataset scaffold for Phase 3.

Contents
- `sample_labels.csv` — small example of (tenant_id, query, doc_id, doc_text, relevance)

How to use
1. Run the generator to produce a larger dataset or export from your DB:

```bash
python tools/generate_retrieval_dataset.py --out data/retrieval_dataset/labels.csv
```

2. The generator attempts to read `AI_AGENT_DATABASE_URL` if present to pull `knowledge_sources` rows; otherwise it emits a small synthetic sample for annotation.

Format
- CSV columns: `tenant_id,query,doc_id,doc_text,relevance`

Relevance values:
- `2` = highly relevant
- `1` = somewhat relevant
- `0` = not relevant

Add more rows or convert to JSONL for training rerankers.
