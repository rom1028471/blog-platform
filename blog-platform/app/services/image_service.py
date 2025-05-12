# backend/app/services/image_service.py
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile, status
from ..models.image import Image
from ..exceptions import FileStorageException

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/gif"}

def save_image(db: Session, file: UploadFile) -> Image:
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise FileStorageException("Invalid file type")
    
    try:
        image_data = file.file.read()
        new_image = Image(
            name=file.filename,
            type=file.content_type,
            data=image_data
        )
        db.add(new_image)
        db.commit()
        db.refresh(new_image)
        return new_image
    except Exception as e:
        raise FileStorageException(f"Error saving image: {str(e)}")

def get_image(db: Session, image_id: UUID) -> Image:
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    return image

def delete_image(db: Session, image_id: UUID) -> None:
    image = get_image(db, image_id)
    db.delete(image)
    db.commit()