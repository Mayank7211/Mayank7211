# Feature Landscape

**Domain:** AI assistant platform for local businesses (brownfield)
**Researched:** 2026-03-21
**Overall confidence:** MEDIUM

## Scope Lens

This feature map is optimized for SMB outcomes in this project context:
- Faster onboarding-to-live for non-technical owners
- Better chat quality that converts visitors to qualified reservations/leads
- Reliable owner notifications so no high-intent request is missed

## Table Stakes

Features users expect by default. Missing these creates immediate trust and adoption risk.

| Feature | Why Expected | Complexity | Dependencies | SMB Value |
|---------|--------------|------------|--------------|-----------|
| Guided onboarding wizard (business profile, hours, services, contact channels) | Competing SMB tools position setup as fast and low-friction | Medium | Tenant model, validation rules, progressive save, sensible defaults | Time-to-value in first session; reduces setup drop-off |
| One-line widget embed + visual brand settings | Website chat tools commonly emphasize quick embed + branded widget | Low | Widget install snippet, theming tokens, preview | Owners can go live without developer help |
| Core knowledge ingestion (FAQ/docs upload, basic parsing status) | SMBs expect assistant answers to reflect their real business details | Medium | File upload pipeline, parsing, indexing, processing states | Fewer incorrect answers, less manual support |
| Fast response + transparent availability behavior (online/offline/away) | Buyers expect immediate response and clear fallback when no human is online | Medium | Chat runtime, availability config, fallback messaging, office-hours settings | Captures after-hours demand instead of losing it |
| Contact capture in chat (name, phone/email) before or during lead flow | Lead capture is core positioning in most SMB chat products | Low | Form prompts, validation, CRM/DB persistence | Converts anonymous traffic to follow-up opportunities |
| Human handoff + shared inbox visibility | SMB teams still need manual takeover for edge cases/high-value leads | Medium | Conversation assignment, inbox/thread model, role permissions | Better close rates for complex inquiries |
| Reservation/lead intent capture schema (service, preferred date/time, party size/notes) | Local-service businesses need structured intent, not only transcript text | Medium | Domain form schema, extraction, persistence, dashboard mapping | Actionable lead records, not just chat logs |
| Owner notifications for new high-intent leads/reservations (email first) | "Never miss a lead" is table-stakes promise; owner alerting drives ROI | Medium | Event triggers, notification templates, reliable delivery/retry | Immediate follow-up and higher conversion |
| Basic analytics (volume, response time, lead count, reservation count) | SMB buyers need proof that chat is helping revenue | Medium | Event instrumentation, dashboard aggregation | Justifies subscription and optimization |
| Consent and basic privacy controls for chat data collection | Consent/data handling controls are standard in modern chatflows | Medium | Consent UX, policy links, audit fields | Reduces legal and trust risk |

## Differentiators

Features that create meaningful advantage for local businesses after table stakes are solid.

| Feature | Value Proposition | Complexity | Dependencies | Why It Differentiates |
|---------|-------------------|------------|--------------|-----------------------|
| Vertical playbooks for top local-business types (dental, medspa, salon, HVAC, restaurant) | Prebuilt intents/prompts/questions shorten setup and improve relevance | Medium | Industry template library, per-tenant overrides, QA dataset | Better first-week performance than generic assistants |
| Conversion-aware chat quality controls (policy checks, forbidden claims, confidence-gated fallback to form/human) | Improves trust and reduces hallucination damage in revenue-critical moments | High | Response guardrails, confidence scoring, fallback orchestration | Safer automation for SMBs without dedicated ops teams |
| Reservation-readiness score + suggested next-best prompt | Helps owner quickly triage leads and prioritize callback effort | Medium | Lead enrichment rules, scoring model, dashboard surfacing | Converts noisy chats into ranked opportunities |
| Multi-channel owner alerts with escalation ladder (email -> SMS -> push/Slack) | Ensures urgent leads are seen quickly, even outside office hours | Medium | Notification routing, escalation timers, channel adapters | Higher response speed and reduced lead leakage |
| Smart after-hours mode (auto-collect intent + offer callback windows) | Turns off-hours traffic into structured next-day work queue | Medium | Availability engine, scheduling slots, lead forms | Strong SMB ROI with minimal staffing changes |
| Source-aware insights (which pages/intents generate reservations) | Connects chat outcomes to marketing pages and spend decisions | High | Click-path tracking, attribution model, analytics UX | Practical growth insights for owner-operators |
| "Owner voice" tuning (tone examples + approved phrasebook) | Keeps responses aligned with brand personality and trust | Medium | Prompt profile storage, style constraints, test preview | Feels local and human rather than generic bot-speak |
| No-show reduction hooks (deposit reminder integration, confirmation cadence) | Protects appointment businesses where no-shows erode margin | High | Booking/payments integrations, reminder policy engine | Directly improves revenue reliability |

## Anti-Features

Features to explicitly avoid in this milestone because they dilute SMB value or increase risk.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Build a full custom CRM inside the platform | High build/maintenance load; duplicates mature tools | Keep lightweight lead/reservation records + export/integration endpoints |
| Overly complex automation builder in v1 | Confusing for non-technical SMB owners; slows adoption | Provide curated templates + a few high-impact toggles |
| Fully autonomous booking writes to external calendars without confirmation | High risk of bad bookings from extraction errors | Use confirmation step and/or owner approval for first milestone |
| Broad omnichannel expansion (WhatsApp, social DMs, voice, etc.) before core web chat reliability | Spreads engineering effort thin and weakens core outcome | Nail website chat + reservation notification reliability first |
| Heavy customization surfaces with dozens of controls | Choice overload and support burden | Opinionated defaults with progressive advanced settings |
| "AI anything" features not tied to lead/reservation outcomes (image generation, novelty tools) | Distracts roadmap from measurable SMB ROI | Prioritize conversion, follow-up speed, and answer accuracy |
| Real-time dynamic pricing/revenue optimization engine | Complex domain logic, high risk of owner distrust | Start with fixed service metadata and simple availability rules |
| Premature enterprise governance layer (deep RBAC matrix, SSO bundles, workflow engines) | Misaligned with current local-business milestone scope | Keep practical tenant security and role basics only |

## Feature Dependencies

```text
Guided onboarding -> Widget embed -> First live chat
Guided onboarding -> Knowledge ingestion -> Higher chat answer quality
Chat runtime + availability settings -> Contact capture -> Reservation/lead intent capture
Reservation/lead intent capture -> Owner notifications -> Faster follow-up
Reservation/lead persistence -> Dashboard visibility -> Owner trust and optimization
Instrumentation -> Analytics -> Prioritization of playbooks and quality fixes
```

## Focus Areas You Asked For

### Onboarding
- Must be low-friction and goal-directed: "Get first lead" is the north star.
- Avoid requiring deep prompt engineering during setup.
- Progressive disclosure is key: only collect required inputs first; defer advanced config.

### Chat Quality
- Prioritize correctness over cleverness for SMB trust.
- Use confidence-gated fallback when uncertain (ask clarification or route to owner/handoff).
- Add lightweight quality review loop: bad-answer report -> prompt/knowledge fix.

### Reservations and Leads
- Treat reservation intent as structured data, not transcript-only text.
- Capture minimum viable fields first, with optional enrichment prompts.
- Preserve provenance: which page/source and which assistant turn triggered lead capture.

### Owner Notifications
- Email is baseline; escalation is differentiator.
- Alert payload should be compact and action-ready: who, what service, when requested, contact, transcript snippet, direct action link.
- Reliability matters more than channel breadth in this milestone (idempotency + retries + failure monitoring).

## MVP Recommendation

Prioritize (in order):
1. Guided onboarding + one-line embed + sane defaults
2. Reliable chat with contact capture and structured reservation/lead intent extraction
3. Deterministic owner email notifications for new high-intent leads
4. Dashboard visibility for captured leads/reservations and basic conversion metrics
5. Confidence-gated fallback/handoff to reduce incorrect high-stakes answers

Defer:
- Broad channel expansion and advanced workflow builders until core lead capture + notification reliability is proven.
- Autonomous booking writes to external systems until confirmation UX and quality controls are mature.

## Complexity and Sequencing Notes

- Fastest ROI sequence for SMB value:
  1) onboarding friction down,
  2) lead capture quality up,
  3) owner alert reliability up,
  4) analytics for iterative improvement.
- Highest rewrite risk if done too late:
  - Structured reservation schema and notification event model.
- Highest operational risk if done too early:
  - Multi-channel automation and autonomous external booking commits.

## Sources

- https://www.hubspot.com/products/service/live-chat (product expectations: routing, chatbot assist, notifications context)
- https://knowledge.hubspot.com/chatflows/create-a-live-chat (implementation expectations: setup, availability, targeting, consent, spam controls)
- https://www.podium.com/webchat/ (SMB positioning: lead capture, unified inbox, brand widget, 24/7 AI response)
- https://www.podium.com/article/what-is-live-chat/ (SMB best practices: speed, offline alternatives, lead opportunities)
- https://www.helpscout.com/live-chat/ (small-team workflow expectations: shared inbox, proactive messaging, in-context support)
- https://www.setmore.com/features/booking-page (booking expectations: 24/7 booking page, deposits/payments, channel distribution)
- https://www.vagaro.com/pro/online-booking (reservation expectations: reminders, deposits, no-show reduction)
- https://www.simplybook.me/en/features (booking ecosystem breadth: intake forms, calendar sync, notifications, reserve channels)

## Confidence Notes

- HIGH: Table-stakes expectations around setup, chat routing, lead capture, availability behavior, and consent controls.
- MEDIUM: Differentiator impact estimates (depends on execution quality and vertical fit).
- LOW-MEDIUM: Competitor marketing claims around conversion uplifts; treat as directional, not guaranteed outcomes.
