# Animated-site tutorial pattern study

This reference records the reusable workflow observed from the supplied animated website-building tutorial. It does not reproduce the tutorial, its source code, or any particular site's protected design.

## Observed workflow

1. Curate a small set of high-quality website references.
2. Select one focused interaction or animated section rather than imitating an entire site.
3. Show a concrete preview of the intended result.
4. Produce a detailed full-build prompt that includes the visual and motion requirements.
5. Keep source-code access so the generated implementation can be inspected and changed.
6. Refine with small, controlled follow-up requests.
7. Review responsive behaviour after the primary experience exists.

## Image-production pattern observed

The tutorial's strongest image lesson is the separation of reference responsibilities. The creator did not rely on one vague style image. He combined multiple inputs with different jobs: an existing composition for spatial logic, an abstract form for the recurring motif, and another source for colour/material direction. He then described which parts to replace and which qualities to preserve.

The still image was resolved before motion. Animation was treated as a second handoff with its own reference and movement instruction rather than asking one generation to invent the image and its behaviour simultaneously.

SITECRAFT adapts this as:

1. map the website role of each required image;
2. label every reference as identity, composition, form, palette/material, lighting, environment, motion, exclusion, or another bounded role;
3. state what to ignore from every reference;
4. generate and approve a still master;
5. create responsive derivatives;
6. hand the approved still to a separate motion brief;
7. verify the result inside the real website composition.

The lesson is the decision structure, not the tutorial's artwork, prompts, provider, or visual expression.

## What is valuable

### Reference curation reduces vague taste language

A concrete reference communicates composition, density, timing, and interaction more effectively than saying “make it premium” or “make it animated.” SITECRAFT should assign a specific role to each reference and extract the mechanism rather than copy the expression.

### A focused animated preview creates a shared target

A short preview can establish the central interaction grammar before a whole site is built. Use it as evidence for timing, spatial logic, and visual hierarchy, not as proof that every route and device is solved.

### A complete first-build brief prevents random invention

The first prompt should define the product surface, context of use, design rules, motion purpose, responsive expectations, and constraints. It should not attempt to solve every final detail in prose.

### Source access preserves ownership and repairability

Generated output must remain inspectable. The user should be able to change components, styles, assets, and logic without returning to the same generator forever.

### Small follow-ups reduce drift

Once the foundation is coherent, make one or two major changes per pass. Restate what must remain unchanged. This is more reliable than repeatedly regenerating the whole site.

### Responsive review must be planned earlier

The tutorial reviews responsive behaviour after the primary build. SITECRAFT strengthens this by defining responsive composition in the Experience Contract before implementation, then verifying it after implementation. This avoids treating mobile as a late squeeze pass.

## SITECRAFT adaptation

Use the tutorial pattern as this sequence:

1. **Reference roles** — identify what each reference contributes.
2. **Experience Contract** — define purpose, surface map, visual grammar, motion, responsive behaviour, and evidence.
3. **Signature proof** — prototype the most important interaction or visual composition.
4. **Foundation build** — establish routes, tokens, content structure, and protected assets.
5. **Bounded passes** — add components, states, motion, and data in controlled changes.
6. **Observe** — capture screenshots and recordings at named states.
7. **Repair** — issue evidence-tied change prompts.
8. **Harden** — accessibility, performance, security, metadata, and release review.

## What not to inherit

Do not assume:

- a visually impressive preview is a usable product;
- the reference is legally or strategically safe to clone;
- one generated prompt replaces information architecture;
- generated source is maintainable without inspection;
- desktop-first animation survives mobile unchanged;
- responsive review can remain an afterthought;
- a builder's preview equals production evidence.

## Tutorial-derived prompt checklist

A build prompt based on references should include:

- asset or product type;
- audience and use moment;
- exact surfaces and actions;
- reference role map;
- original visual concept;
- layout and content hierarchy;
- motion purpose and timing grammar;
- reduced-motion behaviour;
- responsive compositions;
- protected assets and invariants;
- framework or project constraints;
- acceptance criteria;
- explicit avoid list;
- instruction to preserve source access and make bounded changes.
