from fastapi import HTTPException, status
from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.models.review import Review
from app.models.service import Service
from app.models.user import User


def get_freelancer_profile(db: Session, user_id: int) -> dict:
    """Return full public profile for a freelancer. Raises 404 if not found."""

    # 1. Fetch freelancer
    user = db.query(User).filter(User.id == user_id, User.rol == "freelancer").first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Freelancer no encontrado",
        )

    # 2. Active services
    services = (
        db.query(Service)
        .filter(Service.user_id == user_id, Service.estado == "activo")
        .all()
    )

    # 3. Reviews with reviewer name (LEFT JOIN handles deleted reviewers)
    reviews_raw = (
        db.query(
            Review.id,
            Review.rating,
            Review.comentario,
            Review.fecha,
            User.nombre.label("reviewer_nombre"),
        )
        .outerjoin(User, User.id == Review.reviewer_id)
        .filter(Review.reviewed_id == user_id)
        .all()
    )

    # 4. Average rating (None when no reviews — CA6/CA7)
    avg_rating_raw = (
        db.query(func.avg(Review.rating))
        .filter(Review.reviewed_id == user_id)
        .scalar()
    )
    avg_rating = float(avg_rating_raw) if avg_rating_raw is not None else None

    # 5. Assemble response dict
    return {
        "id": user.id,
        "nombre": user.nombre,
        "email": user.email,
        "carrera": user.carrera,
        "semestre": user.semestre,
        "avatar_url": user.avatar_url,
        "bio": user.bio,
        "habilidades": user.habilidades,
        "portafolio": user.portafolio,
        "badges": user.badges,
        "verificado": user.verificado,
        "fecha_registro": user.fecha_registro.isoformat() if user.fecha_registro else None,
        "avg_rating": avg_rating,
        "total_reviews": len(reviews_raw),
        "services": [
            {
                "id": s.id,
                "titulo": s.titulo,
                "descripcion": s.descripcion,
                "precio_basico": float(s.precio_basico) if s.precio_basico is not None else None,
                "precio_estandar": float(s.precio_estandar) if s.precio_estandar is not None else None,
                "precio_premium": float(s.precio_premium) if s.precio_premium is not None else None,
                "tiempo_entrega": s.tiempo_entrega,
                "imagenes": s.imagenes,
                "categoria_id": s.categoria_id,
            }
            for s in services
        ],
        "reviews": [
            {
                "id": r.id,
                "reviewer_nombre": r.reviewer_nombre or "Usuario eliminado",
                "rating": float(r.rating),
                "comentario": r.comentario,
                "fecha": r.fecha.isoformat() if r.fecha else None,
            }
            for r in reviews_raw
        ],
    }
