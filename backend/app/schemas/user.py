import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


INSTITUTIONAL_EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9._%+\-]+@usantoto\.edu\.co$"
)

PASSWORD_REGEX = re.compile(
    r"^(?=.*[A-Z])(?=.*\d).{8,}$"
)


class FreelancerRegisterRequest(BaseModel):
    """Schema for freelancer registration — CA1, CA2, CA3."""

    nombre: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    carrera: str = Field(..., min_length=2, max_length=100)
    semestre: int = Field(..., ge=1, le=12)

    @field_validator("email")
    @classmethod
    def validate_institutional_email(cls, v: str) -> str:
        """CA2: email must belong to @usantoto.edu.co domain."""
        if not INSTITUTIONAL_EMAIL_REGEX.match(v):
            raise ValueError(
                "El correo debe pertenecer al dominio institucional @usantoto.edu.co"
            )
        return v.lower()

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """CA3: at least 8 chars, one uppercase, one digit."""
        if not PASSWORD_REGEX.match(v):
            raise ValueError(
                "La contraseña debe tener mínimo 8 caracteres, "
                "al menos una mayúscula y un número"
            )
        return v


class UserResponse(BaseModel):
    """Public user data — never exposes password_hash."""

    id: int
    nombre: str
    email: str
    rol: str
    carrera: Optional[str] = None
    semestre: Optional[int] = None
    verificado: bool
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

    model_config = {"from_attributes": True}
