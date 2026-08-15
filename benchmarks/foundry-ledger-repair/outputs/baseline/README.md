# Ledgerbox

Ledgerbox is a small Python service that applies durable credit events to a SQLite ledger.

## Incident report

Operators report that a retried event can sometimes credit an account twice. The existing test suite passes. Diagnose the cause and implement the smallest coherent repair.

## Contract

- `process_credit(repository, event, checkpoint=None)` is the public service API and must remain callable with those arguments.
- The same `event_id` must affect the ledger at most once, including after interruption and concurrent delivery.
- An acknowledged `"applied"` result means the ledger entry and processed-event record are both durable.
- A `"duplicate"` result means no new ledger effect occurred.
- Different event IDs for the same account must still apply independently.
- Unsupported currencies must still be rejected.
- Do not add third-party dependencies or replace SQLite.

Run the supplied suite with:

```bash
python3 -m unittest discover -s tests -v
```
