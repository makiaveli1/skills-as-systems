# Ledgerbox repair run report

## Diagnosed cause

The ledger insert and processed-event marker were separate autocommit statements. If execution stopped at the existing `after_credit` checkpoint, the ledger entry was already durable while the marker was absent. A retry therefore passed `has_processed` and inserted the credit again.

The same split boundary also made the check-then-write sequence unsafe for concurrent delivery: two connections could both observe no marker, both commit a ledger entry, and only then contend on the `processed_events` primary key. One caller raised `IntegrityError`, but both credits remained.

The root cause was the absence of one transaction owning the complete idempotent effect. The existing tests covered only sequential duplicates and did not exercise interruption or concurrent connections.

## Changed files

- `src/ledgerbox/db.py`: added a repository-owned `BEGIN IMMEDIATE` transaction context that commits only after the complete operation and rolls back the transaction on body or commit failure.
- `src/ledgerbox/service.py`: moved the processed check, ledger insert, checkpoint, and processed marker into that transaction. The public `process_credit(repository, event, checkpoint=None)` signature and result strings are unchanged.
- `tests/test_service.py`: added regressions for retry after an interruption and duplicate delivery through two concurrent SQLite connections.
- `RUN-REPORT.md`: recorded diagnosis, changes, evidence, limitations, and final state.

No schema, dependency, or public export was changed.

## Tests and reproductions run

Environment observed: Python 3.9.6 and SQLite 3.51.0.

Before the repair:

- `python3 -m unittest discover -s tests -v`: 4 tests passed. This confirmed the supplied suite did not cover the incident.
- Inline checkpoint/retry reproduction: the first call raised at `after_credit`; the retry returned `applied`; final `entry_count=2` and `balance=200` for a 100-cent event. Defect reproduced.
- Inline two-connection concurrent reproduction synchronized at `after_credit`: outcomes were `applied` and `IntegrityError`; final `entry_count=2` and `balance=200`. Concurrent defect reproduced.

After the repair:

- Focused interruption and concurrency tests via `python3 -m unittest ... -v`: 2 tests passed.
- `python3 -m unittest discover -s tests -v`: all 6 tests passed.
- Child-process crash reproduction using `os._exit(23)` at `after_credit`: child exit was 23; retry returned `applied`; final `entry_count=1` and `balance=100`.
- Concurrent stress reproduction using 100 distinct event IDs, each delivered simultaneously through two separate SQLite connections: every pair returned one `applied` and one `duplicate`; final aggregate contained 100 one-cent entries.

## Remaining unverified claims or risks

- Existing databases that already contain orphaned or duplicate ledger rows from incidents before this repair were not reconciled. No safe policy for choosing or removing historical financial rows was supplied, so this repair deliberately does not mutate prior data.
- Behaviour on network filesystems or unusual SQLite builds/configurations was not tested. Verification used the local filesystem and SQLite 3.51.0.
- No deployment or production-data verification was performed.

## Exact final state

Status: **verified with the limits above**.

For supported EUR events, `process_credit` now obtains SQLite's write reservation before checking the processed-event marker. Duplicate deliveries are serialized against that check. A new credit entry and its processed marker commit together; interruption or any exception before successful commit rolls both back. `"applied"` is returned only after commit succeeds, while `"duplicate"` performs no new ledger effect. Distinct event IDs continue to apply independently, and unsupported currencies remain rejected before a transaction begins.
