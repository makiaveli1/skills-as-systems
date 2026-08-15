# Research and reference analysis

Use research to reduce uncertainty, not to decorate a predetermined design.

## Research triggers

Research current sources when the task depends on:

- real users, markets, competitors, products, organisations, or locations;
- current browser, platform, AI-builder, framework, accessibility, security, or deployment behaviour;
- legal, policy, compliance, pricing, or service claims;
- cultural, historical, architectural, fashion, or visual accuracy;
- unfamiliar terminology;
- public brand guidelines or design systems;
- discoverability and structured-data requirements;
- a reference site whose mechanism must be understood before transformation.

Do not browse merely to collect fashionable screenshots.

## Source hierarchy

Prefer:

1. user-owned source material and explicit owner decisions;
2. official specifications, documentation, brand guidelines, and repositories;
3. primary product pages and public design systems;
4. reputable technical or design publications;
5. direct observation of the deployed experience;
6. community discussions and examples for failure patterns or implementation nuance.

Separate verified facts, direct observations, and interpretation.

## Competitive and category review

For each relevant site or product record:

- audience and promise;
- first-screen job;
- navigation and route model;
- proof and conversion sequence;
- content density;
- composition and visual grammar;
- interaction and motion mechanisms;
- responsive changes;
- accessibility and performance signals visible from observation;
- category conventions;
- clichés and gaps;
- what the new project should contrast with.

Do not score a competitor only by visual appeal. A beautiful site can have weak task completion, accessibility, or trust.

## Reference-role map

Assign each reference one or two bounded roles:

- information architecture;
- content hierarchy;
- composition;
- typography;
- colour/material;
- image treatment;
- interaction;
- motion;
- responsive transformation;
- implementation technique;
- evidence or testing method.

Record:

- source and date;
- role;
- exact mechanism;
- what is source-specific;
- what may be transformed;
- project synthesis: what the learned mechanism becomes in this project;
- what must not be copied;
- confidence and unresolved questions.

Avoid giving one reference authority over the whole project.

## Mechanism extraction

Translate a reference into neutral rules.

Instead of:

> Make it like this website.

Use:

> The reference uses a persistent artwork field, a narrow text rail, and route transitions that preserve the selected object. For this project, retain only the continuity mechanism; use the project’s own artwork proportions, route model, typography, colour, and navigation.

This makes the design explainable and reduces copying.

## Diverge only when direction is genuinely open

Do not manufacture three cosmetic variants because a creative process is expected to "show options." When the brief is genuinely unsettled, compare a small number of structurally different directions: different hierarchy, navigation, spatial model, pacing, content relationship, interaction model, or another experience-level choice. Colour swaps and component reskins do not count as meaningful divergence.

When this decision matters, record it in optional `visual_grammar.direction_selection`. Use `exploring` while comparing at least two real directions, `converged` after one is selected, and `not_needed` when the project already has a strong approved direction. After convergence, continue building the selected system instead of repeatedly reopening ideation unless a named reopen condition becomes true.

## Project-native synthesis

A learned mechanism must be translated into the current project before implementation. Express it through this project’s information hierarchy, tokens, typography, components, responsive compositions, accessibility rules, performance budget, and existing code conventions. A reference can suggest a mechanism; it must not become a parallel design system or a hidden source of truth.

## Learning promotion

A successful project can propose a reusable SITECRAFT lesson, but project success alone does not make the lesson core doctrine. Record an optional `sitecraft-learning-candidate` only when a learning is worth preserving. Keep the candidate project-local while it contains:

- the user or owner verdict;
- exact supporting evidence;
- the proposed lesson and bounded scope;
- at least one plausible counterexample risk;
- evidence from a meaningfully contrasting project or stronger external/official evidence before promotion;
- the intended core destination if promotion is approved.

Promotion requires explicit `approved_for_promotion` authority plus contrasting or stronger external evidence. Preserve the original project/example even after promotion so later reviewers can see where the lesson came from instead of rewriting history around the new rule. Rejected or mixed results are useful evidence too; do not delete them merely because they do not support the preferred lesson.

## Visual research boards

A useful reference board should show:

- why each item is present;
- the specific mechanism under study;
- positive and negative examples;
- desktop and narrow states where available;
- motion start/end frames or short clips when timing matters;
- evidence of category sameness to avoid;
- the project-specific synthesis.

Do not build a moodboard made only of attractive but unrelated images.

## Current facts and expiry

For browser support, AI tools, framework features, pricing, platform specifications, or policies, record:

- source;
- access date;
- version or status;
- exact claim supported;
- whether the fact must be rechecked before release.

Use official current sources when the user asks for latest information. Do not treat a dated reference file as permanently current.

## Research output

Return the smallest useful form:

- source table;
- category pattern summary;
- reference-role map;
- opportunities and clichés;
- original design implications;
- unresolved risks;
- claims that require later verification.

Research does not approve a design. It informs the Experience Contract and later evidence requirements.
