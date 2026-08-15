# Performance

Treat performance as user experience, not a score-chasing exercise.

## Core Web Vitals

Use current official thresholds as default targets for most public sites:

- LCP at or below 2.5 seconds;
- INP at or below 200 milliseconds;
- CLS at or below 0.1;
- evaluate at the 75th percentile, separated across mobile and desktop field data when available.

Lab tools diagnose. Field data describes real users. Record which evidence is available.

## Priorities

### Loading and LCP

- make the likely LCP resource discoverable in initial HTML;
- prioritise the correct hero image, text, or media;
- avoid client-rendering essential first content without need;
- size and compress responsive images;
- subset and preload fonts only when justified;
- reduce server and network delay;
- cache immutable assets;
- remove render-blocking work that has no first-view value.

Do not lazy-load the actual LCP image.

### Responsiveness and INP

- minimise long main-thread tasks;
- reduce unnecessary JavaScript and hydration;
- split expensive work;
- avoid large synchronous renders after input;
- use efficient event delegation and state updates;
- keep third-party scripts bounded;
- measure real interactions, not only initial load.

### Stability and CLS

- provide width and height or aspect ratio for media;
- reserve space for async content, banners, embeds, and ads;
- avoid injecting content above the current reading position;
- use stable font strategies;
- avoid layout-inducing animation;
- verify route and filtered-list transitions.

## Animation

Prefer `transform` and `opacity` where possible. Avoid animating geometry and layout properties unless measured and necessary. Review composited layer count, large blur effects, fixed backgrounds, video, canvas, and WebGL on representative devices.

Do not leave continuous decorative animation running when it is offscreen or no longer useful.

## Images and media

Define:

- intrinsic dimensions;
- format and quality;
- responsive `srcset` and `sizes` where relevant;
- art direction;
- loading priority;
- decode behaviour;
- placeholder strategy;
- CDN or transformation route;
- fallback.

Do not request or ship 4K assets merely because they sound premium. Match source dimensions to display need and density.

## Fonts

Use the smallest family and weight set that preserves the design. Verify fallback metrics, `font-display`, preloading, subsetting, and variable-font trade-offs. A brand font that blocks content or creates major layout shift weakens the brand.

## JavaScript and architecture

Default to server-rendered or static content when interaction does not require client state. Use islands, partial hydration, or progressive enhancement when the framework supports them and the project benefits.

Do not turn a content site into a large client application to gain simple transitions.

## Third parties

Inventory analytics, embeds, chat, consent, ads, maps, video, and tracking. Record:

- owner and purpose;
- loading phase;
- data impact;
- performance impact;
- failure behaviour;
- consent requirement;
- removal plan.

## Budgets

Set project-specific budgets for:

- initial JavaScript;
- CSS;
- hero media;
- total first-view transfer;
- third-party work;
- animation frame cost;
- route transition latency.

Budgets are decision tools, not universal numbers.

## Evidence

Use a mix of:

- production or preview field data;
- Lighthouse or equivalent lab runs;
- browser performance traces;
- network waterfalls;
- bundle analysis;
- CPU and network throttling;
- representative mobile hardware where possible.

Do not claim production performance from a single local desktop run.
