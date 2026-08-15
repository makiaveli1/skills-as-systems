# Late QA report

Release is blocked on these observed behaviours:

1. At 320 px, the route area must not create horizontal page scrolling.
2. When a filter or group choice makes the current route unavailable or
   unsuitable, focus may stay where the user put it, but the plan must choose a
   valid visible open route and announce the update.
3. ArrowRight and ArrowLeft from a focused route choice must move focus and
   selection among available visible routes. Closed routes must be skipped.
4. Confirmation must fail until every essential is checked, focus the status,
   and identify what remains. After all essentials are checked it must produce
   a stable success summary containing route and group needs.
5. With reduced motion enabled, functional state changes must remain clear and
   no decorative animation may run continuously.

Repair these issues without a visual rewrite. Perform fresh browser checks at
1440×1000, 390×844, and 320×800 if browser tooling is available, plus keyboard
and reduced-motion checks. State exactly what was and was not observed in
`RUN-REPORT.md`.
