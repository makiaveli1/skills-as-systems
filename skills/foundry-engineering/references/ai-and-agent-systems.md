# AI, LLM, agent, retrieval, and tool systems

## Treat probabilistic components as one subsystem

Separate:

- product contract and deterministic application logic;
- model/provider adapter;
- prompts/instructions and version;
- retrieval/data pipeline;
- tools and effect boundary;
- memory/state and tenancy;
- policy/authorization outside the model;
- evaluation, observability, cost, and fallback.

Do not let a model prompt become the only owner of permissions, validation, business invariants, or irreversible actions.

## Behaviour contract

Define:

- user-visible success and unacceptable outcomes;
- input/content trust classes;
- output schema and validation;
- tool/action allowlist and approval boundary;
- model/version/fallback and capability assumptions;
- latency, cost, token/context, privacy, and retention budgets;
- deterministic and human escalation paths;
- evaluation datasets and change gates.

Model confidence is not authorization or evidence.

## Tool and MCP systems

Treat tool descriptions, arguments, results, resources, prompts, and retrieved content as untrusted inputs. Enforce outside the model:

- authentication and scoped authorization;
- exact project/tenant/user binding;
- argument schema plus semantic validation;
- side-effect classification and approval;
- least privilege and bounded outputs;
- idempotency and durable action identity;
- audit, timeout, cancellation, retry, and recovery;
- secret redaction and data-loss prevention;
- tool catalogue/version freshness.

Do not pass tokens between audiences, assume a tool's name proves safety, or let content instructions override system/user authority. Verify current MCP and provider specifications at implementation time; they evolve.

## Prompt injection and data boundaries

Distinguish instructions from data structurally and by authority. Retrieved documents, webpages, emails, code comments, tool output, and memory may contain hostile instructions. Limit data exposed to each model/tool, isolate tenants, sanitize rendered output, and require external policy checks for effects.

## Retrieval

Define corpus authority, ingestion freshness, chunking/index version, access control, ranking, citations/provenance, deletion, and fallback. Evaluate retrieval separately from generation:

- recall of necessary evidence;
- irrelevant/context-poisoning rate;
- permission filtering;
- freshness and duplicate handling;
- answer faithfulness to retrieved sources.

Large context is not full understanding. Use task-directed iterative retrieval and reopen exact sources for load-bearing decisions.

## Agent state and workflows

Use explicit states, terminal outcomes, budgets, checkpoints, and action identities. Persist only durable facts and references needed to resume. Avoid recursive summaries, hidden permissions, and duplicate paid or destructive effects after retry/handoff.

Multi-agent work requires one canonical owner per shared artifact, bounded context, independent verification, and live-state reconciliation. Agent consensus does not establish truth.

## Evaluation

Test the complete system, not only model output:

- task success and contract adherence;
- deterministic schema/policy checks;
- tool choice, argument validity, and effect correctness;
- retrieval quality and provenance;
- adversarial prompt injection and cross-tenant leakage;
- refusal/approval boundaries;
- latency, cost, reliability, and recovery;
- regression across model/prompt/tool/index versions;
- human judgement where semantics or risk require it.

Use representative, contrasting, and adversarial cases. Keep holdout tests and exact version/configuration. One benchmark score cannot establish production readiness, maintainability, security, or fit for a different repository.

## Provider neutrality

Keep model and tool names in replaceable adapters and runtime configuration. The core contract should survive model replacement, missing tools, and a different host. When a capability is unavailable, return a bounded packet and explicit UNVERIFIED state rather than pretending execution.
