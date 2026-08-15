# Lifecycle re-entry

Use SITECRAFT as a control loop for the governed experience, not as a kickoff
prompt that expires after planning.

## Re-enter at control boundaries

Re-enter SITECRAFT when any of these occurs:

- the brief, audience, priority, acceptance condition, or protected behaviour changes;
- inspection reveals a different owner, state, route, asset, capability, or constraint;
- a build, browser check, visual review, accessibility check, or performance check fails or contradicts the current plan;
- another worker or tool changes an overlapping surface;
- work resumes from a handoff, interruption, or stale context;
- implementation moves into review, hardening, release, or a completion claim.

Before the first substantial edit, re-enter once to compare the proposed build
surface with the current project and compact contract. Before completion,
re-enter **Observe** and **Harden** even when implementation appeared smooth.

## Re-entry operation

1. Inspect fresh project and runtime state.
2. Name what changed and which earlier assumption, decision, or evidence it
   invalidates.
3. Reopen only the affected route and references.
4. Update the compact/full contract only where the experience truth changed.
5. Choose continue, repair, rework, or rollback.
6. Produce evidence at the boundary that changed, then return to the parent
   objective.

Do not restart the entire workflow or reload the full reference library when a
local result changes. Preserve still-valid decisions and evidence.

## Recursive child loops

When work uncovers a consequential defect or unknown, open a bounded child loop
with its own observation, affected invariant, intervention, and proof.
Close that loop before returning to the parent route. If the child changes the
brief or architecture, invalidate and reopen the affected parent decision.

Depth follows consequence, not curiosity. A trivial styling correction does
not need a formal nested artifact. A defect affecting navigation, state,
accessibility, public/private separation, or release evidence does.

## Harness contract

An installed skill cannot grant permissions or force a host that ignores skill
instructions. Once invoked, the active agent must retain SITECRAFT as the
governing lifecycle until the objective is complete or the user explicitly
changes the method. Host adapters should invoke it again at the boundaries
above. Record material re-entry events in the final evidence summary; do not
emit a transcript or ceremonial checkpoint log.
