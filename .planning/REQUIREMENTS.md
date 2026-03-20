# Requirements: AI Assistant Builder for Local Businesses

**Defined:** 2026-03-21
**Core Value:** A local business can go from setup to a working website assistant quickly, and reliably capture customer reservation intent.

## v1 Requirements

### Onboarding

- [ ] **ONB-01**: Business owner can create a tenant profile with name, domain, services, and description.
- [ ] **ONB-02**: Business owner can upload supported documents (PDF, DOCX, TXT) during onboarding.
- [ ] **ONB-03**: System validates file type and file size and returns clear errors for invalid uploads.
- [ ] **ONB-04**: Business owner receives an embeddable widget snippet with tenant-specific configuration.

### Chat Experience

- [ ] **CHAT-01**: Website visitor can open the widget and send/receive chat messages.
- [ ] **CHAT-02**: Assistant responses are tenant-aware and use business context from tenant profile.
- [ ] **CHAT-03**: Assistant maintains short conversation context across a session.
- [ ] **CHAT-04**: System flags low-confidence or escalation-needed interactions for owner visibility.

### Knowledge

- [ ] **KNOW-01**: Uploaded documents are parsed into usable text chunks for retrieval.
- [ ] **KNOW-02**: Assistant can answer frequently asked questions using tenant knowledge context.
- [ ] **KNOW-03**: Owner can add/update tenant knowledge without redeploying widget code.

### Reservations

- [ ] **RSV-01**: System detects reservation or booking intent from chat interactions.
- [ ] **RSV-02**: Reservation details (name/contact/requested time/message) are persisted reliably.
- [ ] **RSV-03**: Business owner receives reservation notifications by email for captured booking intent.
- [ ] **RSV-04**: Notification flow supports retry behavior so transient failures do not silently drop reservations.

### Admin Analytics

- [ ] **ANA-01**: Owner can view dashboard stats for conversations, confidence, and reservations.
- [ ] **ANA-02**: Owner can view recent conversations with timestamps and confidence signals.
- [ ] **ANA-03**: Owner can view pending reservations in a dedicated dashboard view.

### Security and Guardrails

- [ ] **SEC-01**: Tenant-scoped endpoints enforce authorization checks beyond tenant ID possession.
- [ ] **SEC-02**: API CORS policy is restricted to explicit allowed origins for production contexts.
- [ ] **SEC-03**: Chat and upload endpoints enforce abuse protections (rate limits and/or request guards).

## v2 Requirements

### Product Expansion

- **EXP-01**: Owner can configure advanced AI behavior profiles (tone, strictness, escalation policy).
- **EXP-02**: Owner can enable multilingual assistant responses.
- **EXP-03**: Owner can define business hours and appointment slot constraints in dashboard UI.

### Commercialization

- **COM-01**: Platform supports subscription billing and plan management.
- **COM-02**: Platform supports role-based admin access for multi-user business teams.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Native mobile app | Web + widget channels are sufficient for v1 validation |
| Full omnichannel CRM | Not required to validate chat + reservation core value |
| Multi-tenant SSO/OAuth enterprise flows | SMB v1 focus favors simpler onboarding and operations |
| Real-time voice assistant | Adds complexity before proving text-chat reservation outcomes |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| ONB-01 | Phase 1 | Pending |
| ONB-02 | Phase 1 | Pending |
| ONB-03 | Phase 1 | Pending |
| ONB-04 | Phase 1 | Pending |
| CHAT-01 | Phase 2 | Pending |
| CHAT-02 | Phase 2 | Pending |
| CHAT-03 | Phase 2 | Pending |
| CHAT-04 | Phase 2 | Pending |
| KNOW-01 | Phase 3 | Pending |
| KNOW-02 | Phase 3 | Pending |
| KNOW-03 | Phase 3 | Pending |
| RSV-01 | Phase 4 | Pending |
| RSV-02 | Phase 4 | Pending |
| RSV-03 | Phase 4 | Pending |
| RSV-04 | Phase 4 | Pending |
| ANA-01 | Phase 5 | Pending |
| ANA-02 | Phase 5 | Pending |
| ANA-03 | Phase 5 | Pending |
| SEC-01 | Phase 1 | Pending |
| SEC-02 | Phase 1 | Pending |
| SEC-03 | Phase 1 | Pending |

**Coverage:**
- v1 requirements: 21 total
- Mapped to phases: 21
- Unmapped: 0

---
*Requirements defined: 2026-03-21*
*Last updated: 2026-03-21 after initial definition*
