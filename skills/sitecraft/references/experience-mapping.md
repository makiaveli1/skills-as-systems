# Experience mapping

Map what the user must understand and do before choosing a layout.

## Surface inventory

A **surface** is any route, screen, mode, overlay, panel, or distinct state with its own job. For each surface define:

- purpose;
- audience and entry context;
- primary action;
- secondary actions;
- information needed before action;
- success, loading, empty, partial, error, and recovery states;
- navigation entry and exit;
- content authority;
- responsive transformation.

Do not create a page because a common website template includes it.

## One clear job

A screen may support several actions, but one job should dominate. Use the first-screen test:

1. What is this?
2. Who is it for?
3. Why does it matter now?
4. What can the user do next?
5. Why should they trust it?

Not every screen needs to answer all five in text, but the composition and content must make the answers available.

## Journeys

Map journeys as decisions and state changes, not only page sequences.

For each primary journey define:

- trigger;
- user intent;
- information required;
- decision points;
- system responses;
- interruptions and recovery;
- completion signal;
- next likely action.

Include keyboard and narrow-screen implications where the route changes interaction patterns.

## Navigation

Navigation should preserve orientation and priority.

Define:

- global versus local navigation;
- current-location signal;
- forward, backward, and escape behaviour;
- deep-link behaviour;
- browser history behaviour;
- mobile transformation;
- focus destination after route or overlay changes.

Avoid decorative navigation labels, hidden critical routes, duplicate destinations with inconsistent names, and menus that require hover.

## Content hierarchy

Design hierarchy from user questions:

- What must be understood first?
- What can be scanned?
- What requires comparison?
- What is proof?
- What is detail?
- What is optional?
- What is action?

Content order should follow task logic rather than internal company structure.

## States are part of the design

Never treat these as afterthoughts:

- first use;
- empty data;
- slow data;
- partial data;
- permission denied;
- validation error;
- offline or failed request;
- destructive confirmation;
- success and undo;
- expired or stale state.

A polished default screen with weak states is an unfinished experience.

## Conversion without coercion

For marketing and campaign sites, define the conversion path, proof sequence, objection handling, and exit paths. Do not use false urgency, disguised controls, preselected consent, obstructive cancellation, or visual hierarchy that hides material information.

## Map output

For substantial work, produce:

- surface inventory;
- route/state diagram or structured list;
- primary journeys;
- content hierarchy;
- navigation model;
- responsive transformation notes;
- unresolved questions and evidence needs.
