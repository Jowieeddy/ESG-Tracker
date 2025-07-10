# summary_generator.py
import pandas as pd

def generate_summary(pivot_path="us_energy_co2_pivot.csv", forecast_csv="us_gas_forecast_with_ci.csv", output_txt="summary.txt"):
    pivot = pd.read_csv(pivot_path)
    forecast = pd.read_csv(forecast_csv)

    latest_year = pivot["Year"].max()
    last_intensity = pivot.loc[pivot["Year"] == latest_year, "Emissions_Intensity (Mt/TWh)"].values[0]

    avg_forecast_gas = forecast["Gas_Forecast_TWh"].mean()
    projected_total_energy = (
        pivot.loc[pivot["Year"] == latest_year, ["Coal (TWh)", "Renewables (TWh)"]].sum(axis=1).values[0]
        + avg_forecast_gas
    )
    projected_emissions = pivot.loc[pivot["Year"] == latest_year, "Total CO₂ (Mt)"].values[0]  # crude assumption
    projected_intensity = projected_emissions / projected_total_energy

    delta = projected_intensity - last_intensity

    with open(output_txt, "w") as f:
        f.write("📈 ESG Executive Summary\n")
        f.write(f"  Year analyzed: {latest_year}\n")
        f.write(f"  Baseline CO₂ intensity: {last_intensity:.2f} Mt/TWh\n")
        f.write(f"  Avg forecasted gas: {avg_forecast_gas:.1f} TWh\n")
        f.write(f"  Projected total energy: {projected_total_energy:.1f} TWh\n")
        f.write(f"  Estimated CO₂ intensity: {projected_intensity:.2f} Mt/TWh\n")
        f.write(f"  Δ Intensity vs. baseline: {delta:+.2f} Mt/TWh\n")

    print(f"✔ Summary saved to: {output_txt}")
