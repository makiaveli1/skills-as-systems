# Generated Video Production and Review

This module governs AI-generated video that is intended to ship inside a website or web application. It covers asset planning, prompt construction, provider routing, paid-generation control, media review, targeted regeneration, delivery, fallbacks, evidence, and lineage.

It does not turn SITECRAFT into a general video-production skill. A standalone music video, film, social clip, or advertisement with no website use remains outside SITECRAFT unless the user is also designing its web delivery experience.

## 1. Start with the website role

Do not start with a provider or model. Start with the question: what job must moving imagery do here that another medium cannot do as well?

Common justified roles include:

- ambient hero or section loop;
- product behaviour or material transformation;
- spatial reveal that benefits from cinematic motion rather than live 3D;
- chapter-specific narrative footage;
- campaign identity or mood film used as a web surface;
- transition plate between major states;
- bounded background scene that gives a place temporal life;
- human performance where real or generated moving performance is part of the concept.

Common unjustified uses include:

- movement added only to make the page feel expensive;
- a full-screen background that communicates nothing and hurts legibility;
- video replacing a still even though the still would carry the same meaning;
- pre-rendered video replacing useful interactive 3D simply because a video generator is available;
- generated factual or evidentiary footage that could mislead visitors about a real event, person, location, product or service.

When a factual relationship matters, generated footage must be clearly separated from evidence or documentary claims.

## 2. Video asset contract

For every planned asset define, before generation:

- stable asset ID;
- website surface;
- public purpose;
- semantic role;
- target duration;
- master aspect ratio and responsive derivatives;
- loop or finite-play behaviour;
- audio policy: none, ambience, music, dialogue, effects, or mixed;
- subject and identity requirements;
- copy-safe, crop-safe and focal regions;
- first-frame and last-frame requirements;
- continuity requirements that must remain stable across frames, shots, responsive derivatives, and fallback handoffs;
- poster/static fallback;
- reduced-motion equivalent;
- target codec/container and payload budget when known;
- generation route and provider-selection rationale;
- hard acceptance floors;
- maximum paid attempts and budget;
- exact evidence required before integration.

The asset contract should remain useful if the provider changes.

## 3. Reference-role mapping

Multimodal video models work best when references have explicit jobs. Never feed several images or videos into a generator with an instruction equivalent to “use these references.”

Assign each reference one or more bounded roles:

- identity — face, body, product shape, wardrobe, proportions;
- environment — architecture, room, landscape or set;
- composition — framing or spatial arrangement;
- palette/material — colour, surface, fabric, metal, glass or texture;
- lighting — source direction, temperature, contrast and falloff;
- motion — body mechanics, product motion, environmental motion;
- camera — shot size, path, speed, handheld/stabilized character;
- rhythm/audio — pacing, beat, Foley, voice or music relationship;
- exclusion — details specifically not to copy;
- other — narrowly stated contribution.

For each reference record what to preserve and what to ignore. If references conflict, either pick a dominant reference or simplify the stack. Do not make the model resolve a contradiction the creative team has not resolved.

## 4. Prompt construction

### Fast clips

A simple one-shot ambient or product clip can use a compact prompt containing:

- duration/aspect;
- subject + environment;
- precise action;
- camera behaviour;
- lighting/palette/material;
- loop or end-state requirement;
- preservation and avoid rules.

### Director-mode clips

For complex clips use:

1. **Mode/settings** — duration, aspect, audio intent, output style.
2. **Reference map** — what each asset controls and what it must not control.
3. **Scene** — environment, time, light, mood and visual texture.
4. **Subject** — identity, product, wardrobe, expression, posture or geometry.
5. **Action/motion** — physical action, speed, rhythm, environmental motion.
6. **Camera** — framing, viewpoint, lens feel, movement, focus and handoff.
7. **Timing/edit map** — timestamped beats or shot blocks.
8. **Audio** — ambience, music, Foley, speech or silence when supported.
9. **Quality/preservation** — what cannot drift.
10. **Avoid list** — specific unwanted artifacts or model temptations.

### Shot timeline

For multi-shot work, give every shot a bounded duration and purpose. A useful shot block states:

- timestamp;
- shot name;
- visual action;
- camera/framing;
- speed/rhythm;
- visual or physical effect;
- entry/exit transition;
- continuity requirement.

Short-form generated-video work generally benefits from a small number of clear beats rather than overpacked direction. Vary density: a high-energy signature moment usually benefits from a quieter readable hold before or after it.

Treat transitions as authored visual moments when they materially affect continuity. Describe the visual result rather than relying on editing-software terminology.

## 5. Provider and model routing

The provider is an implementation route, not the creative contract.

At execution time discover what the current host can actually use. Compare available providers/models against the asset requirements:

- text-to-video vs image-to-video;
- reference/element consistency;
- first/last frame control;
- multi-shot control;
- maximum duration;
- aspect ratios and resolution;
- native audio;
- downloadable artifact access;
- usage/credit cost when exposed;
- rights and account constraints;
- ability to re-run with controlled changes.

Kling is one optional adapter. The current official endpoint is `https://kling.ai/mcp`. The SITECRAFT project may provide host-specific configuration for it, but the portable core must continue to work without Kling. Complete OAuth interactively in the receiving host, then scan/discover the MCP's actual current tools. Do not invent tool names or persist OAuth credentials in SITECRAFT artifacts.

### Map by semantic capability, not memorized tool names

After live discovery, map the approved asset contract to what the provider currently exposes:

- an approved still, character, product or composition that must anchor the clip → prefer an **image-conditioned video** capability;
- a new scene with no approved visual anchor → consider a **text-conditioned video** capability;
- existing moving footage that must be transformed or extended → require a real **video-conditioned/editing** capability or use another editing route;
- model/argument uncertainty → use a non-generating provider introspection route first when one exists;
- generation status/result retrieval → use the provider's task/status route rather than resubmitting the generation.

If the live catalogue cannot satisfy the asset contract, do not reshape the creative requirement merely to fit the provider. Choose another provider or fall back to a different medium.

## 6. Provider inspection and paid-generation governance

Generated video can consume real credits. Treat provider interaction and generation as bounded external side effects.

### Stage A — provider inspection

After OAuth and live tool discovery, learn the current model/argument requirements through a real non-generating provider introspection capability when one exists. Do not guess model names, defaults or account-specific limits from stale documentation.

When the host classifies every provider tool call as consequential, use a separate narrowly scoped inspection authority. That inspection authority may cover only the exact non-generating introspection calls needed to finish the asset plan; it must not silently authorize generation. If inspection itself can consume credits, disclose that before requesting authority and treat it as spend.

Provider inspection should resolve only what the portable asset contract cannot know in advance, such as:

- currently available models and which generation classes they support;
- required and optional arguments, allowed values and account-tier defaults;
- maximum duration, aspect, resolution, audio or reference constraints;
- provider-reported credit/cost information when reliably exposed.

After inspection, freeze the chosen provider/model/settings for the next attempt or return to planning if the live capability cannot satisfy the asset contract.

### Stage B — generation authority

Before the first paid attempt record:

- `paid_generation`: true/false;
- `max_attempts` — default 3 when the user delegates a bounded experiment and has not selected a lower cap;
- `credit_budget` or equivalent when the provider exposes a reliable unit;
- whether `auto_regenerate` is allowed;
- a bounded provider-interaction budget, including status/result polling;
- failures that permit an automatic second attempt;
- failures that force owner review;
- stop conditions.

Before requesting generation authority, all of these must already be true:

- the website role and chosen generation class are explicit;
- the still/reference master is approved when the route depends on one;
- prompt, reference-role map and timing plan are ready;
- poster/static and reduced-motion fallbacks are defined;
- hard quality floors are written;
- attempt ceiling and spend/credit boundary are declared;
- the host can inspect the returned artifact before autonomous acceptance or regeneration;
- the provider's current live catalogue has been discovered;
- required provider/model arguments have been learned through inspection or another current authoritative source rather than guessed;
- the exact provider/model/settings selected for this attempt have been checked against the asset contract.

Generation authority is the final execution gate, not the moment when creative planning or provider inspection begins.

### Stage C — bounded result polling

Asynchronous generation normally returns a task or generation identifier before the media is ready. Query only that existing task through the provider's status/result capability. Do not submit a second generation merely because the first is still processing.

Set `max_status_polls_per_attempt` before generation. Respect explicit provider cadence guidance when exposed; otherwise avoid rapid repeated polling. Stop polling when the task reaches a terminal state, the poll ceiling is reached, the provider reports an unrecoverable error, or owner review is required. A higher polling ceiling requires new authority when the host counts provider calls.

A provider that does not expose reliable credit consumption can still be used, but SITECRAFT should limit attempts and provider interactions by count and never invent cost numbers.

An increase beyond the declared attempt, interaction or spend budget requires new owner authority.

## 7. Review the actual artifact

A prompt, completion status, thumbnail, or provider “success” message is not creative approval.

The reviewing host must be able to observe the resulting media. Review the full clip when possible. When full playback inspection is unavailable, deterministic frame sampling can support a partial review, but label the unobserved timing/audio portions honestly.

Record:

- exact attempt ID and provider/model when known;
- prompt/reference revision;
- output file identity/hash when locally available;
- duration, dimensions, aspect and audio presence when measurable;
- review method;
- observed defects with timestamps or frame positions;
- hard-floor pass/fail;
- decision: accept, regenerate, fallback, provider-change, or human-review.

## 8. Quality rubric

Do not rely on one vague “looks good” score. Use hard floors plus context-specific judgment.

### Creative and semantic

- Does the clip perform its website role?
- Does the message read without needing prompt knowledge?
- Is the emotional temperature right for the surrounding page?
- Is the signature moment, if one is required, actually legible and memorable?
- Is the footage too busy behind copy or controls?

### Subject and reference fidelity

- identity/product form remains stable;
- proportions and anatomy remain credible;
- wardrobe/material/branding requirements hold;
- first/last frames match when supplied;
- references influence only their assigned roles;
- no unauthorized identity, logo, copyrighted text, watermark or reference residue appears.

### Motion and camera

- physical movement is coherent;
- no unexplained morphing, teleporting, jitter or elastic geometry;
- camera path and framing are intentional;
- cuts or shot handoffs preserve continuity;
- focus behaviour does not distract;
- motion direction complements later website cropping and overlays.

### Temporal integrity

- no visible flicker or temporal instability;
- loop seam is acceptable when the asset loops;
- opening frame loads gracefully with its poster/fallback;
- final state works with the next web state;
- the clip does not rely on continuous motion when reduced motion should receive a still or calmer equivalent.

### Audio

When audio is part of the contract:

- speech, ambience, music and effects are intentional;
- lip-sync or action-sync is acceptable when relevant;
- no unwanted voices/noise appear;
- website autoplay policy is respected;
- visitors can control non-essential audio where appropriate;
- a muted or silent delivery route exists when required by the experience.

### Web delivery

- useful codec/container and dimensions exist;
- master can produce responsive derivatives;
- payload fits the performance budget;
- poster frame is suitable;
- focal/copy-safe areas survive responsive crops;
- mobile behaviour is intentional;
- accessibility and pause/stop rules are met;
- browser support is evidence-backed.

A hard-floor failure cannot be hidden by averaging scores.

## 9. Targeted regeneration

When an attempt fails, diagnose the smallest plausible cause:

- reference-role conflict;
- overloaded prompt;
- unclear action mechanics;
- unsuitable duration;
- insufficient first/last-frame constraint;
- vague camera instruction;
- too many simultaneous subjects;
- inappropriate model/provider route;
- aspect ratio creating composition pressure;
- audio instruction conflicting with visual timing;
- pure model instability.

Then change the smallest responsible variable. Examples:

- keep the scene and identity prompt, but simplify the action;
- keep the action, but replace a conflicting motion reference;
- keep the creative direction, but shorten the clip;
- keep the master shot, but generate a separate mobile derivative rather than forcing one crop;
- preserve all passed dimensions and correct only the failing one.

Do not randomly rewrite the whole prompt after every failure. That destroys lineage and makes improvement impossible to reason about.

## 10. Regeneration stop rules

Stop automatic regeneration when any of these is true:

- `max_attempts` is reached;
- the declared credit/spend budget is reached;
- two consecutive attempts fail the same hard floor with no measurable improvement;
- correcting the defect requires changing the approved concept;
- the provider's output cannot be inspected reliably;
- the generation route produces rights/safety concerns;
- a simpler medium is now clearly the better solution;
- the user requested approval before another paid attempt.

The safe outcome is not always another generation. It may be fallback to an approved still, sourced footage, live CSS/canvas/3D, or human review.

## 11. Video Generation Pack

When the execution host lacks an authenticated generator, produce a portable pack containing:

- asset contract;
- provider-neutral prompt;
- reference-role map;
- shot/timing map;
- audio plan;
- quality rubric;
- avoid list;
- attempt budget;
- review/regeneration rules;
- responsive/crop requirements;
- poster and reduced-motion requirements;
- expected evidence and lineage fields.

A receiving host can map the pack to Kling, Seedance, another provider, or a human production route without rewriting the creative intent.

## 12. Integration into the page

Accepted generation is only a media master. It still has to survive web integration.

Create optimized derivatives rather than shipping an oversized master by default. Test the exact delivered page for:

- preload/autoplay policy;
- muted/default audio state;
- poster behaviour;
- load failure;
- pause and hidden-tab/offscreen behaviour where applicable;
- layout stability;
- text contrast and legibility;
- mobile crop/composition;
- 320 CSS-pixel reflow;
- reduced-motion/static composition;
- network/CPU/GPU cost;
- representative browser engines;
- owner creative approval.

Keep generated-video lineage separate from the runtime delivery derivative.

## 13. Evidence and handoff

Link video evidence to the relevant Capability Plan or video-asset IDs. A handoff should carry the decision IDs, artifact references, accepted/rejected attempt IDs, evidence receipts, blockers and next action — never OAuth credentials, provider cookies, private transcripts, hidden reasoning or inherited permissions.

If a receiving host has Kling configured, it must still rediscover authentication/tool availability and revalidate any paid-generation authority before spending credits.

## 14. Source-derived production principles

SITECRAFT's shot-planning discipline is informed by the supplied video-prompt-builder and CineSeed materials: explicit reference roles, timestamped shot plans, concrete camera/motion direction, effect-density contrast, an intentional energy arc, and targeted failure correction. These are reused as general production principles, not as provider-specific Seedance doctrine.
