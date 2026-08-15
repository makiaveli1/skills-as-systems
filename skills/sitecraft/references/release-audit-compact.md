# Compact release audit

Use this packet when the user asks whether a website is safe or ready to deploy. Do not modify the project unless separately authorised.

## Establish exact state

Record:

- project and deployment target;
- branch, commit, build, or immutable artefact identity;
- Experience Contract revision;
- environment and configuration profile;
- promised operating systems, browsers, engines, form factors, and input modes;
- environment-matrix rows actually tested, with status and evidence;
- routes, roles, and states in scope;
- evidence date and freshness;
- known exclusions.

A green build without exact-state identity is not a release receipt. A pass on one operating system or browser engine is not a cross-platform release receipt.

## Accessibility pass

Verify at minimum:

- semantic structure and meaningful names;
- full keyboard path and visible, unobscured focus;
- dialogs, menus, errors, status, and validation behaviour;
- contrast and non-colour state cues;
- target sizes and non-drag alternatives;
- 320 CSS-pixel reflow, zoom, and text spacing;
- reduced-motion behaviour;
- representative assistive-technology spot checks.

Automated scans are supporting evidence, not conformance proof.

## Performance pass

Distinguish field and lab evidence. Review:

- LCP candidate, discovery, priority, and media sizing;
- INP risks from long tasks, hydration, rendering, and third parties;
- CLS from media, fonts, async content, banners, and transitions;
- JavaScript, CSS, font, image, and third-party budgets;
- representative mobile CPU and network conditions;
- animation properties and continuous work.

Use current official Core Web Vitals thresholds and record the measurement environment.

## Security and privacy pass

Inspect:

- public bundles, static output, source maps, comments, debug routes, and stack traces;
- secrets and environment-variable classification;
- direct access to privileged routes, objects, files, and media;
- authentication, authorization, session expiry, logout, and caching;
- validation, uploads, redirects, rich text, embeds, and error leakage;
- CSP, cookies, CORS, frame policy, referrer policy, permissions policy, and eligible SRI;
- third-party scripts, data sent, consent, owner, and removal path;
- physical exclusion of private tools, metadata, fixtures, and unpublished assets.

Anything delivered to the browser is inspectable.

## Visual and interaction evidence

Require the views and states declared by the Experience Contract, normally including:

- wide and standard desktop;
- short laptop;
- intermediate/tablet;
- narrow mobile;
- 320 CSS-pixel reflow;
- loading, empty, error, success, and permission states;
- keyboard path;
- default and reduced motion;
- overlays, navigation, sticky elements, and browser history.

Use screenshots for composition and recordings for timing and behaviour. Neither replaces semantic or functional testing.

## Metadata and operations

Review:

- titles, descriptions, canonical URLs, social previews, favicons, robots, sitemap, structured data where relevant, and error pages;
- deployment variables, migrations, cache invalidation, observability, alerts, backup, rollback, and incident ownership;
- dependency and third-party status;
- legal, consent, data-retention, and content-ownership requirements appropriate to the project.

## Capability traceability

When the Experience Contract contains material `implementation.capability_plan` entries, check that consequential decisions are traceable into the evidence ledger and current SITECRAFT Review. `capability_scope.reviewed_ids` should identify what was actually reviewed, `unreviewed_ids` should remain explicit, and blockers/findings/repairs should reference the relevant decision IDs when the issue belongs to a specific capability. Do not mark a capability reviewed merely because its dependency is present or the project builds.

## Cross-platform release boundary

Compare `implementation.browser_support` with the environment matrix. Every material support row must be passed, explicitly not required, or accepted by the owner as a bounded exclusion. Local path simulations, schema checks, or one browser engine cannot substitute for real execution in a promised environment. When required machines or services are unavailable, keep the row planned and narrow the release claim or keep release blocked.

## Decision

Return one state:

- `not_ready` — one or more blocking failures or no trustworthy exact state;
- `conditionally_ready` — bounded non-blocking risks are explicitly accepted by the owner;
- `ready_for_owner_approval` — verification is current but release authority is still pending;
- `approved_for_release` — the owner approved the exact evidenced state;
- `released_verified` — the approved state was deployed and post-release evidence matches.

List blockers, accepted risks, stale evidence, and the exact next action. Never publish from an audit request alone.
