from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import ClientRegisterRequest, FreelancerRegisterRequest, UserResponse
from app.services import auth_service
from app.utils.email import send_verification_email

router = APIRouter(prefix="/auth", tags=["auth"])


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
