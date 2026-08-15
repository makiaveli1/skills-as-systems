# SITECRAFT Image Generation Pack

Use this portable pack when a website needs generated or edited raster assets. The Experience Contract remains the authority for the website role, protected foundations, asset IDs, production-job dependencies, responsive requirements, delivery, evidence and approval state. This pack carries execution-ready image instructions; it does not replace the contract or asset ledger.

## 1. Package identity

- Project:
- Experience Contract path and revision:
- Image-system production pack path:
- Asset-ledger path:
- Source host:
- Intended receiving host:
- Current image production boundary:

## 2. Host preflight

Before generating or editing anything, confirm the current host can perform the job it is about to claim.

Record each as `confirmed`, `unavailable`, or `unknown`:

- generate raster images;
- edit an existing raster image while preserving named invariants;
- make each required local or attached reference actually available to the image generator;
- isolate the execution context so only this job's specification, declared references, and unavoidable host policy reach the generator;
- inspect the returned full-resolution image;
- save or import an accepted project-bound image into the project workspace;
- preserve source files and avoid destructive overwrite;
- run or obtain the browser/composition review required by the Experience Contract.

Also record the execution-context mode as `isolated request`, `fresh bounded context`, `mixed conversation context`, or `unknown`.

For users working through a subscription product rather than paid API calls, `fresh bounded context` is a first-class route. A host-native image worker covered by an existing plan or usage allowance is also first-class when it can accept the exact bounded prompt and local reference files. On ChatGPT, prefer a Temporary Chat outside the website Project when available; attach only the current job packet and declared reference image(s). Generate or edit that one job there, then return the candidate to the director/build context for persistence and website review. Start a new bounded chat or isolated host job for each independent production job; for sibling edits, restart every sibling from the same approved parent rather than continuing from the previous sibling.

A filesystem path is not automatically an image-model input. If the generator cannot actually see a required local reference, do not pretend the job is ready. Likewise, a host that technically generates images but may infer from unrelated conversation/project context is not ready for consequential or reference-dependent production work. Use a narrower host-native subtask, a fresh image-only context, an explicit prompt/file execution route, or another capable image-production host. Do not require API spend when a subscription, local or human route satisfies the same contract.

## 3. Production graph

Copy or summarise the authoritative `image_system.production_jobs` entries from the Experience Contract. Do not invent a different order here.

| Job ID | Output asset ID | Intent | Depends on jobs | Required approved assets | Source/edit-target assets | Reference IDs | Parallel group | Prompt section |
|---|---|---|---|---|---|---|---|---|
|  |  | generate/edit |  |  |  |  |  |  |

Rules:

- one distinct output asset = one production job;
- variants of one prompt are exploration candidates for that job, not substitutes for separate asset jobs;
- only independent jobs may run concurrently;
- a dependent job waits until every declared prerequisite and required approved input passes its gate;
- an edit starts from its declared source/edit target, not from the most recently generated sibling;
- when several sibling derivatives must preserve one approved master, every sibling restarts from that same declared master unless the Experience Contract explicitly says otherwise;
- never advance because an image is merely attractive; advance only when the job's acceptance gate passes.

## 4. Per-job execution block

Duplicate this section once per production job.

### Job: `<job-id>`

**Output asset**
- Asset ID:
- Intended filename or workspace reference:
- Website surface:
- Website role and visitor effect:
- Intent: `generate` or `edit`

**Readiness gate**
- Depends on job IDs:
- Required approved asset IDs:
- Source/edit-target asset IDs:
- Reference IDs:
- Ready to execute: yes/no
- If no, blocker:

**Reference map**

| Reference ID | Role | Exact contribution | Preserve | Ignore / do not transfer | Rights / permission |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

**Generation or edit specification**

Use case / asset type:

Primary request:

Scene / backdrop:

Subject:

Composition / framing / negative space:

Lighting / mood:

Colour / materials / texture:

Preserve:

Exclude:

Output ratio / dimensions / format intent:

**Edit-only invariant rule**

If this is an edit, state the change as one bounded operation:

> Change only: `<target change>`.
> Preserve: `<camera / geometry / identity / layout / palette / text / unrelated details>`.
> Do not add or redesign unrelated content.

Repeat the invariants on every edit iteration.

**Acceptance gate**

- hard pass conditions:
- responsive/crop conditions:
- identity/geometry/material conditions:
- text/logo conditions if applicable:
- rights/consent conditions:
- browser/composition evidence required before final site approval:

**Failure decision**

- `APPROVE CANDIDATE` only if all hard pass conditions pass;
- `TARGETED EDIT` when the composition/source is right and one bounded defect can be repaired;
- `REGENERATE JOB` when the job's core composition, identity, geometry, role, or reference interpretation is wrong;
- `BLOCK / CHANGE ROUTE` when the current host cannot supply or inspect the required references or returned artifact;
- `CONTEXT CONTAMINATION / CHANGE ROUTE` when the output imports unrelated workflow notes, UI, text, objects, or project discussion that were not declared in this job;
- stop repeating the same failed approach when the declared stop condition is reached. Do not fix context contamination by merely adding more negative prompt text to the same mixed-context route.

## 5. Candidate and approval lifecycle

For project-bound assets:

1. Generate or edit a candidate without overwriting an approved master.
2. Inspect the actual returned image at useful resolution.
3. Diagnose failures against the job acceptance gate.
4. Make one targeted repair at a time; repeat protected invariants.
5. When the candidate passes image-level QA, save/import it into the project's candidate or working asset area using a stable semantic filename.
6. Record source/reference lineage and the production job's asset ID in the existing asset lineage/ledger fields.
7. Place the candidate in the real website composition and collect the required responsive/browser evidence.
8. Promote it to approved master only after the project's approval rule passes.
9. Create responsive, delivery, motion or lighting derivatives only from the declared approved source.

Do not leave a project-referenced final only in a host-specific generated-media folder, chat attachment, temporary URL, or opaque tool history.

## 6. Naming and persistence

Prefer stable semantic filenames based on asset role and state, for example:

- `home-world-master.png`
- `home-world-mobile.png`
- `era-room-master.png`
- `era-room-shelter.png`

Use versioned or candidate filenames when replacing an existing file has not been explicitly approved. Host-specific temporary names are not project identity.

## 7. Independent-job batching

Batching means scheduling independent jobs efficiently; it does not weaken dependency gates.

Safe:

- generate two unrelated environment assets concurrently when neither depends on the other;
- request several candidates for one job as exploration, then select one before downstream work.

Unsafe:

- generate derivatives before their required base master is accepted;
- let a sibling derivative become the accidental source for the next sibling;
- treat one prompt with several unrelated requested assets as a substitute for distinct jobs when their constraints differ;
- parallelize edits that depend on a mutable, not-yet-approved source.

## 8. Receiving-host handoff

When image production moves to another host:

- re-read the Experience Contract and current production graph;
- re-discover host image-generation, edit, reference-loading, inspection and project-import capabilities;
- verify the exact required reference files or attachments are actually available to that host;
- carry context, not permissions or credentials;
- continue only jobs whose dependency and approval gates are currently satisfied;
- return generated candidates with stable asset IDs, filenames/references, prompts or edit instructions, source/reference lineage, and observed defects;
- do not claim browser/site approval unless the required Sitecraft composition evidence was actually reviewed.

## 9. Final family QA

Before declaring an image family complete, verify:

- every requested asset ID has a real artifact;
- each artifact came from the declared job and source/reference chain;
- sibling derivatives preserve the intended common master rather than drifting cumulatively;
- no approved source was silently overwritten;
- responsive art direction is intentional rather than blind centre-cropping;
- assets work inside the actual website hierarchy, not only in isolation;
- the asset ledger/lineage, evidence matrix and Experience Contract agree on current approval state;
- temporary prompts, local paths, private references and internal review material are not shipped publicly.
