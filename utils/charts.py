import io

import matplotlib.pyplot as plt
import pandas as pd

plt.style.use("seaborn-v0_8-whitegrid")
PALETA = ["#2E86AB", "#E84855", "#F9A03F", "#3B1F2B", "#84BC9C"]


def fig_to_bytes(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=160, bbox_inches="tight")
    buf.seek(0)
    return buf.read()


def grafico_churn_geral(df: pd.DataFrame):
    contagem = df["Customer Status"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.bar(contagem.index, contagem.values, color=PALETA[: len(contagem)])
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
