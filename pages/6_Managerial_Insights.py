import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Managerial Insights", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/Career_Progression_Analysis_Final.csv")

df = load_data()

st.title("👔 Managerial Insights")

# Proxy: manager stability via YearsWithCurrManager
mgr = df.groupby("JobRole")["YearsWithCurrManager"].mean().reset_index()

fig = px.bar(
    mgr,
    x="JobRole",
    y="YearsWithCurrManager",
    title="Manager Stability by Job Role"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

impact = df.groupby("JobRole")[["PromotionGapRatio", "RoleStagnationIndex"]].mean()

st.dataframe(impact.round(2), use_container_width=True)