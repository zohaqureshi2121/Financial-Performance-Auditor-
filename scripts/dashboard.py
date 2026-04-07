import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Financial Performance Auditor", layout="wide")

# Styled Title
st.markdown(
    "<h1 style='color:#2C5282;'>Financial Performance Auditor</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='color:gray; font-size:13px;'>Developed by Zoha Qureshi</p>",
    unsafe_allow_html=True
)

# Load Data
@st.cache_data
def load_data():
    historical = pd.read_csv("data/financial_dataset_with_recommendations.csv")
    predictions = pd.read_csv("data/financial_predictions_2025.csv")
    return historical, predictions

historical_df, prediction_df = load_data()

# Sidebar Selection
st.sidebar.header("Select Company & Year")

company_list = sorted(historical_df["Company_ID"].unique())
selected_company = st.sidebar.selectbox("Select Company", company_list)

year_list = sorted(historical_df["Year"].unique())
selected_year = st.sidebar.selectbox("Select Year", year_list)

company_year_data = historical_df[
    (historical_df["Company_ID"] == selected_company) &
    (historical_df["Year"] == selected_year)
]

# Styled Section Header
def section_header(title):
    st.markdown(f"""
        <div style="
            border-left: 6px solid #4C6A92 ;
            padding-left: 12px;
            margin-top: 30px;
            margin-bottom: 10px;
            font-size: 22px;
            font-weight: 600;
            color:#4C6A92;">
            {title}
        </div>
    """, unsafe_allow_html=True)

# Status color function 
def styled_status(status):
    status = str(status).strip()
    color_map = {
        "Healthy": "#2ecc71",
        "Moderate": "#f1c40f",
        "At Risk": "#e67e22",
        "High Risk": "#e74c3c"
    }
    color = color_map.get(status, "#95a5a6")
    return f"""
        <div style="
            display:inline-block;
            padding:10px 20px;
            border-radius:20px;
            background-color:{color};
            color:white;
            font-weight:600;
            font-size:16px;">
            {status}
        </div>
    """

# KPI Section (Historical)
section_header("Financial Metrics")

if not company_year_data.empty:

    data = company_year_data.iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Revenue", f"${data['Revenue']:,.2f}")

    net_income = data['Net_Income']
    formatted_income = f"-${abs(net_income):,.2f}" if net_income < 0 else f"${net_income:,.2f}"
    col2.metric("Net Income", formatted_income)

    col3.metric("Net Profit Margin", f"{data['Net_Profit_Margin']*100:.2f}%")

    col4, col5, col6 = st.columns(3)
    col4.metric("ROE", f"{data['ROE']*100:.2f}%")
    col5.metric("Debt to Equity", f"{data['Debt_to_Equity']:.2f}")

    if pd.notna(data["Revenue_Growth"]):
        col6.metric("Revenue Growth", f"{data['Revenue_Growth']*100:.2f}%")
    else:
        col6.metric("Revenue Growth", "N/A")

    # Financial Health Section
    section_header("Financial Health")
    col_h1, col_h2 = st.columns(2)
    col_h1.metric("Health Score", f"{int(data['Health_Score'])}")

    with col_h2:
        st.markdown("Health Status")
        st.markdown(styled_status(data["Health_Status"]), unsafe_allow_html=True)

    # Recommendations Section
    section_header("Recommendations")
    st.markdown(
        f"""
        <div style="
            background-color:#f8f9fa;
            padding:12px 16px;
            border-radius:8px;
            font-size:16px;
            line-height:1.7;
        ">
        {data['Final_Recommendations']}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Charts Section
    section_header("Revenue Trend & Financial Breakdown")
    col_left, col_right = st.columns(2)

    with col_left:
        company_history = historical_df[
            historical_df["Company_ID"] == selected_company
        ].sort_values("Year")

        company_prediction = prediction_df[
            prediction_df["Company_ID"] == selected_company
        ]

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=company_history["Year"],
            y=company_history["Revenue"],
            mode="lines+markers",
            name="Historical Revenue"
        ))

        if not company_prediction.empty:
            last_year = company_history["Year"].max()
            last_revenue = company_history.iloc[-1]["Revenue"]
            forecast_year = company_prediction.iloc[0]["Year"]
            forecast_revenue = company_prediction.iloc[0]["Revenue"]

            fig_trend.add_trace(go.Scatter(
                x=[last_year, forecast_year],
                y=[last_revenue, forecast_revenue],
                mode="lines+markers",
                name="Forecast Revenue",
                line=dict(dash="dash")
            ))

        fig_trend.update_layout(
            template="plotly_white",
            xaxis_title="Year",
            yaxis_title="Revenue"
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_right:
        revenue = data["Revenue"]
        net_income = data["Net_Income"]
        expenses = revenue - net_income

        fig_waterfall = go.Figure(go.Waterfall(
            orientation="v",
            measure=["relative", "relative", "total"],
            x=["Revenue", "Expenses", "Net Income"],
            y=[revenue, -expenses, 0],
            increasing=dict(marker=dict(color="green")),
            decreasing=dict(marker=dict(color="crimson")),
            totals=dict(marker=dict(color="royalblue"))
        ))

        fig_waterfall.update_layout(
            title=f"{selected_company} - {selected_year}",
            template="plotly_white",
            yaxis_title="Amount"
        )
        st.plotly_chart(fig_waterfall, use_container_width=True)

# 2025 Prediction Section
section_header("2025 Predicted Financial Outlook")
company_prediction = prediction_df[
    prediction_df["Company_ID"] == selected_company
]

if not company_prediction.empty:
    pred = company_prediction.iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Predicted Revenue (2025)", f"${pred['Revenue']:,.2f}")

    pred_income = pred['Net_Income']
    formatted_pred_income = f"-${abs(pred_income):,.2f}" if pred_income < 0 else f"${pred_income:,.2f}"
    col2.metric("Predicted Net Income (2025)", formatted_pred_income)

    col3.metric("Predicted Net Profit Margin", f"{pred['Net_Profit_Margin']*100:.2f}%")

    col4, col5, col6 = st.columns(3)
    col4.metric("Predicted ROE", f"{pred['ROE']*100:.2f}%")
    col5.metric("Predicted Debt to Equity", f"{pred['Debt_to_Equity']:.2f}")

    if pd.notna(pred["Revenue_Growth"]):
        col6.metric("Predicted Revenue Growth", f"{pred['Revenue_Growth']*100:.2f}%")
    else:
        col6.metric("Predicted Revenue Growth", "N/A")

    section_header("Predicted Financial Health (2025)")
    col_ph1, col_ph2 = st.columns(2)
    col_ph1.metric("Predicted Health Score", f"{int(pred['Health_Score'])}")

    with col_ph2:
        st.markdown("Predicted Health Status")
        st.markdown(styled_status(pred["Health_Status"]), unsafe_allow_html=True)

else:
    st.warning("No prediction available for this company.")