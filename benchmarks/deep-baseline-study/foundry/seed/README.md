# Parcelhouse

Parcelhouse is a small durable job ledger used by a local delivery service. It
stores jobs in SQLite, lets workers lease the next queued job, and records one
delivery result per job.

## Public compatibility

The functions exported from `parcelhouse.__init__` and the existing CLI command
names are public. Existing callers use Python 3.10 through 3.12. Keep the
project dependency-free at runtime.

Run tests from the project root:

```text
python -m unittest discover -s tests -v
```

Builds use standard Python packaging metadata. Production creates databases
with `parcelhouse.initialize(path)`; existing database files must remain usable.
