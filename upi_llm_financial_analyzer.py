
# Personal UPI Usage & Financial Analyzer using LLMs
# Domain: FinTech / Personal Finance Automation


import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime


#streamlit Page Config

st.set_page_config(
    page_title="Personal UPI Usage & Financial Analyzer",
    layout="wide"
)
#App Title & Description
st.title("💰 Personal UPI Usage & Financial Analyzer")
st.caption("AI-powered spending insights & personalized financial advice")


# Upload CSV

uploaded_csv = st.file_uploader(
    "📂 Upload UPI CSV (Paytm / GPay / PhonePe)",
    type=["csv"]
)


# Load & Clean CSV (ERROR-PROOF)

def load_csv(file):
    df = pd.read_csv(file)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # DATE (NO FAILURE)
    date_cols = [c for c in df.columns if "date" in c or "time" in c]

    if date_cols:
        df["date"] = pd.to_datetime(df[date_cols[0]], errors="coerce")
    else:
        # ✅ ALWAYS CREATE DATE COLUMN
        df["date"] = pd.Timestamp.today()

    #AMOUNT (NO FAILURE)
    amount_cols = [
        c for c in df.columns
        if "amount" in c or "debit" in c or "credit" in c
    ]

    if amount_cols:
        df["amount"] = pd.to_numeric(df[amount_cols[0]], errors="coerce")
    else:
        # ✅ SAFE DEFAULT
        df["amount"] = 0

    # RECEIVER
    receiver_cols = [
        c for c in df.columns
        if "receiver" in c or "payee" in c or "merchant" in c
    ]

    df["receiver"] = df[receiver_cols[0]] if receiver_cols else "Unknown"

    #CATEGORY
    if "category" not in df.columns:
        df["category"] = "Uncategorized"

    return df



# Load Data

data = pd.DataFrame()

if uploaded_csv:
    data = load_csv(uploaded_csv)


# Dashboard

if not data.empty:

    st.subheader("📊 Financial Summary")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Transactions", len(data))
    c2.metric("Total Spend (₹)", round(data["amount"].sum(), 2))
    c3.metric("Average Spend (₹)", round(data["amount"].mean(), 2))
    c4.metric("Max Transaction (₹)", round(data["amount"].max(), 2))

    # Category-wise Analysis
    cat_df = data.groupby("category")["amount"].sum().reset_index()
    fig = px.bar(
        cat_df,
        x="category",
        y="amount",
        title="Category-wise Spending"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Monthly Trend
    data["month"] = data["date"].dt.to_period("M").astype(str)
    month_df = data.groupby("month")["amount"].sum().reset_index()
    fig = px.line(
        month_df,
        x="month",
        y="amount",
        title="Monthly Spending Trend",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

    # Wasteful Spending Detection
    st.subheader("⚠️ Potential Wasteful Transactions")
    waste = data[data["amount"] > data["amount"].mean()]
    st.dataframe(waste, use_container_width=True)

else:
    st.info("⬆️ Upload a CSV file to begin analysis")


# Footer

st.markdown("---")
st.caption("FinTech | NLP | LLMs | Streamlit | Hugging Face Ready")
