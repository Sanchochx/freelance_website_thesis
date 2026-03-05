from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import (
    ClientRegisterRequest,
    ForgotPasswordRequest,
    FreelancerRegisterRequest,
    LoginRequest,
    LoginResponse,
    ResendVerificationRequest,
    ResetPasswordRequest,
    UserResponse,
)
from app.services import auth_service
from app.utils.email import send_reset_password_email, send_verification_email

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Inicio de sesión con JWT",
)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Autentica al usuario y devuelve un JWT Bearer token.

    - CA1: recibe email y contraseña
    - CA2: devuelve token JWT válido si las credenciales son correctas
    - CA3: payload del JWT incluye user_id, rol y expiración a 24 horas
    - CA4: error 401 genérico si email o contraseña son incorrectos
    - CA5: error 403 con mensaje informativo si la cuenta no está verificada
    - CA6: el token se devuelve en el body; el cliente lo almacena en localStorage
    """
    return auth_service.login(db, data)


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Cierre de sesión",
)
def logout():
    """
    Cierre de sesión.

    - CA8: el token es stateless (JWT); el cliente debe eliminarlo de localStorage.
    Este endpoint confirma la intención de logout sin requerir autenticación.
    """
    return {"success": True, "message": "Sesión cerrada correctamente"}


@router.post(
    "/register/freelancer",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registro de estudiante freelancer",
)
async def register_freelancer(
    data: FreelancerRegisterRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Registra un nuevo estudiante freelancer.

    - Valida dominio @usantoto.edu.co (CA2)
    - Valida fortaleza de contraseña (CA3)
    - Hashea la contraseña con bcrypt (CA3)
    - Envía email de verificación en segundo plano (CA4)
    - Cuenta queda como no verificada (CA5)
    - Rechaza correos duplicados con 409 (CA6)
    - Asigna rol 'freelancer' automáticamente (CA7)
    """
    user = auth_service.register_freelancer(db, data)

    # CA4 — send verification email asynchronously
    background_tasks.add_task(
        send_verification_email,
        email=user.email,
        nombre=user.nombre,
        token=user.verification_token,
    )

    return user


@router.post(
    "/register/client",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registro de cliente externo",
)
async def register_client(
    data: ClientRegisterRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Registra un nuevo cliente externo (empresa o persona natural).

    - Acepta cualquier dominio de correo válido (CA2)
    - Valida fortaleza de contraseña (CA3)
    - Envía email de verificación en segundo plano (CA4)
    - Cuenta queda como no verificada (CA5)
    - Asigna rol 'client' automáticamente (CA6)
    - Rechaza correos duplicados con 409 (CA8)
    """
    user = auth_service.register_client(db, data)

    # CA4 — send verification email asynchronously
    background_tasks.add_task(
        send_verification_email,
        email=user.email,
        nombre=user.nombre,
        token=user.verification_token,
    )

    return user


@router.get(
    "/verify-email/{token}",
    status_code=status.HTTP_200_OK,
    summary="Verificación de correo electrónico",
)
def verify_email(token: str, db: Session = Depends(get_db)):
    """
    Verifica la cuenta usando el token de un solo uso enviado por email.

    - CA3: activa la cuenta (verificado=True) y elimina el token
    - CA4: retorna mensaje de éxito; el frontend redirige al login
    - CA5: retorna 400 si el token no existe, ya fue usado o expiró
    """
    auth_service.verify_email_token(db, token)
    return {"success": True, "message": "Cuenta verificada correctamente. Ya puedes iniciar sesión."}


@router.post(
    "/forgot-password",
    status_code=status.HTTP_200_OK,
    summary="Solicitud de restablecimiento de contraseña",
)
async def forgot_password(
    data: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Solicita el restablecimiento de contraseña.

    - CA2: envía un email con enlace de restablecimiento si el correo está registrado
    - CA3: siempre devuelve el mismo mensaje de éxito (no revela si el correo existe)
    - CA4: el token expira en 1 hora
    """
    result = auth_service.forgot_password(db, data)

    if result is not None:
        token, nombre = result
        background_tasks.add_task(
            send_reset_password_email,
            email=data.email,
            nombre=nombre,
            token=token,
        )

    # CA3 — always respond with success
    return {
        "success": True,
        "message": "Si ese correo está registrado, recibirás un enlace para restablecer tu contraseña.",
    }


@router.post(
    "/reset-password",
    status_code=status.HTTP_200_OK,
    summary="Restablecimiento de contraseña",
)
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Restablece la contraseña usando el token de un solo uso.

    - CA5: acepta token + nueva contraseña
    - CA6: valida complejidad de contraseña (mínimo 8 caracteres, mayúscula, número)
    - CA7: el token queda invalidado tras el uso
    - CA8: devuelve mensaje de éxito para que el frontend redirija al login
    """
    auth_service.reset_password(db, data)
    return {"success": True, "message": "Contraseña restablecida correctamente. Ya puedes iniciar sesión."}


@router.post(
    "/resend-verification",
    status_code=status.HTTP_200_OK,
    summary="Reenvío del email de verificación",
)
async def resend_verification(
    data: ResendVerificationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Genera un nuevo token de verificación y reenvía el email.

    - CA6: disponible para cuentas no verificadas; genera nuevo token con expiración
    """
    user = auth_service.resend_verification(db, data)

    background_tasks.add_task(
        send_verification_email,
        email=user.email,
        nombre=user.nombre,
        token=user.verification_token,
    )

    return {"success": True, "message": "Email de verificación reenviado. Revisa tu bandeja de entrada."}
