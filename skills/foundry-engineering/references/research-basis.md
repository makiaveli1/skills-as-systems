# FOUNDRY research basis

Use only when maintaining FOUNDRY doctrine or evaluation. These sources informed v1; they are not required task context. Accessed 2026-08-15.

## Repository-level AI engineering

- [SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://arxiv.org/abs/2310.06770) establishes that real issue resolution requires coordinated understanding across repository functions/files and executable environments.
- [RepoCoder: Repository-Level Code Completion Through Iterative Retrieval and Generation](https://aclanthology.org/2023.emnlp-main.151/) supports iterative, task-directed retrieval rather than relying on one in-file or whole-repository context dump.
- [SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](https://papers.nips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf) supports treating navigation, editing, and test interfaces as an engineering surface rather than assuming model reasoning alone is enough.
- [SWE-bench Goes Live](https://arxiv.org/abs/2505.23419) supports fresh, reproducible evaluation and contamination resistance.
- [SWE-CI: Evaluating Agent Capabilities in Maintaining Codebases via Continuous Integration](https://arxiv.org/abs/2603.03823) motivates evaluating regression control and maintainability across sequences, not only one-shot patches.
- [SWE-fficiency](https://openreview.net/forum?id=0pyFbZSfbT) reinforces that repository-level optimization requires real workloads and measured performance.

FOUNDRY inference: a useful coding skill must improve repository targeting, iterative evidence retrieval, regression control, exact-state verification, and maintainability—not merely generated patch quality.

## Review and software quality

- [Google Engineering Practices](https://google.github.io/eng-practices/) and [The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html) support evidence/technical facts over preference, incremental improvement, and review focused on code health rather than perfection.

FOUNDRY inference: existing architecture and conventions should constrain changes; reviewers should distinguish blocking correctness from preference and unrelated cleanup.

## Security and supply chain

- [NIST SP 800-218 SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) grounds secure development across the lifecycle and root-cause prevention.
- [NIST SP 800-218A](https://csrc.nist.gov/pubs/sp/800/218/a/final) extends SSDF for generative AI and foundation-model systems.
- [OWASP ASVS](https://github.com/OWASP/ASVS/tree/v5.0.0) supplies testable application-security requirements; version-specific requirement IDs must be recorded.
- [SLSA specification 1.2](https://slsa.dev/spec/v1.2/) grounds incremental build/source provenance and supply-chain assurance.
- [OWASP LLMSVS](https://owasp.org/www-project-llm-verification-standard/) supplies security verification concerns for LLM applications, agents, tools, dependencies, and monitoring.

FOUNDRY inference: security claims need a scoped threat/assurance model and external enforcement; tests or model instructions alone do not grant protection or authority.

## Reliability and observability

- [Google SRE: Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/) supports evidence-led diagnosis using system examination, logs, metrics, and traces.
- [Google SRE: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) distinguishes user-visible black-box and internal white-box evidence.
- [Google SRE Workbook: Postmortem Culture](https://sre.google/workbook/postmortem-culture/) supports impact assessment, root-cause analysis, and concrete action items without blame.
- [OpenTelemetry specification](https://opentelemetry.io/docs/specs/otel/) provides current signal, correlation, context, and versioning semantics for traces, metrics, logs, and related telemetry.

FOUNDRY inference: observability must answer engineering questions and support causal investigation; internal telemetry alone does not prove user recovery.

## Tool protocols

- [Model Context Protocol specification](https://modelcontextprotocol.io/specification/2026-07-28) and its authorization/security material are current as of the access date.

FOUNDRY inference: model/tool protocols are unstable specialist knowledge. Discover the live specification, validate tool effects outside the model, and keep provider adapters out of portable doctrine.

## Maintenance rule

Recheck versioned or evolving sources before changing doctrine. Preserve the difference between a source-backed fact and FOUNDRY's engineering inference. One benchmark or organization does not establish universal practice; use contrasting evidence and project reality.
