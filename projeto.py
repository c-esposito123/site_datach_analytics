import streamlit as st

pg = st.navigation(
    [
        st.Page("pages/home.py", title="🏠 Página Inicial"),
        st.Page("pages/graficos.py", title="📈 Gráficos"),
        st.Page("pages/tabelas.py", title="📋 Tabelas"),
        st.Page("pages/dowload_relatorio.py", title="📄 Download do Relatório"),
        st.Page("pages/enviar_email.py", title="📧 Enviar E-mail"),
    ],
    position="top",
)

pg.run()