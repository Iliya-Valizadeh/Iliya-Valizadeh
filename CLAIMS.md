# Claims

This repo makes no numbers of its own. Every number in `README.md` comes from another
repo, through `scripts/render_readme.py`:

- `projects.toml` names, for each shown number, the source repo, the key in that repo's
  `reports/metrics.json`, and the row in that repo's own `CLAIMS.md` that covers it.
- The script shows a number only when that row exists, covers the key, and already
  holds the same value. Otherwise it writes nothing.
- `data/sources.json` records the commit of each source repo that fed the numbers, so
  each one can be traced by hand.

The rules are in [ADR 0002](docs/decisions/0002-where-each-number-comes-from.md).

The table below is for numbers in this repo's own docs. Small whole numbers (0 to 10),
years, dates and version numbers are skipped. To skip one line by hand, add the comment
`<!-- not-a-claim -->` to it.

| Claim | Value | Source | Command |
|---|---|---|---|
