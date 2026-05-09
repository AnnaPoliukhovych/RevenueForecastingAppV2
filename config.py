BUSINESS_FEATURE_COLUMNS = [
    "new_registered_users",
    "active_users",
    "platform_visits",
    "paid_enrollments",
    "average_price",
    "discount_rate",
    "marketing_spend",
    "conversion_rate"
]

CALENDAR_COLUMNS = [
    "month",
    "day_of_week"
]

LAG_FEATURE_COLUMNS = [
    "revenue_lag_1",
    "revenue_lag_7",
    "revenue_lag_14",
    "revenue_lag_30",
    "revenue_rolling_mean_7",
    "revenue_rolling_mean_30"
]

FEATURE_COLUMNS = (
    BUSINESS_FEATURE_COLUMNS
    + CALENDAR_COLUMNS
    + LAG_FEATURE_COLUMNS
)

TARGET_COLUMN = "revenue"