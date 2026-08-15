# Narrative motion and living media

Use this module when a website should unfold as a directed experience over time rather than as a conventional stack of sections. It extends `motion-design-and-graphics.md`; it does not replace clear content, semantic structure, accessibility, performance, or ordinary interface feedback.

## Choose motion depth

Motion depth is a creative and production decision, not a quality score.

- **Quiet** — mostly static composition with necessary feedback and restrained reveals.
- **Polished** — normal interface motion, section entrances, hover/focus responses, and occasional editorial transitions.
- **Chapter-led** — one to three important passages unfold through authored scroll or time-based scenes while the rest remains conventional.
- **Motion-led** — the complete experience is storyboarded as a sequence of chapters with living media, responsive alternatives, controls, and motion-specific evidence.

Quiet is a valid premium choice. Do not escalate motion depth merely to make a site appear expensive.

## Originality rule

Do not turn any successful reference, lab, scene type, motif, transition, colour system, or implementation into SITECRAFT's default style.

Every project must derive its narrative device from its own purpose, audience, content, emotional world, assets, and constraints. Continuity may come from a recurring object, character, place, material, camera rule, typographic behaviour, sound relationship, data transformation, spatial frame, chapter rhythm, or another original device. A recurring motif is optional.

Reference analysis should extract mechanisms, not appearance. Never copy a reference site's visual identity, wording, assets, exact scene sequence, or signature effects.

## Write the argument before the animation

Define:

1. the proposition or emotional argument;
2. the chapters required to communicate it;
3. practical information that must remain easy to find;
4. the conversion or completion path;
5. the semantic reading order without animation.

The visitor must understand the essential message when animation, canvas, video, or advanced browser APIs fail.

## Narrative chapter contract

For every authored chapter record:

- **purpose** — what the visitor should understand, feel, or decide;
- **main subject** — the element carrying that beat;
- **continuity device** — optional orientation or relationship to surrounding chapters;
- **arrival** — the first readable state;
- **transition** — the transformation that advances the argument;
- **readable hold** — the settled state where copy and action can be understood;
- **handoff** — how it prepares the next chapter;
- **reverse behaviour** — what happens when the visitor scrolls or navigates backwards;
- **responsive transformation** — the smaller-screen composition, not merely a crop;
- **reduced-motion equivalent** — the direct static or low-motion version;
- **failure state** — what remains when media or runtime support is unavailable.

Do not make every chapter move in the same way. Scene types may include title cards, visual metaphors, kinetic type, character or environmental change, diagrams, comparison states, quiet editorial explanations, ambient pauses, questions, conversion moments, or other project-specific ideas.

## Arrival, transition, hold, handoff

Separate four temporal states:

1. **Arrival** establishes context.
2. **Transition** reveals, transforms, compares, or reorients.
3. **Readable hold** gives the visitor time to understand and act.
4. **Handoff** creates continuity into the next chapter.

Some scenes may be scrubbed by scroll progress. Others may use a threshold trigger followed by a finite sequence. Combining both is valid when their jobs are explicit. Never hide essential content in a fleeting transition frame.

## Orientation without sameness

Large scene changes need orientation, but not every website needs the same persistent rail, grid, motif, or visual frame.

Choose only what the concept needs, such as:

- brand mark or chapter label;
- progress indicator;
- stable navigation or action;
- recurring baseline, horizon, camera position, type role, sound cue, or colour function;
- deliberate contrast and pacing between chapters.

Orientation devices must remain responsive, keyboard-safe, and unobtrusive. A project may use none visually if its content flow already provides sufficient continuity.

## Contrast pacing

Continuous spectacle becomes flat. Alternate density and energy intentionally:

- image-rich scene → sparse title or copy state;
- energetic transformation → readable editorial hold;
- close detail → open spatial pause;
- moving media → still or nearly still composition.

Use contrast to control attention, comprehension, and emotional intensity.

## Living media

Living media keeps a scene active when the visitor is not scrolling. It may use video, canvas, WebGL, image sequences, vector runtimes, or restrained DOM animation.

### Ambient media loop contract

For every loop define:

- narrative or emotional job;
- source, rights, and approved revision;
- delivery route;
- duration and seam strategy;
- mute, autoplay, inline-playback, and control rules;
- poster and first meaningful frame;
- visibility, tab-hidden, and offscreen pause behaviour;
- mobile and constrained-device route;
- reduced-motion and static fallback;
- byte, decode, CPU, GPU, memory, battery, and request budget;
- maximum concurrent loops;
- evidence required to prove playback, seam, pause policy, and fallback.

Automatic motion that lasts more than five seconds and runs beside other content normally needs a pause, stop, or hide mechanism unless essential. Ambient media must never be the only carrier of meaning.

Use direct `<video>` when simple playback is sufficient. Use canvas or WebGL compositing only when the concept genuinely needs masks, shaders, image processing, particles, multiple media layers, or video-as-texture treatment. Keep semantic content and controls outside canvas.

Pause decoders, frame loops, and rendering work when media is offscreen, the tab is hidden, the scene has settled, or reduced motion replaces it.

## Bounded hero variation

A website may select from a small approved set of hero expressions on a new session or refresh. Variation should add replay value without changing the proposition.

Every variant must preserve:

- the same core message and CTA hierarchy;
- equivalent text-safe geometry and contrast;
- compatible focal role and crop behaviour;
- comparable loading and performance cost;
- mobile and reduced-motion equivalents;
- one stable selection during the session;
- approved ownership, lineage, and evidence.

Define the selection policy: random, weighted, sequential, campaign-controlled, audience-controlled, or experiment-controlled. Avoid repeating the last variant when practical. Load only the selected heavy asset unless deliberate preloading is justified.

Do not randomise pricing, navigation, accessibility, legal copy, core conversion logic, or other consequential information.

## Scroll-linked implementation

A common chapter structure uses a tall section containing a viewport-sized sticky stage. Section progress drives state while the stage remains visible. This is one possible pattern, not a required template.

Choose the lightest route:

- CSS scroll-driven animations for simple progress-linked transforms when support and fallback are acceptable;
- Web Animations API for inspectable, reversible, cancellable DOM sequences;
- a specialised timeline library only when pinning, cross-scene sequencing, or browser consistency justifies it;
- canvas, WebGL, or WebGPU for dense custom rendering;
- video or image sequences for photorealistic or heavily composited motion.

Avoid scroll hijacking. Preserve native scrolling, keyboard navigation, history, focus, and direct access to content.

## Responsive transformation

A narrow experience may need a different scene order, crop, density, interaction model, or motion depth. Do not reproduce a desktop pinned sequence at any cost.

Possible changes include shortening scroll distance, removing peripheral layers, replacing a multi-layer scene with one decisive composition, reducing hero variants, moving navigation back into normal flow, or replacing video/canvas with a poster or lighter loop.

## Reduced motion and user control

For chapter-led or motion-led work:

- respect `prefers-reduced-motion` from first render;
- provide an in-product pause or calm control when substantial motion remains;
- replace continuous loops, depth travel, zoom, parallax, blur travel, and rapid peripheral movement;
- show the chapter's clearest settled state directly;
- preserve information, CTA, reading order, and emotional intent;
- test the real operating-system preference and the user control separately.

## Evidence floor

A motion-led claim requires more than still screenshots. Collect:

- chapter beat sheet, style frames, and animatic or timing prototype;
- arrival, transition, readable-hold, and handoff frames for representative chapters;
- forward and reverse recordings;
- hero-variation evidence across repeated sessions;
- loop start, seam, continued playback, offscreen pause, tab-hidden pause, and user-pause evidence;
- wide, short, intermediate, narrow, touch, and reduced-motion recordings;
- semantic, keyboard, focus, and screen-reader checks;
- fallbacks with JavaScript, media, or advanced runtime unavailable;
- frame pacing, long tasks, input delay, memory, CPU/GPU, requests, and constrained-device evidence appropriate to the route;
- exact build, asset, browser, operating system, viewport, input, and preference identities.

A still approves only a frame. A recording cannot prove accessibility or performance. A DOM check cannot prove choreography. Scope every claim to the evidence actually collected.

## Promotion rule

Treat new narrative-motion mechanisms as project or lab experiments first. Add them to SITECRAFT's portable core only after they solve a recurring problem on more than one meaningfully different project, remain explainable in a small rule or optional artifact, and do not force future sites into the same creative language.
