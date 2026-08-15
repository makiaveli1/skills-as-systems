# Codebase understanding

## Contents

[Purpose](#purpose) · [progressive map](#progressive-map) · [search](#search-discipline) · [knowledge](#knowledge-ledger) · [large repositories](#large-repository-bounding) · [sufficiency](#understanding-sufficiency-test) · [artifact](#system-map-artifact) · [failures](#failure-patterns)

## Purpose

Build the minimum accurate model needed to act safely. The goal is neither exhaustive ingestion nor a decorative architecture summary.

## Progressive map

### Layer 0: exact state

Establish:

- project/root identity and nested repositories;
- current checkout, branch/revision, worktree, submodules, and dirty state;
- applicable project instructions and protected files;
- generated, vendored, mirrored, cached, and build-output directories;
- other active writers or automation when relevant.

Stop before writes if two plausible roots, checkouts, or owners remain.

### Layer 1: repository shape

Map only facts that route later inspection:

- languages, runtimes, compilers/interpreters, framework versions;
- build, package, workspace, dependency, and lock systems;
- applications, libraries, services, jobs, CLIs, tests, tooling, and infrastructure;
- deployment and release boundaries;
- primary configuration and documentation entry points.

Prefer manifests and actual commands over filename assumptions.

### Layer 2: subsystem neighbourhood

For the relevant subsystem identify:

- purpose and public entry points;
- inbound callers and outbound dependencies;
- internal boundaries and extension points;
- data/state owned versus borrowed;
- external interfaces and side effects;
- tests, fixtures, observability, and operational controls;
- maintainers or historical decisions when discoverable.

### Layer 3: behavioural path

Trace the concrete path, not a generic component description:

1. trigger or input;
2. parsing and validation;
3. authorization or policy;
4. orchestration;
5. domain owner;
6. state transition and side effects;
7. persistence, message, filesystem, or network boundary;
8. response, rendering, or emitted artifact;
9. error, cancellation, retry, recovery, and observability path;
10. existing proof.

Read implementations on both sides of a boundary. A declared interface does not prove every implementation or caller follows it.

### Layer 4: change and risk surface

Record:

- direct owners and files;
- callers, consumers, schemas, protocols, and public compatibility;
- tests and fixtures that encode intended behaviour;
- data, migrations, configuration, deployment, and operational impact;
- concurrency, ordering, resource, security, and recovery risks;
- unaffected neighbours that need regression protection.

## Search discipline

Use several evidence shapes:

- names and symbols;
- user-visible strings, error text, routes, flags, schema fields, and event names;
- imports/references/callers;
- configuration and dependency declarations;
- tests and fixtures;
- history, blame, design records, and release notes when present;
- runtime logs/traces/state only when needed.

Treat index, language-server, and search results as potentially incomplete or stale. Confirm material conclusions in current source or runtime state.

## Knowledge ledger

For every load-bearing statement record:

- `statement`;
- `status`: KNOWN, INFERRED, UNKNOWN, NEEDS VERIFICATION;
- `evidence`: exact path, symbol, command output, test, runtime observation, or official source;
- `impact_if_wrong`;
- `next_check` when material.

Examples:

- KNOWN: `OrderService calls PaymentPort before persisting confirmation` — observed in current source and focused test.
- INFERRED: `all writers use OrderService` — repository search found no other writer, but runtime plugins were not enumerated.
- UNKNOWN: `production retries this webhook` — deployment configuration unavailable.
- NEEDS VERIFICATION: `migration is non-blocking` — database version and table size could change the result.

## Large-repository bounding

Use a frontier, not whole-repository loading:

1. seed with requested behaviour, failing test, entry point, or public contract;
2. expand one edge outward through calls, data, state, or configuration;
3. add a node only if it can own, constrain, break, or verify the change;
4. record unopened but relevant edges;
5. stop at stable boundaries whose contracts and failure behaviour are sufficient.

Keep repository map, subsystem map, behavioural path, change surface, and risk surface distinct. A subsystem can be well understood while the full repository remains only partially mapped.

## Understanding sufficiency test

Answer without guessing:

- What behaviour exists now and where was it observed?
- Who owns it?
- Which entry points and consumers matter?
- What state, data, or side effects change?
- Which invariants and compatibility promises apply?
- Which code is generated or externally owned?
- What is the smallest coherent intervention?
- What could break outside the direct files?
- How will failure and success be observed?
- Which material unknowns remain, and why are they acceptable?

If a missing answer could select a different owner or make the change unsafe, continue understanding.

## System Map artifact

Use [../schemas/system-map.schema.json](../schemas/system-map.schema.json) when work is large, shared, resumable, or likely to cross boundaries. Keep it factual and pointer-rich. Refresh or mark stale after material repository changes; do not turn it into a second source tree.

## Failure patterns

Reject:

- reading two obvious files and inventing the rest;
- loading the whole repository without a frontier;
- assuming a test name proves the implementation path;
- treating imports as runtime call ownership;
- ignoring configuration, data, generated files, or deployment boundaries;
- trusting an old handoff over current state;
- assuming a clean Git tree means no concurrent worker owns the checkout;
- editing a generated file because it is the first search hit.
