---
title: MASO (Multi-Agent)
description: "Multi-Agent Security Operations (MASO): risk-proportionate runtime controls for systems where many AI agents collaborate. The same three control layers, plus the circuit breaker, now governing what agents do to each other."
template: redesign.html
nav_active: maso
search:
  boost: 3
---

<section class="airs-section airs-hero airs-hero--narrow airs-section--paper airs-section--first">
  <div class="airs-wrap">
    <p class="airs-eyebrow airs-eyebrow--accent airs-hero__eyebrow">MASO (Multi-Agent Security Operations)</p>
    <h1 class="airs-hero__title">When agents work together, trust gets <em class="is-accent">complicated.</em></h1>
    <p class="airs-hero__lead">Multi-Agent Security Operations secures systems where many AI agents collaborate. The same three control layers apply, with the circuit breaker behind them, but now they have to govern what agents do <strong>to each other</strong>.</p>
    <div class="airs-btns">
      <a class="airs-btn airs-btn--primary" href="/maso/demo/">Try the interactive demo &rarr;</a>
      <a class="airs-btn airs-btn--secondary" href="/maso/reference/">Read the full reference</a>
    </div>
  </div>
</section>

<section class="airs-section airs-section--card airs-center">
  <div class="airs-wrap--narrow">
    <figure class="airs-figure">
      <img class="arch-diagram airs-figure__img" src="/images/maso-hero.svg" alt="One chatbot guarded by a single security boundary, versus a fleet of agents each handing work to the next, secured as a system">
      <figcaption class="airs-figure__cap">Securing one chatbot is securing one boundary. Securing a fleet means securing every hand-off between agents.</figcaption>
    </figure>
  </div>
</section>

<section class="airs-section airs-section--paper">
  <div class="airs-wrap">
    <p class="airs-eyebrow">The shift</p>
    <h2 class="airs-h2">One chatbot is one risk. A fleet is a system of risks.</h2>
    <p class="airs-intro">Every agent is fragile in the same ways. Put them in a line and the failures don't add up. They multiply.</p>
    <div class="airs-cards">
      <div class="airs-card">
        <p class="airs-card__label">Injection propagates</p>
        <p class="airs-card__body">A poisoned document one agent reads becomes an instruction the next agent obeys. One foothold spreads down the chain.</p>
      </div>
      <div class="airs-card">
        <p class="airs-card__label">Errors compound</p>
        <p class="airs-card__body">One agent's hallucination becomes another's "fact". Mistakes are repeated with confidence instead of caught.</p>
      </div>
      <div class="airs-card">
        <p class="airs-card__label">Privilege goes transitive</p>
        <p class="airs-card__body">If agent A delegates to agent B, and B can touch a tool, then A effectively can too. Authority leaks through hand-offs.</p>
      </div>
    </div>
  </div>
</section>

<section class="airs-section airs-section--card airs-center">
  <div class="airs-wrap--narrow">
    <p class="airs-eyebrow">The core idea</p>
    <p class="airs-statement">Agents can't police themselves. Something outside the agent has to <em>declare what it should do, constrain what it can do, and judge whether it did the right thing</em>, before an irreversible action is committed.</p>
    <a class="airs-textlink" href="/constraining-agents/">Why agents need external evaluation &rarr;</a>
  </div>
</section>

<section class="airs-section airs-section--paper">
  <div class="airs-wrap">
    <p class="airs-eyebrow">Inside MASO</p>
    <h2 class="airs-h2">Four doors, depending on what you came to do.</h2>
    <p class="airs-intro">MASO is a system, not a checklist. Pick what your deployment needs; consciously deselect the rest.</p>
    <div class="airs-doors">
      <a class="airs-door" href="/maso/understand/">
        <p class="airs-door__label">Understand</p>
        <p class="airs-door__body">The reference, the interactive demo, the anatomy of an agent, the whole framework on one map.</p>
        <span class="airs-door__more">Start with the demo &rarr;</span>
      </a>
      <a class="airs-door" href="/maso/implement/">
        <p class="airs-door__label">Implement</p>
        <p class="airs-door__body">Objective Intent, 11 control domains, three tiers, and integration guides for LangGraph, AutoGen, CrewAI, Bedrock.</p>
        <span class="airs-door__more">Start at Tier 1 &rarr;</span>
      </a>
      <a class="airs-door" href="/maso/operate/">
        <p class="airs-door__label">Operate</p>
        <p class="airs-door__body">PACE resilience, the red-team playbook, and live threat intelligence, how MASO runs, degrades, and fails safe.</p>
        <span class="airs-door__more">How MASO fails safe &rarr;</span>
      </a>
      <a class="airs-door" href="/maso/evidence/">
        <p class="airs-door__label">Evidence</p>
        <p class="airs-door__body">Worked examples, 100-agent and 10k e-commerce stress tests, OWASP mappings, the honest trade-offs.</p>
        <span class="airs-door__more">See the stress tests &rarr;</span>
      </a>
    </div>
  </div>
</section>

<section class="airs-section airs-section--card">
  <div class="airs-wrap">
    <p class="airs-eyebrow">Where to start</p>
    <h2 class="airs-h2">Three concrete first steps.</h2>
    <div class="airs-cards airs-cards--roles">
      <a class="airs-card" href="/maso/demo/">
        <p class="airs-card__title">Try the demo</p>
        <p class="airs-card__body">Watch a multi-agent workflow run, then watch it get attacked. See where each layer catches what the last one missed.</p>
        <span class="airs-card__more">Open the interactive demo &rarr;</span>
      </a>
      <a class="airs-card" href="/maso/reference/">
        <p class="airs-card__title">Read the reference</p>
        <p class="airs-card__body">Every control domain, the OWASP mappings, the tiers, the cost numbers, and the honest trade-offs, in one place.</p>
        <span class="airs-card__more">Read the full reference &rarr;</span>
      </a>
      <a class="airs-card" href="/maso/implementation/tier-1-supervised/">
        <p class="airs-card__title">Pick your tier</p>
        <p class="airs-card__body">Supervised, managed, or autonomous. Start at Tier 1, approve every write, and graduate as you build trust.</p>
        <span class="airs-card__more">Start at Tier 1 &rarr;</span>
      </a>
    </div>
  </div>
</section>

<section class="airs-section airs-section--card airs-center">
  <div class="airs-wrap">
    <p class="airs-eyebrow">Visual navigation</p>
    <h2 class="airs-h2">The whole framework, on one map.</h2>
    <figure class="airs-figure">
      <img class="arch-diagram airs-figure__img" src="/images/maso-tube-map.svg" alt="MASO tube map: coloured lines for control domains, stations for key controls, zones for implementation tiers, and the PACE river running through the centre">
      <figcaption class="airs-figure__cap">Lines are control domains, stations are key controls, zones are tiers, and the PACE river runs through the middle.</figcaption>
    </figure>
  </div>
</section>

<section class="airs-section airs-section--ink airs-center">
  <div class="airs-wrap--narrow">
    <p class="airs-eyebrow">Go deeper</p>
    <h2 class="airs-cta__title">Ready for the full picture?</h2>
    <p class="airs-cta__body">The reference has every control domain, the OWASP mappings, the tiers, the cost numbers, and the honest trade-offs.</p>
    <div class="airs-btns">
      <a class="airs-btn airs-btn--primary" href="/maso/reference/">Read the full reference &rarr;</a>
      <a class="airs-btn airs-btn--secondary" href="https://airuntimesecurity.co.za">Learn MASO step by step</a>
    </div>
  </div>
</section>

<section class="airs-section airs-section--card airs-center">
  <div class="airs-wrap--narrow">
    <p class="airs-eyebrow">Where MASO stops</p>
    <p class="airs-statement">MASO governs the agents you run: what they reach, what they do, and how they are stopped. Patching, the SOC, model safety, and risk acceptance belong to other functions. MASO <em>specifies and verifies</em>; it rarely implements.</p>
    <a class="airs-textlink" href="/core/scope-and-responsibilities/">Scope, boundaries, and the RACI &rarr;</a>
  </div>
</section>

<section class="airs-section airs-section--paper airs-center">
  <div class="airs-wrap--narrow">
    <p class="airs-eyebrow">Not running a fleet yet?</p>
    <p class="airs-statement">If you run one AI system today, the foundation is <em>ASO</em>: the same three layers and circuit breaker, wrapped around a single boundary. Learn it there, and you are already learning MASO.</p>
    <a class="airs-textlink" href="/aso/">The ASO foundation &rarr;</a>
  </div>
</section>

<section class="airs-section airs-section--card airs-center">
  <div class="airs-wrap--narrow">
    <p class="airs-eyebrow">Disambiguation</p>
    <p class="airs-intro">MASO (Multi-Agent Security Operations) is a component of the AIRS framework. It is not affiliated with, endorsed by, or related to the Monetary Authority of Singapore (MAS).</p>
  </div>
</section>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "DefinedTerm",
  "name": "MASO",
  "alternateName": "Multi-Agent Security Operations",
  "description": "MASO (Multi-Agent Security Operations) is a component of the AIRS (AI Runtime Security) framework. It provides risk-proportionate runtime security controls for systems where multiple AI agents collaborate. MASO is not affiliated with, endorsed by, or related to the Monetary Authority of Singapore (MAS) or any monetary authority.",
  "inDefinedTermSet": "https://airuntimesecurity.io/maso/",
  "url": "https://airuntimesecurity.io/maso/"
}
</script>
