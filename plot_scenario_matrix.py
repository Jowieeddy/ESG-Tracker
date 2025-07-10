import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_scenario_matrix(matrix_csv="scenario_matrix.csv", output_path="scenario_matrix_plot.png"):
    """Plots emissions, intensity, cost, and CO2 tax across green shift scenarios."""
    df = pd.read_csv(matrix_csv)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    plt.suptitle("Green Shift Scenario Matrix", fontsize=16, fontweight="bold")

    sns.barplot(x="Shift_%", y="Scenario_Emissions", data=df, ax=axes[0, 0], palette="Blues_d")
    axes[0, 0].set_title("Scenario Emissions (Mt CO₂)")
    axes[0, 0].set_ylabel("Emissions")

    sns.barplot(x="Shift_%", y="Emissions_Intensity", data=df, ax=axes[0, 1], palette="Greens_d")
    axes[0, 1].set_title("Emissions Intensity (Mt/TWh)")
    axes[0, 1].set_ylabel("Intensity")

    sns.barplot(x="Shift_%", y="Energy_Cost", data=df, ax=axes[1, 0], palette="Oranges_d")
    axes[1, 0].set_title("Total Energy Cost ($)")
    axes[1, 0].set_ylabel("Cost")

    sns.barplot(x="Shift_%", y="CO2_Tax_Exposure", data=df, ax=axes[1, 1], palette="Reds_d")
    axes[1, 1].set_title("CO₂ Tax Exposure ($)")
    axes[1, 1].set_ylabel("Tax")

    for ax in axes.flatten():
        ax.set_xlabel("% Gas → Renewables")
        ax.grid(True, axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(output_path, dpi=300)
    print(f"✔ Saved scenario matrix chart to {output_path}")


if __name__ == "__main__":
    plot_scenario_matrix()
