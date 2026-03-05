from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.config import settings

mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

fast_mail = FastMail(mail_config)


async def send_verification_email(email: str, nombre: str, token: str) -> None:
    """
    CA4: Send account verification email to the registered user.
    The link points to the frontend verification route.
    """
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"

    html_body = f"""
    <h2>Hola, {nombre}!</h2>
    <p>Gracias por registrarte en <strong>FreelanceUSTA</strong>.</p>
    <p>Para activar tu cuenta, haz clic en el siguiente enlace:</p>
    <p>
      <a href="{verification_url}" style="
        display:inline-block;padding:12px 24px;background:#4F46E5;
        color:#fff;text-decoration:none;border-radius:6px;
      ">
        Verificar mi cuenta
      </a>
    </p>
    <p>Si no te registraste en FreelanceUSTA, ignora este correo.</p>
    <hr/>
    <small>Este enlace es de un solo uso y expira en 24 horas.</small>
    """

    message = MessageSchema(
        subject="Verifica tu cuenta en FreelanceUSTA",
        recipients=[email],
        body=html_body,
        subtype=MessageType.html,
    )

    await fast_mail.send_message(message)
