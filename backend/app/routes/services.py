from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth import get_current_user, require_verified_freelancer
from app.models.user import User
from app.schemas.service import ServiceResponse
from app.services import service_service
from app.utils.cloudinary import upload_service_image

router = APIRouter(prefix="/services", tags=["services"])


@router.post(
    "",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo servicio",
)
async def create_service(
    titulo: str = Form(..., max_length=100),
    descripcion: str = Form(..., max_length=1200),
    categoria_id: int = Form(...),
    precio_basico: float = Form(..., gt=0),
    precio_estandar: Optional[float] = Form(None, gt=0),
    precio_premium: Optional[float] = Form(None, gt=0),
    tiempo_entrega: int = Form(..., ge=1),
    imagenes: List[UploadFile] = File(...),
    current_user: User = Depends(require_verified_freelancer),
    db: Session = Depends(get_db),
):
    """
    Crea un nuevo servicio para el freelancer autenticado.

    - CA1: solo freelancers verificados pueden crear servicios (JWT + rol + verificado)
    - CA2: recibe título, descripción, categoría, imágenes (1-5), tiempo de entrega y precios
    - CA3: título máx 100 caracteres, descripción máx 1200 caracteres
    - CA4: el servicio se crea en estado 'activo'
    - CA5: imágenes subidas a Cloudinary
    - CA6: categoria_id debe pertenecer a las 8 categorías del sistema
    - CA7: servicio visible en catálogo inmediatamente
    - CA8: máximo 10 servicios activos por freelancer
    """
    # CA2 — image count validation
    if len(imagenes) < 1 or len(imagenes) > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes subir entre 1 y 5 imágenes de ejemplo.",
        )

    # CA5 — upload each image to Cloudinary
    imagen_urls = []
    for img in imagenes:
        url = await upload_service_image(img)
        imagen_urls.append(url)

    service = service_service.create_service(
        db=db,
        user_id=current_user.id,
        titulo=titulo,
        descripcion=descripcion,
        categoria_id=categoria_id,
        precio_basico=precio_basico,
        precio_estandar=precio_estandar,
        precio_premium=precio_premium,
        tiempo_entrega=tiempo_entrega,
        imagen_urls=imagen_urls,
    )

    return _build_response(service)


@router.put(
    "/{service_id}",
    response_model=ServiceResponse,
    status_code=status.HTTP_200_OK,
    summary="Editar un servicio existente",
)
async def update_service(
    service_id: int,
    titulo: Optional[str] = Form(None, max_length=100),
    descripcion: Optional[str] = Form(None, max_length=1200),
    categoria_id: Optional[int] = Form(None),
    precio_basico: Optional[float] = Form(None, gt=0),
    precio_estandar: Optional[float] = Form(None, gt=0),
    precio_premium: Optional[float] = Form(None, gt=0),
    tiempo_entrega: Optional[int] = Form(None, ge=1),
    keep_images: Optional[List[str]] = Form(None),
    new_images: Optional[List[UploadFile]] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Edita un servicio existente del freelancer autenticado.

    - CA1: solo el propietario del servicio puede editarlo
    - CA2: todos los campos son opcionales; solo los enviados se actualizan
    - CA3: los cambios se reflejan de inmediato en el catálogo
    - CA4: se bloquea si hay pedidos en estado 'en_progreso'
    - CA5: keep_images = URLs a conservar; new_images = archivos nuevos a subir
    - CA6: los pedidos existentes no se ven afectados por cambios de precio
    """
    # CA5 — upload new images if provided
    new_image_urls = []
    if new_images:
        for img in new_images:
            url = await upload_service_image(img)
            new_image_urls.append(url)

    service = service_service.update_service(
        db=db,
        service_id=service_id,
        current_user_id=current_user.id,
        titulo=titulo,
        descripcion=descripcion,
        categoria_id=categoria_id,
        precio_basico=precio_basico,
        precio_estandar=precio_estandar,
        precio_premium=precio_premium,
        tiempo_entrega=tiempo_entrega,
        keep_images=keep_images,
        new_image_urls=new_image_urls if new_image_urls else None,
    )

    return _build_response(service)


def _build_response(service) -> ServiceResponse:
    return ServiceResponse(
        id=service.id,
        user_id=service.user_id,
        titulo=service.titulo,
        descripcion=service.descripcion,
        categoria_id=service.categoria_id,
        precio_basico=float(service.precio_basico) if service.precio_basico else None,
        precio_estandar=float(service.precio_estandar) if service.precio_estandar else None,
        precio_premium=float(service.precio_premium) if service.precio_premium else None,
        tiempo_entrega=service.tiempo_entrega,
        imagenes=service.imagenes,
        estado=service.estado,
        fecha_creacion=service.fecha_creacion.isoformat(),
    )
