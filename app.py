import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Career Intelligence Platform",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("data/Career_Progression_Analysis_Final.csv")

    df['EmployeeID'] = [
        f'EMP{i:04d}' for i in range(1, len(df)+1)
    ]

    cluster_labels = {
        0: "Promotion-Stalled Employees",
        1: "Stable Contributors",
        2: "Senior Long-Term Contributors",
        3: "Career Growth Track",
        4: "Early-Career Explorers"
    }

    df["CareerClusterLabel"] = df["CareerCluster"].map(cluster_labels)

    return df


df = load_data()

# ---------------------------------------------------
# 🎯 FRONT PAGE (ADD THIS HERE)
# ---------------------------------------------------

st.title("🚀 Career Intelligence & Retention Optimization Platform")

st.markdown("""
### 🏢 Workforce Analytics Dashboard

A data-driven HR intelligence system designed to analyze employee career progression, retention risk, and promotion gaps using machine learning insights.

---

##  Key Business Objectives

-  Identify employees at risk of attrition  
-  Detect promotion stagnation early  
-  Understand career growth patterns  
-  Segment workforce using ML-based clustering  
-  Improve managerial and departmental decisions  

---

##  What this platform provides

✔ Executive-level workforce overview  
✔ Employee career trajectory mapping  
✔ Promotion gap monitoring system  
✔ Retention risk intelligence center  
✔ Managerial performance insights  

---

## ⚙️ Navigation

Use the sidebar to explore different modules:
 Executive Overview →  Career DNA →  Clusters →  Promotion →  Retention →  Managers
""")

# ---------------------------------------------------
# SIDEBAR (KEEP FILTERS HERE)
# ---------------------------------------------------

st.sidebar.title("📌 Dashboard Filters")

department = st.sidebar.selectbox(
    "Department",
    ["All"] + sorted(df["Department"].unique())
)

jobrole = st.sidebar.selectbox(
    "Job Role",
    ["All"] + sorted(df["JobRole"].unique())
)

priority = st.sidebar.selectbox(
    "Retention Priority",
    ["All"] + sorted(df["RetentionPriority"].unique())
)

filtered_df = df.copy()

if department != "All":
    filtered_df = filtered_df[filtered_df["Department"] == department]

if jobrole != "All":
    filtered_df = filtered_df[filtered_df["JobRole"] == jobrole]

if priority != "All":
    filtered_df = filtered_df[filtered_df["RetentionPriority"] == priority]

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

st.markdown("---")

total_emp = len(filtered_df)

attrition_rate = round(
    (filtered_df["Attrition"].sum() / len(filtered_df)) * 100,
    2
)

high_priority = len(
    filtered_df[filtered_df["RetentionPriority"] == "High Priority"]
)

active_intervention = len(
    filtered_df[
        (filtered_df["RetentionPriority"] == "High Priority")
        & (filtered_df["Attrition"] == 0)
    ]
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Employees", total_emp)

with col2:
    st.metric("Attrition Rate", f"{attrition_rate}%")

with col3:
    st.metric("High Priority Cases", high_priority)

with col4:
    st.metric("Intervention Opportunities", active_intervention)

# ---------------------------------------------------
# (KEEP YOUR REMAINING CHARTS AS-IS BELOW)
# ---------------------------------------------------

# ---------------------------------------------------
# CLUSTER DISTRIBUTION
# ---------------------------------------------------

st.markdown("---")
st.subheader("📊 Career Cluster Distribution")

cluster_counts = (
    filtered_df["CareerClusterLabel"]
    .value_counts()
    .reset_index()
)

cluster_counts.columns = [
    "Career Cluster",
    "Employees"
]

fig_cluster = px.bar(
    cluster_counts,
    x="Career Cluster",
    y="Employees",
    color="Employees",
    text="Employees",
    title="Employee Career Segments"
)

fig_cluster.update_layout(
    height=500
)

st.plotly_chart(
    fig_cluster,
    use_container_width=True
)

# ---------------------------------------------------
# CLUSTER SUMMARY TABLE
# ---------------------------------------------------

st.subheader("📌 Cluster Summary")

summary = filtered_df.groupby(
    "CareerClusterLabel"
)[
    [
        "PromotionGapRatio",
        "RoleStagnationIndex",
        "TrainingIntensityScore",
        "MonthlyIncome"
    ]
].mean().round(2)

st.dataframe(
    summary,
    use_container_width=True
)

# ---------------------------------------------------
# PROMOTION GAP MONITOR
# ---------------------------------------------------

st.markdown("---")
st.subheader("📈 Promotion Gap Monitor")

threshold = st.slider(
    "Select Promotion Gap Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.50,
    step=0.05
)

high_gap = filtered_df[
    filtered_df["PromotionGapRatio"]
    >= threshold
]

st.write(
    f"Employees Above Threshold: {len(high_gap)}"
)

display_cols = [
    "EmployeeID",
    "Department",
    "JobRole",
    "YearsAtCompany",
    "YearsSinceLastPromotion",
    "PromotionGapRatio",
    "RetentionPriority"
]

st.dataframe(
    high_gap[display_cols],
    use_container_width=True
)

# ---------------------------------------------------
# DEPARTMENT ANALYSIS
# ---------------------------------------------------

st.markdown("---")
st.subheader("🏢 Department Intelligence")

dept_summary = filtered_df.groupby(
    "Department"
)[
    [
        "PromotionGapRatio",
        "RoleStagnationIndex",
        "RetentionOpportunityIndex"
    ]
].mean().reset_index()

fig_dept = px.bar(
    dept_summary,
    x="Department",
    y="PromotionGapRatio",
    color="Department",
    title="Average Promotion Gap by Department"
)

st.plotly_chart(
    fig_dept,
    use_container_width=True
)

st.dataframe(
    dept_summary.round(2),
    use_container_width=True
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.success(
    "Career Progression and Promotion Gap Analysis for Retention Optimization at Palo Alto Networks"
)