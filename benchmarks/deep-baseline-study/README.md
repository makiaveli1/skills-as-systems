# Deep baseline study

This study compares a strong Codex baseline with the same Codex deliberately
using one named skill. It asks whether the skill improves the work, changes the
process in a useful way, or introduces costs or regressions.

It does **not** compare different models or competing skill systems.

## Current status

| Skill study | Status | Result |
| --- | --- | --- |
| [SITECRAFT / CAIRN](sitecraft/) | **Complete** | All four candidates passed functional acceptance. SITECRAFT averaged 22/25 in blind visual review versus 18.5/25 for baseline, but the paired repetitions split. The higher average is promising, not proof of a repeatable output advantage. |
| [FOUNDRY](foundry/) | **Pending** | The scenario, staged prompts, and evaluator are public. An interrupted pilot is excluded and final candidates must restart from clean seeds before any score is published. |

For SITECRAFT, start with the [CAIRN overview](sitecraft/), then open the
[detailed result and evidence](sitecraft/results/RESULTS.md).

## Study design

Each skill study uses:

- baseline and named-skill conditions only;
- two independent runs per condition;
- three turns per run;
- new project evidence injected between turns;
- the same Codex CLI version, model, reasoning setting, prompts, seed, sandbox,
  and time limits across conditions;
- deterministic task-specific acceptance checks;
- blind visual review where visual quality is part of the task;
- separate reporting for outcome, reliability, unnecessary change, evidence
  honesty, lifecycle behavior, and execution cost.

The skilled prompt explicitly invokes the installed skill throughout the task.
The baseline prompt contains no replacement framework. Public trace summaries
record only bounded events such as skill reads and completion markers. Raw model
reasoning is neither required nor published.

## Three-stage lifecycle

Every run continues through the same project lifecycle:

1. **Initial work:** build or repair from the frozen starting brief.
2. **Changed evidence:** inject new information that should cause the agent to
   revisit earlier assumptions.
3. **Late verification:** introduce a final QA or incident signal and require a
   justified completion decision.

This design tests whether a skill remains useful after the opening plan instead
of acting only as a one-time prompt.

## Repository layout

```text
deep-baseline-study/
├── README.md                 This overview
├── protocol.json             Shared run configuration
├── sitecraft/
│   ├── README.md             CAIRN result overview
│   ├── seed/                 Frozen starting project
│   ├── prompts/              Frozen staged prompts
│   ├── stimuli/              Evidence injected between stages
│   ├── evaluation/           Static, browser, and blind-review tooling
│   └── results/              Final candidates, screenshots, receipts, and result
└── foundry/
    ├── seed/                 Frozen starting project
    ├── prompts/              Frozen staged prompts
    ├── stimuli/              Incident evidence
    └── evaluation/           Public evaluator and hidden acceptance checks
```

A study without a `results/` directory is not treated as complete.

## Interpretation boundary

Repeated runs can reveal differences on these projects. They cannot prove a
universal advantage across every model, repository, or website. Report sample
size, paired differences, counterexamples, and unverified areas plainly rather
than turning the study into a universal leaderboard.
