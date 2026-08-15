# Interactive Generated Motion

Use this workflow when a website needs a subject to move with scroll, pointer, drag, touch, device orientation, or application state and ordinary CSS/SVG transforms cannot produce the desired physical or cinematic change.

This pattern is informed by Oil Motion's core idea: generate one coherent continuous motion first, clean it, then map user input to deterministic animation progress. The browser should not regenerate AI video during interaction.

## Choose this only when it earns its cost

Good fits:
- product teardown/assembly
- character or mascot turning/following
- material transformation
- pose or state transitions that require occlusion/deformation
- interactive chapter transitions
- generated motion used as a Wallpaper-Engine-like living scene

Do not use it for simple fades, translation, scale, hover states, or decorative parallax that normal web animation can render more cheaply and accessibly.

## Production pipeline

### 1. Define the interaction contract

Specify:
- what the motion communicates
- input source: scroll, pointer X/Y, drag, touch, orientation, app/audio state
- start/middle/end states
- reversible vs one-way behavior
- idle behavior
- desktop/mobile display size
- first-frame and failure fallbacks
- reduced-motion behavior

### 2. Lock key frames

Generate/approve the states that cannot drift. For identity-sensitive subjects, use the Character Identity Board as a master reference.

At minimum define start and end. Add middle/key transition frames when structure, pose, product geometry, wardrobe, branding, or scene layout is likely to drift.

### 3. Generate one continuous motion

Use the best available video model for the job. Keep the generation task focused on physical/visual transformation. Leave translation, scaling, crop, simple camera offset, playback damping, and input mapping to code when code can perform them more reliably.

### 4. Frame QA and cleanup

Inspect the generated sequence for:
- duplicated/near-duplicate frames
- leading/trailing pauses
- hard cuts or flash frames
- identity or geometry drift
- flicker and color jumps
- extra limbs/parts
- broken text/logo details
- unstable transparent/chroma edges

Trim and repair before wiring interaction.

### 5. Delivery format decision

Prefer a single primary route for each animation.

**Alpha WebP sprite/sequence**
- strong for compact, frequently seeked motion
- easy deterministic random access
- useful when transparency is required and total frame area remains reasonable

**All-keyframe chroma MP4 + runtime keying**
- useful for larger/longer one-dimensional motion where an RGBA atlas would be too large
- video compression reduces transfer size
- WebGL/canvas can remove the chroma background at runtime

Other formats are allowed only when project evidence shows they are a better fit. Do not ship multiple heavy primary formats "just in case."

### 6. Map input to progress

Normalize the control input to `0..1`, clamp it, then map it deterministically to frame/time progress.

Examples:
- scroll progress -> animation progress
- horizontal pointer position -> left/right pose progress
- drag distance -> reversible motion progress
- device tilt -> bounded pose/orientation progress
- application/audio state -> a named motion segment

Use `requestAnimationFrame` for visual updates. Keep event handlers light. Apply damping/velocity limits where direct input would otherwise cause jitter.

### 7. Two-dimensional input rule

If both X and Y meaningfully alter pose/viewpoint, one linear clip is not enough. Use an appropriate 2D representation such as a frame grid/manifold, separate coupled axes with validated composition, or a true realtime 3D/2D rig.

Do not pretend a left-right timeline contains missing up/down states.

## Living / Wallpaper-style motion

For ambient scenes, distinguish two layers:

1. **Ambient loop/state** — subtle autonomous movement that keeps the scene alive.
2. **Interactive override/follow** — user or application input temporarily steers progress, focus, camera, intensity, or a related motion channel.

Transitions between idle and follow states must be damped and reversible. Avoid sudden jumps to a distant frame.

Audio-reactive use should map stable derived audio features (for example envelope/energy bands or beat events) to bounded visual parameters, not raw sample noise.

## Performance and accessibility

Required:
- meaningful first frame before heavy assets finish loading
- static/fallback visual on load failure
- `prefers-reduced-motion` path that removes non-essential continuous motion
- mobile-specific asset budget when desktop assets are oversized
- no unbounded frame allocations during interaction
- decode/preload strategy based on real display size
- cleanup for listeners, animation frames, WebGL/canvas resources
- interaction remains usable with keyboard/focus where motion is tied to a control

## Evidence

Record:
- source/generation asset IDs and prompts
- approved key frames
- chosen delivery format and why
- frame count/resolution/encoded size
- desktop/mobile behavior
- reduced-motion behavior
- fast-scroll/reversal/pointer stress result
- final viewport evidence

## Acceptance test

The feature passes only if:
- motion follows the intended input direction at all times
- reverse interaction returns through the same coherent states when reversibility is promised
- fast input does not jitter, wrap, or go out of bounds
- identity/structure remains stable across frames
- first/fallback frames are correct
- mobile performance is acceptable with its own budget
- reduced-motion users still receive the content and functionality
