# Motion design and motion graphics

Use this module when motion is a meaningful part of the website’s identity, storytelling, navigation, feedback, brand expression, or media system. It extends the normal interaction-motion rules; it does not replace them.

## Distinguish the two layers

**Interface motion** explains a product state or relationship. Examples include hover feedback, expanding disclosure, route continuity, drag response, filtering, loading, errors, and success.

**Motion graphics** are authored visual sequences. Examples include kinetic typography, animated brand marks, title cards, composited artwork, editorial loops, explainer sequences, data stories, interactive illustrations, and campaign scenes.

A site may use either layer or both. Do not make a simple interface carry a motion-graphics runtime merely to look sophisticated. Do not reduce a motion-led campaign to generic fade-up components when temporal composition is part of the concept.

## Start with a motion brief

Before choosing a tool, define:

- the job of the motion: orientation, continuity, causality, hierarchy, feedback, attention, character, narrative, explanation, or celebration;
- the emotional temperature: calm, precise, luxurious, playful, tense, ceremonial, energetic, intimate, or another named quality;
- the subject that moves and the subject that remains stable;
- trigger: load, direct action, scroll, route change, data change, time, audio, visibility, or explicit playback;
- lifecycle: one-shot, reversible transition, finite sequence, controlled loop, ambient loop, or interactive state machine;
- interruption and cancellation behaviour;
- no-motion, low-power, unsupported-browser, and slow-network equivalents;
- evidence needed to approve timing and visual quality.

If the motion has no clear job, remove it.

## Temporal composition

Design time with the same care as layout.

### Beats and hierarchy

Break authored sequences into readable beats:

1. establish context;
2. direct attention;
3. reveal or transform the subject;
4. hold long enough to understand it;
5. settle into a useful end state.

The important content must finish in the clearest state. Do not leave the user watching a flourish when the next action is already available.

### Duration roles

Use a small role-based scale rather than arbitrary values:

- **instant feedback**: roughly 70–120 ms for press, hover, toggle, and local acknowledgement;
- **local transition**: roughly 140–260 ms for disclosure, small movement, filter, or compact panel change;
- **structural transition**: roughly 240–450 ms for page regions, major overlays, or meaningful continuity;
- **expressive beat**: roughly 350–700 ms for a rare brand or narrative moment;
- **authored sequence**: timed by beats and comprehension rather than one global duration.

Distance, scale, visual mass, and information density affect perceived speed. Larger changes generally need more time. Frequently repeated actions should be shorter and quieter than rare moments.

### Easing roles

Define reusable easing roles:

- **enter**: arrives quickly and settles;
- **exit**: leaves decisively;
- **standard**: visible throughout the change;
- **emphasised**: reserved for an important expressive moment;
- **direct manipulation**: tracks the user closely, then settles only after release.

Avoid bounce, elastic overshoot, abrupt stops, and mixed curves unless they express a deliberate physical or brand rule. Similar actions should feel related.

### Sequence and stagger

Use stagger to reveal hierarchy, not to animate every child. Keep related elements close in time. Long cascades make users wait and can become repetitive. For multi-element choreography, identify the lead element, dependent elements, overlap, and stable end frame.

### Spatial grammar

Direction should reinforce meaning:

- forward and backward navigation should be distinguishable when useful;
- entrance and dismissal should preserve a believable relationship;
- shared elements may carry identity between states;
- large background or peripheral movement needs extra restraint;
- camera-like movement, depth travel, zoom, and parallax require a stationary reference and a reduced-motion alternative.

## Motion-graphics craft

### Storyboard, style frame, animatic

For substantial sequences, produce three different artifacts:

- **storyboard**: sequence, framing, action, copy, and beats;
- **style frames**: visual finish, type, colour, texture, lighting, compositing, and protected artwork treatment;
- **animatic**: rough timing, holds, transitions, audio relationship, and sequence length.

Do not jump from a mood description directly to polished animation. Timing defects are cheaper to fix in an animatic.

### Kinetic typography

Treat moving type as language first and image second.

Define:

- reading order and line-break authority;
- minimum readable hold time;
- word, line, character, or block-level movement;
- relationship between movement and spoken or musical rhythm;
- safe zones and responsive re-composition;
- whether the text remains selectable and semantic in the DOM;
- captions, transcript, or static equivalent when text is embedded in video or canvas.

Do not make essential copy available only for a few frames. Avoid excessive per-character motion that damages word recognition. Preserve contrast, text scaling, and language expansion.

### Compositing and depth

Document:

- alpha and premultiplication assumptions;
- masks, mattes, clipping, and blend-mode use;
- layer order and occlusion;
- depth and camera rules;
- motion blur and shutter treatment;
- colour space and grading;
- texture, grain, glow, and blur budgets;
- protected artwork crop and aspect-ratio rules;
- transparent-edge and halo checks on light and dark backgrounds.

A convincing composite depends on shared perspective, scale, light, edge treatment, and motion. Effects cannot rescue incompatible source material.

### Loops

Classify loops as functional, illustrative, or ambient. Define the seam, pause point, maximum concurrent loops, offscreen behaviour, low-power behaviour, and user controls. Stop or pause continuous work when it is not visible or no longer useful. Avoid loops that compete with reading or remain active across the whole page.

### Audio relationship

When audio matters, define whether motion follows beats, accents, speech, ambience, or interaction. Never depend on sound alone for meaning. Autoplay audio needs explicit justification and controls. Supply captions or transcripts where the media carries information.

## Choose the lightest delivery route

Select format and runtime from the required result, not from tool preference.

### CSS transitions and animations

Use for direct state changes, small keyframe sequences, simple masks, transforms, opacity, colour, and decorative SVG parts. Prefer this when the animation can remain semantic and does not need complex playback control.

### Web Animations API

Use when JavaScript needs sequencing, cancellation, reversal, dynamic timing, inspection, or playback control. Preserve the underlying DOM change if animation support fails.

### View Transition API

Use for same-document or same-origin route continuity when shared identity and navigation direction matter. Feature-detect it, keep names unique, manage focus and history, and treat the transition as progressive enhancement.

### SVG

Use for scalable line, shape, mask, path, and icon motion when DOM accessibility and CSS or JavaScript control are valuable. Control path complexity and filter cost. Keep essential text as real text when possible.

### Lottie or dotLottie

Use for vector motion exported from an authoring tool when the supported feature set matches the design. Verify the exact player, renderer, masks, gradients, effects, fonts, assets, theming, and platform parity. Optimise keyframes and payloads. Pause offscreen playback and provide a static poster or reduced-motion variant.

Standard Lottie JSON and dotLottie are not identical. Record which format and runtime are required; advanced features such as multi-animation bundles, themes, or state machines may require dotLottie-compatible tooling.

### Rive

Use when the motion graphic needs an interactive state machine, data-driven transitions, reusable artboards, or designer-owned behaviour that must remain editable after integration. Define inputs, states, transitions, settled states, loading, WASM/runtime cost, and a non-interactive fallback.

### Canvas, WebGL, or WebGPU

Use when the visual system requires dense particles, shaders, custom rendering, 3D, image processing, or large numbers of animated objects. This route requires explicit CPU, GPU, memory, battery, input, accessibility, loading, and device fallback budgets. Do not put essential reading or controls only inside a canvas.

### Video or image sequence

Use for photorealistic, heavily composited, simulated, or codec-efficient sequences that do not require internal element interactivity. Define codec and browser support, intrinsic dimensions, poster, preload, autoplay, loop, captions, transparency or alpha requirements, mobile crop, bandwidth variants, and fallback. Avoid GIF for substantial motion when video or vector formats are more efficient.

## Motion asset contract

For every motion asset record:

- asset ID, owner, source, rights, and approved revision;
- storyboard, style-frame, animatic, and final lineage;
- dimensions, aspect ratio, duration, frame rate, colour space, alpha, and audio;
- editable source and delivery format;
- runtime and version;
- trigger, playback, loop, pause, interruption, and end-state rules;
- responsive variants and focal area;
- reduced-motion and static fallback;
- byte, CPU, GPU, memory, and request budgets;
- loading priority and failure state;
- implementation owner and removal path;
- exact evidence required for approval.

Generated motion must retain prompt, model or tool, seed or project identity where available, source assets, edits, and rights status. Do not present a generated preview as an approved master.

## Accessibility and comfort

Use WCAG 2.2 AA as the normal public target and treat animation sensitivity more strictly when the experience is motion-led.

- never communicate essential information through motion alone;
- respect the system reduced-motion preference and add an in-product control when motion remains extensive;
- remove or replace non-essential spatial travel, parallax, zoom, depth, blur travel, and repetitive ambient movement;
- provide pause, stop, or hide controls when automatically moving, blinking, or scrolling content starts by itself, lasts more than five seconds, and runs alongside other content, unless the movement is essential;
- avoid flashes and rapid contrast changes; never exceed three flashes in any one-second period unless the result is demonstrably below the applicable WCAG flash thresholds;
- keep motion local to the task or focal subject;
- preserve keyboard operation, focus, live-region feedback, and reading order;
- provide static posters, transcripts, captions, or semantic equivalents for non-DOM media;
- let people interrupt or skip long sequences;
- test real reduced-motion settings, not merely the existence of a media query.

A fade may be safer than spatial travel, but opacity and blur can still distract. Review the whole composition.

## Performance and energy

- prefer transform and opacity for interface movement where possible;
- avoid repeated layout and paint work in high-frequency animation;
- measure rather than assuming CSS, JavaScript, vector, canvas, or video is cheapest;
- lazy-load non-critical motion and keep the LCP path simple;
- reserve intrinsic space to prevent layout shift;
- stop timers, frame callbacks, decoders, and state machines when hidden or settled;
- cap simultaneous animated regions;
- test representative mobile CPU, GPU, memory, network, battery, and thermal conditions;
- inspect long tasks and input delay while motion is active;
- do not apply `will-change` permanently to many elements;
- provide a lower-complexity route for constrained devices.

## Observe and review

Screenshots approve only frames. Recordings are required for timing, continuity, interruption, scroll relationship, focus movement, and responsive transformation.

For a substantial motion system collect:

- storyboard and approved style frames;
- animatic and timing decision record;
- start, key beat, and settled-state screenshots;
- bounded recordings at declared wide, short, intermediate, narrow, and reduced-motion states;
- keyboard, pointer, touch, scroll, resize, visibility, and cancellation runs;
- slow-load, failed-load, missing-asset, and unsupported-runtime states;
- frame pacing, long-task, memory, CPU/GPU, and request evidence appropriate to the route;
- comparison against the approved asset and motion contract;
- static fallback, captions, transcript, and reduced-motion evidence;
- exact build, runtime, browser, device, viewport, preference, and asset revisions.

Review defects as timing, hierarchy, continuity, rhythm, path, legibility, compositing, performance, comfort, interaction, or fallback failures. “The animation feels off” is not actionable.

## AI motion-builder packet

When asking an AI tool or coding agent to create motion, provide:

- purpose and audience;
- visual concept and protected foundations;
- motion role and emotional temperature;
- storyboard beats and stable end state;
- exact elements allowed to move;
- timing, easing, sequence, path, and loop rules;
- typography, compositing, audio, and asset constraints;
- target format, runtime, browser, and device support;
- reduced-motion and static equivalent;
- byte and performance budgets;
- files or components in scope;
- evidence and rollback requirements;
- explicit instruction not to redesign unrelated surfaces.

Separate generation, integration, and review. An AI-generated animation is a candidate until it has been inspected frame by frame, tested in context, and approved against the Experience Contract.

## Research basis

This module is informed by current official guidance and documentation from W3C/WCAG, Apple Human Interface Guidelines, IBM Carbon, Microsoft Fluent, the Web Animations and View Transition platform documentation, web.dev performance guidance, Adobe After Effects, Rive, and Lottie/dotLottie documentation. See `references/research-basis.md` for source URLs, access date, and the rules derived from them.
