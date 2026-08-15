# Interfaces, services, CLIs, and libraries

## Interface contract

For any public or cross-boundary interface define:

- consumers and trust level;
- inputs, validation, normalization, and limits;
- outputs and stable semantics;
- errors, status, exit codes, and retryability;
- versioning and compatibility;
- idempotency, ordering, pagination, and cancellation;
- security, privacy, rate, and resource boundaries;
- observability without secret or sensitive-data leakage.

Examples and generated clients do not replace the contract.

## API engineering

Preserve resource/operation semantics across transport details. Use stable identifiers, bounded payloads, explicit partial failure, and consistent error shapes. Distinguish authentication from authorization and validate object/action scope server-side.

For retries, declare which operations are idempotent and how keys are scoped, stored, expired, and replayed. For pagination, define ordering and cursor consistency. For asynchronous operations, expose durable identity and terminal states.

Compatibility includes fields, defaults, enum expansion, nullability, status/error behaviour, ordering, rate limits, and side effects—not just endpoint paths.

## Service engineering

Give each service a clear state/data owner and failure domain. Network boundaries require:

- timeouts and cancellation;
- bounded retries with jitter and budgets;
- overload and backpressure policy;
- health/readiness semantics;
- dependency failure handling;
- trace/log/metric correlation;
- version-skew and rollout compatibility;
- recovery and data reconciliation.

Avoid a service boundary created solely to mirror an internal class.

## CLI engineering

Treat the CLI as a scriptable public interface:

- stable commands, flags, environment/config precedence, output modes, and exit codes;
- stdout for requested output, stderr for diagnostics;
- non-interactive behaviour and explicit prompts;
- safe defaults, dry-run/preview where valuable, and clear destructive confirmation;
- shell-independent path and quoting behaviour;
- cancellation and partial-output cleanup;
- machine-readable output with versioned schema when automation depends on it.

Test from an installed artifact, not only an in-repository function call.

## Library/package engineering

Minimize public surface. Separate stable API from internal implementation. Define runtime/platform/dependency support, thread/async safety, resource ownership, error contracts, and deprecation policy.

Test:

- clean installation and import/link;
- representative downstream consumer usage;
- supported versions/platforms;
- package contents and accidental private/secret files;
- backwards compatibility or intentional break;
- examples against the published artifact.

Do not infer compatibility from semantic version numbers alone; verify the public contract and actual consumers.

## Interface review

Ask:

- Can invalid or unauthorized state cross the boundary?
- Is failure actionable and non-sensitive?
- Can old and new versions coexist?
- Are retry and cancellation semantics safe?
- Is the interface smaller than the implementation detail it exposes?
- Can consumers test against it without reproducing the provider?
- Does documentation match the exact shipped artifact?
