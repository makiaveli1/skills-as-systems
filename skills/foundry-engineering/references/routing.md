# FOUNDRY routing

Classify the current work, risk, and available evidence before loading references. A task may change modes; do not replay completed stages without a named reason.

## Modes

| Mode | Primary question | Minimum packet | Common next mode |
|---|---|---|---|
| Explore | What system exists and how does it behave? | understanding compact | Design, Debug, Review |
| Design | What is the smallest architecture that satisfies the constraints? | architecture and design, change compact | Implement, Research |
| Implement | How should required behaviour be added safely? | understanding compact, change compact, verification compact | Test, Review |
| Debug | What evidence distinguishes the cause? | debugging and repair, understanding compact | Repair, Incident |
| Repair | What narrow causal change restores behaviour? | debugging and repair, change compact, verification compact | Test, Review |
| Refactor | How can structure improve while behaviour remains stable? | review and refactoring, change discipline, testing and evidence | Review |
| Review | What can fail, regress, leak, or become hard to operate? | review and refactoring, failure tests | Repair, Security |
| Test | Which risks and behaviours need which evidence? | testing and evidence | Implement, Release |
| Performance | Where is measured cost incurred and what change moves it? | performance engineering | Implement, Verify |
| Security | What assets, trust boundaries, abuse cases, and controls matter? | security engineering | Repair, Verify |
| Migration | How can state or interfaces move without unsafe mixed states? | data and migrations, delivery and release | Implement, Release |
| Release | Is the exact artifact compatible, recoverable, and ready? | delivery and release, verification compact | Recovery |
| Incident | How do we stabilize, learn, and recover without corrupting evidence? | reliability and incidents, debugging and repair | Repair, Recovery |
| Research/Spike | Which unstable fact or risky assumption must be resolved? | research method, architecture and design | Design |

Specialist dimensions such as API, frontend, concurrency, AI systems, or databases may be added to any mode. They do not replace the mode.

## Risk route

Escalate the contract and verification depth when any of these apply:

- irreversible or difficult-to-recover state;
- authentication, authorization, secrets, money, safety, privacy, or legal obligations;
- public API, wire format, package, CLI, schema, or cross-platform compatibility;
- concurrent writers, distributed coordination, retries, ordering, or partial failure;
- production data, migrations, release, deployment, or incident response;
- broad dependency or architecture change;
- missing reproduction, weak tests, or unclear ownership;
- several packages, repositories, languages, runtimes, or teams;
- long-running work or handoff.

High risk does not automatically justify a large change. It justifies more explicit understanding, proof, and recovery.

## Mode transitions

Use explicit transitions when evidence changes the work:

- Debug → Repair when a causal hypothesis survives falsification.
- Repair → Architecture only when the defect cannot be fixed coherently at the owning boundary.
- Implement → Research when a version-sensitive dependency or platform claim controls the design.
- Refactor → Repair when current behaviour is already defective.
- Test → Implement when the failure belongs to production code; do not weaken the test.
- Incident → Recovery before improvement when user impact or data integrity is active.

Record why the mode changed. A new mode may invalidate part of the contract or evidence; stale only the affected responsibility.

## Context budget

Default to:

1. this `SKILL.md`;
2. one compact discipline reference;
3. one or two specialist references;
4. exact repository evidence.

Add a deep reference only for a decision it can change. Prefer heading-bounded reads and targeted search over full manuals. For large repositories, keep maps and source paths outside prose summaries so evidence can be reopened.

## Sufficiency gate

Act when all are true:

- the exact project and state are known;
- the behaviour path and owner are identified;
- material state, data, external, generated, and compatibility boundaries are known;
- the smallest coherent change surface is explainable;
- important unknowns are either resolved, bounded, or explicitly accepted;
- the proof and recovery paths are credible.

Continue exploring when one missing fact could change the owner, architecture, data safety, public contract, or verification result.

## Small-task route

A one-line, reversible, well-localized change does not require a saved map or JSON contract. Still confirm target, protected behaviour, local convention, focused proof, and final diff.

## Advisory-only route

When code or tools are unavailable, provide a bounded diagnosis, design, patch suggestion, or verification plan. Mark execution and runtime claims UNVERIFIED. Do not simulate tool evidence in prose.
