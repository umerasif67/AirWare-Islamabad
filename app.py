from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
daily = pd.read_csv(ROOT / "daily_pollution.csv", parse_dates=["date"]).sort_values("date").set_index("date")
results = pd.read_csv(ROOT / "season_results.csv", parse_dates=["date"]).sort_values("date").reset_index(drop=True)

st.title("AirWare Islamabad")
st.subheader("Historical next-day PM2.5 prediction experiment")
st.write("Select a historical test date to inspect the model's saved prediction for the following day.")
selected = st.selectbox("Choose an input date:", results["date"].dt.strftime("%Y-%m-%d").tolist())
chosen_date = pd.Timestamp(selected)
row = results.loc[results["date"].eq(chosen_date)].iloc[0]
prediction, actual = float(row["predicted"]), float(row["tomorrow"])
baseline = float(daily.loc[chosen_date, "pm25"])
st.subheader(f"Prediction for {(chosen_date + pd.Timedelta(days=1)).date()}")
st.metric("Saved model prediction", f"{prediction:.2f} µg/m³")
st.metric("Persistence baseline", f"{baseline:.2f} µg/m³")
st.metric("Historical dataset value", f"{actual:.2f} µg/m³")
st.write(f"Model absolute error: {abs(actual - prediction):.2f} µg/m³")
st.caption("Historical Open-Meteo/CAMS model-based estimates, not ground-station measurements. Not a live forecast or health advisory.")

st.subheader("Model performance")
st.write(f"Evaluated on {len(results)} historical test examples.")
baseline_values = results["date"].map(daily["pm25"])
baseline_mae = (results["tomorrow"] - baseline_values).abs().mean()
model_mae = (results["tomorrow"] - results["predicted"]).abs().mean()
st.metric("Baseline MAE", f"{baseline_mae:.4f} µg/m³")
st.metric("Calendar-augmented model MAE", f"{model_mae:.4f} µg/m³")
chart_data = results[["date", "tomorrow", "predicted"]].copy()
chart_data["date"] += pd.Timedelta(days=1)
chart_data = chart_data.set_index("date")
chart_data.columns = ["Historical PM2.5 estimate", "Saved model prediction"]
st.line_chart(chart_data)
st.caption("Chart dates are the target day. This test set also informed model development; see README.md.")
st.info("The evaluated training code has a cosine calendar-feature limitation. This viewer uses saved test predictions to match the reported experiment. See README.md.")
st.markdown("Data: [Open-Meteo](https://open-meteo.com/en/docs/air-quality-api) and [CAMS](https://atmosphere.copernicus.eu/).")
