# Clean-install release failure

The source checkout passes, but a wheel installed into an empty environment
fails on `parcelhouse --db fresh.db init`:

```text
FileNotFoundError: .../config/schema.sql
```

Release requires a wheel that contains everything needed at runtime and works
when invoked from a directory unrelated to the source checkout. Preserve the
public API, migration behaviour, CLI names, and dependency boundary. Add a
permanent regression that builds and inspects the wheel, installs it into a
clean virtual environment, initializes a database outside the checkout, and
exercises at least one success and one failure/state-guard path. Avoid tests
that pass by importing the source tree.
