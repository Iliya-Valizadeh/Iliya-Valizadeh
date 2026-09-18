# Iliya Valizadeh

Third-year Data Science student at York University in Toronto, BSc expected 2028.
Looking for a Winter 2027 data science or analytics co-op, January to August 2027.

Two projects below. Every number in them was produced by code in the repo, and if a
metric isn't in the code I don't report it.

## [bank-filings-rag](https://github.com/Iliya-Valizadeh/bank-filings-rag)

Ask a question about RBC's 2024 Annual Report and get an answer back with the page it
came from. The report runs to 250 pages. The text is turned into vectors on my own
machine rather than sent to a hosted API, so the same design would still work on a
document a bank could not send outside. When the pages it pulled do not contain the
answer, it says so instead of guessing.

The testing is where most of the work went. I wrote an answer key by hand, with the true
page for each question, and used it to compare three ways of splitting the report.
Splitting it one page at a time found the right page in the top five 4 times out of 10,
against 1 time out of 10 for fixed 180-word chunks. The answer key is only 10 questions,
so that points in a direction rather than settling anything, and the repo says as much.

## [credit-risk-scorecard](https://github.com/Iliya-Valizadeh/credit-risk-scorecard)

A credit default model on the public Home Credit dataset. Feature pipeline in SQL on
PostgreSQL, then LightGBM at 0.736 ROC-AUC against a logistic regression baseline at
0.734, trained on a 17,000-row sample in which 7.85% of applicants defaulted.

The model score is the smaller half of it. I mapped how many real defaulters you catch
against how many good customers you turn away at each cut-off, found my predicted
probabilities were overstated and traced that back to the class weighting I had added
myself, used SHAP to check which features the model was leaning on, and wrote up the
intended use, the failure modes and when it would need retraining. The limitations are
listed in the repo, including the ones that are not flattering.

## Tools

Python (pandas, NumPy, scikit-learn, LightGBM), SQL and PostgreSQL, sentence-transformers
and FAISS, FastAPI, SHAP, matplotlib and seaborn, Tableau, Power BI, Git.

## Also

Sponsor prize, Federato challenge at Hack the North 2026 ·
DataCamp Associate Data Scientist (assessed), 2026 ·
Co-president, York University Data Science Community

iliyavalizadeh60@gmail.com · [LinkedIn](https://www.linkedin.com/in/iliya-valizadeh) · [iliya-valizadeh.github.io](https://iliya-valizadeh.github.io)
