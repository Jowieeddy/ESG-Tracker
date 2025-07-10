import pandas as pd
import matplotlib.pyplot as plt

def plot_scenario_matrix(csv_path="scenario_matrix.csv", save_path="scenario_matrix_plot.png"):
    # Load the scenario matrix
    df = pd.read_csv(csv_path)

    # Convert Shift_% to string for better x-axis labeling
    df["Shift_%"] = df["Shift_%"].astype(str) + "%"

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Bar chart for CO₂ Emissions Reduction
    ax1.bar(df["Shift_%"], df["Delta_Emissions"], color="green", alpha=0.6, label="Δ Emissions (Mt CO₂)")
    ax1.set_ylabel("Emissions Reduction (Mt CO₂)", color="green")
    ax1.tick_params(axis='y', labelcolor="green")
    ax1.set_xlabel("Green Shift Scenario")

    # Create second axis for energy cost and tax exposure
    ax2 = ax1.twinx()
    ax2.plot(df["Shift_%"], df["Energy_Cost"], color="blue", marker='o', label="Energy Cost ($)")
    ax2.plot(df["Shift_%"], df["CO2_Tax_Exposure"], color="red", marker='x', label="CO₂ Tax Exposure ($)")
    ax2.set_ylabel("Cost ($)", color="black")
    ax2.tick_params(axis='y', labelcolor="black")

    # Title and legend
    plt.title("Green Shift Scenario Outcomes")
    fig.legend(loc="upper center", bbox_to_anchor=(0.5, 1.08), ncol=3)
    fig.tight_layout()
    plt.grid(True)
    plt.savefig(save_path)
    print(f"✔ Saved plot to {save_path}")
    plt.close()

if __name__ == "__main__":
    plot_scenario_matrix()
