from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.service import Service

MAX_ACTIVE_SERVICES = 10


def create_service(
    db: Session,
    user_id: int,
    titulo: str,
    descripcion: str,
    categoria_id: int,
    precio_basico: float,
    tiempo_entrega: int,
    imagen_urls: List[str],
    precio_estandar: Optional[float] = None,
    precio_premium: Optional[float] = None,
) -> Service:
    """
    Create a new service for a verified freelancer.

    - CA4: service is created with estado='activo' by default.
    - CA6: raises 400 if categoria_id is not one of the 8 valid categories.
    - CA7: service is immediately visible in the catalog (estado='activo').
    - CA8: raises 400 if the freelancer already has 10 active services.
    """
    # CA8 — active service limit
    active_count = (
        db.query(Service)
        .filter(Service.user_id == user_id, Service.estado == "activo")
        .count()
    )
    if active_count >= MAX_ACTIVE_SERVICES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes tener más de 10 servicios activos simultáneamente.",
        )

    # CA6 — category must exist in the 8 available categories
    category = db.query(Category).filter(Category.id == categoria_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La categoría seleccionada no es válida.",
        )

    # CA4 — estado='activo' by default
    service = Service(
        user_id=user_id,
        titulo=titulo,
        descripcion=descripcion,
        categoria_id=categoria_id,
        precio_basico=precio_basico,
        precio_estandar=precio_estandar,
        precio_premium=precio_premium,
        tiempo_entrega=tiempo_entrega,
        imagenes=imagen_urls,
        estado="activo",
    )

    db.add(service)
    db.commit()
    db.refresh(service)

    return service
