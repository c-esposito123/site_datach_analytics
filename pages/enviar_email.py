import datetime as dt
import streamlit as st

from utils import (
    carregar_dados,
    saudacao,
    gerar_relatorio_insights,
    enviar_email,
    fig_to_bytes,
    GRAFICOS_DISPONIVEIS,
    NOME_EMPRESA,
)


def render():
    # --- Título ---
    st.title("📧 Envio de Análises por E-mail")
    st.caption(
        "Escolha entre enviar um gráfico estático ou o relatório de insights escrito, "
        "e receba diretamente no seu e-mail."
    )

    # Saudação global
    saudacao()

    df = carregar_dados()

    # --- Escolha do tipo ---
    st.markdown("### 1. O que você deseja enviar?")

    opcao = st.radio(
        "Tipo de conteúdo",
        [
            "📊 Gráfico estático (imagem em anexo)",
            "📝 Relatório de insights (texto)",
        ],
        horizontal=True,
    )

    # --- Destinatário ---
    st.markdown("### 2. Detalhes do envio")

    destinatario = st.text_input(
        "E-mail de destino",
        placeholder="seuemail@exemplo.com",
    )

    imagem_bytes = None
    imagem_nome = "grafico.png"
    corpo_extra = ""

    # --- Conteúdo dinâmico ---
    if opcao.startswith("📊"):
        grafico_escolhido = st.selectbox(
            "Selecione o gráfico",
            list(GRAFICOS_DISPONIVEIS.keys()),
        )

        fig = GRAFICOS_DISPONIVEIS[grafico_escolhido](df)
        st.pyplot(fig, use_container_width=True)

        imagem_bytes = fig_to_bytes(fig)
        imagem_nome = f"{grafico_escolhido.lower().replace(' ', '_')}.png"

        corpo_extra = f"Segue em anexo o gráfico: '{grafico_escolhido}'."

    else:
        relatorio = gerar_relatorio_insights(df)

        with st.expander("👀 Pré-visualizar relatório de insights", expanded=True):
            st.text(relatorio)

        corpo_extra = (
            "Segue em anexo o relatório de insights e análises sobre o churn de clientes."
        )

    # --- Envio ---
    st.markdown("### 3. Enviar")

    assunto = f"Relatório de Análise de Churn — {NOME_EMPRESA}"

    if st.button("📨 Enviar e-mail", type="primary", use_container_width=True):

        if not destinatario:
            st.error("Informe um e-mail de destino válido.")

        else:
            corpo = (
                f"Olá,\n\n"
                f"{corpo_extra}\n\n"
                f"Este conteúdo foi gerado automaticamente pela plataforma de análise de churn "
                f"da {NOME_EMPRESA} em {dt.date.today().strftime('%d/%m/%Y')}.\n\n"
                f"Atenciosamente,\n"
                f"Equipe {NOME_EMPRESA}"
            )

            try:
                if opcao.startswith("📊"):
                    enviar_email(
                        destinatario=destinatario,
                        assunto=assunto,
                        corpo=corpo,
                        imagem_bytes=imagem_bytes,
                        imagem_nome=imagem_nome,
                    )
                else:
                    relatorio = gerar_relatorio_insights(df)
                    enviar_email(
                        destinatario=destinatario,
                        assunto=assunto,
                        corpo=corpo,
                        anexo_texto=relatorio,
                        anexo_texto_nome="relatorio_insights_churn.txt",
                    )

                st.success(f"E-mail enviado com sucesso para {destinatario}! ✅")

            except Exception as e:
                st.error(f"Não foi possível enviar o e-mail: {e}")
                st.info(
                    "Configure SMTP no Streamlit Secrets (.streamlit/secrets.toml "
                    "ou Settings → Secrets no Streamlit Cloud)."
                )