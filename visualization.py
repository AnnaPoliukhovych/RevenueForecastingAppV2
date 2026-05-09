import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def show_forecast_plot(forecast_table):
    plot_data = forecast_table.copy()
    plot_data["date"] = pd.to_datetime(plot_data["date"])

    fig, ax = plt.subplots(figsize=(12, 5))

    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#111827")

    ax.plot(
        plot_data["date"],
        plot_data["predicted_revenue"],
        marker="o",
        linewidth=2,
        color="#60a5fa",
        label="Прогнозований дохід"
    )

    ax.set_title(
        "Прогнозований дохід освітньої онлайн-платформи",
        color="#f9fafb"
    )
    ax.set_xlabel("Дата", color="#e5e7eb")
    ax.set_ylabel("Дохід, грн", color="#e5e7eb")

    ax.tick_params(axis="x", colors="#d1d5db")
    ax.tick_params(axis="y", colors="#d1d5db")

    for spine in ax.spines.values():
        spine.set_color("#4b5563")

    ax.grid(
        True,
        color="#374151",
        linewidth=0.8,
        alpha=0.55
    )

    legend = ax.legend()
    legend.get_frame().set_facecolor("#1f2937")
    legend.get_frame().set_edgecolor("#4b5563")

    for text in legend.get_texts():
        text.set_color("#f9fafb")

    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)