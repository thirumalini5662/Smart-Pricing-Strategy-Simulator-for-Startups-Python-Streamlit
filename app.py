import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from data_generator import generate_customer_data
from pricing_engine import (
    simulate_pricing,
    generate_price_comparison
)
from ml_model import train_revenue_model


# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="Smart Pricing Strategy Simulator",
    page_icon="💰",
    layout="wide"
)


# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("💰 Smart Pricing Strategy Simulator")

st.markdown(
    """
    ### Startup Pricing Analytics Dashboard

    Experiment with different pricing strategies and
    understand their potential impact on revenue,
    profitability, customer retention and lifetime value.
    """
)


# ---------------------------------------------------
# GENERATE CUSTOMER DATA
# ---------------------------------------------------

if "customer_data" not in st.session_state:

    st.session_state.customer_data = (
        generate_customer_data(1000)
    )


df = st.session_state.customer_data


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header("⚙️ Pricing Configuration")


pricing_model = st.sidebar.selectbox(
    "Select Pricing Model",
    [
        "Subscription",
        "Freemium",
        "One-time",
        "Tiered"
    ]
)


customers = st.sidebar.number_input(
    "Customer Base",
    min_value=100,
    max_value=100000,
    value=1000,
    step=100
)


price = st.sidebar.slider(
    "Base Price ($)",
    min_value=5,
    max_value=200,
    value=30
)


churn_rate = st.sidebar.slider(
    "Churn Rate",
    min_value=0.01,
    max_value=0.50,
    value=0.10,
    step=0.01
)


cost_per_customer = st.sidebar.number_input(
    "Cost per Customer ($)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=1.0
)


marketing_spend = st.sidebar.number_input(
    "Marketing Spend ($)",
    min_value=0.0,
    max_value=1000000.0,
    value=5000.0,
    step=500.0
)


# ---------------------------------------------------
# SIMULATION
# ---------------------------------------------------

result = simulate_pricing(
    price=price,
    churn_rate=churn_rate,
    cost_per_customer=cost_per_customer,
    customers=customers,
    marketing_spend=marketing_spend,
    pricing_model=pricing_model
)


# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

st.subheader("📊 Current Scenario")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Revenue",
        f"${result['Revenue']:,.2f}"
    )


with col2:

    st.metric(
        "Profit",
        f"${result['Profit']:,.2f}"
    )


with col3:

    st.metric(
        "Retained Customers",
        f"{result['Retained Customers']:,}"
    )


with col4:

    st.metric(
        "Profit Margin",
        f"{result['Profit Margin']:.2f}%"
    )


# ---------------------------------------------------
# SECOND KPI ROW
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Lost Customers",
        f"{result['Lost Customers']:,}"
    )


with col2:

    st.metric(
        "Total Cost",
        f"${result['Total Cost']:,.2f}"
    )


with col3:

    st.metric(
        "Estimated LTV",
        f"${result['Estimated LTV']:,.2f}"
    )


with col4:

    st.metric(
        "Selected Model",
        pricing_model
    )


# ---------------------------------------------------
# PRICE SIMULATION
# ---------------------------------------------------

st.subheader("📈 Price Point Simulation")


min_price = st.slider(
    "Minimum Price",
    5,
    100,
    10
)


max_price = st.slider(
    "Maximum Price",
    20,
    200,
    100
)


step = st.slider(
    "Price Step",
    1,
    20,
    5
)


comparison_df = generate_price_comparison(
    min_price=min_price,
    max_price=max_price,
    step=step,
    churn_rate=churn_rate,
    cost_per_customer=cost_per_customer,
    customers=customers,
    marketing_spend=marketing_spend,
    pricing_model=pricing_model
)


# ---------------------------------------------------
# REVENUE CHART
# ---------------------------------------------------

st.subheader("💵 Revenue by Price")


fig1, ax1 = plt.subplots()

ax1.plot(
    comparison_df["Price"],
    comparison_df["Revenue"],
    marker="o"
)

ax1.set_xlabel("Price ($)")
ax1.set_ylabel("Revenue ($)")
ax1.set_title("Revenue vs Price")

st.pyplot(fig1)


# ---------------------------------------------------
# PROFIT CHART
# ---------------------------------------------------

st.subheader("💰 Profit by Price")


fig2, ax2 = plt.subplots()

ax2.plot(
    comparison_df["Price"],
    comparison_df["Profit"],
    marker="o"
)

ax2.set_xlabel("Price ($)")
ax2.set_ylabel("Profit ($)")
ax2.set_title("Profit vs Price")

st.pyplot(fig2)


# ---------------------------------------------------
# BEST SIMULATED PROFIT SCENARIO
# ---------------------------------------------------

best_row = comparison_df.loc[
    comparison_df["Profit"].idxmax()
]


st.subheader("🎯 Highest Simulated Profit Scenario")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Price",
        f"${best_row['Price']:,.2f}"
    )


with col2:

    st.metric(
        "Profit",
        f"${best_row['Profit']:,.2f}"
    )


with col3:

    st.metric(
        "Revenue",
        f"${best_row['Revenue']:,.2f}"
    )


st.info(
    "This is the highest-profit scenario within "
    "the simulated price range and assumptions. "
    "It is not a guarantee of real-world performance."
)


# ---------------------------------------------------
# CUSTOMER SEGMENTATION
# ---------------------------------------------------

st.subheader("👥 Customer Segmentation")


segment_counts = (
    df["Segment"]
    .value_counts()
    .reset_index()
)

segment_counts.columns = [
    "Segment",
    "Customers"
]


fig3, ax3 = plt.subplots()

ax3.bar(
    segment_counts["Segment"],
    segment_counts["Customers"]
)

ax3.set_xlabel("Customer Segment")
ax3.set_ylabel("Number of Customers")
ax3.set_title("Customer Segmentation")

st.pyplot(fig3)


# ---------------------------------------------------
# SEGMENT TABLE
# ---------------------------------------------------

st.dataframe(
    segment_counts,
    use_container_width=True
)


# ---------------------------------------------------
# ML SECTION
# ---------------------------------------------------

st.subheader("🤖 Machine Learning Revenue Prediction")


model, mae = train_revenue_model(df)


willingness = st.slider(
    "Customer Willingness-to-Pay",
    5,
    100,
    30
)


customer_churn = st.slider(
    "Customer Churn Probability",
    0.01,
    0.50,
    0.10,
    step=0.01
)


prediction = model.predict(
    [[
        willingness,
        customer_churn
    ]]
)[0]


st.metric(
    "Predicted Revenue Potential",
    f"${prediction:,.2f}"
)


st.write(
    f"Model Mean Absolute Error: {mae:.2f}"
)


# ---------------------------------------------------
# CUSTOMER DATA
# ---------------------------------------------------

st.subheader("📋 Simulated Customer Dataset")


st.dataframe(
    df.head(100),
    use_container_width=True
)


# ---------------------------------------------------
# DOWNLOAD DATA
# ---------------------------------------------------

csv = comparison_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="📥 Download Simulation Results",
    data=csv,
    file_name="pricing_simulation_results.csv",
    mime="text/csv"
)


# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "Smart Pricing Strategy Simulator | "
    "Entrepreneurship Project"
)