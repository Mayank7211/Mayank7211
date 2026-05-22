-- Add embedding column for pgvector support
-- Run this against your Postgres database (pgvector extension required)

BEGIN;

ALTER TABLE IF EXISTS knowledge_sources
ADD COLUMN IF NOT EXISTS embedding vector(1536);

-- Optional: create IVFFLAT index for faster approximate nearest neighbor searches
-- Adjust the 'lists' parameter for your dataset size (e.g., 100-1000)
CREATE INDEX IF NOT EXISTS idx_knowledge_embedding ON knowledge_sources USING ivfflat (embedding) WITH (lists = 100);

COMMIT;
