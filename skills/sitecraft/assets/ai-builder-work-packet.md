# SITECRAFT AI-builder work packet

## Goal

[One observable outcome.]

## Product surface

- Routes/screens/states:
- Components:
- Data/content:
- User actions:

## Context of use

- Primary user:
- Situation:
- Decision or outcome:
- Trust requirements:

## Current project

- Framework/platform:
- Experience Contract reference/revision:
- Exact project state / build fingerprint when available:
- Files/components to inspect first:
- Existing conventions:
- Current observed state:

## Shared-checkout coordination when applicable

Include this whenever the builder may be working in a shared checkout or ownership is not already proven isolated.

- Workspace mode: isolated / shared / unknown
- Checkout reference:
- Checkout status: not_shared / free / reserved / blocked / revalidate_required
- Current owner when reserved:
- Receiver write policy: allowed_after_revalidation / read_only_until_handoff / blocked
- Coordination/release receipt when a shared checkout is marked free:
- Confirm exact checkout state before write: yes

A clean tree does not prove that another chat or agent has released a shared checkout. Local write permission and checkout ownership are separate checks.

## Capability plan when applicable

Include only consequential capability decisions relevant to this pass.

- Experience need:
- Capability class:
- Selected route and why:
- Rejected route(s) and why:
- Integration boundary / which layer owns what:
- Loading and lifecycle:
- Fallback, including reduced-motion/static behaviour where relevant:
- Performance/accessibility/security risks:
- Evidence required after implementation:

Do not let the builder replace surrounding architecture merely because its preferred stack differs.

## Runtime orchestration when applicable

Include only the ownership/bridge facts that intersect this change.

- Related capability decision IDs:
- Concern + scope + current owner:
- Explicit bridge between systems:
- Shared rules the builder must preserve:
- Prohibited conflicts:
- Cleanup / unmount / route-change / hidden-tab behaviour when relevant:

Do not add a second owner for scrolling, navigation, application state, animation timing, media playback, render loops, focus/input, or another declared concern in the same scope.

## Host / execution profile

Record only what the current builder or agent is confirmed able to do now:

- Inspect project/files:
- Modify with bounded scope/rollback:
- Run declared tests/builds:
- Start or inspect preview:
- Control/inspect browser:
- Capture screenshots:
- Capture/inspect temporal recordings:
- Inspect media:
- Research current official sources:
- Persist project state / handoff:
- Deploy/publish authority:

Use `confirmed`, `unavailable`, or `unknown`. Re-discover this profile after a handoff; do not treat host permissions as part of the website contract.

## Visual grammar

- Dominant idea:
- Typography roles:
- Colour roles:
- Layout rules:
- Imagery treatment:
- Anti-patterns:

## Creative distinction when applicable

Include only the project-specific mechanism(s) touched by this pass.

- Intent: task_specific / brand_distinctive / expressive_flagship
- Concrete project driver(s):
- Mechanism ID + what the mechanism actually does:
- Why it belongs to this project:
- Surface(s) where it is used:
- What it must not drift into:
- Familiar patterns deliberately kept for clarity:
- Relevant reference project-synthesis note(s):
- Anti-repetition rule(s):

Do not describe a library, renderer, animation technique, or media type by itself as the creative concept.

## Asset lineage when applicable

Include only consequential assets touched or consumed by this pass.

- Stable asset ID(s):
- Direct parent asset ID(s), if this output is derived from another artifact:
- Reference asset ID(s), if another asset influences identity/composition without being the direct parent:
- Protected master/source properties:
- Delivery derivative / poster / fallback asset ID(s):
- Asset-ledger reference:
- Existing or required evidence ID(s):

Do not reuse one asset ID for materially different masters, fallbacks, or delivery derivatives when approval, payload, or evidence can differ.

## Image-production boundary when applicable

- Image Generation Pack reference:
- Production job ID(s) touched by this build pass:
- Approved image asset ID(s) the builder must consume unchanged:
- Planned/candidate image asset ID(s) that must not be treated as approved:
- Is this builder authorized to generate or edit imagery for the named job(s), or only to consume supplied assets?:
- If generation/editing is authorized, required source/edit-target asset IDs and bounded reference IDs:
- Host reference-loading capability confirmed?:
- Candidate output location / naming rule:
- Browser/composition evidence required before promotion:

An implementation builder must not recreate, restyle, overwrite, or substitute an approved image master merely because it can generate images. If the current pass only consumes an approved asset, use the supplied artifact. If a separate image-production job is required, follow the Experience Contract production graph and Image Generation Pack rather than improvising a new image inside the website build.

## Behaviour

- Interaction rules:
- Motion purpose:
- Reduced-motion equivalent:
- Focus behaviour:
- Loading/error/success:

## Motion system when applicable

- Scope: interface / motion graphics / hybrid
- Motion depth: Quiet / Polished / Chapter-led / Motion-led
- Motion job and emotional temperature:
- Narrative argument and chapter order:
- For each authored chapter: arrival / transition / readable hold / handoff / reverse / responsive / reduced-motion state:
- Project-specific continuity devices, if any:
- Storyboard beats and stable end state:
- Elements allowed to move:
- Duration, easing, sequence, path, and loop rules:
- Kinetic typography and compositing rules:
- Ambient media: job / route / seam / poster / autoplay / pause / offscreen / hidden-tab / fallback / budget:
- Hero variants: approved set / stable selection policy / equivalent copy, CTA, crop, mobile and fallback:
- Delivery format/runtime and reason:
- Playback, interruption, pause, and offscreen behaviour:
- Reduced-motion and static equivalent:
- Byte, CPU/GPU, memory, energy, and request budgets:
- Source asset lineage and protected artwork:
- Motion screenshots, recordings, variation evidence, and performance evidence:

Do not require a recurring motif. Derive continuity from the specific brief. Do not choose Lottie, dotLottie, Rive, canvas, WebGL, WebGPU, video, or a timeline library before the motion brief and delivery constraints justify it.

## Responsive contract

- Wide:
- Short laptop:
- Intermediate/container state:
- Narrow:
- 320 CSS-pixel reflow:

## Change boundary

Change only:

- [bounded files/components]

Preserve:

- [approved assets, content, behaviour, data, routes, and unrelated files]

Do not:

- redesign unrelated surfaces;
- invent data, testimonials, metrics, claims, routes, or features;
- expose secrets or private content;
- remove accessibility behaviour;
- replace project conventions without explaining a blocking reason.

## Acceptance criteria

1. [Observable result]
2. [Responsive result]
3. [Keyboard/accessibility result]
4. [Performance or stability result]
5. [No-regression result]

## After implementation

Run or report:

- build/type/lint/unit checks:
- browser or end-to-end checks:
- screenshots required:
- recording required:
- accessibility checks:
- performance checks:
- security/public-bundle checks:
- exact changed paths:
- resulting project/build fingerprint when available:
- relevant asset IDs and evidence IDs created/updated:
- remaining unverified states:
- shared-checkout coordination state if work is being handed onward:

Do not claim completion from the code change alone. Report changed paths, tests, evidence, failures, remaining unverified states, and any checkout ownership/release change needed for the next host.
