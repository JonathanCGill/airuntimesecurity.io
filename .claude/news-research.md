# AI Runtime Security News Research

You are updating the AI Runtime Security News page at `docs/news.md`.

## Your task

1. **Search** for recent news, articles, research papers, blog posts, and incident reports related to AI runtime security from the past two weeks. Focus on:
   - AI security incidents (prompt injection, jailbreaks, data leakage, agent misuse)
   - New AI safety and security research
   - Regulatory developments affecting AI runtime controls
   - Platform and vendor security announcements (guardrails, filters, model cards)
   - Agentic AI security developments
   - Multi-agent system risks and controls
   - LLM supply chain and model integrity news
   - AI observability and monitoring developments

2. **Select** the 3 to 8 most significant items. Prioritise items that directly relate to runtime security (not training-time or general AI ethics unless they have runtime implications). Apply strict source quality filters (see below).

3. **Decide the MASO verdict** for each item before writing it. Judge it for an organisation that has implemented the named controls as specified, and be conservative:
   - Incidents and vulnerabilities get a **MASO verdict**:
     - `Prevented` (admonition type `success`): the named controls break the attack chain before harm.
     - `Contained` (`warning`): the first step still happens, but the controls limit what it reaches or stop it early.
     - `Not prevented` (`danger`): MASO would not have stopped it. Say so plainly in the first sentence. Do not soften it, and do not list controls as if they would have helped when they would not.
   - Research, guidance, reports, and product launches get a **MASO coverage** rating: `Covered` (`success`), `Partly covered` (`warning`), or `Not covered` (`danger`), depending on whether MASO already specifies what the item calls for.
   - Only cite control IDs that exist in `docs/maso/controls/*.md` (they are defined in table rows as `| **IA-2.7** Name |`). Read the control before citing it. Never invent a control.
   - If an item reveals a gap that a later framework change closed, add a **Framework change** line.
   - Every verdict ends with an **Owned by** line naming who owns what MASO does not cover. Use the functions in `docs/core/scope-and-responsibilities.md` and link the matching anchor (`#vulnerability-management`, `#vendors`, `#enterprise-identity`, `#security-operations`, `#model-providers`, `#platform-engineering`, `#data-governance`, `#risk-and-compliance`), or `#roles` for the agent owner or AI security. Apply that page's three-question boundary test. If nobody owns the gap, write "Nobody yet. This is an open gap in MASO." rather than assigning it to someone it does not fit.

4. **Write each entry** in this format, inserting new items directly after the `<!-- NEWS_START -->` marker. Existing entries remain; newest items go at the top:

```markdown
### YYYY-MM-DD: Title of the news item

**Tags**: Guardrails, Judge, Agentic (whatever applies)

Summary of what happened or was published (2 to 4 sentences), with dates, versions, CVEs, and the people responsible.

!!! danger "MASO verdict: Not prevented"
    **MASO would not have prevented this.** One or two sentences saying why, in plain terms.

    | Failure point | MASO control | Effect |
    |---|---|---|
    | What went wrong at this step | [IA-2.7 Vaulted per-flow credential brokering](maso/controls/identity-and-access.md) | What the control does about it, honestly |
    | Another step | None | Say "None" where no MASO control applies |

    **Not covered**: What MASO would not have caught, and where that belongs instead if known.

    **Owned by**: [Vulnerability management and application security](core/scope-and-responsibilities.md#vulnerability-management).

**Framework relevance**: The fuller reasoning. Link the relevant emerging threat (`maso/threat-intelligence/emerging-threats.md#et-...`), incident tracker entries, and insights pages.

**Source**: [Article title](https://example.com/article) &middot; [Second source](https://example.com)

---
```

The verdict block is parsed at build time (`hooks/news.py`) to feed the home page, the control pages, and the Atom feed, so keep its shape exactly: the `!!!` line with `MASO verdict:` or `MASO coverage:`, a bold first sentence, the three-column table, and the **Not covered** line. Run `python .github/scripts/check-news.py` after editing; it must pass.

## Source quality

Only include items from credible, verifiable sources. Prefer:

- Peer-reviewed research and preprints from known institutions (e.g. arXiv, USENIX, IEEE, ACM)
- Official advisories and announcements from platform providers
- Reporting from established outlets (e.g. The Record, Krebs on Security, Ars Technica, Wired, MIT Technology Review)
- Government and standards bodies (NIST, CISA, ENISA, OWASP)
- Reputable security research blogs (e.g. Trail of Bits, Google Project Zero, company engineering blogs with technical depth)

Do **not** include:

- Vendor marketing or product announcements disguised as news
- Alarmist, sensationalist, or hype-driven coverage
- SEO content farms or AI-generated aggregator sites
- Sources that lack named authors, citations, or technical detail
- Social media posts or unverified claims without corroborating evidence

When summarising, stick to the facts. Do not editorialize or inflate the significance of an item. If a story is only covered by low-quality sources, skip it.

## Writing guidelines

- Never use em dashes or double hyphens. Use commas, colons, full stops, or rephrase instead.
- Write like a human. Match the existing tone of the site.
- Bold for key terms, backticks for code and config, italics for citations.
- Keep summaries concise. Two to four sentences per item.
- Use the exact tag names from the table in `docs/news.md`.
- Always credit the people behind the work. Name researchers, authors, and teams responsible. For example: "Researchers at Trail of Bits, led by *Jane Smith*, found..." or "A paper by *Doe et al.* from Stanford..."

## Framework reference

The AIRS framework has four core layers:

1. **Guardrails**: containment boundaries that block known-bad inputs/outputs (~10ms)
2. **Judge**: Model-as-Judge evaluation for unknown-bad detection (~500ms to 5s)
3. **Human Oversight**: escalation paths for ambiguous cases
4. **Circuit Breaker**: stops all AI traffic on control failure (PACE methodology)

Plus domain-specific controls: IAM, Agentic, MASO, Supply Chain, Multimodal, Memory & Context, Observability, Data Protection, Risk Tiers.

Key framework pages to link to:
- Architecture: `ARCHITECTURE.md`
- Controls: `core/controls.md`
- Risk Tiers: `core/risk-tiers.md`
- Agentic: `core/agentic.md`
- Multi-Agent: `core/multi-agent-controls.md`
- MASO: `maso/README.md`
- Judge Assurance: `core/judge-assurance.md`
- IAM Governance: `core/iam-governance.md`
- Memory & Context: `core/memory-and-context.md`
- Supply Chain: `maso/controls/supply-chain.md`
- Observability: `maso/controls/observability.md`
- Data Protection: `maso/controls/data-protection.md`

## After updating

- Do not commit or push. The CI workflow handles git operations after you finish.
