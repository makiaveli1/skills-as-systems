# Motion and interaction

Use motion to make relationships, state changes, and consequences easier to understand.

This module governs interface motion. When the work includes kinetic typography, animated identity, authored title sequences, composited artwork, editorial loops, interactive vector scenes, 3D, canvas, Lottie or dotLottie, Rive, or video-based motion graphics, also load [motion-design-and-graphics.md](motion-design-and-graphics.md). Keep interface feedback and authored motion graphics related, but do not give them the same budget or production workflow.

## Motion purposes

Every effect must serve at least one purpose:

- **Orientation** — show where content came from or where the user moved.
- **Continuity** — preserve identity between related states or routes.
- **Causality** — connect an action to its result.
- **Hierarchy** — reveal the order or importance of information.
- **Feedback** — confirm input, progress, success, failure, or availability.
- **Attention** — direct focus to a time-sensitive change without competing noise.
- **Character** — express brand personality without reducing usability.

Remove motion that serves only to prove that animation is present.

## Choose the lightest mechanism

- Use CSS transitions for direct state changes.
- Use CSS keyframes for declarative, self-contained sequences.
- Use the Web Animations API when JavaScript needs playback control, dynamic timing, sequencing, cancellation, or inspection.
- Use the View Transition API for continuity across DOM states or same-origin navigations when it fits the architecture.
- Use a specialised library only when its capability is necessary and its bundle, maintenance, and accessibility costs are justified.

Feature-detect progressive APIs. Preserve the state change and full function when the enhancement is unavailable.

## Motion grammar

Define a small grammar:

- duration ranges by purpose;
- easing families;
- entrance and exit relationship;
- spatial direction rules;
- scale and opacity limits;
- stagger rules;
- interrupt and reverse behaviour;
- route-transition behaviour;
- focus timing;
- loading and progress motion;
- ambient-motion budget.

Do not give every component a unique easing and duration.

## Performance

Prefer compositor-friendly properties such as `transform` and `opacity`. Avoid animating layout-inducing properties such as `top`, `left`, `width`, `height`, `margin`, and border width unless the trade-off is measured and justified.

Avoid large blurred layers, excessive fixed elements, unbounded particle systems, and continuous animation that keeps the device busy after the user has stopped interacting.

## Scroll

Scrolling is user-controlled navigation. Do not hijack it.

Allowed scroll-linked behaviour should:

- preserve native scrolling;
- remain understandable if the effect is absent;
- avoid pinning large regions for excessive distances;
- prevent focus from entering invisible content;
- keep URL, history, and browser controls useful;
- avoid nausea-inducing depth or camera motion;
- be tested on touchpads, touch, keyboard, and reduced motion.

## Reduced motion

Design an equivalent state for users who request reduced motion. Depending on the effect:

- remove spatial travel but retain an opacity change;
- replace an animated morph with an immediate state and clear focus move;
- shorten or disable parallax;
- stop autoplay and ambient loops;
- use static progress or status indicators;
- preserve content order and orientation through layout and labels.

Use `prefers-reduced-motion` in CSS and JavaScript where relevant. Test the actual system preference, not only the presence of the media query.

## Interaction states

Specify and test:

- default;
- hover where supported;
- focus-visible;
- active/pressed;
- selected/current;
- disabled;
- loading;
- success;
- warning/error;
- expanded/collapsed;
- drag start, move, drop, and keyboard alternative;
- cancellation and undo.

Do not use hover as the only route to essential information or actions.

## Transition continuity

For shared-element or view transitions:

- give each transitioned element a unique and stable identity;
- preserve aspect ratio or define crop changes intentionally;
- keep the destination interactive only when ready;
- manage focus after the state change;
- skip or simplify transitions when loading is slow;
- verify backward navigation;
- avoid transitioning large page snapshots when a smaller local change is clearer.

## Review

Use recordings to evaluate timing, interruption, scroll behaviour, focus movement, overlays, and route changes. Use screenshots for key start and end states. A single still cannot approve motion quality.
