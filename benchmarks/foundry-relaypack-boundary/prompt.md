# Frozen author prompts

The prompt, seed, and rubric are frozen before either run. Each author receives
an isolated copy of `seed/` and cannot see the other output or evaluator internals.

## Baseline condition

```text
Repair the packaging incident described in README.md. Work in this repository.
Preserve the stated contract, make the smallest coherent repair, add a regression
test that proves the published artifact, and verify the actual installed wheel.

Finish with RUN-REPORT.md containing: diagnosis, changed surfaces, exact checks
run and their outcomes, and anything still unverified. Do not include a hidden
reasoning transcript; record only conclusions and evidence useful to the next
engineer.
```

## FOUNDRY condition

```text
Repair the packaging incident described in README.md. Work in this repository.
Use the installed skill at .agents/skills/foundry-engineering/SKILL.md: read it
fully, follow it, and load only the references it routes for this work.
Preserve the stated contract, make the smallest coherent repair, add a regression
test that proves the published artifact, and verify the actual installed wheel.

Finish with RUN-REPORT.md containing: diagnosis, changed surfaces, exact checks
run and their outcomes, and anything still unverified. Do not include a hidden
reasoning transcript; record only conclusions and evidence useful to the next
engineer.
```
