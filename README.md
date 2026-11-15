# AirWare Islamabad

Veritas AI hackathon project: a historical next-day PM2.5 prediction experiment for Islamabad, with a Streamlit viewer of held-out predictions. This is a historical demonstration, not a live forecast or a health advisory.

## Data and method

The supplied Open-Meteo CSV contains hourly model-based PM2.5 estimates for an Islamabad grid cell (33.700005 N, 73.0 E), in Asia/Karachi time, from 1 January 2023 through 31 October 2026. `explore.py` computes arithmetic daily means, producing 1,400 days. These estimates are not ground-station measurements. The original API request URL and download timestamp were not retained; exact retrieval settings cannot be reconstructed from these files.

`train.py` sorts chronologically and predicts the next day's daily mean from today's PM2.5 and the previous two days. A second linear regression adds calendar features. After dropping missing shifted rows, `split = int(len(df) * 0.8)`, `train = df.iloc[:split-1]` and `test = df.iloc[split:]` produce 1,116 training examples, one excluded boundary row and 280 test examples. Test input dates run from 24 January to 30 October 2026; target dates are one day later. The persistence baseline predicts tomorrow equals today.

## Measured results

Mean absolute error (MAE), in µg/m³; lower is better. All scores use the same 280 test examples.

| Method | MAE (µg/m³) |
| --- | ---: |
| Persistence baseline | 5.4355208333333325 |
| Original linear regression | 5.283313037391308 |
| Calendar-augmented model (originally called seasonal) | 5.227294943483615 |

The calendar-augmented model reduces MAE by approximately 3.83% relative to baseline. Baseline and saved seasonal MAE were independently recomputed from the CSVs during repository preparation. The original regression score comes from the recorded training output; its predictions were not saved separately.

### Seasonal-feature limitation

The evaluated training code uses `sin(2*pi*day/365.25)` but `cos(2*pi*day)` without division by 365.25. For integer days the cosine is effectively constant, so this is not a correctly implemented sine/cosine seasonal pair. The supplied model and measured results are preserved as the actual experiment. Fixing the formula requires retraining and new evaluation; no corrected-model score is claimed. The published app displays saved test predictions, avoiding the original app's different cosine formula producing inconsistent predictions.

## Run

Run from the repository folder with Python and pip:

```sh
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Select a historical input date to compare the saved prediction with persistence and the historical dataset value. The chart covers all 280 examples and labels the target day. No API key or sign-in is needed. A public hosted demo has not been deployed; judges can download and run this repository locally.

To reproduce preprocessing and training (overwrites generated data, model and results):

```sh
python explore.py
python train.py
```

The supplied model records scikit-learn 1.9.1, pinned in requirements. Other original dependency versions were not captured; exact floating-point results may vary by environment. Only deserialize trusted pickle/joblib files. The demo reads CSV predictions and does not need to deserialize the model.

## Files

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit historical evaluation viewer |
| `explore.py` | Hourly-to-daily aggregation |
| `train.py` | Baseline and two regression evaluations |
| `islamabad_pm25.csv.csv` | Supplied hourly export; original filename retained |
| `daily_pollution.csv` | Daily means |
| `season_results.csv` | Test targets, predictions and errors; date is the input day |
| `season_model.pkl` | Supplied trained model |
| `PROJECT_WRITEUP.md` | Short submission write-up |

## Limitations and next steps

The gain is modest and based on one chronological holdout. Calendar features were tried after inspecting the original test result, so this test set also informed development and is not a final untouched validation set. No uncertainty interval or statistical significance was measured. Sudden pollution spikes can be missed. No weather, emissions, traffic or ground-station inputs are used; daily means hide hourly peaks. Next steps are correcting the cosine feature, rolling time splits plus a fresh untouched holdout, and validation against ground-station observations.

## Sources, tools and AI assistance

- Data: [Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api), with acknowledgement to the Copernicus Atmosphere Monitoring Service (CAMS). Open-Meteo documents [CAMS global atmospheric composition forecasts](https://ads.atmosphere.copernicus.eu/datasets/cams-global-atmospheric-composition-forecasts) and requests attribution to the [CAMS ENSEMBLE data providers](https://confluence.ecmwf.int/display/CKB/CAMS+Regional%3A+European+air+quality+analysis+and+forecast+data+documentation). Exact historical export settings were not retained. See [Open-Meteo data licence](https://open-meteo.com/en/licence). Daily aggregation and ML predictions are project transformations of the supplied data.
- [scikit-learn](https://scikit-learn.org/stable/): regression and MAE evaluation.
- [Streamlit](https://docs.streamlit.io/): demonstration interface.
- [pandas](https://pandas.pydata.org/): data processing and daily aggregation.
- [NumPy](https://numpy.org/): numerical and calendar calculations.
- [joblib](https://joblib.readthedocs.io/en/stable/): model serialization.
- [ChatGPT by OpenAI](https://chatgpt.com/): project guidance, code/debugging explanations and submission preparation. Codex assisted with repository preparation, consistency checks and documentation. This is an AI-assisted project; no claim of entirely unaided authorship is made.

## Privacy and access

Only project code, environmental datasets, the supplied model and documentation are included. Text files were checked for credentials, personal contact details and local-machine paths; none were found. Raw CSV coordinates describe an environmental grid cell, not a claimed personal location. No private chats, screenshots, browser data or local configuration files are included. Upstream dependency licences and data terms remain applicable; this repository does not relicense those materials.
