from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt

DEFAULT_PIVOT = Path("us_energy_co2_pivot.csv")


def plot_fuel_mix_share(pivot: pd.DataFrame, save_png: bool = True) -> None:
    """Plot % share of Coal, Gas, Renewables over time and optionally save PNG."""
    share = pivot[["Coal (TWh)", "Gas (TWh)", "Renewables (TWh)"]].copy()
    share = share.div(share.sum(axis=1), axis=0) * 100  # to percent

    ax = share.plot.area(figsize=(10, 6), stacked=True, alpha=0.8)
    ax.set_title("U.S. Electricity Mix (% Share of Coal, Gas, Renewables)")
    ax.set_ylabel("Share (%)")
    ax.set_xlabel("Year")
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)
    plt.tight_layout()
    if save_png:
        png_path = Path("fuel_mix_share.png")
        plt.savefig(png_path, dpi=300)
        print(f"✔ saved {png_path}")
    plt.show()

def _main():
    # CLI: allow optional CSV path
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PIVOT
    if not csv_path.exists():
        sys.exit(f"Pivot file not found: {csv_path}")

    pivot = pd.read_csv(csv_path, index_col="Year")
    plot_fuel_mix_share(pivot)


if __name__ == "__main__":
    _main()
