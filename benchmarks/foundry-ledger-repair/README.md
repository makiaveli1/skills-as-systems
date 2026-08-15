# Ledgerbox: FOUNDRY paired repair

Ledgerbox begins with four green unit tests and a hidden transaction-boundary
failure: interruption after the ledger write leaves a partial durable state, and
two concurrent deliveries can both credit the same event.

Two fresh Codex agents received the same seed and prompt. The baseline had no
skill; the second used FOUNDRY 0.2.0 from an isolated workspace-local install.
Both scored **100/100** under the frozen evaluator.

## What both conditions got right

Both found the same owner and made the same small repair:

- add a repository transaction context using `BEGIN IMMEDIATE`;
- put the duplicate check, credit write, checkpoint, and processed marker inside
  one commit/rollback boundary;
- add interruption/retry and separate-connection concurrency regressions;
- preserve the public function, schema, dependencies, and result values.

The evaluator independently proved rollback after interruption, one effect under
concurrent delivery, compatibility behavior, mutation rejection of the original
defect, bounded scope, and a useful run report.

## Where FOUNDRY changed the work

The scored result was parity, but the evidence record differed. The FOUNDRY run
separated symptom, proximate cause, root cause, and the missing-test contributing
condition. It also added a literal child-process exit check and 100 concurrent
delivery pairs. The baseline used the injected checkpoint and a reopen/retry
durability check. Both evidence sets were valid; FOUNDRY's was wider.

Compare the [baseline project](outputs/baseline/) and [FOUNDRY project](outputs/with-foundry/),
or inspect their [baseline](evidence/baseline.json) and [FOUNDRY](evidence/with-foundry.json)
receipts.

## Reproduce it

Copy [seed](seed/) into two isolated workspaces, use the frozen conditions in
[prompt.md](prompt.md), and install FOUNDRY only in the skilled workspace. Then
run the same evaluator against each result:

```bash
python3 evaluation/evaluate.py /path/to/candidate
```

This is a bounded repair that a strong unspecialized agent can solve. The result
should be published as parity plus an evidence-style difference, not as proof of
general superiority.
