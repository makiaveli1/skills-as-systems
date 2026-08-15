# Animated reference build

Use this packet when creating an original animated site or microsite from visual references.

## Assign reference roles

For every supplied site, image, clip, or recording, name only the mechanism it contributes:

- information architecture;
- composition or spatial rhythm;
- typography hierarchy;
- colour and material treatment;
- artwork treatment;
- interaction pattern;
- motion timing or transition logic;
- responsive behaviour.

State what must not be copied. Do not inherit source branding, text, assets, distinctive composition, or proprietary code.

## Lock the original experience

Before building, define:

- public purpose and audience;
- central visual idea;
- routes, rooms, or states;
- one signature interaction worth prototyping first;
- approved and protected artwork;
- content hierarchy;
- motion purposes;
- browser and performance constraints;
- evidence required for approval.

The result must explain its design logic without naming the reference.

## Protect artwork

For each protected asset record:

- intrinsic dimensions and aspect ratio;
- focal point;
- approved crop behaviour;
- desktop, short-laptop, intermediate, and mobile composition;
- text-overlay rules;
- colour-treatment limits;
- loading priority and responsive sources;
- fallback or alternate asset.

Never stretch artwork. Do not use one `cover` crop for every viewport without review.

## Design responsive compositions

Define explicit states:

- wide desktop;
- standard desktop;
- short laptop or constrained height;
- tablet/intermediate container;
- narrow mobile;
- 320 CSS-pixel reflow.

For each state specify what reflows, stacks, moves, changes interaction, uses an alternate crop, or becomes decorative. Preserve semantic order and task completion.

## Motion grammar

Give every effect a purpose: orientation, continuity, causality, hierarchy, feedback, attention, or brand character.

Prefer:

- CSS transitions for direct state changes;
- CSS keyframes for self-contained sequences;
- Web Animations API for controlled interactive playback;
- View Transition API for progressive route or state continuity;
- specialised libraries only when their capability is necessary.

Preserve function without enhancement. Use transforms and opacity where possible. Avoid scroll hijacking, long pinned scenes, perpetual motion, random stagger, and layout-shifting animation.

## Reduced motion

Design a deliberate equivalent:

- remove spatial travel but keep a clear state change;
- replace morphing with an immediate composition and focus move;
- stop autoplay and ambient loops;
- preserve hierarchy, labels, and orientation;
- test the real system preference.

## AI-builder packet

Give the builder:

- product surface and routes;
- context of use;
- reference-role map;
- original visual grammar;
- protected assets and invariants;
- signature proof target;
- responsive compositions;
- motion and reduced-motion rules;
- framework or codebase constraints;
- acceptance criteria;
- explicit avoid list;
- instruction to preserve source access and modify only bounded areas.

Build foundation first, then components, interaction, responsive corrections, testing, and hardening in separate passes.

## Evidence

Capture screenshots for the major compositions and start/end states. Record the signature interaction, scrolling, overlays, menu behaviour, route continuity, responsive changes, and reduced-motion alternative. A polished preview does not approve the full experience.
