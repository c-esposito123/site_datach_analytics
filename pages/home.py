import streamlit as st

from utils.data import carregar_dados
from utils.sidebar import saudacao


def render():
    saudacao()

    st.title("🏠 Home — DataCH Analytics")
    st.markdown(
        "Bem-vindo à plataforma de análise de **churn de clientes**. "
        "Use o menu lateral para navegar entre gráficos, tabelas, download do relatório e envio por e-mail."
    )

    try:
        df = carregar_dados()
    except FileNotFoundError:
        st.error("Arquivo `base_projeto.csv` não encontrado na raiz do projeto.")
        return

    total_clientes = len(df)
    churn_label = df["Churn Label"].astype(str).str.strip()
    qtd_churn = int((churn_label == "Yes").sum())
    taxa_churn = (qtd_churn / total_clientes * 100) if total_clientes else 0
    receita_perdida = df.loc[churn_label == "Yes", "Total Revenue"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de clientes", f"{total_clientes:,}")
    col2.metric("Clientes em churn", f"{qtd_churn:,}")
    col3.metric("Taxa de churn", f"{taxa_churn:.1f}%")
    col4.metric("Receita perdida", f"${receita_perdida:,.0f}")

    st.markdown("---")
    st.markdown("#### Navegação rápida")
    st.markdown(
        "- **📈 Gráficos** — visualizações sobre o comportamento de churn\n"
        "- **📋 Tabelas** — dados detalhados e filtráveis\n"
        "- **⬇️ Download Relatório** — relatório de insights em texto\n"
        "- **📧 Enviar Email** — compartilhe gráficos e relatórios por e-mail"
    )
