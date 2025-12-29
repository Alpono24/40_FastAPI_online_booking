from fastapi import HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from core.config import MAIL_USERNAME, MAIL_PASSWORD
import logging
import os

logging.basicConfig(
    filename='log_send_mail.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_SERVER="smtp.mail.ru",
    MAIL_PORT=587,  # Используем порт 587 для STARTTLS
    MAIL_FROM=MAIL_USERNAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

fm = FastMail(conf)

async def send_confirmation_email(email: str, service_id: int) -> None:
    message = MessageSchema(
        subject=f"Подтверждение бронирования №{service_id}",
        recipients=[email],
        subtype="plain",
        body=f"Ваше бронирование подтверждено!"
    )
    try:
        await fm.send_message(message)
        logging.info(f"Письмо успешно отправлено на {email}.")
    except Exception as e:
        logging.error(f"Ошибка отправки письма: {e.__class__.__name__}: {e}")
        raise HTTPException(status_code=500, detail="Ошибка отправки письма")

