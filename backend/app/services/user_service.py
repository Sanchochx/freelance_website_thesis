from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.order import Order
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

    # 5. Assemble freelancer response dict
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


def get_client_profile(db: Session, user_id: int) -> dict:
    """Return public profile for a client. Raises 404 if not found. (US-006)"""

    # 1. Fetch client (freelancers can also be clients, but rol must be 'client')
    user = db.query(User).filter(User.id == user_id, User.rol == "client").first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado",
        )

    # 2. Completed orders as client — CA2, CA4 (no montos exposed)
    completed_orders_raw = (
        db.query(
            Order.id,
            Order.estado,
            Order.fecha_creacion,
            Service.titulo.label("service_titulo"),
            User.nombre.label("freelancer_nombre"),
        )
        .outerjoin(Service, Service.id == Order.service_id)
        .outerjoin(User, User.id == Order.freelancer_id)
        .filter(Order.client_id == user_id, Order.estado == "completado")
        .all()
    )

    # 3. Total orders as client (all states) — CA4
    total_contratados = (
        db.query(func.count(Order.id))
        .filter(Order.client_id == user_id)
        .scalar()
        or 0
    )
    total_completados = len(completed_orders_raw)

    # 4. Reviews received by this client (from freelancers) — CA3
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

    # 5. Average rating as client — CA1
    avg_rating_raw = (
        db.query(func.avg(Review.rating))
        .filter(Review.reviewed_id == user_id)
        .scalar()
    )
    avg_rating = float(avg_rating_raw) if avg_rating_raw is not None else None

    # 6. Assemble client response dict — CA6: no email, no wallet_balance
    return {
        "id": user.id,
        "nombre": user.nombre,
        "empresa": user.empresa,
        "avatar_url": user.avatar_url,
        "fecha_registro": user.fecha_registro.isoformat() if user.fecha_registro else None,
        "avg_rating": avg_rating,
        "total_reviews": len(reviews_raw),
        "total_contratados": total_contratados,
        "total_completados": total_completados,
        "pedidos_completados": [
            {
                "id": o.id,
                "service_titulo": o.service_titulo,
                "freelancer_nombre": o.freelancer_nombre or "Usuario eliminado",
                "estado": o.estado,
                "fecha_creacion": o.fecha_creacion.isoformat() if o.fecha_creacion else None,
            }
            for o in completed_orders_raw
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
