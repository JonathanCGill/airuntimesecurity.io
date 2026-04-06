---
description: "Why AI runtime security must extend beyond LLMs to cover diffusion models, voice synthesis, video generation, and other non-language AI systems that are entering production."
---

# Beyond Language Models

*The security framework assumes text in, text out. Production AI has moved on.*

Most AI runtime security guidance, this framework included, centres on large language models. Text prompt goes in, text response comes out. Guardrails check both. A Judge evaluates the output. Humans review escalations.

That model of AI is already a subset of what organisations deploy. Diffusion models generate images and video. Voice synthesis models produce speech indistinguishable from human recordings. Code generation models write and execute software. Reinforcement learning agents take actions in the physical and digital world.

Each of these model types creates runtime security challenges that text-centric controls cannot address.

## Diffusion Models: A Different Attack Surface

Text-to-image diffusion models (Stable Diffusion, DALL-E, Midjourney, Imagen) do not process language the same way LLMs do. They operate in a latent space, converting text embeddings into image representations through iterative denoising. This creates a fundamentally different attack surface.

### Inference-time safety bypass

Diffusion models typically include concept-erasure techniques to prevent generating prohibited content. Recent research shows these are brittle. The ADAtk method achieves over 90% success in bypassing safety mechanisms at inference time, without modifying the model weights, by optimising input text embeddings through gradient guidance.

This is the diffusion model equivalent of a jailbreak, but the mechanisms are different. Text-based guardrails that check the prompt cannot see what happens in the latent space. An innocuous-looking text prompt can produce prohibited imagery if the embeddings are crafted to exploit concept-erasure gaps.

### Open-weight models remove safety entirely

For open-source diffusion models, inference guidance methods and safety filters can be manually removed by anyone with access to the weights. This means the safety layer is not a property of the model but a property of the deployment. If your organisation self-hosts a diffusion model, you own the entire safety stack.

### Membership inference

Attackers can determine whether specific images were in the training data by querying the model and analysing error patterns across diffusion timesteps. This creates privacy risks for organisations using diffusion models trained on proprietary or personal data.

### Backdoor attacks

Malicious triggers can be embedded during training that cause the model to produce specific outputs when activated by particular inputs. Unlike LLM backdoors (which produce specific text), diffusion model backdoors produce specific images, making them harder to detect with text-based monitoring.

## Voice Synthesis: The Trust Boundary That Broke

Voice cloning crossed what researchers call the "indistinguishable threshold" in 2025. A few seconds of audio now produces a clone with natural intonation, rhythm, pauses, and breathing. Deepfake-as-a-service platforms make this accessible to anyone.

The security implications for AI systems are specific:

**Voice-authenticated AI interactions.** Call centres, voice assistants, and accessibility interfaces that use voice as an identity signal are now vulnerable. If your AI system trusts that a voice belongs to a specific person, that trust is misplaced.

**Voice agents as attack targets.** AI systems that communicate via voice (phone agents, virtual assistants) can receive deepfaked voice inputs. The agent cannot distinguish a real caller from a synthetic one.

**Voice output as attack vector.** AI systems that generate voice output (text-to-speech, voice assistants) can be used to produce convincing impersonations. A compromised or misdirected voice agent could generate audio that social-engineers downstream humans.

The scale is significant: deepfake volumes grew from roughly 500,000 in 2023 to 8 million in 2025. Documented financial losses from deepfake-enabled fraud exceeded $200 million in Q1 2025 alone.

### What the framework needs

Voice-specific controls should include:

- **Input verification**: for voice-input AI systems, do not treat voice as an authentication factor without independent verification
- **Output labelling**: generated speech should carry metadata indicating synthetic origin
- **Deepfake detection**: runtime detection of synthetic voice in input streams, similar to how the Guardrails layer filters text
- **Human escalation triggers**: when voice interactions involve high-value actions, require non-voice confirmation

## AI-Generated Code: The Vulnerability Factory

AI code generation is now a runtime security concern, not just a developer productivity tool. In March 2026, at least 35 CVEs were directly attributable to AI-generated code: 27 from Claude Code, 4 from GitHub Copilot, 2 from Devin, and 1 each from Aether and Cursor. Research found that 29.5% of Python and 24.2% of JavaScript AI-generated snippets contained security weaknesses.

Common vulnerability types in AI-generated code include SQL injection, improper input sanitisation, hardcoded credentials, and insecure dependency usage.

This matters for runtime security in two ways:

**Agents that write code.** Agentic AI systems that generate and execute code are producing code with known vulnerability rates. The sandbox contains the execution, but if the generated code is deployed to production (as in CI/CD agents), the vulnerabilities propagate.

**Supply chain contamination.** A "Rules File Backdoor" technique was discovered where hidden unicode characters in configuration files for Cursor and GitHub Copilot inject malicious instructions that the AI follows, producing backdoored code that bypasses human review. This is prompt injection targeting the developer's AI assistant.

### What the framework needs

- Treat AI-generated code as untrusted input, even when generated by a trusted model
- Apply SAND-06 (pre-execution scanning) to all AI-generated code, not just sandboxed execution
- For agents in CI/CD pipelines, require security scanning as a gate before generated code merges
- Monitor for the rules-file backdoor pattern: validate configuration files used by AI coding tools

## Video Generation: Emerging but Real

Text-to-video models (Sora, Runway, Pika) are entering production for content creation, marketing, and training material generation. The security surface combines the challenges of image generation (latent-space attacks, concept-erasure bypass) with temporal dynamics (content that evolves over frames to bypass per-frame detection).

Video generation is earlier in the deployment curve than image or voice. But the pattern is clear: the same safety bypass techniques that work on diffusion models for images will transfer to video, with the added complexity of temporal evasion.

## What This Means for the Framework

The three-layer pattern (Guardrails, Judge, Human Oversight) is model-agnostic in principle. In practice, the implementation assumes text.

Extending to non-LLM models requires:

| Layer | Text (current) | Image/Video | Voice | Code |
|-------|---------------|-------------|-------|------|
| **Guardrails** | Text pattern matching, semantic filtering | Content classifiers, concept-erasure verification, NSFW detection | Deepfake detection, speaker verification | Static analysis, vulnerability scanning |
| **Judge** | LLM-based evaluation | Multimodal model evaluation, human review for ambiguous content | Voice authenticity scoring, intent verification | Security-focused code review (automated and human) |
| **Human Oversight** | Read and assess text | Visual review of generated content | Listen and verify identity claims | Code review with security context |
| **Circuit Breaker** | Output rate, policy violation count | Generation volume, content classifier confidence drops | Voice authentication failure rates | Vulnerability detection rates in generated code |

The architecture extends. The implementations are different.

## Practical Guidance

**Audit your model inventory.** Most organisations deploying AI use more than LLMs. Map every model type in production and assess whether your security controls actually cover it.

**Don't assume text controls transfer.** A guardrail that checks text prompts does not protect against latent-space attacks on diffusion models. Each model type needs controls matched to its actual attack surface.

**Treat voice as untrusted.** Any AI system that accepts or produces voice should treat voice identity as unverified by default.

**Scan AI-generated code.** Apply the same security scanning to AI-generated code that you would apply to code from an untrusted contributor. Automate this in your CI/CD pipeline.

**Plan for convergence.** Multimodal models that combine text, image, voice, and code in a single system will combine all of these attack surfaces. The framework's emerging controls for multimodal systems are the starting point.

!!! info "References"
    - [Adversarial attacks and defenses on text-to-image diffusion models: a survey (Information Fusion, 2024)](https://www.sciencedirect.com/science/article/abs/pii/S1566253524004792)
    - [Attacks and defenses for generative diffusion models: a comprehensive survey (ACM Computing Surveys, 2025)](https://dl.acm.org/doi/10.1145/3721479)
    - [2026 will be the year you get fooled by a deepfake (Fortune, 2025)](https://fortune.com/2025/12/27/2026-deepfakes-outlook-forecast/)
    - [Deepfake-as-a-service exploded in 2025: 2026 threats ahead (Cyble)](https://cyble.com/knowledge-hub/deepfake-as-a-service-exploded-in-2025/)
    - [New vulnerability in GitHub Copilot and Cursor: how hackers can weaponize code agents (Pillar Security)](https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents)
    - [Security weaknesses of Copilot-generated code in GitHub projects (ACM TOSEM, 2025)](https://dl.acm.org/doi/10.1145/3716848)
    - [The security implications of using diffusion models in enterprise AI systems (AIthority)](https://aithority.com/machine-learning/the-security-implications-of-using-diffusion-models-in-enterprise-ai-systems/)
