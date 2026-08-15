# Interaction and routing

## Start from the actual task

Classify the request before doing work:

- **Discover** — research the problem, audience, references, category, technology, or standards.
- **Define** — create the Experience Contract, route map, visual direction, or implementation plan.
- **Create** — build a new site, page, component, design system, or prompt packet.
- **Repair** — fix a bounded defect or weak area without redesigning unrelated parts.
- **Review** — inspect a design, codebase, screenshot, recording, or deployed site without changing it.
- **Evolve** — extend an approved system while preserving lineage.
- **Verify** — collect and assess evidence against acceptance criteria.
- **Release** — harden, package, deploy, or prepare the exact approved state for publication.

Choose Sketch, Make, Repair, Audit, or Evolve mode from the task and explain only the consequential choice.

## Inspect before asking

Use available context first:

1. current conversation and explicit owner decisions;
2. supplied screenshots, recordings, designs, briefs, and assets;
3. current project structure, conventions, tests, history, and protected files;
4. existing Experience Contract, tokens, component rules, and approval records;
5. available host capabilities.

Ask only when the answer materially changes purpose, ownership, architecture, public/private boundaries, or the visual direction. When the user delegates judgment, make the decision and record the assumption.

## Preserve authority

Never silently replace:

- approved artwork or brand foundations;
- owner-selected concepts;
- existing user changes;
- production data or content;
- accessibility or security constraints;
- a verified exact state.

When a stronger alternative is needed, explain the weakness and replace it with a concrete option. Do not criticise without a better route.

## Scope control

Before modification, state or record:

- target outcome;
- exact area in scope;
- protected state;
- acceptance criteria;
- evidence required;
- rollback boundary.

A visual redesign request can justify broad change. A spacing fix cannot.

## Artifact depth

Match the contract to the durability of the work.

Use a **compact working contract** for a bounded single surface when one worker can
hold the state safely and there is no long-lived approval, asset lineage,
multi-runtime ownership, or cross-session coordination requirement. Record only:

- purpose and primary outcome;
- protected trust/content/brand boundaries;
- required states and responsive transformations;
- material implementation choice, if any;
- evidence needed and evidence actually observed;
- remaining release condition.

This may live in the run report or existing project documentation. Do not create a
full schema-shaped JSON artifact solely because SITECRAFT is active.

Create or update the full **Experience Contract** when its machine-readable
durability earns its cost: multiple surfaces or routes, consequential generated
assets, shared runtime ownership, repeated handoffs, approval lineage, staged
release, or an existing contract that is already canonical. Start with the
smallest relevant sections and add optional systems only when they are real.

An existing authoritative contract remains authoritative. The threshold controls
whether to create one, not whether an agent may ignore one already in use.

## Route mesh

Treat Frame, Map, Compose, Choreograph, Build, Observe, and Harden as a connected decision flow rather than separate documents.

- Frame supplies audience, outcome, support, risk and acceptable-complexity constraints.
- Map identifies the surfaces, states and journeys that actually need special capabilities.
- Compose defines the visual mechanisms and which content must remain semantic, live, static or media-led.
- Choreograph defines temporal and spatial behaviour before choosing a motion runtime.
- Build records consequential technology decisions in the Runtime Capability Plan and defines integration boundaries and fallbacks.
- Observe collects evidence that matches those mechanisms and returns failures to the owning route rather than silently changing the contract.
- Harden reconciles dependencies, support, accessibility, performance, security, fallbacks and evidence with the promised release state.

A late-entry repair does not need to replay every route. Recover only the minimum upstream facts required for a safe decision. Read [capability-palette-and-orchestration.md](capability-palette-and-orchestration.md) when technology choice or cross-runtime coordination is consequential.

## User-facing explanations

Use plain language. Explain decisions through visible consequences:

- “This keeps the artwork readable on a short laptop.”
- “This menu becomes a bottom sheet on narrow screens because the desktop rail would cover the content.”
- “The transition is removed in reduced-motion mode, but the state change remains obvious through position and focus.”

Avoid process-heavy narration and unexplained design vocabulary.

## Approval

Separate these states:

- direction approved;
- implementation approved;
- evidence reviewed;
- exact state approved;
- released.

One does not imply the next. A user liking a screenshot does not approve unseen mobile states or production deployment.

## Capability honesty

Before claiming an action, require evidence from the relevant tool. Use phrases such as:

- “The code compiles, but I have not visually inspected it.”
- “The desktop screenshot passed review; mobile interaction is still unverified.”
- “I prepared the prompt but did not run the builder.”

Never convert a plan into a claimed action.
