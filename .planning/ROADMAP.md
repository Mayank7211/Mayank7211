
# Roadmap: AI Assistant Builder for Local Businesses

## Phases

- [ ] **Phase 1: Secure Onboarding Foundation** - Owners can onboard and embed safely with tenant security guardrails in place.
- [ ] **Phase 2: Tenant-Aware Chat Baseline** - Visitors can use live chat with coherent tenant-specific responses.
- [ ] **Phase 3: Reservation Capture and Notification Reliability** - Booking intent is captured, persisted, and delivered to owners reliably.
- [ ] **Phase 4: Knowledge Runtime and Escalation Visibility** - Knowledge-grounded answers and low-confidence flags improve response quality.
- [ ] **Phase 5: Owner Analytics and Reservation Operations** - Owners can monitor performance and act on pending reservations.

## Phase Details

### Phase 1: Secure Onboarding Foundation
**Goal**: A business owner can complete initial setup and deploy a tenant-specific widget while tenant boundaries and abuse protections are enforced.
**Depends on**: Nothing (first phase)
**Requirements**: ONB-01, ONB-02, ONB-03, ONB-04, SEC-01, SEC-02, SEC-03
**Success Criteria** (what must be TRUE):
1. Owner can create a tenant profile with required business details and receives clear validation errors for invalid input.
2. Owner can upload supported onboarding files, and invalid type/size uploads are rejected with actionable error messages.
3. Owner receives a tenant-specific widget snippet that can be embedded without custom backend changes.
4. Requests that do not belong to the authenticated tenant are blocked, and production CORS allows only explicitly configured origins.
5. Chat and upload endpoints throttle or reject abusive request patterns instead of silently over-consuming resources.
**Plans**: 4 plans

Plans:
- [x] 01-00-PLAN.md - Produce Wave 0 backend test scaffolds for ONB-01..04 and SEC-01..03 before implementation waves.
- [x] 01-01-PLAN.md - Enforce tenant authorization dependencies and explicit-origin CORS hardening.
- [x] 01-02-PLAN.md - Implement strict onboarding contracts, parameterized widget snippet defaults, and abuse guardrails.
- [ ] 01-03-PLAN.md - Deliver onboarding UI error clarity and complete Phase 1 automated verification coverage.

### Phase 2: Tenant-Aware Chat Baseline
**Goal**: Website visitors can interact with the widget and receive context-aware responses for the correct business tenant.
**Depends on**: Phase 1
**Requirements**: CHAT-01, CHAT-02, CHAT-03
**Success Criteria** (what must be TRUE):
1. Visitor can open the widget and exchange messages with successful request/response flow.
2. Assistant responses reflect the configured tenant business context rather than generic answers.
3. Short conversation context is preserved across multiple messages in the same session.
**Plans**: TBD

### Phase 3: Reservation Capture and Notification Reliability
**Goal**: Reservation intent is identified and converted into durable owner notifications with no silent drops.
**Depends on**: Phase 2
**Requirements**: RSV-01, RSV-02, RSV-03, RSV-04
**Success Criteria** (what must be TRUE):
1. Reservation or booking intent is detected during chat interactions and converted into a structured reservation record.
2. Reservation details (name, contact, requested time, message) are persisted reliably, including during transient infrastructure failures.
3. Owner receives an email notification for each captured reservation in normal operating conditions.
4. Failed notification attempts are retried and remain visible until delivered or explicitly marked failed.
**Plans**: TBD

### Phase 4: Knowledge Runtime and Escalation Visibility
**Goal**: The assistant answers from tenant knowledge and surfaces uncertain interactions for owner follow-up.
**Depends on**: Phase 2
**Requirements**: KNOW-01, KNOW-02, KNOW-03, CHAT-04
**Success Criteria** (what must be TRUE):
1. Uploaded knowledge files are parsed into retrievable text chunks usable by runtime retrieval.
2. Assistant can answer common tenant FAQs using uploaded knowledge context.
3. Owner can add or update knowledge and have changes reflected without redeploying widget code.
4. Low-confidence or escalation-needed interactions are flagged and visible to the owner.
**Plans**: TBD

### Phase 5: Owner Analytics and Reservation Operations
**Goal**: Owners can monitor conversation quality and reservation throughput, then act on pending reservation workload.
**Depends on**: Phase 3, Phase 4
**Requirements**: ANA-01, ANA-02, ANA-03
**Success Criteria** (what must be TRUE):
1. Owner can view dashboard statistics for conversations, confidence, and reservations.
2. Owner can review recent conversations with timestamps and confidence indicators.
3. Owner can open a dedicated pending reservations view for operational follow-up.
**Plans**: TBD
## Progress Table

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Secure Onboarding Foundation | 2/3 | Executing | 01-03-PLAN.md |
| 2. Tenant-Aware Chat Baseline | 0/0 | Not started | - |
| 3. Reservation Capture and Notification Reliability | 0/0 | Not started | - |
| 4. Knowledge Runtime and Escalation Visibility | 0/0 | Not started | - |
| 5. Owner Analytics and Reservation Operations | 0/0 | Not started | - |

## Coverage Map

- ONB-01 -> Phase 1
- ONB-02 -> Phase 1
- ONB-03 -> Phase 1
- ONB-04 -> Phase 1
- SEC-01 -> Phase 1
- SEC-02 -> Phase 1
- SEC-03 -> Phase 1
- CHAT-01 -> Phase 2
- CHAT-02 -> Phase 2
- CHAT-03 -> Phase 2
- RSV-01 -> Phase 3
- RSV-02 -> Phase 3
- RSV-03 -> Phase 3
- RSV-04 -> Phase 3
- KNOW-01 -> Phase 4
- KNOW-02 -> Phase 4
- KNOW-03 -> Phase 4
- CHAT-04 -> Phase 4
- ANA-01 -> Phase 5
- ANA-02 -> Phase 5
- ANA-03 -> Phase 5

Coverage check: 21/21 v1 requirements mapped.

---
Last updated: 2026-03-21





