---
description: Consistency and accuracy audit of airuntimesecurity.io, focused on factual contradictions, terminology drift, numerical claims, branding, and style-rule violations.
---

# Consistency and Accuracy Audit

*Audit date: 2026-04-14. Scope: 228 markdown files under `docs/`, 6 repo-root markdown files, `mkdocs.yml`, `mkdocs-pdf.yml`, overrides templates, and the `LICENSE`/`pyproject.toml` metadata.*

## Executive summary

| Severity | Category | Finding | Count |
|---|---|---|---|
| Critical | Factual contradiction | "7 domains" vs "ten domains" (MASO) drift across 6 pages | 6 |
| Critical | Factual contradiction | "80 controls" attributed to wrong framework section | 2 |
| Critical | Style rule (CLAUDE.md) | Em-dashes in prose (explicitly forbidden) | 108 in .md, 11 in yml/html |
| High | Accuracy drift | LICENSE copyright year stale vs site | 1 |
| High | Structural drift | Insights landing page missing articles that exist in nav | 10 |
| High | Brand inconsistency | Framework one-liner definition differs in 4 core pages | 4 |
| Medium | Brand inconsistency | Author name "Jonathan C. Gill" vs canonical "Jonathan Gill" | 2 |
| Medium | Metric staleness | Repo-root README "Tests: 99" badge vs 173 actual test functions | 1 |
| Low | UX inconsistency | Duplicate page H1s | 2 pairs (intentional content, needs renaming) |
| Pass | Branding (AIRS canonical) | No variants ("Airs", "A.I.R.S.", etc.) | 0 violations |
| Pass | Risk tier counts | Four-tier (LOW/MED/HIGH/CRITICAL) and three-tier (1/2/3) explicitly distinguished | 0 contradictions |
| Pass | Stakeholder list | Nav, stakeholders/README, and files all align | 0 contradictions |
| Pass | Contact details | One email, one GitHub, one LinkedIn, consistent everywhere | 0 contradictions |
| Pass | PACE expansion | "Primary, Alternate, Contingency, Emergency" everywhere | 0 contradictions |
| Pass | Red-team scenario count | maso/README claims 16, playbook has RT-01…RT-16 | 0 contradictions |

**Verdict: FAIL.** The site has real factual drift (MASO domain count, Foundation vs Infrastructure attribution) that will actively mislead readers, plus pervasive style-rule violations.

## 1. Critical: factual contradictions

### 1.1 MASO domain count: "7" vs "10"

MASO grew from 7 to 10 control domains. The MASO landing page is up to date; six other pages still describe the old state.

**Authoritative statements (current: 10):**

- `docs/maso/README.md:31` — "The ten control domains, three implementation tiers, and PACE resilience model describe what needs to be true…"
- `docs/maso/README.md:126` — "Ten control domains address specific risk categories…"
- `docs/maso/README.md:136` — "The framework organises controls into ten domains."
- `docs/maso/README.md:282` — "All ten control domains fully implemented."
- `docs/maso/README.md:116` — explicitly acknowledges the drift: *"Seven coloured lines represent the original seven control domains. … Model Cognition Assurance, Agentic Task Contract, and Objective Intent were added after the tube map was created."*

**Stale statements (still say 7):**

| File | Line | Text |
|---|---|---|
| `docs/ARCHITECTURE.md` | 49 | "MASO Framework … 128 controls across **7 domains**, 3 implementation tiers, full OWASP dual coverage" |
| `docs/constraining-agents.md` | 170 | "MASO extends it with **128 controls across 7 domains**, covering identity, data protection…" |
| `docs/core/controls.md` | 158 | "MASO Framework - **128 controls across 7 domains** for agent orchestration" |
| `docs/downloads.md` | 38 | "Includes all **7 control domains (128 controls)**, implementation tiers…" |
| `docs/extensions/regulatory/nist-ir-8596-alignment.md` | 214 | "MASO framework … provides **128 controls across 7 domains** specifically for multi-agent orchestration" |
| `docs/what-is-ai-runtime-security.md` | 76 | (references "128 controls" but implicitly through the old framing) |

**Fix:** Update the six stale statements to "10 domains". Also verify whether the "128 controls" total is still accurate after the three new domains (Model Cognition Assurance, Agentic Task Contract, Objective Intent) were added, or whether that number is now stale too. The MASO README does not name a control count, so the source of truth for "128" is unclear.

### 1.2 "Foundation Framework: 80 controls" — wrong attribution

The 80 controls live in **Infrastructure**, not **Foundations**. `docs/foundations/README.md:110` states this explicitly: *"the [infrastructure](../infrastructure/) section defines how — 80 technical controls across 11 domains."* `docs/foundations/README.md` itself does not claim 80 controls; it describes the behavioural three-layer model (Guardrails / Judge / Human Oversight).

Two pages get this wrong:

| File | Line | Text | Problem |
|---|---|---|---|
| `docs/ARCHITECTURE.md` | 36 | "→ **[Foundation Framework](foundations/)** - 80 controls, risk tiers, implementation checklists" | The 80 controls are in `infrastructure/`, not `foundations/`. |
| `docs/what-is-ai-runtime-security.md` | 75 | "The [Foundation Framework](foundations/) for single-agent deployments (80+ controls)" | Same mis-attribution. |

**Fix:** Either attribute the 80 controls to the Infrastructure section (accurate) or make Foundations literally contain a 80-control catalogue. Based on the Foundations README, the first option is correct.

### 1.3 Framework one-liner drift

Four canonical surfaces define AIRS differently. Pick one and align.

| Surface | Definition |
|---|---|
| `mkdocs.yml:3-5` | "AI Runtime Security (AIRS) — the **discipline of monitoring, controlling, and constraining AI system behaviour** in production environments." |
| `docs/README.md:3` | "AI Runtime Security (AIRS) is a **risk-proportionate framework for reducing harm** caused by organisations' use of AI." |
| `docs/what-is-ai-runtime-security.md:3` | "AI Runtime Security (AIRS) is **the discipline of reducing harm** caused by AI systems during live operation." |
| `docs/what-is-ai-runtime-security.md:14` | "AI Runtime Security is **the practice of identifying, assessing, and treating threats** to the confidentiality, integrity, and availability of AI systems in production." |
| `docs/ABOUT.md:19` | "AI Runtime Security (AIRS) discipline, **the practice of identifying, assessing, and treating threats** to AI system behaviour in production environments." |

Three distinct framings: *discipline of monitoring/controlling*, *risk-proportionate framework for reducing harm*, *practice of identifying/assessing/treating threats*. Readers arriving from different entry points will form different mental models of what AIRS is.

**Fix:** Write one canonical sentence. Put it in the site description, the homepage hero, and the about page. All three should match. Variants on body-copy wording are fine; the headline definition should not vary.

## 2. Critical: style-rule violations (CLAUDE.md)

### 2.1 Em-dashes in prose (CLAUDE.md §1: "Never use em dashes")

Counted after excluding fenced code blocks; 108 in markdown prose plus 11 in yml/html.

| File | Em-dashes |
|---|---:|
| `README.md` (repo root, GitHub-facing) | 35 |
| `docs/sdk/tests.md` | 33 |
| `CONTRIBUTING.md` | 20 |
| `SECURITY.md` | 9 |
| `CODE_OF_CONDUCT.md` | 5 |
| `GOVERNANCE.md` | 4 |
| `docs/sdk/examples.md` | 2 |
| `docs/extensions/technical/distill-judge-slm.md` | (not recounted; earlier scan: 1) |
| `overrides/main.html` | 4 |
| `mkdocs-pdf.yml` | 3 |
| `mkdocs.yml` | 2 |
| `overrides/home.html` | 1 |
| `overrides/partials/header.html` | 1 |
| `overrides/partials/tabs.html` | 1 |

The repo-root `README.md` is the single largest offender. Since CLAUDE.md applies to authored content, all of these are violations.

**Fix:** Global replacement pass. Each ` — ` should become either `, ` (mild break), `: ` (introduction of explanation), `. ` (strong break), or the sentence should be rephrased. Do not use ` -- ` as a substitute, which CLAUDE.md also forbids.

## 3. High: metadata and structural drift

### 3.1 LICENSE year

| File | Year |
|---|---|
| `LICENSE:3` | 2025 |
| `mkdocs.yml:85` | 2026 |
| `mkdocs-pdf.yml:30` | 2026 |

**Fix:** Update `LICENSE` to 2026 (or `2025-2026`, depending on preferred convention).

### 3.2 Insights landing page missing 10 articles

`docs/insights/README.md` indexes 38 of the 48 insight articles on disk. Nav in `mkdocs.yml` includes all 48, so users who land on `/insights/` via the tab will not see these ten:

- `agentic-drift.md`
- `beyond-language-models.md`
- `evaluation-integrity-risks.md`
- `feedback-loops.md`
- `the-agent-supply-chain-crisis.md`
- `the-backbone-problem.md`
- `the-sandbox-escape-problem.md`
- `when-learning-goes-wrong.md`
- `why-containment-beats-evaluation.md`
- `you-dont-know-what-youre-deploying.md`

**Fix:** Add each to the appropriate section of `insights/README.md`. Nav category placement in `mkdocs.yml` tells you which section (Architecture, Threats, Models & Technology, etc.) they belong under.

## 4. Medium: brand and metric consistency

### 4.1 Author name variants

Canonical form is "Jonathan Gill" (20+ occurrences in mkdocs configs, ABOUT.md, infrastructure README, repo-root README, GitHub social handle name, LinkedIn social handle name). Two pages use "Jonathan C. Gill" with middle initial:

- `docs/README.md:162` — `Created by <a href="https://www.linkedin.com/in/jonathancgill/">Jonathan C. Gill</a>`
- `docs/what-is-ai-runtime-security.md:95` — `*[Jonathan C. Gill](https://www.linkedin.com/in/jonathancgill/) contributes to the AI Runtime Security discipline…*`

**Fix:** Drop the middle initial in both places, or add it everywhere else. Pick one, apply globally.

### 4.2 "Tests: 99" badge is stale

- `README.md:5` badge: `Tests-99`
- `tests/` actually contains **173** test functions across 10 test files.

**Fix:** Update the badge to reflect the current count, or remove the badge in favour of a dynamic CI-generated one.

## 5. Low: duplicate H1 titles

Three pairs share the same H1; only one pair is clearly a bug.

| H1 | Files | Assessment |
|---|---|---|
| "Open-Weight Models Shift the Burden" | `docs/core/open-weight-models-shift-the-burden.md` and `docs/insights/open-weight-models-shift-the-burden.md` | **Intentional.** The `core/` version is a 10-line redirect stub. No action needed beyond the redirect itself. |
| "Worked Examples" | `docs/extensions/examples/README.md` (single-agent) and `docs/maso/examples/worked-examples.md` (multi-agent) | Different content, cross-reference each other. **Rename** one to disambiguate: e.g., "Single-Agent Worked Examples" and "MASO Worked Examples". |
| "Agentic AI Controls" | `docs/core/agentic.md` (foundation) and `docs/extensions/technical/agentic-controls-extended.md` (deeper dive) | The extended page opens with "This document extends the control framework…" but the H1 is identical. **Rename** to "Agentic AI Controls (Extended)" or similar. |

## 6. What checked out

Findings that were worth investigating and turned out clean:

- **Site name.** "AI Runtime Security" and "AIRS" are used consistently. No variants ("Airs", "A.I.R.S.", "AI-RS") found.
- **Risk tier counts.** The site maintains two distinct tier models (four-tier risk classification, three-tier implementation/autonomy) and explicitly distinguishes them at `docs/core/risk-tiers.md:158`. Every stakeholder page uses them consistently.
- **Six scoring dimensions.** Every page that references the risk-tier classification dimensions says six. Consistent.
- **MASO implementation tiers.** Tier 1 Supervised / Tier 2 Managed / Tier 3 Autonomous, used consistently everywhere.
- **Red team scenario count.** 16 scenarios (RT-01…RT-16). `maso/README.md:305` claims 16, the playbook has 16. Matches.
- **Stakeholder list.** mkdocs.yml nav and `docs/stakeholders/README.md` agree on nine personas.
- **Contact details.** `feedback@airuntimesecurity.io`, `github.com/JonathanCGill`, `linkedin.com/in/jonathancgill/` — identical in every place they appear.
- **PACE expansion.** "Primary, Alternate, Contingency, Emergency" is used consistently at every expansion site.
- **Package version.** `src/airs/__init__.py` and `pyproject.toml` both say `0.1.9`.
- **Author bio numbers.** "30+ years in IT / 20+ years in enterprise security" — consistent across README, ABOUT, and infrastructure README. (Minor variant: "over 30" vs "30+" — stylistic, not factual.)

## 7. Recommended remediation order

1. Fix the MASO "7 domains" drift (§1.1) and the Foundation/Infrastructure attribution error (§1.2). These are reader-visible factual bugs.
2. Verify whether "128 controls" is still current; if not, update it everywhere it appears.
3. Decide the canonical one-line framework definition (§1.3) and align the four surfaces.
4. Run a global em-dash replacement pass (§2.1).
5. Update the LICENSE year (§3.1).
6. Add the ten missing insight articles to `insights/README.md` (§3.2).
7. Fix author-name variants (§4.1) and the stale test-count badge (§4.2).
8. Disambiguate the duplicate H1 titles (§5).

!!! info "References"
    - [CLAUDE.md project writing rules](./CLAUDE.md)
    - [Previous broken-links audit](./AUDIT-BROKEN-LINKS.md)
