# --- Importar Bibliotecas --- #
import plotly.express as px
import streamlit as st

from utils import (
    carregar_dados,
    montar_sidebar,
    saudacao,
    GRAFICOS_DISPONIVEIS,
)
# --- Configurações da página --- #
st.set_page_config(page_title="Gráficos | Análise de Churn", page_icon="📈", layout="wide")

montar_sidebar()
saudacao()

# --- Título da página --- #
st.title("📈 Gráficos de Análise de Churn")
st.caption("Visualizações interativas e estáticas sobre cancelamento de clientes.")

df = carregar_dados()


# --- Gráficos interativos (Plotly) --- #

st.markdown("## 🖱️ Gráficos interativos")

col1, col2 = st.columns(2)

with col1:
    churn_count = df["Churn Label"].value_counts().rename({"Yes": "Cancelou", "No": "Permaneceu"})
    fig1 = px.pie(
        names=churn_count.index,
        values=churn_count.values,
        title="Proporção de Clientes que Cancelaram",
        color=churn_count.index,
        color_discrete_map={"Cancelou": "#E84855", "Permaneceu": "#2E86AB"},
        hole=0.4,
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    receita_por_status = df.groupby("Customer Status")["Total Revenue"].sum().reset_index()
    fig2 = px.bar(
        receita_por_status,
        x="Customer Status",
        y="Total Revenue",
        title="Receita Total por Status do Cliente",
        color="Customer Status",
        color_discrete_sequence=px.colors.qualitative.Set2,
        text_auto=".2s",
    )
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

fig3 = px.scatter(
    df,
    x="Tenure in Months",
    y="Monthly Charge",
    color="Churn Label",
    title="Cobrança Mensal vs. Tempo de Permanência (por Churn)",
    color_discrete_map={"Yes": "#E84855", "No": "#2E86AB"},
    labels={"Churn Label": "Cancelou?"},
    opacity=0.6,
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

#  --- Gráficos estáticos (matplotlib) --- #
st.markdown("## 🖼️ Gráficos estáticos")
st.caption(
    "Estes são os mesmos gráficos que podem ser enviados por e-mail na página "
    "**📧 Envio por E-mail**."
)

cols = st.columns(2)
for i, (nome, funcao) in enumerate(GRAFICOS_DISPONIVEIS.items()):
    with cols[i % 2]:
        st.markdown(f"**{nome}**")
        fig = funcao(df)
        st.pyplot(fig, use_container_width=True)
