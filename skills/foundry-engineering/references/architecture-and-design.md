# Architecture and design

## Contents

[Forces](#begin-with-forces-not-components) · [boundaries](#find-natural-boundaries) · [state](#state-and-data-design) · [options](#option-comparison) · [simplicity](#simplicity-gate) · [greenfield](#greenfield-sequence) · [evidence](#architecture-evidence) · [review](#architecture-review-questions)

## Begin with forces, not components

Resolve:

- user and system outcomes;
- scale, latency, availability, durability, security, privacy, cost, and operability needs;
- team, delivery, runtime, platform, regulatory, and migration constraints;
- known failure modes and recovery expectations;
- current architecture and compatibility when extending an existing system.

Do not turn every quality attribute into a maximum. State the required level and the evidence that will judge it.

## Find natural boundaries

Partition by ownership of behaviour, state, data, policy, lifecycle, scaling, security, and change—not by generic nouns such as `manager`, `service`, or `util`.

For every boundary answer:

- What invariant does it own?
- What data or state is authoritative here?
- Which inputs and outputs cross it?
- How are errors, cancellation, retries, and partial failures represented?
- Can it change independently without duplicating policy?
- Who operates and debugs it?

A module boundary is useful even when everything deploys together. A network boundary adds latency, partial failure, security, versioning, and operational cost; require evidence before creating one.

## State and data design

Identify:

- source of truth versus caches, projections, and replicas;
- lifecycle, transitions, invariants, and invalid states;
- consistency and freshness requirements;
- ownership of identifiers, clocks, ordering, and deduplication;
- transaction and recovery boundaries;
- retention, deletion, migration, and audit requirements.

Draw the state transition before distributing it across callbacks, handlers, or services.

## Option comparison

Compare at least two credible designs when architecture is genuinely open. For each record:

- how it satisfies the main path;
- complexity introduced now;
- constraints it preserves or violates;
- failure and recovery model;
- security and data boundaries;
- operational and test burden;
- compatibility and migration path;
- reasons to reject it.

Do not create fake options when one existing convention clearly owns the need.

## Simplicity gate

Before adding a service, daemon, database, queue, cache, event bus, plugin system, generic repository, or framework, ask:

1. Can an existing owner carry the behaviour coherently?
2. Is the new boundary solving a present scale, lifecycle, security, deployment, or ownership problem?
3. What failure modes appear only because this component exists?
4. How will it be observed, tested, upgraded, and removed?
5. Is a local abstraction or explicit duplication cheaper and safer?

Choose the smallest design that completely satisfies current constraints and does not foreclose a credible next step.

## Greenfield sequence

1. Lock outcomes, constraints, and non-goals.
2. Model core behaviours, states, data, and external actors.
3. Choose boundaries and one owner per invariant.
4. Define interfaces and failure semantics.
5. Select technology from capability needs and operating environment.
6. Build a thin end-to-end slice through real boundaries.
7. Verify risk early: data, security, latency, integration, packaging, or platform.
8. Expand only after the slice proves the architecture.

Do not spend the first iteration building a universal platform around an unproven product path.

## Architecture evidence

Use:

- executable spikes for uncertain integration or performance;
- contract tests for interfaces;
- state-machine tests for lifecycle;
- failure injection for recovery assumptions;
- threat models for trust boundaries;
- load measurements for scaling claims;
- deployment and rollback rehearsal for operational design.

A diagram or design document is a hypothesis until the risky mechanism is exercised.

## Architecture review questions

- Are responsibilities and state owners unambiguous?
- Is essential policy duplicated?
- Are boundaries aligned with transactions and failure domains?
- Can partial failure create impossible state?
- Is the system debuggable without privileged guesswork?
- Are public and internal contracts distinguished?
- Can versions coexist during rollout?
- Is complexity proportional to present need?
- Does the design preserve a safe recovery path?
