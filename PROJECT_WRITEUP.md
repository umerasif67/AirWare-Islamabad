# AirWare Islamabad — Veritas AI hackathon write-up

**Problem.** Explore whether recent particulate pollution history can predict the next day's PM2.5 daily mean for Islamabad using a small, explainable model.

**Data.** A supplied Open-Meteo hourly air-quality export is aggregated into 1,400 daily means, from 1 January 2023 to 31 October 2026. These are model-based estimates, not ground-station observations. The original request URL and download time were not retained.

**Approach.** Persistence predicts tomorrow equals today. A scikit-learn linear regression uses today's PM2.5 and the previous two days; a second model adds calendar features. Chronological splitting gives 1,116 training examples and 280 test examples with one boundary row excluded. Test input dates are 24 January–30 October 2026, predicting the following day.

**Measured results.** Baseline MAE: **5.4355208333333325 µg/m³**. Original regression MAE: **5.283313037391308 µg/m³**. Calendar-augmented model MAE: **5.227294943483615 µg/m³**, approximately **3.83% below baseline**, over 280 examples. Baseline and saved-model MAE were recomputed from supplied CSVs; the original regression score is from recorded training output.

**Demo.** Judges can select a historical input date in Streamlit, compare its saved next-day prediction with persistence and the historical dataset value, and view all 280 predictions on a chart. This is a historical evaluation viewer, not a live service. The repository includes data and local run instructions.

**Limitations.** The training cosine formula omits division by 365.25 and is effectively constant for integer days. The measured experiment is preserved and disclosed; a corrected version has not been evaluated here. The test result informed calendar-feature development, so this is not a final untouched validation set. The gain is modest; no significance or uncertainty estimate was calculated. Sudden spikes remain difficult. Future work includes corrected calendar features, weather inputs, fresh time-based evaluation and ground-station validation.

**Credits.** [Open-Meteo](https://open-meteo.com/en/docs/air-quality-api) and CAMS supply the underlying model-based data; full attribution and provenance limits are in the README. Tools: [scikit-learn](https://scikit-learn.org/stable/), [Streamlit](https://docs.streamlit.io/), [pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/) and [joblib](https://joblib.readthedocs.io/en/stable/). [ChatGPT](https://chatgpt.com/) assisted with project guidance, code/debugging explanations and submission preparation. Codex assisted with repository preparation, checks and documentation.
**Intended user and impact**

AirWare Islamabad is designed as a research prototype for school administrators in Islamabad who want to explore whether next-day air pollution forecasting could help inform outdoor activity planning. The current system demonstrates historical predictions and is not validated for real-time health decisions.

**Our contribution and model limitations**

We tested whether adding calendar information to a model using recent pollution history improved predictions. The resulting model reduced MAE by approximately 3.83% against the persistence baseline. However, it struggled with sudden pollution changes. For example, for May 30, 2026, it predicted 31.51 µg/m³ against a historical estimate of 56.33 µg/m³. The original cosine feature also contains a documented implementation error.
