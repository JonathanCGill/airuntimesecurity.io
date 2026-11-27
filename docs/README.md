---
title: AI Runtime Security (AIRS)
description: "Governance decides what AI should do. MASO verifies what your agents actually do. AIRS is a vendor-neutral, risk-proportionate framework for running AI safely in production: ASO for a single system, MASO for the fleet."
template: redesign.html
nav_active: home
search:
  boost: 2
---

<section class="airs-section airs-hero airs-section--paper airs-section--first airs-center">
  <div class="airs-wrap--narrow">
    <p class="airs-eyebrow airs-eyebrow--accent airs-hero__eyebrow">A framework for running AI safely</p>
    <h1 class="airs-hero__title">Governance decides what AI <em class="is-muted">should</em> do. MASO verifies what your agents <em class="is-accent">actually</em> do.</h1>
    <p class="airs-hero__lead"><strong>Multi-Agent Security Operations</strong> is the heart of AIRS: risk-proportionate runtime controls for systems where many AI agents collaborate, built on the same three layers proven on single systems.</p>
    <div class="airs-btns">
      <a class="airs-btn airs-btn--primary" href="/maso/">Enter MASO &rarr;</a>
      <a class="airs-btn airs-btn--secondary" href="/maso/demo/">&#9654; Try the interactive demo</a>
    </div>
    <p class="airs-fineprint">New to runtime security? <a href="/start/">Start here</a> &middot; Running one model, not a fleet? <a href="/aso/">See ASO</a></p>
  </div>
</section>

<section class="airs-section airs-section--card airs-rd-news" id="in-the-wild">
  <div class="airs-wrap">
    <div class="airs-rd-news__head">
      <div>
        <p class="airs-eyebrow airs-eyebrow--accent">In the wild</p>
        <h2 class="airs-h2">Real agent failures. Would MASO have stopped them?</h2>
        <p class="airs-intro">Every incident on the news page gets a straight answer, the controls that apply, and what MASO would have missed.</p>
      </div>
      <a class="airs-btn airs-btn--secondary" href="/news/">All verdicts &rarr;</a>
    </div>
<!-- NEWS_LATEST -->
  </div>
</section>

<section class="airs-section airs-section--card">
  <div class="airs-wrap">
    <p class="airs-eyebrow">The shift</p>
    <h2 class="airs-h2">One chatbot is one risk. A fleet is a system of risks.</h2>
    <p class="airs-intro">Put fragile agents in a line and the failures don't add up, they multiply.</p>
    <div class="airs-cards">
      <div class="airs-card">
        <p class="airs-card__title">Injection propagates</p>
        <p class="airs-card__body">A poisoned document one agent reads becomes an instruction the next agent obeys.</p>
      </div>
      <div class="airs-card">
        <p class="airs-card__title">Errors compound</p>
        <p class="airs-card__body">One agent's hallucination becomes another's "fact", repeated with confidence instead of caught.</p>
      </div>
      <div class="airs-card">
        <p class="airs-card__title">Privilege goes transitive</p>
        <p class="airs-card__body">If A delegates to B, and B can touch a tool, then A effectively can too. Authority leaks through hand-offs.</p>
      </div>
    </div>
  </div>
</section>

<section class="airs-section airs-section--paper">
  <div class="airs-wrap">
    <p class="airs-eyebrow">One pattern, two scales</p>
    <h2 class="airs-h2">Guardrails prevent. Judge detects. Humans decide. Breakers contain.</h2>
    <div class="airs-scales">
      <a class="airs-scale airs-scale--aso" href="/aso/">
        <p class="airs-scale__label">ASO &middot; Single-agent</p>
        <p class="airs-scale__title">One model, one boundary.</p>
        <p class="airs-scale__body">The three layers and the circuit breaker wrap a single system's input and output. This is the foundation, learn it here, prove it here.</p>
        <span class="airs-scale__more">The ASO foundation &rarr;</span>
      </a>
      <div class="airs-scale__arrow" aria-hidden="true">&rarr;</div>
      <a class="airs-scale airs-scale--maso" href="/maso/">
        <p class="airs-scale__label">MASO &middot; Multi-agent</p>
        <p class="airs-scale__title">Many agents, every hand-off secured.</p>
        <p class="airs-scale__body">The same layers, extended to the space between models: per-agent identity and permissions, epistemic integrity, message-bus security, kill-switch architecture. 11 control domains, 3 tiers, full OWASP dual coverage.</p>
        <span class="airs-scale__more">Enter MASO &rarr;</span>
      </a>
    </div>
  </div>
</section>

<section class="airs-section airs-section--card">
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

<section class="airs-section airs-section--paper" id="roles">
  <div class="airs-wrap">
    <div class="airs-split2">
      <div>
        <p class="airs-eyebrow">For your role</p>
        <h2 class="airs-h2">Three ways in.</h2>
        <div class="airs-stack">
          <a class="airs-minicard" href="/stakeholders/security-leaders/">
            <p class="airs-minicard__title">Set the strategy <span class="airs-minicard__qual">&mdash; security leaders, risk, CIOs</span></p>
            <p class="airs-minicard__body">Is the board confident our agent controls actually work?</p>
          </a>
          <a class="airs-minicard" href="/stakeholders/enterprise-architects/">
            <p class="airs-minicard__title">Design &amp; build <span class="airs-minicard__qual">&mdash; architects, AI engineers</span></p>
            <p class="airs-minicard__body">Where do the controls go, and what do they cost?</p>
          </a>
          <a class="airs-minicard" href="/stakeholders/product-owners/">
            <p class="airs-minicard__title">Own the product <span class="airs-minicard__qual">&mdash; product &amp; business owners</span></p>
            <p class="airs-minicard__body">What do we need in place before we can ship?</p>
          </a>
        </div>
      </div>
      <div>
        <p class="airs-eyebrow">Go deeper</p>
        <h2 class="airs-h2">The thinking behind it.</h2>
        <div class="airs-stack">
          <a class="airs-minicard" href="/reading-paths/">
            <p class="airs-minicard__title">The Golden Thread</p>
            <p class="airs-minicard__body">A guided two-hour path from <em>why runtime security?</em> to <em>how do controls improve?</em></p>
          </a>
          <a class="airs-minicard" href="/insights/">
            <p class="airs-minicard__title">Insights</p>
            <p class="airs-minicard__body">Why guardrails leak, why containment beats evaluation: the failures that force each MASO control into being.</p>
          </a>
          <a class="airs-minicard" href="/news/">
            <p class="airs-minicard__title">News</p>
            <p class="airs-minicard__body">Agentic AI incidents as they break, each with a verdict: prevented, contained, or not prevented by MASO.</p>
          </a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="airs-section airs-section--card">
  <div class="airs-wrap">
    <p class="airs-eyebrow">The lifecycle</p>
    <div class="airs-lifecycle">
      <div class="airs-life airs-life--before">
        <p class="airs-life__title">Before deployment</p>
        <p class="airs-life__body">Which model, which platform, how it ships. <a href="https://aisecuredbydesign.io/">AI Secured by Design &#8599;</a></p>
      </div>
      <div class="airs-life__arrow" aria-hidden="true">&rarr;</div>
      <div class="airs-life airs-life--now">
        <p class="airs-life__title">At runtime &mdash; you are here</p>
        <p class="airs-life__body">AIRS: <a href="/aso/">ASO</a> for one system, <a href="/maso/">MASO</a> for the fleet.</p>
      </div>
    </div>
  </div>
</section>
