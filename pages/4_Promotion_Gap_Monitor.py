import streamlit as st
import pandas as pd

st.set_page_config(page_title="Promotion Gap Monitor", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/Career_Progression_Analysis_Final.csv")

df = load_data()

st.title("📈 Promotion Gap Monitor")

threshold = st.slider("Promotion Gap Threshold", 0.0, 1.0, 0.5, 0.05)

filtered = df[df["PromotionGapRatio"] >= threshold]

st.write(f"Employees above threshold: {len(filtered)}")

st.dataframe(
    filtered[
        [
            "Age",
            "Department",
            "JobRole",
            "YearsAtCompany",
            "YearsSinceLastPromotion",
            "PromotionGapRatio",
            "RetentionPriority"
        ]
    ],
    use_container_width=True
)