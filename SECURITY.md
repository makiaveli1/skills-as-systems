# Security policy

Agent skills are highly trusted instructions. Review a skill and its scripts before installing it, pin versions where appropriate, and keep host permissions narrower than the skill's possible procedures.

The canonical packages in this repository contain no credentials, active MCP configuration, hooks, automatic network calls, or tool pre-approvals. Bundled Python scripts operate on explicitly supplied local paths and do not grant authority.

## Report a vulnerability

Please do not open a public issue for a vulnerability that could expose credentials, private work, or destructive behavior. Use GitHub's private security advisory flow for this repository.

Include:

- affected skill and version;
- the unsafe behavior or trust-boundary failure;
- reproduction steps that do not expose real secrets;
- likely impact;
- any safe mitigation you have tested.

Security claims should distinguish deterministic validation, static inspection, controlled reproduction, and unverified inference.
