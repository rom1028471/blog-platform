from pydantic import BaseModel, UUID4
from datetime import datetime

class ImageResponse(BaseModel):
    id: UUID4
    name: str
    type: str
    created_at: datetime

    class Config:
        from_attributes = True