# Change discipline

## Contents

[Purpose](#contract-not-paperwork) · [fields](#contract-fields) · [coherence](#smallest-coherent-change-test) · [dependencies](#dependency-rule) · [freshness](#stale-state-rule) · [breadth](#broad-change-rule) · [review](#change-review)

## Contract, not paperwork

A Change Contract is a decision boundary. Use it when it prevents ambiguity, accidental expansion, unsafe handoff, or false completion. Do not require a JSON file for a local typo or obvious one-line repair.

## Contract fields

### Objective

State one observable outcome. Separate implementation preference from required behaviour.

### Baseline

Record current behaviour, exact state, and evidence. If the baseline cannot be reproduced, mark that limitation before changing code.

### Target and failure behaviour

Define success, edge cases, invalid inputs, degraded dependencies, cancellation, retries, partial failure, and recovery where relevant.

### Invariants

Name behaviour that must not change:

- public API, CLI, file, schema, protocol, or storage compatibility;
- security and authorization boundaries;
- data integrity and idempotency;
- ordering, concurrency, and transactional guarantees;
- accessibility, performance, or resource budgets;
- user changes, approved content, and operational controls.

### Ownership and change surface

Identify the current owner and smallest coherent surface. Include direct code plus affected tests, configuration, schemas, migrations, docs, observability, and release material. Use an allowlist when the risk of stray edits is high.

### Forbidden changes

Name tempting shortcuts:

- framework or dependency replacement;
- unrelated cleanup;
- deleting or weakening tests;
- catch-all exceptions, silent fallbacks, or hidden retries;
- editing generated/vendor files;
- destructive data cleanup;
- public compatibility breaks;
- security or performance claims without required evidence.

### Risk and verification

Map each material risk to evidence. A long generic test list is weaker than a short claim-to-proof matrix.

### Recovery

Choose one or more:

- source rollback;
- configuration/feature disable;
- compatible dual-read/dual-write window;
- data backup and restore rehearsal;
- compensating operation;
- forward-only repair for irreversible migrations;
- deployment rollback plus post-rollback state verification.

A rollback that loses newly written data is not a valid rollback without an explicit reconciliation plan.

## Smallest coherent change test

Ask:

1. Can an existing owner naturally support this behaviour?
2. Is the defect local, or does its cause cross a boundary?
3. Does the proposed change preserve existing contracts?
4. Does it introduce a second owner for the same concern?
5. Can the new path be tested and operated independently?
6. Is added complexity paid for by a present requirement rather than a hypothetical future?

Small is not synonymous with fragile. Duplicating a critical rule in three callers may be fewer lines today but a larger semantic change surface tomorrow.

## Dependency rule

Before adding or upgrading a dependency, record:

- exact capability needed;
- why current platform/project capability is insufficient;
- current resolved version and compatibility constraints;
- transitive, license, security, build, runtime, and maintenance cost;
- rejected alternatives;
- removal or rollback route;
- verification under the actual resolved dependency graph.

Never use `latest` as reproducible evidence. Verify version-sensitive claims against current official documentation and the actual lock/resolution state.

## Stale-state rule

Immediately before editing:

- refresh target contents and relevant hashes/diff;
- compare contract assumptions with current state;
- detect concurrent changes or generated output drift;
- stop and rebase the plan if ownership or source state moved.

Do not resolve concurrent edits by overwriting them.

## Broad-change rule

For cross-package, multi-repository, migration, or release work:

1. define compatibility order;
2. identify independently deployable steps;
3. keep mixed-version states safe;
4. add observability before risky activation;
5. separate code deployment from behavioural activation where useful;
6. define abort and recovery gates per step;
7. verify consumers before removing compatibility paths.

## Change review

At closeout compare the final state with the contract:

- every changed surface is allowed and explained;
- invariants have matching evidence;
- new failure paths are visible and handled;
- tests were strengthened or preserved;
- no generated, secret, temporary, or unrelated artifact leaked;
- recovery remains feasible after the actual change;
- documentation and compatibility promises match reality.
