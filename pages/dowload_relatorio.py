import datetime as dt

import streamlit as st

from utils import carregar_dados, montar_sidebar, saudacao, gerar_relatorio_insights, NOME_EMPRESA

st.set_page_config(page_title="Download | Análise de Churn", page_icon="📥", layout="wide")

montar_sidebar()
saudacao()

st.title("📥 Download do Relatório")
st.caption("Baixe o relatório completo de insights e análises sobre o churn de clientes em formato .txt.")

df = carregar_dados()
relatorio = gerar_relatorio_insights(df)

st.markdown("### Pré-visualização do relatório")
with st.container(border=True):
    st.text(relatorio)

st.markdown("### Baixar arquivo")

nome_arquivo = f"relatorio_churn_{dt.date.today().isoformat()}.txt"

st.download_button(
    label="⬇️ Baixar relatório (.txt)",
    data=relatorio,
    file_name=nome_arquivo,
    mime="text/plain",
    type="primary",
    use_container_width=True,
)

st.success(f"Relatório gerado por {NOME_EMPRESA} — clique no botão acima para salvar em seu computador.")
