# 🌍 ESG Tracker – Energy Forecasting & Emissions Scenario Simulator

**ESG Tracker** is a data-driven Python tool that forecasts U.S. gas consumption using time series models (ETS & ARIMA), visualizes fuel mix trends, and simulates the impact of green energy shifts on carbon emissions, energy costs, and CO₂ tax exposure. Built with clean CLI interactivity and automation in mind.

---

## 🔍 Features

- 📈 **Forecast U.S. Gas Consumption** – Using ETS & ARIMA models
- 🌿 **Simulate Green Scenarios** – Shift % of gas energy to renewables and see impact
- 💸 **Estimate Energy Costs & CO₂ Tax Exposure**
- 📊 **Visualize Fuel Mix Changes & Emissions Intensity**
- ✅ **Command-Line Interface** – Run targeted scenarios using CLI flags
- 📁 **Outputs clean summary reports, CSVs, and plots**

---

## 🧪 Sample Scenario (10% Green Shift)

```
▶ Running simulate_green_shifts()...
✔ Saved matrix to scenario_matrix.csv
✔ Updated summary in scenario_summary.txt

🌿 Green Shift Scenario Summary (10% Gas → Renewables)
  Δ Emissions: -327.4 Mt CO₂
  Estimated Savings: $15,970
  Δ Tax Exposure: $32,739
```

---

## 🚀 How to Run

1. **Clone the repo**:
   ```bash
   git clone https://github.com/Jowieeddy/ESG-Tracker.git
   cd ESG-Tracker
   ```

2. **Install dependencies** (use a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the forecasting pipeline**:
   ```bash
   python main.py
   ```

4. **Run a scenario shift** (e.g., 10% gas to renewables):
   ```bash
   python main.py --scenario 10
   ```

---

## 🛠 CLI Options

| Flag                | Description                                      |
|---------------------|--------------------------------------------------|
| `--scenario <int>`  | Run a green shift scenario (e.g. `--scenario 10`) |
| `--skip-plots`      | Skip generating diagnostic plots                  |
| `--skip-summary`    | Skip writing `summary.txt`                        |
| `--only-baseline`   | Run baseline forecast only, no scenarios         |

---

## 📂 Project Structure

```
ESG-Tracker/
│
├── main.py                    # Main forecasting pipeline
├── scenario_model.py          # Green shift simulation logic
├── plot_scenario_matrix.py    # Visual plots of shift impact
├── summary_generator.py       # Emissions and cost summary writer
├── ts_diagnostics.py          # Time series diagnostics
├── fuel_mix_share.py          # Fuel mix share visualizer
│
├── scenario_matrix.csv        # Output: scenario grid (auto-generated)
├── scenario_summary.txt       # Output: scenario summary (auto-generated)
├── summary.txt                # Output: emissions summary (auto-generated)
├── .gitignore
└── README.md
```

---

## 📊 Plots & Outputs

- `fuel_mix_share.png`
- `gas_acf_pacf.png`
- `scenario_matrix.csv`
- `summary.txt`
- `scenario_summary.txt`

---

## ✨ Coming Soon

- Interactive dashboard via Streamlit or Gradio
- Enhanced forecasting models (Prophet, LSTM)
- International energy datasets

---

## 👤 Author

Joseph Ugbechie – [@Jowieeddy](https://github.com/Jowieeddy)

---

## 📄 License

MIT License – use freely with attribution.