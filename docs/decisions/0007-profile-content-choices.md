# 0007: Choices made while writing the profile text

Date: 2026-09-26. Status: accepted.

## Context

The content task rewrote the README template to plan section `5.6`. A few points were
not settled by ADRs 0001 to 0006, or the renderer did not yet do what those ADRs
describe. This record lists how each was handled.

## Decisions

The project table is built by the renderer. The template holds one
`{{ project_table }}` line, and each row's words live in `projects.toml` next to that
repo's numbers, as [ADR 0003](0003-five-rows-for-now.md) asks. A repo entry with
`metrics = false` may not have numbers, and its row says it has none. Numbers from
`second-look` carry `synthetic = true`, and the render fails if one sits on a line
without the word "synthetic", as [ADR 0002](0002-where-each-number-comes-from.md) asks.

The "Also" block stays on the same lines as in commit `fe5d040`: the heading on line
`39` and the Hack the North line on line `41`. The text above it was fitted to that
length, so the block did not move at all. A later edit that changes the length of the
text above the block should keep it there too, or ask Iliya first.

The renderer read a range such as `0.762-0.775` in a `CLAIMS.md` Value cell as
`0.762` and minus `0.775`. It now reads it as both ends of a range, the same way
`tools/claims_check.py` does. A minus sign right after a space still counts.

No number is typed into the README. Each interval is shown with its level only when
that level is in the repo's results file. `credit-risk-scorecard` keeps its level in
code, not in `reports/metrics.json`, so its row says "interval" with no level. Adding
the level to that repo's results file and its `CLAIMS.md` would fix this. That is a
change to another repo, so it is logged in `_portfolio/STATUS.md` rather than made here.

The Notes section is left out. No note is published yet, and the renderer does not
read the site's `notes.json` yet. [ADR 0005](0005-drafts-stay-out.md) says a profile
with no published notes has no Notes section. Reading `notes.json`, and the draft
marker rules in that ADR, are still to be built.

The Tools list is kept as Iliya wrote it. Plan section `5.6` does not ask for it, but
it is his own list, and removing it would drop facts only he can confirm.

## Consequences

- The README says nothing about Iliya that is not in the workspace `CLAUDE.md` or in
  his own kept lines.
- The review task at the end of this phase asks him to read the new text before the
  merge.
