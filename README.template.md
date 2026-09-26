# Iliya Valizadeh

Third-year Data Science student at York University in Toronto, BSc expected 2028.
Looking for a Winter 2027 data science or analytics co-op, January to August 2027.

Two projects below. Every number in them was produced by code in the repo, and if a
metric isn't in the code I don't report it.

## [bank-filings-rag](https://github.com/Iliya-Valizadeh/bank-filings-rag)

Ask a question about RBC's 2024 Annual Report (250 pages) and get an answer back with
the page it came from. The text is turned into vectors on my own machine rather than
sent to a hosted API, and when the pages it pulled don't contain the answer, it says so.

Most of the work went into measuring it. I built a 30-question answer key and compared
three ways of splitting the report against three ways of searching it, with bootstrap
intervals and a write-up of every miss. The best setup, whole pages searched by meaning
and by keyword together, found the right page in the top five for 21 of 30 questions.
Only {{ bank_filings_rag.n_verified }} of those questions are checked by hand so far, and on those {{ bank_filings_rag.n_verified }} the intervals are
too wide to rank the setups. The repo says so up front.

## [credit-risk-scorecard](https://github.com/Iliya-Valizadeh/credit-risk-scorecard)

A credit default model on the public Home Credit dataset, trained on all 307,511
applications. LightGBM reaches {{ credit_risk_scorecard.lightgbm_roc_auc }} ROC-AUC against {{ credit_risk_scorecard.logreg_roc_auc }} for a logistic regression
baseline, and a paired bootstrap puts the gap at 0.013 to 0.020.

The model score is the smaller half of it. The class weighting I added made the average
predicted default rate 40% when the real rate is 8%. Calibrating on held-out data brought
it to 8.0% and cut the Brier score by 64%. I also took gender out of the model and
measured what changed. The gap in declines between men and women narrowed but didn't
close, because other inputs still carry gender, and the repo names them.

## Tools

Python (pandas, NumPy, scikit-learn, LightGBM), SQL and PostgreSQL, sentence-transformers
and FAISS, SHAP, matplotlib and seaborn, Tableau, Power BI, Git.

## Also

Sponsor prize, Federato challenge at Hack the North 2026 ·
DataCamp Associate Data Scientist (assessed), 2026 ·
Co-president, York University Data Science Community

iliyavalizadeh60@gmail.com · [LinkedIn](https://www.linkedin.com/in/iliya-valizadeh) · [iliya-valizadeh.github.io](https://iliya-valizadeh.github.io)
