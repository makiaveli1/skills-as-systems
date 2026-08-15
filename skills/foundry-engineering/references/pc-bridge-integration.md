# Optional PC Bridge integration

FOUNDRY remains complete without PC Bridge. This adapter maps engineering procedure onto Bridge capabilities when they are present and approved.

## Ownership boundary

FOUNDRY owns:

- codebase-understanding method;
- engineering modes and specialist routing;
- Change Contract semantics;
- debugging, implementation, review, and verification discipline;
- engineering evidence interpretation;
- failure tests and evaluation.

PC Bridge owns:

- approved project and Workspace boundaries;
- Mission, Goal, WorkAssignment, and WorkerRun identity;
- Authority, permissions, effects, and protected actions;
- file/tool execution and recovery mechanisms;
- canonical coordination and current Workboard/Kanban Lens;
- Context Compiler and capability paging;
- durable Evidence, Effect, verification, Git/worktree, and continuation state.

Do not duplicate these systems inside FOUNDRY artifacts.

## Project targeting

Use Bridge project/workspace inspection to confirm exact root, checkout/worktree, Git state, instructions, generated boundaries, and active coordination. FOUNDRY's System Map may point to canonical Bridge state IDs; it must not widen the approved root.

Never infer permission from a FOUNDRY Change Contract. Current Bridge policy and explicit user authority control execution.

## Context Compiler

Compile bounded engineering context in this order:

1. task/Goal or WorkAssignment contract;
2. exact project and state references;
3. compact FOUNDRY doctrine and selected mode;
4. only matching specialist references;
5. repository evidence for the behavioural path/change surface;
6. current verification and coordination state.

Use capability paging for deeper references or source only when a decision needs them. Avoid giant handoffs and recursive summaries.

## Safe changes

When available and proportionate:

- use exact-state/hash-checked patch plans for shared or sensitive multi-file changes;
- preview before apply;
- revalidate source hashes and ownership immediately before write;
- keep backups/rollback records;
- stop on concurrent drift rather than overwrite;
- use isolated worktrees for independent implementation when Bridge coordination supports them.

The host's file-writing mechanism may differ. The engineering contract stays provider-neutral.

## Work mapping

- Mission: durable overall outcome.
- Goal: bounded engineering result and contract.
- WorkAssignment: owned eligible unit with dependencies, surfaces, invariants, and evidence.
- WorkerRun: one execution attempt with fresh state and capability profile.
- Workboard/Kanban Lens: derived coordination view, not a second task database.

Dependencies should block specific WorkAssignments. Continue other eligible work. Another WorkerRun's report must be reconciled with fresh canonical state before integration.

## Evidence and verification

Store checks as Bridge Evidence/verification receipts when available, tied to exact state, environment, command/action, artifact, and limitation. FOUNDRY still classifies claims as TESTED, OBSERVED, INFERRED, or UNVERIFIED and applies domain floors.

Bridge verification proves only its declared workflow. It does not automatically prove live behaviour, security, performance, accessibility, or release readiness.

## Continuation

Prefer canonical Bridge continuation context and generated Lenses for long-running work. A portable FOUNDRY Continuation Record may point to Bridge Mission/Goal/WorkAssignment/WorkerRun, evidence, and state IDs, but must not copy authority, permissions, hidden reasoning, transcripts, or secrets.

On another host, validate continuity, refresh project/Git/coordination state, and rediscover capabilities before writing.

## Skill Fabric

Use `pc-bridge.skill.json` only as optional discovery, reference routing, and staged workflow metadata. Keep `SKILL.md`, references, schemas, examples, and validators usable without it. Fabric routing must remain specific and context-bounded; ordinary coding work must not load every specialist reference.

Validate the portable package first, then validate through Skill Fabric. A valid manifest cannot repair weak engineering doctrine.
