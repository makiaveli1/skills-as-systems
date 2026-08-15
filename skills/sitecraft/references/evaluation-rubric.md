# SITECRAFT evaluation rubric

Use the rubric to compare a build with its Experience Contract. Scores guide diagnosis; release decisions are controlled by floors and evidence.

## Scoring

Score each area from 0 to 5:

- `0` — absent, inaccessible, unsafe, or fundamentally incompatible with the contract;
- `1` — severe failure requiring redesign or major rework;
- `2` — material weakness with user or production consequences;
- `3` — functional baseline with identifiable limitations;
- `4` — strong, coherent, and evidenced;
- `5` — exceptional for the project’s purpose, with no material unresolved weakness.

Do not award a high score without named evidence. Begin with blocking floors and observed defects, then use scores to summarize what the evidence already supports. When review independence matters, record review provenance; a self-review, fresh-context pass, or automated check must not be described as an independent review.

## Areas

### Purpose and trust

Does the experience make its purpose, audience, outcome, material conditions, proof, and next action clear without manipulation or invented claims?

### Experience architecture

Do routes, surfaces, states, navigation, content hierarchy, journeys, and recovery paths support the real task?

### Distinctive visual grammar

Is there one explainable visual idea expressed through type, colour roles, layout, density, imagery, components, and deliberate exceptions rather than generic AI patterns? When distinction is consequential, can its key mechanisms be traced to concrete project drivers rather than a prior SITECRAFT showcase, an external reference, or the availability of a fashionable runtime? Are familiar interaction patterns kept deliberately where they protect clarity instead of being reinvented for novelty?

### Content and discoverability

Is content accurate, owned, useful, crawlable where intended, correctly described by metadata, and designed for missing, stale, social, and localized states?

### Responsive composition

Are wide, standard, short-height, intermediate, narrow, zoomed, and 320 CSS-pixel states intentionally composed with protected content and artwork?

### Interaction and motion

Are state changes understandable, keyboard and touch operable, interruptible, performant, and supported by a deliberate reduced-motion equivalent?

### Accessibility

Do semantics, names, focus, keyboard paths, contrast, targets, forms, alternatives, reflow, language, motion, and assistive-technology checks meet the declared target?

### Performance

Do loading, LCP, INP, CLS, JavaScript, media, fonts, third parties, and animation stay within project budgets under representative conditions?

### Security and privacy

Are public/private boundaries physical and enforceable, with secrets, authorization, input, output, browser policy, third parties, and production leakage reviewed?

### Maintainability and ownership

Does the implementation respect project conventions, minimise dependency and abstraction cost, preserve source ownership, document tokens and assets, and support bounded rollback?

### Evidence quality

Do screenshots, recordings, tests, traces, scans, receipts, exact-state identity, environment-matrix rows, and approval cover the claims being made and remain current? Are operating-system, browser-engine, input, assistive-technology, and capture-provider claims scoped to the environments actually observed?

## Blocking floors

The following block release regardless of average score:

- purpose or primary task below `3`;
- accessibility below the declared legal or project requirement;
- known critical security or privacy failure;
- private or secret material in the public build;
- primary responsive journey failing at a required composition;
- missing keyboard access to an essential action;
- unresolved data loss, payment, authentication, or irreversible-action failure;
- material content fabrication or rights uncertainty;
- no trustworthy exact-state identity;
- required implementation, visual, interaction, or release evidence missing;
- owner approval absent for an action that requires it.

## Integration veto

Fail the integrated review when systems contradict each other, for example:

- the visual concept hides the primary content;
- responsive changes remove the conversion or recovery path;
- motion breaks focus, history, performance, or reduced-motion behaviour;
- generated artwork cannot survive the declared crops;
- SEO metadata describes a different page than the visible content;
- the component system cannot express required states;
- client architecture exposes data the security boundary declares private;
- an AI-builder repair fixes one viewport by breaking another;
- a screenshot is approved after the implementation has changed.

## Readiness states

Use:

- `concept_only` — direction exists; no implementation evidence;
- `buildable` — contract is sufficient to implement;
- `implemented_unverified` — code exists; observation is incomplete;
- `repair_required` — one or more material failures exist;
- `ready_for_owner_review` — all blocking checks pass; owner decision remains;
- `approved_for_release` — owner approved the exact verified state;
- `released_verified` — deployment matches the approved artefact and post-release checks pass.

## Review output

Report:

- exact project/build and contract revision;
- evidence scope and gaps;
- score and rationale per area;
- blocking floors;
- defects ordered by user consequence and risk;
- strengths worth preserving;
- smallest coherent repair plan;
- stale evidence created by the repair;
- readiness state and next authority required.

Do not average away a failed floor. Do not use a rubric to manufacture false precision from weak evidence.
