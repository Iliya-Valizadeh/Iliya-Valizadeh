# 0003: Five project rows for now, with room for a sixth

Date: 2026-09-26. Status: accepted.

## Context

The portfolio plan (section `5.6`) asks for a table of the six pinned projects. Only
five of them exist today: `credit-risk-scorecard`, `bank-filings-rag`, `second-look`,
`ds-project-standard` and `.github`. The sixth, `fraud-review-queue`, is Phase C of the
plan. Phase C has not started, because it needs a Kaggle key that only Iliya can set
up. The profile must not suggest that a project exists before it does.

## Options

1. Show six rows, with the sixth marked as coming soon. This describes work that does
   not exist.
2. Show five rows, with the count and the rows written into the template. Adding the
   sixth later means editing the template, the tests and the checks.
3. Show five rows, with the rows driven by `projects.toml`. Adding the sixth later
   means adding one entry to the config.

## Decision

Option 3. The table in the template is a loop over the `[[project]]` entries in
`projects.toml`, in the order they appear. The template has no project names, no
fixed count and no empty slot.

The table has five rows for now. The plan's "six pinned projects" becomes five until
Phase C ships `fraud-review-queue`. There is no row, placeholder, "coming soon" text
or number for `fraud-review-queue` anywhere in the config, template or README. Its
name appears only in decision records like this one.

When Phase C is done, adding it takes one new `[[project]]` entry in `projects.toml`
(with its number entries, if its `reports/metrics.json` exists), plus fixture copies
of its files for the offline tests.

A test proves the slot works without naming the future repo. It renders the template
with a test config that has one extra, made-up project, and checks that a sixth row
appears with no change to the template.

## Consequences

- Nothing on the profile describes work that has not been done.
- Adding a project is a config change, not a template change.
- The review task at the end of this phase greps the README, template and config for
  `fraud-review-queue` and expects no match.
