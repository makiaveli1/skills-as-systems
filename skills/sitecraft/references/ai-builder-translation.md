# AI-builder translation

Use AI website builders as implementation environments with different strengths, limits, context models, and pricing. Keep the Experience Contract provider-neutral.

## Builder-neutral sequence

1. **Plan** — define product surface, users, context of use, outcome, constraints, taste, architecture, and evidence.
2. **Foundation** — establish routes, real content shape, tokens, global layout, and protected assets.
3. **Component passes** — build one meaningful component family or surface at a time.
4. **Interaction passes** — add state, data, forms, navigation, motion, and error handling separately.
5. **Responsive passes** — review and correct named compositions rather than saying “make responsive.”
6. **Test passes** — run browser, accessibility, visual, and build checks after the change is stable.
7. **Hardening** — inspect secrets, public bundles, metadata, dependencies, deployment, and rollback.

Do not ask the builder to create a large feature, redesign the whole product, and test everything in one prompt.

## First-build packet

A strong first prompt should include:

### Product surface

Name the actual routes, components, data, and actions. Avoid vague requests such as “make a modern dashboard.”

### Context of use

State who uses it, in what situation, and what decision or outcome they need.

### Constraints and taste

State:

- framework or platform constraints;
- device and input priorities;
- accessibility target;
- visual concept and anti-patterns;
- real or realistic content requirements;
- responsive expectations;
- protected assets;
- performance and privacy boundaries.

### Acceptance

State what must be visible or operable in the first build and what must not be invented.

## File-bounded change packet

For an existing project, provide:

- objective;
- Experience Contract reference/revision and exact project/build state when available;
- exact files or components to inspect first;
- observed current behaviour;
- requested change;
- shared-checkout coordination/write policy when the workspace is shared or ownership is unknown;
- relevant stable asset IDs when consequential media is touched;
- protected behaviour and styling;
- acceptance criteria;
- responsive and accessibility states;
- tests/evidence to produce after implementation;
- instruction not to modify unrelated areas.

When the builder can inspect the codebase, ask it to report its understanding before a risky change. Use plan or discussion mode when available.

## Visual references

Assign a role to each reference:

- information architecture;
- composition;
- type scale;
- colour system;
- interaction;
- motion;
- image treatment;
- component behaviour.

State what must not be copied. Reference mechanisms, not protected expression.

When `visual_grammar.creative_distinction` is relevant to the current pass, carry only the affected mechanism IDs and their concrete project drivers, project reasons, surfaces, drift guards, familiar patterns deliberately kept, and any relevant reference `project_synthesis`. A library, renderer, media type, or animation technique is an implementation route, not the creative concept by itself.

## Real content

Use real or representative content early. Placeholder copy hides hierarchy, overflow, localisation, empty-state, and trust problems.

For data products, define field names, ranges, missing data, statuses, and actions. For marketing sites, provide actual positioning, proof, offers, and objections.

## Capability decisions

When the current pass introduces a consequential runtime, library, framework feature, renderer, media system, or cross-runtime bridge, include only the relevant Runtime Capability Plan entries. State which layer owns surrounding navigation, scrolling, timing, state, focus, data and styling; what the builder must not replace; the fallback; and the evidence required after implementation.

When `implementation.runtime_orchestration` is present, include only the scoped owners, explicit bridges, shared rules and prohibited conflicts that intersect the current change. The builder may implement inside that boundary; it may not silently create a second owner for the same concern in the same scope.

Keep the builder's own tool access separate as a Host Capability Profile. A builder that can edit code but cannot inspect a live browser may implement the change, but the visual or temporal gate remains unverified and should be handed to an observing host. Read [capability-palette-and-orchestration.md](capability-palette-and-orchestration.md) and [harness-integration.md](harness-integration.md).

## Asset lineage

When the pass touches consequential media, carry only the relevant `asset_lineage` records: stable asset IDs, direct parents, reference assets, protected master/source properties, delivery/poster/fallback IDs, asset-ledger reference, and required evidence IDs. Keep direct derivation separate from reference influence, and do not reuse one ID for artifacts that can differ in approval, payload, fallback or evidence.

For generated-image work, also carry only the intersecting `image_system.production_jobs` and the Image Generation Pack reference. Make the builder's authority explicit: **consume approved image assets** and **generate/edit new image assets** are different permissions and tasks. A builder must not regenerate an approved master simply because it has an image tool. When it is authorized to execute an image job, it must re-check dependencies, required approved inputs, edit sources, bounded references, reference-loading capability, candidate persistence and the job acceptance gate before generation.

## Shared checkout coordination

When the workspace is shared or ownership is unknown, carry the current handoff `coordination` state into the builder packet. A clean tree does not prove release. Confirm checkout ownership separately from local write permission before changing project files. If the checkout is reserved, blocked or still requires revalidation, keep the builder read-only until the declared handoff condition is satisfied.

## Iteration discipline

Change one or two major variables per pass. Use prompts for logic and structure; use visual editing tools for small spacing, colour, and type adjustments when the platform supports them.

After each pass:

- inspect the changed surface;
- compare with the contract;
- record exact changed paths and the resulting build/project fingerprint when available;
- record relevant asset IDs and evidence IDs created or changed;
- record failures and remaining unverified states;
- if work is handed onward, record the current checkout ownership/release state instead of assuming a clean tree is free;
- issue a repair prompt tied to evidence;
- avoid repeatedly asking “make it better.”

## Failure repair prompt

Use:

```text
Problem observed:
[exact visible or functional failure]

Evidence:
[viewport, screenshot, recording, error, or test]

Change only:
[bounded target]

Preserve:
[approved behaviour, assets, layout, data, and unrelated files]

Acceptance:
[observable result]

Verify after change:
[tests and evidence]
```

## Portability

SITECRAFT outputs should be adaptable to v0, Lovable, Bolt, Replit Agent, Cursor, Claude Code, Codex, or another builder. Use platform-specific features only in an adapter or execution note. Keep the central contract and acceptance criteria independent.

## Cost and context

Do not dump every reference and requirement into every prompt. Maintain a stable project knowledge file where supported, then send the smallest current packet. Repeat critical invariants when drift appears.

Do not assume the builder remembers an earlier conversation, sees local files, or has the same model and feature set as a previous run.
