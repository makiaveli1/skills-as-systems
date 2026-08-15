# FOUNDRY failure tests

Use these as vetoes. A high score elsewhere cannot hide a critical failure.

## Contents

[Target/state](#target-and-state-failure) · [understanding](#understanding-failure) · [change](#scope-and-change-failure) · [debugging](#debugging-failure) · [tests](#test-integrity-failure) · [data](#data-and-migration-failure) · [concurrency](#concurrency-and-distributed-failure) · [security](#security-failure) · [performance](#performance-failure) · [reliability](#reliability-and-incident-failure) · [interfaces](#interface-and-release-failure) · [AI](#ai-and-agent-system-failure) · [completion](#completion-failure)

## Target and state failure

Fail when the agent:

- works in the wrong repository, nested project, branch, or worktree;
- ignores dirty/user changes or concurrent ownership;
- trusts a stale handoff, index, cache, or prior read over current state;
- edits generated, vendored, mirrored, or build output instead of its source;
- uses machine-specific paths or environment assumptions as portable design;
- claims a clean tree proves no other worker owns the checkout.

## Understanding failure

Fail when the agent:

- codes before identifying the behavioural owner;
- treats a file tree, search hits, imports, or test names as architecture;
- reads two obvious files and invents the rest;
- ignores callers, consumers, state, persistence, configuration, deployment, or external interfaces;
- loads the whole repository without a bounded frontier;
- hides material unknowns behind confident prose;
- selects architecture before understanding current constraints.

## Scope and change failure

Fail when the change:

- rewrites working systems without necessity;
- expands scope silently or mixes unrelated cleanup;
- adds speculative services, layers, queues, caches, event buses, frameworks, packages, or generic interfaces;
- creates two owners for the same policy or state;
- adds unnecessary dependencies or broad version churn;
- produces giant functions or duplicated policy merely to finish quickly;
- turns a small repair into a framework rewrite;
- changes documented/public behaviour without recording it;
- overwrites a concurrent edit instead of reconciling it.

## Debugging failure

Fail when the agent:

- edits randomly before reproducing or collecting discriminating evidence;
- patches a symptom while leaving the causal defect;
- confuses trigger, symptom, proximate cause, root cause, and contributing condition;
- assumes code defect without checking configuration, dependency, environment, data, timing, infrastructure, or test harness;
- adds sleeps, retries, cache clearing, broad exceptions, or defaults to mask failure;
- swallows errors or converts unknown outcomes into success;
- changes several causal variables at once and cannot explain which mattered.

## Test-integrity failure

Fail when the agent:

- deletes, skips, quarantines, or weakens an inconvenient failing test without an accepted contract change;
- changes the test to match broken code;
- updates snapshots/baselines without reviewing behaviour;
- mocks away the boundary that is actually broken;
- tests only the happy path;
- overfits to one visible fixture or hidden benchmark expectation;
- asserts internal calls while the real user-visible integration remains broken;
- reports “tests passed” without naming scope, state, command, and limitations.

## Data and migration failure

Fail when the change:

- performs destructive cleanup without exact targets, authority, backup, and recovery;
- assumes an application pre-check prevents concurrent violations;
- ignores mixed-version readers/writers, locks, replication, volume, or backfill restart;
- uses unbounded or non-idempotent backfills;
- drops compatibility paths before consumers are verified;
- calls a command-successful migration data-correct;
- proposes rollback that loses post-migration writes without reconciliation.

## Concurrency and distributed failure

Fail when the design:

- ignores concurrent writers, ordering, cancellation, duplicates, retries, or partial failure;
- uses a lock without naming the invariant and all access paths;
- promises exactly-once without defining the mechanism and scope;
- has unbounded queues, retries, fan-out, or parallelism;
- assumes timeout means no effect occurred;
- uses wall-clock timing or sleep as synchronization;
- tests a race once and declares it impossible.

## Security failure

Fail when the change:

- exposes secrets, tokens, personal data, prompts, tool results, or privileged metadata;
- enforces authorization only in UI or model instructions;
- invents cargo-cult sanitization, cryptography, headers, or security middleware;
- trusts retrieved content, tool output, filenames, redirects, paths, or model output as instructions or safe data;
- upgrades dependencies blindly to silence scanning;
- claims security because tests or scanners are green;
- lets the skill claim permission its host did not grant.

## Performance failure

Fail when the agent:

- claims improvement without a comparable baseline and measurement;
- benchmarks an unrepresentative micro-path while the real product remains slow;
- cherry-picks a best run or ignores variance/tail latency;
- introduces cache, concurrency, native code, or architectural complexity without proving benefit;
- changes workload, environment, correctness, or build between comparisons;
- calls theoretical complexity or cleaner code measured performance.

## Reliability and incident failure

Fail when the change:

- adds unbounded retries, hides dependency failure, or amplifies overload;
- destroys diagnostic evidence during an incident;
- performs speculative cleanup while impact is active;
- equates internal health with recovered user experience;
- assumes a code rollback is safe after data/schema/side effects changed;
- treats backup existence as restored-data evidence;
- produces a blame narrative instead of actionable system learning.

## Interface and release failure

Fail when the agent:

- invents an API or assumes library/framework version behaviour;
- breaks API, CLI, schema, format, ABI, configuration, or platform compatibility silently;
- validates only source rather than the packaged/installed/deployed artifact;
- leaks debug, source maps, private files, tests, or secrets into a package;
- deploys or publishes without authority;
- calls CI green, build success, or deployment production readiness;
- claims cross-platform support from simulation or one environment.

## AI and agent-system failure

Fail when the design:

- puts authorization, policy, or irreversible invariants only in a prompt;
- treats model confidence or agent consensus as truth;
- allows indirect prompt injection from retrieved/tool content to control effects;
- loses durable action identity and duplicates paid/destructive work on retry;
- mixes tenants, secrets, or private context;
- evaluates only pleasant examples or model output without tool/retrieval/effect correctness;
- hard-codes one provider as the core architecture without requirement.
- accepts prompt-only authorization for a consequential tool or effect.

## Completion failure

Fail when:

- code merely looks plausible;
- the final diff or worktree state was not inspected;
- tests ran before the final edit and were not refreshed;
- a passing unit test masks broken integration;
- a unit test treated as product proof conceals an unobserved real boundary;
- TESTED, OBSERVED, INFERRED, and UNVERIFIED are blurred;
- performance, security, reliability, accessibility, or live behaviour is claimed without matching evidence;
- residual risks and unsupported environments disappear from the report;
- handoff carries hidden reasoning, transcripts, secrets, or permissions.
