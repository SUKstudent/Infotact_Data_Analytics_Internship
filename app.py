import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- CONFIG ----------------
st.set_page_config(page_title="MTA Dashboard", layout="wide")
st.title("📊 Multi-Touch Attribution Dashboard")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("multi_touch_attribution_dataset_cleaned.csv")
    except FileNotFoundError:
        st.error(
            "Dataset file not found. Make sure "
            "'multi_touch_attribution_dataset_cleaned.csv' "
            "exists in the GitHub repository root."
        )
        st.stop()

    if "event_timestamp_utc" in df.columns:
        df["event_timestamp_utc"] = pd.to_datetime(
            df["event_timestamp_utc"], errors="coerce"
        )

    if "event_date" in df.columns:
        df["event_date"] = pd.to_datetime(
            df["event_date"], errors="coerce"
        )

    return df


df = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.title("🎛 Filters")

page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Channel Analysis",
        "Funnel Analysis",
        "Campaign Analysis",
        "Device & Region",
        "Touchpoint Analysis",
        "Insights",
    ],
)

channels = sorted(df["channel"].dropna().unique().tolist())

selected_channels = st.sidebar.multiselect(
    "🎯 Select Channels",
    options=channels,
    default=channels,
)

df = df[df["channel"].isin(selected_channels)]

st.sidebar.info("Multi-Touch Attribution System")

# =========================================================
# OVERVIEW
# =========================================================
if page == "Overview":

    st.subheader("📌 KPI Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Events", len(df))
    col2.metric("Journeys", df["journey_id"].nunique())
    col3.metric("Conversions", int(df["is_conversion"].sum()))
    col4.metric("Revenue", f"${df['conversion_value'].sum():,.2f}")

    st.divider()

    st.subheader("📈 Revenue Trend Over Time")

    trend = (
        df.groupby("event_date")["conversion_value"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        trend,
        x="event_date",
        y="conversion_value",
        markers=True,
        title="Revenue Trend",
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# CHANNEL ANALYSIS
# =========================================================
elif page == "Channel Analysis":

    st.subheader("📡 Channel Performance")

    ch = (
        df.groupby("channel")
        .agg(
            revenue=("conversion_value", "sum"),
            conversions=("is_conversion", "sum"),
            events=("event_id", "count"),
        )
        .reset_index()
    )

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.line(
            ch,
            x="channel",
            y="revenue",
            markers=True,
            title="Revenue by Channel",
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.bar(
            ch,
            x="channel",
            y="conversions",
            color="channel",
            title="Conversions by Channel",
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📊 Revenue Share")

    fig3 = px.pie(
        ch,
        names="channel",
        values="revenue",
        title="Revenue Share by Channel",
    )

    st.plotly_chart(fig3, use_container_width=True)

# =========================================================
# FUNNEL ANALYSIS
# =========================================================
elif page == "Funnel Analysis":

    st.subheader("🎯 Funnel Breakdown")

    funnel = (
        df.groupby("funnel_stage")
        .agg(
            events=("event_id", "count"),
            conversions=("is_conversion", "sum"),
        )
        .reset_index()
    )

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.bar(
            funnel,
            x="funnel_stage",
            y="events",
            color="funnel_stage",
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.line(
            funnel,
            x="funnel_stage",
            y="conversions",
            markers=True,
        )
        st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# CAMPAIGN ANALYSIS
# =========================================================
elif page == "Campaign Analysis":

    st.subheader("📢 Campaign Performance")

    camp = (
        df.groupby("campaign")
        .agg(
            revenue=("conversion_value", "sum"),
            events=("event_id", "count"),
        )
        .reset_index()
        .sort_values("revenue", ascending=False)
    )

    fig1 = px.bar(
        camp,
        x="campaign",
        y="revenue",
        color="campaign",
        title="Revenue by Campaign",
    )

    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(
        camp,
        x="campaign",
        y="events",
        markers=True,
        title="Campaign Events",
    )

    st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# DEVICE & REGION
# =========================================================
elif page == "Device & Region":

    col1, col2 = st.columns(2)

    with col1:
        device = df["device"].value_counts().reset_index()
        device.columns = ["device", "count"]

        fig = px.pie(
            device,
            names="device",
            values="count",
            title="Device Distribution",
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        region = df["region"].value_counts().reset_index()
        region.columns = ["region", "count"]

        fig = px.bar(
            region,
            x="region",
            y="count",
            color="region",
            title="Region Distribution",
        )

        st.plotly_chart(fig, use_container_width=True)

# =========================================================
# TOUCHPOINT ANALYSIS
# =========================================================
elif page == "Touchpoint Analysis":

    st.subheader("🔁 Touchpoint Distribution")

    touch = (
        df.groupby("touchpoint_number")
        .size()
        .reset_index(name="events")
    )

    fig1 = px.line(
        touch,
        x="touchpoint_number",
        y="events",
        markers=True,
        title="Events by Touchpoint",
    )

    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(
        touch,
        x="touchpoint_number",
        y="events",
        title="Touchpoint Events",
    )

    st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# INSIGHTS
# =========================================================
elif page == "Insights":

    st.subheader("🧠 Business Insights")

    avg_touch = (
        df.groupby("journey_id")["touchpoint_number"]
        .max()
        .mean()
    )

    conv_rate = (
        df["is_conversion"].sum()
        / max(df["journey_id"].nunique(), 1)
    )

    st.success(
        f"Average Touchpoints per Journey: {avg_touch:.2f}"
    )

    st.success(
        f"Journey Conversion Rate: {conv_rate:.2%}"
    )

    st.info(
        "Channels are dynamically filtered based on selection."
    )
