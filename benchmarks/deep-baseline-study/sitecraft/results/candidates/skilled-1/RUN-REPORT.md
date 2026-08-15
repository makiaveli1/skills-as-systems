# RUN REPORT

Date: 2026-08-15

## Current state

- Repaired the late QA blockers in `app.js`, `styles.css`, and `index.html` without changing the established field-notebook visual direction.
- The planner still uses progressive enhancement: static route notes remain available in HTML, and the interactive planner hydrates from `data/routes.json`.
- Closed routes remain visible for comparison, but active-plan selection now resolves only to visible open routes.
- Group changes and filter changes now re-resolve the active plan when the current route becomes unavailable or not advised.
- Keyboard ArrowRight and ArrowLeft now move focus and selection across visible open routes only, skipping closed routes.
- Confirmation now fails until every essential is checked, moves focus to the status region, identifies the remaining unchecked essentials, and produces a stable confirmed summary that names both the route and the current group profile.
- The route area has an added overflow hardening pass for narrow widths, and reduced-motion handling remains in place.

## Compact working contract

- Purpose and primary outcome:
  Help a mixed-experience walking group compare the available routes, choose one, surface safety-critical facts quickly, and leave with a clear shared plan summary.
- Protected boundaries:
  No frameworks, no build step, no external assets, no remote requests, no placeholder controls, and usable static content if JavaScript fails.
- Dominant visual idea:
  A calm field-notebook board rather than a marketing page or SaaS dashboard: survey-line background, muted ground palette, framed paper panels, dense route metadata, and restrained motion.
- Required states and responsive transformations:
  Static fallback, enhanced planner, group-needs updates, route filtering, closed-route comparison, automatic valid-route reselection, keyboard route navigation, incomplete checklist warning, confirmed plan success, stacked mobile layout, and reduced-motion mode.
- Material implementation choice:
  Progressive enhancement. The static comparison renders first; the interactive planner is revealed only after `app.js` successfully loads `data/routes.json`.
- Evidence needed:
  Structural proof of the repaired layout/motion guards, exercised proof of the new selection and confirmation logic, and browser verification for the specified viewport and input matrix.

## Material re-entry events

- Re-entered after `QA-REPORT.md` introduced new blocking evidence on Saturday, August 15, 2026.
- Reopened the affected routes only: selection validity, keyboard interaction, confirmation feedback, reduced-motion clarity, and narrow-width overflow risk.
- Preserved the existing visual system and repaired the ownership boundaries in state and feedback instead of redesigning the surface.
- Re-entered before completion for `Observe` and `Harden`, then scoped claims to the exact evidence this host could produce.

## Repairs made

- Added live-plan reselection logic so group/filter changes choose the best visible open route when the prior selection becomes unavailable or not advised.
- Added live-region announcements for automatic route changes and no-open-route states.
- Added ArrowRight and ArrowLeft route navigation that skips closed routes and moves focus to the newly selected open route.
- Made confirmation failures focus the status region and list the remaining essential names instead of only a count.
- Added a stable confirmed summary block in the selected-route panel.
- Added `tabindex="-1"` to the status region so focus can move there on confirmation outcomes.
- Added narrow-width hardening with `min-width: 0`, text wrapping, and overflow guards on route cards, summary blocks, and metric content.

## Tested and observed

### Structural checks

- `node --check app.js` passed on 2026-08-15.
- Required hooks are present in source:
  `data-testid="route-list"`, `data-testid="difficulty-filter"`, `data-testid="group-needs"`, `data-testid="plan-summary"`, `data-testid="essentials"`, `data-testid="confirm-plan"`, `data-testid="plan-status"`, plus `data-route-id`, `aria-pressed`, and `aria-disabled` on route choices.
- Reduced-motion CSS is present:
  `@media (prefers-reduced-motion: reduce)` zeroes transition and animation duration.
- Narrow-width guards are present:
  `overflow-x: clip` on `body`, `min-width: 0` on key layout/content containers, and `overflow-wrap: anywhere` on route and summary text content.

### Exercised functional checks

Ran a local Node VM harness with a fake DOM against the exact `app.js` build and the current `data/routes.json` on 2026-08-15. Observed results:

- Initial mixed-group selection resolves to `Rowan Loop`.
- `Bracken Rise` remains rendered with closed-state comparison copy and cannot become the active plan by click.
- When `Tor Line` is active and group needs change to `child`, the plan auto-updates back to `Rowan Loop` and announces the reason in the status region.
- ArrowRight from a focused closed route resolves to the first visible open route.
- ArrowRight and ArrowLeft move selection and focus between `Rowan Loop` and `Tor Line`, skipping the closed route.
- Confirmation before all essentials are checked focuses the status region and names the remaining unchecked essentials.
- After all essentials are checked, confirmation focuses the status region, reports a success message containing both the current group profile and route, and renders a stable confirmed summary block.
- Filtering to `steady` leaves the closed route visible for comparison, clears the live plan because no open route remains in that filtered view, and announces that condition.

## Unverified in this host

- I did not run a browser on 2026-08-15.
- I did not start a local server on 2026-08-15.
- I did not capture screenshots, recordings, accessibility-tree output, or browser-computed layout evidence.
- I did not observe the experience at 1440×1000, 390×844, or 320×800 in a browser engine.
- I did not observe real keyboard traversal, real pointer behaviour, or real reduced-motion rendering in a browser.
- I therefore did not directly observe whether the repaired route area avoids horizontal page scrolling at 320 px in an actual renderer; I only verified the structural overflow guards listed above.

## Release condition

Not production-ready yet.

Exact next approval condition:
Run the existing build from a local HTTP server in a real browser and verify these states against the repaired files from 2026-08-15:

- 1440×1000, 390×844, and 320×800 layout and reflow;
- no horizontal page scrolling caused by the route area at 320 px;
- group-needs changes for `mixed`, `child`, and `experienced`;
- filter changes that invalidate the current route;
- closed-route comparison without active-plan selection;
- ArrowRight and ArrowLeft route navigation with closed-route skipping;
- confirmation failure focus and remaining-essential naming;
- stable confirmation success summary with route and group profile;
- reduced-motion rendering and state clarity;
- static fallback when JavaScript is unavailable.
