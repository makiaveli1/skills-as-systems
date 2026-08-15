# Benchmark workspace rules

- Work only inside this project.
- Do not inspect parent directories, benchmark evaluators, or other runs.
- Do not access the network, GUI applications, localhost, or existing server
  processes.
- Local tests, SQLite processes, package builds, and temporary virtual
  environments are allowed when they remain inside this workspace or system
  temporary storage and need no network.
- Do not use subagents or external workers.
- Preserve private reasoning; write only decisions, evidence, and limits into
  project artifacts.
