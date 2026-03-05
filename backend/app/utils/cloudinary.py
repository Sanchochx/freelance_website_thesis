import cloudinary
import cloudinary.uploader
from fastapi import HTTPException, UploadFile, status

from app.config import settings

# Configure Cloudinary once at import time
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
)

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


async def upload_avatar(file: UploadFile) -> str:
    """
    Upload an avatar image to Cloudinary and return the secure_url.

    CA4: stores the resulting Cloudinary URL.
    CA6: raises 400 if format is unsupported or file exceeds 5 MB.
    """
    # Validate MIME type (CA6)
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de imagen no soportado. Solo se aceptan JPG, PNG y WEBP.",
        )

    # Read file content to check size (CA6)
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La imagen supera el tamaño máximo permitido de 5 MB.",
        )

    # Upload to Cloudinary
    result = cloudinary.uploader.upload(
        contents,
        folder="freelanceusta/avatars",
        resource_type="image",
    )

    return result["secure_url"]
