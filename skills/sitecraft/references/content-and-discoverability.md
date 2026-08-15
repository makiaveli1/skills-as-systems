# Content, discoverability, and internationalisation

Design content as part of the experience architecture. Do not add SEO, metadata, localisation, or social previews after the visual build is considered finished.

## Content authority

For every important claim record:

- owner or source;
- approval state;
- intended audience;
- page or surface;
- freshness and expiry;
- legal, privacy, or evidence requirement;
- whether AI may transform, summarise, or only place it.

Never invent testimonials, clients, metrics, qualifications, awards, availability, pricing, policies, or product capabilities.

## People-first content

Write for the visitor’s real questions and decisions. Use the language people use when looking for the subject, but do not distort the experience into keyword repetition.

A useful page should make clear:

- what it is;
- who it serves;
- the outcome or value;
- proof and limitations;
- the next action;
- material conditions such as price, access, eligibility, timing, privacy, or cancellation.

Use specific headings that describe the page’s point. Link text should explain its destination or action.

## Search and crawlability

For public content that should be discoverable, verify:

- stable, meaningful URLs;
- successful HTTP responses and indexable content;
- crawlable links rather than click handlers without destinations;
- titles and descriptions matched to page purpose;
- canonical URLs where duplicate routes or parameters exist;
- robots and indexing controls aligned with intent;
- sitemap coverage when useful;
- server or static rendering for essential public content when client-only rendering adds risk;
- image, video, JavaScript, and structured-data guidance appropriate to the content.

Meeting minimum technical requirements does not guarantee indexing or ranking. Do not promise outcomes.

## Metadata and social previews

Define per route:

- document title;
- meta description;
- canonical URL;
- language and direction;
- social title, description, image, and absolute URL;
- favicon and application identity;
- theme colour where useful;
- robots directive;
- structured-data type and source;
- fallback preview.

Social-preview images need a dedicated composition and crop. Do not reuse a desktop hero without checking text, focal point, safe zones, and platform rendering.

## Structured data

Use Schema.org vocabulary only when it truthfully represents visible or available content. Prefer the most specific supported type. Keep structured data consistent with the page, URLs, organisation identity, dates, prices, availability, and images.

Validate the generated graph and monitor errors. Structured data is not permission to add hidden promotional claims.

## Content states

Design content for:

- missing or delayed data;
- outdated information;
- unavailable products or events;
- expired campaigns;
- partial profiles;
- empty search or filters;
- draft, scheduled, archived, or withdrawn material;
- legal or policy updates;
- localisation gaps.

Give stale or unavailable content an intentional route rather than a broken card or silent disappearance.

## Internationalisation

Internationalisation is broader than translation. Decide early whether the experience must support more than one language, script, region, or cultural format.

Use:

- UTF-8 throughout;
- correct `lang` on the document and language changes within it;
- `dir` and bidirectional isolation where needed;
- CSS logical properties instead of hard-coded left/right assumptions;
- locale-aware dates, times, numbers, currency, pluralisation, names, addresses, sorting, and search;
- flexible components for text expansion and different line-breaking behaviour;
- fonts that cover required scripts;
- localized URLs, navigation, metadata, media, and error messages where appropriate;
- user-controlled language selection that does not trap or repeatedly redirect them.

Do not concatenate translated fragments into sentences or assume every name, address, phone number, date, or form field follows one culture’s structure.

## Content modelling

Separate content meaning from one visual component where practical. Define:

- field purpose and type;
- required and optional values;
- length and format constraints;
- allowed markup;
- relationships;
- ownership;
- localisation behaviour;
- lifecycle;
- fallback;
- presentation variants.

Use real or representative content during design and testing. Lorem ipsum hides hierarchy, overflow, tone, and trust failures.

## Measurement

Choose analytics from the Experience Contract’s success signals. Track only what supports a real decision. Define event name, trigger, properties, consent basis, retention, owner, and interpretation.

Do not install broad tracking by default. Avoid collecting sensitive or unnecessary data, and never use analytics as a substitute for user research.

## Content release check

Before release, verify:

- content authority and accuracy;
- no placeholder, fabricated, private, or expired material;
- titles, descriptions, canonical URLs, social previews, robots, and sitemap intent;
- structured data validity and page consistency;
- language and direction metadata;
- long, short, translated, missing, and stale content states;
- links and redirects;
- privacy, consent, and retention implications;
- owner approval for the exact content state.
