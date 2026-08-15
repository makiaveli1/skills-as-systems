# Implementation routing

Choose implementation from the experience and maintenance needs, not from fashion.

## Inspect first

For an existing project, inspect:

- framework and version;
- package manager and lockfile;
- route structure;
- rendering model;
- component and style conventions;
- design tokens;
- data and content sources;
- authentication and authorization;
- tests and scripts;
- deployment target;
- current Git state and user changes;
- performance and accessibility tooling;
- public/private boundaries.

Do not replace the stack merely because another stack would be easier to generate.

## Architecture questions

Resolve:

- Is the experience primarily content, commerce, application state, real-time interaction, or a hybrid?
- Which content must be crawlable or shareable?
- Which states require client JavaScript?
- What can be static, server-rendered, streamed, progressively enhanced, or loaded on demand?
- Who will maintain it?
- What hosting and data constraints exist?
- What is the expected traffic and change frequency?
- What happens when JavaScript, a third party, or a network request fails?

## Default bias

Prefer:

- semantic HTML;
- modern CSS;
- native controls;
- progressive enhancement;
- server or static rendering for public content;
- client state only where needed;
- small dependency surface;
- explicit data boundaries;
- stable URLs and browser history;
- reusable tokens and components without over-abstraction.

Do not build a custom component for behaviour a native element already provides well.

## Capability Palette

Native-first is a baseline, not a ban on libraries or frameworks. When the experience needs consequential capabilities beyond ordinary document and component behaviour, create or update the optional Runtime Capability Plan in `implementation.capability_plan`.

For each material choice, record the experience need, stable capability class, selected route, why it earns its complexity, credible rejected routes, integration boundary, fallback, risks, and evidence required. Keep exact product or library names in `selected_route` rather than creating permanent framework-specific contract fields.

A useful route may be browser-native, a small library, an authored animation runtime, canvas, GPU rendering, 3D, a framework feature, a server capability, or a service. Choose by capability fit, accessibility, performance, support, security, maintenance and evidence, not by familiarity or fashion.

When several runtimes are combined, define one owner per concern such as scrolling, animation clock, route state, application state, focus/input, data, media playback, or render loop. State the bridge between systems and the cleanup boundary. Read [capability-palette-and-orchestration.md](capability-palette-and-orchestration.md).

## Framework route

### Static or multi-page

Use when content, speed, crawlability, resilience, and simple deployment dominate. Browser-native view transitions may add continuity without converting the project into an SPA.

### Server-rendered application

Use when public content and dynamic user state coexist. Keep secrets and privileged data on the server. Separate server and client components or boundaries clearly.

### Single-page application

Use when sustained client interaction, offline behaviour, complex local state, or application-like transitions justify the cost. Preserve deep links, history, loading, error, focus, and performance behaviour.

### Islands or partial hydration

Use when most content is static but selected components need rich interaction.

### Canvas, WebGL, or 3D

Use only when the visual or interactive purpose requires it. Provide accessible alternatives, loading strategy, device fallback, input alternatives, and performance budgets.

## Design-system depth

Match system complexity to project scale:

- small site: tokens and a few composition patterns;
- growing product: documented component states and ownership;
- multi-team platform: versioned tokens, accessibility contracts, contribution rules, and visual regression.

Do not create an enterprise design system for a five-page campaign site.

## Change packets

For each implementation batch specify:

- outcome;
- files or modules in scope;
- exact current evidence;
- protected behaviour;
- data or schema implications;
- responsive behaviour;
- accessibility behaviour;
- performance risks;
- security and privacy risks;
- tests;
- visual evidence;
- rollback boundary.

Prefer one coherent batch over many unrelated edits.

## Dependencies

Before adding a package, ask:

- Is the capability already native?
- Is the package maintained and compatible?
- What does it add to the client bundle?
- Does it introduce styling or accessibility assumptions?
- Can it be loaded only where needed?
- How is it removed later?

Record major dependencies in the Experience Contract. For an evidence-bearing build, also record the actual resolved versions of consequential packages and the lockfile or exact build identity that produced the evidence. Manifest version ranges may follow the project's maintenance policy, but a moving label such as `latest` is not a reproducible evidence claim.

## Content and data

Keep content models independent from visual components where practical. Validate untrusted data. Model empty, partial, delayed, stale, and error states.

Never expose privileged data because the current UI hides it. Authorization belongs at the data or server boundary.

## Definition of implemented

A change is implemented when code exists and declared technical checks pass. It is not visually approved or release-ready until the required observation and hardening evidence passes.
