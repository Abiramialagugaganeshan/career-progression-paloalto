import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Executive Overview", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/Career_Progression_Analysis_Final.csv")

df = load_data()

st.title("📊 Executive Overview")

st.markdown("High-level workforce health and attrition snapshot.")

# KPIs
col1, col2, col3 = st.columns(3)

attrition_rate = round(df["Attrition"].mean() * 100, 2)

with col1:
    st.metric("Total Employees", len(df))

with col2:
    st.metric("Attrition Rate", f"{attrition_rate}%")

with col3:
    st.metric("Avg Monthly Income", round(df["MonthlyIncome"].mean(), 2))

st.markdown("---")

# Attrition by Department
dept = df.groupby("Department")["Attrition"].mean().reset_index()

fig = px.bar(dept, x="Department", y="Attrition", title="Attrition by Department")
st.plotly_chart(fig, use_container_width=True)

# Gender distribution
fig2 = px.pie(df, names="Gender", title="Gender Distribution")
st.plotly_chart(fig2, use_container_width=True)