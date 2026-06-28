import streamlit as st
from utils import montar_sidebar, NOME_EMPRESA


def render():
    # Sidebar
    montar_sidebar()

    # Título
    st.title(f"📊 {NOME_EMPRESA}")

    st.subheader("Plataforma de Análise de Cancelamento de Clientes (Churn)")

    st.markdown(
        """
        Bem-vindo(a) à plataforma de análise de dados da **DataCH Analytics**.

        Somos uma empresa especializada em transformar dados brutos em decisões de negócio.
        Este painel foi desenvolvido para responder à pergunta que mais importa para empresas
        de serviços recorrentes: **por que nossos clientes estão cancelando — e o que podemos
        fazer sobre isso?**
        """
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🧭 O que você encontra aqui")
        st.markdown(
            """
            - **📋 Tabela** — visão estática e detalhada da base de clientes.
            - **📈 Gráficos** — visualizações interativas e estáticas sobre o churn.
            - **📧 Envio por E-mail** — envie um gráfico ou um relatório de insights.
            - **📥 Download do Relatório** — baixe a análise completa em `.txt`.
            """
        )

    with col2:
        st.markdown("### 🏢 Sobre a DataCH Analytics")
        st.markdown(
            """
            Fundada com o propósito de aproximar dados e decisões, a DataCH Analytics atua
            com diagnóstico de cancelamento de clientes (churn), modelagem preditiva e geração
            de relatórios executivos para empresas de telecomunicações, assinaturas e serviços.

            Nosso método combina estatística, visualização de dados e recomendações práticas
            — sempre orientadas pelo que os números realmente mostram.
            """
        )

    st.markdown("---")

    st.info(
        "👈 Use a barra lateral para informar seu nome e navegar entre as páginas do relatório.",
        icon="ℹ️",
    )