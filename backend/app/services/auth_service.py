import secrets

from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import FreelancerRegisterRequest

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
