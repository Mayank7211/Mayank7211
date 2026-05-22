---
phase: 02-tenant-aware-chat-baseline
created: 2026-05-22
owner: Mayank
status: draft
---

# Phase 2 Context: Tenant-Aware Chat Baseline

Goal: Allow website visitors to interact with the widget and receive tenant-specific, context-aware responses that reflect uploaded knowledge and tenant configuration.

Scope:
- Widget request/response plumbing with tenant scoping
- Session continuity for short conversation context
- Minimal latency budget and deterministic error handling

Decisions to confirm during discussion:
- Live chat routing: pass-through to existing ModelGateway vs lightweight prefilter for reservation detection
- Session retention policy: in-memory short sessions vs DB-backed session records
- Tenant context tokenization: top-k retrieval vs hybrid relevance scoring

Integration points:
- `apps/frontend` widget and chat UI
- `apps/backend/app/services/assistant_service.py` chat method
- `apps/backend/app/services/knowledge.py` retrieval pipeline

Next actions:
- Run `/gsd-discuss-phase 02-tenant-aware-chat-baseline` to gather unanswered questions and stakeholder preferences.
