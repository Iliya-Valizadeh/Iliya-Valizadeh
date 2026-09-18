# Iliya Valizadeh

Third-year Data Science student at York University in Toronto, BSc expected 2028.
I build projects end to end and measure them before claiming anything about them.

**Looking for a Winter 2027 data science or analytics co-op**, January to August 2027.

## Projects

| Project | What it is | Measured result |
|---|---|---|
| [bank-filings-rag](https://github.com/Iliya-Valizadeh/bank-filings-rag) | Retrieval-augmented Q&A over RBC's 250-page 2024 annual report. Embeddings run locally so the filing never leaves the machine, every answer cites its source page, and generation is fail-closed when the retrieved evidence does not support an answer. The core of it is the evaluation harness: a hand-labelled gold set scored on hit@k and MRR, run identically across three chunking strategies. | Whole-page chunking retrieves the correct page 4x as often as fixed 180-word windows: hit@5 0.40 vs 0.10, MRR 0.27 vs 0.10 |
| [credit-risk-scorecard](https://github.com/Iliya-Valizadeh/credit-risk-scorecard) | Credit-default model on the Home Credit dataset. SQL feature pipeline in PostgreSQL, LightGBM against a class-weighted logistic baseline, then approval-threshold analysis, a calibration diagnosis traced back to class weighting, SHAP attribution, and a bank-style model-risk write-up. | LightGBM 0.736 validation ROC-AUC against a logistic baseline at 0.734, on a 17,000-row sample with a 7.85% base default rate |

Both repos state their own limitations. The numbers above come from code in the repos.
If a metric isn't in the code, I don't report it.

## Tools

Python (pandas, NumPy, scikit-learn, LightGBM), SQL and PostgreSQL, sentence-transformers
and FAISS, FastAPI, SHAP, matplotlib and seaborn, Tableau, Power BI, Git.

## Also

Sponsor prize winner, Federato challenge, Hack the North 2026 ·
DataCamp Associate Data Scientist (assessed), 2026 ·
Co-president, York University Data Science Community

iliyavalizadeh60@gmail.com · [LinkedIn](https://www.linkedin.com/in/iliya-valizadeh) · [iliya-valizadeh.github.io](https://iliya-valizadeh.github.io)
