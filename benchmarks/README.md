# Codex showcase benchmarks

These paired showcases test whether an installed skill changes a fresh Codex agent's work on the same project and request.

They are examples, not universal model leaderboards. One paired run can demonstrate concrete differences in that run; it cannot prove that every model, host, or task will behave the same way.

## Clean-room rules

1. Freeze the seed, task prompt, rubric, and evaluator before either condition runs.
2. Give each condition a separate copy of the seed.
3. Install the named skill only in the skilled workspace.
4. Do not give either author the rubric's hidden checks, the other condition's output, or an expected implementation.
5. Record the Codex model, date, environment, skill version, prompt, output, commands, and limitations.
6. Run deterministic checks before subjective review.
7. Keep authoring and grading separate where practical.
8. Publish final artifacts and concise findings, not private reasoning transcripts.
9. Label a result `TESTED`, `OBSERVED`, `INFERRED`, or `UNVERIFIED` according to its actual evidence.
10. Never generalize one showcase into a universal claim.

## Included showcases

- [`sitecraft-tideglass`](sitecraft-tideglass/): build a responsive public-safety web experience from a sparse brief.
- [`foundry-ledger-repair`](foundry-ledger-repair/): diagnose and repair a durable-state retry/concurrency defect in an unfamiliar Python repository.
- [`foundry-relaypack-boundary`](foundry-relaypack-boundary/): repair a package that passes source tests but fails after wheel installation.

Each showcase contains the frozen seed and prompt, the predeclared rubric, the resulting baseline and skilled projects, deterministic evidence, screenshots or diffs where relevant, and a concise comparison receipt.

## Conditions

`baseline` receives only the seed and task prompt.

`skilled` receives the same seed and task prompt plus an installed copy of the named skill. The invocation tells Codex where the installed `SKILL.md` is; it does not summarize the skill or reveal the evaluator.

## Reproducing a run

Use a fresh Codex task for every condition. Copy only the showcase's `seed/` directory into a new workspace, then use the relevant prompt from its `prompt.md`. Preserve the complete output directory and report the exact model and host version.

Model output is nondeterministic. Repeat runs before drawing broader conclusions.

## First published run

| Showcase | Baseline | With skill | What this run supports |
| --- | ---: | ---: | --- |
| TIDEGLASS | 97.5/100 | 97/100 | Both builds were excellent; this run supports visual and functional parity, not SITECRAFT superiority. |
| Ledgerbox | 100/100 | 100/100 | Both repaired the transaction boundary; FOUNDRY produced broader crash/concurrency evidence. |
| Relaypack | 100/100 | 100/100 | Both repaired and tested the installed wheel; the baseline regression covered more of the permanent API/CLI contract. |

These are intentionally honest results. Modern coding agents can solve bounded,
well-specified work without a skill. The examples are useful because they expose
where the skills affect method and evidence—and where they add no measurable
score in one run. They should not be advertised as a universal ranking.

The paired runs used SITECRAFT 0.3.0 and FOUNDRY 0.2.0. Findings informed
SITECRAFT 0.3.1 and FOUNDRY 0.2.1; the revised versions have structural regression
coverage but are not retroactively credited with these outputs.
