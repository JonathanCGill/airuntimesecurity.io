---
title: AI Security Infrastructure Controls
description: Infrastructure controls that enforce AI behavioral security across identity, access, logging, network segmentation, and incident response. Select or deselect controls based on your risk tier and organisational context.
template: redesign.html
nav_active: framework
---

<section class="airs-section airs-hero airs-hero--narrow airs-section--paper airs-section--first">
  <div class="airs-wrap">
    <p class="airs-eyebrow airs-eyebrow--accent airs-hero__eyebrow">Infrastructure &middot; The layer underneath</p>
    <h1 class="airs-hero__title">You can't enforce on infrastructure you don't <em class="is-accent">control.</em></h1>
    <p class="airs-hero__lead">The framework tells you <strong>what</strong> to enforce. This layer is <strong>how</strong>: 85 technical controls across identity, logging, network, data, secrets, supply chain, and incident response, each tagged with the risk tiers it applies to.</p>
    <div class="airs-btns">
      <a class="airs-btn airs-btn--primary" href="/infrastructure/reference/">Browse all 85 controls &rarr;</a>
      <a class="airs-btn airs-btn--secondary" href="/infrastructure/mappings/controls-to-three-layers/">See the mappings</a>
    </div>
  </div>
</section>

<section class="airs-section airs-section--card">
  <div class="airs-wrap">
    <p class="airs-eyebrow">The seven questions</p>
    <h2 class="airs-h2">Every control answers one of these.</h2>
    <p class="airs-intro">Behavioral security is only as strong as the infrastructure enforcing it. Each domain answers a question the framework leaves to you.</p>
    <div class="airs-cards airs-cards--roles">
      <a class="airs-card" href="/infrastructure/controls/identity-and-access/">
        <p class="airs-card__title">Identity &amp; Access</p>
        <p class="airs-card__body">Who can reach the model? Authentication, least privilege, control-plane separation, approval workflows.</p>
        <span class="airs-card__more">8 controls &rarr;</span>
      </a>
      <a class="airs-card" href="/infrastructure/controls/logging-and-observability/">
        <p class="airs-card__title">Logging &amp; Observability</p>
        <p class="airs-card__body">How do you know it's working? Model I/O, guardrail and judge decisions, drift detection, SIEM correlation.</p>
        <span class="airs-card__more">10 controls &rarr;</span>
      </a>
      <a class="airs-card" href="/infrastructure/controls/network-and-segmentation/">
        <p class="airs-card__title">Network &amp; Segmentation</p>
        <p class="airs-card__body">What's the blast radius if it fails? Zone architecture, bypass prevention, egress control, gateway enforcement.</p>
        <span class="airs-card__more">8 controls &rarr;</span>
      </a>
      <a class="airs-card" href="/infrastructure/controls/data-protection/">
        <p class="airs-card__title">Data Protection</p>
        <p class="airs-card__body">Where does sensitive data go? Classification, minimisation, PII redaction, access-controlled RAG.</p>
        <span class="airs-card__more">8 controls &rarr;</span>
      </a>
      <a class="airs-card" href="/infrastructure/controls/secrets-and-credentials/">
        <p class="airs-card__title">Secrets &amp; Credentials</p>
        <p class="airs-card__body">How are credentials managed? Context isolation, short-lived tokens, central vault, rotation on exposure.</p>
        <span class="airs-card__more">8 controls &rarr;</span>
      </a>
      <a class="airs-card" href="/infrastructure/agentic/supply-chain/">
        <p class="airs-card__title">Supply Chain</p>
        <p class="airs-card__body">Can you trust the model? Provenance, RAG integrity, tool vetting, AI-BOM, vulnerability monitoring.</p>
        <span class="airs-card__more">8 controls &rarr;</span>
      </a>
      <a class="airs-card" href="/infrastructure/controls/incident-response/">
        <p class="airs-card__title">Incident Response</p>
        <p class="airs-card__body">What happens when things break? AI-specific categories, containment, rollback, post-incident review.</p>
        <span class="airs-card__more">8 controls &rarr;</span>
      </a>
      <a class="airs-card" href="/infrastructure/reference/#agentic-ai-controls">
        <p class="airs-card__title">Agentic controls</p>
        <p class="airs-card__body">Tool access, session &amp; scope, delegation chains, and sandbox patterns for agents that act.</p>
        <span class="airs-card__more">22 more controls &rarr;</span>
      </a>
    </div>
  </div>
</section>

<section class="airs-section airs-section--paper">
  <div class="airs-wrap">
    <p class="airs-eyebrow">Standards &amp; platforms</p>
    <h2 class="airs-h2">Mapped to the standards, ready for the platforms.</h2>
    <p class="airs-intro">Every control maps back to the layered behavioral model and to the standards your auditors already know.</p>
    <div class="airs-cards airs-cards--roles">
      <a class="airs-card" href="/infrastructure/mappings/controls-to-three-layers/">
        <p class="airs-card__title">Standards mappings</p>
        <p class="airs-card__body">ISO 42001 Annex A, NIST AI RMF, SP 800-218A, CSF 2.0, and OWASP LLM &amp; Agentic Top 10.</p>
        <span class="airs-card__more">See the crosswalks &rarr;</span>
      </a>
      <a class="airs-card" href="/infrastructure/reference/#platform-implementation-patterns">
        <p class="airs-card__title">Platform patterns</p>
        <p class="airs-card__body">Reference implementations for AWS Bedrock, Microsoft Foundry, and Databricks.</p>
        <span class="airs-card__more">Implement on your platform &rarr;</span>
      </a>
      <a class="airs-card" href="/infrastructure/reference/">
        <p class="airs-card__title">Full control reference</p>
        <p class="airs-card__body">All 85 controls in detail, the design principles, and the diagram library.</p>
        <span class="airs-card__more">Open the reference &rarr;</span>
      </a>
    </div>
  </div>
</section>

<section class="airs-section airs-section--card airs-center">
  <div class="airs-wrap--narrow">
    <p class="airs-eyebrow">The principle</p>
    <p class="airs-statement">Security is enforced by <em>deterministic infrastructure</em> like gateways, network policy, and vaults, never by prompt instructions that can be overridden. Infrastructure beats instructions.</p>
    <a class="airs-textlink" href="/insights/infrastructure-beats-instructions/">Read the argument &rarr;</a>
  </div>
</section>
