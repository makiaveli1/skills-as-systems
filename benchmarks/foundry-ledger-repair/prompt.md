# Frozen Codex prompts

## Baseline condition

```text
Work only inside the supplied workspace; do not inspect parent or sibling directories.

Ledgerbox operators report that a retried credit event can sometimes credit an account twice even though the existing tests pass. Diagnose the cause and implement the smallest coherent repair that satisfies README.md. Preserve the public API and existing valid behavior. Add regression coverage for the real defect and verify the final state.

You may edit files and run local commands in this workspace. Do not use network access or add dependencies. Do not ask questions unless a missing decision makes safe progress impossible.

Write RUN-REPORT.md containing: diagnosed cause, changed files, tests and reproductions actually run with results, remaining unverified claims or risks, and the exact final state. Do not include hidden reasoning or a transcript.
```

## FOUNDRY condition

```text
Work only inside the supplied workspace and the installed skill directory named below; do not inspect other parent or sibling directories.

Use the installed FOUNDRY skill at .agents/skills/foundry-engineering/SKILL.md for this task. Read its SKILL.md completely, then load only the references relevant to this repair.

Ledgerbox operators report that a retried credit event can sometimes credit an account twice even though the existing tests pass. Diagnose the cause and implement the smallest coherent repair that satisfies README.md. Preserve the public API and existing valid behavior. Add regression coverage for the real defect and verify the final state.

You may edit files and run local commands in this workspace. Do not use network access or add dependencies. Do not ask questions unless a missing decision makes safe progress impossible.

Write RUN-REPORT.md containing: diagnosed cause, changed files, tests and reproductions actually run with results, remaining unverified claims or risks, and the exact final state. Do not include hidden reasoning or a transcript.
```
