import streamlit as st


def apply_custom_styles():
    st.markdown(
        """
        <style>
        .model-badge {
            background: linear-gradient(
                135deg,
                rgba(37, 99, 235, 0.32) 0%,
                rgba(79, 70, 229, 0.22) 45%,
                rgba(124, 58, 237, 0.30) 100%
            );
            border: 1px solid rgba(147, 197, 253, 0.48);
            border-radius: 16px;
            padding: 14px 18px;
            min-height: 74px;
        }

        .model-badge-title {
            color: rgba(226, 232, 240, 0.76);
            font-size: 14px;
            margin-bottom: 6px;
        }

        .model-badge-value {
            color: #dbeafe;
            font-size: 20px;
            font-weight: 700;
        }

        a[href^="#"] {
            display: none !important;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: rgba(34, 197, 94, 0.12);
            border: 1px solid rgba(34, 197, 94, 0.35);
            border-radius: 999px;
            padding: 10px 16px;
            margin: 12px 0 18px 0;
            color: #86efac;
            font-weight: 600;
        }

        .status-dot {
            width: 9px;
            height: 9px;
            border-radius: 50%;
            background: #22c55e;
        }

        .help-card {
            border-radius: 14px;
            padding: 16px 18px;
            margin: 14px 0;
            border: 1px solid rgba(255, 255, 255, 0.14);
        }

        .help-card-blue {
            background: linear-gradient(
                135deg,
                rgba(37, 99, 235, 0.16),
                rgba(15, 23, 42, 0.88)
            );
            border-color: rgba(147, 197, 253, 0.30);
        }

        .help-card-purple {
            background: linear-gradient(
                135deg,
                rgba(124, 58, 237, 0.16),
                rgba(15, 23, 42, 0.88)
            );
            border-color: rgba(196, 181, 253, 0.30);
        }

        .help-card-green {
            background: linear-gradient(
                135deg,
                rgba(22, 163, 74, 0.14),
                rgba(15, 23, 42, 0.88)
            );
            border-color: rgba(134, 239, 172, 0.26);
        }

        .help-card-title {
            color: #ffffff;
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .help-card-text {
            color: rgba(255, 255, 255, 0.82);
            font-size: 15px;
            line-height: 1.55;
        }

        div.stButton > button[kind="primary"] {
            background: linear-gradient(
                135deg,
                rgba(37, 99, 235, 0.34),
                rgba(124, 58, 237, 0.28)
            ) !important;
            color: #f8fafc !important;
            border: 1px solid rgba(191, 219, 254, 0.75) !important;
            border-radius: 14px !important;
            padding: 11px 22px !important;
            font-weight: 750 !important;
            box-shadow: 0 8px 24px rgba(37, 99, 235, 0.24) !important;
        }

        div.stButton > button[kind="primary"]:hover {
            background: linear-gradient(
                135deg,
                rgba(37, 99, 235, 0.52),
                rgba(124, 58, 237, 0.42)
            ) !important;
            color: #ffffff !important;
            border: 1px solid rgba(219, 234, 254, 0.95) !important;
            box-shadow: 0 10px 30px rgba(37, 99, 235, 0.36) !important;
        }

        div.stDownloadButton > button {
            background: rgba(37, 99, 235, 0.18) !important;
            color: #f8fafc !important;
            border: 1px solid rgba(147, 197, 253, 0.55) !important;
            border-radius: 12px !important;
            padding: 10px 18px !important;
            font-weight: 700 !important;
        }

        div.stDownloadButton > button:hover {
            background: rgba(37, 99, 235, 0.32) !important;
            color: #ffffff !important;
            border: 1px solid rgba(191, 219, 254, 0.9) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def show_forecast_success():
    st.markdown(
        """
        <div class="status-badge">
            <span class="status-dot"></span>
            <span>Прогноз успішно сформовано</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_help_card(title, text, variant="blue"):
    st.markdown(
        f"""
        <div class="help-card help-card-{variant}">
            <div class="help-card-title">{title}</div>
            <div class="help-card-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_model_badge(model_name):
    st.markdown(
        f"""
        <div class="model-badge">
            <div class="model-badge-title">Використана модель</div>
            <div class="model-badge-value">{model_name}</div>
        </div>
        """,
        unsafe_allow_html=True
    )