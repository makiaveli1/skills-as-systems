# Public benchmark studies

This directory tests a simple question: **does installing and deliberately using
a named skill change the quality or reliability of a fresh coding agent's work
on the same task?**

The studies compare a strong baseline against the named skill. They are not model
leaderboards, and a single higher score is not treated as proof of general
superiority.

## Current status

| Study | Status | Baseline | With skill | Supported conclusion |
| --- | --- | ---: | ---: | --- |
| [CAIRN / SITECRAFT](deep-baseline-study/sitecraft/) | Complete | 18.5/25 visual average | **22/25 visual average** | All four candidates passed functional acceptance. The visual average favors SITECRAFT, but the two paired comparisons split, so repeatable output superiority is not proven. |
| [Deep FOUNDRY study](deep-baseline-study/) | Pending | Not scored | Not scored | Scenario and evaluator are public. An interrupted pilot is excluded and clean reruns are still required. |
| [Ledgerbox](foundry-ledger-repair/) | Historical bounded example | 100/100 | 100/100 | Correctness parity; FOUNDRY collected wider crash and concurrency evidence. |
| [Relaypack](foundry-relaypack-boundary/) | Historical bounded example | 100/100 | 100/100 | Correctness parity; baseline kept broader permanent regression coverage. |

The old SITECRAFT showcase has been superseded by CAIRN. The two older FOUNDRY
examples remain only until the deeper FOUNDRY study is complete.

## CAIRN in plain English

CAIRN uses two independent baseline runs and two independent SITECRAFT runs. Each
run continues through three stages: an initial build, changed user evidence, and
a late QA repair.

Every candidate passed the same static and browser checks. The blind visual
scores were:

| Candidate | Condition | Score / 25 |
| --- | --- | ---: |
| skilled-1 | SITECRAFT | **24** |
| baseline-2 | Baseline | **22** |
| skilled-2 | SITECRAFT | **20** |
| baseline-1 | Baseline | **15** |

That produces averages of **22/25 for SITECRAFT** and **18.5/25 for baseline**.
However, pairing the corresponding repetitions gives +9 for SITECRAFT in the
first pair and -2 in the second. The benchmark therefore reports the higher
average as promising, while leaving the output-quality conclusion inconclusive
under its own repeatability rule.

Both SITECRAFT runs reopened the skill during all three stages. That is a
separate lifecycle result and should not be confused with the visual score.

See the [CAIRN overview](deep-baseline-study/sitecraft/) for the easiest entry
point, then the [full result](deep-baseline-study/sitecraft/results/RESULTS.md)
for the detailed evidence.

## Clean-room rules

1. Freeze the seed, task prompt, rubric, and evaluator before either condition runs.
2. Give every candidate a separate copy of the same seed.
3. Install the named skill only in the skilled workspace.
4. Do not give either author hidden evaluator checks, another candidate's output, or an expected implementation.
5. Record the model, host version, date, environment, skill version, prompt, output, commands, and limitations.
6. Run deterministic checks before subjective review.
7. Keep authoring and grading separate where practical.
8. Publish final artifacts and concise findings, not private reasoning transcripts.
9. Label claims according to their real evidence and keep unverified claims unverified.
10. Never generalize one benchmark into a universal claim.

## Conditions

`baseline` receives the seed and task prompt, with no substitute methodology.

`skilled` receives the same seed and task plus an installed copy of the named
skill. The prompt points the agent to the installed skill; it does not summarize
the skill or reveal the evaluator.

The deeper study uses the same Codex CLI version, model, reasoning setting,
prompts, seed, sandbox, and time limits for both conditions.

## Reproducing the deeper study

Start with [deep-baseline-study](deep-baseline-study/). Its `protocol.json`
records the run configuration. Each completed project keeps the frozen seed,
staged prompts, injected evidence, evaluator, final candidate projects, and
public result receipts.

Model output is nondeterministic. Repeat runs and report paired differences as
well as averages before drawing broader conclusions.

## Interpretation boundary

These benchmarks can show what happened on these projects under the recorded
conditions. They cannot prove that every model, host, repository, or website
will behave the same way. Modern coding agents can solve bounded tasks without a
skill, and a useful skill should be allowed to produce parity, mixed evidence,
or even a losing repetition without the result being hidden.

CAIRN used SITECRAFT 0.4.0. The two historical FOUNDRY examples used FOUNDRY
0.2.0 and informed 0.2.1. Newer versions are never retroactively credited with
older outputs.
