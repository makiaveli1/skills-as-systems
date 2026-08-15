# Accessibility

Treat accessibility as part of the design and implementation contract, not a final automated score.

## Target

Use WCAG 2.2 Level AA as the default public-web target unless the project requires a stricter or different standard. Record exceptions and legal or organisational requirements separately.

## Structure and meaning

Verify:

- meaningful headings and landmarks;
- correct native elements before ARIA;
- labels, names, roles, values, and instructions;
- DOM reading order matching the intended logical order;
- lists, tables, forms, dialogs, alerts, and status messages represented correctly;
- language and title metadata;
- meaningful link and button text.

Visual grouping cannot replace semantic structure.

## Keyboard and focus

Every interactive path must work without a pointer. Verify:

- visible focus;
- logical focus order;
- no keyboard traps;
- skip or bypass mechanism where needed;
- focus enters and exits overlays deliberately;
- focus returns to the invoking control when appropriate;
- sticky elements do not obscure focused content;
- custom widgets match established keyboard patterns;
- drag operations have non-drag alternatives.

Do not remove outlines without a stronger replacement.

## Reflow, zoom, and text

Verify:

- content reflows at 320 CSS pixels;
- text can enlarge without loss of function;
- text-spacing overrides do not break layouts;
- content does not rely on fixed pixel heights;
- long strings wrap;
- labels and inputs remain usable;
- fixed headers and footers do not consume the narrow viewport.

## Colour and perception

Verify:

- text and UI contrast;
- focus contrast;
- status is not communicated by colour alone;
- selected, error, warning, and disabled states remain distinguishable;
- background images do not compromise text;
- charts and diagrams have labels, patterns, or equivalent data.

## Targets and input

Aim for comfortable controls and use at least the applicable WCAG minimum. Prefer 44 by 44 CSS pixels for primary standalone controls when space permits, especially for frequent, edge-positioned, destructive, or hard-to-undo actions.

Support touch, mouse, keyboard, zoom, and assistive technology without requiring precision gestures.

## Images and media

- Write alt text for the purpose of the image in context.
- Use empty alt for genuinely decorative images.
- Provide captions, transcripts, audio description, or equivalent alternatives when applicable.
- Do not embed essential text into images unless necessary.
- Preserve controls for autoplay, pause, stop, volume, and motion.

## Motion and flashing

Respect reduced motion. Suppress non-essential interaction-triggered motion when the user requests it. Avoid flashing and blinking patterns that can cause harm. Provide pause or stop controls for moving content where required.

## Forms and authentication

Verify:

- visible labels and instructions;
- clear required and format guidance;
- errors connected to fields and summarised where useful;
- preservation of entered values after errors;
- no repeated data entry without reason;
- accessible authentication that does not depend only on memory, puzzles, or impossible transcription;
- confirmation for destructive or irreversible actions.

## Automated and manual testing

Use automated tools to find detectable issues, but do not treat a clean automated report as conformance. Combine:

- semantic and DOM inspection;
- keyboard testing;
- screen-reader spot checks appropriate to the platform;
- zoom and reflow testing;
- contrast and target checks;
- reduced-motion testing;
- form and error testing;
- real content and state review.

Record tool, browser, operating system, viewport, and evidence date.
