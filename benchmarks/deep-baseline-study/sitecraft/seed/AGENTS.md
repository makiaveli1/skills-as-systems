# Benchmark workspace rules

- Work only inside this project.
- Do not inspect parent directories, benchmark evaluators, or other runs.
- Do not access the network, GUI applications, browser drivers, localhost, or
  existing server processes.
- Do not start a preview server. The independent outer evaluator will allocate
  a private random port and perform browser checks after the final turn.
- You may run local syntax and static checks that do not open sockets.
- Do not use subagents or external workers.
- Preserve private reasoning; write only decisions, evidence, and limits into
  project artifacts.
