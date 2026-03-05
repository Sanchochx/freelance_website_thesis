from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import ClientProfileResponse, FreelancerProfileResponse
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}/profile")
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """Public user profile — no auth required (CA2/CA5). Returns freelancer or client profile based on role."""
    user = db.query(User.rol).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    if user.rol == "freelancer":
        data = user_service.get_freelancer_profile(db, user_id)
        return FreelancerProfileResponse(**data)
    elif user.rol == "client":
        data = user_service.get_client_profile(db, user_id)
        return ClientProfileResponse(**data)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil no disponible para este rol")
