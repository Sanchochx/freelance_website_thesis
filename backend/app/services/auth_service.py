import secrets
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import (
    ClientRegisterRequest,
    ForgotPasswordRequest,
    FreelancerRegisterRequest,
    LoginRequest,
    ResendVerificationRequest,
    ResetPasswordRequest,
)
from app.utils.jwt import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain-text password against its bcrypt hash."""
    return pwd_context.verify(plain, hashed)


VERIFICATION_TOKEN_TTL_HOURS = 24
RESET_TOKEN_TTL_HOURS = 1


def generate_verification_token() -> tuple[str, datetime]:
    """Generate a secure random token and its expiry (now + 24 h) for email verification."""
    token = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc) + timedelta(hours=VERIFICATION_TOKEN_TTL_HOURS)
    return token, expires


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

    verification_token, token_expires = generate_verification_token()

    user = User(
        nombre=data.nombre,
        email=data.email,
        password_hash=hash_password(data.password),  # CA3
        rol="freelancer",  # CA7
        carrera=data.carrera,
        semestre=data.semestre,
        verificado=False,  # CA5
        verification_token=verification_token,
        verification_token_expires=token_expires,  # CA2
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

    verification_token, token_expires = generate_verification_token()

    user = User(
        nombre=data.nombre,
        email=data.email,
        password_hash=hash_password(data.password),  # CA3
        rol="client",  # CA6
        empresa=data.empresa,
        verificado=False,  # CA5
        verification_token=verification_token,
        verification_token_expires=token_expires,  # CA2
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def verify_email_token(db: Session, token: str) -> None:
    """
    Verify the account using a one-time email token.

    - CA3: sets verificado=True and clears the token on success
    - CA5: raises 400 if token is not found, already used, or expired
    """
    user = db.query(User).filter(User.verification_token == token).first()

    # CA5 — token not found or already consumed
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El enlace de verificación no es válido o ya fue utilizado.",
        )

    # CA2 / CA5 — token expired
    if user.verification_token_expires is None or datetime.now(timezone.utc) > user.verification_token_expires:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El enlace de verificación ha expirado. Solicita uno nuevo.",
        )

    # CA3 — activate account and invalidate token
    user.verificado = True
    user.verification_token = None
    user.verification_token_expires = None
    db.commit()


def forgot_password(db: Session, data: ForgotPasswordRequest) -> tuple[str, str] | None:
    """
    Generate a password-reset token for the given email if the account exists.

    - CA3: always returns the same success message regardless of whether the email exists;
      returns (token, nombre) when found so the caller can send the email, None otherwise.
    - CA4: token expires in 1 hour.
    """
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        # CA3 — do not reveal whether the email is registered
        return None

    token = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc) + timedelta(hours=RESET_TOKEN_TTL_HOURS)

    user.reset_token = token
    user.reset_token_expires = expires
    db.commit()

    return token, user.nombre


def reset_password(db: Session, data: ResetPasswordRequest) -> None:
    """
    Reset the user's password using the one-time reset token.

    - CA5: accepts token + new_password; sets new hashed password.
    - CA6: password complexity validated in schema.
    - CA7: token is invalidated after use.
    - Raises 400 if token is invalid or expired.
    """
    user = db.query(User).filter(User.reset_token == data.token).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El enlace de restablecimiento no es válido o ya fue utilizado.",
        )

    if user.reset_token_expires is None or datetime.now(timezone.utc) > user.reset_token_expires:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El enlace de restablecimiento ha expirado. Solicita uno nuevo.",
        )

    # CA5 — update password hash
    user.password_hash = hash_password(data.new_password)
    # CA7 — invalidate token
    user.reset_token = None
    user.reset_token_expires = None
    db.commit()


def resend_verification(db: Session, data: ResendVerificationRequest) -> User:
    """
    Issue a new verification token for an unverified account.

    - CA6: generates a fresh token + expiry and returns the user so the
      caller can dispatch the email in a background task.
    - Raises 404 if email not found; raises 400 if already verified.
    """
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe una cuenta registrada con ese correo electrónico.",
        )

    if user.verificado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta cuenta ya está verificada.",
        )

    verification_token, token_expires = generate_verification_token()
    user.verification_token = verification_token
    user.verification_token_expires = token_expires
    db.commit()
    db.refresh(user)

    return user
