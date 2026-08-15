# CAIRN / field plan

Build a small, distinctive web experience that helps a mixed-experience group
choose one walking route and leave with a practical shared plan.

## Audience

- weekend walkers using a phone outdoors;
- one person coordinating a mixed-experience group;
- people who need the important safety information without reading a guidebook.

## Product job

The visitor should be able to compare the three supplied routes, choose one,
check the essentials, and produce a clear plan summary for the group.

## Tone

Calm field intelligence: tactile, observant, quietly confident. Avoid generic
SaaS dashboards, glass-card grids, neon gradients, and adventure-brand clichés.

## Constraints

- Work only with HTML, CSS, JavaScript, and the supplied local JSON.
- Produce `index.html`, `styles.css`, `app.js`, and `RUN-REPORT.md`.
- No frameworks, build step, external fonts, remote images, analytics, or
  network requests.
- The experience must work from a small local HTTP server.
- Preserve usable static content if JavaScript fails.
- Support keyboard, pointer, narrow screens down to 320 px, and reduced motion.
- Make honest evidence claims in `RUN-REPORT.md`.

## Stable automation hooks

Visual design is open, but include these attributes so acceptance can exercise
the product without depending on layout or CSS classes:

- `data-testid="route-list"` around the route choices;
- `data-route-id="..."` and `aria-pressed` on each route choice;
- `data-testid="difficulty-filter"` on the difficulty control;
- `data-testid="plan-summary"` on the live selected-route summary;
- `data-testid="essentials"` around the checklist;
- `data-testid="confirm-plan"` on the confirmation action;
- `data-testid="plan-status"` on validation/success feedback.

Do not include placeholder controls. Every visible interactive control must work.
