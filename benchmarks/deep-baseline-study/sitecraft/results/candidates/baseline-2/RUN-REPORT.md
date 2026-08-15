# RUN REPORT

## Scope

Updated the existing CAIRN release candidate on Saturday, August 15, 2026 in:

- `index.html`
- `styles.css`
- `app.js`
- `verify-cairn.js`

I preserved the field-board visual system and patched the blocked QA paths only:

- narrow-screen layout hardening around the route area
- automatic route normalization when filter or group changes invalidate the current plan
- ArrowLeft / ArrowRight route-choice navigation that skips closed routes
- confirmation error handling that focuses the status and names the remaining essentials
- explicit status focus support and reduced-motion-safe state clarity

## Tested

Executed these local checks:

- `node --check app.js`
- `node verify-cairn.js`
- `node` verification that embedded `route-data` in `index.html` exactly matches `data/routes.json`

## Observed

Observed through the scripted DOM harness in `verify-cairn.js`:

- Initial active plan is `Rowan Loop`.
- Choosing the `hard` filter while `Rowan Loop` is active automatically updates the plan to `Tor Line`, keeps focus on the filter control, and announces the change in the status text.
- Switching from `experienced` with `Tor Line` selected back to `mixed` automatically updates the plan to `Rowan Loop`, keeps focus on the group-needs control, and announces that `Tor Line` is not advised for a mixed group.
- `ArrowRight` and `ArrowLeft` from focused route choices move both focus and selection among visible open routes.
- Arrow-key navigation skips the closed `Bracken Rise` route.
- Submitting the plan with unchecked essentials fails, focuses `data-testid="plan-status"`, and lists the remaining essentials by label.
- Submitting after every essential is checked succeeds and produces a stable summary string containing both the route name and the active group needs.

Observed through static CSS assertions:

- The shell width is capped at `min(1120px, 100%)`.
- The route list collapses to one column at `max-width: 700px`.
- Additional narrow-screen padding reductions apply at `max-width: 420px`.
- Reduced-motion CSS is present and disables animation and transitions.
- No `@keyframes` blocks are defined, so no continuous decorative CSS animation is declared.

## Unverified

These were **not** directly observed in a real browser:

- Visual rendering at `1440×1000`, `390×844`, and `320×800`
- Actual absence of horizontal page scrolling at `320×800`
- Real browser focus-ring placement and scrolling behavior
- Live-region announcement timing in assistive technology
- Real reduced-motion rendering behavior in a browser engine

## Why Unverified

`AGENTS.md` in this workspace forbids browser access, browser drivers, localhost, and preview servers. No local browser tooling was available inside those limits, so I could not perform fresh interactive browser checks. The release-blocking interaction paths were verified with a local scripted harness and static CSS/code inspection instead.
