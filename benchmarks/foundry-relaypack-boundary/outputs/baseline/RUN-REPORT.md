# Run report

## Diagnosis

`relaypack._load_routes()` derived the repository root from `__file__` and read
`config/routes.json` from outside the Python package. The source checkout made
that path exist, but the wheel did not contain it, so an installed command could
not load its data.

## Changed surfaces

- Moved the route data from `config/routes.json` to
  `src/relaypack/routes.json`, beside the code that consumes it.
- Declared `routes.json` as package data in `setup.cfg`.
- Changed `src/relaypack/cli.py` to open the data with
  `importlib.resources.files()`, which works through the installed package
  rather than relying on a repository path or working directory.
- Added `PublishedWheelTests` in `tests/test_relaypack.py`. The regression test
  builds a wheel, checks its ZIP contents, installs it in a fresh virtual
  environment, and exercises the installed API and console script from a
  temporary directory with `PYTHONPATH` removed.

## Checks run and outcomes

1. Before the repair, `python3 -m unittest discover -s tests -v` passed the two
   source-tree tests. This confirmed that the original tests did not cross the
   packaging boundary.
2. After the repair, `python3 -m unittest discover -s tests -v` passed all three
   tests, including `test_installed_wheel_contains_and_uses_route_data`. The
   final run completed in 4.291 seconds with `OK`.
3. Independently built the artifact with
   `python3 -m pip wheel --no-deps --no-build-isolation --wheel-dir /private/tmp/relaypack-verify.twGGQ0/wheelhouse .`.
   It produced `relaypack_demo-0.1.0-py3-none-any.whl` successfully.
4. Installed that exact wheel into a fresh environment with
   `/private/tmp/relaypack-verify.twGGQ0/venv/bin/python -m pip install --no-deps --no-index /private/tmp/relaypack-verify.twGGQ0/wheelhouse/relaypack_demo-0.1.0-py3-none-any.whl`.
   Installation completed successfully as `relaypack-demo-0.1.0`.
5. `unzip -l` against the built wheel showed
   `relaypack/routes.json` in the archive (89 bytes).
6. From `/private/tmp/relaypack-verify.twGGQ0`, outside the checkout and with
   `PYTHONPATH` removed, the installed Python API printed
   `route alpha -> https://api.example.test/v1`.
7. Under the same conditions, the installed `relaypack alpha` console command
   printed `route alpha -> https://api.example.test/v1`.
8. The installed Python API raised `KeyError` for `missing`, and the installed
   `relaypack missing` command reported `unknown route: missing` and exited 2.

## Still unverified

- The repair was exercised on Python 3.9 on macOS. Other supported Python 3.9+
  versions and operating systems were not run here.
- Registry upload/download is not exercised; verification uses the locally
  built wheel that would be published.
- An isolated build that downloads build requirements was not used. The wheel
  was built with the repository's existing `setuptools` and `wheel` tooling via
  `--no-build-isolation`.
