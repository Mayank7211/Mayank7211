---
phase: 1
slug: secure-onboarding-foundation
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-21
---

# Phase 1 - Validation Strategy

Per-phase validation contract for feedback sampling during execution.

## Test Infrastructure

| Property | Value |
|----------|-------|
| Framework | pytest |
| Config file | apps/backend/tests/conftest.py |
| Quick run command | python -m pytest apps/backend/tests/test_tenant_authz.py apps/backend/tests/test_cors_policy.py -q |
| Full suite command | python -m pytest apps/backend/tests/test_onboarding_api.py apps/backend/tests/test_upload_api.py apps/backend/tests/test_widget_snippet.py apps/backend/tests/test_tenant_authz.py apps/backend/tests/test_cors_policy.py apps/backend/tests/test_rate_limits.py -q |
| Estimated runtime | 20-60 seconds |

## Sampling Rate

- After every task commit: run the task-level automated command from the map below.
- After every plan wave: run the full suite command.
- Before /gsd-verify-work: full suite must be green.
- Max feedback latency target: under 60 seconds for task-level checks.

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirements | Test Type | Automated Command | File Exists | Status |
|---------|------|------|--------------|-----------|-------------------|-------------|--------|
| 1-00-01 | 01-00 | 0 | ONB-01, ONB-02, ONB-03, ONB-04, SEC-01, SEC-02, SEC-03 | scaffold/collect | python -m pytest apps/backend/tests/test_onboarding_api.py apps/backend/tests/test_upload_api.py apps/backend/tests/test_widget_snippet.py apps/backend/tests/test_tenant_authz.py apps/backend/tests/test_cors_policy.py apps/backend/tests/test_rate_limits.py --collect-only -q | yes (produced in plan) | pending |
| 1-01-01 | 01-01 | 1 | SEC-01 | api/security | python -m pytest apps/backend/tests/test_tenant_authz.py -q | yes (from 01-00) | pending |
| 1-01-02 | 01-01 | 1 | SEC-02 | api/security | python -m pytest apps/backend/tests/test_cors_policy.py -q | yes (from 01-00) | pending |
| 1-02-01 | 01-02 | 2 | ONB-01, ONB-04 | api/schema | python -m pytest apps/backend/tests/test_onboarding_api.py apps/backend/tests/test_widget_snippet.py -q | yes (from 01-00) | pending |
| 1-02-02 | 01-02 | 2 | ONB-02, ONB-03, SEC-03 | api/limits | python -m pytest apps/backend/tests/test_upload_api.py apps/backend/tests/test_rate_limits.py -q | yes (from 01-00) | pending |
| 1-03-01 | 01-03 | 3 | ONB-01, ONB-02, ONB-03, ONB-04 | frontend/build | npm --prefix apps/frontend run build | n/a | pending |
| 1-03-02 | 01-03 | 3 | ONB-01, ONB-02, ONB-03, ONB-04, SEC-01, SEC-02, SEC-03 | backend/tests | python -m pytest apps/backend/tests/test_onboarding_api.py apps/backend/tests/test_upload_api.py apps/backend/tests/test_widget_snippet.py apps/backend/tests/test_tenant_authz.py apps/backend/tests/test_cors_policy.py apps/backend/tests/test_rate_limits.py -q | yes | pending |
| 1-03-03 | 01-03 | 3 | ONB-01, ONB-02, ONB-03, ONB-04, SEC-01, SEC-02, SEC-03 | phase gate | python -m pytest apps/backend/tests -q; npm --prefix apps/frontend run build | yes | pending |

## Wave 0 Requirements

- apps/backend/tests/conftest.py
- apps/backend/tests/test_onboarding_api.py
- apps/backend/tests/test_upload_api.py
- apps/backend/tests/test_widget_snippet.py
- apps/backend/tests/test_tenant_authz.py
- apps/backend/tests/test_cors_policy.py
- apps/backend/tests/test_rate_limits.py

## Manual-Only Verifications

All phase behaviors have automated verification.

## Validation Sign-Off

- [x] All tasks have automated verify or explicit Wave 0 dependency.
- [x] Sampling continuity is maintained with no gap in automated checks.
- [x] Wave 0 covers all previously MISSING references.
- [x] No watch-mode flags.
- [x] Feedback latency target is defined.
- [x] nyquist_compliant is true in frontmatter.

Approval: pending
