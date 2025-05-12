from pydantic import BaseModel

class RoleResponse(BaseModel):
    name: str
    
    class Config:
        from_attributes = True