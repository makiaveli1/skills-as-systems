# Experience Contract

Use the Experience Contract as the canonical agreement for substantial SITECRAFT work. It is not a moodboard, generated prompt, backlog, or design file. It explains what must remain true while strategy, visuals, code, and evidence evolve.

## Contract roles

The contract should answer:

- What is the public purpose of the experience?
- Who is it for, and in what situation?
- What must each important screen or state enable?
- What user and business outcomes matter?
- What content or assets are authoritative?
- What foundations are protected?
- What visual and interaction rules define the experience?
- What device, browser, accessibility, performance, privacy, and deployment constraints apply?
- What must be observed before approval?
- What is approved, provisional, blocked, or unverified?

## Authority order

Use this order when evidence conflicts:

1. explicit user or owner decision;
2. approved Experience Contract revision;
3. protected brand, content, or system foundation;
4. observed project and user evidence;
5. applicable standards and current official platform guidance;
6. project conventions and implementation constraints;
7. references and competitive patterns;
8. model suggestions and generated alternatives.

An AI-generated implementation never silently outranks an approved decision.

## Required sections

### Identity

Record contract ID, project, version, status, owner, target release, and last update.

### Purpose and audience

Record the public purpose, audience, context of use, primary outcome, secondary outcomes, and trust requirements.

### Experience map

Record route or mode inventory, screen/state purpose, primary journeys, conversion or completion path, navigation model, and content hierarchy.

### Visual grammar

Record the dominant visual idea, typography roles, colour roles, spacing/density logic, layout behaviour, imagery treatment, component language, and anti-patterns.

### Behaviour and motion

Record interaction states, transition grammar, scroll rules, motion purpose, reduced-motion equivalents, focus behaviour, loading/error feedback, and prohibited motion.

### Continuity when applicable

Use optional `continuity_system` only when several pages, states, assets, clips, or later agents must preserve the same identity or state logic. Record a small set of named anchors, authoritative state dimensions, family-level checks, and conditions that make dependent work stale. Do not add it to a simple site merely because the field exists.

Use stable typed targets where the contract already has an ID, for example `surface:workshop-detail` or `state:workshop-detail:available`. Free-form scope labels remain valid for concepts that do not map cleanly to one surface or state. Handoffs may carry only the relevant continuity IDs; the Experience Contract remains their authority.

When a visual direction is genuinely unsettled, optional `visual_grammar.direction_selection` can record two or more structurally different experience arguments before convergence. Use `not_needed` when the brief already provides a strong direction. After convergence, reopen the choice only for a named reason such as owner rejection or new evidence that invalidates the selected direction.

### Asset lineage when media crosses systems

For consequential media that moves between image, video, motion, delivery and evidence stages, add the optional `asset_lineage` spine. Keep it deliberately small: stable asset ID, kind/stage, direct parent IDs, reference IDs, external source references, the SITECRAFT systems that use the asset, related capability/evidence IDs, approval state, and the detailed ledger path when one exists.

Use `parent_asset_ids` only for direct derivation such as crop, edit, animation, transcode, poster extraction or web-delivery derivative. Use `reference_asset_ids` when another internal asset influences identity, continuity, composition or another role without being the direct source artifact. Delivered derivatives should normally receive their own IDs when they can have different approval, payload, fallback or evidence states.

The detailed CSV asset ledger remains the production record; `asset_lineage` is the cross-system spine that lets the Experience Contract, image/video/motion systems and evidence point to the same identities. Use [asset-and-media-pipeline.md](asset-and-media-pipeline.md).

### Image system when applicable

For image-led work, add the optional `image_system` section. Record whether imagery is sourced, generated, or mixed; the website role of each asset; bounded reference roles; production stages; generation or human routes; and, when several generated/edited assets have ordering or source dependencies, an optional execution policy plus `production_jobs` graph that distinguishes generate from edit, prerequisites, required approved inputs, direct edit sources, reference IDs, persistence and acceptance gates. Then record preservation rules, responsive derivatives, still-to-motion handoff, delivery, accessibility, performance, lineage, and exact evidence. Use [generated-image-production.md](generated-image-production.md) and the portable [Image Generation Pack](../assets/image-generation-pack.md) when execution must move across hosts.

A generated image must have a named website role before production begins. References must declare what they contribute and what must be ignored. Approve the still master before motion or final responsive derivatives. When generation tools are unavailable, the contract should still produce a portable Image Generation Pack.

### Motion system when applicable

For generated or sourced video that will ship inside the website, add the optional `video_system` section. Record each clip's web role, duration/aspect/audio policy, first-frame requirement, last-frame requirement, continuity constraints when they matter, reference-role mapping, poster or reduced-motion fallback, provider-selection strategy, paid-generation attempt/spend boundary, quality hard floors, regeneration stop rules, delivery, lineage and exact evidence. Keep exact provider tools and credentials out of the contract; discover them on the executing host. A paid automatic regeneration loop must always be bounded. Use [generated-video-production.md](generated-video-production.md).

For motion-led work, add the optional `motion_system` section. Record whether the scope is interface motion, motion graphics, or hybrid; choose motion depth; and, only when needed, add narrative chapters, continuity devices, living-media rules, hero-variation rules, temporal grammar, kinetic typography, compositing, delivery format and runtime, playback, accessibility equivalents, performance budget, ownership, and exact evidence. Continuity devices are optional and must be derived from the project rather than imposed as a reusable house motif. Use [motion-design-and-graphics.md](motion-design-and-graphics.md) and [narrative-motion-and-living-media.md](narrative-motion-and-living-media.md).

Do not add a heavy motion system to a site that needs only normal interface feedback. When motion graphics are central, do not hide their production, asset, runtime, or fallback decisions inside vague animation notes.

### Responsive contract

Record supported compositions rather than device names alone. Include wide desktop, short laptop, tablet or intermediate container states, narrow mobile, and 320 CSS-pixel reflow. Define what stacks, moves, collapses, scrolls, persists, or becomes a different interaction pattern.

### Implementation contract

Record architecture choice, project conventions, component and token ownership, data/content sources, public/private boundaries, browser support, dependencies, and change boundaries.

When a technology decision is consequential, add an optional `implementation.capability_plan`. Record the experience need, stable capability class, selected route, reason, credible rejected routes, integration boundary, loading strategy where relevant, fallback, risks, and evidence required. Keep library/framework names in the replaceable `selected_route` rather than turning them into permanent schema concepts. When several consequential runtimes interact on the same surface or concern, add optional `implementation.runtime_orchestration` with scoped ownership, explicit bridges, shared rules and prohibited conflicts. The host's own tools and permissions do not belong in these plans; discover those separately as a Host Capability Profile. Use [capability-palette-and-orchestration.md](capability-palette-and-orchestration.md).

### Evidence contract

Record required screenshots, recordings, browser tests, accessibility checks, performance checks, security checks, visual baselines, reviewers, and evidence freshness. When evidence proves a consequential media asset, carry its stable `asset_id` into the evidence matrix `asset_ids` field so proof for a source master, fallback, responsive derivative or delivered web asset cannot be confused.

When the support promise spans multiple operating systems, browser engines, input methods, or assistive-technology stacks, add `environment_matrix` rows. Each row records the exact environment, status, evidence, and limitations. Keep `implementation.browser_support` as the intended promise and `evidence_contract.environment_matrix` as observed proof. Use `support_claim_rule` to state that one environment cannot verify another. See [platform-and-browser-portability.md](platform-and-browser-portability.md).

### Release state

Use one of:

- `draft` — direction exists but implementation or evidence is incomplete;
- `buildable` — decisions are sufficient to implement;
- `implemented_unverified` — code exists but required observation is missing;
- `review` — evidence exists and owner review is pending;
- `approved` — owner approved the exact evidenced state;
- `blocked` — a named issue prevents progression;
- `released` — exact approved state was deployed and release evidence exists.

## Revision rule

Change the contract when a decision changes, not whenever a note is added. Preserve revision history. Record:

- previous revision;
- changed fields;
- reason;
- evidence;
- decision authority;
- whether earlier screenshots, baselines, or approvals are stale.

## Small-task fallback

For a bounded repair, use a compact contract containing:

- problem;
- expected state;
- protected state;
- files or components in scope;
- acceptance criteria;
- evidence required.

Do not create bureaucracy for a one-line fix, but do not make unbounded changes without an explicit contract.
