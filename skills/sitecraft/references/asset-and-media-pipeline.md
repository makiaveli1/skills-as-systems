# Asset and media pipeline

Treat generated and sourced media as production assets with roles, rights, variants, and evidence. Do not fill empty layouts with arbitrary AI imagery.

For image-led work, use [generated-image-production-compact.md](generated-image-production-compact.md) for the short route and [generated-image-production.md](generated-image-production.md) for the full reference-role, still-master, derivative, motion-handoff, and evidence workflow.

## Reference-role stack and still-first rule

Before generating, assign every input reference one bounded role: identity, composition, form, palette/material, lighting, environment, motion, exclusion, or another precisely named contribution. State what must be ignored from each reference. This converts references into controlled design inputs rather than an invitation to clone a finished expression.

Lock the still-image master before animation. The default sequence is asset brief → reference-role map → candidate stills → approved still master → responsive derivatives → separate motion handoff → rendered website evidence. Do not ask one overloaded generation to solve concept, responsive art direction, motion, and final integration simultaneously.

## Asset brief

For every important asset define:

- purpose and surface;
- audience and viewing context;
- semantic role;
- subject or content;
- composition and focal point;
- expected crop and negative space;
- aspect ratios and responsive variants;
- lighting, colour, material, and texture;
- relationship to typography and UI;
- accessibility alternative;
- loading priority and performance budget;
- source, rights, consent, and approval;
- what must remain invariant across edits.

The asset should strengthen the visual grammar and user task.

## Source types

Classify assets as:

- owner-supplied and protected;
- commissioned;
- licensed stock or archive;
- official third-party material;
- generated from scratch;
- generated edit or composite;
- interface capture or product evidence;
- decorative system asset;
- temporary placeholder.

Record licence, attribution, model or generator, prompt or edit instruction, input references, creation date, and approval state where applicable.

## Generated-image production graph

For multi-asset or reference-dependent image work, plan the execution order in the optional Experience Contract `image_system.production_jobs` before prompting.

Keep the responsibilities separate:

- `image_system.asset_roles` explains why each image exists in the website;
- `image_system.reference_roles` bounds what each reference may contribute;
- `image_system.production_jobs` records generate/edit intent, prerequisites, required approved inputs, direct edit sources, reference IDs and acceptance gates;
- `asset_lineage` and the detailed asset ledger record what was actually produced, its direct parents/references and current approval state;
- the evidence matrix records whether the resulting artifact worked in the actual site.

Do not duplicate the whole asset ledger inside the production graph. Use stable asset IDs to connect the systems.

A generation job creates a new image from a brief and bounded references. An edit job materially modifies a declared source image while preserving named invariants; its output should name that source as a direct parent. When several derivatives must preserve one master, each sibling should restart from the declared approved parent unless the contract explicitly defines another lineage.

Only independent jobs may be executed concurrently. A downstream job does not become ready merely because a prerequisite artifact exists; any declared approval gate must also pass.

## Generated-image prompting

Write prompts in a maintainable order:

1. asset type and use case;
2. subject;
3. scene or background;
4. composition and viewpoint;
5. lighting and colour;
6. visual medium and texture;
7. exact text and typography only when needed;
8. reference-image roles;
9. preservation rules;
10. exclusions;
11. aspect ratio, size, and output intent.

Use visible facts rather than empty quality words. Specify focal point, framing, placement, and negative space when the website layout depends on them.

For photorealism, request real texture, believable materials, natural light behaviour, and ordinary imperfections. Avoid over-polished “AI campaign” skin, impossible reflections, plastic materials, and generic colour grading.

## Reference images

Assign each reference a bounded role:

- identity;
- pose;
- composition;
- lighting and colour;
- material and styling;
- environment;
- crop or aspect ratio.

State what to ignore. A style reference must not silently replace the subject, clothing, logo, text, or background.

For edits, use:

- change only the named target;
- preserve identity, geometry, camera, layout, text, colour, and unrelated details;
- no extra objects, text, logos, filters, or style drift.

Repeat critical invariants on every iteration.

## Typography in generated media

Prefer adding important website typography in HTML or a design tool. When text must be generated into an image:

- quote the exact text;
- request it once only;
- define placement, hierarchy, font mood, colour, and contrast;
- keep copy short;
- spell difficult names letter by letter;
- use a high-quality setting appropriate to small text;
- inspect at full resolution;
- retain a text-free version for repair.

Do not use text embedded in an image when the content needs to be searchable, selectable, translated, resized, frequently updated, or read by assistive technology.

## Responsive variants

Generate or prepare only variants that the design needs. Common roles:

- wide hero;
- standard landscape;
- portrait or narrow composition;
- social preview;
- thumbnail;
- high-density but bounded source;
- transparent or plain-background extraction when supported;
- reduced-detail mobile asset.

Use art direction when the focal story changes, not merely smaller files. Preserve intrinsic width and height to prevent layout shift.

## Website delivery

For raster images define:

- master format and dimensions;
- derivative formats and widths;
- compression target;
- `srcset` and `sizes` strategy;
- eager versus lazy loading;
- fetch priority for the likely LCP asset;
- width and height or aspect ratio;
- colour profile;
- CDN or local transform route;
- fallback.

Do not lazy-load the actual LCP image. Lazy-load offscreen media when appropriate. Use `<picture>` when art direction or format negotiation is needed.

For video define:

- poster;
- muted/autoplay rules;
- controls;
- captions and transcript;
- codec and fallback;
- preload and loading behaviour;
- reduced-motion or static equivalent;
- mobile and data-saving behaviour;
- loop length and interruption.

When the video itself is AI-generated, also define the reference-role map, provider-selection strategy, paid attempt/spend boundary, hard quality floors, attempt lineage and targeted regeneration rule before generation. Use [generated-video-production.md](generated-video-production.md). A generated master still needs the same web-delivery checks above.

## Motion assets

When an asset moves, add temporal and runtime lineage. Record storyboard, style-frame, animatic, editable source, final master, duration, frame rate, alpha, colour space, audio, trigger, loop, pause, end state, runtime, responsive variants, static fallback, reduced-motion equivalent, and performance evidence.

Choose CSS, Web Animations, View Transitions, SVG, Lottie or dotLottie, Rive, canvas, WebGL, WebGPU, video, or image sequences from the required behaviour and delivery constraints. Do not label an asset only as “animation”; the exact format and runtime affect accessibility, performance, browser support, editability, and ownership.

Use [motion-design-and-graphics.md](motion-design-and-graphics.md) for the full motion brief, temporal grammar, kinetic typography, compositing, playback, and evidence contract.

## Cross-system asset lineage

For consequential assets that cross image, video, motion, delivery or evidence stages, use the optional Experience Contract `asset_lineage` spine. It complements the detailed CSV asset ledger; it does not replace it.

Use one stable `asset_id` whenever several SITECRAFT systems refer to the same production asset. Distinguish relationship types deliberately:

- `parent_asset_ids` — direct derivation. The child is materially made from the parent, such as a crop, edit, animation, transcode, poster extraction or web-delivery derivative.
- `reference_asset_ids` — influence without direct derivation. The referenced asset may control identity, continuity, lighting, composition or another role, but the new asset is a separate branch.
- `external_source_refs` — supplied references or source authorities that are not themselves tracked as internal SITECRAFT asset IDs.

Do not call a continuity reference a parent merely because it influenced generation. Do not reuse one ID for a master and its compressed delivery derivative when they can have different approval, payload or evidence states.

When `asset_lineage.ledger_path` is declared, consequential lineage records should also exist in that ledger. Keep the core lineage columns even when a project adds useful project-specific fields: `asset_id`, `lineage_stage`, `parent_asset_ids`, `reference_asset_ids`, `capability_decision_ids`, `evidence_ids`, and `approval_state`. Use semicolons inside CSV fields when several stable IDs are listed.

Evidence that proves a specific asset should carry that stable ID in the evidence matrix `asset_ids` field. This lets a reviewer distinguish proof for a source master, generated master, fallback, responsive derivative, or delivered web asset instead of attaching all evidence to a vague family name.

Use the traceability-bundle validator when the Experience Contract, asset ledger and evidence matrix are all available. It should catch broken parent/reference links, approval drift, unknown capability/evidence IDs, evidence pointing to unknown lineage assets, and current evidence rows recorded against the wrong Experience Contract revision.

## Asset QA

Review:

- identity and subject integrity;
- hands, faces, anatomy, geometry, reflections, shadows, and perspective;
- text and logo accuracy;
- focal point at every crop;
- colour consistency with the site;
- thumbnail readability;
- full-resolution artefacts;
- accessibility purpose and alt text;
- rights, consent, and attribution;
- file dimensions, weight, format, and metadata;
- whether private prompts, filenames, or source data are embedded or shipped.

A generated asset is not approved because it is attractive. It must work in the actual composition and state.

## Asset ledger

Maintain an asset ledger with:

- asset ID and filename;
- role and routes;
- source and rights;
- lineage stage plus direct parent and reference asset IDs where applicable;
- master and derivatives;
- intrinsic dimensions;
- focal point and crop rules;
- prompt or edit lineage;
- related Capability Plan decision IDs and evidence IDs where consequential;
- approval state;
- performance treatment;
- alt-text status;
- owner;
- replacement and expiry notes.
