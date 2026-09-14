---
title: Machine-Readable Control Catalog
description: "Downloadable YAML and JSON of all 80 infrastructure controls, with a documented schema for ingesting them into GRC platforms, SIEM enrichment, and CI/CD policy gates."
---

# Machine-Readable Control Catalog

The 80 infrastructure controls are published as human-readable pages *and* as structured data, so security teams can ingest them programmatically instead of scraping HTML. The catalog is generated from a single source of truth and is byte-identical to the copy on [aisecuredbydesign.io](https://aisecuredbydesign.io/infrastructure/catalog/). airuntimesecurity.io is authoritative.

<div class="grid cards" markdown>

-   :material-code-json: **controls.json**

    ---

    The full catalog as JSON. Best for programmatic ingestion and jq.

    [:octicons-download-24: Download controls.json](controls.json)

-   :material-file-document-outline: **controls.yaml**

    ---

    The same catalog as YAML. Best for config repos and policy pipelines.

    [:octicons-download-24: Download controls.yaml](controls.yaml)

</div>

## What is in it

Every one of the 80 controls, grouped into 11 domains, with the risk tiers it applies to, whether it is agentic, the behavioural layers it supports, and the runtime layer it most directly enables. The top level also carries the risk-tier model and the runtime-layer legend, so a consumer needs no other file to interpret a row.

## Schema

```yaml
catalog: AI Security Infrastructure Controls
version: "1.0.0"          # semver; bump on any control change
as_at: "2026-08-03"
authority: airuntimesecurity.io
license: MIT
risk_tier_model:
  named: [LOW, MEDIUM, HIGH, CRITICAL]
  simplified:              # the Tier 1/2/3 shorthand and its meaning
    "1": { named: [LOW, MEDIUM], meaning: "..." }
    "2": { named: [HIGH], meaning: "..." }
    "3": { named: [CRITICAL], meaning: "..." }
runtime_layers:            # legend for primary_runtime_layer_code
  L1: "Layer 01 - Guardrails (deterministic prevention)"
  L2: "Layer 02 - Model-as-Judge / reviewing (detection)"
  L3: "Layer 03 - Human Oversight (decision)"
  CB: "Circuit Breaker (containment, maps to PACE Emergency)"
total_controls: 80
domains:
  - slug: identity-and-access
    name: Identity & Access Management
    control_count: 8
    controls:
      - id: IAM-04
        title: Constrain agent tool invocation
        tier_applicability: "Tier 2+ (agentic)"   # human-readable
        min_tier: 2                                 # simplified 1/2/3; 1 == all tiers
        agentic: true
        behavioural_layers: [guardrails, model-as-judge, human-oversight]
        primary_runtime_layer: "Layer 01 - Guardrails"
        primary_runtime_layer_code: L1
        reference:
          aisecuredbydesign: "https://aisecuredbydesign.io/infrastructure/controls/identity-and-access/"
          airuntimesecurity: "https://airuntimesecurity.io/infrastructure/controls/identity-and-access/"
```

### Field reference

| Field | Type | Meaning |
|-------|------|---------|
| `id` | string | Stable control ID, e.g. `IAM-04`. Never reused. |
| `title` | string | Short control objective. |
| `tier_applicability` | string | Human-readable tier scope as shown on the control pages. |
| `min_tier` | integer | Lowest simplified tier the control applies to (`1`, `2`, or `3`). `1` means all tiers. |
| `agentic` | boolean | True if the control is specific to agentic (tool-using, code-running, delegating) systems. |
| `behavioural_layers` | list | Which of the three behavioural layers the control supports. Every control supports all three. |
| `primary_runtime_layer` | string | The runtime layer the control most directly enables. |
| `primary_runtime_layer_code` | enum | `L1`, `L2`, `L3`, or `CB`. See the [handoff matrix](../handoff-matrix.md). |
| `reference` | object | Canonical URLs for the control on each site. |

## Using it

=== "GRC ingestion (Python)"

    ```python
    import json, urllib.request

    url = "https://airuntimesecurity.io/infrastructure/catalog/controls.json"
    catalog = json.load(urllib.request.urlopen(url))

    # Flatten to rows for a GRC register.
    rows = [
        {
            "control_id": c["id"],
            "domain": d["name"],
            "objective": c["title"],
            "min_tier": c["min_tier"],
            "agentic": c["agentic"],
        }
        for d in catalog["domains"]
        for c in d["controls"]
    ]
    print(f"Loaded {len(rows)} controls at catalog version {catalog['version']}")
    ```

=== "Scope to your tier (jq)"

    ```bash
    # Every control that applies at Tier 2 or below (HIGH-risk systems).
    curl -s https://airuntimesecurity.io/infrastructure/catalog/controls.json \
      | jq '[.domains[].controls[] | select(.min_tier <= 2) | .id]'
    ```

=== "SIEM enrichment (jq)"

    ```bash
    # Build an id -> primary runtime layer lookup for alert tagging.
    curl -s https://airuntimesecurity.io/infrastructure/catalog/controls.json \
      | jq 'reduce (.domains[].controls[]) as $c ({}; . + {($c.id): $c.primary_runtime_layer_code})'
    ```

=== "CI/CD policy gate (yq)"

    ```bash
    # Fail a pipeline if a service tagged CRITICAL is missing a mandatory control.
    # min_tier is the LOWEST tier a control applies from, so a CRITICAL service
    # inherits every control at or below its own tier, not just the Tier 1 baseline.
    yq '.domains[].controls[] | select(.min_tier <= 3) | .id' controls.yaml \
      | sort > required-controls.txt
    sort implemented-controls.txt > implemented-controls.sorted.txt

    # comm exits 0 whether or not it printed anything, so test the output itself
    # rather than chaining on its status, or the gate reports success while
    # printing the controls that are missing.
    missing="$(comm -23 required-controls.txt implemented-controls.sorted.txt)"
    if [ -n "$missing" ]; then
      echo "Missing mandatory controls for a CRITICAL service:" >&2
      echo "$missing" >&2
      exit 1
    fi
    echo "All mandatory controls implemented."
    ```

## Versioning

The catalog carries a semantic `version`. Any change to a control's ID, tier applicability, or layer mapping bumps the version. Pin to a version in automation and review the [changelog](../../changelog.md) before upgrading. The companion [policy-as-code templates](../policy/README.md) reference these same control IDs.

!!! warning "Do not hand-edit the data files"
    `controls.yaml` and `controls.json` are generated. Edit the source of truth and regenerate so both sites stay identical, rather than editing the published files directly.

!!! info "References"
    - [Infrastructure Controls Reference](../reference.md)
    - [Control Handoff Matrix](../handoff-matrix.md)
    - [Policy as Code: OPA and Kyverno](../policy/README.md)
    - [Glossary and Unified Taxonomy](../../glossary.md)
