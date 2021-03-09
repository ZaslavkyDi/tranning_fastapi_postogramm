from sendgrid import Mail, SendGridAPIClient

from app.core.config import settings


# @celery.task()
def send_email(to: str, subject: str, html: str) -> None:
    sendgrid = SendGridAPIClient(settings.sendgrid_api_key)
    message = Mail(
        from_email=settings.email_from,
        to_emails=to,
        subject=subject,
        html_content=html
    )

    sendgrid.send(message)
