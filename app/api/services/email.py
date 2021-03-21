import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings
from app.core.enums import EmailMimeTypeEnum


class EmailSender:
    def __init__(self):
        self._context = ssl.create_default_context()

    def send_email(self, to: str, subject: str, content: str, mimetype: EmailMimeTypeEnum) -> None:
        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = settings.email_sender
        message["To"] = to

        payload = MIMEText(content, mimetype.value)
        message.attach(payload)

        with smtplib.SMTP_SSL(settings.smtp_server, settings.smtp_server_port, context=self._context) as server:
            server.login(user=settings.email_sender, password=settings.email_password)
            server.sendmail(
                from_addr=settings.email_sender,
                to_addrs=to,
                msg=message.as_string()
            )
