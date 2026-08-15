# Failure tests

Use these as vetoes. A strong score in one area must not hide a critical failure in another.

## Purpose failure

Fail when:

- the first screen cannot explain what the experience is or what to do;
- sections exist only because a template expects them;
- visual spectacle competes with the primary task;
- conversion goals override trust or informed choice;
- the design solves an internal organisation chart rather than the user's need.

## Generic-AI failure

Fail when the site relies on interchangeable patterns without a project reason:

- purple gradient or neon glow as default AI identity;
- glass cards floating over a blurred background;
- repeated centred headline/subheadline/button sections;
- uniform oversized rounded cards;
- fake analytics and meaningless charts;
- random sparkles, grids, blobs, and orbiting icons;
- generic “future of innovation” copy;
- identical fade-up animation on every element;
- stock people or generated faces with no content role.

A familiar pattern is allowed when it serves the task and the rest of the system remains specific.

## House-style repetition failure

Fail or redesign when SITECRAFT's own prior successes become an unearned house style:

- a previous showcase's hero composition, recurring motif, chapter rhythm, transition device, image sequence or signature interaction reappears mainly because it worked before;
- several projects use different colours or libraries but preserve the same underlying page argument and scene sequence;
- a technology choice such as 3D, generated video, canvas, scroll choreography or a motion library is treated as the source of creative distinction;
- the design cannot trace its distinctive mechanisms back to concrete project drivers, content, brand truth, user behaviour or category contrast;
- references are analysed correctly but the final synthesis still reproduces their combined visual logic rather than forming a project-specific system;
- novelty is added to familiar tasks that would be clearer with conventional navigation, controls, forms or reading patterns.

Do not fail merely because a pattern is familiar. Keep familiar interaction when it protects orientation, accessibility, trust or task completion. The failure is unearned repetition or novelty theatre, not reuse itself.

## Reference-copy failure

Fail when:

- composition, imagery, type treatment, motion, or distinctive details reproduce a reference too closely;
- the result depends on another brand's identity;
- source code or assets were copied without rights;
- the prompt names a reference but does not define what to transform;
- the new experience cannot explain its own design logic.

## Information-architecture failure

Fail when:

- routes and states have no clear job;
- navigation hides critical destinations;
- different labels lead to the same place without reason;
- browser back, deep links, or current-location signals are broken;
- empty, error, loading, or permission states are missing;
- mobile removes meaningful content or actions.

## Visual-system failure

Fail when:

- colour values have no roles;
- hierarchy relies only on card borders;
- spacing is uniform rather than intentional;
- typography cannot handle real content;
- components use inconsistent states or icons;
- protected artwork is stretched, over-cropped, recoloured, or obscured;
- the interface looks like several unrelated themes.

## Responsive failure

Fail when:

- desktop is merely scaled down;
- layout works only at common presets;
- short viewports hide actions or trap scrolling;
- 320 CSS-pixel reflow requires two-dimensional scrolling without a justified exception;
- hover-only functions remain on touch;
- sticky or fixed elements obscure focus or content;
- text enlargement breaks containers;
- mobile interaction patterns are not intentionally redesigned.

## Motion failure

Fail when:

- animation has no purpose;
- scrolling is hijacked;
- motion blocks input or delays content;
- reduced-motion mode removes essential orientation or function;
- layout-inducing animation causes instability;
- ambient motion never stops;
- route transitions break history, focus, or aspect ratio;
- a still screenshot is used to approve temporal behaviour.

## Accessibility failure

Fail when:

- essential actions are not keyboard operable;
- focus is invisible, trapped, lost, or obscured;
- visible labels and accessible names disagree;
- semantic order conflicts with visual order;
- contrast, status, or meaning relies on colour alone;
- forms do not identify errors clearly;
- automated tools are treated as proof of conformance;
- the reduced-motion preference is ignored.

## Performance failure

Fail when:

- the LCP resource is hidden behind unnecessary client work;
- large media is shipped without sizing or responsive variants;
- layout shifts are visible or unreserved content appears;
- interaction is blocked by long tasks;
- heavy libraries duplicate browser-native features;
- performance is claimed from one unthrottled local run;
- decorative effects dominate the device budget.

## Security and privacy failure

Fail when:

- secrets or privileged data enter the browser bundle;
- private content is shipped and hidden client-side;
- authorization exists only in UI conditions;
- source maps, debug routes, stack traces, or internal metadata leak unintentionally;
- third-party scripts have no purpose, owner, or data review;
- public and private builds share an uncontrolled export path;
- the builder prompt contains production secrets or sensitive user data.

## Evidence failure

Fail when:

- “tested,” “reviewed,” “saved,” “deployed,” or “verified” lacks tool evidence;
- screenshots omit relevant dimensions or state;
- recordings do not show the complete interaction;
- a build or lint pass is treated as visual approval;
- baselines are updated without review;
- implementation changes occur after approval without revalidation;
- a result from one operating system, browser engine, input mode, assistive technology, or capture provider is presented as universal evidence;
- a path simulation, parser test, container, or emulation is described as real execution on an untested platform;
- exact release state cannot be identified.

## Release veto

Do not call the project ready when any blocking failure remains, required evidence is missing, or owner approval does not cover the exact state being released.
