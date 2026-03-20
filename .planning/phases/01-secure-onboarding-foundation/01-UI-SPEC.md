---
phase: 01
slug: secure-onboarding-foundation
status: draft
shadcn_initialized: true
preset: base-nova
created: 2026-03-21
---

# Phase 01 - UI Design Contract

> Visual and interaction contract for frontend implementation in Phase 1.

---

## Design System

| Property | Value |
|----------|-------|
| Tool | shadcn |
| Preset | base-nova (detected from `npx shadcn info`) |
| Component library | shadcn/ui (base-nova, base primitives) |
| Icon library | lucide |
| Font | Body: Trebuchet MS stack (existing). Heading: Book Antiqua/Palatino stack (existing). |

Source notes:
- `01-RESEARCH.md`: React + Vite frontend, no rewrite; extend existing UI.
- `apps/frontend/src/styles.css`: existing typography and palette direction.
- `apps/frontend/components.json`: generated during this run.

---

## Spacing Scale

Declared values (multiples of 4):

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | Icon gaps, inline micro-spacing |
| sm | 8px | Label-to-input spacing |
| md | 16px | Default field and card spacing |
| lg | 24px | Section padding |
| xl | 32px | Inter-panel spacing |
| 2xl | 48px | Major section separation |
| 3xl | 64px | Page vertical rhythm |

Exceptions: Minimum interactive target remains 44px height for icon-only or compact controls.

---

## Typography

| Role | Size | Weight | Line Height |
|------|------|--------|-------------|
| Body | 16px | 400 | 1.5 |
| Label | 14px | 600 | 1.4 |
| Heading | 20px | 600 | 1.2 |
| Display | 28px | 600 | 1.2 |

Contract limits:
- Allowed weights: 400 and 600 only.
- Allowed sizes for this phase: 14, 16, 20, 28.

---

## Color

| Role | Value | Usage |
|------|-------|-------|
| Dominant (60%) | #f4efe4 | Page background and large canvas regions |
| Secondary (30%) | #fff9f0 | Cards, panels, and secondary surfaces |
| Accent (10%) | #0f766e | Primary CTA, focus ring, active onboarding state |
| Destructive | #b42318 | Delete/remove/reject actions and hard errors |

Accent reserved for:
- Primary onboarding CTA button only.
- Focus state ring on active form controls.
- Active step indicator in onboarding flow.

---

## Copywriting Contract

| Element | Copy |
|---------|------|
| Primary CTA | Create Tenant Profile |
| Empty state heading | No onboarding documents yet |
| Empty state body | Upload a PDF, DOCX, or TXT file to personalize your assistant before going live. |
| Error state | We could not complete setup. Fix the highlighted fields or file constraints, then try again. |
| Destructive confirmation | Remove file: Remove this file from onboarding? This action cannot be undone. |

Source notes:
- `1-CONTEXT.md` D-02 and D-08 require clear, actionable, deterministic feedback.
- `ROADMAP.md` success criteria require validation and upload errors to be explicit.

---

## Registry Safety

| Registry | Blocks Used | Safety Gate |
|----------|-------------|-------------|
| shadcn official | button | not required (official registry, verified 2026-03-21) |
| third-party registries | none | n/a |

---

## Checker Sign-Off

- [ ] Dimension 1 Copywriting: PASS
- [ ] Dimension 2 Visuals: PASS
- [ ] Dimension 3 Color: PASS
- [ ] Dimension 4 Typography: PASS
- [ ] Dimension 5 Spacing: PASS
- [ ] Dimension 6 Registry Safety: PASS

**Approval:** pending
