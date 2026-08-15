# Technical research method

## Research only when it can change the work

Research current sources when:

- an API, framework, tool, standard, model, platform, vulnerability, version, or product capability may have changed;
- repository evidence depends on undocumented external behaviour;
- a security, legal, financial, compatibility, or production decision needs high confidence;
- the technology or failure is unfamiliar or disputed;
- the design relies on a performance, concurrency, storage, or protocol guarantee;
- current alternatives materially affect architecture or dependency choice.

Do not browse for stable elementary language facts when local code and established knowledge are sufficient.

## Source order

Prefer:

1. official language/platform/framework/database/tool documentation;
2. specifications, standards, RFCs, and authoritative security guidance;
3. upstream repositories, source, release notes, and issue trackers;
4. primary research papers and benchmark artifacts;
5. first-party engineering reports with reproducible detail.

Use secondary sources for discovery or contrasting experience, not as the only authority for a load-bearing technical claim.

## Version and environment discipline

Record:

- question and decision it affects;
- exact product/library/specification version or date;
- relevant platform/runtime/configuration;
- source URL/title and access date;
- quoted or paraphrased guarantee within copyright limits;
- confidence, contradiction, and unresolved gaps;
- how the finding changed or challenged the plan.

Confirm that documentation matches the repository's actual resolved version. Current “latest” documentation may be wrong for the project.

## Challenge, do not confirm

Search for:

- documented limitations and unsupported combinations;
- migration and deprecation notes;
- security considerations and failure semantics;
- version-specific incompatibilities;
- counterexamples and benchmark setup limits;
- cost, operational, and maintenance consequences.

If research only restates the preferred plan, run a deliberate disconfirmation pass.

## Spikes

Use a bounded executable spike when documentation cannot settle integration, performance, packaging, platform, or concurrency behaviour. Define one question, fixed budget, disposable surface, success/failure criteria, and what may enter production.

A spike result is environment-scoped evidence, not universal doctrine. Keep experimental dependencies and code out of the main change unless the decision is approved.

## Research closeout

Separate:

- verified facts;
- project-specific inference;
- unstable assumptions to recheck;
- rejected options and why;
- remaining unknowns;
- exact implementation or verification consequence.

Read [research-basis.md](research-basis.md) only when maintaining FOUNDRY's doctrine or evaluation basis.
