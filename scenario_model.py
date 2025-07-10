import pandas as pd

def simulate_green_shifts(
    pivot_path="us_energy_co2_pivot.csv",
    forecast_csv="us_gas_forecast_with_ci.csv",
    output_txt="scenario_summary.txt",
    matrix_csv="scenario_matrix.csv",
    gas_co2_factor=0.41,  # Mt/TWh
    co2_tax=100,          # $/Mt
    gas_cost=60,          # $/MWh
    renew_cost=40,        # $/MWh
    shift_levels=[0.05, 0.10, 0.20, 0.30]
):
    pivot = pd.read_csv(pivot_path)
    forecast = pd.read_csv(forecast_csv)

    latest_year = pivot["Year"].max()
    gas_forecast = forecast["Gas_Forecast_TWh"].values
    renew_base = pivot.loc[pivot["Year"] == latest_year, "Renewables (TWh)"].values[0]

    baseline_emissions = gas_forecast * gas_co2_factor
    baseline_energy = gas_forecast + renew_base
    baseline_intensity = baseline_emissions.mean() / baseline_energy.mean()
    baseline_tax = baseline_emissions.mean() * co2_tax
    baseline_cost = gas_forecast.mean() * gas_cost

    summary_lines = []
    matrix = []

    for pct in shift_levels:
        gas_shifted = gas_forecast * (1 - pct)
        renew_shifted = renew_base + (gas_forecast * pct)
        scenario_energy = gas_shifted + renew_shifted
        scenario_emissions = gas_shifted * gas_co2_factor
        scenario_intensity = scenario_emissions.mean() / scenario_energy.mean()
        scenario_tax = scenario_emissions.mean() * co2_tax
        scenario_cost = (gas_shifted.mean() * gas_cost) + ((gas_forecast.mean() * pct) * renew_cost)

        delta_emissions = scenario_emissions.mean() - baseline_emissions.mean()
        delta_intensity = scenario_intensity - baseline_intensity
        delta_cost = baseline_cost - scenario_cost
        delta_tax = baseline_tax - scenario_tax

        # Append to matrix
        matrix.append([
            int(pct * 100),
            scenario_emissions.mean(),
            delta_emissions,
            scenario_intensity,
            scenario_cost,
            scenario_tax
        ])

        # Build readable summary line
        summary_lines.append(
            f"{int(pct*100):>2}% shift → Δ Emissions: {delta_emissions:+.1f} Mt CO₂, "
            f"Δ Intensity: {delta_intensity:+.3f}, "
            f"Savings: ${delta_cost:,.0f}, "
            f"Tax Δ: ${delta_tax:,.0f}"
        )

    # Save summary
    with open(output_txt, "w") as f:
        f.write("🌿 Green Shift Scenario Comparison\n\n")
        f.write(f"Baseline Gas Forecast: {gas_forecast.mean():.1f} TWh\n")
        f.write(f"Baseline Emissions: {baseline_emissions.mean():.1f} Mt CO₂\n")
        f.write(f"Baseline Intensity: {baseline_intensity:.3f} Mt/TWh\n")
        f.write(f"Baseline Cost: ${baseline_cost:,.0f}\n")
        f.write(f"Baseline CO₂ Tax: ${baseline_tax:,.0f}\n\n")
        f.write("Scenario Comparisons:\n")
        f.write("\n".join(summary_lines))
        f.write("\n")

    # Save matrix as CSV
    matrix_df = pd.DataFrame(matrix, columns=[
        "Shift_%", "Scenario_Emissions", "Delta_Emissions",
        "Emissions_Intensity", "Energy_Cost", "CO2_Tax_Exposure"
    ])
    matrix_df.to_csv(matrix_csv, index=False)
    print(f"✔ Saved matrix to {matrix_csv}")
    print(f"✔ Updated summary in {output_txt}")
