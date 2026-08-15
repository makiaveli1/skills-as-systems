# Visual system

Create a visual grammar that can generate many coherent screens without making every screen identical.

## Start with one dominant idea

Describe the visual concept as a relationship between purpose and form, for example:

- archival evidence arranged like an editorial reading room;
- a live operations system with dense status hierarchy and calm control;
- a music world presented as navigable rooms rather than a promotional landing page;
- a training site that feels like a clear field guide rather than enterprise software.

Do not begin with a list of adjectives or fashionable effects.

## Define roles, not swatches

### Colour

Assign roles:

- canvas;
- raised or inset surface;
- primary text;
- secondary text;
- border and separator;
- primary action;
- secondary action;
- focus;
- success, warning, error, and information;
- artwork or campaign accent.

Test combinations in real components. A palette is not accessible because individual hex values look attractive.

### Typography

Define:

- display voice;
- interface heading;
- body and long-form reading;
- label and metadata;
- numeric or tabular data;
- code where relevant;
- fallbacks and loading behaviour.

Use fluid type carefully. Preserve browser zoom and user font settings by retaining `rem` influence in `clamp()` and container-query formulas.

### Spacing and density

Create a rhythm with a small set of intentional steps. Define where the interface is spacious, compressed, or data-dense. Do not give every section identical top and bottom padding.

### Shape, edge, and depth

Define when to use square, rounded, clipped, framed, inset, elevated, or border-only treatments. Avoid assigning every block the same large radius and shadow.

## Layout grammar

Record:

- grid and alignment logic;
- container strategy;
- text measure;
- full-bleed and constrained regions;
- overlap and layering rules;
- asymmetry rules;
- focal-point placement;
- negative-space behaviour;
- exceptions.

Use layout to communicate hierarchy. Do not depend on card borders to explain every relationship.

## Component language

Define components as behaviour plus appearance:

- anatomy;
- content constraints;
- states;
- responsive behaviour;
- keyboard and focus behaviour;
- motion behaviour;
- token ownership;
- allowed variants.

A design system should reduce accidental inconsistency without flattening the experience into generic primitives.

## Imagery and protected artwork

For each image role define:

- source and rights status;
- crop behaviour;
- focal point;
- aspect ratio;
- intrinsic dimensions;
- colour treatment;
- overlay or text rules;
- loading priority;
- alt-text purpose;
- mobile crop or alternate asset.

Protect approved artwork proportions. Use `object-fit`, intrinsic sizing, dedicated wrappers, or alternate compositions instead of stretching or arbitrary cropping.

## Project-specific distinction chain

When visual or experiential distinction materially matters, build a short traceable chain before choosing effects or runtimes:

1. name the concrete project drivers — user behaviour, content shape, brand truth, product behaviour, place, material, category convention, trust need or another real constraint;
2. derive a small number of design mechanisms from those drivers;
3. state where each mechanism appears and what job it performs;
4. state what each mechanism must not drift into;
5. name familiar patterns that should remain familiar because they protect orientation, accessibility, trust or task completion;
6. record anti-repetition rules when a previous SITECRAFT project, showcase or fashionable pattern could bias the direction.

Use optional `visual_grammar.creative_distinction` for this when the distinction is consequential. Leave it `null` for ordinary work where the dominant idea and normal visual grammar are sufficient.

Do not invent a signature mechanism merely to fill the field. A task-specific utility site can be excellent through unusually clear information hierarchy, precise states, disciplined density and trustworthy content without theatrical novelty.

## Reference transformation

When using a reference site, image, or tutorial:

1. identify the useful mechanism;
2. identify what makes it specific to the source;
3. retain the mechanism only when it supports the new purpose;
4. change composition, content logic, brand language, and implementation details;
5. translate the mechanism into the project’s own tokens, typography, components, responsive rules, accessibility requirements, and existing implementation conventions;
6. verify that the result no longer depends on source imitation.

If the design direction is genuinely unresolved, compare structurally different experience arguments before polishing one. If the brief already provides a strong approved direction, do not create alternative concepts merely to satisfy a process ritual. Record consequential divergence/convergence in optional `visual_grammar.direction_selection`.

## Anti-generic review

Reject or justify:

- purple or blue gradient as default “AI” identity;
- decorative glassmorphism;
- floating feature-card grids;
- fake dashboards and meaningless charts;
- giant rounded rectangles around every section;
- stock photos of smiling office teams;
- abstract blobs and sparkles with no brand role;
- repeated centred headline/subheadline/button stacks;
- random icon libraries with mixed stroke and fill systems;
- uniform reveal animation on every element;
- content rewritten into vague startup language.

## Visual-system output

Produce:

- dominant visual idea;
- token roles;
- type system;
- layout grammar;
- component rules;
- imagery rules;
- motion relationship;
- protected foundations;
- deliberate exceptions;
- anti-pattern list.
