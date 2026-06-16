import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Retention Center", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/Career_Progression_Analysis_Final.csv")

df = load_data()

st.title("🛡 Retention Center")

high_risk = df[df["RetentionPriority"] == "High Priority"]

st.metric("High Risk Employees", len(high_risk))

st.markdown("---")

fig = px.histogram(
    df,
    x="RetentionPriority",
    color="Department",
    title="Retention Priority Distribution"
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(high_risk, use_container_width=True)