# Review and refactoring

## Review from consequence

Review the exact change and its context. Begin with findings, not a summary or score.

Inspect in this order when relevant:

1. requirement and behaviour correctness;
2. data loss, security, privacy, money, safety, and irreversible actions;
3. state ownership, concurrency, transactions, retries, and failure handling;
4. public compatibility and integration boundaries;
5. regression coverage and test integrity;
6. reliability, observability, performance, and resource lifecycle;
7. maintainability, clarity, duplication, and architecture fit;
8. style covered by project convention.

## Finding shape

Every actionable finding should contain:

- exact location and observed behaviour;
- triggering conditions;
- user or system consequence;
- why existing checks miss it;
- severity based on impact and likelihood;
- smallest repair direction;
- evidence needed to close it.

Do not present speculation as a defect. Label questions and uncertain risks clearly.

## Review boundaries

Do not demand a rewrite because another design is preferred. Accept local convention when several approaches are valid and the change improves code health. Separate blocking issues from non-blocking improvements and unrelated existing debt.

Review tests as production code. Catch assertions that no longer protect the requirement, mocks that remove the real boundary, snapshots updated without scrutiny, and fixtures that overfit one path.

## Behaviour-preserving refactoring

Before refactoring:

- define preserved observable behaviour and explicitly accepted changes;
- identify callers, consumers, serialization, timing, error, and performance contracts;
- create characterization tests where intent is not otherwise evidenced;
- isolate generated/vendor code and user changes;
- choose reversible steps with reviewable diffs.

Refactoring is not a license to repair hidden bugs silently. If current behaviour is defective, open a Repair contract and test the intended change.

## Safe sequence

1. Establish baseline and characterization.
2. Add or strengthen a seam without changing behaviour.
3. Move one responsibility or dependency at a time.
4. Keep old and new paths equivalent during transition when necessary.
5. Run focused and consumer regression checks after each coherent step.
6. Remove compatibility paths only after every consumer is verified.
7. Compare final public behaviour, performance where material, and diff scope.

## Abstraction test

Extract only when there is evidenced shared policy, lifecycle, variation, or change pressure. Similar syntax is not automatically the same responsibility.

A good abstraction:

- has a precise name and owner;
- reduces semantic duplication;
- makes invalid states harder;
- preserves useful local differences;
- does not require callers to know hidden implementation categories;
- remains testable at its contract.

Reject premature generic interfaces, configuration objects that hide every decision, giant utility modules, and inheritance used only to share a few lines.

## Technical debt

Classify debt by consequence: defect risk, change amplification, operational cost, security exposure, performance cost, onboarding cost, or obsolete dependency. Pay debt inside a feature only when it directly reduces that feature's risk or change surface. Track unrelated debt separately with evidence, not opportunistic rewrites.

## Completion

Refactoring is complete only when:

- preserved behaviours remain evidenced;
- accepted behaviour changes are explicit;
- consumers and integration paths still work;
- old paths and dead compatibility code are removed or intentionally retained;
- observability and operational ownership remain clear;
- the final structure is simpler under the actual change pressure.
