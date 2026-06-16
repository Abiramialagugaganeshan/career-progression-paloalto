import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cluster Intelligence", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/Career_Progression_Analysis_Final.csv")

df = load_data()

st.title("🧠 Cluster Intelligence")

cluster_summary = df.groupby("CareerCluster").mean(numeric_only=True)

st.subheader("Cluster Averages")
st.dataframe(cluster_summary)

st.markdown("---")

fig = px.bar(
    df.groupby("CareerCluster")["MonthlyIncome"].mean().reset_index(),
    x="CareerCluster",
    y="MonthlyIncome",
    title="Average Income by Career Cluster"
)

st.plotly_chart(fig, use_container_width=True)