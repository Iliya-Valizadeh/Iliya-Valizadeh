# 0002: Where each number on the profile comes from

Date: 2026-09-26. Status: accepted.

## Context

Every number in this portfolio must trace to a committed script through a `CLAIMS.md`
row. The profile makes no numbers of its own. It shows numbers that other repos make
and already list in their own `CLAIMS.md`. Two of the five repos,
`ds-project-standard` and `.github`, have no `reports/metrics.json`, because they hold
rules and templates, not a model.

## Options

1. Copy the numbers into this repo by hand. They drift, and nothing checks them.
2. Read each repo's JSON file and trust it. A number could then appear on the profile
   that its own repo never claims.
3. Read each repo's JSON file and its `CLAIMS.md` from the same commit, and show a
   number only when both agree.

## Decision

Option 3, with these rules.

Fetching:

- For each repo, `git ls-remote https://github.com/Iliya-Valizadeh/<repo> refs/heads/main`
  gives the current commit of `main`. No key and no API call are needed.
- The script then reads `https://raw.githubusercontent.com/Iliya-Valizadeh/<repo>/<commit>/<file>`
  for the JSON file and for `CLAIMS.md`. Both come from the same commit, so they
  cannot disagree because one was read a moment later than the other.
- The script uses no key, token or paid API. The repos are public.

Each shown number has one entry in `projects.toml` with:

- `id`: the placeholder name used in the template
- `repo` and `file`: which JSON file on that repo's `main`
- `path`: the dotted key inside that file
- `row`: the exact text of the Claim cell in that repo's `CLAIMS.md`
- `format`: how many decimals, whether it is shown as a percent, and whether it has a
  thousands comma

The check, for every entry:

1. The row named by `row` exists in the source repo's `CLAIMS.md`.
2. That row's Source cell names the same file, and its `#key`, if it has one, is the
   start of `path`. So the row really covers this value.
3. The formatted value equals a number in that row's Value cell, using the same number
   matching as the vendored `tools/claims_check.py`.

If any step fails, the script writes nothing and exits with an error.

The planned numbers for the five rows are below. Values are left out of this record on
purpose, because they live in the source repos and can change there.

| Repo | Shown number | File and path | `CLAIMS.md` row (Claim cell) |
|---|---|---|---|
| `credit-risk-scorecard` | LightGBM ROC-AUC, 95% interval, baseline | `reports/metrics.json`: `models.lightgbm.roc_auc`, `bootstrap.roc_auc.lightgbm.lo`, `bootstrap.roc_auc.lightgbm.hi`, `models.logreg.roc_auc` | "ROC-AUC and PR-AUC by model, with 95% intervals" <!-- not-a-claim --> |
| `bank-filings-rag` | hit@5 with its interval, and the baseline with its interval | `reports/metrics.json`: `headline.model.value`, `headline.model.ci_low`, `headline.model.ci_high`, and the same three under `headline.baseline` | "Headline hit@5, whole pages + hybrid, ..." and "Baseline hit@5, fixed chunks + dense, ..." |
| `bank-filings-rag` | number of hand-checked questions | `reports/metrics.json`: `n_questions.verified` | "Hand-checked questions" |
| `second-look` | recurring recall with its interval, and the baseline | `reports/metrics.json`: `engine.recurring.recall.value`, `.ci_low`, `.ci_high`, `baseline.recurring.recall.value` | "Recurring recall" and "Baseline recurring precision and recall" |
| `ds-project-standard` | none | none | none |
| `.github` | none | none | none |

The "..." stands for the rest of the Claim cell, which `projects.toml` spells out in
full.

Special rules:

- A repo entry with `metrics = false` cannot have number entries. The script refuses
  to render one. Its row in the table shows words, never a number. These two repos are
  shown with no headline number, and none is ever invented for them.
- Every `second-look` number measured on its synthetic test statements is marked
  `synthetic = true` in the config. A test fails if such a number appears in a table cell or sentence without the word "synthetic".
- The README may not contain a number that did not come from a placeholder. The check
  uses the number rules of `tools/claims_check.py` (years, dates and whole numbers up
  to ten are skipped). A typed number fails the build.
- A number with no `CLAIMS.md` row in its own repo is left out of the profile and
  logged in `_portfolio/STATUS.md`. This phase adds no rows to other repos.

Today's README has three numbers that no source row backs: the page count of the
annual report, the `21 of 30` count, and the Brier score cut given as a percent. The
content task drops or rewords them. It does not compute them.

## Consequences

- `data/sources.json` names the source commit of every shown number, so any number can
  be traced by hand: this repo, then the source repo at that commit, then its
  `CLAIMS.md` row, then the script that made it.
- This repo's own `CLAIMS.md` says that the profile makes no numbers and points to
  `projects.toml` and `data/sources.json`.
- The fetching, row matching and number formatting are written here first, in
  `scripts/`. The site repo copies them and records this repo's commit, so the site
  and the profile follow one rule.
- Offline tests use copies of the source files from these commits, recorded in
  `tests/fixtures/SOURCES.md`: `credit-risk-scorecard` at `35a17fd`, `bank-filings-rag`
  at `45246f8`, `second-look` at `0da821d`.
