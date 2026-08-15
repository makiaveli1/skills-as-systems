# Evidence and visual QA

Approval must be tied to evidence from the exact state under review.

## Evidence classes

### Structural evidence

Examples: DOM, semantic tree, source, computed styles, route map, component tree.

Proves structure and implementation facts. Does not prove visual quality.

### Static visual evidence

Examples: screenshots, contact sheets, visual diffs.

Proves composition at a specific viewport and state. Does not prove interaction or timing.

### Temporal evidence

Examples: screen recordings, traces, animation timelines.

Proves movement, timing, scroll, overlay, and interaction sequences. Does not prove semantic accessibility.

### Functional evidence

Examples: unit, integration, end-to-end, form, route, and API tests.

Proves declared behaviours under tested conditions. Does not prove taste or all visual states.

### Accessibility evidence

Examples: keyboard run, accessibility tree, automated scan, screen-reader spot check, zoom and reduced-motion tests.

Automated checks cover only detectable rules and must not be presented as full conformance.

### Performance evidence

Examples: field data, lab audits, traces, waterfalls, bundle analysis.

Record environment and distinguish local, preview, and production evidence.

### Security and boundary evidence

Examples: secret scan, public bundle inspection, source-map check, route/authorization test, dependency scan, deployment configuration review.

## Capability-linked evidence

Do not apply the same QA packet to every technical stack. When `implementation.capability_plan` contains consequential mechanisms, derive additional evidence from those mechanisms and carry it into the Evidence Contract.

Examples:

- scroll or animation timelines need temporal, interruption, reverse and reduced-motion evidence;
- authored vector runtimes need asset/loading/state/fallback evidence;
- canvas, GPU and 3D need responsive/device fallback, frame pacing, input responsiveness, lifecycle/cleanup and appropriate memory or energy observations;
- media needs poster/failure/playback/visibility/loading and byte-budget evidence;
- framework or server/client boundaries need route/history/loading/error/data and security evidence;
- realtime state needs reconnect, stale-state, ordering, conflict and failure evidence.

The Runtime Capability Plan declares what must be proved. The Evidence Contract records where it was actually proved. A host that lacks the required observation capability must leave that gate unverified rather than substituting a different evidence class. See [capability-palette-and-orchestration.md](capability-palette-and-orchestration.md).

For consequential capability decisions, carry the contract decision ID into the evidence ledger's optional `capability_decision_ids` column. Use a semicolon-separated list only when one evidence item genuinely judges more than one decision. The SITECRAFT Review may then reference the same IDs through `capability_scope`, blocking floors, findings, or repair steps. This creates traceability without copying the technical decision into every artifact.

## Minimum visual matrix

For substantial public sites, review:

- wide desktop;
- standard desktop;
- short laptop;
- tablet or intermediate state;
- narrow mobile;
- 320 CSS-pixel reflow;
- default and reduced motion;
- at least one keyboard path;
- loading, empty, error, and success where relevant.

Add landscape mobile, high-density data, long translation, dark mode, logged-out, permission-denied, or other states when the experience requires them.

## Environment matrix

Keep visual and interaction coverage separate from operating-system and browser coverage. The viewport matrix answers **which composition or state** was reviewed. The environment matrix answers **where and how** it was reviewed.

For every material support row record:

- operating system and architecture;
- browser name, engine, and version when known;
- native, headless, remote, emulated, containerised, or virtualised execution;
- form factor, viewport, device-pixel ratio, input modes, motion preference, and assistive technology;
- automation, screenshot, recording, or manual provider;
- exact build identity and contract revision;
- status, evidence references, limitations, reviewer, and date.

A passed row does not pass another row. A simulated Windows-style path test on macOS is not a Windows browser receipt. See [platform-and-browser-portability.md](platform-and-browser-portability.md).

## Screenshot discipline

Record:

- exact URL or route;
- commit/build identity when available;
- viewport width and height;
- browser, rendering engine, operating system, and architecture;
- native, headless, remote, emulated, containerised, or virtualised execution;
- zoom, device-pixel ratio, theme, motion preference, input mode, assistive technology, and authentication state;
- screenshot or automation provider and known capture limitations;
- timestamp;
- expected baseline or contract revision.

Crop only after preserving a full-context capture. Do not approve from a compressed preview when typography, artefacts, or spacing require full resolution.

## Recording discipline

Record only the bounded interaction under review. Include start, action, response, and stable end state. Review:

- input response;
- focus movement;
- motion continuity;
- scroll and sticky behaviour;
- loading and interruption;
- overlay entry, containment, escape, and return;
- route and browser-history behaviour;
- responsive state changes;
- reduced-motion alternative.

## Visual regression

Use screenshot comparison for stable surfaces and critical states. Keep baselines in a controlled environment because rendering varies by browser, operating system, fonts, hardware, and headless settings.

A baseline update is a review action, not a way to make a failed test green. Require an explanation and evidence for intentional differences.

Mask or stabilise clocks, random data, cursors, remote ads, animation, and nondeterministic regions when they are not under test.

## Defect language

Report defects as:

- observed evidence;
- expected contract;
- user consequence;
- likely ownership layer;
- severity;
- smallest repair;
- verification needed.

Avoid “looks off” without identifying hierarchy, alignment, crop, contrast, rhythm, interaction, or content cause.

## Review provenance

Start reviews with blocking floors and observed defects; use scores only after the evidence and failures are clear. When review independence matters, record who or what performed each pass and how it relates to the build:

- self-review — useful for immediate defect finding, but not independent;
- fresh-context review — the same actor re-checking with fresh context; stronger against local tunnel vision, still not independent;
- independent-agent review — a separate reviewer or agent that did not author the current change;
- human-owner review — the owner’s judgement and approval authority;
- automated evidence check — schema, test, diff, accessibility scan, performance check, or another machine check with a narrow stated scope.

Do not call a self-review, fresh-context pass, or automated check “independent.” A small repair does not need ceremony; use provenance where it materially changes confidence, approval, or handoff quality.

## Diagnostic escalation

Begin with the lightest evidence that can answer the question: structure, screenshots, recordings, interaction checks, accessibility checks, and ordinary performance observations. Escalate only when a real defect remains unexplained or a consequential mechanism needs deeper proof.

Useful escalations can include console output, network evidence, browser/runtime logs, route/history state, traces, performance profiles, media metadata, or frame-level inspection. Define the trigger and scope before collecting them, and stop once the cause or required proof is clear. A trace or log does not broaden the claim beyond the environment and state actually observed.

Use optional `evidence_contract.diagnostic_escalation` when the project has a known class of failures that may require this deeper route. Leave it absent for ordinary work.

### Host-safe evidence execution

Treat the host's execution boundaries as part of evidence integrity. If a visual renderer, screenshot command, browser harness, or diagnostic action is not allowed by the host's safe test/workflow runner, do not rename it, wrap it in an allowed test script, or otherwise disguise arbitrary execution as verification. Prefer an explicitly declared preview/dev process, a host-native browser or capture capability, a narrowly approved capability lease, or a separate bounded evidence worker. If none is available, record the evidence plan and mark that state unverified.

A host-approved preview process may be used to expose the real application to a browser review surface when it preserves the application's actual layout/state and remains outside the public build. Record whether a viewport is native, headless, or embedded/emulated; an iframe or scaled review frame proves only the layout/state rendered inside its declared viewport and does not become native-device evidence.

## Approval receipts

An approval record should include:

- contract revision;
- exact build or commit;
- evidence paths or IDs;
- views and interactions reviewed;
- known exclusions;
- reviewer and decision;
- date;
- whether release is authorised.

Any implementation change after the receipt makes affected evidence stale until revalidated.

## Capability honesty

If a host cannot capture or inspect evidence, provide an evidence plan and mark the state unverified. Scope every claim to the exact environment observed. Never fabricate screenshots, recordings, tests, browser inspection, operating-system coverage, browser-engine coverage, assistive-technology coverage, or cross-platform confidence.
