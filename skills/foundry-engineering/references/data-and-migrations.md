# Data, persistence, and migrations

## Model ownership first

Identify:

- authoritative store and schema owner;
- writers, readers, replicas, caches, projections, exports, and backups;
- identity, uniqueness, ordering, time, nullability, and retention rules;
- transaction boundary and isolation assumptions;
- expected volume, skew, growth, and access paths;
- recovery point and recovery time requirements.

Do not treat an ORM model as the complete data contract.

## Transactional correctness

Define invariants in terms of committed state. Check:

- atomicity across all required writes;
- isolation and anomalies tolerated or forbidden;
- idempotency under retries and duplicate delivery;
- constraint enforcement in the correct owner;
- lost update, write skew, stale read, and read-modify-write races;
- side effects relative to commit and rollback;
- outbox/inbox or compensation when a transaction cannot span boundaries.

An application-level pre-check does not replace a database constraint under concurrency.

## Query and persistence changes

Use real query plans and representative data when performance matters. Inspect indexes, selectivity, join cardinality, lock behaviour, transaction duration, pagination, batching, and N+1 patterns. A query that is fast on an empty development database proves little.

## Migration contract

Record:

- source and target schemas/formats;
- compatible mixed-version states;
- reader/writer deployment order;
- backfill strategy, batching, throttling, and resume cursor;
- constraints and validation order;
- lock, storage, replication, and runtime impact;
- abort, rollback, restore, or forward-fix strategy;
- reconciliation and completion queries;
- data retention and privacy effects.

Verify database/version-specific DDL and locking behaviour against current official documentation before execution.

## Expand–migrate–contract

For online compatibility where appropriate:

1. **Expand:** add backward-compatible schema or format.
2. **Deploy compatible writers/readers:** tolerate both states.
3. **Backfill:** resumable, idempotent, observable, and bounded.
4. **Verify:** counts, checksums, invariants, sampling, error queues, and consumer behaviour.
5. **Switch authority:** change reads/writes with rollback or feature control.
6. **Observe:** wait through a suitable safety window.
7. **Contract:** remove old paths only after all consumers and recovery needs are cleared.

Do not dual-write casually. Define ordering, partial failure, retry, and reconciliation.

## Destructive changes

Before drop, delete, rewrite, or irreversible transformation:

- enumerate all consumers and unknown access paths;
- take or verify a suitable backup/snapshot;
- rehearse restore or forward recovery at representative scale;
- preserve legal/retention/deletion obligations;
- use explicit human authority when required;
- prove no older binary or job still depends on the data;
- record final counts and state.

## Backfills

Backfills must be restartable and safe under concurrent writes. Define item identity, cursor/checkpoint, idempotency key, conflict policy, rate limits, observability, poison-record handling, and validation. Do not let one corrupt row block an unbounded job without a quarantine/review path.

## Migration evidence

Collect:

- schema and application compatibility tests;
- representative dry run or clone rehearsal;
- lock/duration/storage/replication measurements;
- pre/post invariant queries and counts;
- backfill progress and error records;
- mixed-version tests;
- restore, rollback, or forward-fix rehearsal;
- exact migration and application revisions.

“Migration command succeeded” is not proof that application state, all rows, or consumers are correct.
