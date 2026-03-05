from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.order import Order
from app.models.service import Service
from app.utils.cloudinary import delete_cloudinary_image

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


def update_service_status(db: Session, service_id: int, current_user_id: int, nuevo_estado: str) -> Service:
    """
    Pause or reactivate a service owned by current_user_id.

    - CA1: sets estado='pausado' (service hidden from catalog).
    - CA3: sets estado='activo' (service visible again).
    """
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servicio no encontrado.")

    if service.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para modificar este servicio.",
        )

    service.estado = nuevo_estado
    db.commit()
    db.refresh(service)
    return service


def delete_service(db: Session, service_id: int, current_user_id: int) -> None:
    """
    Soft-delete a service by setting estado='eliminado'.

    - CA4: allowed only when no active orders exist.
    - CA5: raises 400 with explanation if active orders are found.
    - CA6: record is preserved in DB (soft delete); historical orders kept.
    """
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servicio no encontrado.")

    if service.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar este servicio.",
        )

    # CA4/CA5 — block deletion if active orders exist
    active_orders = (
        db.query(Order)
        .filter(
            Order.service_id == service_id,
            Order.estado.notin_(["completado", "cancelado"]),
        )
        .count()
    )
    if active_orders > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "No puedes eliminar este servicio porque tiene pedidos activos. "
                "Espera a que todos los pedidos finalicen antes de eliminar el servicio."
            ),
        )

    # CA6 — soft delete (preserves record and historical orders)
    service.estado = "eliminado"
    db.commit()


def update_service(
    db: Session,
    service_id: int,
    current_user_id: int,
    titulo: Optional[str] = None,
    descripcion: Optional[str] = None,
    categoria_id: Optional[int] = None,
    precio_basico: Optional[float] = None,
    precio_estandar: Optional[float] = None,
    precio_premium: Optional[float] = None,
    tiempo_entrega: Optional[int] = None,
    keep_images: Optional[List[str]] = None,
    new_image_urls: Optional[List[str]] = None,
) -> Service:
    """
    Update an existing service owned by current_user_id.

    - CA1: raises 403 if the requester is not the service owner.
    - CA2: all fields are optional; only provided ones are updated.
    - CA3: changes are immediately visible (committed to DB).
    - CA4: raises 400 if service has any order in 'en_progreso'.
    - CA5: computes final image list from keep_images + new_image_urls;
           deletes from Cloudinary any removed images.
    - CA6: price changes don't affect existing orders (orders store their own price).
    """
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servicio no encontrado.")

    # CA1 — ownership check
    if service.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para editar este servicio.",
        )

    # CA4 — block edit if orders are in progress
    orders_in_progress = (
        db.query(Order)
        .filter(Order.service_id == service_id, Order.estado == "en_progreso")
        .count()
    )
    if orders_in_progress > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "No puedes editar este servicio mientras tenga pedidos en progreso. "
                "Espera a que finalicen antes de hacer cambios."
            ),
        )

    # CA6 — validate categoria if provided
    if categoria_id is not None:
        category = db.query(Category).filter(Category.id == categoria_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La categoría seleccionada no es válida.",
            )

    # CA5 — image management
    if keep_images is not None or new_image_urls:
        original_images = service.imagenes or []
        kept = keep_images if keep_images is not None else original_images
        final_images = list(kept) + (new_image_urls or [])

        if len(final_images) < 1 or len(final_images) > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El servicio debe tener entre 1 y 5 imágenes.",
            )

        # Delete from Cloudinary any images that were removed
        for url in original_images:
            if url not in kept:
                delete_cloudinary_image(url)

        service.imagenes = final_images

    # Apply field updates
    if titulo is not None:
        service.titulo = titulo
    if descripcion is not None:
        service.descripcion = descripcion
    if categoria_id is not None:
        service.categoria_id = categoria_id
    if precio_basico is not None:
        service.precio_basico = precio_basico
    if precio_estandar is not None:
        service.precio_estandar = precio_estandar
    if precio_premium is not None:
        service.precio_premium = precio_premium
    if tiempo_entrega is not None:
        service.tiempo_entrega = tiempo_entrega

    db.commit()
    db.refresh(service)

    return service
