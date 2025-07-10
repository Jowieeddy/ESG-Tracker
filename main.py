import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.api import ExponentialSmoothing # type: ignore
from statsmodels.tsa.arima.model import ARIMA # type: ignore
from sklearn.metrics import mean_absolute_error, mean_squared_error # type: ignore
from ts_diagnostics import diagnostics_decompose
from fuel_mix_share import plot_fuel_mix_share
from summary_generator import generate_summary

ENERGY_CSV = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"
CO2_CSV = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"


def load_data():
    print("↘ downloading OWID energy dataset …")
    energy = pd.read_csv(ENERGY_CSV, usecols=[
        "country", "year",
        "coal_consumption", "gas_consumption", "renewables_consumption"
    ])
    print("↘ downloading OWID CO₂ dataset …")
    co2 = pd.read_csv(CO2_CSV)
    return energy, co2


def merge_and_clean(energy, co2):
    co2_us = co2[co2["country"] == "United States"]
    energy_us = energy[energy["country"] == "United States"]

    keep_cols = {
        "coal_co2": "Coal CO₂ (Mt)",
        "gas_co2": "Gas CO₂ (Mt)",
        "other_industry_co2": "Other CO₂ (Mt)",
        "co2": "Total CO₂ (Mt)"
    }
    valid_cols = ["country", "year"] + [k for k in keep_cols if k in co2_us.columns]
    co2_us = co2_us[valid_cols].rename(columns={k: v for k, v in keep_cols.items() if k in co2_us.columns})

    merged = (
        energy_us.merge(co2_us, on=["country", "year"], how="inner")
        .dropna()
        .rename(columns={
            "year": "Year",
            "coal_consumption": "Coal (TWh)",
            "gas_consumption": "Gas (TWh)",
            "renewables_consumption": "Renewables (TWh)"
        })
        .astype({"Year": int})
        .sort_values("Year")
    )

    pivot = merged.set_index("Year")[
        [col for col in merged.columns if col.endswith("(TWh)") or col.endswith("(Mt)")]
    ]

    # Add Emissions Intensity
    if "Total CO₂ (Mt)" in pivot.columns:
        pivot["Total Electricity (TWh)"] = pivot[["Coal (TWh)", "Gas (TWh)", "Renewables (TWh)"]].sum(axis=1)
        pivot["Emissions_Intensity (Mt/TWh)"] = pivot["Total CO₂ (Mt)"] / pivot["Total Electricity (TWh)"]

    merged.to_csv("us_energy_co2_merged.csv", index=False)
    pivot.to_csv("us_energy_co2_pivot.csv")
    print("✔ saved us_energy_co2_merged.csv and us_energy_co2_pivot.csv")
    return merged, pivot

def evaluate_models(ts, train_end_year=2015):
    if not isinstance(ts.index, pd.PeriodIndex):
        ts = ts.copy()
        ts.index = pd.PeriodIndex(ts.index, freq="Y")

    years = ts.index.year
    train = ts[years <= train_end_year]
    test = ts[years > train_end_year]

    ets_model = ExponentialSmoothing(train, trend="add", seasonal=None).fit()
    arima_model = ARIMA(train, order=(1, 1, 1)).fit()

    ets_fcst = ets_model.forecast(len(test))
    arima_fcst = arima_model.forecast(len(test))

    def _metrics(actual, pred):
        mae = mean_absolute_error(actual, pred)
        rmse = np.sqrt(mean_squared_error(actual, pred))
        return mae, rmse

    ets_mae, ets_rmse = _metrics(test, ets_fcst)
    arima_mae, arima_rmse = _metrics(test, arima_fcst)

    results = {
        "ETS": {"mae": ets_mae, "rmse": ets_rmse, "model": ets_model},
        "ARIMA": {"mae": arima_mae, "rmse": arima_rmse, "model": arima_model}
    }

    return results, test


def forecast_gas(ts):
    evals, _ = evaluate_models(ts)

    best_name = min(evals, key=lambda k: evals[k]["rmse"])
    best_model = evals[best_name]["model"]
    forecast = best_model.forecast(5)

    resid_std = (ts - best_model.fittedvalues).std()
    ci_upper = forecast + 1.96 * resid_std
    ci_lower = forecast - 1.96 * resid_std

    print(f"\nModel comparison (test window):")
    for k, v in evals.items():
        print(f"  {k:5}  MAE={v['mae']:.1f}  RMSE={v['rmse']:.1f}")
    print(f"▶  Selected model: {best_name}")

    return forecast, ci_lower, ci_upper


def plot_energy_forecast(pivot, forecast, ci_lower, ci_upper):
    plt.figure(figsize=(10, 6))
    for col in ["Coal (TWh)", "Gas (TWh)", "Renewables (TWh)"]:
        plt.plot(pivot.index, pivot[col], label=col.replace(" (TWh)", ""))

    forecast_index = pd.period_range(start=pivot.index[-1] + 1, periods=5, freq="Y")
    plt.plot(forecast_index.year, forecast.values, "r--", label="Gas Forecast", lw=2)
    plt.fill_between(forecast_index.year, ci_lower, ci_upper, color="red", alpha=0.15, label="95% CI")

    plt.title("U.S. Energy Consumption by Source (5-yr Gas Forecast + CI)")
    plt.xlabel("Year")
    plt.ylabel("TWh")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    out = pd.DataFrame({
        "Year": forecast_index,
        "Gas_Forecast_TWh": forecast.values,
        "CI_Lower": ci_lower.values,
        "CI_Upper": ci_upper.values
    })
    out.to_csv("us_gas_forecast_with_ci.csv", index=False)
    print("✔ saved us_gas_forecast_with_ci.csv")


import argparse
from scenario_model import simulate_green_shifts

def run_pipeline(args):
    energy, co2 = load_data()
    merged, pivot = merge_and_clean(energy, co2)

    gas_ts = pivot["Gas (TWh)"].dropna()
    gas_ts.index = pd.PeriodIndex(gas_ts.index, freq="Y")

    if not args.skip_plots:
        diagnostics_decompose(gas_ts, model_name="Gas")

    forecast, ci_lo, ci_hi = forecast_gas(gas_ts)

    if not args.skip_plots:
        plot_energy_forecast(pivot, forecast, ci_lo, ci_hi)
        plot_fuel_mix_share(pivot)

    if not args.skip_summary:
        generate_summary()

    if args.scenario:
        print("▶ Running simulate_green_shifts()...")
        simulate_green_shifts(shift_levels=[args.scenario / 100])
        print("✔ Finished simulate_green_shifts()")

    elif not args.only_baseline:
        print("▶ Running simulate_green_shifts() with default shift levels...")
        simulate_green_shifts()
        print("✔ Finished simulate_green_shifts()")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="U.S. Energy & Emissions Forecasting Tool")
    parser.add_argument("--scenario", type=int, help="Run scenario with specified percent green shift (e.g., 10 for 10%)")
    parser.add_argument("--skip-plots", action="store_true", help="Skip generating plots")
    parser.add_argument("--skip-summary", action="store_true", help="Skip generating textual summaries")
    parser.add_argument("--only-baseline", action="store_true", help="Run baseline only without scenario modeling")
    
    args = parser.parse_args()
    run_pipeline(args)
