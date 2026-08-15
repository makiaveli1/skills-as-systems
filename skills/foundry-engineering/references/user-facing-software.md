# User-facing software

## Model the experience as states and tasks

For frontend, desktop, and mobile work identify:

- primary tasks and navigation/orientation;
- loading, empty, partial, error, offline, permission, conflict, and success states;
- local versus server authority and synchronization;
- input methods, focus, keyboard, touch, pointer, screen size, text size, language, and assistive technology;
- platform lifecycle: startup, background, resume, interruption, window/process loss, and updates;
- performance and resource budgets.

Do not begin with component hierarchy alone.

## State ownership

Give remote data, local draft, navigation, authentication, feature state, form validation, cache, and optimistic updates explicit owners. Derive view state where possible instead of synchronizing duplicates.

For optimistic operations define pending identity, conflict handling, rollback/reconciliation, duplicate submission, offline retry, and user-visible outcome. Never hide an uncertain write as success.

## Accessibility

Use semantic/native platform controls and APIs first. Verify names, roles, values, focus order and visibility, keyboard and switch paths, touch targets, contrast, text resizing/reflow, error association, status announcements, motion preferences, and alternatives to gesture-only or visual-only interaction.

Automation detects only part of accessibility. Use direct keyboard, accessibility-tree, assistive-technology, zoom/text-size, reduced-motion, and platform checks according to the support promise.

## Responsive and adaptive behaviour

Design intentional compositions and interactions for actual constraints, not scaled screenshots. Check narrow width, short height, intermediate containers, large text, software keyboards, safe areas, rotation, multi-window, and platform chrome.

Preserve task, content, and recovery paths across layouts. Hover, right-click, drag, or gesture cannot be the only path unless the platform contract explicitly allows it.

## Platform integration

Desktop/mobile work must respect:

- application lifecycle and state restoration;
- filesystem, sandbox, permission, notification, deep-link, clipboard, and background-execution contracts;
- signed packaging, updates, rollback, and data-version compatibility;
- battery, memory, network, and storage constraints;
- platform-specific accessibility and interaction conventions.

Verify current OS/SDK requirements against official documentation. Do not generalize evidence from one simulator, browser, architecture, or device to another.

## Frontend performance and reliability

Measure startup, interaction response, rendering/frame pacing, network waterfalls, memory growth, cache behaviour, and error recovery under representative conditions. Prevent duplicate listeners, leaked subscriptions, stale async updates, blocking main-thread work, oversized bundles/media, and hydration/render mismatches where applicable.

## Evidence

Match evidence to claims:

- source/DOM/view hierarchy for structure;
- screenshots for exact visual states;
- recordings for temporal behaviour;
- keyboard/touch/assistive checks for interaction;
- network/runtime logs for integration;
- profiles and field/lab data for performance;
- installed builds on supported platforms for packaging and lifecycle.

A screenshot does not prove interaction, and a component test does not prove the real product journey.
