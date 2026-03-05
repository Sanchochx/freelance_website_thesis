from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.schemas.user import (
    ClientProfileResponse,
    ClientProfileUpdateRequest,
    FreelancerProfileResponse,
    FreelancerProfileUpdateRequest,
    ProfileUpdateResponse,
    UserResponse,
)
from app.services import user_service
from app.utils.cloudinary import upload_avatar as cloudinary_upload_avatar

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


@router.put("/{user_id}/profile", response_model=ProfileUpdateResponse)
def update_profile(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update the authenticated user's profile.

    CA1: Freelancer can edit bio, habilidades, portafolio.
    CA2: Client can edit nombre and empresa.
    CA3: Email cannot be changed through this endpoint.
    CA5: Changes are saved and reflected immediately.
    CA7: Only the owner can edit their profile (JWT user_id must match path user_id).
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes editar el perfil de otro usuario",
        )

    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Usa PUT /users/{user_id}/profile/freelancer o /client según tu rol",
    )


@router.put("/{user_id}/profile/freelancer", response_model=ProfileUpdateResponse)
def update_freelancer_profile(
    user_id: int,
    body: FreelancerProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update freelancer-specific profile fields.

    CA1: bio, habilidades, portafolio. CA3: email excluded. CA7: own user only.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes editar el perfil de otro usuario",
        )
    if current_user.rol != "freelancer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Este endpoint es solo para freelancers",
        )

    updated = user_service.update_freelancer_profile(db, user_id, body)
    return ProfileUpdateResponse(
        data=UserResponse.model_validate(updated),
    )


@router.put("/{user_id}/profile/client", response_model=ProfileUpdateResponse)
def update_client_profile(
    user_id: int,
    body: ClientProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update client-specific profile fields.

    CA2: nombre, empresa. CA3: email excluded. CA7: own user only.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes editar el perfil de otro usuario",
        )
    if current_user.rol != "client":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Este endpoint es solo para clientes",
        )

    updated = user_service.update_client_profile(db, user_id, body)
    return ProfileUpdateResponse(
        data=UserResponse.model_validate(updated),
    )


@router.post("/{user_id}/avatar", response_model=ProfileUpdateResponse)
async def upload_avatar(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload a new profile picture.

    CA4: Image uploaded to Cloudinary; resulting secure_url stored in users.avatar_url.
    CA6: Returns 400 if file > 5 MB or format not JPG/PNG/WEBP.
    CA7: Only the owner can change their avatar.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes editar el perfil de otro usuario",
        )

    avatar_url = await cloudinary_upload_avatar(file)
    updated = user_service.update_avatar_url(db, user_id, avatar_url)
    return ProfileUpdateResponse(
        data=UserResponse.model_validate(updated),
    )
