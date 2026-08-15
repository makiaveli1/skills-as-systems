# Collaboration and continuity

## Durable work is not the worker

Represent a work unit with:

- objective and completion boundary;
- exact project/state reference;
- dependencies and blockers;
- owned read/write surfaces;
- protected invariants;
- inputs and canonical references;
- expected output and evidence;
- authority/effect limits;
- next eligible work.

Do not create a second project-management system inside FOUNDRY. Use the host's durable work model when present.

## Delegation

Delegate bounded, independently useful work such as repository mapping, targeted research, test analysis, performance profiling, security review, or an isolated implementation surface. Avoid several workers editing the same canonical files or all rediscovering the entire repository.

Give the minimum sufficient context and exact source references. Require findings, artifacts, diffs, and evidence—not giant transcripts or hidden reasoning.

## Ownership and dependencies

One canonical owner integrates each shared artifact or overlapping change surface. A dependency blocks only work that requires it; workers may continue eligible independent work.

Before writing shared state:

- refresh current file/worktree/branch state;
- confirm ownership or reservation;
- compare expected hashes/revision when available;
- stop on overlap and reconcile with the current owner.

A clean tree does not prove no other worker intends to write it.

## Review independence

Another worker's claim is information, not Authority. Reviewers should receive the contract, exact change, relevant source, and evidence, without being coached toward a verdict. Distinguish self, fresh-context, independent-agent, automated, and human-owner review.

## Continuation record

Use `schemas/continuation-record.schema.json` for genuine cross-session, cross-worker, or cross-host work. Carry:

- objective and current status;
- exact state/fingerprint when available;
- system map and change contract references;
- established findings with evidence;
- changed surfaces;
- current verification and limitations;
- unresolved issues and blockers;
- dependencies and ownership;
- important invariants;
- one or more next eligible actions;
- references needed to resume.

Do not copy full files or histories into the record. Point to canonical state.

## Receiving procedure

Before continuing:

1. verify project identity and current checkout;
2. inspect fresh Git/worktree and file state;
3. validate referenced artifacts when possible;
4. compare continuation state with current state and mark drift;
5. rediscover tools, permissions, environment, and ownership;
6. reopen exact sources for load-bearing findings;
7. continue only eligible work within current authority.

If state moved, refresh the map/contract/record rather than forcing stale assumptions.

## Authority boundary

Continuation must declare that permissions are not carried. Never include secrets, hidden reasoning, private transcripts, temporary credentials/URLs, or another host's approval. Tool access and project scope must be re-established by the receiving environment.

## Learning

Classify learned material as:

- verified project convention;
- project-local environment quirk;
- reusable framework/language pattern;
- general engineering pattern;
- failure pattern;
- candidate FOUNDRY doctrine.

One outcome does not establish a universal rule. Promote only the transferable mechanism after contrasting evidence, counterexample analysis, explicit review, bounded target, and reversible change. Preserve project-local knowledge outside the public skill.
