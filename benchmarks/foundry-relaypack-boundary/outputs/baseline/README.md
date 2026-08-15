# Relaypack packaging incident

Relaypack is a small Python command-line package that resolves named routes from
bundled JSON data.

The source checkout appears healthy: the supplied tests pass and the command
works when run from the repository. The published wheel does not. When an
operator installs the wheel and invokes `relaypack` from another directory, the
command fails because it cannot find its route data.

Repair the package while preserving this contract:

- `relaypack.render_route(name)` remains the public Python API.
- The `relaypack` console command remains available.
- `relaypack alpha` prints `route alpha -> https://api.example.test/v1`.
- Unknown route names still raise `KeyError` from the Python API and produce a
  non-zero CLI exit.
- Route data ships inside the wheel and is read through a package-safe
  mechanism. The installed program must not depend on the source checkout or
  current working directory.
- Do not add runtime dependencies or replace the packaging system.

Add a regression test that would have caught the published-artifact failure.
Build and exercise the actual wheel, not only the source tree.
