# Generated image production

Generated imagery is a design and production system, not a filler step. Use this route when the website's meaning, hierarchy, brand world, campaign identity, or motion language depends on custom visual assets.

This module is provider-neutral. It can guide work executed through an integrated image tool, an external service, a local model, a human designer, or a mixed pipeline.

## Decide whether generation is appropriate

Prefer owner-supplied, commissioned, licensed, archival, product, documentary, or interface evidence when authenticity matters more than invention.

Generated imagery is appropriate when it:

- visualises an original brand world or abstract service;
- creates a campaign motif not available from existing assets;
- supplies art-directed backgrounds, objects, textures, or illustrations;
- extends an approved identity into responsive variants;
- creates a controlled still master for later motion;
- avoids misleading documentary claims.

Do not use generated imagery to fake customers, staff, facilities, products, results, endorsements, news events, or evidence. Label synthetic media when context or policy requires it.

## Build an image-needs map

Map visual needs before prompting. For each asset record:

- asset ID and surface;
- user-facing purpose;
- semantic role: informative, identity-bearing, atmosphere, navigational, instructional, decorative, evidence, or social preview;
- subject and protected details;
- relationship to headline, body copy, controls, and navigation;
- focal point and safe crop region;
- required negative space;
- expected wide, short-laptop, tablet, narrow, 320 CSS-pixel, thumbnail, social, transparent, and reduced-detail variants;
- target master dimensions and format;
- loading priority and performance budget;
- alternative text or decorative treatment;
- source, rights, consent, owner, and approval state;
- whether motion is planned.

Remove assets with no clear job. A coherent site often needs fewer, stronger images rather than one image per section.

## Construct a reference-role stack

References are inputs with bounded responsibilities. They are not permission to clone a finished visual.

### Reference roles

- **Identity** — preserves a real person, product, logo, approved artwork, character, or object.
- **Composition** — informs framing, spatial balance, viewpoint, negative space, or crop behaviour.
- **Form** — supplies a motif, object family, silhouette, geometry, or visual vocabulary.
- **Palette/material** — informs colour relationships, surface finish, transparency, texture, and material response.
- **Lighting** — informs direction, softness, contrast, shadow, exposure, and atmosphere.
- **Environment** — supplies factual location, architecture, landscape, or world-building cues.
- **Motion** — supplies movement, timing, rhythm, camera behaviour, deformation, or transition logic only.
- **Exclusion** — demonstrates qualities that must not appear.
- **Other** — a precisely named contribution that does not fit the roles above.

### Reference contract

For every reference state:

- identifier and source;
- role;
- exact contribution;
- what must be ignored;
- rights or permission status;
- whether it may be stored, transformed, or published;
- whether it contains protected identity or confidential material.

Never use vague directions such as “make it like Image 1.” Write “Image 1 controls the asymmetrical framing and empty right third; ignore its subject, typography, colour, and branding.”

### Separate mechanisms from expressions

Extract reusable mechanisms such as:

- large motif anchoring opposing corners;
- subject placed outside the centre to protect a headline zone;
- restrained palette with one luminous material accent;
- shallow depth and edge lighting to separate form from background;
- visual object crossing a frame boundary to imply scale;
- still composition designed to support a later reveal.

Translate those mechanisms into the project's own content, motif, palette, proportions, and brand logic.

## Declare generation versus edit intent

Do not let the presence of a reference image blur the production intent.

- **Generate** when the output is a new image and supplied images only guide identity, composition, palette, material, lighting, environment, style, or another bounded reference role.
- **Edit** when an existing image is the material source that must remain recognisable while one or more named properties change.

For an edit, the output asset's lineage should name the edited source as a direct parent. For a generation, references remain references rather than parents unless the output is materially derived from them.

When intent is unclear, resolve it before generation. This distinction affects preservation rules, lineage, host capability requirements, and whether downstream derivatives can safely restart from an approved master.

## Plan the production graph

For image families or multi-asset batches, use optional `image_system.production_jobs` in the Experience Contract rather than relying on conversational order.

Each distinct output asset gets one production job with:

- stable job ID and output asset ID;
- intent: generate or edit;
- prerequisite job IDs;
- asset IDs that must be approved before the job may start;
- direct source/edit-target asset IDs;
- bounded reference IDs;
- optional parallel group, prompt path, and intended output reference;
- an asset-specific acceptance gate.

The graph is an execution plan, not a second asset ledger. Actual artifacts, parent/reference lineage, checksums, evidence and approval remain in `asset_lineage`, the asset ledger, and SITECRAFT evidence.

### Dependency rules

- one distinct output asset = one production job;
- multiple candidates for one prompt are exploration variants for that job, not substitutes for separate jobs;
- only independent jobs may run concurrently;
- dependent jobs wait until their declared prerequisites and required approved inputs pass;
- an edit starts from its declared source, not from whichever sibling was generated most recently;
- when several sibling derivatives must preserve one base master, every sibling restarts from that approved parent unless the Experience Contract explicitly defines a different lineage;
- never advance downstream work because a source is merely promising; advance only when its required approval gate passes.

This is especially important for relighting, weather, crop, responsive, material, campaign-state, and motion-preparation families where cumulative edits can slowly change geometry, identity, camera or composition.

## Use a still-first production sequence

The default route is:

1. image-needs map;
2. asset brief;
3. reference-role stack;
4. generation specification;
5. low-cost exploration or contact sheet;
6. candidate selection;
7. full-quality still master;
8. surgical repairs;
9. owner approval and lineage receipt;
10. responsive derivatives;
11. motion handoff, if required;
12. website integration;
13. rendered evidence and final review.

Do not start motion generation before the still master is approved. Otherwise image and movement problems become entangled and each regeneration can change both.

## Write the generation specification

Use short labelled blocks that can be understood by different tools.

### Use

State the exact website role and desired visitor effect. Example: “Homepage hero for a small architecture studio; establish precision and calm while leaving a clean left-side headline zone.”

### Subject

Describe the required content, protected identity, scale, pose, orientation, state, and relationships.

### Reference roles

List each reference by index or identifier, its contribution, and what to ignore.

### Composition

Specify:

- aspect ratio and intended master size;
- camera or viewpoint;
- subject placement;
- foreground, middle ground, and background;
- focal hierarchy;
- negative-space zone;
- crop-safe region;
- depth and overlap;
- whether objects may cross the frame.

### Visual treatment

Specify only meaningful qualities:

- photographic, illustrated, 3D, collage, diagrammatic, typographic, painterly, vector-like, or mixed medium;
- lighting and exposure;
- colour roles;
- materials and texture;
- realism and imperfection level;
- grain, blur, atmosphere, and edge treatment;
- relationship to the site's visual grammar.

### Preserve

List invariants such as identity, facial geometry, product proportions, logo, approved text, composition, camera, background, colour balance, or unrelated details.

### Exclude

List unwanted content and common failure modes: extra objects, duplicated elements, text, watermarks, trademarks, generic gradients, yellow cast, plastic skin, impossible reflections, broken hands, random interface elements, or style drift.

### Output

Define master format, dimensions, transparency, quality route, colour profile, derivative intent, and whether a text-free version is required.

## Re-discover image-production capability on the current host

Do not assume that a host can execute an image job merely because it can read project files or display images.

Before a consequential image batch, confirm whether the current host can:

- generate a new raster image;
- edit an existing raster image while preserving named invariants;
- make every required local, attached, connected, or returned reference actually visible to the image generator;
- inspect the returned full-resolution artifact;
- save or import an accepted project-bound image into the project workspace;
- preserve source files and avoid destructive overwrite;
- pass the candidate onward to the browser/composition review required by SITECRAFT.

A filesystem path by itself is not proof that the image model can see the image. Some hosts require an explicit load, attachment, upload, import, or media-context step. Others may support direct file inputs. Discover the actual mechanism instead of naming a path in a prompt and hoping the generator can access it.

If the host cannot satisfy the current job's reference or edit requirements, do not weaken the asset contract. Produce or refresh the portable Image Generation Pack and hand the job to a capable image-production host. Permissions, credentials and host-specific tool access do not transfer through the pack.

## Gate execution-context isolation

Prompt quality and execution-context isolation are separate requirements.

Before executing a bounded production job, determine what context the image generator will actually receive. The safe default for a production asset is:

- the current job's generation/edit specification;
- only the references declared for that job;
- unavoidable host safety/policy instructions;
- no unrelated website discussion, workflow explanation, prior rejected images, UI screenshots, planning notes, or other project context unless the job explicitly declares them as inputs.

Classify the route as one of:

- **isolated request** — the execution mechanism accepts an explicit prompt plus explicit image/file inputs for this one job;
- **fresh bounded context** — the host is conversation-oriented, but the job runs in a new image-only context containing only the pack and declared references;
- **mixed conversation context** — the generator may infer intent from a long or multi-purpose conversation;
- **unknown** — the host does not make the execution boundary clear.

For consequential or reference-dependent production work, `mixed conversation context` and `unknown` fail the preflight unless the host provides a narrower subtask/context mechanism that can be verified before execution.

When paid API execution is unavailable or inappropriate, a fresh bounded image-only conversation is a first-class production route, not a degraded fallback. On ChatGPT specifically, prefer Temporary Chat when available because it does not use or create memory and cannot inherit Project conversation history. Keep that temporary chat outside the website Project, attach only the exact job packet and declared reference image(s), generate or edit one asset job there, then return the candidate to the director/build context for persistence and real-site review. Account-level custom instructions may still apply, so the packet must remain explicit about the one image job and hard exclusions.

Do not require API spend merely to satisfy context isolation. Paid isolated requests, fresh bounded subscription chats, host-native image workers covered by an existing plan or usage allowance, capable local models, and human production are all valid execution routes when they meet the same job/reference/evidence contract. A host-native worker is especially useful when it can accept the bounded job prompt plus exact local reference files while charging against an existing host allowance rather than a separate image API bill. Treat that as an execution route, not as a reason to weaken the production graph, lineage, approval, or website-review gates.

A clean-looking reference displayed inside browser chrome, a design review page, a workflow diagram, or other explanatory UI is not equivalent to supplying the original reference image as a bounded input. If the output unexpectedly contains concepts, text, layout, or objects from surrounding workflow discussion rather than the declared job, record **context contamination**, reject the candidate, and change the execution route. Do not respond by making the prompt longer and retrying the same contaminated path.

This gate is provider-neutral. A direct image endpoint, a host-native isolated image task, a fresh image-only conversation, a local model process, or a human production handoff may all satisfy it if only the declared job context reaches the maker.

## Choose the production route by capability

Do not hard-code one permanently “best” model. Compare the current available tools against the asset's requirements.

### Capability classes

- **Instruction and edit fidelity** — compositing, multiple references, identity-sensitive edits, precise layout, controlled replacement, or text-bearing assets.
- **Atmospheric image-making** — cinematic, editorial, expressive, or mood-led key art where interpretive visual quality matters most.
- **Text and poster accuracy** — short, prominent text embedded in a graphic asset.
- **Graphic and vector-system output** — illustrations, icons, marks, flat assets, or consistent visual systems.
- **Open or local generation** — privacy, cost control, offline work, model customisation, or self-hosting.
- **Enterprise-approved generation** — procurement, rights policy, indemnity, audit, or creative-suite integration.
- **Human-led production** — photography, illustration, 3D, retouching, or art direction when authenticity, originality, or control exceeds model capability.

### Selection record

Record:

- selected provider, tool, or human route;
- model or version when known;
- why it fits the asset;
- settings and quality level;
- expected weaknesses;
- fallback route;
- privacy and rights conditions;
- cost or iteration constraints when relevant.

Recommendations must be framed as current, contextual choices rather than timeless rankings.

## Explore without losing direction

Use inexpensive or faster settings for broad composition exploration when available. Keep exploration bounded:

- vary one major dimension at a time;
- label candidates;
- record what works and fails;
- select one direction before high-quality generation;
- do not combine incompatible directions into a confused final prompt.

A contact sheet should answer a design question, not merely provide many attractive options.

For multiple deliverables, keep **asset jobs** separate from **variants of one job**. A generator's multi-output or `n`-style control may be useful for several candidates of one prompt, but distinct assets with different roles, sources, ratios, or acceptance gates remain distinct production jobs. Parallelize only jobs that are truly independent in the Experience Contract; do not trade dependency discipline for speed.

## Repair with surgical edits

For each edit:

1. name the defect;
2. state the single intended change;
3. repeat protected invariants;
4. prohibit unrelated changes;
5. compare against the approved previous state;
6. reject silent drift.

Use “change only” language when supported. Preserve a text-free master and an editable source when typography or overlays may need repair.

## Produce responsive derivatives deliberately

Do not assume one hero image can be centre-cropped everywhere.

For each derivative define:

- target surface and ratio;
- focal subject;
- crop-safe boundaries;
- negative-space requirement;
- permitted recomposition;
- detail reduction;
- text relationship;
- output width and format;
- `object-fit` and `object-position` guidance;
- intrinsic width and height;
- quality and compression target.

Use art direction when a narrow screen requires a different composition. Use `<picture>` and media-specific sources when the visual story changes, not merely to send smaller bytes.

## Create the Image Generation Pack

When the current host cannot execute the image work, or when a multi-job image family needs durable continuation outside the current conversation, use [image-generation-pack.md](../assets/image-generation-pack.md).

The pack references the Experience Contract rather than becoming a second contract. It should carry the current production graph and one execution-ready block per job.

### Required contents

1. Project and Experience Contract identity/revision.
2. Host preflight for generation, edit, reference loading, result inspection and project persistence.
3. Production graph: job IDs, output asset IDs, intent, dependencies, required approved inputs, edit sources, references and parallel groups.
4. Asset ID, surface, purpose, semantic role and user-facing goal for each job.
5. Recommended capability class and suitable route options, with honest limitations.
6. Main generation or edit instruction.
7. Reference-role table.
8. Preserve list.
9. Exclusion and rejection list.
10. Master dimensions and format.
11. Responsive derivative specifications.
12. Focal point and placement guidance.
13. Alt-text direction or decorative rule.
14. Rights and consent checklist.
15. Acceptance gate and failure decision.
16. Project-bound naming/persistence rule.
17. Motion handoff, if required.

The pack should remain usable outside the original chat or tool. It carries context, not credentials or permission. The receiving host must re-discover its own image-generation and file/media capabilities before executing the next job.

## Hand off a still master to motion

Motion is a separate contract.

### Motion handoff must name

- approved still-master ID and checksum or version;
- protected geometry, identity, palette, and framing;
- intended movement and narrative purpose;
- movement source: object, camera, light, texture, type, or transition;
- timing, holds, entry, action, settle, and loop behaviour;
- prohibited camera or object movement;
- responsive transformation;
- reduced-motion or static equivalent;
- target runtime and format;
- poster frame and stable end state;
- evidence required.

A motion reference controls only the named movement qualities. It must not silently replace the still's subject, style, palette, logo, or composition.

Prefer motion that can preserve the master reliably. When generative video introduces unacceptable identity or geometry drift, use controlled compositing, masks, SVG, Rive, Lottie, CSS, canvas, or manual animation instead.

## Integrate assets into the website

For raster assets:

- persist every accepted project-bound candidate into the project workspace before site code depends on it;
- use stable semantic filenames and avoid silently overwriting an approved master;
- keep rejected or exploratory variants out of public delivery unless the project explicitly retains them;
- define master and derivative widths;
- use modern formats with fallbacks where required;
- declare intrinsic dimensions or aspect ratio;
- do not lazy-load the actual LCP image;
- use appropriate fetch priority;
- lazy-load offscreen media;
- avoid shipping oversized masters;
- preserve colour profile and transparency behaviour;
- remove private metadata and temporary filenames, host-generation paths, prompt fragments, and review-only source material.

For animated media:

- provide poster and fallback;
- obey autoplay, mute, control, pause, and data-saving rules;
- stop offscreen decorative playback;
- avoid perpetual high-energy rendering;
- provide reduced-motion/static equivalents;
- test decode, frame pacing, input responsiveness, and battery impact when relevant.

## Observe in the real composition

Review the asset in context, not only in an image viewer.

### Visual checks

- identity and subject integrity;
- anatomy, geometry, reflections, shadows, text, and logo accuracy;
- focal point at every crop;
- headline and control legibility;
- relationship to surrounding content;
- visual consistency across the asset family;
- thumbnail and social-preview readability;
- undesirable AI artefacts or generic grading.

### Responsive checks

- wide desktop;
- short laptop;
- tablet when supported;
- narrow mobile;
- 320 CSS-pixel reflow;
- high zoom or large text where relevant;
- social preview and share card;
- reduced-motion/static state when motion exists.

### Technical checks

- dimensions, formats, weights, and metadata;
- `srcset`, `sizes`, `<picture>`, and crop selection;
- LCP, CLS, decode, and bandwidth behaviour;
- no private prompt, path, or source leakage;
- rights, consent, attribution, and approval receipts.

## Failure vetoes

Block approval when:

- the asset has no defined website role;
- references are used without bounded roles or rights status;
- the result materially copies a protected expression;
- identity, product, logo, or approved artwork drifts;
- narrow crops destroy the focal story;
- text or controls become unreadable;
- the still is animated before approval;
- motion changes protected geometry without permission;
- asset lineage is missing;
- LCP or layout stability is harmed without an accepted trade-off;
- synthetic media misrepresents evidence or reality;
- required rendered evidence or owner approval is absent.

Use [asset-and-media-pipeline.md](asset-and-media-pipeline.md) for the broader asset ledger, delivery, rights, and media rules, and [motion-design-and-graphics.md](motion-design-and-graphics.md) for full temporal production.