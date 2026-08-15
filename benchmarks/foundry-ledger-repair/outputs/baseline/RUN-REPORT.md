# Ledgerbox run report

## Diagnosed cause

`connect()` enables SQLite autocommit, while `process_credit()` previously performed the ledger insert and processed-event insert as separate statements. If the process was interrupted at the existing `after_credit` checkpoint, the ledger insert was already durable but no processed-event record existed. A retry therefore passed `has_processed()` and inserted a second credit. The separate check and writes also allowed two connections delivering the same event concurrently to observe it as unprocessed before either recorded the marker.

The repair wraps the processed-event check, ledger insert, checkpoint, and processed-event insert in one `BEGIN IMMEDIATE` transaction. An interruption rolls back both writes. Competing SQLite writers are serialized, so a waiting delivery rechecks the processed-event record after the winning transaction commits. `"applied"` is returned only after the transaction commits.

## Changed files

- `src/ledgerbox/db.py`: added a repository transaction context that starts an immediate SQLite transaction, commits successful work, and rolls back failures.
- `src/ledgerbox/service.py`: made the existing credit/deduplication workflow one atomic transaction without changing the public function signature or result values.
- `tests/test_service.py`: added regression coverage for interruption followed by retry and for concurrent delivery through separate connections.
- `RUN-REPORT.md`: recorded the diagnosis, changes, verification, risks, and final state.

## Tests and reproductions run

### Before the repair

- `python3 -m unittest discover -s tests -v` — PASS: 4 tests passed, confirming the supplied suite did not expose the incident.
- Direct interruption/retry reproduction using the public API and a checkpoint that raised at `after_credit` — reproduced the defect: `retry=applied balance=5000 entries=2` for a 2500-cent event.

### After the repair

- `python3 -m unittest discover -s tests -v` — PASS: 6 tests passed. This includes the new interruption/retry and concurrent duplicate-delivery regressions, plus all four original behavior tests.
- Durability check using the public API, closing the database after `"applied"`, reopening it, and retrying the same event — PASS: `initial=applied`, then `retry=duplicate balance=2500 entries=1`.

## Remaining unverified claims or risks

- No literal operating-system process kill or power-loss test was run; interruption was injected by raising from the provided checkpoint. SQLite crash recovery itself was not independently tested.
- High-contention behavior beyond the configured five-second SQLite busy timeout was not load-tested. Such contention may surface a SQLite timeout error, but the transaction prevents a partial or duplicate credit.

## Exact final state

- `process_credit(repository, event, checkpoint=None)` retains its public signature.
- EUR credits for distinct event IDs still apply independently.
- Unsupported currencies are still rejected before persistence work begins.
- A successful event commits its ledger entry and processed-event marker together and returns `"applied"` only after commit.
- A retry after interruption cannot observe a committed partial credit; the interrupted attempt rolls back, and the retry applies exactly once.
- Concurrent delivery of one event ID produces one `"applied"` result and one `"duplicate"` result, with one ledger entry.
- The complete test suite passes: 6 tests, 0 failures, 0 errors.
