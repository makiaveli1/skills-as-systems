# Relaypack: FOUNDRY installed-artifact repair

Relaypack's source tests pass, but its wheel omits runtime JSON and the installed
CLI searches for a repository-relative file. The benchmark tests whether an
agent verifies the artifact users actually receive.

Two fresh Codex agents received the same frozen seed and prompt. The baseline
had no skill; the second used FOUNDRY 0.2.0 from an isolated workspace-local
install. Both scored **100/100**.

## What both conditions got right

Both repairs:

- moved the JSON into the Python package;
- loaded it with `importlib.resources`;
- declared package data without adding a runtime dependency;
- built and installed a wheel in an isolated environment;
- exercised the installed command outside the checkout;
- preserved successful and unknown-route behavior.

The evaluator also removed the build checkout before executing the installed
program, inspected wheel members, tested the Python API and CLI, and mutation-
tested the candidate regression against the original defect.

Compare the [baseline project](outputs/baseline/) and [FOUNDRY project](outputs/with-foundry/),
or inspect the complete [baseline](evidence/baseline.json) and
[FOUNDRY](evidence/with-foundry.json) receipts.

## What the run taught us

FOUNDRY produced a clearer before/after evidence taxonomy and explicitly scoped
the tested environment. However, the baseline's permanent regression covered
wheel contents, installed API, successful CLI, and both negative contracts,
while the FOUNDRY project's permanent test covered the installed successful CLI
and relied on its run checks for the rest.

That gap informed FOUNDRY 0.2.1: packaging repairs now require the permanent
regression itself to build, inspect, install, isolate, and exercise all incident-
relevant success and failure contracts. An external evaluator may widen proof,
but may not substitute for the test that travels with the package. Version 0.2.1
was structurally validated; these outputs remain the honest 0.2.0 run.

## Reproduce it

Copy [seed](seed/) into two isolated workspaces, use [prompt.md](prompt.md), and
install FOUNDRY only in the skilled workspace. Then run:

```bash
python3 evaluation/evaluate.py /path/to/candidate
```

The evaluator uses Python's standard library plus the environment's existing
`pip`, `setuptools`, and `wheel`. It performs no registry publication and makes
no cross-platform claim.
