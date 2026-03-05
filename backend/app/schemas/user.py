import re
from typing import List, Optional

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


class ClientRegisterRequest(BaseModel):
    """Schema for external client registration — CA1–CA3, CA6."""

    nombre: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    empresa: Optional[str] = Field(None, max_length=150)

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
    empresa: Optional[str] = None
    verificado: bool
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    """Schema for login — CA1: email and password fields."""

    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Schema for successful login response — CA2, CA3."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class ResendVerificationRequest(BaseModel):
    """Schema for resend-verification endpoint — CA6."""

    email: EmailStr


class ServiceSummary(BaseModel):
    """Public summary of a freelancer's active service."""

    id: int
    titulo: str
    descripcion: Optional[str] = None
    precio_basico: Optional[float] = None
    precio_estandar: Optional[float] = None
    precio_premium: Optional[float] = None
    tiempo_entrega: Optional[int] = None
    imagenes: Optional[List[str]] = None
    categoria_id: Optional[int] = None

    model_config = {"from_attributes": True}


class ReviewSummary(BaseModel):
    """Public summary of a review left on a freelancer."""

    id: int
    reviewer_nombre: str
    rating: float
    comentario: Optional[str] = None
    fecha: str  # ISO-8601


class FreelancerProfileResponse(BaseModel):
    """Full public profile for a freelancer — US-005."""

    id: int
    nombre: str
    email: str
    carrera: Optional[str] = None
    semestre: Optional[int] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    habilidades: Optional[List[str]] = None
    portafolio: Optional[List[str]] = None
    badges: Optional[List[str]] = None
    verificado: bool
    fecha_registro: str  # ISO-8601
    avg_rating: Optional[float] = None  # None when no reviews (CA6)
    total_reviews: int
    services: List[ServiceSummary]
    reviews: List[ReviewSummary]


class OrderHistoryItem(BaseModel):
    """Completed order summary for a client profile — CA2 (no montos)."""

    id: int
    service_titulo: Optional[str] = None
    freelancer_nombre: str
    estado: str
    fecha_creacion: str  # ISO-8601


class ClientProfileResponse(BaseModel):
    """Public profile for a client — US-006. No email or wallet_balance (CA6)."""

    id: int
    nombre: str
    empresa: Optional[str] = None  # CA1
    avatar_url: Optional[str] = None
    fecha_registro: str  # ISO-8601 — CA1
    avg_rating: Optional[float] = None  # avg as client — CA1
    total_reviews: int
    total_contratados: int   # CA4
    total_completados: int   # CA4
    pedidos_completados: List[OrderHistoryItem]  # CA2
    reviews: List[ReviewSummary]  # CA3
