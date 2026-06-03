import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from datetime import date, timedelta

from visualization import show_forecast_plot
from forecasting import (
    load_saved_model_artifact,
    forecast_selected_period_with_saved_model
)

from export_utils import dataframe_to_excel_bytes

from ui_components import (
    apply_custom_styles,
    show_forecast_success,
    show_help_card,
    show_model_badge
)


st.set_page_config(
    page_title="Прогнозування доходів освітньої онлайн-платформи",
    layout="wide"
)

apply_custom_styles()

st.title("Прогнозування доходів освітньої онлайн-платформи")

st.write(
    "Аналітична панель для формування прогнозу доходу освітньої онлайн-платформи "
    "на основі машинного навчання."
)


def rename_forecast_table(forecast_table):
    return forecast_table.rename(
        columns={
            "date": "Дата",
            "predicted_revenue": "Прогнозований дохід, грн"
        }
    )


try:
    model_artifact = load_saved_model_artifact()
except Exception as error:
    import streamlit as st
    st.error(f"Model load failed: {error}")
    st.stop()


prepared_data = model_artifact["prepared_data"]
best_ml_model_name = model_artifact["best_ml_model_name"]
training_rows = model_artifact["training_rows"]
training_start_date = model_artifact["training_start_date"]
training_end_date = model_artifact["training_end_date"]


st.subheader("Інформація про модель")

col1, col2, col3, col4 = st.columns(4)

with col1:
    show_model_badge(best_ml_model_name)

with col2:
    st.metric("Кількість рядків даних", training_rows)

with col3:
    st.metric(
        "Початок періоду даних",
        training_start_date.strftime("%Y-%m-%d")
    )

with col4:
    st.metric(
        "Кінець періоду даних",
        training_end_date.strftime("%Y-%m-%d")
    )


tab_forecast, tab_help = st.tabs(
    ["Прогнозування", "Довідка"]
)


with tab_forecast:
    st.subheader(
        "Формування прогнозу доходу",
        help="Оберіть бажаний період прогнозу"
    )

    last_dataset_date = prepared_data["date"].max().date()
    minimum_forecast_start = last_dataset_date + timedelta(days=1)

    today = date.today()

    if today > minimum_forecast_start:
        default_start = today
    else:
        default_start = minimum_forecast_start

    default_end = default_start + timedelta(days=29)

    if "forecast_start_date" not in st.session_state:
        st.session_state["forecast_start_date"] = default_start

    if "forecast_end_date" not in st.session_state:
        st.session_state["forecast_end_date"] = default_end

    forecast_col1, forecast_col2 = st.columns(2)

    with forecast_col1:
        forecast_start_date = st.date_input(
            "Дата початку прогнозу",
            value=st.session_state.get("forecast_start_date", default_start),
            min_value=minimum_forecast_start,
            format="YYYY/MM/DD",
            key="forecast_start_date"
        )

    with forecast_col2:
        forecast_end_date = st.date_input(
            "Дата завершення прогнозу",
            value=st.session_state.get("forecast_end_date", default_end),
            min_value=minimum_forecast_start,
            format="YYYY/MM/DD",
            key="forecast_end_date"
        )

    dates_are_filled = (
        forecast_start_date is not None
        and forecast_end_date is not None
    )

    dates_are_ordered = (
        dates_are_filled
        and forecast_end_date >= forecast_start_date
    )

    if dates_are_ordered:
        forecast_days = (forecast_end_date - forecast_start_date).days + 1
        forecast_period_key = (
            forecast_start_date.isoformat(),
            forecast_end_date.isoformat()
        )

        st.write(f"Обраний період прогнозування: **{forecast_days} днів**.")
    else:
        forecast_days = None
        forecast_period_key = None

    if st.button("Виконати прогноз", type="primary"):
        if not dates_are_filled:
            st.warning("Введіть дату початку та дату завершення прогнозу.")
            st.stop()

        if forecast_start_date < minimum_forecast_start:
            st.warning(
                f"Дата початку прогнозу не може бути раніше "
                f"{minimum_forecast_start.strftime('%Y/%m/%d')}."
            )
            st.stop()

        if forecast_end_date < forecast_start_date:
            st.warning(
                "Дата завершення прогнозу не може бути раніше дати початку прогнозу."
            )
            st.stop()

        days_from_history = (forecast_start_date - last_dataset_date).days

        if days_from_history > 90:
            st.warning(
                "Дата початку прогнозу віддалена від останньої дати в історичних даних "
                "більше ніж на 90 днів. Такий прогноз слід розглядати як орієнтовний."
            )

        if forecast_days > 365:
            st.warning(
                "Обрано період прогнозування понад 365 днів. "
                "Для довгострокових прогнозів точність може бути нижчою."
            )

        _, _, future_forecast_table = forecast_selected_period_with_saved_model(
            prepared_data,
            model_artifact,
            forecast_start_date,
            forecast_end_date
        )

        st.session_state["forecast_period_key"] = forecast_period_key
        st.session_state["future_forecast_table"] = future_forecast_table

        show_forecast_success()

    forecast_is_actual = (
        "future_forecast_table" in st.session_state
        and forecast_period_key is not None
        and st.session_state.get("forecast_period_key") == forecast_period_key
    )

    if forecast_is_actual:
        future_forecast_table = st.session_state["future_forecast_table"]

        st.subheader("Підсумкові показники прогнозу")

        total_revenue = future_forecast_table["predicted_revenue"].sum()
        average_daily_revenue = future_forecast_table["predicted_revenue"].mean()
        min_revenue = future_forecast_table["predicted_revenue"].min()
        max_revenue = future_forecast_table["predicted_revenue"].max()

        recent_30_average = prepared_data["revenue"].tail(30).mean()
        average_delta = average_daily_revenue - recent_30_average

        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

        with metric_col1:
            st.metric(
                "Сумарний дохід за період",
                f"{total_revenue:,.2f} грн"
            )

        with metric_col2:
            st.metric(
                "Середній дохід/день",
                f"{average_daily_revenue:,.2f} грн",
                delta=f"{average_delta:,.2f} грн ніж останній місяць даних"
            )

        with metric_col3:
            st.metric(
                "Мінімальний дохід/день",
                f"{min_revenue:,.2f} грн"
            )

        with metric_col4:
            st.metric(
                "Максимальний дохід/день",
                f"{max_revenue:,.2f} грн"
            )

        display_forecast_table = rename_forecast_table(
            future_forecast_table.copy()
        )

        with st.expander("Графік прогнозованого доходу", expanded=True):
            show_forecast_plot(future_forecast_table)

        with st.expander("Таблиця прогнозу", expanded=False):
            st.dataframe(
                display_forecast_table,
                use_container_width=True,
                hide_index=True
            )

        csv_result = display_forecast_table.to_csv(index=False).encode("utf-8-sig")

        excel_result = dataframe_to_excel_bytes(
            display_forecast_table,
            "Прогноз"
        )

        download_col1, download_col2, _ = st.columns([1.2, 1.2, 5])

        with download_col1:
            st.download_button(
                label="Завантажити прогноз у CSV",
                data=csv_result,
                file_name="forecast_selected_period.csv",
                mime="text/csv"
            )

        with download_col2:
            st.download_button(
                label="Завантажити прогноз у XLSX",
                data=excel_result,
                file_name="forecast_selected_period.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    elif (
        "future_forecast_table" in st.session_state
        and forecast_period_key is not None
    ):
        st.info(
            "Період прогнозування було змінено. "
            "Натисніть кнопку «Виконати прогноз», щоб оновити результат."
        )


with tab_help:
    st.subheader("Довідка користувача")

    show_help_card(
        "Призначення системи",
        "Система призначена для прогнозування майбутнього доходу освітньої "
        "онлайн-платформи на основі моделі машинного навчання.",
        "blue"
    )

    show_help_card(
        "Логіка роботи",
        "У застосунку використовується готова модель, яка була обрана після "
        "порівняння моделей за метриками точності.",
        "purple"
    )

    show_help_card(
        "Використана модель",
        f"Поточна збережена модель: <b>{best_ml_model_name}</b>. "
        "Якщо модель буде повторно навчена на іншому наборі даних, у застосунку може "
        "використовуватися інший алгоритм.",
        "green"
    )

    show_help_card(
        "Формування прогнозу",
        "Користувач обирає період прогнозування, після чого система формує прогноз "
        "доходу на основі збереженої моделі та історичних даних, використаних під час навчання.",
        "blue"
    )

    show_help_card(
        "Обмеження прогнозу",
        "Прогноз є орієнтовним результатом роботи моделі. Його точність може знижуватися, "
        "якщо обраний період значно віддалений від останньої дати історичних даних або якщо "
        "умови функціонування платформи суттєво змінилися.",
        "purple"
    )
