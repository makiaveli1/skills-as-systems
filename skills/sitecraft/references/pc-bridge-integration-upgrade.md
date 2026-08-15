# PC Bridge Integration Upgrade — Sitecraft Creative Capabilities

This contract keeps Sitecraft's new image/video/motion capabilities aligned with PC Bridge rather than leaving them as prompt-only documentation.

## Goals

- Skill Fabric can discover the new Sitecraft capabilities and references.
- Protected external actions remain protected.
- Model/tool availability is discovered at runtime instead of assumed.
- parallel chats cannot silently overwrite the same Sitecraft files
- long-running/paid generation state survives handoff without duplicate submission
- generated assets remain inside approved project/output roots

## Capability routing

### Character Identity Board / Creative DNA
Read-only planning and prompt construction require no protected external capability. Image generation/editing should use the host's available image-generation surface; do not force API-key image generation when a built-in host image tool is intended.

### Oil Motion / interactive generated motion
Treat Oil Motion as optional reference/skill logic. Sitecraft may implement the resulting browser code itself. External generation used to create a continuous source clip follows the selected model's protected route.

### MiniMax H3
1. discover/probe an external MiniMax MCP before declaring H3 availability
2. if MCP lacks H3, use the official configured `mmx` CLI only with a project-scoped raw-shell lease
3. do not install tools or create credentials implicitly
4. preserve task ID/output provenance

### Kling
Keep current Kling integration and routing untouched. H3 is additive, not a replacement path.

## Parallel-change safety

Before modifying the skill package:
1. capture current file hashes/mtime for every target
2. prepare an exact multi-file plan against those source hashes
3. preview the plan
4. immediately before apply, verify source hashes again
5. apply atomically with backups/rollback
6. if any source hash moved, stop and rebuild the plan from the new live state

Do not resolve a concurrent edit by overwriting it.

## Handoff state for generation work

Persist only operational state required to continue safely:
- target project
- capability/model/transport chosen
- generation mode
- reference role/order
- task ID if one exists
- whether a paid creation request has already been submitted
- output target path
- last verified task state
- next safe action

Never store API keys, auth tokens, private prompt scratchpads, or unnecessary raw media copies in handoffs.

## Skill Fabric / manifest expectations

Sitecraft's PC Bridge metadata should expose the new reference modules as discoverable task guidance and include trigger language for:
- character identity board / character sheet / identity consistency
- creative DNA / reference analysis / visual reference decomposition
- interactive generated motion / scroll-controlled generated motion / pointer-follow motion / living wallpaper-style motion
- MiniMax H3 / Hailuo H3 / multimodal video generation

Routing should remain additive and specific so ordinary website work does not automatically load every heavy media reference.

## Verification

After updating the Sitecraft package:
- validate manifest/JSON/schema files
- run Sitecraft package tests
- run focused new-reference tests
- run PC Bridge integration/routing tests
- explicitly run Kling route/regression cases
- confirm no existing Kling integration file changed unless an independent bug fix was required
- bump version only after all checks pass
