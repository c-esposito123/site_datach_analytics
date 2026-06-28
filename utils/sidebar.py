import streamlit as st

from utils.sidebar import menu

from pages import (
    home,
    graficos,
    tabelas,
    download_relatorio,
    enviar_email,
)

st.set_page_config(page_title="DataCH Analytics", page_icon="📊", layout="wide")

pagina = menu()

if pagina == "🏠 Home":
    home.render()

elif pagina == "📈 Gráficos":
    graficos.render()

elif pagina == "📋 Tabelas":
    tabelas.render()

elif pagina == "⬇️ Download Relatório":
    download_relatorio.render()

elif pagina == "📧 Enviar Email":
    enviar_email.render()
