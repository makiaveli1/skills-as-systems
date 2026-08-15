# Change discipline — compact

Use before consequential edits.

## Change Contract

Resolve:

- **objective:** the user-visible or system outcome;
- **baseline:** current behaviour and evidence;
- **target:** changed behaviour and failure cases;
- **invariants:** what must remain true;
- **owner:** the narrowest natural owner;
- **surface:** allowed files/modules/data/configuration and affected neighbours;
- **forbidden:** unrelated cleanup, generated output, public breaks, or destructive actions not authorized;
- **risk:** what could fail, leak, race, corrupt, or become incompatible;
- **verification:** proof matched to each claim;
- **recovery:** rollback, compatibility window, backup, or forward-fix route.

For a tiny reversible edit, working notes are enough. For substantial, shared, risky, or resumable work use `schemas/change-contract.schema.json`.

## Intervention rule

Choose the smallest coherent change, not the fewest typed lines. Prefer the existing owner. Add abstraction or dependency only when it removes a current, evidenced pressure and has a named owner, boundary, lifecycle, failure mode, and verification cost.

Re-read targets before editing. Preserve user changes. Change sources rather than generated output. Keep unrelated cleanup separate.

## Closeout

Inspect the final diff. Every changed line must support the contract. Re-run focused proof, affected regressions, and exact-state checks. Mark unsupported claims UNVERIFIED.

Read [change-discipline.md](change-discipline.md) for compatibility, migrations, broad changes, or rollback-sensitive work.
