# SITECRAFT deep baseline study

For a shorter explanation of the benchmark and where to find each public artifact, start with the [CAIRN overview](../README.md).

## Plain result

SITECRAFT clearly changed how the agent worked, but this study does **not** prove
a repeatable output-quality win. All four candidates passed the same static and
headless-browser acceptance checks. The named-skill condition had a higher
average visual score, but the repetitions split:

- the two SITECRAFT candidates averaged **22/25** in the blind visual review;
- the two baseline candidates averaged **18.5/25**;
- the blind reviewer ranked a SITECRAFT candidate first;
- repetition one favored SITECRAFT by 9 points, while repetition two favored
  baseline by 2 points;
- both SITECRAFT runs reopened the skill in all three project stages instead of
  using it only at the beginning.

The average uplift is promising, but it does not satisfy the predeclared rule
that both skilled repetitions must improve before calling a skill advantage.
The supported conclusion is narrower: SITECRAFT reliably changed lifecycle
behavior and may improve visual quality, but more repetitions are needed to
separate skill effect from run-to-run model variation.

## Conditions

- Model: `gpt-5.4`
- Reasoning effort: `high`
- Harness: Codex CLI `0.147.0`
- SITECRAFT: `0.4.0`
- Conditions: baseline and named skill only
- Replicates: two per condition
- Stages per replicate: initial build, changed user evidence, late QA repair
- Browser evidence: headless Chrome at 1440×1000, 390×844, and 320×800, plus
  no-JavaScript content, keyboard interaction, closed-route safety,
  confirmation guards, focus, and reduced motion

The product evaluator was calibrated to the documented automation hooks and to
safe equivalent implementations, then frozen and rerun against all four
unchanged candidates. Raw model transcripts and private reasoning are not part
of the public evidence. The compact `execution-summary.json` records cumulative
host token counters, completed-command counts, and skill-read events without
publishing commands or reasoning.

## Functional acceptance

| Candidate | Condition | Static checks | Browser checks |
|---|---|---:|---:|
| baseline-1 | Baseline | Pass | Pass |
| baseline-2 | Baseline | Pass | Pass |
| skilled-1 | SITECRAFT | Pass | Pass |
| skilled-2 | SITECRAFT | Pass | Pass |

## Blind visual review

The reviewer received desktop and mobile screenshots labeled only A–D. The
condition map was revealed after grading.

| Blind label | Candidate | Condition | Score / 25 | Rank |
|---|---|---|---:|---:|
| C | skilled-1 | SITECRAFT | 24 | 1 |
| D | baseline-2 | Baseline | 22 | 2 |
| A | skilled-2 | SITECRAFT | 20 | 3 |
| B | baseline-1 | Baseline | 15 | 4 |

The reviewer found `skilled-1` strongest because it combined a brief-specific
identity with the clearest end-to-end planning flow on desktop and mobile. The
full review is in `blind-visual-review.json`.

## Evidence boundary

This study supports a narrow conclusion: for this evolving static web-product
task, SITECRAFT preserved full functional acceptance, produced a higher average
blind visual score, and remained active when evidence changed. The split
repetitions mean the output-quality result is inconclusive under the study's
own repeatability rule. It does not establish production readiness,
screen-reader behavior, native-device behavior, cross-browser coverage, or
superiority across every web task or model.
