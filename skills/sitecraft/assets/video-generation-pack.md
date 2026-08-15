# SITECRAFT Video Generation Pack

Use one copy per website video asset. This pack is provider-neutral; map it to the authenticated generator available on the executing host. For real execution, also instantiate `assets/video-generation-workflow-template.json` and keep its machine-checkable stage/evidence fields synchronized with this pack.

## Asset contract

- Asset ID:
- Website surface:
- Website role / purpose:
- Semantic role:
- Duration target:
- Master aspect ratio:
- Responsive derivatives:
- Loop or finite playback:
- Audio policy:
- First-frame requirement:
- Last-frame requirement:
- Continuity requirements across frames/shots/fallbacks:
- Copy-safe / crop-safe region:
- Poster / static fallback:
- Reduced-motion equivalent:
- Payload / delivery budget:
- Related Capability Plan decision ID:

## Route decision

- Can a still / CSS-WAAPI / SVG / canvas / live 3D / sourced-video route perform this role well enough? yes / no
- If no, why does generated motion materially improve the experience?
- Generation class: image-conditioned / text-conditioned / video-conditioned-editing / other discovered capability
- Why this class fits the asset contract:
- What must not be changed merely to fit the provider:

## Reference-role map

For every input reference state its exact role and exclusions.

- Reference ID:
  - Role: identity / environment / composition / palette-material / lighting / motion / camera / rhythm-audio / exclusion / other
  - Contributes:
  - Must preserve:
  - Must ignore:
  - Rights / provenance status:

## Director prompt

### Mode / settings

Duration, aspect, output intent and audio intent.

### Scene

Environment, lighting, mood, palette and texture.

### Subject

Identity, product, wardrobe, expression, posture, geometry and preservation rules.

### Action / motion

Concrete physical action, speed, rhythm and environmental motion.

### Camera

Framing, viewpoint, lens feel, movement, focus and transition behaviour.

### Shot / timing map

- 0–Xs:
- X–Ys:
- Y–Zs:

Mark any genuine signature moment and readable hold.

### Audio

Music, ambience, Foley, dialogue or silence. State synchronization requirements.

### Quality / preservation constraints

What cannot drift between frames or shots.

### Avoid

Specific unwanted artifacts, text, logos, morphing, anatomy/geometry failures, reference leakage, camera behaviour or stylistic errors.

## Provider inspection budget

Use this before generation when the provider exposes non-generating introspection for current models, arguments, limits or account-specific defaults.

- Provider selected at runtime:
- Live catalogue discovered: yes / no
- Provider inspection required: yes / no
- Inspection authority separate from generation authority: yes / no
- Exact introspection calls permitted:
- Inspection can consume credits: yes / no / unknown
- Inspection result / model-settings receipt:
- Provider/model/settings frozen for next attempt: yes / no

Inspection authority must not silently authorize generation when the host can enforce separate scopes.

## Paid-generation budget

- Paid generation: yes / no
- Provider selected at runtime:
- Exact provider/model/settings for next attempt:
- Maximum attempts:
- Automatic regeneration allowed: yes / no
- Credit/spend budget, when provider exposes a reliable unit:
- Maximum status/result polls per attempt:
- Poll cadence rule:
- Owner approval required again when:
- Stop conditions:

## Pre-generation gate

All must be yes before requesting generation authority:

- Website role is explicit: yes / no
- Generation class is explicit: yes / no
- Approved still/reference master exists when required: yes / no / not applicable
- Prompt + reference-role map + timing plan are ready: yes / no
- Poster/static + reduced-motion fallbacks are defined: yes / no
- Hard quality floors are written: yes / no
- Attempt ceiling, provider-interaction ceiling and spend/credit boundary are declared: yes / no
- Host can inspect the returned artifact: yes / no
- Current provider catalogue was discovered live: yes / no
- Required provider/model arguments were learned from live inspection or another current authoritative source: yes / no
- Exact provider/model/settings were checked against the asset contract: yes / no

If any answer is no, do not request generation authority yet.

For asynchronous jobs, status/result polling must query the existing generation task only. Do not resubmit generation because a result is still processing.

## Acceptance rubric

Hard floors should be binary where possible.

- Website-role adherence:
- Subject / product / identity stability:
- Motion coherence:
- Camera / framing:
- Lighting / material continuity:
- Temporal stability / flicker / morphing:
- Loop seam or first/last-frame fidelity:
- Copy-safe / responsive crop:
- Audio / sync when applicable:
- Unwanted text / watermark / logo artifacts:
- Originality / rights boundary:
- Delivery / performance suitability:
- Poster / static / reduced-motion equivalent:

Acceptance rule:

## Attempt ledger

### Attempt 1

- Provider/model/tool:
- Prompt/reference revision:
- Artifact reference/hash:
- Generation settings:
- Credits/cost reported by provider:
- Review method:
- Hard-floor failures:
- Timestamp/frame observations:
- Decision: accept / regenerate / fallback / provider-change / human-review
- Targeted change for next attempt:

Repeat only within the declared budget.

## Integration evidence

- Master accepted:
- Responsive derivatives created:
- Poster verified:
- Real page desktop evidence:
- Mobile / 320 CSS-pixel evidence:
- Reduced-motion evidence:
- Audio/autoplay/control evidence:
- Performance evidence:
- Browser-engine evidence:
- Evidence references / receipts carried into the machine workflow:
- Owner approval:
