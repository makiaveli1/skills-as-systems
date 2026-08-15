# TIDEGLASS run report

## What was built

A polished, responsive, single-page public information experience for the fictional **TIDEGLASS / East Breakwater** departure briefing.

The page includes:

- An unmistakable top-of-page **Demonstration data — not for navigation** boundary, reinforced beside the advisory and form.
- A high-contrast current decision, best departure window, and four observation values.
- Three touch- and keyboard-operable time bands. Selection updates the decision and all displayed observation fields from one local state object and announces the new state.
- The four-item departure checklist and required advisory.
- A local-only email demonstration with empty, invalid, submitting, success, and deterministic failure states. `fail@demo.test` exercises the failure path. It contains no transmission or retention mechanism.
- Responsive compositions for wide, intermediate, narrow, and 320 CSS-pixel layouts; visible focus; reduced-motion and forced-colour treatments.
- A SITECRAFT experience contract recording the trust boundary, visual system, behaviour, responsive rules, capability choices, and remaining evidence gate.

The dominant visual idea is a harbour instrument board translated into a crisp public information sheet: warm paper, blue-black instrument surfaces, tabular readings, signal amber, and square-edged controls. No images, generated media, external fonts, frameworks, or runtime dependencies are used.

## Files changed

- `index.html` — semantic page structure and all required public content.
- `styles.css` — visual system, responsive compositions, focus states, reduced motion, and forced-colour support.
- `app.js` — local outlook selection, keyboard handling, live announcements, and form-state simulation.
- `README.md` — run instructions, interaction notes, and trust boundary.
- `EXPERIENCE-CONTRACT.json` — SITECRAFT contract revision 1.
- `RUN-REPORT.md` — this build and evidence record.

`BRIEF.md` and the installed SITECRAFT skill were read only.

## Checks actually run

| Check | Result |
| --- | --- |
| `node --check app.js` | Passed; JavaScript syntax is valid. |
| Local interaction harness using a mocked DOM | Passed; all three outlook selections, ArrowRight focus/selection, and empty, invalid, submitting, success, and failure form paths behaved as specified. The temporary harness was removed after the run. |
| Structural source check | Passed; 22 IDs are unique, all `for` and ARIA ID references resolve, and header/main/section/footer/form/h1 landmarks are present. |
| Required-content check | Passed; 21 decision, observation, checklist, and form-title strings were found across the public HTML and JavaScript. |
| Public-boundary scan | Passed; no `fetch`, XHR, WebSocket, beacon, local/session storage, IndexedDB, cookie, or remote HTTP(S) mechanism appears in `index.html`, `styles.css`, `app.js`, or `README.md`. |
| CSS structural check | Passed; 133 opening and closing rule blocks balance, and 62rem, 42rem, 24rem, reduced-motion, and forced-colour rules are present. |
| JSON parse | Passed for both `EXPERIENCE-CONTRACT.json` and the authoritative SITECRAFT schema. |
| Full JSON Schema validator | Not run; the local Python `jsonschema` package is not installed. The contract was checked against the required schema structure during authoring and parses as JSON, but that is not a substitute for validator evidence. |
| Installed `tidy` HTML check | Inconclusive; this host's linter is an older HTML4 build that rejects HTML5 landmarks such as `header`, `main`, and `section` and misreads UTF-8 punctuation. Its exit code was 2, so it is not treated as HTML5 conformance evidence. |
| Local Playwright availability probe | Unavailable; there is no local Playwright/browser executable in the workspace, and the no-install probe produced no usable browser evidence. No package or browser was downloaded. |

## Remaining unverified claims

- Visual composition, clipping, and horizontal reflow have not been observed in a real browser at the required viewport matrix.
- Pointer/touch behaviour and the keyboard path have been source- and harness-checked, but not manually exercised in a browser.
- Screen-reader announcements, browser zoom, forced colours, and reduced-motion behaviour have not been observed with assistive technology or browser emulation.
- Colour contrast has been designed for high contrast but has not been measured with an accessibility audit tool.
- No browser performance, layout-shift, or cross-engine measurements were available. The public payload is 28,303 bytes before the contract/report and has no external requests, but that does not replace runtime evidence.
- The experience contract has not been run through a complete JSON Schema validator in this host.
- Human visual approval and release approval have not been requested.

## Exact next useful review

Open `index.html` locally in a modern browser and review the exact build at **1440×900, 1024×768, 768×1024, 390×844, and 320×568**. At 320 pixels and 200% zoom, confirm there is no horizontal scroll or clipped value. Then use Tab plus Arrow/Home/End across the time bands, run the form with empty input, `not-an-email`, `crew@example.com`, and `fail@demo.test`, and repeat with reduced motion enabled. Finish with a screen-reader spot check of the demonstration warning, selected time state, update announcement, input label, and form status. Human approval of that matrix is the next release condition.
