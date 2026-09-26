# Iliya Valizadeh

Data science that shows its work.

I study Data Science (BSc) at York University in Toronto. I'm in my third year and I
graduate in April 2028. I'm looking for a Winter 2027 data science or analytics co-op.
I'm not in York's formal co-op stream, but my program allows work terms of up to
twelve months.

## Projects

In the three data projects, every number traces back to the script that made it. Each
of them also records its design choices and has a page on what is weak. The other two
repos hold the template and the shared files that make this the default. A script
fills in the numbers below from each repo's results, and only if its `CLAIMS.md` lists them.

| Project | What it is | Most interesting finding | Headline number |
|---|---|---|---|
| [credit-risk-scorecard](https://github.com/Iliya-Valizadeh/credit-risk-scorecard) | A model that ranks loan applicants by the risk that they miss payments, then turns that score into a probability. It uses the public Home Credit data from Kaggle. | The class weighting I chose made the raw probabilities far too high. Calibrating on held-out data fixed them and left the ranking almost the same. Taking gender out of the model narrowed the gap in declines between men and women, but did not close it, because other inputs still carry gender. | How well it ranks risky applicants above safe ones ([ROC-AUC](https://github.com/Iliya-Valizadeh/credit-risk-scorecard/blob/main/docs/glossary.md#roc-auc)): 0.769 (interval 0.762 to 0.775), against 0.752 for a logistic regression baseline |
| [bank-filings-rag](https://github.com/Iliya-Valizadeh/bank-filings-rag) | Answers questions about RBC's 2024 Annual Report and names the page each answer came from. The text is turned into vectors on my own machine, not sent to a hosted service. | The model that turns text into vectors reads only the start of each page, and most pages are much longer than that. So search by meaning over whole pages mostly sees the top of each page. A model that reads more could change which setup wins. | How often the right page is in the top five ([hit@5](https://github.com/Iliya-Valizadeh/bank-filings-rag/blob/main/docs/glossary.md#hit5)): 0.58 (95% interval 0.33 to 0.83) on 12 hand-checked questions, against 0.25 (0.00 to 0.50) for fixed-size chunks. The intervals overlap, so no setup clearly wins yet |
| [second-look](https://github.com/Iliya-Valizadeh/second-look) | Reads a bank or card statement in your browser and flags charges worth a second look: subscriptions, price rises, double charges and odd spending. Each flag comes with one plain sentence. | It failed the bar I set before I saw any result. After two fixes, two checks still fall short, including the share of recurring flags that are right. The repo reports that instead of moving the bar. | Share of planted recurring charges it finds ([recall](https://github.com/Iliya-Valizadeh/second-look/blob/main/docs/glossary.md#recall)), on synthetic statements only: 0.9588 (95% interval 0.9467 to 0.9695), against 0.7772 for a simple baseline |
| [ds-project-standard](https://github.com/Iliya-Valizadeh/ds-project-standard) | A Copier template that gives each new data science repo the same docs, tests and CI checks. A build stops when a number has no source, a page is hard to read, or a link is broken. | It scores itself zero overall on the ML Test Score, a published checklist of how ready a system is for real use. The score page says why. | None. It holds rules and templates, not a model |
| [.github](https://github.com/Iliya-Valizadeh/.github) | Shared issue forms, a pull request checklist and a security policy. GitHub uses them for any of my repos that has no copy of its own. | GitHub does not share a license from this repo the way it shares the forms, so each repo keeps its own license file. | None. It holds rules and templates, not a model |

## How I work

- I now write down how a project will be judged before I see any results. The second-look [evaluation plan](https://github.com/Iliya-Valizadeh/second-look/blob/main/docs/eval_plan.md) was committed before any evaluation code.
  My two older projects got their plans later, and each plan says so in its title ([example](https://github.com/Iliya-Valizadeh/credit-risk-scorecard/blob/main/docs/eval_plan.md)).
- Every number has a source. Each data project has a `CLAIMS.md` that links each number to the file and command that made it ([example](https://github.com/Iliya-Valizadeh/credit-risk-scorecard/blob/main/CLAIMS.md)).
  CI fails when a number in the docs has no row there ([the check](https://github.com/Iliya-Valizadeh/ds-project-standard/blob/main/tools/claims_check.py)).
- I say what is weak before a reader finds it.
  Each data project ranks its limits by how much they could change the result ([example](https://github.com/Iliya-Valizadeh/second-look/blob/main/docs/whats_weak.md)).

## Tools

Python (pandas, NumPy, scikit-learn, LightGBM), SQL and PostgreSQL, sentence-transformers
and FAISS, SHAP, matplotlib and seaborn, Tableau, Power BI, Git.

## Also

Sponsor prize, Federato challenge at Hack the North 2026 ·
DataCamp Associate Data Scientist (assessed), 2026 ·
Co-president, York University Data Science Community

iliyavalizadeh60@gmail.com · [LinkedIn](https://www.linkedin.com/in/iliya-valizadeh) · [iliya-valizadeh.github.io](https://iliya-valizadeh.github.io)
