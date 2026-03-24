---
description: "Sandbox patterns for agentic AI: containing code-generating agents with execution isolation, file system restrictions, network controls, and resource limits."
---

# Sandbox Patterns for Agentic AI

> **Control Domain:** Agentic - Execution Controls  
> **Purpose:** Contain the execution environment for agents that generate and run code, interact with file systems, or manipulate infrastructure.  
> **Extends:** NET-01 (network zones) and SESS-02 (session isolation) with execution-specific depth.

## The Problem

Code-generating agents (coding assistants, data analysis agents, automation agents) don't just produce text - they produce executable code and then run it. This means a prompt injection or model error can result in:

- Arbitrary code execution on infrastructure the agent has access to.
- File system access (read, write, delete) beyond the intended scope.
- Network requests to unintended destinations.
- Resource exhaustion (CPU, memory, disk, network).
- Persistent changes that outlive the agent session.

The standard controls (guardrails, tool permissions) are necessary but insufficient for code execution. Code is inherently unconstrained - a single line of Python can do anything the runtime environment permits. The sandbox is what limits what "anything" means.

## Control Objectives

| ID | Objective | Risk Tiers |
|----|-----------|------------|
| SAND-01 | Execute agent-generated code in isolated sandbox environments | All (code-gen agents) |
| SAND-02 | Restrict sandbox file system access to declared paths | All (code-gen agents) |
| SAND-03 | Restrict sandbox network access to declared destinations | All (code-gen agents) |
| SAND-04 | Enforce resource limits on sandbox execution | All (code-gen agents) |
| SAND-05 | Prevent persistent state from sandbox escaping the session | Tier 2+ (code-gen agents) |
| SAND-06 | Scan generated code before execution | Tier 2+ (code-gen agents) |

## SAND-01: Isolated Execution Environments

Agent-generated code must never execute in the same environment as the AI system's infrastructure, backend services, or control plane.

### Isolation Levels

| Level | Technology | Use Case |
|-------|-----------|----------|
| **Process isolation** | Separate process with reduced privileges (seccomp, AppArmor) | Low-risk data analysis, read-only operations |
| **Container isolation** | Ephemeral container per execution (Docker, gVisor) | Standard code execution, file manipulation |
| **VM isolation** | Separate virtual machine per execution | High-risk code execution, Tier 3+ systems |
| **Remote sandbox** | Execution on a separate, disposable host | Maximum isolation, untrusted code execution |

### Selection Criteria

| Risk Factor | Lower Isolation OK | Higher Isolation Required |
|------------|-------------------|--------------------------|
| Code reads data only | ✓ | |
| Code writes to file system | | ✓ |
| Code makes network requests | | ✓ |
| Code installs packages | | ✓ |
| Code runs user-provided input | | ✓ |
| Tier 3+ system | | ✓ |

## SAND-02: File System Restrictions

The sandbox must restrict file system access to explicitly declared paths.

### Access Rules

| Access Type | Permitted | Implementation |
|-------------|-----------|----------------|
| **Read** | Declared input directories only | Mount specific directories read-only |
| **Write** | Declared output directory only | Mount a single output directory read-write |
| **Execute** | Pre-installed runtimes only | No package installation without pre-approval |
| **Temp** | Sandbox-local temp directory | Mounted as tmpfs, size-limited |
| **System** | None | No access to /etc, /var, /proc, system binaries |
| **Other sessions** | None | No access to other sandbox instances' file systems |

### What This Prevents

- Agent-generated code reading sensitive files from the host or other sessions.
- Code writing persistent backdoors to the file system.
- Code modifying system configuration or installing persistent software.
- Cross-session data leakage via shared file system paths.

## SAND-03: Network Restrictions

Sandbox network access must be explicitly constrained.

### Default: No Network Access

For most code execution tasks, the sandbox should have **no network access** by default. The agent's tools handle external communication via the authorization gateway (IAM-04) and egress proxy (NET-04). The sandbox itself doesn't need network access.

### When Network Access Is Required

If the code genuinely needs network access (e.g., fetching a dataset from an approved URL), it must be:

- Restricted to declared destinations (allowlist).
- Routed through the egress proxy.
- Protocol-restricted (HTTPS only).
- Rate-limited.
- Logged.

### What This Prevents

- Agent-generated code exfiltrating data to attacker-controlled servers.
- Reverse shells or C2 channels from within the sandbox.
- The sandbox being used as a network pivot to attack internal systems.
- Cryptocurrency mining or other resource abuse via network access.

## SAND-04: Resource Limits

Without resource limits, agent-generated code can cause denial of service through resource exhaustion.

### Limits

| Resource | Limit | Enforcement |
|----------|-------|-------------|
| **CPU time** | Maximum wall-clock time per execution (e.g., 60 seconds) | Kill process on timeout |
| **Memory** | Maximum memory allocation (e.g., 512MB) | OOM-kill on breach |
| **Disk** | Maximum disk usage in output directory (e.g., 100MB) | Write failure on breach |
| **Processes** | Maximum process/thread count (e.g., 10) | Fork failure on breach |
| **File descriptors** | Maximum open files (e.g., 100) | Open failure on breach |
| **Output size** | Maximum output returned to the agent (e.g., 1MB) | Truncate on breach |

### Enforcement

Use OS-level resource controls (cgroups, ulimits) rather than application-level checks. The code being executed is untrusted - application-level limits can be circumvented.

## SAND-05: No Persistent State Escaping Sessions

Code execution within a sandbox must not create persistent state that survives the session.

### Requirements

- Sandbox environments are **ephemeral** - created at execution start, destroyed at execution end.
- Output files are returned to the agent via the authorized path, not left on a shared file system.
- No installed packages, modified configurations, or created users persist beyond the execution.
- Environment variables, process state, and temporary files are destroyed.
- For container-based sandboxes: containers are created from a clean image per execution, never reused.

### What This Prevents

- An attacker using prompt injection to install a persistent backdoor in the execution environment.
- Cross-execution contamination (poisoned output from execution N affecting execution N+1).
- Accumulated state creating a growing attack surface over time.

## SAND-06: Pre-Execution Code Scanning

Before agent-generated code is executed, scan it for dangerous patterns.

### Scanning Targets

| Pattern | Risk | Action |
|---------|------|--------|
| Network calls (`requests`, `urllib`, `socket`, `fetch`) | Data exfiltration | Block unless network access explicitly permitted |
| File system access outside declared paths | Unauthorised read/write | Block |
| Subprocess/shell execution (`os.system`, `subprocess`, `exec`) | Sandbox escape | Block or flag for review |
| Package installation (`pip install`, `npm install`) | Supply chain attack | Block unless pre-approved |
| Encoded/obfuscated code | Evasion attempt | Flag for review |
| Resource-intensive patterns (infinite loops, fork bombs) | DoS | Flag, rely on resource limits as backup |
| Credential patterns in code | Credential exposure | Redact and flag |

### Limitations

Code scanning catches known dangerous patterns but is inherently incomplete - the sandbox resource limits and isolation are the primary controls. Code scanning is defence in depth, not a replacement for sandboxing.

## Why Container Isolation Alone Is Not Enough

Research from the University of Oxford and the UK AI Security Institute demonstrates that frontier LLMs can escape standard container sandboxes when common misconfigurations are present. Their **SandboxEscapeBench** benchmark tested 18 escape scenarios across orchestration, runtime, and kernel layers and found that top-tier models (Opus 4.5, GPT-5) solve easy misconfiguration scenarios at near-100% rates and achieve roughly 40% success on harder runtime and kernel exploits.

This means the controls above are not theoretical. Without proper implementation of SAND-01 through SAND-06, a sufficiently capable model with shell access can discover and exploit weaknesses in its own sandbox. The research also found that models opportunistically discover unintended escape paths, reinforcing that agents will explore beyond intended boundaries.

Container isolation should be treated as one layer of defence, not the only layer. Token budgets and retry policies are also security-relevant: inference-time compute scales escape probability roughly log-linearly, and many successful escapes cost approximately $1 per attempt.

For the full analysis, see [The Sandbox Escape Problem](../../insights/the-sandbox-escape-problem.md).

## Platform-Neutral Implementation Checklist

- [ ] All agent-generated code executes in isolated sandbox environments
- [ ] Isolation level selected based on risk tier and code capabilities
- [ ] File system access restricted to declared input/output paths
- [ ] Default: no network access from sandbox
- [ ] Network access (when required) allowlisted, proxied, and logged
- [ ] Resource limits enforced at OS level (CPU, memory, disk, processes)
- [ ] Sandbox environments ephemeral - no persistent state across executions
- [ ] Pre-execution code scanning for dangerous patterns
- [ ] Sandbox execution logged with code, output, resource usage, and duration
- [ ] Sandbox escape attempts detected and classified as security incidents

