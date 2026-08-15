# Testing and evidence

## Contents

[Claims](#start-from-claims-and-risks) · [responsibilities](#test-responsibilities) · [regression](#regression-design) · [integrity](#test-integrity) · [advanced tests](#property-model-and-differential-testing) · [concurrency](#concurrency-and-nondeterminism) · [provenance](#evidence-provenance) · [widening](#widening-strategy) · [closeout](#exact-state-closeout)

## Start from claims and risks

Build a verification matrix:

| Claim or risk | Best evidence | Exact state/environment | Pass condition | Limitation |
|---|---|---|---|---|

Do not start with every available test command. Select evidence that can actually falsify the claim.

## Test responsibilities

### Static and construction checks

Syntax, formatting, compilation, types, schemas, dependency resolution, generated-code consistency, and packaging catch malformed states. They rarely prove behaviour.

### Unit tests

Use for local rules, transformations, state transitions, and edge cases. Keep them deterministic and focused. Avoid asserting private implementation details unless those details are the contract.

### Contract and component tests

Use at process, service, package, protocol, database, or UI-component boundaries. Verify both producer and consumer assumptions, including error shapes and compatibility.

### Integration tests

Use real combinations where boundary behaviour, configuration, serialization, persistence, or framework integration is the risk. Replace only expensive or uncontrollable dependencies; do not mock away the defect.

### End-to-end and live checks

Use for critical product journeys and operational reality. Scope the environment precisely. A preview environment is not production; a headless browser is not every supported device.

### Non-functional evidence

Use controlled measurements or adversarial checks for performance, security, reliability, accessibility, concurrency, and recovery. Each discipline has its own reference.

## Regression design

A regression test should:

- fail for the original cause or unsafe behaviour;
- pass for the repair;
- exercise the owning layer;
- distinguish the bug from nearby valid behaviour;
- resist overfitting to one fixture;
- remain meaningful if the implementation changes.

Reproduce the previous failure after the fix. If reproduction was never established, state what proxy evidence was used.

## Test integrity

Fail the work when a change:

- deletes or skips an inconvenient test without an accepted contract change;
- relaxes an assertion beyond the intended new behaviour;
- replaces a real boundary with a mock to hide integration failure;
- updates a snapshot or baseline without reviewing the change;
- adds sleeps, retries, order dependencies, or global state to mask nondeterminism;
- makes a test pass only for one fixture while the behaviour remains wrong;
- asserts the implementation was called but not that the user-visible effect occurred.

When the test is wrong, explain the obsolete assumption and add evidence for the intended contract before changing it.

## Property, model, and differential testing

Use when examples underspecify a broad input or state space:

- property-based tests for invariants across generated inputs;
- state-machine/model tests for allowed transitions and sequences;
- differential tests against a trusted implementation or prior version;
- metamorphic tests when exact outputs vary but relationships must hold;
- fuzzing for parsers, protocols, unsafe boundaries, and crash resistance.

These techniques are not automatic requirements. Use them when they materially expand coverage of the risk.

## Concurrency and nondeterminism

Control clocks, randomness, schedulers, network faults, and shared state where possible. Test ordering, cancellation, timeout, retry, duplicate delivery, stale reads, and partial failure explicitly. A test that passes once does not establish race freedom.

## Evidence provenance

For each check record:

- exact project revision/artifact and dirty state;
- command or manual action;
- environment, runtime, dependency, and configuration versions that matter;
- inputs/fixtures and real versus simulated boundaries;
- result and relevant output reference;
- date/freshness and reviewer;
- limitations and untested neighbours.

Distinguish self-review, fresh-context review, independent review, human review, and automated checks. Only the last three have independent actors, and automated scope may still be narrow.

## Widening strategy

Start near the changed owner for fast feedback, then widen by dependency and risk neighbourhood. Do not run a massive suite first when a focused failure can reveal the cause. Do not stop at focused success when compatibility, packaging, or integration is material.

## Exact-state closeout

Before completion:

1. inspect the final diff and changed/untracked/generated artifacts;
2. confirm tests ran after the final edit;
3. identify stale evidence invalidated by later changes;
4. confirm built or deployed artifacts correspond to the reviewed source;
5. classify every material claim as TESTED, OBSERVED, INFERRED, or UNVERIFIED;
6. preserve residual risks and next checks.

Use `schemas/verification-receipt.schema.json` when evidence must survive a handoff or approval gate.
