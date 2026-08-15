# Codebase understanding — compact

Use before significant work in an existing system.

1. **Target state.** Confirm project root, checkout/worktree, revision, dirty files, user changes, instructions, generated/vendor boundaries, and concurrent ownership.
2. **Repository map.** Identify languages, runtimes, build/package systems, entry points, packages, deployables, configuration, tests, and external interfaces.
3. **Behavioural path.** Trace the requested behaviour from entry through owner, dependencies, state and side effects, persistence or remote boundaries, failure handling, and tests.
4. **Change surface.** Name direct files/modules, callers, consumers, contracts, data, configuration, operations, and evidence likely to move.
5. **Risk neighbourhood.** Inspect compatibility, authorization, transactions, concurrency, generated code, performance, recovery, and deployment only where the path touches them.
6. **Knowledge ledger.** Mark material statements KNOWN, INFERRED, UNKNOWN, or NEEDS VERIFICATION with exact evidence references.
7. **Sufficiency.** Act only when the owner, invariants, smallest coherent surface, proof path, and important unknowns are explainable.

Do not equate a file tree, symbol search, import graph, or test list with full understanding. Use [codebase-understanding.md](codebase-understanding.md) for large, unfamiliar, cross-boundary, or high-risk systems.
