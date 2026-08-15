# Debugging and repair

## Contents

[Loop](#the-evidence-loop) · [failure](#define-the-failure-precisely) · [cause levels](#cause-levels) · [fault classes](#fault-classes) · [hypotheses](#hypothesis-table) · [escalation](#evidence-escalation) · [intermittence](#intermittent-failures) · [repair](#repair-selection) · [environment](#environment-versus-code-diagnosis) · [closeout](#closeout)

## The evidence loop

Use:

`symptom → reproduce → collect → narrow → hypothesize → falsify → locate → repair → replay → regress → widen`

Do not edit until at least one hypothesis explains the evidence and names an owning layer, unless the action is a reversible diagnostic probe.

## Define the failure precisely

Record:

- expected versus actual behaviour;
- first known bad state and last known good state when available;
- inputs, environment, versions, configuration, data shape, timing, and frequency;
- impact and affected users/systems;
- deterministic, intermittent, load-dependent, time-dependent, or environment-specific character;
- current reproduction and missing reproduction conditions.

Do not turn an error message into the problem statement when it may be downstream noise.

## Cause levels

Distinguish:

- **symptom:** visible failure;
- **proximate cause:** immediate mechanism producing it;
- **root cause:** condition whose correction prevents recurrence in the intended scope;
- **contributing condition:** factor that increased probability, severity, or detection delay;
- **trigger:** event that exposed the latent condition.

A repair may need to address root cause plus selected contributing conditions. Do not label every systemic weakness the root cause of one incident.

## Fault classes

Route evidence across:

- code defect;
- configuration or feature-state mismatch;
- dependency/version or build-resolution issue;
- environment, platform, permission, or resource issue;
- malformed, stale, corrupt, or unexpected data;
- race, timing, ordering, cancellation, or clock issue;
- infrastructure, network, storage, or service dependency;
- test, fixture, mock, or harness defect;
- user workflow, contract, or environment mismatch.

Inspect boundaries before rewriting business logic.

## Hypothesis table

For each plausible cause record:

- why it fits existing evidence;
- prediction that would be true if correct;
- cheapest discriminating observation;
- result;
- status: supported, weakened, falsified, or untested.

Prefer tests that separate two hypotheses. Change one causal variable at a time where practical.

## Evidence escalation

Start with the lightest evidence that can discriminate:

1. focused reproduction and logs/errors;
2. current configuration, dependency, and data inspection;
3. targeted assertions or instrumentation;
4. debugger, trace, profile, packet/query plan, or state snapshot;
5. controlled fault, timing, load, or environment experiment.

Stop escalating when the cause and repair proof are clear. Remove temporary instrumentation or explicitly retain it as useful observability.

## Intermittent failures

Control or record:

- seeds and randomness;
- clocks, time zones, and deadlines;
- scheduling and concurrency;
- network latency, retries, and duplicate delivery;
- shared mutable state and test order;
- resource pressure and rate limits;
- cache, replica, and eventual-consistency state.

Do not add a sleep or retry until the intended synchronization or failure contract is understood.

## Repair selection

Fix the owning cause at the narrowest coherent layer. A valid repair:

- makes the previous failure impossible or handled by contract;
- preserves valid neighbouring behaviour;
- exposes rather than swallows unexpected failure;
- adds a regression test at the responsible boundary;
- avoids dependency or architecture churn unless the cause requires it;
- includes recovery for data or operational side effects.

Broad catch-all exceptions, default values, cache deletion, environment recreation, and version upgrades may hide the symptom. Use them only when they are the proven contract.

## Environment-versus-code diagnosis

Compare a minimal matrix of known-good and failing dimensions: source revision, lock/resolved dependencies, runtime, OS/architecture, configuration, credentials/permissions, data/fixture, external service, and execution command. Change one dimension or use a controlled environment snapshot.

If the code is correct only under undocumented environment state, the system may still have a reproducibility or configuration defect.

## Closeout

Require:

- previous failure replayed successfully or limitation stated;
- regression test that fails for the causal defect;
- focused and widened verification;
- final state and diff inspected;
- root/proximate/contributing causes reported accurately;
- temporary workarounds and residual risks named;
- incident or operational follow-up routed separately when needed.
