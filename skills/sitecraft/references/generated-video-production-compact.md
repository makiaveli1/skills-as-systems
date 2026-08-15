# Generated Video Production — Compact

Use this route when a website genuinely benefits from generated video: an ambient hero loop, product motion study, narrative chapter clip, campaign identity sequence, transition plate, or another bounded web-media role. Do not trigger SITECRAFT for a standalone video with no website use.

## Decide whether video earns its cost

Video is not a prestige default. Prefer still imagery, CSS/WAAPI, SVG, canvas, live 3D, or ordinary footage when they communicate the same thing more clearly or cheaply.

Generate video only when motion over time materially carries atmosphere, story, product behaviour, spatial change, human performance, or another experience need that a still or live interface cannot deliver as well.

Record the decision in the Experience Contract `video_system` and, when technically consequential, link it to `implementation.capability_plan`.

## Choose the cheapest sufficient route first

Before selecting a provider, classify the need:

1. **No generated video** — use a still, CSS/WAAPI, SVG, canvas, live 3D, or sourced footage when it performs the role well enough.
2. **Animate an approved still or identity-critical frame** — prefer an image-conditioned video route so composition, subject or product identity starts from a locked master.
3. **Create a new moving scene with no approved visual anchor** — use a text-conditioned video route only when the scene genuinely benefits from generated motion.
4. **Transform or extend existing moving footage** — use a video-conditioned/editing route only when the live-discovered provider actually exposes one; otherwise fall back to a suitable editing/runtime route instead of pretending the capability exists.

This classification belongs to SITECRAFT's creative plan. Provider availability must not change the creative requirement merely to make a tool usable.

## Map each asset before generation

For every planned clip define:

- website surface and role;
- purpose and message;
- target duration and aspect ratios;
- loop / non-loop behaviour;
- audio policy;
- first-frame requirement, last-frame requirement, and continuity constraints when they matter;
- copy-safe or crop-safe regions;
- reference assets and exactly what each reference controls;
- poster / static / reduced-motion equivalent;
- delivery and performance budget;
- acceptance rubric;
- generation provider only after the host discovers what is available.

A reference should have one bounded role where possible: identity, environment, composition, palette/material, lighting, motion, camera, rhythm/audio, exclusion, or other. State what must be ignored when a reference contains unrelated details.

## Prompt in director form

For complex generation use this order:

1. mode / duration / aspect ratio;
2. reference-role map;
3. scene and subject;
4. action and physical motion;
5. camera behaviour;
6. shot or timing map;
7. audio when relevant;
8. visual-quality and preservation constraints;
9. avoid list.

For multi-shot clips, define shot durations, framing, viewpoint, camera movement, transition logic, and the energy arc. Name one signature moment only when the concept genuinely needs it. Prefer concrete visual results over editing-software jargon.

## Provider inspection and paid generation

Treat provider inspection and generation as separate execution stages when the host can enforce that boundary.

**Stage A — inspect the provider.** After OAuth/tool discovery, use only the provider's non-generating introspection capability needed to learn the current models, arguments, limits or account-specific defaults for this asset. If the host classifies every provider call as consequential, request a narrowly scoped inspection authority that does not authorize generation. Do not call generation merely to discover whether a setting works.

**Stage B — authorize generation.** Only after the exact provider/model/settings can be checked against the asset contract should the host request generation authority for the approved asset and attempt.

Before the first paid attempt declare:

- `max_attempts` — a small bounded number; default 3 when the owner has not set a lower limit;
- whether automatic regeneration is allowed;
- the maximum credit or spend budget when the provider exposes one;
- a bounded provider-interaction budget, including task/status polling;
- which failures permit regeneration;
- which failures require human review or a different route.

For asynchronous jobs, poll only through the provider's status/result capability, respect any provider cadence guidance, and cap status checks per attempt. Do not resubmit generation because a result is still processing.

Never burn credits indefinitely. Repeated generations with no material improvement trigger a stop condition.

## Review → regenerate → accept

After each attempt:

1. save/import the exact artifact and lineage;
2. inspect the actual video, not only its prompt or thumbnail;
3. judge the declared hard floors;
4. record defects with timestamps or deterministic sampled frames where possible;
5. accept only when all hard floors pass;
6. otherwise change the smallest prompt/reference/settings cause that plausibly fixes the defect;
7. regenerate only while the declared attempt and spend budget remains;
8. stop for owner review, fallback, or provider change when the budget is exhausted or improvement stalls.

If the host cannot inspect the video, it cannot autonomously approve or regenerate it. Return a review checklist or hand it to a host that can observe the media.

## Quality floors

Adapt these to the asset, but normally review:

- prompt and story adherence;
- subject / product / identity consistency;
- anatomy, object and geometry stability;
- physically coherent motion;
- camera continuity and framing;
- lighting, palette and material continuity;
- unwanted text, watermarks, logos or artifacts;
- temporal coherence, flicker and morphing;
- loop seam when looping;
- first/last-frame fidelity when supplied;
- copy-safe and responsive crop safety;
- audio presence, sync and appropriateness when audio is intended;
- website payload, codec, dimensions and loading fit;
- reduced-motion / poster equivalent;
- rights, provenance and originality boundaries.

Do not average away a hard failure with a high overall score.

## Provider adapters

The portable core does not require Kling or another generator. A host adapter may expose one.

For Kling MCP, the known endpoint is `https://kling.ai/mcp`. Authenticate through the host's supported OAuth flow, discover the current MCP tools at runtime, and then map those tools to SITECRAFT video needs. Do not hard-code guessed tool names, credentials, model availability, prices, or credit costs into the portable contract.

If Kling is unavailable, use another discovered provider only when it satisfies the same asset contract; otherwise return a portable Video Generation Pack.

## Delivery gate

A generated video is not website-ready merely because the generation looks good. Before integration verify the exact delivered derivative in the real page for autoplay policy, audio control, poster fallback, loading, mobile composition, reduced motion, pause/stop rules where applicable, performance, browser support and owner approval.

See [generated-video-production.md](generated-video-production.md) for the deep workflow.