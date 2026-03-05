from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.utils.jwt import decode_access_token

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Dependency that validates the Bearer JWT and returns the authenticated user.

    CA7: protected routes reject requests with missing or invalid tokens with 401.
    Usage: add `current_user: User = Depends(get_current_user)` to any endpoint.
    """
    payload = decode_access_token(credentials.credentials)

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: falta el identificador de usuario",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El usuario asociado al token no existe",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def require_role(*roles: str):
    """
    Dependency factory that enforces one of the given roles.

    Usage: `current_user: User = Depends(require_role('freelancer', 'admin'))`
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.rol not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para realizar esta acción",
            )
        return current_user
    return role_checker


def require_verified_freelancer(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency that ensures the current user is a verified freelancer.

    US-004 CA7: an unverified freelancer cannot publish services.
    Usage: add `current_user: User = Depends(require_verified_freelancer)` to service-creation endpoints.
    """
    if current_user.rol != "freelancer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los freelancers pueden realizar esta acción",
        )
    if not current_user.verificado:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Debes verificar tu correo electrónico antes de publicar servicios",
        )
    return current_user
