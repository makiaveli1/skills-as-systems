# Existing-codebase repair — compact

Use when the primary task is to fix or narrowly evolve an existing website without rewriting it.

1. **Inspect first.** Identify the framework, package manager, routes, components, tokens, assets, tests, deployment rules, local changes and exact current build identity.
2. **Bound the repair.** Record the defect, reproduction, owning files, protected foundations, editable areas, permitted dependencies, line or file budget and rollback boundary.
3. **Prove the baseline.** Capture relevant before-state code, hashes, screenshots, interaction states and failing tests. Do not infer a visual or behavioural defect from source alone.
4. **Patch narrowly.** Change only the smallest responsible layer. Preserve content, routes, semantics, design tokens, approved assets, browser history, accessibility and unrelated behaviour. Do not hide overflow, remove content, disable motion globally, replace the stack or redesign the page as a shortcut.
5. **Verify both sides.** Run the failing regression, existing tests, responsive and keyboard checks, visual comparison and unaffected-path tests. Compare protected-file hashes and list every changed path.
6. **Report honestly.** Distinguish fixed, verified, visually reviewed and release-approved. Missing evidence keeps the result blocked.

Deep routes: [implementation-routing.md](implementation-routing.md), [failure-tests.md](failure-tests.md), [evidence-and-qa.md](evidence-and-qa.md).