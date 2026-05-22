"""Lightweight runner to keep the async embedding worker running.

This script re-runs the async worker in a loop with a small backoff so it can
be supervised by systemd or run in the foreground via `nohup`/tmux.

Usage:
  AI_AGENT_DATABASE_URL="postgresql+asyncpg://user:pass@host:5432/db" \
  AI_AGENT_OPENAI_API_KEY="sk-..." \
  python apps/backend/scripts/run_embedding_worker.py
"""
import asyncio
import logging
import time

from apps.backend.scripts.async_compute_embeddings import main as worker_main  # type: ignore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("embedding-runner")


async def run_loop():
    backoff_seconds = 60
    while True:
        try:
            logger.info("Starting embedding worker run")
            # worker_main runs till it exhausts available rows; we re-run after a pause
            await worker_main()
            logger.info("Worker run finished; sleeping before next check")
            await asyncio.sleep(60 * 5)
        except Exception:
            logger.exception("Embedding worker crashed; will retry after backoff")
            await asyncio.sleep(backoff_seconds)
            backoff_seconds = min(backoff_seconds * 2, 3600)


if __name__ == "__main__":
    asyncio.run(run_loop())
