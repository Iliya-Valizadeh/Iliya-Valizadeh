# 0001: How the profile README is built and synced

Date: 2026-09-26. Status: accepted.

## Context

This repo is Iliya's GitHub profile. Until now it held one hand-typed `README.md`, so
its numbers could drift away from the project repos they describe. The portfolio plan
(section `5.6`) says the numbers must be generated, never typed. A script reads each
repo's `reports/metrics.json` from GitHub and renders the README from a template. A
GitHub Action runs it daily and on demand, and commits only when something changed.

The profile is not a website. GitHub shows `README.md` from `main`, so there is nothing
to deploy. The site repo, `Iliya-Valizadeh.github.io`, has its own build and its own
decision record.

## Options

1. A static site generator or a templating framework. It brings many packages and
   rules to learn for one Markdown file.
2. A GitHub Action from the marketplace that fills a README. Its code lives in someone
   else's repo, and it is hard to test offline.
3. One small Python script that uses only the standard library, with its own tests.

## Decision

Option 3. The pieces are:

- `README.template.md`: the README text with placeholders such as
  `{{ credit_risk_scorecard.auc }}`. The script fails on an unknown placeholder, and
  on a known value that the template never uses.
- `projects.toml`: the ordered list of repos and, for each shown number, where it comes
  from. [ADR 0002](0002-where-each-number-comes-from.md) sets the rules.
- `scripts/render_readme.py`: reads the config, fetches the source files, checks every
  number against its source repo's `CLAIMS.md`, fills the template, and writes
  `README.md` only if the text changed. It also writes `data/sources.json`, which
  records the commit of each source repo that fed the numbers. The script does no
  arithmetic other than rounding and turning a fraction into a percent.
- `--offline` makes the script read committed fixture copies in `tests/fixtures/`
  instead of the network. Tests and local checks use it.
- `.github/workflows/sync.yml`: runs on a daily schedule and on `workflow_dispatch`.
  It renders from the live files, runs the same checks as CI, and commits `README.md`
  and `data/sources.json` only when the README text changed. It uses the built-in
  `GITHUB_TOKEN` with `contents: write` and no other secret. If a check fails, it
  commits nothing and the run fails, so a person looks at it.
- `.github/workflows/ci.yml`: runs the checks in
  [ADR 0004](0004-checks-and-the-hack-the-north-guard.md) on every push and pull
  request.

Packaging follows the other repos: `pyproject.toml`, a committed `uv.lock`, and Python
`3.11`. The script needs no packages at run time. `ruff`, `mypy`, `pytest`,
`pytest-cov` and `textstat` are development packages only.

A `.gitattributes` file sets `* text=auto eol=lf`. The copy of `README.md` in the
fe5d040 commit already uses LF line endings, so this changes no committed bytes. It
stops Windows checkouts from turning the README into CRLF, which would break the byte
comparison in the Hack the North guard.

## Consequences

- One template and one config file control the whole README.
- A number changes on the profile only when its source repo changes on `main` and its
  `CLAIMS.md` row agrees.
- The sync can fail when a source repo renames a `CLAIMS.md` row. That is on purpose.
  The fix is a one-line change to `projects.toml`, made by a person.
- The live profile changes only when `phase-e-profile` is merged to `main`.
