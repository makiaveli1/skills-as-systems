# Research basis

Use current official sources when standards, browser support, framework behaviour, AI-builder features, or platform rules may have changed. This file records the initial evidence base for SITECRAFT v0.1.0. Verify again when exact current behaviour matters.

Accessed: 2026-08-04.

## Accessibility

### WCAG 2.2

Source: W3C Web Content Accessibility Guidelines 2.2
https://www.w3.org/TR/WCAG22/

Applied rules:

- use WCAG 2.2 Level AA as the default public-web target;
- include focus not obscured, dragging alternatives, target size, accessible authentication, and reflow in review;
- do not treat automated testing as full conformance.

### Reflow

Source: W3C Understanding Success Criterion 1.4.10: Reflow
https://www.w3.org/WAI/WCAG22/Understanding/reflow.html

Applied rules:

- verify non-exempt vertical content at 320 CSS pixels without two-dimensional scrolling;
- test zoom and split-view behaviour, not only phone presets;
- review fixed and sticky content for focus obstruction.

### Reduced motion

Source: W3C Technique C39: Using `prefers-reduced-motion`
https://www.w3.org/WAI/WCAG22/Techniques/css/C39

Applied rules:

- suppress non-essential interaction-triggered motion for users requesting reduced motion;
- test the real system preference;
- design an equivalent state rather than deleting orientation and feedback.

## Responsive design

### Container queries

Sources:

- web.dev: Container queries
  https://web.dev/learn/css/container-queries/
- web.dev: Container queries and units in action
  https://web.dev/articles/baseline-in-action-container-queries

Applied rules:

- use viewport queries for macro composition and container queries for component context;
- retain `rem` influence in fluid typography so user zoom and font settings remain meaningful;
- design components to adapt to unexpected containers.

## Motion

### View Transition API

Sources:

- MDN: View Transition API
  https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API
- Chrome for Developers: Smooth transitions with the View Transition API
  https://developer.chrome.com/docs/web-platform/view-transitions

Applied rules:

- use view transitions for orientation and continuity where architecture and support permit;
- feature-detect and preserve the DOM update as a fallback;
- support same-document and same-origin cross-document routes where appropriate;
- verify focus, browser history, slow navigation, aspect ratio, and reduced motion.

### Web Animations API

Sources:

- MDN: Web Animations API
  https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API
- MDN: Using the Web Animations API
  https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API/Using_the_Web_Animations_API

Applied rules:

- use the browser animation engine when JavaScript needs playback control;
- use CSS for simpler declarative effects;
- avoid importing a large animation library when native APIs are sufficient.

## Performance

### Core Web Vitals

Sources:

- web.dev: Web Vitals
  https://web.dev/articles/vitals
- web.dev: The most effective ways to improve Core Web Vitals
  https://web.dev/articles/top-cwv

Applied rules:

- target LCP <= 2.5s, INP <= 200ms, and CLS <= 0.1 at the 75th percentile;
- distinguish field and lab evidence;
- make LCP resources discoverable and prioritised;
- reserve space for media and async content;
- prefer transform and opacity over layout-inducing animation;
- avoid unnecessary JavaScript and long main-thread tasks.

## Visual testing

### Playwright visual comparisons

Source: Playwright: Visual comparisons
https://playwright.dev/docs/test-snapshots

Applied rules:

- use `toHaveScreenshot()` or an equivalent controlled visual baseline for stable critical states;
- keep baseline and comparison environments consistent;
- review baseline changes rather than updating them to silence failures;
- stabilise nondeterministic content when it is not under test.

## AI builders

### Vercel v0 prompting

Source: Vercel: How to prompt v0
https://vercel.com/blog/how-to-prompt-v0

Applied rules:

- define product surface, context of use, and constraints/taste;
- specify real components, data, and actions instead of vague product categories;
- use prompt changes for structure and logic and visual editing for small presentation changes where available.

### Lovable

Sources:

- Prompting best practices
  https://docs.lovable.dev/prompting/prompting-one
- From idea to working app
  https://docs.lovable.dev/tips-tricks/from-idea-to-app
- Browser testing
  https://docs.lovable.dev/features/browser-testing

Applied rules:

- plan before building;
- use real content;
- build modular components rather than entire products in one pass;
- separate a large change from the browser-testing prompt.

### Bolt

Sources:

- Prompt effectively
  https://support.bolt.new/best-practices/prompting-effectively
- Maximize token efficiency
  https://support.bolt.new/best-practices/maximizing-token-efficiency

Applied rules:

- create a clear blueprint before the first prompt;
- build incrementally;
- add one feature or bounded change at a time;
- keep project knowledge current and restate relevant context.

### Replit Agent

Sources:

- Build with Agent
  https://docs.replit.com/learn/build-with-agent
- Plan vs Build Mode
  https://docs.replit.com/learn/plan-vs-build-mode

Applied rules:

- use planning and building as a sequence;
- define success, context, and constraints;
- review, test, and use checkpoints for recovery.

## Security and public/private separation

### OWASP Web Security Testing Guide

Sources:

- OWASP WSTG
  https://owasp.org/www-project-web-security-testing-guide/
- Review Web Page Content for Information Leakage
  https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/05-Review_Web_Page_Content_for_Information_Leakage

Applied rules:

- inspect client JavaScript, comments, metadata, source maps, debug files, endpoints, and configuration for information leakage;
- test security throughout definition, development, deployment, and maintenance;
- treat browser-delivered material as inspectable.

### Next.js environment variables

Source: Next.js: Environment Variables
https://nextjs.org/docs/pages/guides/environment-variables

Applied rules:

- variables prefixed `NEXT_PUBLIC_` are inlined into browser JavaScript at build time;
- `.env` secrets should not be committed;
- keep privileged values server-side and use runtime server access when needed.

### Subresource Integrity

Source: MDN: Subresource Integrity
https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Subresource_Integrity

Applied rules:

- use integrity hashes for eligible third-party scripts and styles;
- pair SRI with appropriate CORS and policy deployment;
- use report-only policy rollout when introducing broad integrity requirements.

## Maintenance rule

Record factual browser or platform claims with a source date. When the user asks for latest support, pricing, API, model, deployment, or legal behaviour, browse official sources again instead of relying on this snapshot.

## Content, search, and internationalisation

### Google Search Essentials

Sources:

- Google Search Essentials
  https://developers.google.com/search/docs/essentials
- Developer guide to Search
  https://developers.google.com/search/docs/fundamentals/get-started-developers

Applied rules:

- create helpful, reliable, people-first public content;
- use descriptive titles, headings, links, alt text, and crawlable URLs;
- ensure public pages return usable indexable content and are not unintentionally blocked;
- do not promise indexing or rankings;
- align images, video, JavaScript, and structured data with their current guidance.

### Internationalisation

Sources:

- W3C: Language on the Web
  https://www.w3.org/International/getting-started/language
- W3C Internationalization Quick Tips
  https://www.w3.org/International/quicktips/index
- W3C: Declaring language in HTML
  https://www.w3.org/International/questions/qa-html-language-declarations.html

Applied rules:

- internationalise early rather than treating translation as a final content pass;
- use UTF-8, document and in-page language metadata, bidirectional direction, logical CSS properties, and locale-aware formats;
- design components, forms, navigation, fonts, and media for different languages, scripts, cultural formats, and text expansion.

### Metadata and structured data

Sources:

- MDN: Web page metadata
  https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Webpage_metadata
- Schema.org
  https://schema.org/
- Schema.org Validator
  https://schema.org/docs/validator.html

Applied rules:

- define route-specific title, description, canonical URL, social-preview data, language, indexing intent, and structured-data source;
- use absolute social image URLs;
- keep structured data truthful and consistent with visible content;
- validate generated structured-data graphs.

## Design tokens

Sources:

- Design Tokens Community Group: first stable specification announcement
  https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/
- Design Tokens Format Module 2025.10
  https://www.designtokens.org/tr/2025.10/format/

Applied rules:

- for systems that need cross-tool or cross-platform token exchange, prefer the stable vendor-neutral DTCG 2025.10 format where compatible;
- keep token roles human-readable and typed;
- use aliases, groups, themes, and extensions deliberately;
- record that the specification is a Community Group report rather than a W3C Recommendation, and recheck later versions before migration.

## Images and media delivery

Sources:

- MDN: `<img>`
  https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/img
- MDN: Responsive images
  https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images
- MDN: Images guide
  https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Images

Applied rules:

- declare intrinsic image dimensions to reduce layout shift;
- use `srcset`, `sizes`, and `<picture>` for responsive delivery and art direction;
- lazy-load suitable offscreen images while keeping the likely LCP asset eagerly discoverable and prioritised;
- generate only the responsive variants the composition needs rather than shipping oversized masters.

## Generated image production and reference-role synthesis

Research refreshed: 2026-08-05.

Sources:

- user-supplied animated website-building tutorial, studied as an observational workflow rather than a design authority;
- supplied GPT image-generation prompting guide covering structured prompts, multi-image roles, composition, preservation constraints, iterative edits, text, and production settings;
- the responsive-image and media-delivery sources above.

Applied rules:

- map the website purpose of every important image before generation;
- assign each input reference one bounded role and state what must be ignored;
- identify references by index or identifier when multiple images are supplied;
- separate composition, form, palette/material, identity, lighting, environment, motion, and exclusion inputs;
- generate and approve a still master before motion so visual and temporal defects do not become entangled;
- use short labelled prompt sections and small single-purpose repair passes rather than overloaded regeneration;
- repeat protected invariants on every edit;
- provide a portable Image Generation Pack when generation tools are unavailable;
- treat provider recommendations as current capability matches, not permanent rankings;
- verify generated assets inside real responsive compositions and record lineage, rights, accessibility, performance, and approval.

SITECRAFT's reference-role vocabulary, `image_system` contract, Image Generation Pack, still-to-motion handoff, and release vetoes are an original synthesis built from these principles. They do not reproduce the tutorial's artwork, prompts, provider choices, or protected expression.

## Motion design and motion graphics expansion

Research refreshed: 2026-08-04.

### Purpose, hierarchy, and choreography

Sources:

- Apple Human Interface Guidelines: Motion
  https://developer.apple.com/design/human-interface-guidelines/motion
- IBM Carbon Design System: Motion overview
  https://carbondesignsystem.com/elements/motion/overview/
- IBM Carbon Design System: Motion choreography
  https://carbondesignsystem.com/elements/motion/choreography/
- Microsoft Fluent 2: Motion
  https://fluent2.microsoft.design/motion

Applied rules:

- motion must support feedback, orientation, continuity, hierarchy, progress, meaning, or a deliberate emotional moment;
- distinguish frequent productive motion from rare expressive motion;
- derive motion opportunities from product purpose, information hierarchy, and user journey before choosing effects;
- use consistent duration, easing, path, sequence, and spatial relationships;
- let people interrupt motion and avoid making routine actions wait for expressive animation;
- keep the stable end state focused on the important content;
- constrain motion to the focal task and avoid unrelated movement elsewhere on the screen.

### Motion sensitivity, flashing, and reduced motion

Sources:

- W3C Understanding WCAG 2.2 Success Criterion 2.3.3: Animation from Interactions
  https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions
- W3C Understanding WCAG 2.2 Success Criterion 2.2.2: Pause, Stop, Hide
  https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html
- W3C Understanding WCAG 2.2 Success Criterion 2.3.1: Three Flashes or Below Threshold
  https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold
- W3C WCAG 2.2
  https://www.w3.org/TR/WCAG22/
- Apple Human Interface Guidelines: Accessibility
  https://developer.apple.com/design/human-interface-guidelines/accessibility
- Microsoft Fluent 2: Accessible motion design
  https://fluent2.microsoft.design/motion

Applied rules:

- non-essential interaction-triggered motion must be suppressible through user preference or an explicit control when needed;
- avoid parallax, large spatial travel, zoom, depth changes, repetitive peripheral motion, rapid flashes, and jarring movement;
- provide a static, semantic, captioned, or otherwise equivalent communication path;
- test the actual system reduced-motion setting;
- keep focus, status announcements, reading order, and controls functional when motion is removed;
- do not assume a fade or blur is harmless without reviewing the full composition.

### Web platform implementation and performance

Sources:

- Chrome for Developers: Smooth transitions with the View Transition API
  https://developer.chrome.com/docs/web-platform/view-transitions
- Chrome for Developers: Same-document view transitions
  https://developer.chrome.com/docs/web-platform/view-transitions/same-document
- Chrome for Developers: Cross-document view transitions
  https://developer.chrome.com/docs/web-platform/view-transitions/cross-document
- web.dev: Animations and performance
  https://web.dev/articles/animations-and-performance
- web.dev: How to create high-performance CSS animations
  https://web.dev/articles/animations-guide
- MDN: Web Animations API
  https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API

Applied rules:

- treat view transitions as progressive enhancement around a DOM or navigation change;
- preserve fallback behaviour, focus, browser history, aspect ratio, and unique transition identity;
- use CSS for simple declarative state changes and Web Animations when playback control, sequencing, cancellation, or inspection is needed;
- prefer transform and opacity for frequent interface motion, while measuring the real rendering path;
- avoid unnecessary layout and paint work, excessive permanent `will-change`, and uncontrolled frame callbacks;
- record browser support and runtime versions when advanced APIs affect the contract.

### Motion-graphics authoring and reusable templates

Sources:

- Adobe After Effects: Work with Motion Graphics templates
  https://helpx.adobe.com/after-effects/using/creating-motion-graphics-templates.html
- Adobe After Effects: Animating text
  https://helpx.adobe.com/after-effects/using/animating-text.html
- Adobe After Effects: Setting, selecting, and deleting keyframes
  https://helpx.adobe.com/after-effects/using/setting-selecting-deleting-keyframes.html
- Adobe After Effects: Editing keyframes and Graph Editor
  https://helpx.adobe.com/after-effects/desktop/animate-in-after-effects/animation-keyframes/editing-moving-copying-keyframes.html
- Adobe After Effects: Compositing and transparency
  https://helpx.adobe.com/after-effects/desktop/work-with-transparency-and-compositing/compositing-in-after-effects/compositing-transparency-overview-resources.html
- Adobe After Effects: Alpha channels, masks, and mattes
  https://helpx.adobe.com/after-effects/using/alpha-channels-masks-mattes.html

Applied rules:

- separate storyboard, style-frame, animatic, editable source, and delivery master;
- expose only deliberate template controls so downstream editors can customise content without silently breaking the visual system;
- record keyframes, interpolation, easing, typography selectors, motion blur, masks, mattes, alpha, blending, and colour assumptions;
- preserve typography readability and resolution independence where possible;
- review transparent edges and premultiplication on every intended background;
- retain source lineage and do not treat a rendered preview as the editable master.

### Interactive vector runtimes

Sources:

- Rive: State Machine overview
  https://rive.app/docs/editor/state-machine/state-machine
- Rive Web runtime: State Machine playback
  https://rive.app/docs/runtimes/web/state-machines
- Rive Web runtime parameters and performance marks
  https://rive.app/docs/runtimes/web/rive-parameters

Applied rules:

- use Rive when interactive state machines, data-bound transitions, reusable artboards, or designer-owned runtime behaviour justify the WASM and rendering cost;
- define states, inputs, transitions, settled behaviour, loading, pause, stop, and fallback explicitly;
- stop advancing when settled or offscreen;
- profile runtime loading, parsing, first frames, and active playback;
- do not embed essential text or controls only inside the rendered artboard.

### Lottie and dotLottie

Sources:

- LottieFiles: Supported Lottie features
  https://lottiefiles.com/supported-features
- LottieFiles: Why use Lottie and the distinction between Lottie JSON and dotLottie
  https://lottiefiles.com/blog/working-with-lottie-animations/why-use-lottie
- LottieFiles: How to optimise Lottie for production
  https://lottiefiles.com/blog/optimize/how-to-optimize-lottie-for-production
- LottieFiles: Lottie Accessibility Analyzer
  https://help.lottiefiles.com/hc/en-us/articles/43259873084569-lottie-accessibility-analyzer
- LottieFiles: dotLottie Web GPU rendering update
  https://lottiefiles.com/blog/working-with-lottie-animations/hardware-accelerated-lottie-on-the-web-dotlottie-web-now-ships-webgl-webgpu

Applied rules:

- record the exact format, player, renderer, and supported feature set rather than saying only “Lottie”;
- verify masks, gradients, effects, fonts, raster assets, themes, state machines, and cross-platform rendering;
- remove redundant keyframes and optimise payloads before production;
- pause offscreen animation and supply static or reduced-motion alternatives;
- profile CPU, GPU, memory, WASM, and input responsiveness for the chosen renderer;
- do not assume newer GPU routes are appropriate without current browser and device verification.

### Format-routing rule

Use the lightest route that preserves the intended experience:

- CSS for simple state and decorative motion;
- Web Animations for controlled DOM sequences;
- View Transitions for route or state continuity;
- SVG for scalable line, shape, mask, and icon work;
- Lottie or dotLottie for supported authored vector sequences;
- Rive for interactive vector state machines;
- canvas, WebGL, or WebGPU for dense custom rendering and 3D;
- video for photorealistic, simulated, or heavily composited sequences without internal element interactivity.

The choice remains provisional until accessibility, maintenance, loading, browser support, performance, responsive behaviour, and evidence needs are evaluated in the real project.
