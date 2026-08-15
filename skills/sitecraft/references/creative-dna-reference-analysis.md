# Creative DNA Reference Analysis

Use Creative DNA analysis when the user gives a website, campaign, video, image, product page, motion reference, or visual system they like and wants Sitecraft to learn from it without cloning it.

The purpose is to extract *transferable design logic* rather than surface-copying a reference.

## The three-step rule

1. **Extract** — identify observable design decisions and the role each one plays.
2. **Abstract** — convert those decisions into reusable principles independent of the source brand/content.
3. **Recombine** — rebuild the principles around the user's own brand, content, assets, and experience goal.

Never treat "make it like this" as permission to reproduce protected copy, logos, signature illustrations, exact layouts, or distinctive proprietary assets.

## Creative DNA map

Analyze only the dimensions relevant to the task.

### 1. Core idea
- What is the experience trying to make the visitor feel or understand?
- What is the single memorable visual/interaction idea?
- What is deliberately restrained?

### 2. Composition DNA
- dominant focal point
- symmetry/asymmetry
- foreground/midground/background relationships
- negative-space behavior
- crop and scale language
- viewport occupation and density
- section rhythm and transitions

### 3. Color and light DNA
- palette roles, not just hex values
- contrast hierarchy
- key/fill/rim or ambient-light logic
- gradients, glow, bloom, shadow, haze, grain
- how color changes with interaction or narrative state

### 4. Typography DNA
- display/body relationship
- scale jumps
- weight/width/spacing behavior
- line-length and rhythm
- type as interface vs type as visual material
- animated or spatial typography behavior

### 5. Material and texture DNA
- glass, metal, paper, cloth, skin, liquid, grain, noise, blur, depth
- edge treatment and surface response
- 2D/3D/photographic/illustrative balance

### 6. Image and asset DNA
- subject treatment
- camera/framing logic
- cutout vs environmental imagery
- reference-role mapping
- identity consistency requirements
- generated vs captured asset boundaries

### 7. Motion DNA
- what moves and what stays still
- easing character
- speed range and rhythm
- scroll coupling
- pointer/touch response
- parallax depth
- continuous generated motion vs programmatic transform
- idle behavior and interaction takeover
- reduced-motion fallback

### 8. Interaction DNA
- discoverability of interactive areas
- hover/focus/press/drag/scroll states
- feedback latency and damping
- direct-manipulation feeling vs cinematic playback
- whether motion communicates state or only decorates it

### 9. Narrative DNA
- opening promise
- reveal order
- tension/build/payoff
- repeated motifs
- route/section continuity
- what the user learns at each beat

### 10. Production DNA
- likely asset types
- runtime complexity
- responsive strategy
- performance tradeoffs
- accessibility implications
- what must be generated once vs rendered in-browser

## Output format

For each important reference, produce:

```text
REFERENCE: [name/url/file]
ROLE: [composition / motion / lighting / typography / identity / interaction / etc.]
OBSERVABLE DNA:
- ...
TRANSFERABLE PRINCIPLES:
- ...
DO NOT COPY:
- ...
SITECRAFT TRANSLATION:
- ...
PROOF NEEDED:
- ...
```

Then synthesize a project-level Creative DNA contract containing only the principles that will actually be implemented.

## Reference conflict rule

When multiple references disagree, assign each a role. Example:

- Reference A controls composition.
- Reference B controls motion rhythm.
- Reference C controls lighting/material mood.
- The user's brand system controls color and typography.

Do not average conflicting references into an incoherent style soup.

## Acceptance test

A Creative DNA analysis is good only if:

- another designer/developer can implement it without seeing the original reference
- it explains *why* each borrowed principle matters
- it identifies what must not be copied
- it distinguishes identity/style references from motion/camera/layout references
- it converts inspiration into implementation and QA requirements
- the finished product still reads as the user's own brand/system
