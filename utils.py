
import smtplib
import matplotlib.pyplot as plt
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

import io

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# --- Páginas de navegação --- #
pg = st.navigation(
    [
        st.Page('./pages/home.py', title='Página Inicial'),
        st.Page('./pages/graficopy', title='Gráficos'),
        st.Page('./pages/tabelas.py', title='Tabela'),
        st.Page('./pages/dowload_relatorio.py.py', title='Dowload do Relatório'),
        st.Page('./pages/enviar_email.py', title='Enviar e-mail')
    ],
    position='top'
)

plt.style.use("seaborn-v0_8-whitegrid")
PALETA = ["#2E86AB", "#E84855", "#F9A03F", "#3B1F2B", "#84BC9C"]

CSV_PATH = "base_projeto.csv"

NOME_EMPRESA = "DataCH Analytics"



@st.cache_data
def carregar_dados(caminho: str = CSV_PATH) -> pd.DataFrame:
    df = pd.read_csv("base_projeto.csv")

    # Normalização leve de tipos
    colunas_numericas = [
        "Age", "Number of Dependents", "Tenure in Months",
        "Avg Monthly Long Distance Charges", "Avg Monthly GB Download",
        "Monthly Charge", "Total Charges", "Total Refunds",
        "Total Extra Data Charges", "Total Long Distance Charges",
        "Total Revenue", "Satisfaction Score", "Churn Score", "CLTV",
    ]
    for col in colunas_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# --- Sidebar --- #
def montar_sidebar():
    st.sidebar.title("⚙️ Configurações")

    if "nome_usuario" not in st.session_state:
        st.session_state["nome_usuario"] = ""

    nome = st.sidebar.text_input(
        "Seu nome",
        value=st.session_state["nome_usuario"],
        placeholder="Digite seu nome...",
        key="input_nome_sidebar",
    )
    st.session_state["nome_usuario"] = nome

    st.sidebar.markdown("---")
    st.sidebar.caption(f"📊 {NOME_EMPRESA}")
    st.sidebar.caption("Plataforma de Análise de Churn")


def saudacao():
    nome = st.session_state.get("nome_usuario", "").strip()
    if nome:
        st.markdown(f"#### 👋 Olá, **{nome}**! Seja bem-vindo(a) de volta.")
    else:
        st.markdown("#### 👋 Olá! Que bom ter você aqui.")
        st.caption("Dica: preencha seu nome na barra lateral para uma experiência personalizada.")
    st.markdown("")


# --- Relatórios --- #
def gerar_relatorio_insights(df: pd.DataFrame) -> str:
    total_clientes = len(df)
    churn_label = df["Churn Label"].astype(str).str.strip()
    qtd_churn = (churn_label == "Yes").sum()
    taxa_churn = (qtd_churn / total_clientes * 100) if total_clientes else 0

    receita_perdida = df.loc[churn_label == "Yes", "Total Revenue"].sum()
    ticket_medio_churn = df.loc[churn_label == "Yes", "Monthly Charge"].mean()
    ticket_medio_geral = df["Monthly Charge"].mean()

    motivo_top = (
        df.loc[churn_label == "Yes", "Churn Category"]
        .value_counts()
        .head(3)
    )

    contrato_churn = (
        df.loc[churn_label == "Yes", "Contract"]
        .value_counts(normalize=True)
        .mul(100)
        .round(1)
    )

    satisfacao_media_churn = df.loc[churn_label == "Yes", "Satisfaction Score"].mean()
    satisfacao_media_geral = df["Satisfaction Score"].mean()

    tenure_medio_churn = df.loc[churn_label == "Yes", "Tenure in Months"].mean()
    tenure_medio_geral = df["Tenure in Months"].mean()

    linhas = []
    linhas.append(f"RELATÓRIO DE ANÁLISE DE CHURN — {NOME_EMPRESA}")
    linhas.append("=" * 60)
    linhas.append("")
    linhas.append("1. VISÃO GERAL")
    linhas.append(f"   - Total de clientes na base: {total_clientes}")
    linhas.append(f"   - Clientes que cancelaram (churn): {qtd_churn}")
    linhas.append(f"   - Taxa de churn: {taxa_churn:.1f}%")
    linhas.append(f"   - Receita total perdida com cancelamentos: ${receita_perdida:,.2f}")
    linhas.append("")
    linhas.append("2. PRINCIPAIS MOTIVOS DE CANCELAMENTO")
    for motivo, qtd in motivo_top.items():
        linhas.append(f"   - {motivo}: {qtd} casos")
    linhas.append("")
    linhas.append("3. PERFIL DE QUEM CANCELA")
    linhas.append(
        f"   - Ticket médio mensal de quem cancelou: ${ticket_medio_churn:,.2f} "
        f"(vs. ${ticket_medio_geral:,.2f} da base geral)"
    )
    linhas.append(
        f"   - Satisfação média de quem cancelou: {satisfacao_media_churn:.1f} "
        f"(vs. {satisfacao_media_geral:.1f} da base geral)"
    )
    linhas.append(
        f"   - Tempo médio de permanência de quem cancelou: {tenure_medio_churn:.1f} meses "
        f"(vs. {tenure_medio_geral:.1f} meses da base geral)"
    )
    linhas.append("   - Distribuição de tipo de contrato entre quem cancelou:")
    for contrato, pct in contrato_churn.items():
        linhas.append(f"        * {contrato}: {pct}%")
    linhas.append("")
    linhas.append("4. INTERPRETAÇÃO")
    linhas.append(
        "   Os dados indicam que o cancelamento está fortemente concentrado em clientes com"
    )
    linhas.append(
        "   contratos mensais (Month-to-Month), menor tempo de permanência e nota de satisfação"
    )
    linhas.append(
        "   mais baixa do que a média da base. Os motivos mais citados envolvem concorrência"
    )
    linhas.append(
        "   (ofertas melhores de outras empresas) e insatisfação com o serviço prestado, o que"
    )
    linhas.append(
        "   sugere um problema de percepção de valor frente ao preço cobrado."
    )
    linhas.append("")
    linhas.append("5. RECOMENDAÇÕES BASEADAS EM DADOS")
    linhas.append(
        "   - Incentivar a migração de contratos mensais para contratos de 1 ou 2 anos,"
    )
    linhas.append(
        "     oferecendo descontos ou benefícios que compensem o compromisso de prazo maior."
    )
    linhas.append(
        "   - Criar um programa de retenção direcionado aos clientes nos primeiros meses"
    )
    linhas.append(
        "     de relacionamento, período em que o risco de cancelamento é mais alto."
    )
    linhas.append(
        "   - Monitorar de forma proativa clientes com Satisfaction Score baixo e Churn Score"
    )
    linhas.append(
        "     elevado, oferecendo suporte ou condições especiais antes do cancelamento."
    )
    linhas.append(
        "   - Revisar a política de preços e ofertas em segmentos onde a concorrência é citada"
    )
    linhas.append(
        "     como motivo principal de saída, especialmente em planos de Fibra Óptica."
    )
    linhas.append(
        "   - Investir em qualidade de serviço (suporte técnico, segurança online e backup),"
    )
    linhas.append(
        "     já que clientes sem esses adicionais tendem a cancelar mais."
    )
    linhas.append("")
    linhas.append("=" * 60)
    linhas.append(f"Relatório gerado automaticamente por {NOME_EMPRESA}.")

    return "\n".join(linhas)


# --- Gráficos --- #
def fig_to_bytes(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=160, bbox_inches="tight")
    buf.seek(0)
    return buf.read()


def grafico_churn_geral(df: pd.DataFrame):
    contagem = df["Customer Status"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.bar(contagem.index, contagem.values, color=PALETA[:len(contagem)])
    ax.set_title("Distribuição de Clientes por Status", fontsize=13, fontweight="bold")
    ax.set_ylabel("Quantidade de clientes")
    for i, v in enumerate(contagem.values):
        ax.text(i, v + max(contagem.values) * 0.01, str(v), ha="center", fontweight="bold")
    fig.tight_layout()
    return fig


def grafico_motivos_churn(df: pd.DataFrame):
    churn = df[df["Churn Label"] == "Yes"]
    contagem = churn["Churn Category"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.barh(contagem.index[::-1], contagem.values[::-1], color=PALETA[1])
    ax.set_title("Motivos de Cancelamento por Categoria", fontsize=13, fontweight="bold")
    ax.set_xlabel("Quantidade de clientes")
    fig.tight_layout()
    return fig


def grafico_churn_por_contrato(df: pd.DataFrame):
    tab = pd.crosstab(df["Contract"], df["Churn Label"], normalize="index") * 100
    fig, ax = plt.subplots(figsize=(6, 4.5))
    tab.plot(kind="bar", stacked=True, ax=ax, color=[PALETA[4], PALETA[1]])
    ax.set_title("Taxa de Churn por Tipo de Contrato (%)", fontsize=13, fontweight="bold")
    ax.set_ylabel("Percentual de clientes (%)")
    ax.set_xlabel("")
    ax.legend(title="Churn", labels=["Não", "Sim"])
    plt.setp(ax.get_xticklabels(), rotation=0)
    fig.tight_layout()
    return fig


def grafico_satisfacao_vs_churn(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6, 4.5))
    dados = [
        df.loc[df["Churn Label"] == "No", "Satisfaction Score"].dropna(),
        df.loc[df["Churn Label"] == "Yes", "Satisfaction Score"].dropna(),
    ]
    bp = ax.boxplot(dados, labels=["Permaneceu", "Cancelou"], patch_artist=True)
    for patch, cor in zip(bp["boxes"], [PALETA[4], PALETA[1]]):
        patch.set_facecolor(cor)
    ax.set_title("Satisfação do Cliente vs. Churn", fontsize=13, fontweight="bold")
    ax.set_ylabel("Satisfaction Score")
    fig.tight_layout()
    return fig


GRAFICOS_DISPONIVEIS = {
    "Distribuição de clientes por status": grafico_churn_geral,
    "Motivos de cancelamento": grafico_motivos_churn,
    "Churn por tipo de contrato": grafico_churn_por_contrato,
    "Satisfação vs. churn": grafico_satisfacao_vs_churn,
}
