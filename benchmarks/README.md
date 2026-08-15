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

## Current deeper study

[`deep-baseline-study`](deep-baseline-study/) uses only baseline and named-skill
conditions, with two independent runs and three changing project stages per
run.

- **SITECRAFT / CAIRN is complete.** All four candidates passed the same
  functional checks. SITECRAFT averaged 22/25 in blind visual review and
  baseline averaged 18.5/25, but the two paired comparisons split. Under the
  predeclared repeatability rule, output superiority remains inconclusive.
- **FOUNDRY is pending.** Its seed, staged prompts, incidents, and evaluator are
  available for inspection. An interrupted pilot is excluded and no result is
  claimed until every condition restarts from a clean seed.

The repository temporarily retains two earlier, bounded FOUNDRY examples:

- [`foundry-ledger-repair`](foundry-ledger-repair/): a durable-state retry and
  concurrency repair;
- [`foundry-relaypack-boundary`](foundry-relaypack-boundary/): a package that
  passes source tests but fails after wheel installation.

These older examples will be replaced when the deeper FOUNDRY study is complete.
The old SITECRAFT showcase has already been superseded by CAIRN.

## Conditions

`baseline` receives only the seed and task prompt.

`skilled` receives the same seed and task prompt plus an installed copy of the named skill. The invocation tells Codex where the installed `SKILL.md` is; it does not summarize the skill or reveal the evaluator.

## Reproducing a run

Use a fresh Codex task for every condition. Copy only the showcase's `seed/` directory into a new workspace, then use the relevant prompt from its `prompt.md`. Preserve the complete output directory and report the exact model and host version.

Model output is nondeterministic. Repeat runs before drawing broader conclusions.

## Current results

| Study | Baseline | With skill | What the evidence supports |
| --- | ---: | ---: | --- |
| CAIRN (two runs each) | 18.5/25 average | 22/25 average | Equal functional acceptance and a higher SITECRAFT visual average, but split paired results mean no repeatable output advantage is proven. Both skilled runs used the skill again after project changes. |
| Ledgerbox (earlier bounded example) | 100/100 | 100/100 | Both repaired the transaction boundary; FOUNDRY produced broader crash and concurrency evidence. |
| Relaypack (earlier bounded example) | 100/100 | 100/100 | Both repaired and tested the installed wheel; the baseline regression covered more of the permanent API and command-line contract. |

These are intentionally honest results. Modern coding agents can solve bounded,
well-specified work without a skill. A higher average is not the same as a
repeatable win, and process differences are not automatically product-quality
differences. These studies should not be advertised as a universal ranking.

CAIRN used SITECRAFT 0.4.0. The two earlier FOUNDRY examples used 0.2.0 and
informed 0.2.1; newer versions are not retroactively credited with those
outputs.
