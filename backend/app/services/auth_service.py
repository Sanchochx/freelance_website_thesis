import secrets

from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import ClientRegisterRequest, FreelancerRegisterRequest, LoginRequest
from app.utils.jwt import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain-text password against its bcrypt hash."""
    return pwd_context.verify(plain, hashed)


def generate_verification_token() -> str:
    """Generate a secure random token for email verification."""
    return secrets.token_urlsafe(32)


def register_freelancer(db: Session, data: FreelancerRegisterRequest) -> User:
    """
    Register a new freelancer.

    - CA3: password is hashed with bcrypt
    - CA5: account starts as unverified (verificado=False)
    - CA6: raises 409 if email already exists
    - CA7: rol is set to 'freelancer'
    """
    # CA6 — duplicate email check
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una cuenta registrada con ese correo electrónico",
        )

    verification_token = generate_verification_token()

    user = User(
        nombre=data.nombre,
        email=data.email,
        password_hash=hash_password(data.password),  # CA3
        rol="freelancer",  # CA7
        carrera=data.carrera,
        semestre=data.semestre,
        verificado=False,  # CA5
        verification_token=verification_token,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login(db: Session, data: LoginRequest) -> dict:
    """
    Authenticate a user and return a JWT.

    - CA2: returns a valid JWT on success
    - CA3: JWT payload contains sub=user_id, rol, exp
    - CA4: returns generic 401 if email or password is wrong (no field hint)
    - CA5: returns 403 with resend hint if account is not verified
    """
    # CA4 — look up user; use same error for wrong email or wrong password
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # CA5 — account must be verified
    if not user.verificado:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Tu cuenta aún no ha sido verificada. "
                "Revisa tu correo o solicita un nuevo enlace de verificación."
            ),
        )

    # CA2, CA3 — generate token
    token = create_access_token(user_id=user.id, rol=user.rol)

    return {"access_token": token, "token_type": "bearer", "user": user}


def register_client(db: Session, data: ClientRegisterRequest) -> User:
    """
    Register a new external client.

    - CA3: password is hashed with bcrypt
    - CA5: account starts as unverified (verificado=False)
    - CA6: rol is set to 'client'
    - CA8: raises 409 if email already exists
    """
    # CA8 — duplicate email check
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una cuenta registrada con ese correo electrónico",
        )

    verification_token = generate_verification_token()

    user = User(
        nombre=data.nombre,
        email=data.email,
        password_hash=hash_password(data.password),  # CA3
        rol="client",  # CA6
        empresa=data.empresa,
        verificado=False,  # CA5
        verification_token=verification_token,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
