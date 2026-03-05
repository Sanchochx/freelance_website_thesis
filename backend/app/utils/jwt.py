from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status

from app.config import settings


def create_access_token(user_id: int, rol: str) -> str:
    """
    Create a signed JWT with sub=user_id, rol, and exp=24h.

    CA2: returned on successful login.
    CA3: payload contains user_id, rol, and expiration timestamp.
    """
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {
        "sub": str(user_id),
        "rol": rol,
        "exp": expire,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT.

    CA7: raises 401 if token is missing, expired, or invalid.
    Returns the decoded payload dict.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
