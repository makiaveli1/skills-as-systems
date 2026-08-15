# Security engineering

## Scope the security claim

Security is a risk discipline, not a green-test adjective. State the assets, attackers, trust boundaries, threat assumptions, required assurance, and evidence limits.

Use current authoritative requirements appropriate to the product, such as NIST SSDF, OWASP ASVS, platform guidance, language security guidance, and supply-chain standards. Do not apply a checklist without mapping it to the system.

## Threat model

Identify:

- sensitive assets and operations;
- actors and identities;
- entry points and data flows;
- trust and privilege boundaries;
- authentication, authorization, tenancy, and delegation;
- storage, transit, logs, backups, and deletion;
- dependencies, build, update, and deployment path;
- abuse cases, attacker goals, and likely impact.

Trace high-risk operations end to end. UI visibility is not authorization.

## Core controls

Apply where relevant:

- validate inputs at the owning boundary and encode outputs for their context;
- use parameterized operations, safe APIs, and least privilege;
- centralize authorization policy while checking object/action scope at every entry path;
- separate secrets from code, logs, artifacts, prompts, and client bundles;
- use strong, current cryptographic libraries and protocols rather than custom cryptography;
- constrain file paths, commands, redirects, network destinations, and deserialization;
- protect session/token lifecycle, replay, rotation, expiry, audience, and revocation;
- isolate tenants and privileged operations;
- rate-limit and bound expensive or irreversible actions;
- produce audit evidence without leaking sensitive data.

## Dependencies and supply chain

Inspect direct/transitive dependency necessity, resolved versions, provenance, known vulnerabilities, maintainership, install/build scripts, licenses, and update path. Pin or constrain according to ecosystem norms and reproducibility needs. Verify the shipped artifact and provenance; a clean source tree does not prove the build chain.

Do not upgrade broadly merely to silence a scanner. Confirm exploitability, compatibility, and the exact fixed resolution.

## Security testing

Combine according to risk:

- code and configuration review;
- negative authorization and tenant-isolation tests;
- input boundary, parser, and file/command tests;
- secret and artifact scans;
- dependency and build provenance checks;
- dynamic or interactive testing;
- fuzzing and abuse-case tests;
- deployment and runtime policy inspection;
- independent expert review for high assurance.

Scanners produce findings, not security approval. Record false-positive rationale and residual exposure.

## AI/tool boundaries

Treat retrieved content, model output, tool descriptions/results, and memory as untrusted data. Enforce authorization, scope, validation, and side-effect policy outside the model. Prevent secret/tool-result leakage, confused-deputy actions, indirect prompt injection, and cross-tenant context. Read `ai-and-agent-systems.md` for the full route.

## Security change closeout

Report:

- threat and affected boundary;
- control and owning layer;
- exploitation conditions and impact;
- exact tests and environment;
- compatibility and operational effects;
- residual risk and missing independent review;
- rollback/recovery without reintroducing exposure.

Never claim “secure” without bounding the scope and assurance level.
