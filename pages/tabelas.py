import streamlit as st
from utils import carregar_dados, saudacao


def render():
    # --- Título ---
    st.title("📋 Tabela de Clientes")
    st.caption("Visão estática da base de dados, com filtros simples para facilitar a leitura.")

    # Saudação global (nome do usuário)
    saudacao()

    df = carregar_dados()

    # --- Filtros ---
    col1, col2, col3 = st.columns(3)

    with col1:
        status_opcoes = ["Todos"] + sorted(df["Customer Status"].dropna().unique().tolist())
        status_filtro = st.selectbox("Status do cliente", status_opcoes)

    with col2:
        contrato_opcoes = ["Todos"] + sorted(df["Contract"].dropna().unique().tolist())
        contrato_filtro = st.selectbox("Tipo de contrato", contrato_opcoes)

    with col3:
        internet_opcoes = ["Todos"] + sorted(df["Internet Service"].dropna().unique().tolist())
        internet_filtro = st.selectbox("Possui internet", internet_opcoes)

    # --- Filtro aplicado ---
    df_filtrado = df.copy()

    if status_filtro != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Customer Status"] == status_filtro]

    if contrato_filtro != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Contract"] == contrato_filtro]

    if internet_filtro != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Internet Service"] == internet_filtro]

    st.markdown(f"**{len(df_filtrado)}** clientes encontrados com os filtros selecionados.")

    # --- Colunas da tabela ---
    colunas_exibicao = [
        "Customer ID", "Gender", "Age", "Married", "Dependents", "City", "State",
        "Tenure in Months", "Contract", "Internet Service", "Monthly Charge",
        "Total Charges", "Satisfaction Score", "Customer Status", "Churn Label",
        "Churn Score", "CLTV", "Churn Category", "Churn Reason",
    ]

    colunas_existentes = [c for c in colunas_exibicao if c in df_filtrado.columns]

    # --- Tabela ---
    st.dataframe(
        df_filtrado[colunas_existentes],
        use_container_width=True,
        height=480,
        hide_index=True,
    )

    st.markdown("---")

    # --- Resumo estatístico ---
    st.markdown("### 📐 Resumo estatístico das principais métricas numéricas")

    metricas = [
        "Age",
        "Tenure in Months",
        "Monthly Charge",
        "Total Charges",
        "Satisfaction Score",
        "Churn Score",
        "CLTV",
    ]

    metricas_existentes = [m for m in metricas if m in df_filtrado.columns]

    st.table(df_filtrado[metricas_existentes].describe().round(2))