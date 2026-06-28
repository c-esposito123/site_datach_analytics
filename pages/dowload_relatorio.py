import streamlit as st

from utils.data import carregar_dados
from utils.report import gerar_relatorio_insights


def render():
    st.title("⬇️ Download Relatório")

    try:
        df = carregar_dados()
    except FileNotFoundError:
        st.error("Arquivo `base_projeto.csv` não encontrado na raiz do projeto.")
        return

    relatorio = gerar_relatorio_insights(df)

    st.text_area("Pré-visualização do relatório", relatorio, height=400)

    st.download_button(
        label="⬇️ Baixar relatório (.txt)",
        data=relatorio.encode("utf-8"),
        file_name="relatorio_churn.txt",
        mime="text/plain",
    )

    # Guarda na sessão para reaproveitar na página de e-mail
    st.session_state["ultimo_relatorio_texto"] = relatorio
