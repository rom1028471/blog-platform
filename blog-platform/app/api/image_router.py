# backend/app/api/image_router.py
from fastapi import APIRouter, UploadFile, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from uuid import UUID
from ..schemas.image import ImageResponse
from ..schemas.user import UserResponse
from ..services.image_service import save_image, get_image, delete_image
from ..dependencies import get_current_user, get_db

router = APIRouter(prefix="/images")

@router.post("/", response_model=ImageResponse, status_code=201)
async def upload_image(
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    return save_image(db, file)

@router.get("/{image_id}")
async def get_image_by_id(
    image_id: UUID,
    db: Session = Depends(get_db)
):
    image = get_image(db, image_id)
    headers = {
        "Content-Type": image.type,
        "Content-Disposition": f"inline; filename={image.name}"
    }
    return StreamingResponse(
        iter([image.data]),
        media_type=image.type,
        headers=headers
    )

@router.delete("/{image_id}")
async def delete_image_by_id(
    image_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    delete_image(db, image_id)
    return {"message": "Image deleted"}