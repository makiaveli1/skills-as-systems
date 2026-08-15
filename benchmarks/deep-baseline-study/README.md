# Deep baseline study

This study asks one narrow question: does installing and deliberately using the
named skill improve Codex's work compared with the same Codex without it?

It does not compare different models or competing skill systems.

## Current status

- **SITECRAFT:** complete. All four candidates passed functional acceptance;
  the named-skill condition averaged 22/25 in blind visual review versus 18.5
  for baseline, but the repetitions split and do not prove a repeatable
  advantage. Read the [results](sitecraft/results/RESULTS.md).
- **FOUNDRY:** the scenario, staged prompts, and evaluator are published for
  inspection, but the interrupted pilot is excluded and no deeper result is
  claimed yet. Final runs must restart from clean seeds.

## Design

- one SITECRAFT project and one FOUNDRY project;
- baseline and named-skill conditions only;
- two independent runs per condition;
- three turns in each run, with new files and changed evidence injected between
  turns;
- the same Codex CLI version, model, reasoning setting, prompts, seed, sandbox,
  and time limits in every condition;
- deterministic task-specific acceptance checks plus blind visual review for
  the web project;
- outcome, reliability, unnecessary change, evidence honesty, and execution
  cost reported separately rather than collapsed into a universal skill score.

The skilled prompt explicitly invokes the installed skill throughout the task.
The baseline prompt contains no substitute methodology. Trace summaries record
whether the skilled run reopened its skill or routed references after new
evidence; raw model reasoning is neither collected nor published.

See [protocol.json](protocol.json) for the run configuration. Completed project
folders contain their seeds, staged prompts, injected evidence, acceptance
checks, final outputs, and result receipts. A project without a `results/`
directory is not a completed study.

## Interpretation boundary

Repeated runs can reveal differences on these projects. They cannot prove a
universal advantage across every model, repository, or website. Report sample
size, dimensions, and counterexamples plainly rather than turning the study
into a universal leaderboard.
