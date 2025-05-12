from pydantic import BaseModel, UUID4

class TagResponse(BaseModel):
    id: UUID4
    text: str
    
    class Config:
        from_attributes = True