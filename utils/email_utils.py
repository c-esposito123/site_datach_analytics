import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import streamlit as st


def enviar_email(
    destinatario: str,
    assunto: str,
    corpo: str,
    imagem_bytes: bytes | None = None,
    imagem_nome: str = "grafico.png",
    anexo_texto: str | None = None,
    anexo_texto_nome: str = "relatorio.txt",
):
    try:
        remetente = st.secrets["email"]["remetente"]
        senha_app = st.secrets["email"]["senha_app"]
        servidor_smtp = st.secrets["email"].get("servidor_smtp", "smtp.gmail.com")
        porta_smtp = int(st.secrets["email"].get("porta_smtp", 587))
    except Exception as exc:
        raise RuntimeError(
            "Credenciais de e-mail não configuradas em st.secrets. "
            "Configure o arquivo .streamlit/secrets.toml (local) ou os Secrets do app no Streamlit Cloud."
        ) from exc

    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto

    msg.attach(MIMEText(corpo, "plain", "utf-8"))

    if imagem_bytes is not None:
        img = MIMEImage(imagem_bytes, name=imagem_nome)
        img.add_header("Content-Disposition", "attachment", filename=imagem_nome)
        msg.attach(img)

    if anexo_texto is not None:
        anexo = MIMEApplication(anexo_texto.encode("utf-8"), Name=anexo_texto_nome)
        anexo.add_header("Content-Disposition", "attachment", filename=anexo_texto_nome)
        msg.attach(anexo)

    contexto = ssl.create_default_context()
    with smtplib.SMTP(servidor_smtp, porta_smtp) as servidor:
        servidor.starttls(context=contexto)
        servidor.login(remetente, senha_app)
        servidor.sendmail(remetente, destinatario, msg.as_string())
