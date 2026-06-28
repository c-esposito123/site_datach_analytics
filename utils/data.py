import pandas as pd
import streamlit as st

CSV_PATH = "base_projeto.csv"

COLUNAS_NUMERICAS = [
    "Age", "Number of Dependents", "Tenure in Months",
    "Avg Monthly Long Distance Charges", "Avg Monthly GB Download",
    "Monthly Charge", "Total Charges", "Total Refunds",
    "Total Extra Data Charges", "Total Long Distance Charges",
    "Total Revenue", "Satisfaction Score", "Churn Score", "CLTV",
]


@st.cache_data
def carregar_dados(caminho: str = CSV_PATH) -> pd.DataFrame:
    df = pd.read_csv(caminho)

    for col in COLUNAS_NUMERICAS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df
