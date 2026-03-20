# AI Assistant Builder for Local Businesses

## What This Is

A multi-tenant AI assistant platform for local businesses that provides website chat, business-specific responses, and admin visibility into conversations and reservations. Business owners onboard their assistant, embed a widget, upload knowledge, and monitor outcomes through a dashboard. Website visitors get fast answers and can submit reservation-style requests.

## Core Value

A local business can go from setup to a working website assistant quickly, and reliably capture customer reservation intent.

## Requirements

### Validated

- ✓ Multi-tenant tenant creation and management flows exist in backend APIs and frontend onboarding.
- ✓ Embeddable chat widget exists with branding and placement customization.
- ✓ Chat backend flow exists with model gateway and tenant-aware prompting.
- ✓ Knowledge upload/parsing exists for supported document formats.
- ✓ Basic analytics and reservation-oriented tracking endpoints exist.

### Active

- [ ] End-to-end reservation notification flow sends booking details to the business owner email.
- [ ] Reservation capture data is consistently persisted and visible in admin dashboard workflows.
- [ ] Onboarding-to-live path remains simple for non-technical business owners.

### Out of Scope

- Native mobile apps — web and widget experience are the v1 priority.
- Multi-provider billing/subscription automation — defer until core reservation capture is stable.

## Context

- Existing brownfield codebase with FastAPI backend, React frontend, embeddable widget, and SQL schema.
- Current focus is local-business adoption, fast setup, and practical outcomes rather than platform breadth.
- Existing docs indicate Groq-based model integration, document parsing, analytics APIs, and admin dashboard capabilities.
- Codebase map has been generated under `.planning/codebase/` to anchor architecture, stack, quality, and concerns.

## Constraints

- **Tech stack**: Keep compatibility with existing FastAPI + React + widget architecture — avoid disruptive rewrites.
- **Usability**: Setup flow must stay simple for small business operators — minimize operational overhead.
- **Reliability**: Reservation capture and owner notification must be dependable — this is core business value.
- **Security**: Tenant-scoped data paths need safer defaults — current concerns must be reduced as implementation proceeds.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Keep brownfield architecture as baseline | Existing implementation already covers core MVP flows | — Pending |
| Prioritize reservation notification to owner email in v1 | Directly tied to business ROI and immediate usefulness | — Pending |
| Keep onboarding + widget embed as first-class path | Fast time-to-value is critical for local business adoption | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? -> Move to Out of Scope with reason
2. Requirements validated? -> Move to Validated with phase reference
3. New requirements emerged? -> Add to Active
4. Decisions to log? -> Add to Key Decisions
5. "What This Is" still accurate? -> Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check - still the right priority?
3. Audit Out of Scope - reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-03-21 after initialization*
