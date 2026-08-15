# Build, dependencies, CI, packaging, compatibility, and release

## Build reality

Identify the authoritative build entry points, supported environments, generated steps, dependency locks/resolution, artifacts, and release pipeline. Prefer repository-provided commands over reconstructed shell sequences.

Verify reproducibility with the actual resolved graph and clean inputs where feasible. A local incremental build can hide missing files, undeclared dependencies, or stale generated output.

## Dependency changes

For additions/upgrades/removals record capability need, current and target resolved versions, compatibility, transitive changes, licenses, security, build/runtime impact, platform support, and rollback. Review lockfile changes; do not accept unrelated churn.

Verify current upstream documentation and release notes for version-sensitive behaviour. Do not invent APIs or assume the latest major version.

## CI discipline

Understand trigger, job graph, environment, caches, secrets, artifacts, required checks, and local reproduction limits. Diagnose the first causal failure; later failures may be downstream noise.

Do not weaken gates, skip jobs, pin stale images indefinitely, or rerun repeatedly without diagnosing flakiness. Separate product failure, test failure, infrastructure failure, and configuration failure.

## Packaging

Test the artifact users receive:

- clean build and package contents;
- install/upgrade/uninstall where relevant;
- entry points, resources, native binaries, and runtime dependencies;
- signatures, hashes, provenance, licenses, and SBOM when required;
- absence of secrets, private sources, tests, debug data, or unintended files;
- examples and consumer tests against the packaged artifact.

## Compatibility

List public contracts: API, ABI, CLI, file format, schema, protocol, configuration, environment, package, extension, platform, and operational behaviour. Define supported version skew and deprecation/removal policy.

Use consumer/contract tests and mixed-version tests. A source-compatible change may still break binary, behavioural, performance, or data compatibility.

## Cross-platform engineering

Use language-native path/process APIs and repository entry points. Account for filesystem case/symlink/permission differences, path separators, line endings, shells, architectures, locale/time zone, signals, networking, packaging, and platform security models.

Evidence from one OS, architecture, container, simulator, or browser remains scoped to that environment. Simulation is not native execution.

## Release gate

Before release verify:

- intended changes and compatibility notes;
- exact source/artifact identity and clean packaging;
- required tests and independent review;
- security/privacy and supply-chain checks;
- migration order and mixed-version safety;
- rollout, canary/feature control, monitoring, abort, and rollback/recovery;
- documentation, configuration, and support promises;
- authority for publishing or deployment.

Deployment is not release verification. Observe startup, critical journeys, telemetry, data state, and artifact/version after rollout.

## Release evidence pack

Use the verification receipt rather than inventing a separate artifact unless the project already has one. Link build, package, test, security, migration, approval, rollout, and post-release evidence by exact state.
