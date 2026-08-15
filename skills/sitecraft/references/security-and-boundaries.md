# Security and public/private boundaries

Design public and private systems as separate trust zones. Hiding an element in the interface does not protect its data or code.

## Classify material

Before implementation classify:

- public content;
- public configuration;
- authenticated user data;
- privileged staff or owner data;
- secrets and credentials;
- internal tools and routes;
- unpublished assets;
- debug and test material;
- analytics and consent data;
- third-party content.

Record where each class may exist: repository, build system, server, browser bundle, storage, logs, screenshots, and deployment output.

## Public build rule

Anything shipped to the browser must be treated as inspectable. Do not place secrets, privileged routes, internal notes, hidden answers, private metadata, unrestricted keys, or sensitive API responses in client code merely because the UI does not display them.

Framework variables explicitly marked public are bundled for the browser. Use server-only variables for secrets and privileged configuration.

## Physical exclusion

Prefer separate directories, build entries, environment boundaries, repositories, services, or deployment targets for private tools when practical. A public build process should not copy private material and then attempt to hide it with CSS, routing, or client-side conditions.

Use allowlists for public export when the project contains mixed public and private material.

## Source and debug material

Review production output for:

- source maps;
- comments and metadata;
- internal file paths;
- stack traces;
- debug panels;
- development routes;
- test fixtures;
- staging endpoints;
- feature flags;
- verbose errors;
- hidden administration links;
- embedded configuration.

Decide deliberately whether production source maps are needed and how they are access-controlled.

## Authentication and authorization

Authentication proves identity. Authorization decides access. Enforce authorization at the server, API, database, or storage boundary, not only in components or route guards.

Test:

- direct requests to privileged routes;
- object-level access;
- role changes;
- expired sessions;
- missing and malformed tokens;
- browser history after logout;
- cached private responses;
- file and media URLs;
- administrative actions.

## Input and output

Validate untrusted input at the appropriate boundary. Encode output for its context. Use parameterised database access. Treat filenames, uploads, rich text, URLs, redirects, markdown, HTML, and third-party embeds as attack surfaces.

## Browser defences

Use appropriate controls such as:

- Content Security Policy;
- secure, HttpOnly, SameSite cookies;
- HTTPS and secure contexts;
- frame and clickjacking protection;
- referrer policy;
- permissions policy;
- CORS with explicit origins;
- Subresource Integrity for eligible third-party resources;
- safe link handling for new tabs;
- dependency and supply-chain review.

Choose policies for the architecture and test them; do not copy a header block without understanding breakage and reporting.

## Third parties

For each external script, embed, font, analytics service, form, map, payment, chat, or CDN record:

- purpose;
- data sent;
- consent basis;
- loading and failure behaviour;
- privileges;
- integrity and origin controls;
- performance cost;
- owner;
- removal path.

## AI-builder boundaries

Do not paste production secrets, private user data, unpublished credentials, or sensitive datasets into a builder prompt. Use placeholders and the platform's secret management. Inspect generated code for hard-coded keys, permissive policies, unauthorised data access, and public debug output.

## Release checks

Before public release:

- inspect the generated public bundle and static output;
- search for secret patterns and private identifiers;
- verify environment-variable classification;
- test direct access to protected routes and objects;
- confirm error responses do not leak internals;
- inspect source maps and build artefacts;
- verify third-party origins and policies;
- record unresolved risk and owner acceptance.

Do not call the site secure because no obvious key appears in the repository. Security requires architecture-appropriate testing and maintenance.
