from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import FreelancerProfileResponse
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}/profile", response_model=FreelancerProfileResponse)
def get_freelancer_profile(user_id: int, db: Session = Depends(get_db)):
    """Public freelancer profile — no auth required (CA2)."""
    return user_service.get_freelancer_profile(db, user_id)
