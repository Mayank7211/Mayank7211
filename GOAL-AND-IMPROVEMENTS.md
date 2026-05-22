# Goal and Improvements

## Product Goal
Build an affordable AI assistant builder for small local businesses (consultants, doctors, clinics, service providers) where a user submits business information and gets a production-ready assistant website widget and API.

## Core Constraints
- Keep cost very low.
- Avoid lock-in to expensive private APIs.
- Be production-ready (reliability, safety, logs, monitoring, multi-tenant).

## North Star
Time from business info submission to live assistant: under 30 minutes.

## MVP Scope (Phase 1)
- Business onboarding form:
  - Business name, domain, category, services, FAQ, location, phone, WhatsApp/email.
- Knowledge ingestion:
  - Manual text, website URL crawl, PDF upload.
- Assistant generation:
  - Prompt template + domain profile + retrieved business context.
- Deployment output:
  - Embeddable chat widget script.
  - REST endpoint for chat.
- Basic admin panel:
  - Edit content, view conversations, export leads.

## Recommended Architecture
- Frontend: Next.js + Tailwind + component library.
- Backend API: FastAPI or NestJS.
- Database: Postgres (multi-tenant schema or tenant_id isolation).
- Vector store: pgvector first, move to dedicated vector DB later only if needed.
- Queue/jobs: Redis + background worker for crawling and indexing.
- AI gateway layer:
  - Unified model interface so providers can be swapped without changing business logic.
- Hosting:
  - App on low-cost VPS or container platform.
  - Cloudflare for DNS, TLS, tunnel/edge routing where useful.

## Model Strategy (Low Cost + Production)
- Tier 1 (default): low-cost public API providers for open models.
- Tier 2 (fallback): self-hosted open model (vLLM/Ollama) for continuity.
- Tier 3 (premium optional): paid provider only for high-value tenants.

Use routing rules:
- Short/simple queries -> cheaper small model.
- Complex or low-confidence queries -> stronger model.
- Hard timeout + retry + fallback provider.

## Production Readiness Checklist
- Auth and tenant isolation enforced everywhere.
- Rate limits per tenant and per IP.
- Prompt injection and data exfiltration guardrails.
- Output moderation and unsafe intent handling.
- Observability:
  - Structured logs, latency metrics, token/cost tracking, error alerts.
- Backups and restore drills.
- SLAs and incident response playbook.

## High-Impact Improvements
1. Domain packs:
   - Ready templates for doctor, consultant, salon, legal, tuition, etc.
2. Lead capture workflow:
   - Collect user name/phone/email and send to business CRM or WhatsApp.
3. Multilingual support:
   - Hindi + English first for local adoption.
4. Human handoff:
   - Escalate to WhatsApp/call when confidence is low.
5. Auto website sync:
   - Re-crawl business website on schedule and refresh knowledge.
6. Evaluation harness:
   - Golden Q/A tests per tenant to detect regressions before deployment.

## 14-Day Execution Plan
Day 1-2:
- Finalize data model (tenant, assistant, knowledge source, conversation, lead).
- Define model gateway interface.

Day 3-5:
- Build onboarding form + backend create-assistant API.
- Add website crawl + text ingestion + vector indexing.

Day 6-8:
- Build chat API with retrieval + prompt assembly.
- Add widget embed script.

Day 9-10:
- Add analytics dashboard (conversations, lead count, token usage).
- Add rate limiting + logging + retries/fallback.

Day 11-12:
- Add basic safety rules and refusal templates.
- Add multilingual support and lead capture flow.

Day 13-14:
- Load testing, bug fixes, production checklist pass.
- Deploy first pilot tenant.

## Success Metrics
- Setup completion rate.
- First response latency.
- Lead conversion rate.
- Cost per 1,000 messages.
- Resolution without human handoff.
- Monthly active tenants.
