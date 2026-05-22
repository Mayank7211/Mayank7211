# Phase 3 CONTEXT — Retrieval + Relevance Tuning

Scope
- Phase: 3 — Retrieval + Relevance Tuning
- Goal: Produce reliable reranking (cross-encoder) that meaningfully improves precision@k and user-visible relevance, plus a reproducible evaluation pipeline and CI smoke checks.

Decisions (actionable, code-linked)

1) Reranker model & training strategy
- Decision: Use a cross-encoder as the primary reranker for Phase 3 accuracy experiments. Prototype/fine-tune using a compact cross-encoder (example: `cross-encoder/ms-marco-MiniLM-L-6-v2`) to balance quality and latency.
- Rationale: cross-encoders provide highest short-list accuracy for reranking small candidate pools; our repo already contains a `CrossEncoderReranker` wrapper and a worker (`tools/reranker_worker.py`).
- Training signal: canonical source is human-annotated graded labels (0/1/2). Augment with synthetic positives (retrieval augmentation) and hard negatives mined from the current vector adapter. Use cross-entropy on pairwise labels or listwise loss if supported.
- Latency target (production): aim for <100ms per single-query rerank on a compact cross-encoder; if not achievable, distill to a faster model or serve as a microservice behind async caching.
- Fallback: keep the existing TF‑IDF fallback (in `apps/backend/app/services/reranker.py`) to guarantee deterministic behavior in CI and low-resource environments.

Implementation actions
- Prepare JSONL training files from `data/retrieval_dataset/labels.csv` (fields: `tenant_id,query,doc_id,doc_text,relevance`). Script: `tools/convert_labels_to_jsonl.py` (recommended next task).
- Fine-tune on a small GPU instance; use Hugging Face / sentence-transformers training scripts with early stopping.

2) Dataset labeling & batching workflow
- Decision: Adopt JSONL as canonical dataset exchange format with schema:
  - `tenant_id`, `query`, `doc_id`, `doc_text`, `relevance` (0/1/2), optional `annotator_id`, `timestamp`, `notes`.
- Pooling strategy: generate candidate pools by running the current `default_vector_adapter.query(tenant_id, query, top_k=100)` and use top-K pooling for annotation (K=100 default). Also include random negatives for coverage.
- Annotation QA: dual annotation + adjudication for disagreements on the dev/test sets. Perform lightweight reviewer QA for production labels.
- Batching: annotate in batches of 1k–5k query/document pairs; prioritize high-frequency queries and tenant coverage.

Implementation actions
- Provide `tools/generate_annotation_batches.py` to produce JSONL batches and upload-ready CSVs. (Next task.)
- Maintain a small `datasets/` registry with dataset id, source, and split info.

3) Offline scoring storage, keying & invalidation
- Decision: Use Redis ZSETs for precomputed reranker scores keyed by a stable namespace that includes model version and a query hash. Key format:
  - `reranker:{model_version}:query:{sha1(query)}`
- Store: members = `doc_id`, score = float (higher = more relevant). Use `ZADD` for atomic updates.
- TTL and invalidation:
  - Set a default TTL (e.g., 7 days) to limit storage growth.
  - On ingestion of new/updated docs for `tenant_id`, enqueue invalidation of keys whose candidate pools include changed docs. Practical approach: on ingest, delete cached keys for that tenant (or set a short TTL) and schedule worker recompute for popular queries.
- Consistency:
  - Use Redis zsets for fast lookup; if durable archival is required, persist top-K snapshots to Postgres as `reranker_snapshots` with `model_version` and `dataset_id` columns.

Implementation actions
- Update `tools/reranker_worker.py` to write keys using the model version env var (e.g., `RERANKER_MODEL=v1`).
- Add `app/services/reranker_cache.py` abstraction (Redis lookup -> fallback to live rerank) to centralize access.

4) Evaluation metrics, thresholds & CI gating
- Decision: Use the following metric suite for experiments and gating:
  - Primary: MRR@10, P@1, P@3
  - Secondary: NDCG@10, Recall@k
- Dataset split: dev (60%), validation (20%), test (20%) — ensure tenant-wise splits where tenant-sensitive behavior exists.
- CI gating policy (initial): keep lightweight smoke in CI (current precision@k script). Add nightly full evaluation job that runs the full test set and records metrics. Do not block merges on noisy full-eval; require manual promotion of models. Set conservative alert thresholds (e.g., post_p@3 >= baseline + 0.02 or post_p@3 >= 0.6 absolute) and flag regressions in PRs.

Implementation actions
- Extend `tools/run_retrieval_eval_full.py` to compute MRR and NDCG and emit `evaluation/{dataset_id}/{model_version}/summary.json`.
- Add a nightly GitHub Action `retrieval-eval-nightly.yml` to run full evaluation on larger datasets (requires credentials + environment variables). Keep a small CI smoke workflow on PRs (already present).

Code-context pointers
- `apps/backend/app/services/cross_encoder_reranker.py` — CrossEncoder wrapper + fallback.
- `tools/reranker_worker.py` — offline worker that writes Redis zsets.
- `apps/backend/app/services/assistant_service.py` — schedules rerank background tasks and consults feature flags.
- `tools/run_retrieval_eval_full.py` — evaluation runner (precision@k, aggregates) and currently writes CSV/JSON outputs.

Deferred ideas (captured but not in Phase 3 scope)
- Full annotation UI and crowdsourcing integration (separate phase). I'll add to backlog.
- Learned reranker distillation to reduce latency (post-Phase 3).

Next steps (recommended immediate work)
1. Convert existing CSV to JSONL and create `datasets/phase3-dev.jsonl` and `phase3-test.jsonl` (tooling task).  
2. Deploy Redis (dev) and run `tools/reranker_worker.py` on the dev dataset to populate top-K zsets.  
3. Run large-scale evaluation on the dev set and collect MRR/NDCG.  
4. Fine-tune a compact cross-encoder on the dev set; repeat evaluation and record metrics.  

Ready to proceed: I will (a) add conversion and dataset-batching scripts, (b) extend the eval runner to compute MRR/NDCG and save structured summaries, and (c) implement `racker_cache.py` to centralize Redis lookups — unless you want a different order.
