# Responsive and intrinsic layout

Design responsive behaviour as intentional compositions that preserve meaning, task completion, and visual hierarchy.

## Do not design by device labels alone

Use device names only as shorthand. Define behaviour by available space, content pressure, input method, aspect ratio, and viewport height.

Required review states for substantial sites:

- wide desktop;
- standard desktop;
- short laptop or reduced viewport height;
- intermediate/tablet composition;
- narrow mobile;
- 320 CSS-pixel reflow;
- 200% text enlargement and high zoom where applicable.

A site can look correct on a phone preset and still fail on a short laptop, split-screen window, browser zoom, translated text, or large user font.

## Macro and micro responsiveness

Use viewport media queries for page-level composition changes. Use container queries when a reusable component must respond to the space it actually receives rather than the full viewport.

Prefer intrinsic layout tools:

- grid with `minmax()` and `auto-fit` or `auto-fill` where appropriate;
- flex wrapping;
- `clamp()` with accessible minimums and `rem` influence;
- logical properties;
- `min()`, `max()`, `fit-content()`, and `aspect-ratio`;
- intrinsic image dimensions;
- `max-width: 100%` and proportional height for media;
- content-based breakpoints.

Do not create dozens of arbitrary breakpoints to repair a rigid desktop layout.

## Composition decisions

For every major surface define what happens when space contracts:

- remains fixed;
- scales within bounds;
- wraps;
- stacks;
- reorders while preserving semantic DOM order;
- moves to another region;
- collapses behind a clear control;
- becomes horizontally scrollable with accessible panel sizing;
- changes interaction pattern;
- is removed because it is decorative;
- uses alternate media or crop.

Record the reason. “Hide on mobile” is not sufficient for meaningful content or functionality.

## Reflow

At a width equivalent to 320 CSS pixels, non-exempt content must remain available without two-dimensional scrolling. Verify:

- text wraps;
- long URLs and unbroken strings do not force overflow;
- images and embeds fit their containers;
- forms and labels reflow;
- tables have a justified alternative or controlled horizontal region;
- horizontal card panels fit within the narrow viewport when read;
- fixed or sticky elements do not obscure content or keyboard focus;
- overlays remain operable.

## Short viewport height

Test 768px and smaller effective heights where relevant. Common failures include:

- full-screen heroes hiding calls to action;
- fixed headers and bottom bars consuming most of the viewport;
- modals extending beyond the screen;
- art being clipped by viewport-height units;
- scroll-locked panels with unreachable controls.

Use modern viewport units deliberately and preserve escape and scrolling.

## Typography

Keep body text anchored to user-respectful `rem` values. When using fluid type:

- set readable minimum and maximum sizes;
- preserve zoom response;
- control line length;
- verify text spacing and translated expansion;
- avoid container-unit formulas that overpower user settings.

## Media and artwork

Preserve intrinsic proportions. Define focal points and alternate crops instead of stretching.

For protected art, choose among:

- contain with intentional surrounding space;
- cover with approved focal crop;
- art-directed `<picture>` sources;
- separate mobile composition;
- scrollable gallery or lightbox;
- background only when semantics and quality permit.

## Interaction changes

A responsive layout may require a different interaction, not a smaller version:

- desktop side rail → mobile bottom sheet;
- hover disclosure → explicit button;
- multi-column compare → stepper or scrollable panels;
- persistent inspector → modal or dedicated route;
- drag-only control → buttons and direct manipulation alternatives.

## Evidence

Capture exact viewport dimensions and zoom or emulation settings. Review screenshots together when hierarchy depends on comparison. Use recordings for menus, overlays, sticky elements, transitions, and orientation changes.
