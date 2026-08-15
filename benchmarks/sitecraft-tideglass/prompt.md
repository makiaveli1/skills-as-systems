# Frozen Codex prompts

## Baseline condition

```text
Work only inside the supplied workspace; do not inspect parent or sibling directories.

Build the project described in BRIEF.md completely. You may create and edit files in this workspace and run local checks. Do not ask questions unless a missing decision makes safe progress impossible. Do not use external services or network dependencies.

Verify what you can in the available environment. Put the finished website in the workspace root and write RUN-REPORT.md containing: what you built, files changed, checks actually run and their results, remaining unverified claims, and the exact next useful review. Do not include hidden reasoning or a transcript.
```

## SITECRAFT condition

```text
Work only inside the supplied workspace and the installed skill directory named below; do not inspect other parent or sibling directories.

Use the installed SITECRAFT skill at .agents/skills/sitecraft/SKILL.md for this task. Read its SKILL.md completely, then load only the references relevant to this project.

Build the project described in BRIEF.md completely. You may create and edit files in this workspace and run local checks. Do not ask questions unless a missing decision makes safe progress impossible. Do not use external services or network dependencies.

Verify what you can in the available environment. Put the finished website in the workspace root and write RUN-REPORT.md containing: what you built, files changed, checks actually run and their results, remaining unverified claims, and the exact next useful review. Do not include hidden reasoning or a transcript.
```
