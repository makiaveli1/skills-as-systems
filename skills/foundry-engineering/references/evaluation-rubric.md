# FOUNDRY evaluation rubric

Evaluate the engineering outcome against the actual contract. Begin with blocking floors and observed defects; use scores only as a summary.

## Contents

[Score](#score) · [areas](#areas) · [blocking floors](#blocking-floors) · [integration veto](#integration-veto) · [readiness](#readiness-states) · [output](#evaluation-output)

## Score

Use 0–5 per area:

- `0` absent, unsafe, or fundamentally wrong;
- `1` severe failure requiring a new approach;
- `2` material weakness with likely user/system consequence;
- `3` functional baseline with bounded limitations;
- `4` strong, coherent, and evidenced;
- `5` exceptional for the actual constraints with no material unresolved weakness.

Do not award evidence-backed scores from inference alone.

## Areas

### Target and understanding

Was the exact project/state identified? Are repository shape, behavioural path, owner, state/data, boundaries, change surface, and material unknowns understood at the depth required?

### Contract and scope

Are baseline, target, invariants, allowed/forbidden surfaces, risks, proof, and recovery explicit without creating unnecessary paperwork?

### Correctness and failure behaviour

Does the implementation satisfy normal, edge, invalid, degraded, cancellation, retry, and recovery behaviour relevant to the contract?

### Architecture and simplicity

Does the change fit existing ownership and conventions? Is added abstraction/dependency/distribution justified by current forces? Is there one owner per invariant?

### Data, state, and concurrency

Are transactions, persistence, ordering, idempotency, mixed versions, concurrent writers, and invalid states handled correctly where relevant?

### Security and privacy

Are assets, trust boundaries, authorization, validation, secrets, dependencies, tool effects, and data exposure addressed at the required assurance?

### Performance and reliability

Are performance claims measured under representative conditions? Are timeouts, overload, retries, recovery, observability, and operational failure proportional to the system?

### Compatibility and delivery

Are public interfaces, dependencies, builds, packages, platforms, migrations, rollout, and rollback compatible and evidenced?

### Testing and evidence

Do tests target the real owner and prior failure? Are integration/runtime/non-functional claims supported by matching, fresh, exact-state evidence? Is test integrity preserved?

### Maintainability and continuity

Is the final system clearer to inspect, change, operate, review, and resume? Are decisions and continuation pointers compact, factual, and authoritative?

## Blocking floors

Block completion or release regardless of average score when any applies:

- wrong or unresolved project/worktree/state;
- material behaviour owner or invariant unknown;
- known data loss/corruption, critical security/privacy, money, safety, or authorization failure;
- destructive or irreversible action without authority and recovery;
- public compatibility break outside the contract;
- regression test weakened or real integration still broken;
- concurrency/migration path can create invalid state;
- required exact-state, runtime, package, or recovery evidence missing;
- performance/security/reliability claim unsupported by its discipline;
- user or release authority missing;
- secrets/private material exposed;
- final state differs from the state that was verified.

## Integration veto

Fail when individually plausible parts contradict:

- tests prove a helper while the product path bypasses it;
- API schema and implementation disagree;
- migration and deployment order cannot coexist;
- retry policy duplicates effects;
- UI optimistic success outruns durable state;
- new cache violates source-of-truth freshness;
- security policy exists only in one entry path;
- package contents differ from reviewed source;
- rollback cannot read the new data state;
- handoff points to stale evidence or a different revision.

## Readiness states

- `understanding_required`
- `contract_ready`
- `implementation_in_progress`
- `implemented_unverified`
- `repair_required`
- `ready_for_review`
- `verified_with_limits`
- `approved_for_release`
- `released_observed`
- `blocked`

## Evaluation output

Report exact state, evidence scope, blocking floors, findings ordered by consequence, strengths worth preserving, smallest repair, stale evidence caused by that repair, readiness, and next authority/action. Do not average away a failed floor.

For compact expected-behaviour examples, see [worked pressure tests](../examples/scenario-walkthroughs.md). Use `scripts/evaluate_scenarios.py` to check routing budgets, negative routing, adversarial case completeness, and artifact corruption gates.
