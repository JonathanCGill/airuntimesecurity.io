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

3. **Map each item** to the relevant AIRS framework controls. Use the tags defined in the news page header. Each item should reference at least one tag. Link to the most relevant framework page where possible.

4. **Write each entry** in this format, inserting new items between the `<!-- NEWS_START -->` and `<!-- NEWS_END -->` markers. Existing entries should remain, newest items go at the top:

```markdown
### YYYY-MM-DD: Title of the news item

**Tags**: Guardrails, Judge, Agentic (whatever applies)

Brief summary of what happened or was published (2 to 4 sentences). Explain why it matters for AI runtime security. Written in a clear, direct tone.

**Framework relevance**: Explain which AIRS controls would have helped, or why this validates part of the framework. Link to the relevant page, e.g. [Controls](core/controls.md) or [Agentic AI Controls](core/agentic.md).

**Source**: [Article title](https://example.com/article)

---
```

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
