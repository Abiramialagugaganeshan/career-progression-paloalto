import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Career DNA Explorer", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/Career_Progression_Analysis_Final.csv")

df = load_data()

st.title("🧬 Career DNA Explorer")

emp_id = st.selectbox("Select Employee Index", df.index)

emp = df.loc[emp_id]

st.subheader("Employee Profile")

st.write(emp)

st.markdown("---")

# PCA Visualization
fig = px.scatter(
    df,
    x="PCA1",
    y="PCA2",
    color="CareerCluster",
    title="Career DNA Map (PCA Projection)"
)

fig.add_scatter(
    x=[emp["PCA1"]],
    y=[emp["PCA2"]],
    mode="markers",
    marker=dict(size=15, color="red"),
    name="Selected Employee"
)

st.plotly_chart(fig, use_container_width=True)