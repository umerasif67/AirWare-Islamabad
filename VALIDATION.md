# Submission preparation checks

Checked on 15 November 2026:

- Re-ran the unchanged supplied `train.py` against a copy of `daily_pollution.csv` in a separate verification folder. Output matched all three reported MAEs exactly: baseline 5.4355208333333325, original regression 5.283313037391308, calendar-augmented model 5.227294943483615. Training count 1,116; test count 280.
- Independently recomputed baseline and saved-model MAE from the supplied CSVs. All 280 saved next-day targets matched the daily dataset, and all stored absolute errors matched their predictions and targets within 1e-10.
- Ran the published `app.py` with Streamlit's AppTest. It completed with no app exceptions, exposed 280 date options and displayed MAEs 5.4355 and 5.2273. Its initial example displayed saved prediction 30.60, persistence 26.74 and historical target 48.03 µg/m³.
- Checked project text files for credential patterns, personal contact details and local-machine paths; none found. Original source files were left unchanged. Only explicitly selected project files are uploaded.
- Opened the cited official documentation without the user's signed-in session. The CAMS dataset landing page timed out in the initial check; its link is present in the Open-Meteo documentation. Other cited documentation pages loaded.

Verification environment: Python 3.14.8, pandas 3.1.1, NumPy 2.5.4, scikit-learn 1.9.1, joblib 1.6.0, Streamlit 1.67.0. These are the versions observed during preparation, not a claim about the earlier training environment. Requirements pin scikit-learn to the version recorded in the supplied model; other dependencies are unpinned.

This validation preserves the original calendar-feature formula and its limitation described in the README. It does not establish real-world forecast reliability or evaluate a corrected seasonal model.
