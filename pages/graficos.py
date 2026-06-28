import streamlit as st

from utils.charts import GRAFICOS_DISPONIVEIS
from utils.data import carregar_dados


def render():
    st.title("📈 Gráficos")

    try:
        df = carregar_dados()
    except FileNotFoundError:
        st.error("Arquivo `base_projeto.csv` não encontrado na raiz do projeto.")
        return

    escolha = st.selectbox("Selecione o gráfico", list(GRAFICOS_DISPONIVEIS.keys()))

    fig = GRAFICOS_DISPONIVEIS[escolha](df)
    st.pyplot(fig)

    # Guarda na sessão para reaproveitar na página de e-mail
    st.session_state["ultimo_grafico_nome"] = escolha
    st.session_state["ultimo_grafico_fig"] = fig
