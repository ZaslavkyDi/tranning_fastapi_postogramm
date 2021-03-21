from app.api.services.email import EmailSender
from app.backgroud.worker import celery
from app.core.enums import EmailMimeTypeEnum


# @celery.task()
def send_html_email(to: str, subject: str, html: str) -> None:
    email_sender = EmailSender()
    email_sender.send_email(
        to=to,
        subject=subject,
        content=html,
        mimetype=EmailMimeTypeEnum.html
    )
