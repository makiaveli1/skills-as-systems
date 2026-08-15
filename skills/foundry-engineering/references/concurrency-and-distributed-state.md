# Concurrency and distributed state

## Begin with the state machine

Write:

- states and valid transitions;
- actor allowed to initiate each transition;
- invariant before and after;
- atomic boundary;
- ordering and clock assumptions;
- duplicate, delayed, lost, reordered, or concurrent event behaviour;
- cancellation, timeout, retry, and recovery behaviour.

If the state machine cannot be stated, concurrency primitives will only hide confusion.

## Shared-memory reasoning

Identify every shared mutable location and its synchronization owner. Establish the required happens-before relationship. Check:

- atomicity versus compound read-modify-write;
- lock scope, ordering, reentrancy, priority, and starvation;
- visibility and memory-model guarantees;
- lifecycle and use-after-close/use-after-free risks;
- blocking inside async/event-loop code;
- cancellation and cleanup;
- thread/task-safe library contracts.

Locks protect invariants, not lines of code. One invariant should have one synchronization policy.

## Async and evented systems

Make ownership explicit for tasks, futures, callbacks, streams, subscriptions, and resources. Handle:

- structured lifetime and orphaned work;
- cancellation propagation;
- timeout versus completion races;
- backpressure and bounded queues;
- ordering across parallel operations;
- error aggregation and partial completion;
- cleanup on every terminal path.

Do not add sleeps to create an assumed order.

## Distributed correctness

Assume networks delay, duplicate, reorder, partition, and fail partially. Processes restart. Clocks skew. Storage and caches have distinct consistency.

For each operation define:

- request identity and idempotency scope;
- authority and consistency model;
- retry owner and budget;
- deduplication lifetime;
- timeout semantics: unknown outcome is not necessarily failure;
- conflict and stale-write policy;
- reconciliation or compensation;
- observability correlation.

“Exactly once” usually decomposes into at-least-once delivery plus idempotent effect, or a tightly scoped transactional mechanism. State the actual guarantee.

## Coordination choices

Prefer the simplest primitive that enforces the invariant:

- immutability or ownership transfer;
- atomic/compare-and-swap;
- mutex/read-write lock/semaphore;
- single-writer actor or event loop;
- bounded queue/channel;
- database transaction/constraint;
- lease, fencing token, consensus, or durable log for distributed ownership.

Do not introduce distributed coordination where local serialization or a database constraint is sufficient.

## Failure tests

Exercise when relevant:

- simultaneous writers;
- duplicate and reordered messages;
- crash before and after durable write;
- timeout with eventual success;
- retry storm and thundering herd;
- stale lease or leader;
- cancellation during commit or cleanup;
- process restart with in-flight work;
- queue saturation and backpressure;
- clock skew and expiry boundary;
- partial dependency outage.

Use deterministic schedulers, model checking, stress repetition, fault injection, or state-machine property tests where the risk justifies them. A thousand passing runs reduce uncertainty but do not prove race freedom.

## Evidence

Pair code reasoning with observed tests and runtime state. Record platform/runtime because memory and scheduler behaviour differ. Verify persistence and messaging guarantees against the actual versions and configuration in use.
