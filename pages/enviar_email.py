import streamlit as st

from utils.charts import fig_to_bytes
from utils.data import carregar_dados
from utils.email_utils import enviar_email
from utils.report import gerar_relatorio_insights


def render():
    st.title("📧 Enviar Email")
    st.caption(
        "Envie o relatório de insights e/ou o último gráfico gerado por e-mail. "
        "Requer credenciais configuradas em `st.secrets['email']`."
    )

    destinatario = st.text_input("E-mail do destinatário")
    assunto = st.text_input("Assunto", value="Relatório de Análise de Churn")
    corpo = st.text_area(
        "Mensagem",
        value="Olá,\n\nSegue em anexo o relatório de análise de churn.\n\nAtenciosamente.",
        height=150,
    )

    incluir_relatorio = st.checkbox("Anexar relatório de insights (.txt)", value=True)
    incluir_grafico = st.checkbox(
        "Anexar último gráfico gerado na página 📈 Gráficos", value=False
    )

    if incluir_grafico and "ultimo_grafico_fig" not in st.session_state:
        st.warning(
            "Nenhum gráfico foi gerado ainda. Visite a página 📈 Gráficos antes de enviar."
        )

    if st.button("✉️ Enviar e-mail", type="primary"):
        if not destinatario:
            st.error("Informe o e-mail do destinatário.")
            return

        try:
            anexo_texto = None
            if incluir_relatorio:
                df = carregar_dados()
                anexo_texto = gerar_relatorio_insights(df)

            imagem_bytes = None
            if incluir_grafico and "ultimo_grafico_fig" in st.session_state:
                imagem_bytes = fig_to_bytes(st.session_state["ultimo_grafico_fig"])

            enviar_email(
                destinatario=destinatario,
                assunto=assunto,
                corpo=corpo,
                imagem_bytes=imagem_bytes,
                anexo_texto=anexo_texto,
            )
            st.success(f"E-mail enviado com sucesso para {destinatario}! ✅")
        except RuntimeError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"Falha ao enviar e-mail: {e}")
