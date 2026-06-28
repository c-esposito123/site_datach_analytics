import streamlit as st

from utils.data import carregar_dados


def render():
    st.title("📋 Tabelas")

    try:
        df = carregar_dados()
    except FileNotFoundError:
        st.error("Arquivo `base_projeto.csv` não encontrado na raiz do projeto.")
        return

    with st.expander("🔍 Filtros", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            status_opts = sorted(df["Customer Status"].dropna().unique().tolist())
            status_sel = st.multiselect("Status do cliente", status_opts, default=status_opts)
        with col2:
            contrato_opts = sorted(df["Contract"].dropna().unique().tolist())
            contrato_sel = st.multiselect("Tipo de contrato", contrato_opts, default=contrato_opts)

    df_filtrado = df[
        df["Customer Status"].isin(status_sel) & df["Contract"].isin(contrato_sel)
    ]

    st.caption(f"Exibindo {len(df_filtrado):,} de {len(df):,} registros")
    st.dataframe(df_filtrado, use_container_width=True)