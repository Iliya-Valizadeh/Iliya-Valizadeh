# 0004: The checks this repo runs, and the Hack the North guard

Date: 2026-09-26. Status: accepted.

## Context

Every repo in the portfolio runs the same writing and number checks in CI. They live
in `ds-project-standard/tools`. This repo is not a data science project, so parts of
the house standard do not fit it. It has neither a model nor a dataset, and its README
has no "Try it" section.

One line of the README has a hard rule. At commit `fe5d040`, the README ends with an
"Also" block: the `## Also` heading, three short lines, and the contact line (lines
`39` to `45` of that file). The first of the three short lines, line `41`, is the one
about Hack the North. That line and the block around it must never change, move or be
reformatted. Nothing about Hack the North may be added or removed. This record does
not repeat the line's text, so that the text lives only in the README, its template
and the test fixture.

## Options

For the checkers:

1. Generate this repo from the `ds-project-standard` template with `copier`. The
   template also brings a project README layout, `src/`, a model card and a datasheet,
   none of which fit a profile.
2. Write new, smaller checkers here. They would drift from the rules every other repo
   follows.
3. Copy the checker files from `ds-project-standard/tools` as they are, note the
   source commit, and add a test that fails if a copy is edited.

For the guard:

1. Compare the README with `git show fe5d040:README.md` in the test. CI clones only
   the last commit by default, so the old commit may not be there.
2. Commit a fixture copy of the old README and compare against it.

## Decision

Checkers: option 3. These files are copied byte for byte from `ds-project-standard`
at commit `602ec779782c7466703a2093832e0e091c3316b8`: `tools/_markdown.py`,
`tools/ai_signs_check.py`, `tools/readability_check.py`, `tools/claims_check.py`,
`tools/links_check.py` and `tools/lychee.toml`. `tools/readme_sections.py` is not
copied, because the profile does not use the project README layout.
`tools/SOURCE.json` records the source commit and the SHA-256 of each file, and a test
fails if any copy differs from it. `tools/README.md` says not to edit them here.

New code in this repo covers what those tools do not: numbers that come from other
repos, and the guard. It is small and lives in `scripts/`.

The gates, run in `ci.yml` on every push and pull request, and again by `sync.yml`
before it commits:

| Gate | Command, in short | Scope |
|---|---|---|
| Lint and format | `ruff check`, `ruff format --check` | `scripts/`, `tests/` |
| Types | `mypy` | `scripts/` |
| Tests | `pytest` with coverage of `scripts/` at `80%` or more, offline | `tests/` <!-- not-a-claim --> |
| Hack the North guard | `pytest tests/test_hack_the_north.py`, as its own named step | `README.md`, `README.template.md` |
| AI signs | `tools/ai_signs_check.py`, zero flags | `README.md`, `docs/` |
| Readability | `tools/readability_check.py`, grade `12` or below | `README.md`, `docs/` <!-- not-a-claim --> |
| Numbers | `scripts/check_numbers.py` ([ADR 0002](0002-where-each-number-comes-from.md)) | `README.md` |
| Claims in docs | `tools/claims_check.py` with this repo's `CLAIMS.md` | `docs/` |
| Local links | `tools/links_check.py` | `README.md`, `docs/` |
| Web links | `lychee --config tools/lychee.toml` | `README.md`, `docs/` |

The number check in CI reads the source files at the commits named in
`data/sources.json`. Those URLs never change, so the result does not depend on the
day it runs. Only lychee and this check need the network.

Guard: option 2. `tests/fixtures/readme_fe5d040.md` is an exact copy of
`git show fe5d040:README.md`. The test first checks that the fixture's SHA-256 is
`e3d9f5b99329e30eb93087f673535aa4288cd4421dafa75d7a067a5f54f64603`, so an edited
fixture fails. Then it checks, on the committed `README.md`, on `README.template.md`,
and on a fresh offline render:

1. The file contains no carriage return, so the bytes compare cleanly.
2. Line `41` of the fixture appears exactly once, as a whole line, byte for byte. Its
   SHA-256, without the newline, is
   `43601ec39830bc17c221247c1f9f440528cb226b6ebd724b5723f86c4bcfbf22`.
3. The "Also" block, lines `39` to `45` of the fixture, appears once as one unbroken
   run, byte for byte. Its SHA-256, with a newline after each line, is
   `ee0af9367052ab40a4575f4c77727eb007b4eec5e3de25dc25027805f3dd9bf7`.
4. The file ends with that block and one newline, as it does at `fe5d040`. So the
   block cannot move up the page.
5. The regular expression `hack\W*the\W*north`, ignoring case, matches exactly once.
   So nothing about it is added anywhere else in the file. The same expression must
   match nothing in `projects.toml`, `data/` or any other file the renderer writes.

The line number of the Hack the North line is not checked, because the content above
the block will change in this phase. Its place is fixed by rule 4 instead.

On top of the test, any task that commits a change to the README or its template also
compares the line with the one at `fe5d040` by hand before it commits.

## Consequences

- The writing rules here are the same rules every project repo follows.
- A newer version of the tools needs a new copy and a new `tools/SOURCE.json`, made on
  purpose.
- The guard cannot be passed by editing the fixture, and it cannot be skipped by a
  sync run, because `sync.yml` runs it before it commits.
- `make demo` and the project README layout check do not apply to this repo.
