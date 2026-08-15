# Reliability, observability, incidents, and recovery

## Reliability target

Define critical user journeys, service level indicators/objectives where appropriate, error budget or acceptable failure, dependencies, recovery objectives, and degraded behaviour. Reliability beyond the required level can consume disproportionate complexity and cost.

## Failure design

For each critical path identify:

- dependency timeout and cancellation;
- bounded retry, backoff, jitter, and retry budget;
- overload, admission control, queue bounds, and backpressure;
- circuit/open-state or fallback semantics when justified;
- duplicate, partial, and unknown outcomes;
- health/readiness and safe startup/shutdown;
- state recovery, reconciliation, and manual controls;
- feature disable, rollout halt, or rollback path.

Retries multiply load. One layer should own them for a given operation.

## Observability by question

Instrument so operators can answer:

- Is the user-visible objective failing?
- Where in the path is time or failure occurring?
- Which version, tenant, region, dependency, or operation is affected?
- What state transition or deployment preceded it?
- Can impact and recovery be verified?

Use metrics for trends/objectives, logs for events and state details, traces for causal paths, and profiles for resource attribution. Correlate without leaking sensitive data. Instrumentation volume and cardinality need budgets.

Alert on actionable user/system consequences, not every internal anomaly. Preserve detailed diagnostic signals for investigation.

## Incident sequence

1. Confirm and bound impact.
2. Stabilize users/data; stop harmful changes or traffic where authorized.
3. Establish roles, communication, timeline, and exact state for serious incidents.
4. Preserve evidence while running reversible diagnostics.
5. Form and falsify hypotheses.
6. Mitigate with the lowest-risk effective action.
7. Verify recovery from the user/system view.
8. Repair root cause separately if mitigation is temporary.
9. Record follow-up owners and evidence.

Do not perform speculative cleanup during an active incident. Do not destroy logs or state needed for diagnosis.

## Recovery and rollback

Verify rollback against data and version compatibility. A code rollback may fail after a schema, queue, cache, or external side effect changed. Define forward recovery, reconciliation, restore, and user repair where rollback is unsafe.

Rehearse backups and restore; backup existence does not prove recoverability.

## Post-incident learning

Separate trigger, proximate cause, root cause, contributing conditions, impact multipliers, detection gaps, and response friction. Prefer corrective actions that change system conditions, tests, observability, rollout, or recovery—not vague reminders to be careful.

Keep learning scoped. One incident may establish a local failure pattern; universal doctrine needs broader evidence.

## Evidence

Record impact window, exact versions/configuration, timeline, telemetry references, mitigation, recovery checks, residual risk, and follow-ups. Never claim complete recovery from an internal metric alone when the user path remains unobserved.
