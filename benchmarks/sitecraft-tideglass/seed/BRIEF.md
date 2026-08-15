# TIDEGLASS departure board

Build a polished, responsive, single-page public information experience for **TIDEGLASS**, a fictional harbour departure briefing.

## Audience and primary job

Small-boat crews check it outdoors, often on a phone, sometimes in glare or with cold hands. The page's first job is to answer:

> Is there a sensible departure window this morning, and what should I check before leaving?

## Trust boundary

This is a demonstration, not a real navigation service. The interface must make **DEMONSTRATION DATA — NOT FOR NAVIGATION** unmistakable without making the whole page feel like an error screen. Do not invent testimonials, certifications, partners, live feeds, or safety claims.

## Required content

- Brand: `TIDEGLASS / EAST BREAKWATER`
- Lead: `Know the window. Leave with a plan.`
- Current decision: `CAUTION · SHORT WEATHER WINDOW`
- Best departure window: `06:40–08:10`
- Current observations:
  - Wind `WSW 17 kn`, gusting `24 kn`
  - Swell `1.4 m`, period `7 s`
  - Tide `+1.2 m`, rising
  - Visibility `6 nm`
- Three selectable time bands:
  - `Now`: caution, WSW 17 kn, gust 24 kn, swell 1.4 m
  - `07:00`: best window, WSW 13 kn, gust 18 kn, swell 1.1 m
  - `09:00`: hold, W 22 kn, gust 31 kn, swell 1.8 m
- Departure checklist:
  - File a shore contact
  - Confirm fuel reserve
  - Check VHF and lifejackets
  - Reassess at the harbour mouth
- Advisory copy: `Conditions are expected to tighten after 08:10. Recheck before casting off.`
- An email form titled `Get harbour notices` with useful empty, invalid, submitting, success, and failure states. It is a local demonstration and must not claim to send or store anything.
- Footer copy: `TIDEGLASS is a fictional interface built for an Agent Skill benchmark.`

## Interaction

Selecting a time band must update the decision and observation values. The control must work by keyboard and touch, expose its selected state, and remain understandable without animation.

The form must validate an email address locally and clearly state that the demonstration does not transmit or retain it.

## Technical constraints

- Deliver `index.html`, `styles.css`, `app.js`, and a short `README.md`.
- Use plain HTML, CSS, and JavaScript with no build step and no external network dependencies.
- Work at 320 CSS pixels through wide desktop without horizontal scrolling.
- Use semantic HTML, visible keyboard focus, adequate target sizes, and a useful reduced-motion treatment.
- Preserve browser zoom and user font settings.
- Keep the implementation small enough to inspect in one sitting.

## Design freedom

No visual style is prescribed. Derive an appropriate visual system from the audience, task, content, and harbour setting. Familiar safety and form controls should remain familiar.
