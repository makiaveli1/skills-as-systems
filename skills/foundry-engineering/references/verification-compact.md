# Verification — compact

Use before claiming completion.

## Evidence classes

- **TESTED:** a declared automated or manual check passed in a named environment and exact state.
- **OBSERVED:** behaviour or state was directly inspected at runtime or in an artifact.
- **INFERRED:** evidence supports the conclusion, but the claim was not directly exercised.
- **UNVERIFIED:** required proof was unavailable, failed, stale, or out of scope.

## Verification ladder

Select only layers that match the risk:

1. syntax, format, compile, static analysis, and types;
2. focused tests for changed behaviour;
3. regression tests for the prior failure and protected neighbours;
4. integration, contract, system, or end-to-end checks;
5. build, package, install, startup, and configuration checks;
6. runtime, UI, API, database, filesystem, queue, or external-boundary observation;
7. adversarial, security, performance, reliability, concurrency, and recovery evidence;
8. final diff, artifact identity, worktree state, and evidence freshness.

## Claim rules

- Green unit tests do not prove integration or deployment.
- A build does not prove runtime behaviour.
- A screenshot does not prove interaction or accessibility.
- A scanner does not prove security.
- A benchmark without comparable baseline, workload, and environment does not prove improvement.
- A mocked boundary does not prove the real boundary.
- A passing test that misses the product path is not completion evidence.

Record commands/actions, environment, exact state, outcomes, and limitations. Use `schemas/verification-receipt.schema.json` for significant or resumable work. Read [testing-and-evidence.md](testing-and-evidence.md) for deeper strategy.
