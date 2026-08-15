# Character Identity Board — GPT Image 2

Use this workflow when a character, artist avatar, mascot, product-persona, or recurring human figure must remain visually consistent across later images, covers, storyboards, website scenes, or video generation.

This is an identity-control artifact, not a decorative character sheet.

## Default model and output

- Prefer `gpt-image-2` for new production work.
- Target a true 2:1 landscape identity board. When the current host/model supports custom 2:1 output, use it directly; otherwise generate the strongest supported landscape canvas and crop/extend/pad to an exact 2:1 deliverable without changing the approved identity.
- Use the host/model equivalent of high quality for final identity boards and a cheaper/faster draft mode for exploratory passes when available.
- Treat reference fidelity, exact output size, and other execution parameters as discovered host/model capabilities rather than universal prompt settings. Do not hard-code an API parameter that the current execution surface has not confirmed.
- Use one identity/style reference as the dominant anchor unless the task explicitly calls for separate identity and style references.

## Reference Look Lock

Before generating the board, extract a strict observable identity lock from Image A:

- face shape and facial proportions
- skin tone and visible complexion traits
- eye shape, brows, nose, lips, jaw, ears
- hair silhouette, texture, length, parting, hairline
- body proportions, height impression, shoulder/torso/limb ratios
- outfit pieces, fit, material, trim, accessories, footwear
- palette and material colors
- rendering medium, line quality, shading, texture, grain
- lighting logic and background treatment
- distinctive asymmetries, marks, jewelry, or design details

Only perspective-dependent visibility may change. Do not invent, relocate, duplicate, remove, or redesign identity-defining details unless the requested edit explicitly requires it.

## Copy-paste master prompt

```text
Create a 2:1 premium cinematic CHARACTER IDENTITY BOARD using Image A as the sole character and style reference.

REFERENCE LOOK LOCK
First analyze Image A and establish a strict visual identity lock from all observable character traits, proportions, design details, outfit details, colors, materials, rendering medium, linework, shading, texture, lighting, and background treatment. Apply this locked identity consistently across every angle, pose, and expression. Do not redesign or reinterpret the character. Correct only obvious generation/anatomy errors while preserving the intended design. Nothing may drift, relocate, disappear, duplicate, or be invented; only perspective-dependent visibility may change.

COMPOSITION
Use a clean minimal background color chosen to contrast clearly and elegantly with the character palette. Avoid grids, blueprints, labels, and standard turnaround-sheet styling. Never overlap or crop the studies.

RIGHT 25% — HERO PORTRAIT
The rightmost 25% is one full-height, edge-to-edge close-up portrait completely filling that area with no margins or empty space. Match Image A's identity, art style, lighting, colors, and background treatment. Keep the face and defining head silhouette sharply readable. Place no text or other studies over it.

LEFT 10% — EXPRESSIONS
Reserve the leftmost 10% for exactly four clearly separated expression portraits arranged vertically. Make every emotion and head direction distinctly different:
1. front-facing
2. left three-quarter
3. right three-quarter
4. side profile
The gaze follows the head angle naturally. Preserve the exact same facial identity, proportions, features, hairstyle, and art style in all four.

CENTER 65% — BODY STUDIES
Use the central 65% for exactly five fully visible, clearly separated body studies:
1. one large off-center hero full-body pose facing directly toward the viewer, head straight, eyes visible, face sharp and unobstructed
2. one back full-body view in a different pose
3. one side full-body view in a different pose
4. one top-down body angle
5. one low-angle body angle
Keep every view anatomically coherent and consistent with the locked identity.

REQUEST-SPECIFIC EDITS
Apply only these requested removals/additions if supplied: [INSERT REQUEST-SPECIFIC CHANGES]. Do not generalize a one-off removal into the permanent identity.

HARD CONSTRAINTS
No text, arrows, labels, notes, annotations, silhouettes, detail callouts, seated poses, leaning poses, crouching poses, environments, extra characters, alternate costumes, logos, watermarks, duplicated details, obscured faces, overlapping figures, cropped studies, malformed anatomy, extra fingers/limbs, inconsistent features, or style drift.
```

## Acceptance test

Reject and regenerate/repair the board if any of these fail:

1. Canvas is 2:1.
2. One and only one identity/style anchor controls the board unless references were explicitly role-split.
3. Rightmost 25% is an edge-to-edge hero portrait with no overlaid study/text.
4. Leftmost 10% contains exactly four expression portraits, one per required head direction.
5. Center contains exactly five body studies with the required front/back/side/top-down/low-angle coverage.
6. Every study is fully visible, separated, and uncropped.
7. Face, hair, body proportions, outfit, palette, materials, and rendering style stay consistent.
8. No alternate costume, unexplained prop, logo, text, or extra character appears.
9. Hands and anatomy are plausible enough to serve as downstream references.
10. The front hero body and hero portrait are immediately recognizable as the same identity.

## Repair strategy

Prefer surgical edits over full regeneration when the board is otherwise successful:

```text
Change only [specific failing study/detail]. Preserve every other panel, identity trait, pose, crop, color, lighting choice, layout boundary, and rendering characteristic exactly. Do not redesign the character or alter any successful study.
```

If more than two identity-critical regions drift, regenerate from Image A rather than stacking broad edits.
