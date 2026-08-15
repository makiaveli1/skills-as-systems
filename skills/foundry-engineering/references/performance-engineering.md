# Performance engineering

## No baseline, no improvement claim

Define:

- user/system workload and success metric;
- representative data size, distribution, concurrency, and warm/cold state;
- environment, hardware, runtime, dependency, configuration, and build;
- latency distribution, throughput, resource, cost, startup, memory, or energy target;
- noise controls and number of samples;
- correctness invariants that optimization must preserve.

Do not optimize a convenient microbenchmark when the product bottleneck lies elsewhere.

## Measure and localize

1. Establish reproducible baseline and variance.
2. Measure end-to-end user or system path.
3. Profile to locate time, allocations, I/O, contention, network, rendering, query, or cache cost.
4. Form a causal hypothesis.
5. Change one material mechanism.
6. Re-run the same workload/environment.
7. Check correctness, regressions, and resource trade-offs.

Use distributions and tail behaviour where averages hide user impact.

## Common surfaces

Inspect only when evidence points there:

- algorithmic complexity and data structures;
- repeated work, allocation, serialization, copying, and parsing;
- database plans, round trips, batching, indexes, locks, and transaction length;
- network payload, connection reuse, caching, compression, and concurrency;
- blocking, lock contention, queueing, backpressure, and scheduler overhead;
- frontend bundle/media, rendering, layout, main-thread work, and memory leaks;
- startup, dynamic loading, compilation, and initialization;
- cache hit quality, invalidation correctness, staleness, and memory cost.

## Optimization discipline

Prefer eliminating work before parallelizing it, and fixing ownership before adding caches. Every cache needs key, value, source of truth, invalidation, consistency, capacity, eviction, failure, and observability contracts.

Parallelism can increase contention, memory, nondeterminism, and tail latency. Prove the workload benefits and concurrency remains correct.

Do not trade correctness, security, accessibility, debuggability, or maintainability for an unimportant benchmark gain.

## Benchmark integrity

Reject:

- different workloads or builds between baseline and result;
- unrepresentative tiny inputs or warmed state;
- single-run claims;
- hidden debug/profiling overhead in only one side;
- compiler dead-code elimination or benchmark harness cost dominating the work;
- cherry-picked best samples;
- throughput improvement with unacceptable latency, memory, or error cost;
- local lab claims presented as production field impact.

## Evidence record

Capture commands/harness, revision, environment, workload, sample count, raw or summarized results, variance, profile references, correctness checks, and limitations. Classify results as lab, staging, canary, or production observation.

Performance work is complete when a real constraint moved measurably, correctness stayed intact, and the added complexity earns its ongoing cost.
