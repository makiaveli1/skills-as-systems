# Cancellation incident and compatibility decision

An operator cancelled a leased job after learning the address was unsafe. The
worker completed seconds later and Parcelhouse recorded the delivery anyway.

## Required state semantics

- Cancelling a queued job moves it directly to `cancelled`.
- Cancelling a leased job records `cancel_requested` and returns `True`.
- A worker attempting to complete `cancel_requested` must receive `False`; no
  delivery row may be created, and the job must become `cancelled`.
- Expiry recovery moves `cancel_requested` to `cancelled`, never back to queued.
- A different worker must never complete another worker's lease.

Existing version-1 databases are live and contain queued and leased rows. The
application must migrate them in place, preserve their data, and make repeated
initialization safe. The public Python function signatures and CLI command names
must remain compatible. Runtime dependencies remain forbidden.
