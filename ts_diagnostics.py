import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf # type: ignore

def diagnostics_decompose(ts, model_name="TimeSeries"):
    """Run ACF and PACF diagnostics only—STL skipped for annual data."""
    fig, axes = plt.subplots(2, 1, figsize=(10, 6))
    plot_acf(ts.dropna(), lags=24, ax=axes[0])
    plot_pacf(ts.dropna(), lags=24, ax=axes[1])
    axes[0].set_title(f"{model_name} - ACF")
    axes[1].set_title(f"{model_name} - PACF")
    plt.tight_layout()
    plt.savefig(f"{model_name.lower()}_acf_pacf.png", dpi=300)
    print(f"✔ saved {model_name.lower()}_acf_pacf.png")
