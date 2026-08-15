# Worked pressure tests

These are compact applications of FOUNDRY, not claims that a real repository or production system was executed. They show the decision path, evidence boundary, and veto that an evaluator should expect.

## Large unfamiliar repository

**Request:** explain how checkout reaches payment and fulfilment before proposing a change.

**Route:** Explore → `understanding-compact` → `codebase-understanding` → interface and data depth.

**Expected work:** confirm exact repository state; find the externally reachable checkout entry; trace the runtime path to the payment owner, durable order transition, queue or event boundary, fulfilment consumer, and tests/operations. Build a bounded System Map with unopened edges and knowledge labels.

**Gate:** sufficient to explain the named path, owners, state transitions, failure paths, and proof sources. It is not necessary to read unrelated analytics or administration subsystems.

**Veto:** a directory tree or import graph presented as architecture; implementation proposed before behavioural ownership is established.

## Mixed-version data migration

**Request:** move 300 million live rows to a new state model while old and new applications coexist.

**Route:** Migration + Release → data, concurrency, change-discipline, verification, and delivery depth.

**Expected contract:** preserve old-reader and old-writer safety; define authoritative representation during transition; expand schema first; deploy compatible readers/writers; run bounded idempotent backfill with progress and reconciliation; verify consumers; contract only after the observation window.

**Evidence:** sampled and aggregate data invariants, backfill restart tests, mixed-version integration tests, lock/replication observations, rollback and roll-forward rehearsal, exact rollout state.

**Veto:** one-shot rewrite; unbounded transaction; “command succeeded” treated as data correctness; rollback that cannot represent post-migration writes.

## Timeout-driven duplicate effect

**Request:** two workers sometimes charge the same idempotency key after a timeout.

**Route:** Debug + Repair → debugging, distributed state, data, and testing depth.

**Hypotheses:** the key is scoped per attempt; the durable uniqueness constraint is absent or bypassed; retry occurs before provider reconciliation; two writer paths disagree about ownership.

**Expected repair:** first reproduce or collect traces across the durable action identity. Treat timeout as an unknown outcome. Put the guarantee at the shared durable boundary, reconcile provider/ledger state, and make retries reuse the action identity.

**Evidence:** deterministic overlap test or production trace, uniqueness/conflict behaviour, timeout reconciliation test, duplicate delivery test, widened payment regression suite.

**Veto:** process-local lock without writer inventory; a sleep; a claim of exactly-once without mechanism and scope.

## Unit green, product broken

**Request:** serializer unit tests pass, but the published client rejects the real response.

**Route:** Debug + Repair + Test → debugging, interfaces, and testing depth.

**Expected work:** reproduce through the published/installed client; record the exact server and client artifacts; trace serialization, transport, schema generation, packaging, and client decoding; compare the real payload with the contract.

**Evidence:** failing real-boundary reproduction, causal difference, focused regression, generated-contract consistency, packaged artifact smoke test.

**Veto:** mock the published client and declare completion from the helper unit test.

## Concurrent worker drift

**Request:** apply a prepared patch after another worker changed the same parser files.

**Route:** Explore + Review → collaboration, change discipline, and compact understanding.

**Expected work:** stop the stale apply; refresh current files, diff/hashes, ownership, and tests; determine whether changes overlap semantically; assign one integration owner; rebuild the patch against current state; rerun affected evidence.

**Veto:** trust the handoff over fresh state, overwrite the other change, or infer authority from a clean worktree.

## Rewrite pressure

**Request:** replace an application framework to repair one validation function.

**Route:** Review + Implement → change compact, architecture, and failure tests.

**Expected decision:** challenge the proposed means; identify the current validator owner and failing path; compare a bounded repair with any genuine architectural constraint. Select the repair unless evidence shows the existing framework cannot satisfy the contract.

**Veto:** framework novelty, aesthetics, or agent convenience used as rewrite justification.
