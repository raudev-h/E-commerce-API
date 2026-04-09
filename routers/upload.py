from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from core.config import settings
from core import security
from models import User
from typing import Annotated
import cloudinary
import cloudinary.uploader

router = APIRouter(prefix="/upload", tags=["upload"])

cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
)


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    current_admin: Annotated[User, Depends(security.get_current_admin)] = None,
):
    if file.content_type not in ("image/jpeg", "image/png", "image/webp"):
        raise HTTPException(status_code=400, detail="Only JPEG, PNG and WebP images are allowed")

    contents = await file.read()
    result = cloudinary.uploader.upload(contents, folder="ecommerce/products")
    return {"url": result["secure_url"]}
