# Relaypack packaging repair run report

## Diagnosis

- **Symptom (OBSERVED):** source-checkout tests passed, but a wheel installed in a fresh virtual environment failed when `relaypack alpha` was run from `/private/tmp`.
- **Proximate cause (OBSERVED):** the installed loader derived `config/routes.json` from the installed module path and raised `FileNotFoundError` for `<venv>/lib/python3.9/config/routes.json`.
- **Root cause (OBSERVED):** route data lived outside the `relaypack` package, was not declared as package data, and therefore was absent from the wheel. Runtime lookup also depended on repository layout rather than a package-resource boundary.
- **Contributing condition (KNOWN):** the original unit tests inserted `src/` into `sys.path` and exercised only the checkout, so they could not detect missing wheel contents or an installed console-command failure.

## Changed surfaces

- Moved the route data from `config/routes.json` to `src/relaypack/routes.json`, making the package the single owner of the runtime resource.
- Declared `routes.json` in `setup.cfg` under `[options.package_data]`; no dependency or packaging-backend change was made.
- Changed `src/relaypack/cli.py` to open the data via `importlib.resources` instead of deriving a repository-relative filesystem path.
- Added `tests/test_wheel.py`. The regression builds a wheel, installs it into a fresh virtual environment, changes to a directory outside the checkout, invokes the installed `relaypack` entry point, and asserts its output.

## Checks and outcomes

Environment: Darwin 25.2.0 arm64, Python 3.9.6, pip 21.2.4, pytest 8.4.2. This supplied directory has no Git metadata, so a revision identifier and Git diff/status are unavailable.

### Before repair

- `python3 -m unittest discover -s tests -v` — **PASS**, 2 tests. This established that the checkout-only suite did not reproduce the packaging boundary.
- `python3 -m pip wheel . --no-deps --no-build-isolation --wheel-dir /private/tmp/foundry-relaypack-skilled-baseline` — **PASS**; built `relaypack_demo-0.1.0-py3-none-any.whl` with SHA-256 `b16ee6b267ec2a84b688b7acdffeb0df5e2410fc49d9d23883b11d6217bacb13`.
- `unzip -l /private/tmp/foundry-relaypack-skilled-baseline/relaypack_demo-0.1.0-py3-none-any.whl` — **OBSERVED FAILURE CONDITION**; the 7-file wheel contained Python modules and metadata but no JSON route data.
- Installed that baseline wheel into a new virtual environment and ran `relaypack alpha` from `/private/tmp` — **EXPECTED FAIL**, exit 1 with `FileNotFoundError` for the virtual environment's nonexistent `config/routes.json`.

### After repair

- `python3 -m unittest tests.test_relaypack -v` — **PASS**, 2 source/API tests.
- `python3 -m unittest tests.test_wheel -v` — **PASS**, 1 wheel build/install/console regression test.
- `python3 -m pytest -q -p no:cacheprovider` — **PASS**, 3 tests in 4.44 seconds. This was the final full-suite run with cache generation disabled.
- `python3 -m pip wheel . --no-deps --no-build-isolation --wheel-dir /private/tmp/foundry-relaypack-skilled-final` — **PASS**; built the repaired wheel with SHA-256 `b9deae0b7f6c2abf15df270a0f61c6025eeeac96ed523e81d80b505df847f0b7`.
- `unzip -l /private/tmp/foundry-relaypack-skilled-final/relaypack_demo-0.1.0-py3-none-any.whl` — **PASS/OBSERVED**; the 8-file wheel contains `relaypack/routes.json` and does not include the test suite or repository-level configuration.
- Installed the repaired wheel into a new virtual environment, changed to `/private/tmp`, and ran `relaypack alpha` — **PASS**; stdout was exactly `route alpha -> https://api.example.test/v1`.
- From that same installed wheel, asserted `relaypack.render_route("alpha")` and that `relaypack.render_route("missing")` raises `KeyError` — **PASS**.
- From that same installed wheel, ran `relaypack missing` — **PASS for failure contract**; exit 2 with `relaypack: error: unknown route: missing`.

## Still unverified

- Execution was verified on the stated Darwin arm64/Python 3.9 environment only; other supported Python versions and operating systems were not exercised.
- The build used the environment's installed build tooling with `--no-build-isolation` because the `build` frontend is not installed. A network-isolated clean build environment was not exercised.
- No package index publication or post-publication download was performed; publishing was outside the requested and available authority.
