# "Your turn" item 2 - finish send_welcome_email. See LESSON.md Step 4 for
# the exact pattern.

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from config import settings

mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)


async def send_welcome_email(to_email: str) -> None:
    # TODO: build a MessageSchema (subject="Welcome to the Students API!",
    # recipients=[to_email], body="Thanks for registering. Your account is
    # ready.", subtype=MessageType.plain), then
    # await FastMail(mail_config).send_message(message)
    pass
