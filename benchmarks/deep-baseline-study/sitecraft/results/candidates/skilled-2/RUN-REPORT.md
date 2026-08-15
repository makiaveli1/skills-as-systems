# RUN REPORT

## Scope

- Built the complete single-page CAIRN route-planning experience from `BRIEF.md`.
- Updated the existing single-page experience after new moderated-session evidence in `NEW-EVIDENCE.md`.
- Repaired the late QA blockers from `QA-REPORT.md` without redesigning the existing field-sheet experience.
- Preserved the field-sheet visual identity and repaired only the affected layout, state, keyboard, checklist, and reduced-motion behaviour in `index.html`, `styles.css`, and `app.js`.
- Preserved all required acceptance hooks:
  - `data-testid="route-list"`
  - `data-route-id` and `aria-pressed`
  - `data-testid="difficulty-filter"`
  - `data-testid="group-needs"`
  - `data-testid="plan-summary"`
  - `data-testid="essentials"`
  - `data-testid="confirm-plan"`
  - `data-testid="plan-status"`

## Compact Contract

- Purpose and primary outcome:
  Help a mixed-experience walking group compare three routes, choose one, and leave with a practical shared plan summary.
- Protected boundaries:
  No frameworks, no build step, no external fonts or remote media, no network requests, usable static content if JavaScript fails, keyboard support, narrow-screen support down to 320 px, reduced-motion support.
- Visual direction:
  Keep the existing field-sheet planner with topographic background rhythm, serif route naming, restrained earthy palette, and a sticky decision card.
- Required states:
  Default selected route, route switching, difficulty filtering, group-needs switching, closed-route comparison, blocked confirmation for closed routes, checklist-gated confirmation, success and failure plan feedback, no-script fallback, narrow-screen reflow, and reduced motion.
- Material implementation choice:
  Route controls remain real anchors so they still navigate to route notes without JavaScript; JavaScript upgrades them into a live selector/filter system, a status-aware confirmation model, arrow-key route movement, and an interactive essentials checklist. Affected planning rules were moved into pure functions so they can be verified in Node without browser access.
- Evidence needed:
  Source inspection, static syntax checks, functional verification of the changed planning logic, structural verification of the reduced-motion and 320 px safeguards, and honest statement of what could not be observed in this host.

## Consequential Decisions

- Kept `Rowan Loop` as the mixed/child default and made `Tor Line` the strongest experienced-only open option through guidance rather than a visual redesign.
- Left closed routes visible for comparison, but prevented them from being confirmed as the active plan.
- Added a `group-needs` control that changes suitability, watchpoints, share text, and essentials while preserving ascent, terrain, signal, and timing detail.
- Clarified that difficulty means combined effort, ground, and route commitment, because moderated users misread the original labels.
- Made each essential explain why it matters in the current route context.
- Added a real essentials checklist and changed confirmation so it fails with a specific remaining-items message until every essential is checked.
- Limited automatic route correction to context changes such as filters and group needs, so closed routes remain manually comparable.
- Added a filter fallback to `all` when the chosen filter would otherwise leave no visible open suitable route.

## Material Re-entry Events

- Re-entered SITECRAFT after `NEW-EVIDENCE.md` changed the state model and invalidated the earlier assumption that every route could become the active plan.
- Reopened only routing, lifecycle, and evidence references because the visual system still held and did not need replacement.
- Re-entered again after `QA-REPORT.md` blocked release and invalidated the earlier verification boundary.

## Tested And Observed

- Project-aware inspection completed for `BRIEF.md`, `NEW-EVIDENCE.md`, `QA-REPORT.md`, `data/routes.json`, and the final source files.
- Local source and syntax checks completed:
  - `node --check app.js`
  - `python3 -c "from html.parser import HTMLParser; ..."` against `index.html`
  - `git diff --check`
- Functional logic verification completed in Node against the repaired QA boundaries:
  - when group needs change from experienced to child while `Tor Line` is selected and confirmed, the plan reselects `Rowan Loop`, resets the filter to `all`, clears the old confirmation, and produces an update announcement;
  - when the `steady` filter would leave only closed `Bracken Rise`, the plan resets to `all` so a visible open route remains selected;
  - ArrowRight from `Rowan Loop` and ArrowLeft from `Tor Line` skip closed `Bracken Rise`;
  - confirmation fails until every essential is checked and names the remaining unchecked items;
  - confirmation succeeds after all essentials are checked and the success summary contains both route and group label.
- Structural CSS/source verification completed for the repaired narrow-screen and reduced-motion safeguards:
  - a dedicated `@media (max-width: 360px)` block is present for extra-small layout tightening;
  - overflow wrapping rules are present on the route and summary text that previously risked 320 px overflow;
  - `@media (prefers-reduced-motion: reduce)` is present;
  - no `@keyframes` blocks are present in `styles.css`, so no continuous decorative animation is authored there.
- The workspace was already dirty from delivered project files and new evidence; I preserved that state and only edited the CAIRN surface files.

## Unverified

- I did not open the experience in a browser.
- I did not start a local HTTP server.
- I did not capture screenshots, recordings, accessibility tree output, or automated browser interaction.
- I did not test on multiple browser engines or operating systems.
- I could not run the requested 1440×1000, 390×844, or 320×800 browser checks because this workspace prohibits browser drivers, GUI applications, localhost/server use, and existing server processes.
- I could not run a DOM-level local harness because `jsdom` is not installed in this workspace.
- Real browser observation remains unverified for:
  - actual absence of horizontal page scrolling at 320 px;
  - real focus movement and announcement timing during filter/group auto-reselection;
  - real keyboard event handling for ArrowLeft/ArrowRight on route choices;
  - actual focus landing on the status region after confirmation failure or success;
  - actual reduced-motion rendering with the operating-system preference enabled.

These limits come from the workspace rules in `AGENTS.md` and the local tool availability in this workspace.

## Current Status

- Implementation updated for the new evidence and the late QA blockers.
- Static-first fallback present.
- Required hooks present in source.
- Syntax-level, logic-level, and source-structure verification complete.
- Browser-observed layout, focus, keyboard, and reduced-motion evidence remain unverified in this environment.

## Release Condition

Release should remain blocked until the next reviewer can run it from a small local HTTP server in a browser and directly verify:

1. Keyboard flow across group-needs controls, filter chips, route choices, and the confirmation action.
2. The route area does not create horizontal page scrolling at 320 px.
3. Filter and group changes announce automatic plan reselection without stealing focus.
4. ArrowLeft and ArrowRight on route choices move focus and selection across visible open routes and skip closed `Bracken Rise`.
5. Confirmation failure focuses the status region and identifies the remaining unchecked essentials.
6. Confirmation success yields a stable summary that includes both route and group needs.
7. Reduced-motion behaviour remains clear with no decorative animation running continuously.
8. Final visual quality and contrast in at least one desktop and one mobile viewport.
