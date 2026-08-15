# Moderated session findings

Six people tried the first build on phones. Four were first-time hill walkers.

- People understood the route names but not whether “easy”, “steady”, and
  “hard” described fitness, terrain, or navigation.
- The coordinator needs to plan for one child and one person who tires easily.
- Several people tried to select Bracken Rise even after the ranger update
  closed it because of a damaged footbridge.
- Users wanted to know *why* an essential mattered, not only tick a box.
- Expert walkers still want ascent, terrain, signal, and timing details.

## Changed requirements

- `data/routes.json` now includes `suitability`, `why`, and current status data.
- Closed routes must remain comparable but cannot become the active plan.
- Add a group-needs choice with at least `mixed`, `child`, and `experienced`.
- Put `data-testid="group-needs"` on that choice group or control.
- Changing group needs must update route guidance without erasing expert detail.
- Preserve the existing visual identity and working behaviour rather than
  redesigning the whole experience.
