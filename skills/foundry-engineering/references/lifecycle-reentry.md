# Lifecycle re-entry

FOUNDRY governs the engineering lifecycle, not only the first plan. Keep it
active until the objective is complete or the user explicitly changes method.

## Re-entry triggers

Re-enter the loop when:

- user intent, scope, invariants, compatibility, authority, or acceptance changes;
- inspection finds a different owner, dependency, state boundary, or risk surface;
- a test, build, runtime observation, review, benchmark, or security check fails or contradicts the current model;
- a dependency, environment, branch, worktree, generated source, or concurrent writer changes relevant state;
- work resumes after interruption or handoff;
- the task changes mode, such as Debug → Repair → Migration → Release;
- the agent is about to claim completion.

Always re-enter before the first consequential edit to compare the proposed
change surface with fresh state. Always re-enter verification and failure tests
before completion.

## Re-entry operation

1. Inspect fresh state at the invalidated boundary.
2. Mark which KNOWN, INFERRED, UNKNOWN, contract item, hypothesis, or evidence
   is no longer current.
3. Re-route only the affected mode and specialist references.
4. Update the system map or change contract only when its truth changed.
5. Choose continue, revise, rollback, reproduce, or ask for a consequential
   decision.
6. Verify the affected claim, then return to the parent objective.

Preserve still-valid understanding and evidence. Do not restart the whole
workflow, reload the whole atlas, or create a new artifact merely to signal
compliance.

## Recursive child loops

A consequential defect, unknown, or failed assumption opens a bounded child loop:

`observe → classify invalidation → understand → contract → intervene → verify → challenge → return`

The child inherits the parent's applicable invariants and authority but never
widens them. If it changes an upstream assumption, reopen the affected parent
decision. Close child loops with evidence or an explicit verification gap; do
not bury them under a green parent test suite.

Depth follows risk. A local formatting correction may need only a fresh diff.
A new data, concurrency, security, compatibility, or deployment boundary needs
its matching specialist route and proof.

## Harness contract

A portable skill cannot force invocation in a host that ignores installed
skills. Once invoked, the active agent must retain this lifecycle contract and
host adapters should reinvoke FOUNDRY at the triggers above. In the final
receipt, identify material re-entry events and the state they invalidated.
Never expose hidden reasoning or manufacture checkpoint paperwork.
