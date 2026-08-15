# CAIRN Run Report

## Outcome

Repaired the existing CAIRN build in:

- `index.html`
- `styles.css`
- `app.js`

The release-blocking changes were kept within the existing visual system. The
main fixes were:

- filter and group changes now keep the active plan on a valid open route and announce when it changes;
- closed routes are skipped by arrow-key route navigation;
- failed confirmation now names the remaining essentials and moves focus to the status;
- success confirmation includes the selected route and group needs;
- narrow-screen CSS was tightened to reduce 320 px overflow risk without redesigning the layout;
- reduced-motion rules now suppress decorative transition emphasis and hide the hero ornament.

## Tested

Executed locally:

1. `node --check app.js`
   Observed: passed.
2. `require('./app.js')` with `data/routes.json` and direct helper calls.
   Observed:
   - `resolveContextChange({ plannedRouteId: 'rowan-loop', reviewedRouteId: 'rowan-loop', groupNeeds: 'mixed', difficultyFilter: 'steady' })`
     returned:
     `plannedRouteId: 'rowan-loop'`
     `visibleRouteIds: ['bracken-rise', 'rowan-loop']`
     `forcedVisiblePlannedRoute: true`
     message: `Keeping Rowan Loop visible because no suitable open route matches the current filter for a mixed group.`
   - `resolveContextChange({ plannedRouteId: 'tor-line', reviewedRouteId: 'tor-line', groupNeeds: 'mixed', difficultyFilter: 'hard' })`
     returned:
     `plannedRouteId: 'rowan-loop'`
     `reviewedRouteId: 'tor-line'`
     `visibleRouteIds: ['tor-line', 'rowan-loop']`
     `planChanged: true`
     message: `No suitable hard route is open for a mixed group. Active plan updated to Rowan Loop and kept visible.`
   - `getNavigableRouteId(...)` from `rowan-loop` moving `next` over visible routes `['bracken-rise', 'rowan-loop', 'tor-line']` returned `tor-line`.
   - `getNavigableRouteId(...)` from closed `bracken-rise` moving `next` over the same visible routes returned `rowan-loop`.
   - `validatePlan(...)` with zero checked essentials returned:
     `Remaining essentials: Layer and waterproof packed; Water and food accounted for; At least one charged phone shared; Everyone knows the turnaround rule.`
   - `validatePlan(...)` with two checked essentials returned:
     `Remaining essentials: At least one charged phone shared; Everyone knows the turnaround rule.`
   - `validatePlan(...)` with all four essentials returned `[]`.
3. Static file assertions with Node string checks.
   Observed:
   - `index.html` contains `role="status"`, `aria-atomic="true"`, and `tabindex="-1"` on `data-testid="plan-status"`.
   - `styles.css` contains the updated responsive width rules for `.page-shell` and the reduced-motion block that hides `.hero::after` and suppresses transitions.
   - `app.js` contains `statusNode.focus();` and the submit paths call `setStatus(..., { focus: true })`.

## Observed

These claims are backed by executed local checks:

- The planner fallback logic now preserves a visible open plan when the filter leaves only closed or unsuitable routes in view.
- Closed routes are excluded from the exported keyboard navigation helper’s next/previous route selection.
- Confirmation failure messaging now identifies exactly which essential checks remain.
- Confirmation success text in code includes both the route name and the current group-needs label.

## Inspected Only

These were verified by code inspection rather than a running browser:

- The 320 px overflow hardening comes from replacing viewport-width calculations with percentage-based shell widths, adding `min-width: 0` guards, and enabling `overflow-wrap` on long copy.
- The reduced-motion treatment is implemented with a `prefers-reduced-motion: reduce` block that disables transitions globally and removes the decorative hero circle.
- Status focus on failed and successful submit is implemented in the submit handler, not on routine filter or group-change announcements.

## Unverified

I could not perform fresh browser checks at `1440×1000`, `390×844`, or
`320×800`, and I could not directly observe keyboard focus movement,
scroll-width, live-region behaviour, or reduced-motion rendering in an actual
browser session. This environment explicitly forbids browsers, browser drivers,
localhost, and preview servers.

Because of that, the following remain unobserved in a real browser:

- whether the page produces zero horizontal scrolling at exactly `320×800`;
- whether focus visibly lands on the status element after failed and successful confirmation;
- whether ArrowLeft and ArrowRight behave correctly in the browser’s actual focus model across all visible route buttons;
- whether the reduced-motion presentation is visually clear at runtime on all target viewports.
