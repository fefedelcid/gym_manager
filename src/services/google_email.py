import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from mimetypes import guess_type
from src.utils import print_log
import os

def send_email_with_attachments(creds, to_email, subject, body_text, attachments=[]):
    """
    Envía un correo con adjuntos utilizando la API de Gmail y OAuth2.

    :param creds: Credenciales OAuth2 válidas.
    :param to_email: Dirección de destino.
    :param subject: Asunto del correo.
    :param body_text: Cuerpo del mensaje.
    :param attachments: Lista de rutas a archivos adjuntos.
    """
    try:
        # Crear mensaje
        message = EmailMessage()
        message.set_content(body_text)
        message["To"] = to_email
        message["From"] = "me"
        message["Subject"] = subject


        # Adjuntar archivos
        for filepath in attachments:
            if not os.path.isfile(filepath):
                print_log(f"❌ Archivo no encontrado: {filepath}")
                continue

            mime_type, _ = guess_type(filepath)
            maintype, subtype = mime_type.split("/") if mime_type else ("application", "octet-stream")

            with open(filepath, "rb") as f:
                file_data = f.read()
                filename = os.path.basename(filepath)

            message.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=filename)

        # Convertir a formato que Gmail espera
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Enviar con API
        service = build("gmail", "v1", credentials=creds)
        send_message = service.users().messages().send(
            userId="me",
            body={"raw": encoded_message}
        ).execute()

        print_log(f"📤 Correo enviado con ID: {send_message['id']}")
        return True

    except Exception as e:
        print_log(f"[ERROR] al enviar correo: {e}")
        return False