# Blind visual review: CAIRN

Review four anonymized implementations of the same small web experience. You
receive one desktop and one mobile screenshot for candidates A, B, C, and D.
Do not guess which workflow produced them.

The product helps a mixed-experience walking group compare three routes, choose
one, cover practical safety essentials, and leave with a shared plan. The tone
is calm field intelligence: tactile, observant, and quietly confident. Generic
SaaS dashboards, glass-card grids, neon gradients, and adventure-brand clichés
are explicitly unwanted.

Functional acceptance, keyboard behavior, overflow, no-JavaScript content, and
reduced motion are evaluated separately. Judge only what the screenshots can
support.

For each candidate, score these task-specific dimensions from 1 to 5:

1. `field_identity`: distinctive visual identity appropriate to the brief;
2. `decision_hierarchy`: how clearly the page helps the group understand what
   matters and make a route decision;
3. `content_clarity`: legibility and scanability of safety, route, and group
   guidance;
4. `responsive_composition`: whether desktop and mobile feel intentionally
   composed rather than merely stacked;
5. `coherence_and_polish`: consistency, finish, spacing, type, and restraint.

Return strict JSON only with this shape:

```json
{
  "candidates": {
    "A": {
      "scores": {
        "field_identity": 1,
        "decision_hierarchy": 1,
        "content_clarity": 1,
        "responsive_composition": 1,
        "coherence_and_polish": 1
      },
      "total": 5,
      "strengths": ["..."],
      "weaknesses": ["..."]
    }
  },
  "ranking": ["A", "B", "C", "D"],
  "winner": "A",
  "decision": "One concise paragraph grounded only in visible evidence.",
  "limits": ["What the screenshots cannot establish."]
}
```

Use the full 1–5 range when warranted. Do not reward density by itself. Do not
reward decorative novelty that weakens the planning job. If candidates are
close, say so.
