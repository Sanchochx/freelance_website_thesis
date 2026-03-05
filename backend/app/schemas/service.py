from typing import List, Literal, Optional

from pydantic import BaseModel


class CategoryResponse(BaseModel):
    """Public category data."""

    id: int
    nombre: str
    icono: Optional[str] = None

    model_config = {"from_attributes": True}


class ServiceResponse(BaseModel):
    """Full service data returned after creation or on detail view — US-009."""

    id: int
    user_id: int
    titulo: str
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None
    precio_basico: Optional[float] = None
    precio_estandar: Optional[float] = None
    precio_premium: Optional[float] = None
    tiempo_entrega: Optional[int] = None
    imagenes: Optional[List[str]] = None
    estado: str
    fecha_creacion: str  # ISO-8601

    model_config = {"from_attributes": True}


class ServiceStatusUpdateRequest(BaseModel):
    """Body for PATCH /services/{id}/status — CA1, CA3."""

    estado: Literal["activo", "pausado"]
