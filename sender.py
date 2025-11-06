"""
Módulo simple para construir y enviar correos vía SMTP usando la librería estándar.

Configuración desde variables de entorno:
- SMTP_HOST: host SMTP (ej: smtp.gmail.com)
- SMTP_PORT: puerto (ej: 587)
- SMTP_USER: usuario/login
- SMTP_PASSWORD: contraseña o app password
- FROM_EMAIL: dirección remitente
- TO_EMAIL: dirección(s) receptoras, separadas por comas
"""

import os
import smtplib
from email.message import EmailMessage
from typing import List


def _parse_recipients(recipients: str) -> List[str]:
    return [r.strip() for r in recipients.split(",") if r.strip()]


def build_message(subject: str, body: str, from_email: str, to_emails: List[str]) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = ", ".join(to_emails)
    msg.set_content(body)
    return msg


def send_email():
    """Envía un correo usando la configuración presente en variables de entorno.

    Lanza excepción si faltan variables obligatorias o si falla el envío.
    """
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    from_email = os.environ.get("FROM_EMAIL")
    to_email = os.environ.get("TO_EMAIL")

    if not all([smtp_host, smtp_user, smtp_password, from_email, to_email]):
        raise RuntimeError("Faltan variables de entorno SMTP. Revisa .env.example para la lista.")

    to_list = _parse_recipients(to_email)

    subject = os.environ.get("EMAIL_SUBJECT", "Correo automático")
    body = os.environ.get("EMAIL_BODY", "Este es un envío automático.")

    msg = build_message(subject, body, from_email, to_list)

    # Conexión y envío
    if smtp_port == 465:
        # SMTP sobre SSL/TLS
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
    else:
        # SMTP normal + STARTTLS
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            try:
                server.starttls()
                server.ehlo()
            except Exception:
                # algunos servidores no soportan STARTTLS; seguir sin él
                pass
            server.login(smtp_user, smtp_password)
            server.send_message(msg)


if __name__ == "__main__":
    # Prueba simple (requiere variables de entorno)
    try:
        send_email()
        print("Correo enviado (si la configuración SMTP es correcta)")
    except Exception as e:
        print(f"Error al enviar correo: {e}")
