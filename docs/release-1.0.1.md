# Collection 1.0.1 release receipt

Date: 2026-08-15

## Scope

- SITECRAFT 0.3.0
- FOUNDRY 0.2.0
- Claude Code collection plugin 1.0.1

## Corrections and improvements

- Public authorship, ownership, copyright, PC Bridge, and Git attribution use **MAKIAVELI** only.
- The repository README now leads with one-prompt and one-line installation paths.
- Codex and standalone Claude installs from a checkout accept `install.py codex|claude`.
- SITECRAFT, FOUNDRY, architecture, and portability documents now begin with a plain-language quick start.
- The portable skill doctrine remains provider-neutral and unchanged by the onboarding simplification.

## Local release evidence

- Tracked files and filenames contain only the intended public skill material and attribution.
- Official Agent Skills validation passes for both canonical packages.
- Repository validation, clean-install smoke tests, 22 SITECRAFT tests, and 14 FOUNDRY tests pass.
- FOUNDRY's evaluator passes 22 positive, 6 negative, 16 adversarial, and 4 mutation-gate cases.
- Claude Code 2.1.232 accepts the marketplace and plugin manifests and installs exactly the two intended skills at plugin version 1.0.1.

## Public release gates

Before the release is tagged, the exact public commit must also pass GitHub Actions, a fresh Codex installation, a fresh Claude Code marketplace installation, archive extraction tests, attribution and privacy scans, and SHA-256 verification. The release description records that final public evidence.

## Evidence boundary

A successful installation proves package delivery and discovery layout. It does not prove every model version will route identically or that every task-specific browser, deployment, security, or performance claim has been observed.
